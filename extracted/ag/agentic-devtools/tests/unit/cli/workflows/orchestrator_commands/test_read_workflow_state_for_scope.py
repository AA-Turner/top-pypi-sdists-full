"""Tests for _read_workflow_state_for_scope."""

import json
from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import _read_workflow_state_for_scope


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
def test_returns_workflow_from_scoped_state_file(mock_get_bootstrap_state, tmp_path) -> None:
    mock_get_bootstrap_state.return_value = {"identity": "abc"}
    state_file = tmp_path / ".agdt" / "workflows" / "abc" / "42" / "state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps({"workflow": {"active": "orchestrate-feature"}}), encoding="utf-8")

    assert _read_workflow_state_for_scope(tmp_path, "42") == {"active": "orchestrate-feature"}


@patch("agentic_devtools.cli.workflows.orchestrator_commands._resolve_identity")
@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
def test_falls_back_to_resolved_identity_when_bootstrap_identity_missing(
    mock_get_bootstrap_state, mock_resolve_identity, tmp_path
) -> None:
    mock_get_bootstrap_state.return_value = {}
    mock_resolve_identity.return_value = "abc"
    state_file = tmp_path / ".agdt" / "workflows" / "abc" / "42" / "state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps({"workflow": {"active": "orchestrate-feature"}}), encoding="utf-8")

    assert _read_workflow_state_for_scope(tmp_path, "42") == {"active": "orchestrate-feature"}


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
def test_uses_unscoped_state_when_scope_is_unsafe(mock_get_bootstrap_state, tmp_path) -> None:
    mock_get_bootstrap_state.return_value = {"identity": "abc"}
    state_file = tmp_path / ".agdt" / "workflows" / "_unscoped" / "state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps({"workflow": {"active": "orchestrate-feature"}}), encoding="utf-8")

    assert _read_workflow_state_for_scope(tmp_path, "../42") == {"active": "orchestrate-feature"}


@patch("agentic_devtools.cli.workflows.orchestrator_commands.get_bootstrap_state")
def test_returns_empty_dict_for_non_mapping_state_or_workflow(mock_get_bootstrap_state, tmp_path) -> None:
    mock_get_bootstrap_state.return_value = {"identity": "abc"}
    state_file = tmp_path / ".agdt" / "workflows" / "abc" / "42" / "state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps([]), encoding="utf-8")

    assert _read_workflow_state_for_scope(tmp_path, "42") == {}

    state_file.write_text(json.dumps({"workflow": "invalid"}), encoding="utf-8")

    assert _read_workflow_state_for_scope(tmp_path, "42") == {}
