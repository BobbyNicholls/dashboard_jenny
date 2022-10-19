def get_last_close_price(soup_text: str) -> float:
    soup_index = soup_text.index("The last closing price")
    soup_sub_text = soup_text[soup_index + 23 :]
    return float(soup_sub_text[: soup_sub_text.index("D")])


def get_market_cap_in_billions(soup_text: str) -> float:
    soup_index = soup_text.lower().index("the total number of outstanding shares.")
    soup_sub_text = soup_text[soup_index + 39 :]
    try:
        return float(soup_sub_text[: soup_sub_text.index("B USD")])
    except:
        try:
            return float(soup_sub_text[: soup_sub_text.index("T USD")]) * 1000
        except:
            raise ValueError("market cap is not in billions or trillions for asset provided???")


def get_52wk_high(soup_text: str) -> float:
    soup_index = soup_text.lower().index(
        "en the high and low prices over the past 52 weeks"
    )
    soup_sub_text = soup_text[soup_index + 50 :]
    return float(soup_sub_text[soup_sub_text.index("- $")+3:soup_sub_text.index("Market")])

