# UV in Docker docs: https://docs.astral.sh/uv/guides/integration/docker/#getting-started
#FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
FROM python:3.13-alpine AS base
ARG APP_DIR=/app
ARG SRC_DIR=bot
WORKDIR ${APP_DIR}
LABEL authors="Levchenko V.V"

FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.7.15 /uv /bin/uv
ENV UV_PYTHON_DOWNLOADS=0 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable

COPY ${SRC_DIR} ${SRC_DIR}
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable


FROM base
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy ONLY the virtual environment and bot folder
COPY --from=builder --chown=appuser:appgroup ${APP_DIR}/.venv ./.venv
COPY --from=builder --chown=appuser:appgroup ${APP_DIR}/${SRC_DIR} ${SRC_DIR}

ENV PATH="${APP_DIR}/.venv/bin:$PATH"

USER appuser

CMD ["python", "-m", "bot.main"]
