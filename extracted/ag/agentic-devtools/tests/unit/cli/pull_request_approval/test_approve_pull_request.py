from __future__ import annotations

import json

from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalResult
from agentic_devtools.cli import pull_request_approval as commands


def test_prints_result(monkeypatch, capsys) -> None:
    result = PullRequestApprovalResult(True, "github", "approved")
    monkeypatch.setattr(commands, "_build_approval_request", lambda **_: object())
    monkeypatch.setattr(commands, "dispatch_pull_request_approval", lambda _: result)
    assert commands.approve_pull_request()["status"] == "approved"
    assert json.loads(capsys.readouterr().out)["success"] is True
