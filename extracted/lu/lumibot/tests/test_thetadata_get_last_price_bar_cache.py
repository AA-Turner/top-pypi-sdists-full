from datetime import datetime

import pandas as pd
import pytz

from lumibot.backtesting.thetadata_backtesting_pandas import ThetaDataBacktestingPandas
from lumibot.entities import Asset, Data


def test_thetadata_get_last_price_caches_within_bar(monkeypatch):
    monkeypatch.setattr(ThetaDataBacktestingPandas, "kill_processes_by_name", lambda *_a, **_k: None)

    start = datetime(2024, 1, 2, 9, 30, tzinfo=pytz.UTC)
    end = datetime(2024, 1, 2, 9, 35, tzinfo=pytz.UTC)
    idx = pd.date_range(start, periods=3, freq="1min", tz="UTC")

    asset = Asset("SPY", asset_type=Asset.AssetType.STOCK)
    quote = Asset("USD", asset_type=Asset.AssetType.FOREX)
    df = pd.DataFrame(
        {"open": [1.0, 2.0, 3.0], "high": [1.0, 2.0, 3.0], "low": [1.0, 2.0, 3.0], "close": [1.0, 2.0, 3.0], "volume": [1, 1, 1]},
        index=idx,
    )
    data = Data(asset=asset, df=df, quote=quote, timestep="minute")

    ds = ThetaDataBacktestingPandas(datetime_start=start, datetime_end=end, pandas_data=[data])
    ds._datetime = idx[1]

    calls = {"count": 0}

    def _noop_update(*_a, **_k):
        calls["count"] += 1

    monkeypatch.setattr(ds, "_update_pandas_data", _noop_update)

    first = ds.get_last_price(asset, timestep="minute", quote=quote)
    second = ds.get_last_price(asset, timestep="minute", quote=quote)
    assert first == second
    assert calls["count"] == 1

    # Cache is dt-scoped: a new bar should trigger a new lookup.
    ds._datetime = idx[2]
    third = ds.get_last_price(asset, timestep="minute", quote=quote)
    assert third is not None
    assert calls["count"] == 2

