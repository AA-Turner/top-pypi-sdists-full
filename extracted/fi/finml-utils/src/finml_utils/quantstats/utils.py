# original code: QuantStats: Portfolio analytics for quants
# https://github.com/ranaroussi/quantstats Copyright 2019-2023 Ran Aroussi
# Licensed originally under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0


import io as _io

import numpy as np
import pandas as pd

from . import stats as _stats


def multi_shift(df: pd.Series | pd.DataFrame, shift: int = 3) -> pd.DataFrame:
    """Get last N rows relative to another row in pandas"""
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)

    dfs = [df.shift(i) for i in np.arange(shift)]
    for ix, dfi in enumerate(dfs[1:]):
        dfs[ix + 1].columns = [str(col) for col in dfi.columns + str(ix + 1)]
    return pd.concat(dfs, 1, sort=True)


def to_returns(prices: pd.Series | pd.DataFrame) -> pd.Series | pd.DataFrame:
    """Calculates the simple arithmetic returns of a price series"""
    return prices.pct_change().replace([np.inf, -np.inf], float("NaN"))


def to_prices(
    returns: pd.Series | pd.DataFrame, base: float = 1e5
) -> pd.Series | pd.DataFrame:
    """Converts returns series to price data"""
    returns = returns.copy().fillna(0).replace([np.inf, -np.inf], float("NaN"))

    return base + base * _stats.compsum(returns)


def to_log_returns(returns: pd.Series | pd.DataFrame) -> pd.Series | float:
    """Converts returns series to log returns"""
    try:
        return np.log(returns + 1).replace([np.inf, -np.inf], float("NaN"))
    except Exception:  # noqa
        return 0.0


def exponential_stdev(
    returns: pd.Series | pd.DataFrame, window: int = 30, is_halflife: bool = False
) -> pd.Series | pd.DataFrame:
    """Returns series representing exponential volatility of returns"""
    halflife = window if is_halflife else None
    return returns.ewm(
        com=None, span=window, halflife=halflife, min_periods=window
    ).std()


def rebase(
    prices: pd.Series | pd.DataFrame, base: float = 1.0
) -> pd.Series | pd.DataFrame:
    """
    Rebase all series to a given intial base.
    This makes comparing/plotting different series together easier.
    Args:
        * prices: Expects a price series/dataframe
        * base (number): starting value for all series.
    """
    return prices.dropna() / prices.dropna().iloc[0] * base


def group_returns(
    returns: pd.Series | pd.DataFrame, groupby: str, compounded: bool = False
) -> pd.Series | pd.DataFrame:
    """Summarize returns
    group_returns(df, df.index.year)
    group_returns(df, [df.index.year, df.index.month])
    """
    if compounded:
        return returns.groupby(groupby).apply(_stats.comp)
    return returns.groupby(groupby).sum()


def aggregate_returns(
    returns: pd.Series | pd.DataFrame, period=None, compounded: bool = True
) -> pd.Series | pd.DataFrame:
    """Aggregates returns based on date periods"""
    if period is None or "day" in period:
        return returns
    index = returns.index

    if "month" in period:
        return group_returns(returns, index.month, compounded=compounded)

    if "quarter" in period:
        return group_returns(returns, index.quarter, compounded=compounded)

    if period == "A" or any(x in period for x in ["year", "eoy", "yoy"]):
        return group_returns(returns, index.year, compounded=compounded)

    if "week" in period:
        return group_returns(returns, index.week, compounded=compounded)

    if "eow" in period or period == "W":
        return group_returns(returns, [index.year, index.week], compounded=compounded)

    if "eom" in period or period == "M":
        return group_returns(returns, [index.year, index.month], compounded=compounded)

    if "eoq" in period or period == "Q":
        return group_returns(
            returns, [index.year, index.quarter], compounded=compounded
        )

    if not isinstance(period, str):
        return group_returns(returns, period, compounded)

    return returns


def to_excess_returns(
    returns: pd.Series | pd.DataFrame,
    rf: float | pd.Series | pd.DataFrame,
    nperiods: int | None = None,
) -> pd.Series | pd.DataFrame:
    """
    Calculates excess returns by subtracting
    risk-free returns from total returns

    Args:
        * returns (Series, DataFrame): Returns
        * rf (float, Series, DataFrame): Risk-Free rate(s)
        * nperiods (int): Optional. If provided, will convert rf to different
            frequency using deannualize
    Returns:
        * excess_returns (Series, DataFrame): Returns - rf
    """
    if isinstance(rf, int):
        rf = float(rf)

    if not isinstance(rf, float):
        rf = rf[rf.index.isin(returns.index)]

    if nperiods is not None:
        # deannualize
        rf = np.power(1 + rf, 1.0 / nperiods) - 1.0

    return returns - rf


def _prepare_prices(data: pd.Series | pd.DataFrame, base: float = 1.0):
    """Converts return data into prices + cleanup"""
    data = data.copy()
    if isinstance(data, pd.DataFrame):
        for col in data.columns:
            if data[col].dropna().min() <= 0 or data[col].dropna().max() < 1:
                data[col] = to_prices(data[col], base)

    # is it returns?
    # elif data.min() < 0 and data.max() < 1:
    elif data.min() < 0 or data.max() < 1:
        data = to_prices(data, base)

    if isinstance(data, pd.DataFrame | pd.Series):
        data = data.fillna(0).replace([np.inf, -np.inf], float("NaN"))

    return data


def _file_stream():
    """Returns a file stream"""
    return _io.BytesIO()


def _count_consecutive(data: pd.Series | pd.DataFrame):
    """Counts consecutive data (like cumsum() with reset on zeroes)"""

    def _count(data: pd.Series | pd.DataFrame):
        return data * (data.groupby((data != data.shift(1)).cumsum()).cumcount() + 1)

    if isinstance(data, pd.DataFrame):
        for col in data.columns:
            data[col] = _count(data[col])
        return data
    return _count(data)
