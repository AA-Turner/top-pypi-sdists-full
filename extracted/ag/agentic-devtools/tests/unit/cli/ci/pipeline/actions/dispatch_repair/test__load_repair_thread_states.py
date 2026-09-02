"""Tests for _load_repair_thread_states()."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import _load_repair_thread_states
from agentic_devtools.cli.ci.review_thread_state import ReviewThreadStates


class TestLoadRepairThreadStates:
    """Tests for optional repair-thread state loading."""

    @patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.fetch_review_thread_states")
    def test_returns_resolved_comment_ids_for_healthy_result(self, mock_fetch) -> None:
        mock_fetch.return_value = ReviewThreadStates(states={101: (True, False), 202: (False, True)})
        provider = MagicMock()

        assert _load_repair_thread_states(provider, 42) == {101}
        mock_fetch.assert_called_once_with(provider, 42)

    @patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.fetch_review_thread_states")
    def test_returns_none_when_lookup_degrades(self, mock_fetch) -> None:
        mock_fetch.return_value = ReviewThreadStates(degraded=True, reason="unsupported")

        assert _load_repair_thread_states(MagicMock(), 42) is None

    @patch("agentic_devtools.cli.ci.pipeline.actions.dispatch_repair.fetch_review_thread_states")
    def test_returns_all_resolved_comment_ids_regardless_of_reply_flag(self, mock_fetch) -> None:
        mock_fetch.return_value = ReviewThreadStates(
            states={101: (True, True), 202: (False, False), 303: (True, False)}
        )

        assert _load_repair_thread_states(MagicMock(), 42) == {101, 303}
