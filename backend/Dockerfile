
FROM python:3.11-slim

WORKDIR /app

# MySQL接続に必要な依存パッケージを追加
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc

# cryptographyをインストール（MySQL認証のために必要）
RUN pip install --no-cache-dir cryptography

# 依存関係インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
