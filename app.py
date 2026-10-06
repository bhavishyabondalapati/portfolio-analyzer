import pandas as pd
import plotly.express as px
import streamlit as st

import analyzer as an

st.set_page_config(page_title="Portfolio Analyzer", layout="wide")
st.title("Stock Portfolio Analyzer")


@st.cache_data(ttl=3600, show_spinner="Downloading prices...")
def load_prices() -> pd.DataFrame:
    return an.download_prices()


try:
    prices = load_prices()
except Exception as e:
    st.error(f"Could not download data: {e}")
    st.stop()

with st.sidebar:
    st.header("Settings")
    tickers = st.multiselect("Tickers", list(prices.columns), default=list(prices.columns))
    min_d, max_d = prices.index.min().date(), prices.index.max().date()
    date_range = st.date_input("Date range", (min_d, max_d), min_value=min_d, max_value=max_d)
    rf = st.number_input("Risk-free rate (annual, %)", 0.0, 20.0, 0.0, 0.25) / 100

if len(tickers) == 0:
    st.warning("Select at least one ticker.")
    st.stop()
if len(date_range) != 2:
    st.info("Pick both a start and end date.")
    st.stop()

start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
sel = prices.loc[start:end, tickers]
if len(sel) < 3:
    st.warning("Not enough data in that date range.")
    st.stop()
rets = an.daily_returns(sel)

st.subheader("Price (rebased to 100)")
rebased = sel / sel.bfill().iloc[0] * 100
st.plotly_chart(px.line(rebased, labels={"value": "Rebased price", "index": "Date",
                                          "variable": "Ticker"}),
                use_container_width=True)

st.subheader("Metrics")
m = an.metrics_table(rets, rf)
st.dataframe(m.style.format({"Annualized Return": "{:.2%}", "Volatility": "{:.2%}",
                             "Sharpe Ratio": "{:.2f}"}), use_container_width=True)

st.subheader("Correlation of daily returns")
if len(tickers) < 2:
    st.info("Select two or more tickers to see correlations.")
else:
    st.plotly_chart(px.imshow(an.correlation_matrix(rets), text_auto=".2f",
                              zmin=-1, zmax=1, color_continuous_scale="RdBu_r"),
                    use_container_width=True)
