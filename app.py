# app.py
import streamlit as st
import plotly.express as px

from src.data import load_revenue_by_product
from src.forecast import forecast_all

st.set_page_config(page_title="Google 10-Year Revenue Forecast", layout="wide")

st.title("Alphabet (Google) 10-Year Revenue Forecast")
st.caption("Real revenue by product • Forecasted using quarterly time series models")

@st.cache_data
def get_data():
    return load_revenue_by_product()

@st.cache_data
def get_forecast(df, years):
    return forecast_all(df, years)

df = get_data()

years = st.sidebar.slider("Forecast Horizon (Years)", 5, 15, 10)
forecast_df = get_forecast(df, years)

tab1, tab2 = st.tabs(["Historical Data", "Forecast"])

with tab1:
    product = st.selectbox("Product", sorted(df["product"].unique()))
    hist = df[df["product"] == product]

    fig = px.line(
        hist,
        x="date",
        y="revenue",
        title=f"{product} – Historical Revenue"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    product = st.selectbox("Forecast Product", sorted(forecast_df["product"].unique()))
    fc = forecast_df[forecast_df["product"] == product]

    fig = px.line(
        fc,
        x="date",
        y="forecast",
        title=f"{product} – {years}-Year Forecast"
    )
    st.plotly_chart(fig, use_container_width=True)

    total = (
        forecast_df
        .groupby("date")["forecast"]
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        total,
        x="date",
        y="forecast",
        title="Total Google Revenue Forecast"
    )
    st.plotly_chart(fig2, use_container_width=True)
