FROM python:3.11-slim

ENV PORT=50051 \
    MODEL_PATH=/app/models/model.pkl \
    MODEL_VERSION=v1.0.0

WORKDIR /app

COPY . .

RUN apt update && \
    apt install curl -y && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

RUN /root/.local/bin/uv self update && \
    /root/.local/bin/uv sync --no-cache

EXPOSE 50051

CMD ["/root/.local/bin/uv", "run", "main.py"]
