"""Tests for resolve_thread function."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.commands import resolve_thread


class TestResolveThread:
    """Tests for resolve_thread command."""

    def test_delegates_to_provider_neutral_implementation(self, temp_state_dir, clear_state_before):
        """Test that resolve_thread delegates to the provider-agnostic implementation."""
        mock_result = MagicMock()
        with patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread",
            return_value=mock_result,
        ) as mock_new_resolve:
            result = resolve_thread()
            mock_new_resolve.assert_called_once_with(provider="azure_devops")
            assert result is mock_result

    def test_propagates_failed_result(self, temp_state_dir, clear_state_before):
        """Test that a failed resolution result is propagated unchanged."""
        mock_result = MagicMock()
        mock_result.success = False
        with patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread",
            return_value=mock_result,
        ):
            result = resolve_thread()
            assert result is mock_result
            assert result.success is False
