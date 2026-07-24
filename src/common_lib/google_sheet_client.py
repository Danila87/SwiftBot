import pandas as pd

from gspread import service_account, Client
from typing import Optional, Dict
from config import SHEET_ID
from pathlib import Path

class GoogleSheetClient:
    def __init__(
        self,
        json_path: str,
        table_id: str
    ):
        self._table_client: Client = service_account(
            filename=json_path,
        )
        self._table = self._table_client.open_by_key(table_id)

    def get_data_from_table(
        self,
        sheet_name: str,
        header_border: Optional[int] = None
    ) -> Dict:
        """
        Получить данные с листа
        :param sheet_name: Название листа
        :param header_border: Граница таблицы
        :return: Dict - Данные листа
        """

        worksheet = self._table.worksheet(sheet_name)
        raw_data = worksheet.get_all_values()

        data = {}

        for index, row in enumerate(raw_data):
            row = row[:header_border]
            if index == 0:
                data = {
                    key: [] for key in row
                }
                continue

            for key, value in zip(data.keys(), row):
                data[key].append(value)

        return data

    def get_data_from_table_as_dataframe(
        self,
        sheet_name: str,
        header_border: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Получить данные с листа в виде датафрейма
        :param sheet_name: Название листа
        :param header_border: Граница таблицы
        :return: pd.DataFrame - Данные листа
        """

        result = self.get_data_from_table(
            sheet_name=sheet_name,
            header_border=header_border
        )

        try:
            data_df = pd.DataFrame(result)
        except Exception as e:
            print(f"Ошибка преобразования к датафрейму {e}")
            data_df = pd.DataFrame()

        return data_df

    def get_users(self) -> pd.DataFrame:
        """
        Получить всех пользователей с таблицы
        :return: pd.DataFrame - Датафрейм с пользователями
        """

        return self.get_data_from_table_as_dataframe(
            sheet_name="Работает ФСБ",
            header_border=8
        )

    @property
    def client(self) -> Client:
        return self.client

    @property
    def worksheets(self):
        return self.client.worksheets()


swift_table_client = GoogleSheetClient(
    json_path="swiftbot-500412-9c7cc1c291c5.json",
    table_id="1jStirZh3ve0CtwyH6GCBpwfXwhlMTmyUBGzFBOikXHY"
)
