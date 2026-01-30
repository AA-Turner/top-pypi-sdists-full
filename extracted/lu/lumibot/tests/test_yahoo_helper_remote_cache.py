from __future__ import annotations

import pickle
from pathlib import Path

import pandas as pd

from lumibot.tools import yahoo_helper


def test_yahoo_helper_hydrates_pickle_via_remote_cache(monkeypatch, tmp_path: Path):
    cache_calls: list[Path] = []

    class FakeCache:
        enabled = True

        def ensure_local_file(self, local_path: Path, *_args, **_kwargs):
            local_path = Path(local_path)
            cache_calls.append(local_path)
            local_path.parent.mkdir(parents=True, exist_ok=True)
            frame = pd.DataFrame({"Close": [1.0]}, index=[pd.Timestamp("2020-01-01")])
            obj = yahoo_helper._YahooData("TEST", "1d", frame)
            with local_path.open("wb") as handle:
                pickle.dump(obj, handle)
            return True

    fake_cache = FakeCache()
    monkeypatch.setattr("lumibot.tools.backtest_cache.get_backtest_cache", lambda: fake_cache)

    monkeypatch.setattr(yahoo_helper.YahooHelper, "LUMIBOT_YAHOO_CACHE_FOLDER", str(tmp_path))
    monkeypatch.setattr(yahoo_helper.YahooHelper, "CACHING_ENABLED", True)

    result = yahoo_helper.YahooHelper.check_pickle_file("TEST", "1d")
    assert result is not None
    assert cache_calls == [tmp_path / "TEST_1d.pickle"]


def test_yahoo_helper_uploads_pickle_via_remote_cache(monkeypatch, tmp_path: Path):
    upload_calls: list[Path] = []

    class FakeCache:
        enabled = True

        def on_local_update(self, local_path: Path, *_args, **_kwargs):
            upload_calls.append(Path(local_path))
            return True

    fake_cache = FakeCache()
    monkeypatch.setattr("lumibot.tools.backtest_cache.get_backtest_cache", lambda: fake_cache)

    monkeypatch.setattr(yahoo_helper.YahooHelper, "LUMIBOT_YAHOO_CACHE_FOLDER", str(tmp_path))
    monkeypatch.setattr(yahoo_helper.YahooHelper, "CACHING_ENABLED", True)

    frame = pd.DataFrame({"Close": [1.0]}, index=[pd.Timestamp("2020-01-01")])
    yahoo_helper.YahooHelper.dump_pickle_file("TEST", "1d", frame)

    expected = tmp_path / "TEST_1d.pickle"
    assert expected.exists()
    assert upload_calls == [expected]

