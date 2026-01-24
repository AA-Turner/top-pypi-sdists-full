from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pandas as pd
import pytest

from lumibot.entities.asset import Asset
from lumibot.tools import thetadata_helper


def test_snapshot_cache_placeholder_does_not_refetch_full_session(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """
    Regression test (acceptance gate invariant)
    -------------------------------------------
    When a full-session snapshot cache is a negative cache (all rows missing=True), we must NOT
    attempt a "refetch to cover full session". Doing so would enqueue Data Downloader work on
    every CI run even though S3 is warm (with the placeholder), violating the warm-cache
    acceptance invariant.
    """

    # Keep everything local + deterministic. We only care that the function does not call the
    # downloader fetch path when the cache represents a stable negative result.
    class _StubCache:
        enabled = False

    monkeypatch.setattr(thetadata_helper, "get_backtest_cache", lambda: _StubCache())
    monkeypatch.setattr(thetadata_helper, "get_trading_dates", lambda *_args, **_kwargs: [date(2025, 10, 1)])
    monkeypatch.setattr(thetadata_helper, "_compute_session_bounds", lambda *_args, **_kwargs: ("09:30:00", "16:00:00"))

    def _unexpected_fetch(*_args, **_kwargs):
        raise AssertionError("Unexpected get_historical_data() call for placeholder-only snapshot cache")

    monkeypatch.setattr(thetadata_helper, "get_historical_data", _unexpected_fetch)

    # Point the cache folder at the temp dir (thetadata_helper builds cache paths from this global).
    monkeypatch.setattr(thetadata_helper, "LUMIBOT_CACHE_FOLDER", str(tmp_path))

    asset = Asset(
        symbol="UBER",
        asset_type="option",
        expiration=date(2028, 1, 21),
        strike=115.0,
        right="CALL",
    )

    cache_file = thetadata_helper.build_snapshot_cache_filename(
        asset,
        trading_day=date(2025, 10, 1),
        interval_label="1m",
        start_time="09:30:00",
        end_time="16:00:00",
        datastyle="quote",
    )
    cache_file.parent.mkdir(parents=True, exist_ok=True)

    # Match the placeholder shape written by `update_cache(...)` (datetime column + missing=True).
    df_placeholder = pd.DataFrame(
        [
            {
                "datetime": pd.Timestamp("2025-10-01 20:00:00+00:00"),
                "open": None,
                "high": None,
                "low": None,
                "close": None,
                "volume": None,
                "missing": True,
            }
        ]
    )
    df_placeholder.to_parquet(cache_file, engine="pyarrow", compression="snappy")

    # Any dt-window inside the day is fine; the important part is that the cache is placeholder-only.
    start_dt = datetime(2025, 10, 1, 9, 30)
    end_dt = datetime(2025, 10, 1, 9, 35)
    df = thetadata_helper.get_historical_data_snapshot_cached(
        asset,
        start_dt,
        end_dt,
        60_000,
        datastyle="quote",
        include_after_hours=True,
        prefer_full_session=True,
    )

    assert df is not None
    assert not df.empty
    assert "missing" in df.columns
    assert bool(df["missing"].fillna(False).astype(bool).all())

