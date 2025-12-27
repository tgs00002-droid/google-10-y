# src/data.py
import pandas as pd
import requests

URL = "https://stockanalysis.com/stocks/goog/metrics/revenue-by-segment/"

def load_revenue_by_product() -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(URL, headers=headers, timeout=30).text

    tables = pd.read_html(html)
    df = tables[0]

    df.rename(columns={df.columns[0]: "date"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"]).dt.to_period("Q").dt.to_timestamp("Q")

    def parse_money(x):
        if isinstance(x, str):
            x = x.replace(",", "")
            if x.endswith("B"):
                return float(x[:-1]) * 1e9
            if x.endswith("M"):
                return float(x[:-1]) * 1e6
        return float(x)

    products = df.columns.drop("date")
    for c in products:
        df[c] = df[c].apply(parse_money)

    tidy = df.melt(
        id_vars="date",
        var_name="product",
        value_name="revenue"
    ).dropna()

    return tidy.sort_values(["product", "date"])
