"""Tests for _helpers.get_run_id."""

from __future__ import annotations

from unittest.mock import patch


class TestGetRunId:
    def test_returns_none_outside_langgraph_context(self):
        """get_run_id returns None when called outside a LangGraph runnable context."""
        from agentic_devtools.orchestration.nodes._helpers import get_run_id

        with patch("langgraph.config.get_config", side_effect=RuntimeError("no context")):
            assert get_run_id() is None

    def test_returns_run_id_string_inside_langgraph_context(self):
        """get_run_id returns the run_id from the LangGraph configurable dict."""
        from agentic_devtools.orchestration.nodes._helpers import get_run_id

        with patch(
            "langgraph.config.get_config",
            return_value={"configurable": {"run_id": "abc-123"}},
        ):
            assert get_run_id() == "abc-123"

    def test_returns_none_when_run_id_absent_from_configurable(self):
        """get_run_id returns None when configurable dict has no run_id key."""
        from agentic_devtools.orchestration.nodes._helpers import get_run_id

        with patch("langgraph.config.get_config", return_value={"configurable": {}}):
            assert get_run_id() is None

    def test_returns_none_when_run_id_is_falsy(self):
        """get_run_id returns None when run_id is present but empty/falsy."""
        from agentic_devtools.orchestration.nodes._helpers import get_run_id

        with patch("langgraph.config.get_config", return_value={"configurable": {"run_id": ""}}):
            assert get_run_id() is None
