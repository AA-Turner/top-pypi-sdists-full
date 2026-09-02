"""Tests for explicit ACP pricing extraction."""

from datetime import UTC, datetime, timedelta

import pytest

import agentic_devtools.ai_providers.copilot_discovery as copilot_discovery
from agentic_devtools.ai_providers.copilot_discovery import extract_acp_pricing

_PRICING = {
    "inputRatePerM": 1.25,
    "outputRatePerM": 10,
    "currency": "USD",
    "rateUnit": "USD per 1M tokens",
    "assumedInputTokens": 100_000,
    "assumedOutputTokens": 10_000,
    "costDataAsOf": "2026-08-27T00:00:00+00:00",
}


def test_category_only_metadata_is_not_a_price() -> None:
    assert (
        extract_acp_pricing({"modelId": "x", "_meta": {"copilotUsage": "0.33x", "copilotPriceCategory": "low"}}) is None
    )


@pytest.mark.parametrize(
    "value",
    [True, object(), "not-a-decimal", float("inf"), -1],
)
def test_rejects_invalid_numeric_rates(value: object) -> None:
    with pytest.raises(ValueError):
        extract_acp_pricing({**_PRICING, "inputRatePerM": value})


@pytest.mark.parametrize("timestamp", [None, "not-a-timestamp", "2026-08-27T00:00:00"])
def test_rejects_invalid_timestamps(timestamp: object) -> None:
    with pytest.raises(ValueError):
        extract_acp_pricing({**_PRICING, "costDataAsOf": timestamp})


def test_rejects_future_timestamp() -> None:
    future = (datetime.now(UTC) + timedelta(days=1)).isoformat()
    with pytest.raises(ValueError, match="must not be in the future"):
        extract_acp_pricing({**_PRICING, "costDataAsOf": future})


def test_rejects_timestamp_when_timezone_normalization_overflows(monkeypatch) -> None:
    class OverflowingTimestamp:
        tzinfo = object()

        def astimezone(self, timezone):
            raise OverflowError

    monkeypatch.setattr(
        copilot_discovery,
        "datetime",
        type("FakeDatetime", (), {"fromisoformat": staticmethod(lambda value: OverflowingTimestamp())}),
    )
    with pytest.raises(ValueError):
        extract_acp_pricing({**_PRICING, "costDataAsOf": "2026-08-27T00:00:00+00:00"})


def test_accepts_z_suffix_timestamp() -> None:
    result = extract_acp_pricing({**_PRICING, "costDataAsOf": "2026-08-27T00:00:00Z"})
    assert result is not None
    assert result["costDataAsOf"] == "2026-08-27T00:00:00+00:00"


@pytest.mark.parametrize("field", ["currency", "rateUnit"])
def test_rejects_blank_currency_or_rate_unit(field: str) -> None:
    with pytest.raises(ValueError):
        extract_acp_pricing({**_PRICING, field: "  "})


def test_rejects_non_canonical_rate_unit() -> None:
    with pytest.raises(ValueError, match="USD per 1M tokens"):
        extract_acp_pricing({**_PRICING, "rateUnit": "USD per 1K tokens"})


def test_rejects_non_usd_currency() -> None:
    with pytest.raises(ValueError, match="currency must be 'USD'"):
        extract_acp_pricing({**_PRICING, "currency": "EUR"})


def test_rejects_non_mapping_record() -> None:
    with pytest.raises(ValueError, match="must be a mapping"):
        extract_acp_pricing([])  # type: ignore[arg-type]


def test_extracts_complete_record_level_pricing_before_meta() -> None:
    result = extract_acp_pricing(
        {
            "modelId": "x",
            **_PRICING,
            "_meta": {**_PRICING, "inputRatePerM": 99},
        }
    )
    assert result is not None
    assert result["inputRatePerM"] == "1.25"


def test_extracts_complete_meta_pricing() -> None:
    result = extract_acp_pricing({"modelId": "x", "_meta": _PRICING})
    assert result is not None
    assert result["outputRatePerM"] == "10"


@pytest.mark.parametrize(
    "payload",
    [
        {"inputRatePerM": 1},
        {**_PRICING, "outputRatePerM": "NaN"},
        {**_PRICING, "assumedInputTokens": True},
        {**_PRICING, "costDataAsOf": "2026-08-27T00:00:00"},
    ],
)
def test_partial_or_malformed_pricing_is_invalid(payload: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        extract_acp_pricing(payload)
