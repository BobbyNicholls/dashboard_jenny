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
