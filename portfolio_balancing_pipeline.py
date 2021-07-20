from dagster import pipeline, solid
import pandas as pd
import pandas_datareader.data as web


def get_cv(ticker, month_offset=24):
    df = web.DataReader(
        ticker,
        "yahoo",
        (pd.to_datetime("now") - pd.DateOffset(months=month_offset)).date(),
        pd.to_datetime("now").date(),
    )
    return (df["Close"].std() / df["Close"].mean()) * 100


@solid
def get_portfolio_variances():
    portfolio_tickers = [
        "BABA",
        "ASTS",
        "JKS",
        "CRSR",
        "FLGT",
        "ADBE",
        "MSFT",
        "FB",
        "GOOG",
    ]
    return pd.Series(
        data=[get_cv(ticker) for ticker in portfolio_tickers], index=portfolio_tickers
    ).sort_values(ascending=False)


@solid
def calc_light_scaled_allocation(context, variances, light_scalar=2):
    lsmcv = light_scalar * variances.max()
    light_scaled_variances = lsmcv - variances
    light_scaled_weighting = light_scaled_variances / light_scaled_variances.sum()
    light_scaled_allocation = light_scaled_weighting * 100_000
    context.log.info(
        f"\nWith a Light Scalar of {light_scalar} this is your distribution:"
        "\n" + str(light_scaled_allocation.astype(int))
    )


@pipeline
def serial_pipeline():
    calc_light_scaled_allocation(get_portfolio_variances())
