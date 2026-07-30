import pandas as pd

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from common_lib.google_sheet_client import swift_table_client

from routers.admin_commands.middlewares import CheckAdminMiddleware

from config import ADMIN_USERS, TG_GROUP_ID, TG_TRADE_GROUP_ID

from common_lib.telethon_client import telethon_client

admin_commands_router = Router()
admin_commands_router.message.middleware(CheckAdminMiddleware(
    admin_users_ids=ADMIN_USERS
))


def normalize_series_username(
    usernames: pd.Series
) -> set:
    data = usernames[~usernames.isin(["", "none", "nan"])].dropna()
    data = data.apply(lambda username: f"@{username.lower().strip()}")

    return set(data)


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


@admin_commands_router.message(Command("get_sheet_report"))
async def get_sheet_report(
    message: Message,
):

    users_result = {
        "in_group_not_table_users": {
            "data": [],
            "message": "Пользователи которые есть в группе но нет в таблице:"
        },
        "not_group_in_table_users": {
            "data": [],
            "message": "Пользователи которые есть в таблице но нет в группе:"
        }
    }

    main_group_users_df = await telethon_client.get_chat_users(
        chat_id=TG_GROUP_ID
    )
    main_group_users_set = normalize_series_username(
        usernames=main_group_users_df["username"]
    )

    sheet_users_df = swift_table_client.get_users()
    sheet_users_set = normalize_series_username(
        usernames=sheet_users_df["Имя пользователя через @ (смотри свой профиль)"].apply(lambda username: username.replace("@", ""))
    )

    users_result["in_group_not_table_users"]["data"] = list(main_group_users_set - sheet_users_set)
    users_result["not_group_in_table_users"]["data"] = list(sheet_users_set - main_group_users_set)

    for users_type in users_result.values():
        await message.answer(
            f"{users_type['message']} {', '.join(users_type['data']) if users_type['data'] else 'Не обнаружено'}"
        )

    await message.answer(
        "Ссылка на таблицу - https://clck.ru/3T2tEh"
    )


@admin_commands_router.message(Command("get_trade_report"))
async def get_trade_report(
    message: Message,
):
    main_group_users_df = await telethon_client.get_chat_users(
        chat_id=TG_GROUP_ID
    )
    main_group_users_set = normalize_series_username(
        usernames=main_group_users_df["username"]
    )

    trade_group_users_df = await telethon_client.get_chat_users(
        chat_id=TG_TRADE_GROUP_ID
    )
    trade_group_users_set = normalize_series_username(
        usernames=trade_group_users_df["username"]
    )

    trade_group_not_join_users = list(main_group_users_set - trade_group_users_set)

    await message.answer(
        f"Пользователи которые есть в основной группе но нет в барахолке: {', '.join(trade_group_not_join_users) if trade_group_not_join_users else 'Не обнаружено'}"
    )