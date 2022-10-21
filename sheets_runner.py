from google.oauth2.credentials import Credentials
import gspread
import pandas as pd

from scraping_runner import scrape

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
SPREADSHEET_KEY = "1nYYIkdzyH55uP6nAbRbkBJe5sWZPwJc6Z2GJ4O_j2sc"
TICKERS = ["MSFT", "GOOG"]


def runner():
    # If modifying these scopes, delete the file token.json.
    credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    gc = gspread.authorize(credentials)
    worksheet_name = "API Test"
    sheet = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = sheet.worksheet(worksheet_name)
    current_df = pd.DataFrame(worksheet.get_all_records())
    results_df = scrape(TICKERS)
    results_df["date"] = str(pd.to_datetime("today").date())
    new_df = current_df.append(results_df)
    worksheet.clear()
    worksheet.update([new_df.columns.values.tolist()] + new_df.values.tolist())


if __name__ == "__main__":
    runner()

