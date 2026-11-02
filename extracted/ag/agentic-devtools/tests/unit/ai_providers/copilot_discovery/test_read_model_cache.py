import json
import time
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from agentic_devtools.ai_providers.copilot_discovery import read_model_cache

_ENTRY = {"modelId": "gpt-5-mini", "name": "GPT-5 mini"}


def _write(cache_path: Path, payload: object) -> None:
    cache_path.write_text(json.dumps(payload), encoding="utf-8")


def test_returns_records_for_a_fresh_cache(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 1000.0, "models": [_ENTRY]})

    records = read_model_cache(cache_path=cache_path, now=1100.0)

    assert records is not None
    assert len(records) == 1
    assert records[0].model_id == "gpt-5-mini"
    assert records[0].source == "acp-cache"
    assert records[0].observed_at == datetime.fromtimestamp(1000.0, UTC).isoformat()


def test_redacts_credentials_from_a_cache_before_normalization(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(
        cache_path,
        {
            "version": 1,
            "fetchedAt": 1000.0,
            "models": [dict(_ENTRY, token="secret-value", nested={"apiKey": "nested-secret"})],
        },
    )

    records = read_model_cache(cache_path=cache_path, now=1000.0)

    assert records is not None
    metadata = records[0].raw_metadata
    assert isinstance(metadata, Mapping)
    assert metadata["token"] == "<redacted>"
    nested = metadata["nested"]
    assert isinstance(nested, Mapping)
    assert nested["apiKey"] == "<redacted>"


def test_uses_wall_clock_time_when_no_clock_is_injected(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": time.time(), "models": [_ENTRY]})

    assert read_model_cache(cache_path=cache_path) is not None


def test_returns_none_for_an_expired_cache(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 1000.0, "models": [_ENTRY]})

    assert read_model_cache(cache_path=cache_path, ttl_seconds=900, now=2000.0) is None


def test_returns_none_for_a_cache_written_in_the_future(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 5000.0, "models": [_ENTRY]})

    assert read_model_cache(cache_path=cache_path, now=1000.0) is None


def test_returns_an_expired_cache_when_stale_reads_are_allowed(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 1000.0, "models": [_ENTRY]})

    records = read_model_cache(cache_path=cache_path, allow_stale=True, now=999999.0)

    assert records is not None
    assert len(records) == 1
    assert records[0].model_id == "gpt-5-mini"
    assert records[0].source == "acp-cache"
    assert records[0].observed_at == datetime.fromtimestamp(1000.0, UTC).isoformat()


def test_rejects_future_timestamp_even_when_stale_reads_are_allowed(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 5000.0, "models": [_ENTRY]})

    assert read_model_cache(cache_path=cache_path, allow_stale=True, now=1000.0) is None


def test_returns_none_when_the_cache_is_missing(tmp_path: Path) -> None:
    assert read_model_cache(cache_path=tmp_path / "missing.json") is None


def test_returns_none_for_malformed_json(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    cache_path.write_text("{not json", encoding="utf-8")

    assert read_model_cache(cache_path=cache_path) is None


def test_returns_none_for_a_non_object_payload(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, ["not", "an", "object"])

    assert read_model_cache(cache_path=cache_path) is None


def test_returns_none_when_the_model_list_is_not_a_list(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 1000.0, "models": {}})

    assert read_model_cache(cache_path=cache_path, now=1000.0) is None


def test_returns_none_when_the_schema_version_is_missing_or_unsupported(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"fetchedAt": 1000.0, "models": [_ENTRY]})

    assert read_model_cache(cache_path=cache_path, now=1000.0) is None

    _write(cache_path, {"version": 999, "fetchedAt": 1000.0, "models": [_ENTRY]})

    assert read_model_cache(cache_path=cache_path, now=1000.0) is None


def test_returns_none_when_the_timestamp_is_invalid(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": True, "models": [_ENTRY]})

    assert read_model_cache(cache_path=cache_path) is None

    _write(cache_path, {"version": 1, "fetchedAt": "1000", "models": [_ENTRY]})

    assert read_model_cache(cache_path=cache_path) is None


def test_returns_none_when_no_entry_is_usable(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 1000.0, "models": ["junk"]})

    assert read_model_cache(cache_path=cache_path, now=1000.0) is None


def test_defaults_to_the_shared_cache_path(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 1000.0, "models": [_ENTRY]})

    with patch("agentic_devtools.ai_providers.copilot_discovery.get_cache_path", return_value=cache_path):
        assert read_model_cache(now=1000.0) is not None


def test_returns_none_when_the_timestamp_is_nan_or_infinite(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    cache_path.write_text(
        json.dumps({"version": 1, "fetchedAt": float("nan"), "models": [_ENTRY]}, allow_nan=True),
        encoding="utf-8",
    )
    assert read_model_cache(cache_path=cache_path) is None

    cache_path.write_text(
        json.dumps({"version": 1, "fetchedAt": float("inf"), "models": [_ENTRY]}, allow_nan=True),
        encoding="utf-8",
    )
    assert read_model_cache(cache_path=cache_path) is None


def test_returns_none_when_a_model_entry_contains_a_non_json_constant(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    cache_path.write_text(
        json.dumps(
            {"version": 1, "fetchedAt": 1000.0, "models": [dict(_ENTRY, latency=float("nan"))]},
            allow_nan=True,
        ),
        encoding="utf-8",
    )

    assert read_model_cache(cache_path=cache_path, now=1000.0) is None


def test_returns_none_when_normalization_raises_validation_error(tmp_path: Path) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 1000.0, "models": [_ENTRY]})

    with patch(
        "agentic_devtools.ai_providers.copilot_discovery._normalize_entries",
        side_effect=ValueError("bad entry"),
    ):
        assert read_model_cache(cache_path=cache_path, now=1000.0) is None


@pytest.mark.parametrize("timestamp_error", [OverflowError, OSError])
def test_returns_none_when_timestamp_conversion_fails(tmp_path: Path, timestamp_error: type[Exception]) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": -1e20, "models": [_ENTRY]})

    with patch("agentic_devtools.ai_providers.copilot_discovery.datetime") as mock_datetime:
        mock_datetime.fromtimestamp.side_effect = timestamp_error("bad timestamp")
        assert read_model_cache(cache_path=cache_path, allow_stale=True, now=0.0) is None


@pytest.mark.parametrize("invalid_ttl", [True, "900", float("nan"), float("inf"), -1.0])
def test_rejects_invalid_ttl_values(tmp_path: Path, invalid_ttl: Any) -> None:
    cache_path = tmp_path / "copilot-models.json"
    _write(cache_path, {"version": 1, "fetchedAt": 1000.0, "models": [_ENTRY]})

    with pytest.raises(ValueError, match="ttl_seconds must be a finite non-negative number"):
        read_model_cache(cache_path=cache_path, ttl_seconds=invalid_ttl, now=1000.0)
