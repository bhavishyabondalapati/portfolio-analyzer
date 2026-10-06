import numpy as np
import pandas as pd
import pytest

import analyzer as an


@pytest.fixture
def prices():
    idx = pd.bdate_range("2024-01-01", periods=5)
    return pd.DataFrame({"A": [100, 110, 121, 133.1, 146.41],
                         "B": [100, 100, 100, 100, 100]}, index=idx)


def test_daily_returns(prices):
    r = an.daily_returns(prices)
    assert len(r) == 4
    assert r["A"].iloc[0] == pytest.approx(0.10)
    assert (r["B"] == 0).all()


def test_annualized_return_constant_growth(prices):
    r = an.daily_returns(prices)
    expected = 1.1 ** 252 - 1
    assert an.annualized_return(r)["A"] == pytest.approx(expected)
    assert an.annualized_return(r)["B"] == pytest.approx(0)


def test_volatility_and_sharpe(prices):
    r = an.daily_returns(prices)
    assert an.annualized_volatility(r)["B"] == 0
    assert np.isnan(an.sharpe_ratio(r)["B"])  # zero vol -> undefined
    rng = np.random.default_rng(0)
    r2 = pd.DataFrame({"X": rng.normal(0.001, 0.01, 500)})
    vol = an.annualized_volatility(r2)["X"]
    assert vol == pytest.approx(r2["X"].std() * np.sqrt(252))
    assert an.sharpe_ratio(r2)["X"] == pytest.approx(an.annualized_return(r2)["X"] / vol)


def test_correlation_matrix():
    rng = np.random.default_rng(1)
    a = rng.normal(size=200)
    r = pd.DataFrame({"A": a, "B": 2 * a, "C": -a})
    c = an.correlation_matrix(r)
    assert c.shape == (3, 3)
    assert c.loc["A", "B"] == pytest.approx(1)
    assert c.loc["A", "C"] == pytest.approx(-1)
    assert np.allclose(np.diag(c), 1)
