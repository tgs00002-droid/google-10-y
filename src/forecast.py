# src/forecast.py
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def forecast_product(df, product, years=10):
    s = (
        df[df["product"] == product]
        .set_index("date")["revenue"]
        .asfreq("Q")
        .interpolate()
    )

    model = SARIMAX(
        s,
        order=(1,1,1),
        seasonal_order=(1,1,1,4),
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    res = model.fit(disp=False)
    steps = years * 4
    pred = res.get_forecast(steps)

    out = pred.predicted_mean.reset_index()
    out.columns = ["date", "forecast"]
    out["product"] = product
    return out


def forecast_all(df, years=10):
    frames = []
    for p in df["product"].unique():
        frames.append(forecast_product(df, p, years))
    return pd.concat(frames)
