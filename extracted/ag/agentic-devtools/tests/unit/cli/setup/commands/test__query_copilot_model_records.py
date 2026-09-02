"""Tests for _query_copilot_model_records."""

from unittest.mock import patch

from agentic_devtools.ai_providers.models import ModelRecord
from agentic_devtools.cli.setup.commands import _query_copilot_model_records

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


class TestQueryCopilotModelRecords:
    """Tests for _query_copilot_model_records."""

    def test_returns_complete_records_and_forwards_default_flags(self) -> None:
        """Returns unmodified ACP records and forwards default query flags."""
        records = [_record("gpt-5-mini"), _record("claude-sonnet-5")]
        with patch(_DISCOVER, return_value=records) as mock_discover:
            result = _query_copilot_model_records()

        assert result == records
        mock_discover.assert_called_once_with(refresh=True, allow_stale=False)

    def test_forwards_refresh_and_stale_flags_independently(self) -> None:
        """Forwards refresh/cache flags without coupling them."""
        with patch(_DISCOVER, return_value=[]) as mock_discover:
            result = _query_copilot_model_records(refresh=False, allow_stale=True)

        assert result == []
        mock_discover.assert_called_once_with(refresh=False, allow_stale=True)
