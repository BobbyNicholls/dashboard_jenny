from typing import List

import pandas as pd


def get_revenue(dfs: List[pd.DataFrame]) -> float:
    rev_df = dfs[0]
    assert "Revenue" in rev_df[rev_df.columns[0]].iloc[0], (
        "Google has changed the layout of their page so that revenue is no longer in the table the is pulled by pandas"
        " from the html data scraped from the quote page."
    )

    rev_str = rev_df[rev_df.columns[1]].iloc[0]
    try:
        return float(rev_str[: rev_str.index("B")]) * 4
    except ValueError:
        try:
            return (float(rev_str[: rev_str.index("M")]) / 1000) * 4
        except ValueError:
            raise ValueError("revenue is not expressed in billions or millions??")


def get_net_profit_margin(dfs: List[pd.DataFrame]) -> float:
    npm_df = dfs[0]
    assert "Net profit margin" in npm_df[npm_df.columns[0]].iloc[3], (
        "Google has changed the layout of their page so that net profit margin is no longer in the table the is pulled "
        "by pandas from the html data scraped from the quote page."
    )

    return float(npm_df[npm_df.columns[1]].iloc[3])


def get_net_income_growth(dfs: List[pd.DataFrame]) -> float:
    net_income_growth_df = dfs[0]
    assert (
        "Net income" in net_income_growth_df[net_income_growth_df.columns[0]].iloc[2]
    ), (
        "Google has changed the layout of their page so that net profit margin is no longer in the table the is pulled "
        "by pandas from the html data scraped from the quote page."
    )
    net_inc_growth_str = net_income_growth_df[net_income_growth_df.columns[2]].iloc[2]
    return float(net_inc_growth_str[: net_inc_growth_str.index("%")].replace(",", ""))
