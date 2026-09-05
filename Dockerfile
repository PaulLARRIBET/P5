FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv sync --frozen --no-dev

COPY models ./models
COPY sql ./sql

ENV PYTHONPATH=/app/src

EXPOSE 7860

CMD ["uv", "run", "uvicorn", "p5.app:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "7860"]