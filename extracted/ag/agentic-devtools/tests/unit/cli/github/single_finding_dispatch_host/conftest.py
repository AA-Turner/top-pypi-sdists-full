"""Shared valid handoff fixtures for host and CLI unit tests."""

import json
import os
import stat
import time
from pathlib import Path
from subprocess import CompletedProcess, TimeoutExpired
from typing import Any

import pytest

from agentic_devtools.ai_providers.agent_tasks_payload import AgentTasksPayload
from agentic_devtools.cli.github.review_orchestration import Finding, Reservation
from agentic_devtools.cli.github.single_finding_dispatch import (
    AcceptancePersistenceError,
    AcceptedTaskIdentity,
    SingleFindingDispatchAdapter,
    SingleFindingDispatchResult,
    SingleFindingHandoff,
    TaskAcceptance,
    finding_payload_digest,
)
from agentic_devtools.cli.github.single_finding_dispatch_host import (
    GitHubSingleFindingDispatchHost,
    _dispatch_marker,
)

_REPO = "example/project"
_PR_NUMBER = 7
_HEAD_SHA = "a" * 40
_WORKFLOW_LOGIN = "dispatch-user"


class FakeGh:
    def __init__(self, responses: list[object]) -> None:
        self.responses = responses
        self.calls: list[tuple[list[str], dict[str, Any]]] = []

    def __call__(self, args: list[str], **kwargs: Any) -> CompletedProcess[str]:
        self.calls.append((args, kwargs))
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        assert isinstance(response, CompletedProcess)
        return response


def _completed(stdout: str = "", returncode: int = 0, stderr: str = "") -> CompletedProcess[str]:
    return CompletedProcess(["gh"], returncode, stdout, stderr)


def _pr_response(
    *,
    base_ref: str = "main",
    head_ref: str = "feature",
    head_sha: str = _HEAD_SHA,
) -> CompletedProcess[str]:
    return _completed(
        json.dumps(
            {
                "base_ref": base_ref,
                "head_ref": head_ref,
                "head_sha": head_sha,
            }
        )
    )


def _gh_for_current_handoff(
    handoff: SingleFindingHandoff,
    *,
    resolved: bool = False,
    comments: str = "",
    post_response: object | None = None,
) -> FakeGh:
    comments_array = json.dumps([[{"body": comments, "user": {"login": _WORKFLOW_LOGIN}}]] if comments else [[]])
    responses: list[object] = [
        _pr_response(),
        _completed(str(resolved).lower()),
        _completed(comments_array),
        _pr_response(),
        _completed("false"),
    ]
    if post_response is not None:
        responses.append(post_response)
    return FakeGh(responses)


def _gh_for_dispatch_state_change(marker: str, changed_state: str) -> tuple[FakeGh, tuple[str, int]]:
    comments = marker if changed_state in {"marker", "identity-failure"} else "previous comment"
    pages = json.dumps([[{"body": comments, "user": {"login": _WORKFLOW_LOGIN}}], []])
    responses: list[object] = [_pr_response(), _completed("false"), _completed(pages)]
    if changed_state == "marker":
        responses.append(_completed(_WORKFLOW_LOGIN))
    elif changed_state == "identity-failure":
        responses.append(_completed("", returncode=1))
    if changed_state == "head":
        responses.append(_pr_response(head_sha="b" * 40))
    elif changed_state == "thread":
        responses.extend((_pr_response(), _completed("true")))
    expected = {
        "marker": ("already_active", 4),
        "head": ("head_changed", 4),
        "thread": ("already_resolved", 5),
        "identity-failure": ("blocked", 4),
    }
    return FakeGh(responses), expected[changed_state]


def _dispatch(
    state_dir: Path,
    handoff: SingleFindingHandoff,
    payload: AgentTasksPayload,
    gh: FakeGh,
) -> SingleFindingDispatchResult:
    host = GitHubSingleFindingDispatchHost(state_dir, run_safe=gh)
    return SingleFindingDispatchAdapter(host, clock=lambda: 100).dispatch(handoff, payload)


def _dispatch_with_uncertain_retry(
    state_dir: Path,
    handoff: SingleFindingHandoff,
    payload: AgentTasksPayload,
    first_gh: FakeGh,
) -> SingleFindingDispatchResult:
    first_result = _dispatch(state_dir, handoff, payload, first_gh)
    retry_gh = FakeGh([_pr_response(), _completed("false"), _completed("[[]]")])
    retry_result = _dispatch(state_dir, handoff, payload, retry_gh)

    assert retry_result.outcome == "acceptance_unknown"
    assert len(retry_gh.calls) == 3
    assert all("POST" not in args for args, _ in retry_gh.calls)
    return first_result


def _assert_prior_attempt_guard_branches(
    host: GitHubSingleFindingDispatchHost,
    handoff: SingleFindingHandoff,
    record_path: Path,
) -> None:
    assert host._check_prior_uncertain_attempt(handoff) is None
    record_path.write_text("{", encoding="utf-8")
    malformed_json = host._check_prior_uncertain_attempt(handoff)
    assert malformed_json is not None and malformed_json.outcome == "blocked"
    record_path.write_text("[]", encoding="utf-8")
    malformed_record = host._check_prior_uncertain_attempt(handoff)
    assert malformed_record is not None and malformed_record.outcome == "blocked"
    record_path.write_text("{}", encoding="utf-8")
    missing_outcome = host._check_prior_uncertain_attempt(handoff)
    assert missing_outcome is not None and missing_outcome.outcome == "blocked"
    record_path.write_text('{"outcome":"unrecognized"}', encoding="utf-8")
    invalid_outcome = host._check_prior_uncertain_attempt(handoff)
    assert invalid_outcome is not None and invalid_outcome.outcome == "blocked"


def _assert_durable_persistence(
    host: GitHubSingleFindingDispatchHost,
    handoff: SingleFindingHandoff,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from agentic_devtools.cli.github import single_finding_dispatch_host as module
    from agentic_devtools.cli.github.single_finding_dispatch import AcceptancePersistenceError, TaskAcceptance

    original_replace = os.replace
    original_open = os.open
    original_fsync = os.fsync
    replacements: list[tuple[Path, Path]] = []
    opened_directories: dict[int, Path] = {}
    synced_directories: list[Path] = []

    def track_replace(source: str | os.PathLike[str], destination: str | os.PathLike[str]) -> None:
        source_path, destination_path = Path(source), Path(destination)
        replacements.append((source_path, destination_path))
        original_replace(source_path, destination_path)

    def track_open(path: str | os.PathLike[str], flags: int, *args: Any, **kwargs: Any) -> int:
        file_descriptor = original_open(path, flags, *args, **kwargs)
        if stat.S_ISDIR(os.fstat(file_descriptor).st_mode):
            opened_directories[file_descriptor] = Path(path)
        return file_descriptor

    def track_fsync(file_descriptor: int) -> None:
        directory = opened_directories.pop(file_descriptor, None)
        if directory is not None:
            synced_directories.append(directory)
        original_fsync(file_descriptor)

    monkeypatch.setattr(module.os, "replace", track_replace)
    monkeypatch.setattr(module.os, "open", track_open)
    monkeypatch.setattr(module.os, "fsync", track_fsync)
    assert host.persist_acceptance(handoff, TaskAcceptance("blocked", None, "not dispatched"), 1) is True

    assert len(replacements) == 1
    assert replacements[0][0].parent == replacements[0][1].parent
    assert not replacements[0][0].exists()
    assert synced_directories == [replacements[0][1].parent]
    _assert_prior_attempt_guard_branches(host, handoff, replacements[0][1])

    def fail_directory_fsync(file_descriptor: int) -> None:
        if stat.S_ISDIR(os.fstat(file_descriptor).st_mode):
            raise OSError("directory sync failed")
        original_fsync(file_descriptor)

    monkeypatch.setattr(module.os, "fsync", fail_directory_fsync)
    with pytest.raises(AcceptancePersistenceError, match="directory sync failed"):
        host.persist_acceptance(handoff, TaskAcceptance("blocked", None, "not dispatched"), 1)

    assert not host._reservation_contexts


@pytest.fixture(autouse=True)
def _host_test_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from agentic_devtools.cli.github import single_finding_dispatch_host as module

    monkeypatch.setattr(module, "_RESERVATION_LOCK_ROOT", tmp_path / "dispatch-locks", raising=False)
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "test-workflow-token")
    monkeypatch.delenv("GH_TOKEN", raising=False)
    monkeypatch.delenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", raising=False)


@pytest.fixture
def handoff_and_payload() -> tuple[SingleFindingHandoff, AgentTasksPayload]:
    finding = Finding(
        review_id=1,
        reviewer_id=2,
        comment_id=3,
        suppressed_body=None,
        thread_id="PRRT_kwDOExample",
        path="src/example.py",
        side="RIGHT",
        supporting_files=(),
        side_effects=("branch-write",),
        status="reserved",
        attempt_id="attempt-1",
        task_id=None,
        session_id=None,
    )
    pr_url = f"https://github.com/{_REPO}/pull/{_PR_NUMBER}"
    finding_id = finding.identity(pr_url)
    payload = AgentTasksPayload(
        prompt="repair one finding",
        model="gpt-5.6-luna",
        base_ref="main",
        head_ref="feature",
        custom_agent="agdt.address-copilot-review.evaluate-and-respond",
        create_pull_request=False,
    )
    handoff = SingleFindingHandoff.model_validate(
        {
            "run_id": "00000000-0000-4000-8000-000000000001",
            "pr_url": pr_url,
            "base_ref": "main",
            "head_ref": "feature",
            "expected_head": _HEAD_SHA,
            "finding_id": finding_id,
            "payload_digest": finding_payload_digest(finding_id, payload),
            "attempt_id": "attempt-1",
            "deadline_at": 200,
            "reservation": Reservation(
                finding_id=finding_id,
                attempt_id="attempt-1",
                head_sha=_HEAD_SHA,
                resources=("effect:branch-write", "file:src/example.py"),
            ),
            "finding": finding.model_dump(),
            "authorized_actions": ("repair",),
            "remaining_failure_budgets": {
                "throttling": 3,
                "transport": 3,
                "credential": 1,
                "oauth": 1,
                "repair": 2,
            },
        }
    )
    return handoff, payload


@pytest.fixture
def handoff(handoff_and_payload: tuple[SingleFindingHandoff, AgentTasksPayload]) -> SingleFindingHandoff:
    return handoff_and_payload[0]


@pytest.fixture
def payload(handoff_and_payload: tuple[SingleFindingHandoff, AgentTasksPayload]) -> AgentTasksPayload:
    return handoff_and_payload[1]


def _assert_post_and_persist(
    tmp_path: Path,
    handoff: SingleFindingHandoff,
    payload: AgentTasksPayload,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from agentic_devtools.cli.github import single_finding_dispatch_host as module

    monkeypatch.setenv("GH_TOKEN", "unrelated-ambient-token")
    monkeypatch.setenv("GH_HOST", "github.enterprise.example")
    gh = _gh_for_current_handoff(handoff, post_response=_completed("987654"))
    host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=gh)
    monkeypatch.setattr(module.time, "monotonic", lambda: 100.0 if len(gh.calls) < 6 else 201.0)
    result = SingleFindingDispatchAdapter(host, clock=lambda: 100).dispatch(handoff, payload)
    assert result.outcome == "acceptance_unknown"
    assert (result.task_id, result.session_id) == (None, None)
    assert host._comment_ids == {}
    post_calls = [(args, kwargs) for args, kwargs in gh.calls if "POST" in args]
    assert len(post_calls) == 1
    args, kwargs = post_calls[0]
    assert all(
        call_kwargs["env"]["GH_TOKEN"] == "test-workflow-token" and call_args[1:3] == ["--hostname", "github.com"]
        for call_args, call_kwargs in gh.calls
    )
    assert os.environ["GH_TOKEN"] == "unrelated-ambient-token"
    assert kwargs["shell"] is False
    timeout = kwargs["timeout"]
    assert isinstance(timeout, float)
    assert 0 < timeout <= 100
    thread_args = gh.calls[1][0]
    assert thread_args[thread_args.index("-f") + 1] == f"id={handoff.finding.thread_id}"
    assert "-F" not in thread_args
    assert args[args.index("--input") + 1] == "-"
    body_input = kwargs["input"]
    assert isinstance(body_input, str)
    body = json.loads(body_input)["body"]
    assert body.startswith("@copilot\n\nrepair one finding")
    assert _dispatch_marker(handoff) in body
    records = list((tmp_path / "dispatch-attempts").glob("*.json"))
    assert len(records) == 1
    record = json.loads(records[0].read_text(encoding="utf-8"))
    assert record["attempt_id"] == handoff.attempt_id
    assert (record["comment_id"], record["task_id"], record["session_id"]) == (987654, None, None)
    guard = next((tmp_path / "dispatch-locks" / "unresolved-deliveries").glob("*.json"))
    assert json.loads(guard.read_text(encoding="utf-8"))["comment_id"] is None


def _assert_accepted_replay_preserves_identity(
    tmp_path: Path,
    handoff: SingleFindingHandoff,
    payload: AgentTasksPayload,
) -> None:
    host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
    accepted = TaskAcceptance("accepted", AcceptedTaskIdentity("task-accepted", "session-accepted"), "accepted")
    assert host.persist_acceptance(handoff, accepted, 1)
    retry_gh = FakeGh([_pr_response(), _completed("false"), _completed("[[]]"), _pr_response(), _completed("false")])
    result = _dispatch(tmp_path, handoff, payload, retry_gh)
    record = json.loads(next((tmp_path / "dispatch-attempts").glob("*.json")).read_text(encoding="utf-8"))
    assert result.outcome == "already_active"
    assert all("POST" not in args for args, _ in retry_gh.calls)
    assert (record["task_id"], record["session_id"]) == ("task-accepted", "session-accepted")
    _assert_review_regressions(tmp_path, handoff, payload)


def _assert_unknown_replay_preserves_identity(
    tmp_path: Path,
    handoff: SingleFindingHandoff,
    payload: AgentTasksPayload,
) -> None:
    host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
    identity = AcceptedTaskIdentity("task-observed", "session-observed")
    assert host.persist_acceptance(handoff, TaskAcceptance("unknown", identity, "delivery is uncertain"), 1)
    record_path = next((tmp_path / "dispatch-attempts").glob("*.json"))
    before = json.loads(record_path.read_text(encoding="utf-8"))

    retry_gh = FakeGh([_pr_response(), _completed("false"), _completed("[[]]")])
    result = _dispatch(tmp_path, handoff, payload, retry_gh)

    after = json.loads(record_path.read_text(encoding="utf-8"))
    assert result.outcome == "acceptance_unknown"
    assert (result.task_id, result.session_id) == ("task-observed", "session-observed")
    assert (after["task_id"], after["session_id"]) == (before["task_id"], before["session_id"])


def _assert_malformed_unknown_identity_is_not_rewritten(
    tmp_path: Path,
    handoff: SingleFindingHandoff,
    payload: AgentTasksPayload,
) -> None:
    host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
    assert host.persist_acceptance(
        handoff,
        TaskAcceptance("unknown", AcceptedTaskIdentity("task-observed", "session-observed"), "delivery is uncertain"),
        1,
    )
    record_path = next((tmp_path / "dispatch-attempts").glob("*.json"))
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["task_id"] = "unsafe task id"
    record_path.write_text(json.dumps(record), encoding="utf-8")
    before = record_path.read_bytes()

    retry_gh = FakeGh([_pr_response(), _completed("false"), _completed("[[]]")])
    result = _dispatch(tmp_path, handoff, payload, retry_gh)

    assert result.outcome == "blocked"
    assert record_path.read_bytes() == before


def _assert_review_regressions(
    tmp_path: Path,
    handoff: SingleFindingHandoff,
    payload: AgentTasksPayload,
) -> None:
    for path in (tmp_path / "dispatch-locks" / "unresolved-deliveries").glob("*.json"):
        path.unlink()
    marker = _dispatch_marker(handoff)
    spoofed = FakeGh(
        [
            _pr_response(),
            _completed("false"),
            _completed(json.dumps([[{"body": marker, "user": {"login": "untrusted-user"}}]])),
            _completed(_WORKFLOW_LOGIN),
            _pr_response(),
            _completed("false"),
            _completed("987654"),
        ]
    )
    assert _dispatch(tmp_path / "spoofed", handoff, payload, spoofed).outcome == "acceptance_unknown"
    assert sum("POST" in args for args, _ in spoofed.calls) == 1
    next((tmp_path / "dispatch-locks" / "unresolved-deliveries").glob("*.json")).unlink()
    failed_identity, _ = _gh_for_dispatch_state_change(marker, "identity-failure")
    assert _dispatch(tmp_path / "identity-failed", handoff, payload, failed_identity).outcome == "blocked"

    for index, changed in enumerate(("head", "thread")):
        gh, (expected, _) = _gh_for_dispatch_state_change(marker, changed)
        state_dir = tmp_path / f"final-check-{index}"
        result = _dispatch(state_dir, handoff, payload, gh)
        assert result.outcome == expected and not any("POST" in args for args, _ in gh.calls)
        record = json.loads(next((state_dir / "dispatch-attempts").glob("*.json")).read_text(encoding="utf-8"))
        assert record["outcome"] == expected

    _assert_unknown_replay_preserves_identity(tmp_path / "identity", handoff, payload)
    _assert_malformed_unknown_identity_is_not_rewritten(tmp_path / "malformed", handoff, payload)
    invalid_guard_host = GitHubSingleFindingDispatchHost(tmp_path / "invalid-guard", run_safe=FakeGh([]))
    assert invalid_guard_host.reserve_branch_write(handoff, 1)
    invalid_guard = invalid_guard_host._attempt_state.unresolved_guard_path(handoff)
    invalid_guard.parent.mkdir(parents=True, exist_ok=True)
    invalid_guard.write_text("{", encoding="utf-8")
    invalid_guard_result = invalid_guard_host._check_unresolved_guard(handoff)
    assert invalid_guard_result is not None and invalid_guard_result.outcome == "blocked"
    assert not invalid_guard_host._reservation_contexts
    invalid_guard.unlink()

    uncertain = _gh_for_current_handoff(handoff, post_response=TimeoutExpired(["gh"], 1))
    assert _dispatch(tmp_path / "owner", handoff, payload, uncertain).outcome == "acceptance_unknown"
    next_handoff = handoff.model_copy(
        update={
            "run_id": "00000000-0000-4000-8000-000000000002",
            "attempt_id": "attempt-2",
            "finding": handoff.finding.model_copy(update={"attempt_id": "attempt-2"}),
            "reservation": handoff.reservation.model_copy(update={"attempt_id": "attempt-2"}),
        }
    )
    retry_gh = FakeGh([_pr_response(), _completed("false"), _completed("[[]]")])
    result = _dispatch(tmp_path / "other-workflow", next_handoff, payload, retry_gh)
    assert result.outcome == "acceptance_unknown"


def _assert_release_clears_unpersisted_comment_id(
    tmp_path: Path,
    handoff: SingleFindingHandoff,
    payload: AgentTasksPayload,
) -> None:
    host = GitHubSingleFindingDispatchHost(
        tmp_path, run_safe=_gh_for_current_handoff(handoff, post_response=_completed("987654"))
    )
    assert host.reserve_branch_write(handoff, 2)
    assert host.create_task_if_head(handoff, payload, 2).outcome == "unknown"
    assert host._comment_ids
    host.release_branch_write(handoff)
    assert host._comment_ids == {}


def _assert_reconciliation_failure_does_not_escape(
    tmp_path: Path,
    handoff: SingleFindingHandoff,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
    assert host.reserve_branch_write(handoff, 1)

    def fail_reconciliation(
        _handoff: SingleFindingHandoff,
        _acceptance: TaskAcceptance,
        _timeout: int,
        *,
        record_outcome: str | None = None,
    ) -> bool:
        if record_outcome == "blocked":
            raise AcceptancePersistenceError("reconciliation failed")
        return True

    def fail_to_start(*args: object, **kwargs: Any) -> CompletedProcess[str]:
        raise OSError("could not start GitHub CLI")

    monkeypatch.setattr(host._attempt_state, "persist_acceptance", fail_reconciliation)
    monkeypatch.setattr(host, "_run_gh", fail_to_start)
    acceptance = host._post_comment(handoff, "example/project", 7, "body", time.monotonic() + 10)

    assert acceptance.outcome == "blocked"
    assert not host._reservation_contexts
