FROM python:3.12-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY app.py .
COPY quiz_explorer/ quiz_explorer/
COPY data/ data/

EXPOSE 8501

CMD ["uv", "run", "--no-dev", "streamlit", "run", "app.py", "--server.address=0.0.0.0"]
