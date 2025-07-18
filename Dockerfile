FROM python:3.12-slim AS builder

WORKDIR /app

ENV PIP_PROGRESS_BAR=off
ENV PIP_NO_COLOR=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --disable-pip-version-check mcp==1.2.0
RUN pip install --no-cache-dir --disable-pip-version-check pydantic==2.8.2
RUN pip install --no-cache-dir --disable-pip-version-check python-dateutil==2.9.0
RUN pip install --no-cache-dir --disable-pip-version-check tzdata
RUN pip install --no-cache-dir --disable-pip-version-check starlette==0.39.0
RUN pip install --no-cache-dir --disable-pip-version-check uvicorn==0.32.0

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src/ ./src
COPY pyproject.toml README.md ./

ENV PIP_PROGRESS_BAR=off
ENV PIP_NO_COLOR=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --disable-pip-version-check -e .

EXPOSE 8000

CMD ["python", "-m", "temporal_awareness_mcp.http_main"]