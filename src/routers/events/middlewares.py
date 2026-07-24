from typing import Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import ChatMemberUpdated

from common_lib.google_sheet_client import swift_table_client

from config import TG_TRADE_GROUP_ID

class NewUserMiddleware(BaseMiddleware):
    """
    Мидварь для отсеивания тех юзеров, которые уже есть в таблице, но добавлены в беседу повторно.
    Также отсеивает все события добавления/удаления в группу барахолку.
    """
    async def __call__(
        self,
        handler: Callable,
        event: ChatMemberUpdated,
        data: Dict
    ):
        if event.chat.id == int(TG_TRADE_GROUP_ID):
            return

        if event.new_chat_member.status == "member":
            users_df = swift_table_client.get_users()

            if not (
                cur_user := users_df[
                    users_df["Имя пользователя через @ (смотри свой профиль)"] == f"@{event.new_chat_member.user.username}"]
            ).empty:
                return

        return await handler(event, data)