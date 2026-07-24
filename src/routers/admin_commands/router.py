from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from common_lib.google_sheet_client import swift_table_client

from routers.admin_commands.middlewares import CheckAdminMiddleware

from config import ADMIN_USERS

admin_commands_router = Router()
admin_commands_router.message.middleware(CheckAdminMiddleware(
    admin_users_ids=ADMIN_USERS
))


@admin_commands_router.message(Command("check_users_login"))
async def check_users(
    message: Message,
):
    users_df = swift_table_client.get_users()
    users_without_username = users_df[
        (
            users_df["Имя пользователя через @ (смотри свой профиль)"] == '')
        | (
            users_df["Имя пользователя через @ (смотри свой профиль)"].isna()
           )
    ]

    users_without_username_message = f"У следующих пользователей отсутствует username в таблице: {', '.join(users_without_username['Никнейм в телеге'].values.tolist())}"

    await message.answer(users_without_username_message)


@admin_commands_router.message(Command("get_users_car_number"))
async def get_users_car_number(
    message: Message,
):
    pass
