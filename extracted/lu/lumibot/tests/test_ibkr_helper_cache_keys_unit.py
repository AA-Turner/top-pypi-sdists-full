from __future__ import annotations

from datetime import datetime, timezone

from lumibot.entities import Asset


def test_ibkr_helper_separates_cache_by_history_source(monkeypatch, tmp_path):
    import lumibot.tools.ibkr_helper as ibkr_helper

    monkeypatch.setattr(ibkr_helper, "LUMIBOT_CACHE_FOLDER", tmp_path.as_posix())

    calls: list[str] = []

    def fake_queue_request(url: str, querystring, headers=None, timeout=None):
        if url.endswith("/ibkr/iserver/secdef/search"):
            return [{"conid": 123, "sections": [{"secType": "CRYPTO", "exchange": "ZEROHASH"}]}]
        if url.endswith("/ibkr/iserver/marketdata/history"):
            calls.append(str(querystring.get("source")))
            return {
                "data": [
                    {"t": 1700000000000, "o": 1, "h": 2, "l": 1, "c": 2, "v": 10},
                    {"t": 1700000060000, "o": 2, "h": 3, "l": 2, "c": 3, "v": 11},
                ]
            }
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(ibkr_helper, "queue_request", fake_queue_request)

    asset = Asset(symbol="BTC", asset_type="crypto")
    quote = Asset(symbol="USD", asset_type="forex")
    start = datetime.fromtimestamp(1700000000, tz=timezone.utc)
    end = datetime.fromtimestamp(1700000060, tz=timezone.utc)

    df_trades = ibkr_helper.get_price_data(
        asset=asset,
        quote=quote,
        timestep="minute",
        start_dt=start,
        end_dt=end,
        source="Trades",
    )
    assert not df_trades.empty

    df_bidask = ibkr_helper.get_price_data(
        asset=asset,
        quote=quote,
        timestep="minute",
        start_dt=start,
        end_dt=end,
        source="Bid_Ask",
    )
    assert not df_bidask.empty

    assert calls == ["Trades", "Bid_Ask"]

    parquet_files = list((tmp_path / "ibkr").rglob("*.parquet"))
    assert any("TRADES" in path.name for path in parquet_files)
    assert any("BID_ASK" in path.name for path in parquet_files)


def test_ibkr_helper_crypto_venue_is_part_of_cache_key(monkeypatch, tmp_path):
    import lumibot.tools.ibkr_helper as ibkr_helper

    monkeypatch.setattr(ibkr_helper, "LUMIBOT_CACHE_FOLDER", tmp_path.as_posix())

    calls = {"secdef": 0}

    def fake_queue_request(url: str, querystring, headers=None, timeout=None):
        if url.endswith("/ibkr/iserver/secdef/search"):
            calls["secdef"] += 1
            return [
                {"conid": 111, "sections": [{"secType": "CRYPTO", "exchange": "ZEROHASH"}]},
                {"conid": 222, "sections": [{"secType": "CRYPTO", "exchange": "PAXOS"}]},
            ]
        if url.endswith("/ibkr/iserver/marketdata/history"):
            return {"data": [{"t": 1700000000000, "o": 1, "h": 2, "l": 1, "c": 2, "v": 10}]}
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(ibkr_helper, "queue_request", fake_queue_request)

    asset = Asset(symbol="BTC", asset_type="crypto")
    quote = Asset(symbol="USD", asset_type="forex")
    start = datetime.fromtimestamp(1700000000, tz=timezone.utc)
    end = datetime.fromtimestamp(1700000060, tz=timezone.utc)

    monkeypatch.setenv("IBKR_CRYPTO_VENUE", "ZEROHASH")
    df1 = ibkr_helper.get_price_data(asset=asset, quote=quote, timestep="minute", start_dt=start, end_dt=end)
    assert not df1.empty

    monkeypatch.setenv("IBKR_CRYPTO_VENUE", "PAXOS")
    df2 = ibkr_helper.get_price_data(asset=asset, quote=quote, timestep="minute", start_dt=start, end_dt=end)
    assert not df2.empty

    assert calls["secdef"] == 2

    parquet_files = list((tmp_path / "ibkr").rglob("*.parquet"))
    assert any("ZEROHASH" in path.name for path in parquet_files)
    assert any("PAXOS" in path.name for path in parquet_files)
