import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np


def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']))


def unpack_data(asset_info, vals_to_unpack):
    return [asset_info[val] for val in vals_to_unpack]


tickers = ["ADBE", "MSFT", "FB", "NFLX", "AAPL", "AMZN", "GOOG", "TTD", "GME", "TSLA", "PINS", "TWTR"]
#tickers = ["APPS", "AVV.L"]
asset_infos = [yf.Ticker(ticker).info for ticker in tickers]

"""
Wikipedia on "enterpriseToRevenue":
Enterprise value/sales is a financial ratio that compares the total value of the company to its sales. The ratio is, 
strictly speaking, denominated in years; it demonstrates how many dollars of EV are generated by one dollar of yearly 
sales. Generally, the lower the ratio, the cheaper the company is
"""

"""
The net income applicable to common shares figure on an income statement is the bottom-line profit belonging to the 
common stockholders, who are the ultimate owners, a company reported during the period being measured.
"""

# values we want:
financial_fundamentals = [
    "forwardPE",
    "trailingPE",
    "marketCap",
    "enterpriseToRevenue",
    "profitMargins",
    "forwardEps",
    "trailingEps",
    # "revenueQuarterlyGrowth",  # growth in revenue, not working right now, always returns a None
    "netIncomeToCommon",
    "earningsQuarterlyGrowth",  # growth in profit
]
technicals = [
    "fiftyTwoWeekHigh",
    "fiftyTwoWeekLow",
    "previousClose",
    "sharesShort",
    "shortRatio",
    "shortPercentOfFloat",
]
industry = "industry"

# get historical market data, here max is 5 years.
# df = adbe.history(period="3mo")

cols = financial_fundamentals

financials_df = pd.DataFrame(
    columns=cols,
    data=[unpack_data(x, cols) for x in asset_infos],
)

cols = ["fiftyTwoWeekHigh", "previousClose", "earningsQuarterlyGrowth"]

context_df = pd.DataFrame(
    columns=cols,
    data=[unpack_data(x, cols) for x in asset_infos],
)

context_df['close_to_high_ratio'] = context_df['previousClose'] / context_df['fiftyTwoWeekHigh']
context_df['symbol'] = tickers
context_df = context_df[["symbol"] + list(context_df.columns[:-1])]

financials_df['symbol'] = tickers
financials_df = financials_df[["symbol"] + list(financials_df.columns[:-1])]
financials_df['revenue_bn'] = financials_df['netIncomeToCommon']/financials_df['profitMargins']/1000000000
financials_df['market_cap_bn'] = financials_df['marketCap']/1000000000
financials_df['market_cap_over_revenue'] = financials_df['market_cap_bn'] / financials_df['revenue_bn']
financials_df = financials_df.drop(['marketCap'], axis=1)

target = 'market_cap_over_revenue'

###
### Make the valuation scatter plot
###
plt.figure(0)
ax = financials_df.set_index('profitMargins')[target].plot(style='o')
label_point(financials_df["profitMargins"], financials_df[target], financials_df["symbol"], ax)
x = np.array(financials_df["profitMargins"])
y = np.array(financials_df[target])
m, b = np.polyfit(x, y, 1)
ax.plot(x, m*x + b)
ax.set_xlabel("Profit Margin")
ax.set_ylabel("Market cap / revenue")
ax.plot()

###
### Make the context scatter plot
###
plt.figure(1)
ax1 = context_df.set_index("close_to_high_ratio")["earningsQuarterlyGrowth"].plot(style='o')
label_point(context_df["close_to_high_ratio"], financials_df["earningsQuarterlyGrowth"], context_df["symbol"], ax1)
# x = np.array(context_df["close_to_high_ratio"])
# y = np.array(financials_df["earningsQuarterlyGrowth"])
# plt.scatter(x, y)
ax1.xlabel("Close to high ratio")
ax1.ylabel("Quarterly earnings growth")
ax1.plot()

# to check keys
for inf in asset_infos:
    print(target in inf.keys())

