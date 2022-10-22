from typing import List
import urllib.request as urllib

from bs4 import BeautifulSoup
import pandas as pd

from utils.dataframe_searching import (
    get_revenue,
    get_net_profit_margin,
    get_net_income_growth,
)
from utils.text_searching import (
    get_last_close_price,
    get_market_cap_in_billions,
    get_52wk_high,
)


def scrape_data(
    url: str,
    market_caps: List[float],
    headrooms: List[float],
    revenues: List[float],
    net_profit_margins: List[float],
    net_income_yoy_growths: List[float],
):
    html_data = urllib.urlopen(url).read()
    dfs = pd.read_html(html_data)
    soup = BeautifulSoup(html_data, "html.parser")
    soup_text = soup.get_text()
    market_cap = get_market_cap_in_billions(soup_text)
    last_close_price = get_last_close_price(soup_text)
    year_high = get_52wk_high(soup_text)
    revenue = get_revenue(dfs)
    net_prof_margin = get_net_profit_margin(dfs)
    net_income_growth = get_net_income_growth(dfs)
    headrooms.append((year_high - last_close_price) / last_close_price)
    revenues.append(revenue)
    net_profit_margins.append(net_prof_margin)
    net_income_yoy_growths.append(net_income_growth)
    market_caps.append(market_cap)


def get_sp500_stocks_by_sector(sector: str) -> List[str]:
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html_data = urllib.urlopen(sp500_url).read()
    dfs = pd.read_html(html_data)
    sector_df = dfs[0]
    print(sector_df.groupby("GICS Sector").count()["CIK"].rename("Count by sector"))
    return list(sector_df[sector_df["GICS Sector"] == sector]["Symbol"])


def get_sp500_stocks() -> pd.DataFrame:
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html_data = urllib.urlopen(sp500_url).read()
    dfs = pd.read_html(html_data)
    return dfs[0]
