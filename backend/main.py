from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

DATABASE_URL = "mysql+pymysql://vote_user:vote_pass@db:3306/vote_app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

#テンプレート設定(HTML ダッシュボード)
templates = Jinja2Templates(directory="templates")

# DB接続関数
def get_db():
    return mysql.connector.connect(
        host="mysql_vote_db",        # docker-compose のサービス名
        user="vote_user",
        password="vote_pass", # MySQL root パスワード
        database="vote_app"   # データベース名
    )


# Flutter からアクセスを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    option = Column(String(50))
    count = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

class VoteRequest(BaseModel):
    option: str

@app.get("/votes")
def get_votes():
    db = SessionLocal()
    votes = db.query(Vote).all()
    db.close()
    return [{"option": v.option, "count": v.count} for v in votes]

@app.post("/vote")
def vote(req: VoteRequest):
    db = SessionLocal()
    vote = db.query(Vote).filter(Vote.option == req.option).first()
    if vote:
        vote.count += 1
    else:
        vote = Vote(option=req.option, count=1)
        db.add(vote)
    db.commit()
    db.close()
    return {"message": f"Vote for {req.option} counted!"}


class VoteRequest(BaseModel):
    option: str

@app.post("/vote")
def vote(req: VoteRequest):
    # 本来はDBに保存などする
    print(f"投票: {req.option}")
    return {"message": f"{req.option} に投票しました"}


#HTML ダッシュボード
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT `option`, count FROM votes")
    results = cursor.fetchall()
    db.close()
    return templates.TemplateResponse("dashboard.html", {"request": request, "votes": results})

