# Portfolio Analyzer

A Streamlit dashboard that downloads two years of daily adjusted prices for AAPL, MSFT, GOOGL, JPM, and SPY and reports annualized return, volatility, Sharpe ratio, and return correlations. Ticker selection, date range, and risk-free rate are adjustable, and all charts and tables update interactively.

## Features

- **Price download** from Yahoo Finance via yfinance (adjusted for splits and dividends), cached across Streamlit reruns.
- **Rebased price chart**: each series divided by its first value and scaled to 100 for comparison on one axis.
- **Metrics table**: annualized return, annualized volatility, and Sharpe ratio per ticker.
- **Correlation heatmap** of daily returns.
- **Controls**: ticker subset, date range, and annual risk-free rate (default 0%), with validation messages for empty selections or too few trading days.

## Method

| Metric | Definition |
|---|---|
| Daily return | `price_t / price_{t-1} − 1` |
| Annualized return | `growth ** (252 / n_days) − 1`, where `growth` is the compounded daily return |
| Annualized volatility | Standard deviation of daily returns × √252 |
| Sharpe ratio | `(annualized return − risk-free rate) / annualized volatility` |
| Correlation | Pearson correlation of daily returns |

All calculations live in `analyzer.py` with no UI code; `app.py` contains only the Streamlit interface.

| Library | Role |
|---|---|
| yfinance | Historical prices with no API key |
| pandas, NumPy | Time-series returns, statistics, and correlations |
| Streamlit | Interactive web app |
| Plotly | Interactive line chart and heatmap |
| pytest | Tests of the calculations |

## Quickstart

```bash
conda create -n portfolio-analyzer python=3.12 -y
conda activate portfolio-analyzer
pip install -r requirements.txt
streamlit run app.py
```

The dashboard opens at http://localhost:8501.

## Running tests

```bash
pytest
```

4 tests check each calculation against small synthetic price series with known answers; no network access is required.

## Project structure

```
portfolio-analyzer/
├── analyzer.py            Price download and statistics (no UI code)
├── app.py                 Streamlit dashboard: sidebar controls, chart, table, heatmap
├── tests/
│   └── test_analyzer.py   Calculation tests with known answers
├── pytest.ini             Test discovery and import path
└── requirements.txt
```

## Design decisions

- **Returns, not prices.** Statistics are computed on returns, which are comparable across tickers with very different price levels.
- **252 trading days per year** for annualization.
- **Separated calculation and UI** so the math is testable without Streamlit.
- **`@st.cache_data` on the download**, since Streamlit reruns the script on every interaction.

## Limitations and future work

- Historical statistics do not predict future performance. This project is not financial advice.
- The ticker list is fixed at download time; the sidebar selects among the five default tickers.
- Depends on Yahoo Finance availability and rate limits through yfinance.
- Possible extensions: portfolio weights and combined portfolio metrics, drawdown, and beta against SPY.
