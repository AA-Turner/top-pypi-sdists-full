from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalRequest
from agentic_devtools.cli import pull_request_approval as commands


def test_async_snapshots_request(monkeypatch) -> None:
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    monkeypatch.setattr(commands, "_build_approval_request", lambda **_: request)
    runner = MagicMock()
    monkeypatch.setattr(commands, "run_function_in_background", runner)
    monkeypatch.setattr(commands, "print_task_tracking_info", MagicMock())
    commands.approve_pull_request_async()
    assert runner.call_args.kwargs["func_kwargs"] == request.__dict__


def test_async_isolates_concurrent_launches(monkeypatch) -> None:
    """Two detached launches for different PRs must not share mutable snapshot state."""
    first_request = PullRequestApprovalRequest("github", "owner/repo-one", 1, "First LGTM", "a" * 40)
    second_request = PullRequestApprovalRequest("azure_devops", "org/project/repo-two", 2, "Second LGTM")
    requests = iter([first_request, second_request])
    monkeypatch.setattr(commands, "_build_approval_request", lambda **_: next(requests))
    runner = MagicMock(side_effect=["task-1", "task-2"])
    monkeypatch.setattr(commands, "run_function_in_background", runner)
    tracker = MagicMock()
    monkeypatch.setattr(commands, "print_task_tracking_info", tracker)

    commands.approve_pull_request_async(
        provider="github", repository="owner/repo-one", pull_request_id=1, content="First LGTM", expected_head="a" * 40
    )
    commands.approve_pull_request_async(
        provider="azure_devops", repository="org/project/repo-two", pull_request_id=2, content="Second LGTM"
    )

    first_kwargs = runner.call_args_list[0].kwargs["func_kwargs"]
    second_kwargs = runner.call_args_list[1].kwargs["func_kwargs"]
    assert first_kwargs == first_request.__dict__
    assert second_kwargs == second_request.__dict__
    assert first_kwargs is not second_kwargs
    assert first_kwargs["provider"] == "github"
    assert second_kwargs["provider"] == "azure_devops"
    assert first_kwargs["pull_request_id"] == 1
    assert second_kwargs["pull_request_id"] == 2
    assert first_kwargs["expected_head"] == "a" * 40
    assert second_kwargs["expected_head"] is None
    assert tracker.call_args_list[0].args[0] == "task-1"
    assert tracker.call_args_list[1].args[0] == "task-2"
