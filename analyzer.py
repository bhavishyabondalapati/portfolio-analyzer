"""Data download and portfolio statistics."""
from __future__ import annotations

import numpy as np
import pandas as pd

TICKERS = ["AAPL", "MSFT", "GOOGL", "JPM", "SPY"]
TRADING_DAYS = 252


def download_prices(tickers=TICKERS, period: str = "2y") -> pd.DataFrame:
    """Download daily adjusted close prices (one column per ticker)."""
    import yfinance as yf

    data = yf.download(list(tickers), period=period, interval="1d",
                       auto_adjust=True, progress=False)
    if data.empty:
        raise RuntimeError("yfinance returned no data (network issue or rate limit?)")
    prices = data["Close"]
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(list(tickers)[0])
    prices.index = pd.to_datetime(prices.index).tz_localize(None)
    return prices.dropna(how="all").sort_index()


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna(how="all")


def annualized_return(returns: pd.DataFrame, periods: int = TRADING_DAYS) -> pd.Series:
    """Geometric annualized return."""
    growth = (1 + returns).prod()
    n = returns.count()
    return growth ** (periods / n) - 1


def annualized_volatility(returns: pd.DataFrame, periods: int = TRADING_DAYS) -> pd.Series:
    return returns.std() * np.sqrt(periods)


def sharpe_ratio(returns: pd.DataFrame, risk_free: float = 0.0,
                 periods: int = TRADING_DAYS) -> pd.Series:
    vol = annualized_volatility(returns, periods)
    return (annualized_return(returns, periods) - risk_free) / vol.replace(0, np.nan)


def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.corr()


def metrics_table(returns: pd.DataFrame, risk_free: float = 0.0) -> pd.DataFrame:
    return pd.DataFrame({
        "Annualized Return": annualized_return(returns),
        "Volatility": annualized_volatility(returns),
        "Sharpe Ratio": sharpe_ratio(returns, risk_free),
    })
