.PHONY: install
install:
	uv sync

.PHONY: install-dev
install-dev:
	uv sync --all-extras

.PHONY: run
run:
	uv run -m bot.app

.PHONY: migrate
migrate:
	uv run -m alembic upgrade head

.PHONY: run-docker-detached
run-docker-detached:
	docker compose build
	docker compose up -d

.PHONY: run-docker
run-docker:
	docker compose build
	docker compose up

.PHONY: stop-docker
stop-docker:
	docker compose down

# Autogenerate migrations that receives message as command line argument
# Example: make autogen-migrations message="create table users"
.PHONY: autogen-migrations
autogen-migrations:
	uv run alembic revision --autogenerate -m "$(message)"
