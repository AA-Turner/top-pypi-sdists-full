"""Tests for ``get_model_metadata``."""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from agentic_devtools.cli.config.project_config import get_model_metadata

_FRESH_TIMESTAMP = (datetime.now(timezone.utc) - timedelta(days=1)).replace(microsecond=0).isoformat()

_VALID_ENTRY = {
    "modelId": "claude-opus-4.8",
    "surfaces": {
        "copilot": {"modelId": "claude-opus-4.8"},
        "vscode": {"displayName": "claude-opus-4.8"},
        "docs": {"displayName": "claude-opus-4.8"},
    },
    "inputRatePerM": 3,
    "outputRatePerM": 15,
    "currency": "USD",
    "rateUnit": "USD per 1M tokens",
    "assumedInputTokens": 100_000,
    "assumedOutputTokens": 10_000,
    "modelledSessionCost": "0.45",
    "priceCategory": "standard",
    "provenance": "curated",
    "costDataAsOf": _FRESH_TIMESTAMP,
}


class TestGetModelMetadata:
    """Tests for the model metadata accessor."""

    def test_blank_model_id_returns_none(self):
        assert get_model_metadata("   ") is None

    def test_non_string_model_id_returns_none(self):
        assert get_model_metadata(42) is None  # type: ignore[arg-type]

    def test_models_not_dict_returns_none(self):
        with patch(
            "agentic_devtools.cli.config.project_config.load_project_config",
            return_value={"models": "bad"},
        ):
            assert get_model_metadata("alpha") is None

    def test_model_entry_not_dict_returns_none(self):
        with patch(
            "agentic_devtools.cli.config.project_config.load_project_config",
            return_value={"models": {"alpha": "not-a-dict"}},
        ):
            assert get_model_metadata("alpha") is None

    def test_invalid_model_entry_returns_none(self):
        with patch(
            "agentic_devtools.cli.config.project_config.load_project_config",
            return_value={"models": {"alpha": {"modelId": "alpha", "surfaces": {"copilot": "bad"}}}},
        ):
            assert get_model_metadata("alpha") is None

    def test_valid_entry_is_returned(self):
        with patch(
            "agentic_devtools.cli.config.project_config.load_project_config",
            return_value={"models": {"claude-opus-4.8": _VALID_ENTRY}},
        ):
            result = get_model_metadata("claude-opus-4.8")
            assert result is not None
            assert result["modelId"] == "claude-opus-4.8"
