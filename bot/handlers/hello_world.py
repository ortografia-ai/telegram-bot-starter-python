from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from bot.auth import restricted_below
from bot.dataaccess.users import get_user, create_or_update_user
from bot.models import User, UserRole


async def _hello_world(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user = update.effective_user
    if not telegram_user or telegram_user.is_bot:
        return
    user = get_user(telegram_user.id)

    if not user:
        user = create_or_update_user(
            User(
                id=telegram_user.id,
            )
        )

    if not update.effective_chat:
        return
    response = "Hello, world! You are now registered in the system."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return


def hello_world_handler(command: str) -> CommandHandler:
    handler = CommandHandler(command, _hello_world)
    return handler


@restricted_below(UserRole.ADMIN)
async def _restricted_hello_world(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not update.effective_chat:
        return
    response = "Hello, world! You are authorized."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return


def restricted_hello_world_handler(command: str) -> CommandHandler:
    handler = CommandHandler(command, _restricted_hello_world)
    return handler
