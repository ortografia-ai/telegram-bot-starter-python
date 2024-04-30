from functools import wraps
import logging

from bot.models import UserRole
from bot.dataaccess.users import get_user


# Decorator to restrict access to certain commands based on user role
def restricted_below(user_role: UserRole):
    def decorator(func):
        @wraps(func)
        async def wrapped(update, context, *args, **kwargs):
            user_id = update.effective_user.id
            user = get_user(user_id)
            if not user or user.user_role > user_role:
                logging.info(f"Unauthorized! Access denied for user_id: {user_id}.")
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="You are not authorized to use this command.",
                )
                return
            return await func(update, context, *args, **kwargs)

        return wrapped

    return decorator
