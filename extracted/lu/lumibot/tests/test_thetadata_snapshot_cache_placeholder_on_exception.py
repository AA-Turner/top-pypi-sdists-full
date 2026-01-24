from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

from lumibot.entities import Asset
from lumibot.tools.backtest_cache import CacheMode
from lumibot.tools import thetadata_helper


def test_get_historical_data_snapshot_cached_writes_placeholder_on_fetch_exception(tmp_path, monkeypatch):
    """Snapshot caches must go warm even when the downloader request errors out."""

    class _DummyCacheManager:
        enabled = False
        mode = CacheMode.DISABLED

    monkeypatch.setattr(thetadata_helper, "get_backtest_cache", lambda: _DummyCacheManager())
    monkeypatch.setattr(thetadata_helper, "LUMIBOT_CACHE_FOLDER", str(tmp_path))

    def _boom(*_args, **_kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(thetadata_helper, "get_historical_data", _boom)

    asset = Asset(
        symbol="MELI",
        asset_type=Asset.AssetType.OPTION,
        expiration=date(2022, 1, 21),
        strike=1660.0,
        right="CALL",
    )
    start_dt = thetadata_helper.LUMIBOT_DEFAULT_PYTZ.localize(datetime(2022, 1, 21, 8, 30, 0))
    end_dt = start_dt + timedelta(minutes=5)

    result = thetadata_helper.get_historical_data_snapshot_cached(
        asset,
        start_dt,
        end_dt,
        60_000,
        datastyle="quote",
        include_after_hours=True,
    )
    assert result is None

    cache_file = thetadata_helper.build_snapshot_cache_filename(
        asset,
        trading_day=date(2022, 1, 21),
        interval_label="1m",
        # Options snapshot caches are normalized to the regular session window to avoid
        # placeholder-only extended-hours fetch loops and to keep cache keys stable.
        start_time="09:30:00",
        end_time="16:00:00",
        datastyle="quote",
    )

    assert cache_file.exists(), f"Expected snapshot cache file to exist: {cache_file}"
    assert Path(str(tmp_path)) in cache_file.parents

    df = pd.read_parquet(cache_file)
    assert not df.empty
    assert "missing" in df.columns
