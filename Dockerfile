# ベースイメージにPython 3.10-slimを使用
FROM python:3.10-slim

WORKDIR /app

# 依存関係をインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# ソースをコピー
COPY src /app/src
COPY tests /app/tests
COPY app /app/app

# コンテナ起動時にStreamlitを起動する
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
