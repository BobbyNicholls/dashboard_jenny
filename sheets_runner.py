import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gspread
import pandas as pd

from scraping_runner import scrape


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
TICKERS = ["NFLX"]
credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
gc = gspread.authorize(credentials)
spreadsheet_key = "1nYYIkdzyH55uP6nAbRbkBJe5sWZPwJc6Z2GJ4O_j2sc"
worksheet_name = "API Test"
sheet = gc.open_by_key(spreadsheet_key)
worksheet = sheet.worksheet("API Test")
results_df = scrape(TICKERS)
# worksheet.clear() clears all cells, use this to update a spreadsheet anew with the old one appended from before
worksheet.update([results_df.columns.values.tolist()] + results_df.values.tolist())

