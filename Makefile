.PHONY: install
install:
	poetry install

.PHONY: install-dev
install-dev:
	poetry install --all-extras

.PHONY: run
run:
	poetry run python -m bot.app

.PHONY: migrate
migrate:
	poetry run python -m alembic upgrade head

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
	poetry run alembic revision --autogenerate -m "$(message)"
