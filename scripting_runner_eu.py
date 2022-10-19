"""
Attributes:
https://support.google.com/docs/answer/3093281?hl=en-GB

"""

import pandas as pd

from configs import stocks_i_own_eur as tickers
from utils.data_scraping import scrape_data
from utils.plotting import plot_results

url_formats = [
    "https://www.google.com/finance/quote/{ticker}:LON",
    "https://www.google.com/finance/quote/{ticker}:EBR",
    "FAILED",
]

market_caps = []
headrooms = []
revenues = []
net_profit_margins = []
net_income_yoy_growths = []
failures = []
exceptions = []
for ticker in tickers:
    print(f"Working on ticker: {ticker}")
    for url_format in url_formats:
        try:
            url = url_format.replace("{ticker}", ticker)
            scrape_data(url, market_caps, headrooms, revenues, net_profit_margins, net_income_yoy_growths)
            break
        except Exception as e:
            exceptions.append(e)
            if url_format == "FAILED":
                print(f"Ticker: {ticker} has failed to scrape with all URL formats.")
                failures.append(ticker)
                break
            continue

result_df = pd.DataFrame(
    {
        "ticker": [ticker for ticker in tickers if ticker not in failures],
        "market_cap": market_caps,
        "headroom_to_52wk": headrooms,
        "revenue": revenues,
        "net_profit_margin": net_profit_margins,
        "net_income_yoy_growth": net_income_yoy_growths,
    }
)
result_df["market_cap_over_revenue"] = result_df["market_cap"] / result_df["revenue"]
result_df.to_csv("results.csv", index=False)
plot_results(result_df)
