FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
    build-base \
    curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync --frozen --no-cache

COPY . .

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_GATHER_USAGE_STATS=false

CMD ["uv", "run", "streamlit", "run", "app.py"]
