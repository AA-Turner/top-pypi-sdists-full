"""Tests for _query_copilot_models."""

from unittest.mock import patch

from agentic_devtools.ai_providers.models import ModelRecord
from agentic_devtools.cli.setup.commands import _query_copilot_models

_DISCOVER = "agentic_devtools.ai_providers.copilot_discovery.discover_copilot_models"


def _record(model_id: str) -> ModelRecord:
    return ModelRecord(
        name=model_id,
        model_id=model_id,
        provider="copilot",
        context_window=128000,
        max_output_tokens=None,
        supports_tools=True,
        raw_metadata={"modelId": model_id},
    )


class TestQueryCopilotModels:
    """Tests for _query_copilot_models."""

    def test_returns_model_ids_from_acp_discovery(self):
        """Returns the model ids discovered over ACP."""
        with patch(_DISCOVER, return_value=[_record("gpt-5-mini"), _record("claude-haiku-4.5")]) as mock_discover:
            result = _query_copilot_models()

        assert result == ["gpt-5-mini", "claude-haiku-4.5"]
        mock_discover.assert_called_once_with(refresh=True, allow_stale=False)

    def test_forwards_the_no_refresh_opt_out(self):
        """refresh=False and allow_stale=True are forwarded independently."""
        with patch(_DISCOVER, return_value=[]) as mock_discover:
            result = _query_copilot_models(refresh=False, allow_stale=True)

        assert result == []
        mock_discover.assert_called_once_with(refresh=False, allow_stale=True)

    def test_no_stale_fallback_by_default_when_refresh_is_skipped(self):
        """refresh=False alone does not enable the stale-cache fallback."""
        with patch(_DISCOVER, return_value=[]) as mock_discover:
            result = _query_copilot_models(refresh=False)

        assert result == []
        mock_discover.assert_called_once_with(refresh=False, allow_stale=False)
