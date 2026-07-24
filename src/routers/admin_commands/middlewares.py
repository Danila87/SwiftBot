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
        data: Dict
    ):
        if not self._admin_users_ids:
            return await handler(event, data)

        if event.from_user.id not in self._admin_users_ids:
            await event.delete()
            return

        return await handler(event, data)