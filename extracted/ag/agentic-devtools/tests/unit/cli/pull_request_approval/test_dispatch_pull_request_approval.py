from __future__ import annotations

import threading

from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalRequest, PullRequestApprovalResult
from agentic_devtools.cli import pull_request_approval as commands


def test_dispatches_to_selected_adapter(monkeypatch) -> None:
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    expected = PullRequestApprovalResult(True, "github", "approved")
    adapter = type("Adapter", (), {"approve": lambda self, _: expected})()
    monkeypatch.setattr(commands, "_adapter_for", lambda _: adapter)
    assert commands.dispatch_pull_request_approval(request) == expected


def test_converts_adapter_errors_to_failed_result(monkeypatch) -> None:
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    monkeypatch.setattr(commands, "_adapter_for", lambda _: (_ for _ in ()).throw(RuntimeError("boom")))
    result = commands.dispatch_pull_request_approval(request)
    assert result.success is False
    assert result.status == "failed"


def test_sanitizes_adapter_errors_in_failed_result(monkeypatch) -> None:
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    monkeypatch.setenv("GH_TOKEN", "super-secret-token")
    monkeypatch.setattr(
        commands,
        "_adapter_for",
        lambda _: (_ for _ in ()).throw(RuntimeError("approval failed for super-secret-token")),
    )
    result = commands.dispatch_pull_request_approval(request)
    assert result.success is False
    assert result.status == "failed"
    assert "super-secret-token" not in result.error
    assert "[REDACTED]" in result.error


def test_converts_system_exit_to_failed_result(monkeypatch) -> None:
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    monkeypatch.setattr(commands, "_adapter_for", lambda _: (_ for _ in ()).throw(SystemExit(1)))
    result = commands.dispatch_pull_request_approval(request)
    assert result.success is False
    assert result.status == "failed"
    assert "readiness check exited with code 1" in result.error


def test_serializes_concurrent_approvals_for_the_same_target(monkeypatch, tmp_path) -> None:
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    monkeypatch.setattr(commands.Path, "home", lambda: tmp_path)
    first_entered = threading.Event()
    release_first = threading.Event()
    second_entered = threading.Event()
    count_lock = threading.Lock()
    calls = 0

    class Adapter:
        def approve(self, _request):
            nonlocal calls
            with count_lock:
                calls += 1
                call_number = calls
            if call_number == 1:
                first_entered.set()
                assert release_first.wait(2)
            else:
                second_entered.set()
            return PullRequestApprovalResult(True, "github", "approved")

    monkeypatch.setattr(commands, "_adapter_for", lambda _: Adapter())
    first = threading.Thread(target=commands.dispatch_pull_request_approval, args=(request,))
    second = threading.Thread(target=commands.dispatch_pull_request_approval, args=(request,))
    first.start()
    assert first_entered.wait(1)
    second.start()
    assert not second_entered.wait(0.1)
    release_first.set()
    first.join(2)
    second.join(2)
    assert not first.is_alive()
    assert not second.is_alive()
    assert second_entered.is_set()
