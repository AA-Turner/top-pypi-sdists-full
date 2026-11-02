"""Tests for emit_routing_record (issue #2117)."""

import json

from agentic_devtools.cli.jira import create_epic_router
from agentic_devtools.cli.jira.create_epic_router import emit_routing_record


def test_tree_record_includes_file_path(capsys):
    emit_routing_record(create_epic_router.MODE_TREE, create_epic_router.BASIS_FILE_PRESENT, file_path="plan.json")
    out = capsys.readouterr().out
    assert out.endswith("\n")
    assert out.count("\n") == 1
    record = json.loads(out)
    assert record == {
        "event": create_epic_router.ROUTING_EVENT,
        "mode": "tree",
        "basis": "file_present",
        "file_path": "plan.json",
    }


def test_legacy_record_omits_file_path(capsys):
    emit_routing_record(create_epic_router.MODE_LEGACY, create_epic_router.BASIS_LEGACY_PRESENT)
    record = json.loads(capsys.readouterr().out)
    assert record == {
        "event": create_epic_router.ROUTING_EVENT,
        "mode": "legacy",
        "basis": "legacy_state_present",
    }
