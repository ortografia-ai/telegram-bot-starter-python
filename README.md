# telegram-bot-starter-python

This is a telegram bot starter repository with the following characteristics:

- uv dependency management
- ruff linting and formatting
- pre-commit hooks configured for:
    - ruff linting and formatting
    - uv checks
    - mypy type checking
- SQLModel ORM with SQLite configured already
- alembic migrations
- pydantic models
- docker support with a lean multi-stage image build process
- it comes with a `User` database model and authorization to restrict the use of certain commands to some users.

The bot comes with four commands:

1. `/start`: This simply prints a message.
2. `/commands`: This prints the list of commands available.
3. `/helloworld`: This command registers the user sending the message in database and responds with a simple message.
4. `/restrictedhelloworld`: This command sends a simple message if the user is registered and is above ADMIN.

## Installation

1. Clone this repository
2. Install dependencies by running `make install-dev` or `uv sync --all-extras`
3. Install the pre-commit hooks by running `uv run pre-commit install`
4. Run the database migrations by running `make migrate`

## Create and run the bot

1. Create the Telegram bot: To create a telegram bot, you need to register it with Telegram and obtain a token. Follow these [instructions](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).
2. Get your Telegram ID: After obtaining the token, get your own Telegram ID. There is no official way to do it but you can try to follow these [instructions](https://www.alphr.com/telegram-find-user-id/).
3. With these two, copy the `.env.example` to a `.env` file and fill it with your data.
4. Build the docker image by running `docker compose build`
5. Run the service with docker by running `docker compose up`
6. You are all set now! Look for your bot in Telegram and try the commands.

