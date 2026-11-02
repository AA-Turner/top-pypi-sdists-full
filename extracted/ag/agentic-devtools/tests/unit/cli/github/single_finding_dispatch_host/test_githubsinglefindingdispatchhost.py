"""Tests for the production GitHub single-finding dispatch host."""

import json
import os
import time
from pathlib import Path
from subprocess import CompletedProcess, TimeoutExpired
from typing import Any
from unittest.mock import MagicMock

import pytest

from agentic_devtools.ai_providers.agent_tasks_payload import AgentTasksPayload
from agentic_devtools.cli.github.single_finding_dispatch import (
    AcceptedTaskIdentity,
    SingleFindingDispatchAdapter,
    SingleFindingHandoff,
    TaskAcceptance,
    finding_payload_digest,
)
from agentic_devtools.cli.github.single_finding_dispatch_host import (
    GitHubSingleFindingDispatchHost,
    _dispatch_marker,
    _DispatchDeadlineExpired,
)

from .conftest import (
    _HEAD_SHA,
    FakeGh,
    _assert_accepted_replay_preserves_identity,
    _assert_durable_persistence,
    _assert_post_and_persist,
    _assert_reconciliation_failure_does_not_escape,
    _assert_release_clears_unpersisted_comment_id,
    _completed,
    _dispatch,
    _dispatch_with_uncertain_retry,
    _gh_for_current_handoff,
    _gh_for_dispatch_state_change,
    _pr_response,
)


class TestGitHubSingleFindingDispatchHost:
    def test_rejects_invalid_constructor_and_timeout_values(
        self, tmp_path: Path, handoff: SingleFindingHandoff
    ) -> None:
        with pytest.raises(TypeError, match="state_dir"):
            GitHubSingleFindingDispatchHost("not-a-path")  # type: ignore[arg-type]
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
        with pytest.raises(ValueError, match="timeout_seconds"):
            host.reserve_branch_write(handoff, True)  # type: ignore[arg-type]
        assert host.reserve_branch_write(handoff, 2)
        with pytest.raises(ValueError, match="timeout_seconds"):
            host.persist_acceptance(handoff, TaskAcceptance("blocked", None, "not dispatched"), True)  # type: ignore[arg-type]
        assert host.reserve_branch_write(handoff, 2)
        host.release_branch_write(handoff)

    def test_reserves_and_releases_pr_branch_write_lock(self, tmp_path: Path, handoff: SingleFindingHandoff) -> None:
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
        other_scope = GitHubSingleFindingDispatchHost(tmp_path / "other-workflow", run_safe=FakeGh([]))

        assert host.reserve_branch_write(handoff, 2) is True
        assert list((tmp_path / "dispatch-locks").glob("*.lock"))
        assert host.reserve_branch_write(handoff, 2) is False
        assert other_scope.reserve_branch_write(handoff, 2) is False
        host.release_branch_write(handoff)
        assert other_scope.reserve_branch_write(handoff, 2) is True
        other_scope.release_branch_write(handoff)
        host.release_branch_write(handoff)

    def test_returns_false_when_reservation_is_already_owned(
        self, tmp_path: Path, handoff: SingleFindingHandoff, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from agentic_devtools.cli.github import single_finding_dispatch_host as module
        from agentic_devtools.file_locking import FileLockError

        def fail_to_lock(*args: object, **kwargs: object):
            raise FileLockError("contended")

        monkeypatch.setattr(module, "locked_file", fail_to_lock)
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))

        assert host.reserve_branch_write(handoff, 1) is False

    def test_closes_lock_when_reservation_storage_fails(
        self, tmp_path: Path, handoff: SingleFindingHandoff, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from agentic_devtools.cli.github import single_finding_dispatch_host as module

        context = MagicMock()

        class FailingReservations(dict[str, Any]):
            def __setitem__(self, key: str, value: Any) -> None:
                raise RuntimeError("reservation storage failed")

        monkeypatch.setattr(module, "locked_file", lambda *args, **kwargs: context)
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
        host._reservation_contexts = FailingReservations()

        with pytest.raises(RuntimeError, match="reservation storage failed"):
            host.reserve_branch_write(handoff, 1)

        context.__exit__.assert_called_once()

    def test_adapter_blocks_when_reservation_storage_is_unavailable(
        self, tmp_path: Path, handoff: SingleFindingHandoff, payload: AgentTasksPayload
    ) -> None:
        (tmp_path / "dispatch-locks").write_text("not a directory", encoding="utf-8")
        gh = FakeGh([])
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=gh)

        result = SingleFindingDispatchAdapter(host, clock=lambda: 100).dispatch(handoff, payload)

        assert result.outcome == "blocked"
        assert "branch-write reservation" in result.reason
        assert gh.calls == []

    def test_blocks_create_when_no_reservation_is_held(
        self, tmp_path: Path, handoff: SingleFindingHandoff, payload: AgentTasksPayload
    ) -> None:
        gh = FakeGh([])

        acceptance = GitHubSingleFindingDispatchHost(tmp_path, run_safe=gh).create_task_if_head(handoff, payload, 1)

        assert acceptance.outcome == "blocked"
        assert gh.calls == []

    def test_blocks_when_deadline_expires_before_post_process_starts(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        from agentic_devtools.cli.github import single_finding_dispatch_host as module

        gh = FakeGh([_pr_response(), _completed("false"), _completed("[[]]"), _pr_response(), _completed("false")])
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=gh)
        assert host.reserve_branch_write(handoff, 1) is True
        monkeypatch.setattr(module.time, "monotonic", lambda: 10.0 if len(gh.calls) < 3 else 12.0)

        acceptance = host.create_task_if_head(handoff, payload, 1)

        assert acceptance.outcome == "blocked"
        assert not host._reservation_contexts
        assert len(gh.calls) == 3
        assert all("POST" not in args for args, _ in gh.calls)

    def test_adapter_posts_once_and_persists_comment_before_return(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _assert_post_and_persist(tmp_path, handoff, payload, monkeypatch)

    def test_release_clears_unpersisted_comment_id(
        self, tmp_path: Path, handoff: SingleFindingHandoff, payload: AgentTasksPayload
    ) -> None:
        _assert_release_clears_unpersisted_comment_id(tmp_path, handoff, payload)

    @pytest.mark.parametrize(
        ("pr_response", "expected_outcome"),
        [
            (_pr_response(head_sha="b" * 40), "head_changed"),
            (_pr_response(base_ref="release"), "head_changed"),
            (_pr_response(head_ref="other"), "head_changed"),
            (_completed("", returncode=1, stderr="read failed"), "blocked"),
            (None, "blocked"),
        ],
    )
    def test_adapter_makes_no_write_when_pr_state_does_not_match_or_cannot_be_read(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        pr_response: CompletedProcess[str] | None,
        expected_outcome: str,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        if pr_response is None:
            monkeypatch.delenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT")
            monkeypatch.setenv("GH_TOKEN", "unrelated-ambient-token")
        gh = FakeGh([pr_response] if pr_response is not None else [])
        result = _dispatch(tmp_path, handoff, payload, gh)

        assert result.outcome == expected_outcome
        assert all("POST" not in args for args, _ in gh.calls)
        assert not (tmp_path / "dispatch-attempts").exists()

    @pytest.mark.parametrize(
        "pr_response",
        [
            _completed("not-json"),
            _completed("[]"),
            _completed('{"base_ref":"main","head_ref":"feature"}'),
            _completed('{"base_ref":"","head_ref":"feature","head_sha":"' + _HEAD_SHA + '"}'),
            _completed('{"base_ref":"main","head_ref":"","head_sha":"' + _HEAD_SHA + '"}'),
            _completed('{"base_ref":"main","head_ref":"feature","head_sha":""}'),
        ],
    )
    def test_blocks_when_pr_response_is_malformed(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        pr_response: CompletedProcess[str],
    ) -> None:
        gh = FakeGh([pr_response])
        result = _dispatch(tmp_path, handoff, payload, gh)

        assert result.outcome == "blocked"
        assert len(gh.calls) == 1

    def test_blocks_when_assigned_thread_id_is_missing(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
    ) -> None:
        invalid_finding = handoff.finding.model_copy(update={"thread_id": None})
        invalid_handoff = handoff.model_copy(update={"finding": invalid_finding})
        gh = FakeGh([_pr_response()])
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=gh)
        assert host.reserve_branch_write(invalid_handoff, 1) is True

        acceptance = host.create_task_if_head(invalid_handoff, payload, 1)

        assert acceptance.outcome == "blocked"
        assert len(gh.calls) == 1
        assert not host._reservation_contexts

    def test_adapter_makes_no_write_when_assigned_thread_is_resolved(
        self, tmp_path: Path, handoff: SingleFindingHandoff, payload: AgentTasksPayload
    ) -> None:
        gh = FakeGh([_pr_response(), _completed("true")])
        result = _dispatch(tmp_path, handoff, payload, gh)

        assert result.outcome == "already_resolved"
        assert len(gh.calls) == 2
        assert all("POST" not in args for args, _ in gh.calls)

    @pytest.mark.parametrize("changed_state", ["marker", "head", "thread"])
    def test_adapter_makes_no_write_for_existing_dispatch_marker(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        changed_state: str,
    ) -> None:
        gh, expected = _gh_for_dispatch_state_change(_dispatch_marker(handoff), changed_state)
        result = _dispatch(tmp_path, handoff, payload, gh)

        assert (result.outcome, len(gh.calls)) == expected
        assert all("POST" not in args for args, _ in gh.calls)
        assert "--jq" not in gh.calls[2][0]

    @pytest.mark.parametrize(
        "responses",
        [
            [_pr_response(), _completed("", returncode=1, stderr="thread read failed")],
            [_pr_response(), _completed("not-a-boolean")],
            [_pr_response(), _completed("false"), _completed("", returncode=1, stderr="comments read failed")],
            [_pr_response(), _completed("false"), _completed("{invalid-json}")],
            [_pr_response(), _completed("false"), _completed("{}")],
            [_pr_response(), _completed("false"), _completed(json.dumps([42]))],
            [_pr_response(), _completed("false"), _completed(json.dumps([[42]]))],
            [_pr_response(), _completed("false"), _completed(json.dumps([[{"body": None}]]))],
        ],
    )
    def test_blocks_without_post_when_thread_or_dedup_state_cannot_be_read(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        responses: list[object],
    ) -> None:
        gh = FakeGh(responses)
        result = _dispatch(tmp_path, handoff, payload, gh)

        assert result.outcome == "blocked"
        assert all("POST" not in args for args, _ in gh.calls)

    def test_blocks_when_thread_lookup_exits_unsuccessfully(
        self, tmp_path: Path, handoff: SingleFindingHandoff, payload: AgentTasksPayload
    ) -> None:
        gh = FakeGh([_pr_response(), _completed("", returncode=1)])
        result = _dispatch(tmp_path, handoff, payload, gh)

        assert result.outcome == "blocked"
        assert len(gh.calls) == 2

    def test_blocks_when_per_operation_deadline_is_exhausted(
        self,
        tmp_path: Path,
    ) -> None:
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
        with pytest.raises(TimeoutExpired):
            host._run_gh(["api", "endpoint"], time.monotonic() - 1)

    def test_releases_reservation_when_an_unexpected_state_error_escapes(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
    ) -> None:
        host = GitHubSingleFindingDispatchHost(
            tmp_path,
            run_safe=FakeGh([RuntimeError("unexpected transport error")]),
        )
        assert host.reserve_branch_write(handoff, 1) is True

        with pytest.raises(RuntimeError, match="unexpected transport error"):
            host.create_task_if_head(handoff, payload, 1)

        assert not host._reservation_contexts

    def test_ambiguous_post_failure_is_persisted_without_inventing_task_ids(
        self, tmp_path: Path, handoff: SingleFindingHandoff, payload: AgentTasksPayload
    ) -> None:
        result = _dispatch_with_uncertain_retry(
            tmp_path,
            handoff,
            payload,
            _gh_for_current_handoff(handoff, post_response=TimeoutExpired(["gh"], 1)),
        )

        assert result.outcome == "acceptance_unknown"
        record = json.loads(next((tmp_path / "dispatch-attempts").glob("*.json")).read_text(encoding="utf-8"))
        assert record["comment_id"] is None
        assert record["task_id"] is None
        assert record["session_id"] is None

    def test_uncertain_replay_preserves_evidence_and_review_regressions(
        self, tmp_path: Path, handoff: SingleFindingHandoff, payload: AgentTasksPayload
    ) -> None:
        _dispatch(tmp_path, handoff, payload, _gh_for_current_handoff(handoff, post_response=_completed("987654")))
        retry_gh = FakeGh([_pr_response(), _completed("false"), _completed("[[]]")])
        retry_result = _dispatch(tmp_path, handoff, payload, retry_gh)

        assert retry_result.outcome == "acceptance_unknown"
        assert all("POST" not in args for args, _ in retry_gh.calls)
        record = json.loads(next((tmp_path / "dispatch-attempts").glob("*.json")).read_text(encoding="utf-8"))
        assert record["comment_id"] == 987654

        _assert_accepted_replay_preserves_identity(tmp_path, handoff, payload)

    def test_post_sends_long_prompt_through_stdin(
        self, tmp_path: Path, handoff: SingleFindingHandoff, payload: AgentTasksPayload
    ) -> None:
        long_payload = AgentTasksPayload(**{**payload.to_dict(), "prompt": "x" * 40_000})
        long_handoff = handoff.model_copy(
            update={"payload_digest": finding_payload_digest(handoff.finding_id, long_payload)}
        )
        gh = _gh_for_current_handoff(long_handoff, post_response=_completed("987654"))

        result = _dispatch(tmp_path, long_handoff, long_payload, gh)

        assert result.outcome == "acceptance_unknown"
        args, kwargs = next((args, kwargs) for args, kwargs in gh.calls if "POST" in args)
        assert "--field" not in args
        assert args[args.index("--input") + 1] == "-"
        assert kwargs["input"] == json.dumps({"body": f"@copilot\n\n{'x' * 40_000}\n\n{_dispatch_marker(handoff)}"})

    @pytest.mark.parametrize("post_response", [OSError("process could not start"), _DispatchDeadlineExpired(["gh"], 0)])
    def test_post_process_start_failure_is_blocked_not_ambiguous(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        post_response: BaseException,
    ) -> None:
        gh = _gh_for_current_handoff(handoff, post_response=post_response)
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=gh)

        result = SingleFindingDispatchAdapter(host, clock=lambda: 100).dispatch(handoff, payload)

        assert result.outcome == "blocked"
        assert not host._reservation_contexts
        record = json.loads(next((tmp_path / "dispatch-attempts").glob("*.json")).read_text(encoding="utf-8"))
        assert record["outcome"] == "blocked"

    def test_failure_to_reconcile_unsent_attempt_is_nonfatal(
        self, tmp_path: Path, handoff: SingleFindingHandoff, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _assert_reconciliation_failure_does_not_escape(tmp_path, handoff, monkeypatch)

    @pytest.mark.parametrize(
        "post_response",
        [
            _completed("", returncode=1, stderr="request failed"),
            _completed("not-a-comment-id"),
        ],
    )
    def test_ambiguous_post_responses_are_persisted_without_comment_id(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        post_response: CompletedProcess[str],
    ) -> None:
        gh = _gh_for_current_handoff(handoff, post_response=post_response)
        result = _dispatch(tmp_path, handoff, payload, gh)

        assert result.outcome == "acceptance_unknown"
        record = json.loads(next((tmp_path / "dispatch-attempts").glob("*.json")).read_text(encoding="utf-8"))
        assert record["comment_id"] is None

    def test_persists_known_task_and_session_ids(self, tmp_path: Path, handoff: SingleFindingHandoff) -> None:
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
        identity = AcceptedTaskIdentity("task-2", "session-2")
        acceptance = TaskAcceptance("accepted", identity, "task accepted")
        second_run = handoff.model_copy(update={"run_id": "00000000-0000-4000-8000-000000000002"})

        assert host.persist_acceptance(handoff, acceptance, 1) is True
        assert host.persist_acceptance(second_run, acceptance, 1) is True
        records = list((tmp_path / "dispatch-attempts").glob("*.json"))
        assert len(records) == 2
        assert host._attempt_key(handoff) != host._attempt_key(second_run)
        record = json.loads(records[0].read_text(encoding="utf-8"))
        assert record["task_id"] == "task-2"
        assert record["session_id"] == "session-2"

    def test_persist_replacement_failure_preserves_existing_record_and_cleans_temp_file(
        self, tmp_path: Path, handoff: SingleFindingHandoff, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from agentic_devtools.cli.github import single_finding_dispatch_host as module
        from agentic_devtools.cli.github.single_finding_dispatch import AcceptancePersistenceError

        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
        acceptance = TaskAcceptance("blocked", None, "not dispatched")
        assert host.persist_acceptance(handoff, acceptance, 1) is True
        record_path = next((tmp_path / "dispatch-attempts").glob("*.json"))
        previous_record = record_path.read_text(encoding="utf-8")

        def fail_replace(source: str | os.PathLike[str], destination: str | os.PathLike[str]) -> None:
            raise OSError("replace failed")

        monkeypatch.setattr(module.os, "replace", fail_replace)
        with pytest.raises(AcceptancePersistenceError, match="replace failed"):
            host.persist_acceptance(handoff, TaskAcceptance("unknown", None, "delivery uncertain"), 1)

        assert record_path.read_text(encoding="utf-8") == previous_record
        assert list(record_path.parent.glob("*.tmp")) == []
        assert not host._reservation_contexts

    def test_persist_is_atomic_and_durably_syncs_parent_directory(
        self, tmp_path: Path, handoff: SingleFindingHandoff, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=FakeGh([]))
        _assert_durable_persistence(host, handoff, monkeypatch)

    @pytest.mark.parametrize("fail_on_write", [1, 2])
    def test_adapter_reports_persistence_failure_and_releases_lock(
        self,
        tmp_path: Path,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        monkeypatch: pytest.MonkeyPatch,
        fail_on_write: int,
    ) -> None:
        from agentic_devtools.cli.github import single_finding_dispatch_attempt_store as module

        gh = _gh_for_current_handoff(handoff, post_response=TimeoutExpired(["gh"], 1))
        original_locked_file = module.locked_file
        persistence_writes = 0

        def fail_to_persist(path: Path, **kwargs: Any):
            nonlocal persistence_writes
            if path.parent.name == "dispatch-attempts":
                persistence_writes += 1
                if persistence_writes == fail_on_write:
                    raise OSError("disk unavailable")
            return original_locked_file(path, **kwargs)

        monkeypatch.setattr(module, "locked_file", fail_to_persist)
        host = GitHubSingleFindingDispatchHost(tmp_path, run_safe=gh)
        result = SingleFindingDispatchAdapter(host, clock=lambda: 100).dispatch(handoff, payload)

        if fail_on_write == 1:
            assert result.outcome == "blocked"
            assert all("POST" not in args for args, _ in gh.calls)
            assert not (tmp_path / "dispatch-attempts").exists()
            assert not host._reservation_contexts
            return

        assert result.outcome == "acceptance_unknown"
        assert "disk unavailable" in result.reason
        assert not host._reservation_contexts
        record = json.loads(next((tmp_path / "dispatch-attempts").glob("*.json")).read_text(encoding="utf-8"))
        assert record["outcome"] == "in_flight"
        retry_gh = FakeGh(
            [_pr_response(), _completed("false"), _completed("[[]]"), _pr_response(), _completed("false")]
        )
        retry_result = _dispatch(tmp_path, handoff, payload, retry_gh)
        assert retry_result.outcome == "acceptance_unknown"
        assert all("POST" not in args for args, _ in retry_gh.calls)
