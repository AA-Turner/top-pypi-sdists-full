"""Tests for _get_feature_slug."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import _get_feature_slug


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_get_feature_slug_returns_default_when_context_missing(mock_get_workflow_state) -> None:
    mock_get_workflow_state.return_value = {}

    assert _get_feature_slug() == "default-feature"


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_workflow_state")
def test_get_feature_slug_sanitizes_and_truncates_context_value(mock_get_workflow_state) -> None:
    mock_get_workflow_state.return_value = {"context": {"feature_slug": "x" * 50}}

    assert _get_feature_slug() == "x" * 40
