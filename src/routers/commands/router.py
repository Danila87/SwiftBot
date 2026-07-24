import asyncio
import re

from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from config import ACCESS_USER_PERMISSIONS
from routers.commands.race import get_race_results

commands_router = Router()


@commands_router.message(Command("start"))
async def start_command(message: Message):
    await message.reply(
        text="Бем бем"
    )

@commands_router.message(Command("check_me"))
async def check_me_command(
    message: Message,
    bot: Bot
):
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        permissions=ACCESS_USER_PERMISSIONS
    )

@commands_router.message(Command("race"))
async def race_command(
    message: Message,
    command: CommandObject
):
    """
    Команда, которая позволяет вызвать другого участника на гонку
    """

    if not command.args:
        await message.reply("Выберите участника для вызова на гонку.\nПример команды \race @test_user")
        return

    called_users = re.findall(r"@[^@\s]+", command.args)

    race_message = await message.answer(
        text=f"Начинается заезд\n@{message.from_user.username} VS {command.args}"
    )

    await asyncio.sleep(5)

    await race_message.edit_text(
        text="Гонка началась!"
    )

    race_results = get_race_results(
        users=[message.from_user.username, *called_users]
    )

    message_text = "\n".join([f"{index}: {race}" for index, race in enumerate(race_results)])
    pass