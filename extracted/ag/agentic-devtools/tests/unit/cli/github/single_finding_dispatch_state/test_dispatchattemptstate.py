"""Tests for ``DispatchAttemptState``."""

import json
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any

import pytest

from agentic_devtools.cli.github.single_finding_dispatch import (
    AcceptancePersistenceError,
    AcceptedTaskIdentity,
    TaskAcceptance,
)
from agentic_devtools.cli.github.single_finding_dispatch_state import DispatchAttemptState
from tests.unit.cli.github.single_finding_dispatch_host.conftest import _PR_NUMBER, _REPO


class TestDispatchAttemptState:
    def test_persists_and_restores_unknown_acceptance_identity(self, tmp_path: Path, handoff: Any) -> None:
        state = DispatchAttemptState(tmp_path / "workflow", tmp_path / "shared")
        identity = AcceptedTaskIdentity("task-observed", "session-observed")
        acceptance = TaskAcceptance("unknown", identity, "delivery is uncertain")

        assert state.persist_acceptance(handoff, acceptance, 1)
        record_path = state._state_dir / "dispatch-attempts" / f"{state.attempt_key(handoff)}.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        restored = state.check_prior_attempt(handoff)

        assert record["marker"] == state.dispatch_marker(handoff)
        assert record["repository"] == _REPO
        assert record["pr_number"] == _PR_NUMBER
        assert restored == TaskAcceptance(
            "unknown", identity, "previous dispatch delivery may still be active; no retry was posted"
        )

    @pytest.mark.parametrize(
        "record",
        [
            [],
            {"outcome": "invalid"},
            {"outcome": "unknown", "comment_id": 0},
            {"outcome": "unknown", "task_id": "unsafe task id"},
            {"outcome": "unknown", "task_id": "task-1", "session_id": ""},
            {"outcome": "unknown", "session_id": "session-1"},
        ],
    )
    def test_blocks_malformed_prior_attempts(self, tmp_path: Path, handoff: Any, record: object) -> None:
        state = DispatchAttemptState(tmp_path, tmp_path / "shared")
        path = tmp_path / "dispatch-attempts" / f"{state.attempt_key(handoff)}.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(record), encoding="utf-8")

        result = state.check_prior_attempt(handoff)

        assert result is not None
        assert result.outcome == "blocked"

    def test_handles_missing_unreadable_accepted_and_terminal_prior_attempts(
        self, tmp_path: Path, handoff: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        state = DispatchAttemptState(tmp_path, tmp_path / "shared")
        path = tmp_path / "dispatch-attempts" / f"{state.attempt_key(handoff)}.json"
        assert state.check_prior_attempt(handoff) is None
        path.parent.mkdir(parents=True)
        path.write_text("{", encoding="utf-8")
        result = state.check_prior_attempt(handoff)
        assert result is not None
        assert result.outcome == "blocked"
        path.write_text(json.dumps({"outcome": "accepted"}), encoding="utf-8")
        result = state.check_prior_attempt(handoff)
        assert result is not None
        assert result.outcome == "already_active"
        path.write_text(json.dumps({"outcome": "blocked"}), encoding="utf-8")
        assert state.check_prior_attempt(handoff) is None

        for task_id, session_id in ((None, "session"), (42, None), ("task", 42)):
            path.write_text(
                json.dumps({"outcome": "unknown", "task_id": task_id, "session_id": session_id}),
                encoding="utf-8",
            )
            result = state.check_prior_attempt(handoff)
            assert result is not None
            assert result.outcome == "blocked"

        path.write_text(json.dumps({"outcome": "unknown"}), encoding="utf-8")
        result = state.check_prior_attempt(handoff)
        assert result is not None
        assert result.outcome == "unknown"
        assert result.identity is None

        original_read_text = Path.read_text

        def fail_read(self: Path, *args: Any, **kwargs: Any) -> str:
            if self == path:
                raise OSError("read failed")
            return original_read_text(self, *args, **kwargs)

        monkeypatch.setattr(Path, "read_text", fail_read)
        result = state.check_prior_attempt(handoff)
        assert result is not None
        assert result.outcome == "blocked"

    def test_guards_unresolved_deliveries_and_clears_them(self, tmp_path: Path, handoff: Any) -> None:
        state = DispatchAttemptState(tmp_path / "workflow", tmp_path / "shared")
        path = state.unresolved_guard_path(handoff)
        assert state.check_unresolved_guard(handoff) is None
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(state.unresolved_guard_record(handoff)), encoding="utf-8")
        result = state.check_unresolved_guard(handoff)
        assert result is not None
        assert result.outcome == "unknown"

        malformed = state.unresolved_guard_record(handoff, comment_id=0)
        path.write_text(json.dumps(malformed), encoding="utf-8")
        result = state.check_unresolved_guard(handoff)
        assert result is not None
        assert result.outcome == "blocked"
        path.write_text("{", encoding="utf-8")
        result = state.check_unresolved_guard(handoff)
        assert result is not None
        assert result.outcome == "blocked"
        state.clear_unresolved_guard(handoff)
        assert state.check_unresolved_guard(handoff) is None

    def test_unreadable_guard_blocks_dispatch(
        self, tmp_path: Path, handoff: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        state = DispatchAttemptState(tmp_path / "workflow", tmp_path / "shared")
        path = state.unresolved_guard_path(handoff)
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(state.unresolved_guard_record(handoff)), encoding="utf-8")
        original_read_text = Path.read_text

        def fail_read(self: Path, *args: Any, **kwargs: Any) -> str:
            if self == path:
                raise OSError("read failed")
            return original_read_text(self, *args, **kwargs)

        monkeypatch.setattr(Path, "read_text", fail_read)
        result = state.check_unresolved_guard(handoff)
        assert result is not None
        assert result.outcome == "blocked"

    def test_records_in_flight_and_updates_the_observed_comment_id(self, tmp_path: Path, handoff: Any) -> None:
        state = DispatchAttemptState(tmp_path / "workflow", tmp_path / "shared")
        state.record_in_flight(handoff, 1)
        guard_path = state.unresolved_guard_path(handoff)
        assert json.loads(guard_path.read_text(encoding="utf-8"))["comment_id"] is None

        state.update_unresolved_comment_id(handoff, 123, 1)

        assert json.loads(guard_path.read_text(encoding="utf-8"))["comment_id"] == 123

    def test_cleans_guard_when_in_flight_persistence_fails(
        self, tmp_path: Path, handoff: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        from agentic_devtools.cli.github import single_finding_dispatch_state as module

        state = DispatchAttemptState(tmp_path / "workflow", tmp_path / "shared")

        def fail_write(path: Path, record: dict[str, Any], timeout_seconds: int) -> None:
            if path.parent.name == "dispatch-attempts":
                raise AcceptancePersistenceError("attempt store unavailable")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(record), encoding="utf-8")

        monkeypatch.setattr(module, "write_attempt_record", fail_write)
        with pytest.raises(AcceptancePersistenceError, match="attempt store unavailable"):
            state.record_in_flight(handoff, 1)

        assert not state.unresolved_guard_path(handoff).exists()

    def test_reads_dispatch_identity_and_validated_comment_authors(self, handoff: Any) -> None:
        state = DispatchAttemptState(Path("."), Path("."))
        responses = iter(
            [
                CompletedProcess(["gh"], 0, "dispatch-user", ""),
                CompletedProcess(
                    ["gh"],
                    0,
                    json.dumps([[{"body": "body", "user": {"login": "dispatch-user"}}], []]),
                    "",
                ),
            ]
        )

        def run_gh(args: list[str], deadline: float) -> CompletedProcess[str]:
            return next(responses)

        assert state.read_dispatch_identity(run_gh, 5) == "dispatch-user"
        assert state.read_pr_comments(run_gh, _REPO, _PR_NUMBER, 5) == [("body", "dispatch-user")]

    @pytest.mark.parametrize(
        "response",
        [
            CompletedProcess(["gh"], 1, "", "failed"),
            CompletedProcess(["gh"], 0, "", ""),
            CompletedProcess(["gh"], 0, "{}", ""),
            CompletedProcess(["gh"], 0, "[42]", ""),
            CompletedProcess(["gh"], 0, "[[42]]", ""),
            CompletedProcess(["gh"], 0, '[[{"body":"body"}]]', ""),
        ],
    )
    def test_rejects_untrusted_or_malformed_github_reads(self, response: CompletedProcess[str]) -> None:
        state = DispatchAttemptState(Path("."), Path("."))

        def run_gh(args: list[str], deadline: float) -> CompletedProcess[str]:
            return response

        with pytest.raises((ValueError, json.JSONDecodeError)):
            state.read_pr_comments(run_gh, _REPO, _PR_NUMBER, 5)

    @pytest.mark.parametrize(
        "response",
        [CompletedProcess(["gh"], 1, "", "failed"), CompletedProcess(["gh"], 0, "", "")],
    )
    def test_rejects_failed_identity_lookup(self, response: CompletedProcess[str]) -> None:
        state = DispatchAttemptState(Path("."), Path("."))
        with pytest.raises(ValueError, match="dispatch identity"):
            state.read_dispatch_identity(lambda args, deadline: response, 5)
