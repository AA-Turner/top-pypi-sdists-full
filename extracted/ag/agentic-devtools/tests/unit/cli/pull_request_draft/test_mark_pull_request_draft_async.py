from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.pull_request_draft import PullRequestDraftRequest
from agentic_devtools.cli import pull_request_draft as commands


def test_starts_background_task(monkeypatch, capsys) -> None:
    task_calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

    def run_task(*args: object, **kwargs: object) -> SimpleNamespace:
        task_calls.append((args, kwargs))
        return SimpleNamespace(id="task")

    monkeypatch.setattr(
        commands,
        "build_draft_request",
        lambda **_kwargs: PullRequestDraftRequest("github", "owner/repo", 42),
    )
    monkeypatch.setattr(commands, "run_function_in_background", run_task)
    monkeypatch.setattr(commands, "print_task_tracking_info", lambda task, message: print(message))
    commands.mark_pull_request_draft_async()
    assert "Marking pull request as draft" in capsys.readouterr().out
    assert task_calls == [
        (
            (commands._MODULE, "_run_request_snapshot"),
            {
                "command_display_name": "agdt-mark-pull-request-draft",
                "func_kwargs": {
                    "provider": "github",
                    "repository": "owner/repo",
                    "pull_request_id": 42,
                    "dry_run": False,
                    "organization": None,
                    "project": None,
                },
            },
        )
    ]


def test_invalid_request_exits_with_failure_result(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr(commands, "build_draft_request", MagicMock(side_effect=ValueError("bad request")))

    with pytest.raises(SystemExit) as exc_info:
        commands.mark_pull_request_draft_async()

    assert exc_info.value.code == 1
    assert '"status": "invalid"' in capsys.readouterr().out
