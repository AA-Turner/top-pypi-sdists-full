"""Tests for complete throttle lookup response validation."""

import json

import pytest

from agentic_devtools.cli.ci.dispatcher_policy import _parse_workflow_run


@pytest.mark.parametrize(
    ("body", "message"),
    [
        (b"\xff", "without a JSON response"),
        (b"not JSON", "without a JSON response"),
        (b"[]", "invalid JSON response"),
        (b"{}", "missing workflow_runs"),
        (b'{"workflow_runs":{}}', "invalid workflow_runs"),
        (b'{"workflow_runs":[null]}', "invalid workflow run"),
        (b'{"workflow_runs":[{}]}', "invalid updated_at value"),
        (b'{"workflow_runs":[{"updated_at":12}]}', "invalid updated_at value"),
        (b'{"workflow_runs":[{"updated_at":" "}]}', "invalid updated_at value"),
        (b'{"workflow_runs":[{"updated_at":"invalid"}]}', "invalid updated_at timestamp"),
    ],
)
def test_refuses_unknown_run_state(body, message):
    with pytest.raises(RuntimeError, match=message):
        _parse_workflow_run(body)


def test_accepts_empty_history():
    assert _parse_workflow_run(b'{"workflow_runs":[]}') == {}


def test_returns_validated_latest_run():
    run = {"status": "completed", "updated_at": "2026-10-25T12:00:00Z"}
    assert _parse_workflow_run(json.dumps({"workflow_runs": [run]}).encode()) == run
