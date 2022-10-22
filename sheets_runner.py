from google.oauth2.credentials import Credentials
import gspread
import pandas as pd

from utils.data_scraping import get_sp500_stocks
from scraping_runner import scrape

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
SPREADSHEET_KEY = "1nYYIkdzyH55uP6nAbRbkBJe5sWZPwJc6Z2GJ4O_j2sc"


def runner():
    credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(SPREADSHEET_KEY)
    sp500_stocks_df = get_sp500_stocks()
    todays_date = str(pd.to_datetime("today").date())
    for worksheet_name in sp500_stocks_df["GICS Sector"].unique():
        print("====================\nReviewing Sector: {}\n====================\n")
        worksheet = sheet.worksheet(worksheet_name)
        current_df = pd.DataFrame(worksheet.get_all_records())
        tickers = list(
            sp500_stocks_df["Symbol"][sp500_stocks_df["GICS Sector"] == worksheet_name]
        )
        results_df = scrape(tickers)
        results_df["date"] = todays_date
        new_df = current_df.append(results_df).drop_duplicates(
            ["ticker", "date"], keep="last"
        )
        worksheet.clear()
        worksheet.update([new_df.columns.values.tolist()] + new_df.values.tolist())


if __name__ == "__main__":
    runner()
