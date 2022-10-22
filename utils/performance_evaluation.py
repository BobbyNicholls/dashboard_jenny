import numpy as np
import pandas as pd


def get_performance_metrics(result_df: pd.DataFrame) -> pd.DataFrame:
    result_df = result_df.copy()
    coeficient, constant = np.polyfit(
        np.array(result_df["net_profit_margin"]),
        np.array(result_df["market_cap_over_revenue"]),
        1,
    )
    result_df["predicted_mkt_cap_over_rev"] = (
        coeficient * result_df["net_profit_margin"] + constant
    )
    result_df["mkt_cap_differential"] = (
        result_df["market_cap_over_revenue"] - result_df["predicted_mkt_cap_over_rev"]
    )
    result_df["relative_growth_performance"] = (
        result_df["net_income_yoy_growth"] - result_df["net_income_yoy_growth"].mean()
    )
    result_df = result_df.sort_values("mkt_cap_differential")
    return result_df
