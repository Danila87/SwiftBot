import asyncio

from aiogram import Router, Bot
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.chat_member_updated import ChatMemberUpdated
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER

from config import NOT_ACCESS_USER_PERMISSIONS, ACCESS_USER_PERMISSIONS, TG_GROUP_ID

from .callback_factorys import CheckUserData
from .middlewares import NewUserMiddleware

from common_lib.google_sheet_client import swift_table_client

events_router = Router()
events_router.chat_member.middleware(NewUserMiddleware())


@events_router.callback_query(CheckUserData.filter())
async def check_user(
    callback: CallbackQuery,
    callback_data: CheckUserData,
    bot: Bot
):
    """
    Проверка вступившего пользователя на выполнение условий
    """

    if callback.from_user.id != callback_data.user_id:
        return

    is_valid = True
    message = ""

    users_df = swift_table_client.get_users()

    if (
        cur_user := users_df[users_df["Имя пользователя через @ (смотри свой профиль)"] == f"@{callback_data.username}"]
    ).empty:
        is_valid = False
        message += "Не выполнены следующие условия:\n- Заполнено поле 'Имя пользователя через @'."

    if not cur_user.empty:
        if not cur_user[["Никнейм в телеге", "Имя пользователя через @ (смотри свой профиль)", "Район обитания", "Метро обитания (ближайшее)"]].squeeze().all():
            is_valid = False
            message += "\n- Заполнены все необходимые поля"

    if is_valid:
        await callback.message.edit_text("Вы заполнили таблицу. Доступ открыт!")
        await bot.restrict_chat_member(
            chat_id=TG_GROUP_ID,
            user_id=callback_data.user_id,
            permissions=ACCESS_USER_PERMISSIONS
        )
        await asyncio.sleep(5)
        await callback.message.delete()

    else:
        message += "\n\nСсылка на таблицу - https://docs.google.com/spreadsheets/d/1jStirZh3ve0CtwyH6GCBpwfXwhlMTmyUBGzFBOikXHY/edit?gid=0&clckid=57df63e4#gid=0"
        builder = InlineKeyboardBuilder()
        builder.button(
            text="Проверить",
            callback_data=CheckUserData(
                user_id=callback_data.user_id,
                username=callback_data.username,
            )
        )

        try:
            await callback.message.edit_text(
                text=message,
                reply_markup=builder.as_markup()
            )
        except Exception as e:
            pass

        await callback.answer()

@events_router.chat_member(
    ChatMemberUpdatedFilter(
        IS_NOT_MEMBER >> IS_MEMBER
    )
)
async def invite_user(
    event: ChatMemberUpdated,
    bot: Bot,
    **kwargs
):
    """
    Ивент "Приглашение/Вступление пользователя"
    """
    message = (
        f"\n\n1) Заполнить таблицу https://docs.google.com/spreadsheets/d/1jStirZh3ve0CtwyH6GCBpwfXwhlMTmyUBGzFBOikXHY/edit?gid=0&clckid=57df63e4#gid=0."

    )
    await bot.restrict_chat_member(
        chat_id=event.chat.id,
        user_id=event.new_chat_member.user.id,
        permissions=NOT_ACCESS_USER_PERMISSIONS
    )

    builder = InlineKeyboardBuilder()
    builder.button(
            text="Проверить ✅",
            callback_data=CheckUserData(
                user_id=event.new_chat_member.user.id,
                username=event.new_chat_member.user.username,
            )
    )
    if (
        admin_user := event.from_user
    ).id == (
        invited_user := event.new_chat_member.user
    ).id:
         await event.answer(
             text=f"Приветствую @{invited_user.username} в нашем уютном клубе!{message}",
             parse_mode=ParseMode.HTML,
             reply_markup=builder.as_markup()
         )
    else:
        await event.answer(
            text=f"Пользователь @{admin_user.username} пригласил @{invited_user.username}!{message}",
            parse_mode=ParseMode.HTML,
            reply_markup=builder.as_markup()
        )


@events_router.chat_member(
    ChatMemberUpdatedFilter(
        IS_MEMBER >> IS_NOT_MEMBER
    )
)
async def left_user(event: ChatMemberUpdated):
    """
    Ивент "Удаление/выход пользователя"
    """

    if (
        admin_user := event.from_user
    ).id == (
        invited_user := event.new_chat_member.user
    ).id:
        await event.answer(
            text=f"Пользователь @{invited_user.username} вышел из чата!",
            parse_mode=ParseMode.HTML,
        )
    else:
        await event.answer(
            text=f"Пользователь @{admin_user.username} исключил @{invited_user.username}!",
            parse_mode=ParseMode.HTML,
        )
