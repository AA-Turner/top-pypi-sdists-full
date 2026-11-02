"""Durable workflow-scoped attempts and shared unresolved-delivery guards."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any

from agentic_devtools.cli.github.review_orchestration import parse_pr_url
from agentic_devtools.cli.github.single_finding_dispatch import (
    AcceptancePersistenceError,
    AcceptedTaskIdentity,
    SingleFindingHandoff,
    TaskAcceptance,
)
from agentic_devtools.cli.github.single_finding_dispatch_attempt_store import write_attempt_record


class DispatchAttemptState:
    """Persist dispatch evidence at workflow and shared-reservation scopes."""

    def __init__(self, state_dir: Path, shared_lock_root: Path) -> None:
        self._state_dir = state_dir
        self._shared_lock_root = shared_lock_root
        self.comment_ids: dict[str, int | None] = {}

    @staticmethod
    def attempt_key(handoff: SingleFindingHandoff) -> str:
        repository, pr_number, _ = parse_pr_url(handoff.pr_url)
        value = f"{repository}\n{pr_number}\n{handoff.run_id}\n{handoff.attempt_id}"
        return hashlib.sha256(value.encode()).hexdigest()

    def persist_acceptance(
        self,
        handoff: SingleFindingHandoff,
        acceptance: TaskAcceptance,
        timeout_seconds: int,
        *,
        record_outcome: str | None = None,
    ) -> bool:
        repository, pr_number, _ = parse_pr_url(handoff.pr_url)
        attempt_key = self.attempt_key(handoff)
        identity = acceptance.identity
        record = {
            "repository": repository,
            "pr_number": pr_number,
            "expected_head": handoff.expected_head,
            "finding_id": handoff.finding_id,
            "attempt_id": handoff.attempt_id,
            "marker": self.dispatch_marker(handoff),
            "outcome": record_outcome if record_outcome is not None else acceptance.outcome,
            "comment_id": self.comment_ids.get(attempt_key),
            "task_id": identity.task_id if identity is not None else None,
            "session_id": identity.session_id if identity is not None else None,
        }
        path = self._state_dir / "dispatch-attempts" / f"{attempt_key}.json"
        write_attempt_record(path, record, timeout_seconds)
        return True

    @staticmethod
    def dispatch_marker(handoff: SingleFindingHandoff) -> str:
        repository, pr_number, _ = parse_pr_url(handoff.pr_url)
        return (
            "<!-- agdt:ai-pr-loop-dispatch "
            f"repo={repository} pr={pr_number} head={handoff.expected_head} finding={handoff.finding_id} -->"
        )

    def check_prior_attempt(self, handoff: SingleFindingHandoff) -> TaskAcceptance | None:
        path = self._state_dir / "dispatch-attempts" / f"{self.attempt_key(handoff)}.json"
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return None
        except OSError, UnicodeDecodeError, json.JSONDecodeError:
            return TaskAcceptance("blocked", None, "previous dispatch attempt could not be read")
        if not isinstance(record, dict):
            return TaskAcceptance("blocked", None, "previous dispatch attempt is malformed")
        outcome = record.get("outcome")
        if not isinstance(outcome, str) or outcome not in {
            "accepted",
            "already_active",
            "already_resolved",
            "head_changed",
            "in_flight",
            "unknown",
            "blocked",
        }:
            return TaskAcceptance("blocked", None, "previous dispatch attempt outcome is malformed")
        if outcome == "accepted":
            return TaskAcceptance("already_active", None, "previous dispatch attempt was accepted")
        if outcome not in {"in_flight", "unknown"}:
            return None
        comment_id = record.get("comment_id")
        task_id, session_id = record.get("task_id"), record.get("session_id")
        if comment_id is not None and (type(comment_id) is not int or comment_id <= 0):
            return TaskAcceptance("blocked", None, "previous dispatch comment ID is malformed")
        try:
            identity = self._restore_identity(task_id, session_id)
        except ValueError:
            return TaskAcceptance("blocked", None, "previous dispatch task identity is malformed")
        self.comment_ids[self.attempt_key(handoff)] = comment_id
        return TaskAcceptance(
            "unknown", identity, "previous dispatch delivery may still be active; no retry was posted"
        )

    @staticmethod
    def _restore_identity(task_id: object, session_id: object) -> AcceptedTaskIdentity | None:
        if task_id is None:
            if session_id is not None:
                raise ValueError("session_id requires task_id")
            return None
        if not isinstance(task_id, str) or (session_id is not None and not isinstance(session_id, str)):
            raise ValueError("task and session IDs must be strings")
        return AcceptedTaskIdentity(task_id, session_id)

    def check_unresolved_guard(self, handoff: SingleFindingHandoff) -> TaskAcceptance | None:
        path = self.unresolved_guard_path(handoff)
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return None
        except OSError, UnicodeDecodeError, json.JSONDecodeError:
            return TaskAcceptance("blocked", None, "unresolved dispatch guard could not be read")
        repository, pr_number, _ = parse_pr_url(handoff.pr_url)
        comment_id = record.get("comment_id") if isinstance(record, dict) else None
        if (
            not isinstance(record, dict)
            or record.get("repository") != repository
            or record.get("pr_number") != pr_number
            or record.get("expected_head") != handoff.expected_head
            or record.get("finding_id") != handoff.finding_id
            or record.get("outcome") != "in_flight"
            or (comment_id is not None and (not isinstance(comment_id, int) or isinstance(comment_id, bool)))
            or (isinstance(comment_id, int) and comment_id <= 0)
        ):
            return TaskAcceptance("blocked", None, "unresolved dispatch guard is malformed")
        return TaskAcceptance("unknown", None, "previous dispatch delivery may still be active; no retry was posted")

    def read_dispatch_identity(self, run_gh: Callable[..., CompletedProcess[str]], deadline: float) -> str:
        result = run_gh(["api", "user", "--jq", ".login"], deadline)
        if result.returncode != 0 or not result.stdout.strip():
            raise ValueError("dispatch identity lookup failed")
        return result.stdout.strip()

    def read_pr_comments(
        self,
        run_gh: Callable[..., CompletedProcess[str]],
        repository: str,
        pr_number: int,
        deadline: float,
    ) -> list[tuple[str, str]]:
        result = run_gh(
            [
                "api",
                "--paginate",
                "--slurp",
                f"repos/{repository}/issues/{pr_number}/comments",
            ],
            deadline,
        )
        if result.returncode != 0:
            raise ValueError("pull request comment lookup failed")
        pages = json.loads(result.stdout)
        if not isinstance(pages, list):
            raise ValueError("pull request comment response is malformed")
        comments: list[tuple[str, str]] = []
        for page in pages:
            if not isinstance(page, list):
                raise ValueError("pull request comment response is malformed")
            for comment in page:
                user = comment.get("user") if isinstance(comment, dict) else None
                body = comment.get("body") if isinstance(comment, dict) else None
                author = user.get("login") if isinstance(user, dict) else None
                if not isinstance(body, str) or not isinstance(author, str) or not author:
                    raise ValueError("pull request comment response is malformed")
                comments.append((body, author))
        return comments

    def record_in_flight(self, handoff: SingleFindingHandoff, timeout_seconds: int) -> None:
        try:
            write_attempt_record(
                self.unresolved_guard_path(handoff),
                self.unresolved_guard_record(handoff),
                timeout_seconds,
            )
            self.persist_acceptance(
                handoff,
                TaskAcceptance("unknown", None, "dispatch attempt is in flight"),
                timeout_seconds,
                record_outcome="in_flight",
            )
        except AcceptancePersistenceError:
            self.clear_unresolved_guard(handoff)
            raise

    def unresolved_guard_record(
        self, handoff: SingleFindingHandoff, *, comment_id: int | None = None
    ) -> dict[str, Any]:
        repository, pr_number, _ = parse_pr_url(handoff.pr_url)
        return {
            "repository": repository,
            "pr_number": pr_number,
            "expected_head": handoff.expected_head,
            "finding_id": handoff.finding_id,
            "outcome": "in_flight",
            "comment_id": comment_id,
        }

    def unresolved_guard_path(self, handoff: SingleFindingHandoff) -> Path:
        repository, pr_number, _ = parse_pr_url(handoff.pr_url)
        key = f"{repository}\n{pr_number}\n{handoff.expected_head}\n{handoff.finding_id}"
        digest = hashlib.sha256(key.encode()).hexdigest()
        return self._shared_lock_root / "unresolved-deliveries" / f"{digest}.json"

    def update_unresolved_comment_id(
        self, handoff: SingleFindingHandoff, comment_id: int, timeout_seconds: int
    ) -> None:
        write_attempt_record(
            self.unresolved_guard_path(handoff),
            self.unresolved_guard_record(handoff, comment_id=comment_id),
            timeout_seconds,
        )

    def clear_unresolved_guard(self, handoff: SingleFindingHandoff) -> None:
        self.unresolved_guard_path(handoff).unlink(missing_ok=True)
