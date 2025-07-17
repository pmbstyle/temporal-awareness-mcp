FROM python:3.12-slim AS builder

ARG POETRY_VERSION=1.8.2
WORKDIR /app

RUN pip install "poetry==${POETRY_VERSION}"

RUN poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY src/ ./src
COPY pyproject.toml poetry.lock README.md ./

RUN /app/.venv/bin/pip install -e .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "-m", "temporal_awareness_mcp.http_main"]