"""
Attributes:
https://support.google.com/docs/answer/3093281?hl=en-GB

"""

import pandas as pd

from configs import sp500_health_care_tickers as tickers
from utils.data_scraping import scrape_data
from utils.performance_evaluation import get_performance_metrics
from utils.plotting import plot_results, plot_performance_metrics

url_formats = [
    "https://www.google.com/finance/quote/{ticker}:NYSE",
    "https://www.google.com/finance/quote/{ticker}:NASDAQ",
    "https://www.google.com/finance/quote/{ticker}:BATS",
    "FAILED",
]


def runner():
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
                scrape_data(
                    url,
                    market_caps,
                    headrooms,
                    revenues,
                    net_profit_margins,
                    net_income_yoy_growths,
                )
                break
            except Exception as e:
                exceptions.append(f"{ticker}: {e}")
                if url_format == "FAILED":
                    print(
                        f"Ticker: {ticker} has failed to scrape with all URL formats."
                    )
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
    result_df["market_cap_over_revenue"] = (
        result_df["market_cap"] / result_df["revenue"]
    )
    plot_results(result_df)
    result_df = get_performance_metrics(result_df)
    plot_performance_metrics(result_df)
    return result_df


if __name__ == "__main__":
    result_df = runner()
    result_df.to_csv("results.csv", index=False)
    print(result_df)
