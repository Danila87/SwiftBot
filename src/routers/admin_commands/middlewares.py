from typing import Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Optional, List

class CheckAdminMiddleware(BaseMiddleware):
    """
    Мидварь для отсеивания не админов
    """
    def __init__(
        self,
        admin_users_ids: Optional[List[int]]
    ):
        self._admin_users_ids = admin_users_ids

    async def __call__(
        self,
        handler: Callable,
        event: Message,
        data: Dict,
    ):
        tg_user = await data["bot"].get_chat_member(
            chat_id=data["event_context"].chat_id,
            user_id=data["event_context"].user_id
        )
        if tg_user.status not in ("creator", "administrator"):
            await event.delete()
            return

        return await handler(event, data)