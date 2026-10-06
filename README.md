# Portfolio Analyzer

Streamlit dashboard that downloads 2 years of daily prices (AAPL, MSFT, GOOGL, JPM, SPY) via yfinance and shows
a rebased price chart, return/volatility/Sharpe metrics, and a correlation heatmap of daily returns.

## Setup (conda)

```bash
conda create -n portfolio-analyzer python=3.12 -y
conda activate portfolio-analyzer
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## Test

```bash
pytest
```

## Notes
- Metrics: geometric annualized return, volatility = daily std x sqrt(252), Sharpe = (return - risk-free) / volatility (risk-free adjustable in the sidebar, default 0).
- Prices are split/dividend-adjusted closes and cached for 1 hour.
- Code: `analyzer.py` (data + stats), `app.py` (UI), `tests/` (pytest).
