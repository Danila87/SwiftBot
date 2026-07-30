import pandas as pd
from telethon import TelegramClient
from config import TG_API_ID, TG_API_HASH

class TelethonClient:
    def __init__(
        self,
        api_id: int,
        api_hash: str,
    ):
        self._api_id = api_id
        self._api_hash = api_hash
        self._client = TelegramClient(
            "Danila87",
            api_id=api_id,
            api_hash=api_hash,
        )

    async def get_chat_users(
        self,
        chat_id: int,
    ) -> pd.DataFrame:
        """
        Получить пользователей группы в виде датафрейма
        :param chat_id: id чата. Обязательно с -100 в начале
        :return: pd.DataFrame - список пользователей чата
        """
        async with self._client as client:
            user_list = []
            users = await client.get_participants(chat_id)
            for user in users:
                user_list.append(user.to_dict())

        return pd.DataFrame(user_list)

telethon_client = TelethonClient(
    api_id=TG_API_ID,
    api_hash=TG_API_HASH,
)