import pandas as pd
import yfinance as yf

adbe = yf.Ticker("ADBE")
# get stock info
x = adbe.info
print(x['marketCap'])

"""
returns:
{
 'quoteType': 'EQUITY',
 'quoteSourceName': 'Nasdaq Real Time Price',
 'currency': 'USD',
 'shortName': 'Microsoft Corporation',
 'exchangeTimezoneName': 'America/New_York',
  ...
 'symbol': 'MSFT'
}
"""

# get historical market data, here max is 5 years.
df = adbe.history(period="3mo")