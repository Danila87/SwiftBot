from aiogram.filters.callback_data import CallbackData

class CheckUserData(CallbackData, prefix="check_user"):
    user_id: int
    username: str