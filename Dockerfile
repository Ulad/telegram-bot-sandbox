# UV in Docker docs: https://docs.astral.sh/uv/guides/integration/docker/#getting-started

FROM python:3.13-alpine AS base
# APP_DIR - name of the root dir in Docker where the project will be installed.
# SRC_DIR - name of the dir with the main code. Must match the name in the project.
ARG APP_DIR=/app
ARG SRC_DIR=bot
WORKDIR ${APP_DIR}
LABEL authors="Levchenko V.V"
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.7.15 /uv /bin/uv
ENV UV_PYTHON_DOWNLOADS=0 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

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
