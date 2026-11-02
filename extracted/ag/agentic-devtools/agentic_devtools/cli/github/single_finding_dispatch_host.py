"""Production GitHub host for bounded single-finding dispatches."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from collections.abc import Callable, Sequence
from contextlib import ExitStack
from dataclasses import asdict
from pathlib import Path
from subprocess import CompletedProcess, TimeoutExpired
from typing import Any, Literal

from agentic_devtools.ai_providers.agent_tasks_payload import AgentTasksPayload
from agentic_devtools.cli.ci.credential_roles import GH_TOKEN, require_default_repo_workflow_token
from agentic_devtools.cli.github.review_orchestration import parse_pr_url
from agentic_devtools.cli.github.single_finding_dispatch import (
    BRANCH_WRITE_RESOURCE,
    AcceptancePersistenceError,
    SingleFindingDispatchAdapter,
    SingleFindingDispatchHost,
    SingleFindingHandoff,
    TaskAcceptance,
)
from agentic_devtools.cli.github.single_finding_dispatch_state import DispatchAttemptState
from agentic_devtools.cli.subprocess_utils import run_safe
from agentic_devtools.file_locking import FileLockError, locked_file
from agentic_devtools.state import get_state_dir

__all__ = ["GitHubSingleFindingDispatchHost", "main"]

_RESERVATION_LOCK_ROOT = Path.home() / ".agdt" / "locks" / "single-finding-dispatch"


def _dispatch_marker(handoff: SingleFindingHandoff) -> str:
    """Return the stable hidden marker identifying one repository/PR/head/finding."""
    return DispatchAttemptState.dispatch_marker(handoff)


class _StateReadError(RuntimeError):
    """A required authoritative GitHub state could not be read."""


class _DispatchDeadlineExpired(TimeoutExpired):
    """The dispatch deadline expired before starting the GitHub CLI process."""


class GitHubSingleFindingDispatchHost(SingleFindingDispatchHost):
    """Implement serialized compare-and-post dispatches through GitHub's PR comment route.

    The PR comment provides the production ``@copilot`` route without relying on
    the Agent Tasks API. Since that route does not synchronously expose a task or
    session ID, a posted comment is returned as an unknown acceptance and its
    comment ID is durably recorded before the adapter returns.
    """

    def __init__(
        self,
        state_dir: Path,
        *,
        run_safe: Callable[..., CompletedProcess[str]] = run_safe,
    ) -> None:
        if not isinstance(state_dir, Path):
            raise TypeError("state_dir must be a pathlib.Path")
        self._state_dir = state_dir
        self._run_safe = run_safe
        self._attempt_state = DispatchAttemptState(state_dir, _RESERVATION_LOCK_ROOT)
        self._reservation_contexts: dict[str, ExitStack] = {}
        self._comment_ids = self._attempt_state.comment_ids

    def reserve_branch_write(self, handoff: SingleFindingHandoff, timeout_seconds: int) -> bool:
        """Acquire the cross-process reservation for this PR's branch-write effect."""
        _validate_timeout(timeout_seconds)
        lock_path, key = self._lock_path(handoff)
        if key in self._reservation_contexts:
            return False
        stack = ExitStack()
        try:
            context = locked_file(lock_path, mode="a+", timeout=timeout_seconds)
            stack.enter_context(context)
            self._reservation_contexts[key] = stack
        except FileLockError:
            stack.close()
            return False
        except Exception:
            stack.close()
            raise
        return True

    def release_branch_write(self, handoff: SingleFindingHandoff) -> None:
        """Release the branch-write reservation previously acquired for this handoff."""
        self._release_reservation(handoff)

    def create_task_if_head(
        self,
        handoff: SingleFindingHandoff,
        payload: AgentTasksPayload,
        timeout_seconds: int,
    ) -> TaskAcceptance:
        """Re-read the PR, assigned thread and dispatch markers before one PR comment."""
        _validate_timeout(timeout_seconds)
        reservation_key = self._reservation_key(handoff)
        if reservation_key not in self._reservation_contexts:
            return TaskAcceptance("blocked", None, "branch-write reservation is not held")
        deadline = time.monotonic() + timeout_seconds
        try:
            repository, pr_number, _ = parse_pr_url(handoff.pr_url)
            rejection = self._check_pr_state(handoff, repository, pr_number, deadline)
            if rejection is not None:
                return rejection
            rejection = self._check_thread_state(handoff, deadline)
            if rejection is not None:
                return rejection
            marker = self._check_dispatch_marker(handoff, repository, pr_number, deadline)
            if isinstance(marker, TaskAcceptance):
                return marker
            prior_attempt = self._check_existing_dispatch(handoff)
            if prior_attempt is not None:
                return prior_attempt

            body = f"@copilot\n\n{payload.prompt}\n\n{marker}"
            self._comment_ids[self._attempt_key(handoff)] = None
            rejection = self._record_in_flight(handoff, deadline)
            if rejection is not None:
                return rejection
            rejection = self._check_pr_state(handoff, repository, pr_number, deadline, release_reservation=False)
            if rejection is None:
                rejection = self._check_thread_state(handoff, deadline, release_reservation=False)
            if rejection is not None:
                try:
                    self._mark_attempt_not_delivered(handoff, rejection)
                finally:
                    self._release_reservation(handoff)
                return rejection
            return self._post_comment(handoff, repository, pr_number, body, deadline)
        except Exception:
            self._release_reservation(handoff)
            raise

    def _post_comment(
        self,
        handoff: SingleFindingHandoff,
        repository: str,
        pr_number: int,
        body: str,
        deadline: float,
    ) -> TaskAcceptance:
        attempt_key = self._attempt_key(handoff)
        try:
            result = self._run_gh(
                [
                    "api",
                    f"repos/{repository}/issues/{pr_number}/comments",
                    "--method",
                    "POST",
                    "--input",
                    "-",
                    "--jq",
                    ".id",
                ],
                deadline,
                input_data=json.dumps({"body": body}),
            )
        except _DispatchDeadlineExpired, OSError:
            self._mark_attempt_not_delivered(
                handoff, TaskAcceptance("blocked", None, "GitHub CLI request was not sent")
            )
            return self._no_write(handoff, "blocked", "GitHub CLI request was not sent")
        except TimeoutExpired:
            return TaskAcceptance("unknown", None, "PR comment delivery may have succeeded")
        # A non-zero CLI exit does not prove that GitHub rejected the POST.
        comment_id = self._parse_comment_id(result.stdout) if result.returncode == 0 else None
        self._comment_ids[attempt_key] = comment_id
        if comment_id is None:
            return TaskAcceptance("unknown", None, "PR comment delivery result is ambiguous")
        try:
            self._update_unresolved_guard_comment_id(handoff, comment_id, deadline)
        except AcceptancePersistenceError as error:
            return TaskAcceptance(
                "unknown", None, f"PR comment posted, but its ID could not be recorded: {error.reason}"
            )
        return TaskAcceptance("unknown", None, "PR comment posted; task identity is not yet observable")

    def _record_in_flight(self, handoff: SingleFindingHandoff, deadline: float) -> TaskAcceptance | None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return self._no_write(handoff, "blocked", "deadline expired before recording the in-flight attempt")
        try:
            self._attempt_state.record_in_flight(handoff, max(1, int(remaining)))
        except AcceptancePersistenceError as error:
            return self._no_write(handoff, "blocked", error.reason)
        return None

    def _check_pr_state(
        self,
        handoff: SingleFindingHandoff,
        repository: str,
        pr_number: int,
        deadline: float,
        *,
        release_reservation: bool = True,
    ) -> TaskAcceptance | None:
        try:
            pr_state = self._read_pr(repository, pr_number, deadline)
        except OSError, TimeoutExpired, _StateReadError, TypeError, ValueError:
            return self._no_write(
                handoff,
                "blocked",
                "authoritative pull request state could not be read",
                release_reservation=release_reservation,
            )
        if (
            pr_state["base_ref"] != handoff.base_ref
            or pr_state["head_ref"] != handoff.head_ref
            or pr_state["head_sha"] != handoff.expected_head
        ):
            return self._no_write(
                handoff,
                "head_changed",
                "current pull request refs or head SHA differ",
                release_reservation=release_reservation,
            )
        return None

    def _check_thread_state(
        self,
        handoff: SingleFindingHandoff,
        deadline: float,
        *,
        release_reservation: bool = True,
    ) -> TaskAcceptance | None:
        thread_id = handoff.finding.thread_id
        if thread_id is None:
            return self._no_write(
                handoff,
                "blocked",
                "assigned review thread ID is missing",
                release_reservation=release_reservation,
            )
        try:
            is_resolved = self._read_thread_resolution(thread_id, deadline)
        except OSError, TimeoutExpired, _StateReadError, ValueError:
            return self._no_write(
                handoff,
                "blocked",
                "assigned review thread state could not be read",
                release_reservation=release_reservation,
            )
        if is_resolved:
            return self._no_write(
                handoff,
                "already_resolved",
                "assigned review thread is already resolved",
                release_reservation=release_reservation,
            )
        return None

    def _check_dispatch_marker(
        self,
        handoff: SingleFindingHandoff,
        repository: str,
        pr_number: int,
        deadline: float,
    ) -> str | TaskAcceptance:
        marker = _dispatch_marker(handoff)
        try:
            comments = self._attempt_state.read_pr_comments(self._run_gh, repository, pr_number, deadline)
        except OSError, TimeoutExpired, _StateReadError, TypeError, ValueError:
            return self._no_write(handoff, "blocked", "existing pull request comments could not be read")
        matches = [(body, author) for body, author in comments if marker in body]
        if matches:
            try:
                dispatch_login = self._attempt_state.read_dispatch_identity(self._run_gh, deadline)
            except OSError, TimeoutExpired, _StateReadError, TypeError, ValueError:
                return self._no_write(handoff, "blocked", "dispatch identity could not be verified")
            if any(author.casefold() == dispatch_login.casefold() for _, author in matches):
                self._clear_unresolved_guard(handoff)
                return self._no_write(handoff, "already_active", "matching dispatch marker already exists")
        return marker

    def _check_unresolved_guard(self, handoff: SingleFindingHandoff) -> TaskAcceptance | None:
        acceptance = self._attempt_state.check_unresolved_guard(handoff)
        if acceptance is not None and acceptance.outcome == "blocked":
            self._release_reservation(handoff)
        return acceptance

    def _update_unresolved_guard_comment_id(
        self, handoff: SingleFindingHandoff, comment_id: int, deadline: float
    ) -> None:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise AcceptancePersistenceError("deadline expired before recording the observed comment ID")
        self._attempt_state.update_unresolved_comment_id(handoff, comment_id, max(1, int(remaining)))

    def _clear_unresolved_guard(self, handoff: SingleFindingHandoff) -> None:
        self._attempt_state.clear_unresolved_guard(handoff)

    def _check_prior_uncertain_attempt(self, handoff: SingleFindingHandoff) -> TaskAcceptance | None:
        acceptance = self._attempt_state.check_prior_attempt(handoff)
        if acceptance is not None and acceptance.outcome != "unknown":
            self._release_reservation(handoff)
        return acceptance

    def _check_existing_dispatch(self, handoff: SingleFindingHandoff) -> TaskAcceptance | None:
        prior = self._check_prior_uncertain_attempt(handoff)
        return prior if prior is not None else self._check_unresolved_guard(handoff)

    def persist_acceptance(
        self,
        handoff: SingleFindingHandoff,
        acceptance: TaskAcceptance,
        timeout_seconds: int,
        *,
        _record_outcome: str | None = None,
        _release_reservation: bool = True,
    ) -> bool:
        """Atomically persist the attempt and observed PR comment/task/session identities."""
        try:
            _validate_timeout(timeout_seconds)
            return self._attempt_state.persist_acceptance(
                handoff,
                acceptance,
                timeout_seconds,
                record_outcome=_record_outcome,
            )
        finally:
            # Surface unlock failures; Python chains them to any active persistence error.
            if _release_reservation:
                self._release_reservation(handoff)

    def _mark_attempt_not_delivered(self, handoff: SingleFindingHandoff, acceptance: TaskAcceptance) -> None:
        try:
            self._attempt_state.persist_acceptance(
                handoff,
                acceptance,
                1,
                record_outcome=acceptance.outcome,
            )
        except AcceptancePersistenceError:
            # Recording an unsent attempt is best-effort; release/finalization must proceed.
            pass
        finally:
            self._clear_unresolved_guard(handoff)

    def _read_pr(self, repository: str, pr_number: int, deadline: float) -> dict[str, str]:
        result = self._run_gh(
            [
                "api",
                f"repos/{repository}/pulls/{pr_number}",
                "--jq",
                "{base_ref:.base.ref,head_ref:.head.ref,head_sha:.head.sha}",
            ],
            deadline,
        )
        if result.returncode != 0:
            raise _StateReadError("pull request lookup failed")
        data = json.loads(result.stdout)
        if not isinstance(data, dict):
            raise _StateReadError("pull request response is not an object")
        base_ref, head_ref, head_sha = data.get("base_ref"), data.get("head_ref"), data.get("head_sha")
        if (
            not isinstance(base_ref, str)
            or not base_ref
            or not isinstance(head_ref, str)
            or not head_ref
            or not isinstance(head_sha, str)
            or not head_sha
        ):
            raise _StateReadError("pull request response omitted refs or head SHA")
        return {"base_ref": base_ref, "head_ref": head_ref, "head_sha": head_sha}

    def _read_thread_resolution(self, thread_id: str, deadline: float) -> bool:
        result = self._run_gh(
            [
                "api",
                "graphql",
                "-f",
                f"id={thread_id}",
                "-f",
                "query=query($id: ID!) { node(id: $id) { ... on PullRequestReviewThread { isResolved } } }",
                "--jq",
                ".data.node.isResolved",
            ],
            deadline,
        )
        if result.returncode != 0 or result.stdout.strip() not in {"true", "false"}:
            raise _StateReadError("review thread lookup failed")
        return result.stdout.strip() == "true"

    def _run_gh(
        self,
        args: list[str],
        deadline: float,
        *,
        input_data: str | None = None,
    ) -> CompletedProcess[str]:
        timeout = deadline - time.monotonic()
        if timeout <= 0:
            raise _DispatchDeadlineExpired(["gh", *args], 0)
        try:
            token = require_default_repo_workflow_token("dispatch a single finding")
        except RuntimeError as error:
            raise OSError("workflow credential is unavailable") from error
        options: dict[str, Any] = {
            "capture_output": True,
            "text": True,
            "shell": False,
            "timeout": timeout,
            "env": {**os.environ, GH_TOKEN: token},
        }
        if input_data is not None:
            options["input"] = input_data
        return self._run_safe(
            ["gh", "--hostname", "github.com", *args],
            **options,
        )

    def _no_write(
        self,
        handoff: SingleFindingHandoff,
        outcome: Literal["already_active", "already_resolved", "head_changed", "blocked"],
        reason: str,
        *,
        release_reservation: bool = True,
    ) -> TaskAcceptance:
        if release_reservation:
            self._release_reservation(handoff)
        return TaskAcceptance(outcome, None, reason)

    def _release_reservation(self, handoff: SingleFindingHandoff) -> None:
        self._comment_ids.pop(self._attempt_key(handoff), None)
        stack = self._reservation_contexts.pop(self._reservation_key(handoff), None)
        if stack is not None:
            stack.close()

    def _reservation_key(self, handoff: SingleFindingHandoff) -> str:
        repository, pr_number, _ = parse_pr_url(handoff.pr_url)
        return f"{repository}:{pr_number}:{BRANCH_WRITE_RESOURCE}"

    def _lock_path(self, handoff: SingleFindingHandoff) -> tuple[Path, str]:
        key = self._reservation_key(handoff)
        digest = hashlib.sha256(key.encode()).hexdigest()
        return _RESERVATION_LOCK_ROOT / f"{digest}.lock", key

    @staticmethod
    def _attempt_key(handoff: SingleFindingHandoff) -> str:
        return DispatchAttemptState.attempt_key(handoff)

    @staticmethod
    def _parse_comment_id(stdout: str) -> int | None:
        value = stdout.strip()
        if not re.fullmatch(r"[1-9][0-9]*", value):
            return None
        return int(value)


def _validate_timeout(timeout_seconds: int) -> None:
    if type(timeout_seconds) is not int or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be a positive integer")


def main(argv: Sequence[str] | None = None) -> None:
    """Dispatch one validated handoff loaded from a JSON file."""
    parser = argparse.ArgumentParser(description="Dispatch one bounded AI PR Loop finding")
    parser.add_argument("handoff_file", help="JSON file containing handoff and payload objects")
    args = parser.parse_args(argv)
    try:
        envelope = json.loads(Path(args.handoff_file).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        parser.error(f"could not read handoff JSON: {error}")
    if not isinstance(envelope, dict) or set(envelope) != {"handoff", "payload"}:
        parser.error("handoff JSON must contain exactly 'handoff' and 'payload' objects")
    if not isinstance(envelope["handoff"], dict) or not isinstance(envelope["payload"], dict):
        parser.error("'handoff' and 'payload' must both be JSON objects")
    try:
        handoff = SingleFindingHandoff.model_validate(envelope["handoff"])
        payload = AgentTasksPayload(**envelope["payload"])
    except (TypeError, ValueError) as error:
        parser.error(f"handoff or payload validation failed: {error}")
    host = GitHubSingleFindingDispatchHost(get_state_dir())
    try:
        result = SingleFindingDispatchAdapter(host, clock=lambda: int(time.time())).dispatch(handoff, payload)
    except ValueError as error:
        parser.error(f"dispatch validation failed: {error}")
    print(json.dumps(asdict(result), sort_keys=True))


if __name__ == "__main__":
    main()
