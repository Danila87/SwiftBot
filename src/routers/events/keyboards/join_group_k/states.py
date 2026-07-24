from aiogram.filters.state import StatesGroup, State

class WelcomeKeyboard(StatesGroup):
    welcome_s = State()
    checkout_s = State()