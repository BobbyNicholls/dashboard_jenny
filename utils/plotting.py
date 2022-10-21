import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def label_point(x, y, val, ax):
    a = pd.concat({"x": x, "y": y, "val": val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point["x"], point["y"], str(point["val"]))


def plot_results(result_df: pd.DataFrame):
    fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2)
    fig.set_size_inches(18.5, 7.5)
    x = np.array(result_df["net_profit_margin"])
    y = np.array(result_df["market_cap_over_revenue"])
    ax2.scatter(x, y)
    label_point(
        result_df["net_profit_margin"],
        result_df["market_cap_over_revenue"],
        result_df["ticker"],
        ax2,
    )
    coefficient, constant = np.polyfit(x, y, 1)
    ax2.plot(x, coefficient * x + constant)
    ax2.set_xlabel("Profit Margin")
    ax2.set_ylabel("Market cap / revenue")
    ax2.plot()

    x = np.array(result_df["headroom_to_52wk"])
    y = np.array(result_df["net_income_yoy_growth"])
    ax3.scatter(x, y)
    label_point(
        result_df["headroom_to_52wk"],
        result_df["net_income_yoy_growth"],
        result_df["ticker"],
        ax3,
    )
    ax3.set_xlabel("Headroom percent to 52 week high")
    ax3.set_ylabel("Net income YoY growth")
    ax3.plot()
    fig.savefig(f"plots/plot {str(pd.to_datetime('today'))[:19].replace(':','-')}.png")
    plt.close(fig)


def plot_performance_metrics(result_df: pd.DataFrame):
    fig2, ax = plt.subplots(nrows=1, ncols=1)
    x = np.array(result_df["mkt_cap_differential"])
    y = np.array(result_df["relative_growth_performance"])
    ax.set_xlabel("Market Cap Differential")
    ax.set_ylabel("Relative growth performance vs cohort")
    ax.scatter(x, y)
    label_point(
        result_df["mkt_cap_differential"],
        result_df["relative_growth_performance"],
        result_df["ticker"],
        ax,
    )
    ax.plot()
