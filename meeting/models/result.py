import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
KEY_NAME = os.getenv("KEY_NAME")
SHEET_ID = os.getenv("SHEET_ID")
SHEET_NAME = "回答"
RANGE_NAME = f"{SHEET_NAME}!A1:E100"

creds = Credentials.from_service_account_file(KEY_NAME, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)


def get_form_responses():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()
    values = result.get("values", [])

    if not values:
        return []

    headers = values[0]
    data = values[1:]

    aggregated_data = {"headers": headers, "data": data}

    return aggregated_data


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    print(get_form_responses())
