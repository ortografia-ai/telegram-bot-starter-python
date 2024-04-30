import html
import json
import logging
import traceback

from telegram import Update, BotCommand
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.constants import (
    BOT_COMMANDS,
    START_COMMAND,
    COMMANDS_COMMAND,
    HELLO_WORLD_COMMAND,
    RESTRICTED_HELLO_WORLD_COMMAND,
)
from bot.settings import get_settings
from bot.handlers.hello_world import hello_world_handler, restricted_hello_world_handler


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = get_settings()
    # Log the error before we do anything else, so we can see it even if something
    # breaks.
    logging.error("Exception while handling an update:", exc_info=context.error)
    if isinstance(update, Update) and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Something went wrong. Please contact the developer.",
        )
    # traceback.format_exception returns the usual python message about an
    # exception, but as a list of strings rather than a single string, so we
    # have to join them together.
    error_traceback = context.error.__traceback__ if context.error else None
    tb_list = traceback.format_exception(None, context.error, error_traceback)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what
    # happened. You might need to add some logic to deal with messages longer than
    # the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = "
        f"{html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=settings.developer_chat_id, text=message, parse_mode=ParseMode.HTML
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hello! I am a bot that can help you with some tasks.",
        )


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat:
        message = "\n".join(f"/{command[0]} - {command[1]}" for command in BOT_COMMANDS)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat:
        commands_list = "\n".join(
            f"/{command[0]} - {command[1]}" for command in BOT_COMMANDS
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "I'm sorry but I don't understand that command. Here is the list of "
                f"available commands:\n{commands_list}"
            ),
        )


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [BotCommand(*command) for command in BOT_COMMANDS]
    )


if __name__ == "__main__":
    settings = get_settings()
    application = (
        ApplicationBuilder()
        .token(settings.telegram_bot_token)
        .post_init(post_init)
        .build()
    )

    start_handler = CommandHandler(START_COMMAND, start)
    commands_handler = CommandHandler(COMMANDS_COMMAND, commands)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # Register handlers
    application.add_handler(start_handler)
    application.add_handler(commands_handler)
    application.add_handler(hello_world_handler(HELLO_WORLD_COMMAND))
    application.add_handler(
        restricted_hello_world_handler(RESTRICTED_HELLO_WORLD_COMMAND)
    )
    application.add_handler(unknown_handler)

    # Register error handler
    application.add_error_handler(error_handler)

    application.run_polling()
