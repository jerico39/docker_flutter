from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://vote_user:vote_pass@db:3306/vote_app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# テンプレート
templates = Jinja2Templates(directory="templates")

# SQLAlchemy モデル
class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    option = Column(String(50), unique=True)
    count = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

# Pydantic リクエスト
class VoteRequest(BaseModel):
    option: str

# API: 投票一覧
@app.get("/votes")
def get_votes():
    db = SessionLocal()
    votes = db.query(Vote).all()
    db.close()
    return [{"option": v.option, "count": v.count} for v in votes]

# API: 投票
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

# HTML ダッシュボード
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    db = SessionLocal()
    votes = db.query(Vote).all()
    db.close()
    # votes を辞書リストに変換してテンプレートに渡す
    votes_data = [{"option": v.option, "count": v.count} for v in votes]
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "votes": votes_data}
    )
