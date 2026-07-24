from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Case
from routers.events.keyboards.join_group_k.states import WelcomeKeyboard

async def test(**kwargs):
    pass

async def check_user(**kwargs):
    pass

welcome_window = Window(
    Const("Привет! Нажми на кнопку для разблокировки"),
    Button(
        Const("Разблокировать"),
        id="check_user",
        on_click=check_user
    ),
    state=WelcomeKeyboard.welcome_s,
    getter=test
)

check_welcome_window = Window(
    Case({
        True:Const("Поздравляю со вступлением!"),
        False:Const("Ты не заполнил таблицу"),
    },
        selector="is_check"
    ),  # just a constant text
    Button(Const("Разблокировать"), id="check_user"),  # button with text and id
    state=WelcomeKeyboard.checkout_s,
)

