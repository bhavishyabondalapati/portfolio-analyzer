# Portfolio Analyzer

A Streamlit dashboard that downloads two years of daily stock prices for AAPL, MSFT, GOOGL, JPM, and SPY. It calculates returns, risk (volatility), Sharpe ratio, and how the stocks move together, then shows them as charts and tables. You can pick tickers and a date range and everything updates.

## Tools and libraries used

| Tool | Why it was chosen |
|---|---|
| **yfinance** | Free way to download historical prices from Yahoo Finance, with no API key. |
| **pandas** | The standard library for time-series tables; makes returns and correlations one-liners. |
| **numpy** | Fast math, used here for the square root in annualized volatility. |
| **Streamlit** | Turns a plain Python script into an interactive web app without writing HTML or JavaScript. |
| **Plotly** | Interactive charts (hover, zoom) and a ready-made heatmap. |
| **pytest** | Simple, popular testing framework. |
| **conda** | Keeps this project's packages in their own environment, separate from `(base)`. |

## File structure

```
portfolio-analyzer/
├── analyzer.py            # Downloads prices and calculates all the statistics (no UI code)
├── app.py                 # The Streamlit dashboard: sidebar controls, chart, table, heatmap
├── tests/
│   ├── __init__.py        # Empty file that marks tests/ as a Python package
│   └── test_analyzer.py   # pytest tests that check the calculations against known answers
├── pytest.ini             # Tells pytest where the tests are and to import from the project root
├── requirements.txt       # List of Python packages needed
├── .gitignore             # Files git should not track (caches, venvs, .env, .DS_Store)
└── README.md              # This file
```

## Setup steps

Create a conda environment named after the project folder and install the packages:

```bash
conda create -n portfolio-analyzer python=3.12 -y
conda activate portfolio-analyzer
pip install -r requirements.txt
```

## How to run it

Start the dashboard (it opens at http://localhost:8501):

```bash
streamlit run app.py
```

Run the tests:

```bash
pytest
```

## How it was built

1. Created a separate conda environment, `portfolio-analyzer`, so nothing was installed into `(base)`.
2. Wrote `requirements.txt` and `.gitignore`.
3. Wrote `analyzer.py`: a function to download prices with yfinance, then small functions for daily returns, annualized return, volatility, Sharpe ratio, and the correlation matrix.
4. Wrote `tests/test_analyzer.py` using tiny made-up price series where the right answer is known, and ran pytest until it passed.
5. Checked the real download works (501 trading days, no missing values for all 5 tickers).
6. Wrote `app.py`: sidebar controls, a rebased price chart, a metrics table, and a correlation heatmap, with friendly messages for bad input (no tickers, too few days).
7. Ran Streamlit and opened it in a browser to confirm everything renders without errors.
8. Wrote this README, committed in small steps, and pushed to GitHub.

## Key concepts

- **Daily return**: `today / yesterday - 1`. Returns, not prices, are what you analyze, because they are comparable across stocks.
- **Annualized return**: compound the daily returns, then scale to a year (252 trading days): `growth ** (252 / n_days) - 1`.
- **Volatility**: the standard deviation of daily returns times `sqrt(252)`. It measures how bumpy the ride is. Variance grows linearly with time, so the standard deviation grows with its square root.
- **Sharpe ratio**: `(return - risk_free_rate) / volatility`. It is the return you earned per unit of risk; higher is better. The risk-free rate defaults to 0 here and can be changed in the sidebar.
- **Correlation matrix**: values from -1 to +1 for how two stocks' daily returns move together. A low correlation means a better diversification benefit. SPY correlates strongly with the others because they are inside it.
- **Adjusted close prices**: prices corrected for splits and dividends, so returns are not distorted.
- **Rebasing to 100**: dividing each price series by its first value, so stocks with very different prices can share one chart.
- **Separation of concerns**: calculations live in `analyzer.py` and the UI in `app.py`, which makes the math easy to test.
- **Caching** (`@st.cache_data`): Streamlit reruns the script on every interaction, so the download is cached to avoid re-fetching.
- **Limitations**: past performance doesn't predict the future, and this is an educational project, not financial advice.
