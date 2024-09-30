import os

import gspread
from dotenv import load_dotenv
import requests
from requests.exceptions import JSONDecodeError

load_dotenv()
key_name = os.getenv("KEY_NAME")
sheet_id = os.getenv("SHEET_ID")

def write_password(password) -> None:
    sheet_name = "概要"
    gc = gspread.service_account(filename=key_name)
    wks = gc.open_by_key(sheet_id).worksheet(sheet_name)
    wks.update_cell(8, 2, password)


def write_agenda(agendas, password) -> None:
    sheet_name = "質問"
    gc = gspread.service_account(filename=key_name)
    wks = gc.open_by_key(sheet_id).worksheet(sheet_name)
    last_row = len(wks.col_values(1))
    k = 3
    cnt = 0
    plus_rows = []
    for agenda in agendas:
        cnt += 1
        if cnt % 2 == 0:
            agenda = agenda[0]
            while "+" in agenda:
                idx = agenda.find("+")
                agenda = agenda[idx + 1 :]
                idx = agenda.find("\n")
                one_agenda = agenda[:idx]
                if "告知" not in one_agenda:
                    plus_rows.append(one_agenda)
                    k += 1
    for i, agenda_text in enumerate(plus_rows, start=3):
        wks.update_cell(i, 1, agenda_text)
    for j in range(3 + len(plus_rows), last_row + 1):
        wks.update_cell(j, 1, "")

    write_password(password)


# エラーハンドリングの追加
def fetch_sheet_metadata(client, sheet_id, params=None):
    try:
        response = client.request(
            "get",
            f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}",
            params=params,
        )
        response.raise_for_status()
        return response.json()
    except JSONDecodeError:
        print("JSONデコードエラー: レスポンスが無効なJSON形式です。")
        return None
    except requests.exceptions.RequestException as e:
        print(f"リクエストエラー: {e}")
        return None
