FROM public.ecr.aws/docker/library/python:3.12-slim-bookworm AS base

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

# Copy the application into the container.
COPY bot ./bot

# Install the application dependencies.
RUN uv sync --frozen --no-cache --no-dev

ENTRYPOINT ["uv", "run", "-m", "bot.app"]