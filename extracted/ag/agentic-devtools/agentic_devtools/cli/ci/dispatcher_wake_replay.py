"""Replay persisted dispatcher intent through the existing scheduled watchdog."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import UTC, datetime
from functools import cached_property
from typing import Any
from unittest.mock import patch

from agentic_devtools.cli.ci.cooldown import persist_cooldown
from agentic_devtools.cli.ci.credential_roles import (
    require_default_repo_workflow_token,
)
from agentic_devtools.cli.ci.dispatcher_throttle import DispatcherThrottle
from agentic_devtools.cli.ci.dispatcher_wake_store import DispatcherWakeStore
from agentic_devtools.cli.ci.dispatcher_wakeup import wake_resume_at
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider, _gh_api
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.watchdog_command import (
    _provider_cooldown,
    _reconcile_due_probes_and_check_availability,
    ai_pr_loop_watchdog_command,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

logger = logging.getLogger(__name__)
MAX_REPLAY_ENTRIES = 5


class DispatcherWakeReplay:
    """Retain pending intent until a guarded POST succeeds or its PR becomes obsolete.

    The existing watchdog concurrency group serializes replay invocations. Variable
    writes remain best-effort, not transactional: an unconfirmed acknowledgment
    leaves intent pending, and subsequent runs must recheck all live guards.
    """

    def __init__(self, provider: GitHubActionsProvider, store: DispatcherWakeStore | None = None) -> None:
        self.provider = provider
        self.store = store if store is not None else DispatcherWakeStore(provider)
        self.scheduler_wake_required = False
        self.scheduler_wake: tuple[str, dict[str, Any]] | None = None
        self.persistence_unconfirmed = False
        self.dispatch_failed = False
        self._post_attempted = False
        self.retained_wakes: dict[str, dict[str, Any]] = {}
        self.retained_wake_required = False

    def run(self, repository: str, default_branch: str) -> bool:
        """Return whether a POST was attempted, preventing a second dispatch in this invocation."""
        self._post_attempted = False
        self.__dict__.pop("_eligible_pr_numbers", None)
        self.scheduler_wake_required = False
        self.scheduler_wake = None
        self.persistence_unconfirmed = False
        self.dispatch_failed = False
        self.retained_wakes = {}
        self.retained_wake_required = False
        try:
            entries = self.store.entries()
        except Exception as exc:
            logger.warning(
                "Dispatcher wake store unavailable; retaining ordinary watchdog behavior: %s", type(exc).__name__
            )
            return False
        pending = {key: entry for key, entry in entries.items() if entry["status"] == "pending"}
        self.retained_wakes = pending
        self.retained_wake_required = bool(pending)
        if not pending:
            return False
        now = time.time()
        due = sorted(
            ((key, entry) for key, entry in pending.items() if entry["resume_at"] <= now),
            key=lambda pair: pair[1]["resume_at"],
        )
        if due:
            run_id = os.environ.get("GITHUB_RUN_ID", "")
            has_run_id = run_id.isascii() and run_id.isdigit() and len(run_id) <= 20
            offset = (int(run_id) if has_run_id else int(now)) % len(due)
            due = due[offset:] + due[:offset]
        for key, entry in due[:MAX_REPLAY_ENTRIES]:
            try:
                if self._replay(key, entry, repository, default_branch):
                    break
            except Exception as exc:
                self._handle_replay_error(key, entry, exc)
                break
            if self.scheduler_wake_required:
                break
        print("::notice::Dispatcher wake reconciliation complete; unacknowledged intent remains pending.")
        return self._post_attempted

    def _handle_replay_error(self, key: str, entry: dict[str, Any], error: Exception) -> None:
        if isinstance(error, (ProviderRateLimitError, RetryableError)) and error.is_rate_limit:
            self._postpone_rate_limit(key, entry, error)
            logger.warning("Dispatcher wake remains pending after provider rate limit")
            return
        if self._post_attempted:
            self._report_replay_failure(entry, error, operation="POST")
        else:
            self._report_replay_failure(entry, error, operation="pre-dispatch replay")

    def _report_replay_failure(self, entry: dict[str, Any], error: Exception, *, operation: str) -> None:
        message = str(error).casefold()
        if any(word in message for word in ("permission", "forbidden", "unauthorized", "denied")):
            diagnostic = "authorization denied"
        else:
            status = re.search(r"\bHTTP(?:/\d(?:\.\d)?)?\s+([45]\d{2})\b", str(error), re.IGNORECASE)
            if status is not None:
                diagnostic = f"HTTP {status.group(1)}"
            else:
                diagnostic = f"{type(error).__name__} provider failure"
        self.dispatch_failed = True
        print(
            f"::error::Dispatcher wake {operation} failed ({diagnostic}) for PR {entry['pr_number']} "
            f"head {entry['head_sha']} event {entry['event']}; pending intent retained."
        )

    def _postpone_rate_limit(
        self, key: str, entry: dict[str, Any], error: ProviderRateLimitError | RetryableError
    ) -> None:
        shared_persisted = False
        wake_persisted = False
        now = time.time()
        try:
            resume_at = wake_resume_at(self.provider, error, now=now)
            provider_error = self._provider_rate_limit_error(error, resume_at=resume_at)
        except Exception as exc:
            logger.warning("Could not derive shared dispatcher deadline: %s", type(exc).__name__)
            resume_at = None
            provider_error = None
        if provider_error is not None and resume_at is not None:
            try:
                receipt = persist_cooldown(self.provider, provider_error, now=now)
                shared_persisted = receipt is not None and receipt[1].resume_at >= resume_at
            except Exception as exc:
                logger.warning("Could not persist shared provider cooldown: %s", type(exc).__name__)
            if not shared_persisted:
                logger.warning(
                    "Shared provider cooldown persistence unconfirmed or shorter than wake deadline "
                    "for PR %s head %s event %s",
                    entry["pr_number"],
                    entry["head_sha"],
                    entry["event"],
                )
        if resume_at is not None:
            try:
                wake_persisted = self.store.postpone(key, entry, resume_at)
            except Exception as exc:
                logger.warning("Could not persist dispatcher wake deadline: %s", type(exc).__name__)
            if not wake_persisted:
                logger.warning(
                    "Dispatcher wake deadline persistence unconfirmed for PR %s head %s event %s",
                    entry["pr_number"],
                    entry["head_sha"],
                    entry["event"],
                )
        self.persistence_unconfirmed = not (shared_persisted or wake_persisted)
        if not self.persistence_unconfirmed and resume_at is not None:
            self.retained_wakes[key] = {**entry, "resume_at": resume_at}
        if self.persistence_unconfirmed:
            print(
                "::error::Rate-limited dispatcher wake has no confirmed shared or per-wake deadline; "
                "watchdog fallback is blocked."
            )

    @staticmethod
    def _provider_rate_limit_error(
        error: ProviderRateLimitError | RetryableError,
        *,
        resume_at: float,
    ) -> ProviderRateLimitError:
        return ProviderRateLimitError(
            reset_timestamp=resume_at,
            remaining=0,
            provider=error.provider,
            credential_identity=error.credential_identity,
            source=error.source,
        )

    def _defer_for_provider_cooldown(self, key: str, entry: dict[str, Any]) -> bool:
        paused = _provider_cooldown(self.provider, datetime.fromtimestamp(time.time(), UTC))
        if paused is None:
            return False
        self.retained_wakes[key] = {**entry, "resume_at": paused[1].resume_at}
        if not self.store.postpone(key, entry, paused[1].resume_at):
            logger.warning(
                "Provider cooldown deferral unconfirmed for PR %s head %s event %s",
                entry["pr_number"],
                entry["head_sha"],
                entry["event"],
            )
        return True

    def _replay(self, key: str, entry: dict[str, Any], repository: str, default_branch: str) -> bool:
        if self._defer_for_provider_cooldown(key, entry):
            return False
        token = require_default_repo_workflow_token("replay a pending dispatcher wake")
        pr = self._current_pr(key, entry, repository, token)
        if pr is None:
            return False
        throttle = DispatcherThrottle(max_attempts=1, retry_window_seconds=0)
        latest_run = throttle._lookup_last_run(repository, default_branch)
        if throttle._is_throttled(latest_run):
            return False
        _, available, reason = _reconcile_due_probes_and_check_availability(
            repository, latest_run, datetime.fromtimestamp(time.time(), UTC)
        )
        if not available:
            logger.warning(
                "Dispatcher wake blocked by watchdog availability gate for PR %s head %s event %s: %s",
                entry["pr_number"],
                entry["head_sha"],
                entry["event"],
                reason,
            )
            return False
        if not self._eligible(entry, pr, repository):
            return False
        if self.store.entries().get(key) != entry or self._current_pr(key, entry, repository, token) is None:
            return False
        if throttle._is_throttled(throttle._lookup_last_run(repository, default_branch)):
            return False
        if self._defer_for_provider_cooldown(key, entry):
            return False
        self._post_attempted = True
        _gh_api(
            f"/repos/{repository}/actions/workflows/ai-pr-loop-throttler.yml/dispatches",
            method="POST",
            body={"ref": default_branch},
            token=token,
        )
        if not self.store.acknowledge(key, entry):
            logger.warning(
                "Dispatcher wake POST accepted but acknowledgment unconfirmed; live guards must be rechecked"
            )
        return True

    def acknowledge_scheduler_handoff(self, outcome: dict[str, Any] | None) -> None:
        """Retire a closed-event wake only after confirmed repository scheduling or no work."""
        if self.scheduler_wake is None or not isinstance(outcome, dict):
            return
        if outcome.get("availability_established") is not True:
            return
        no_work = (
            outcome.get("decision") == "no_eligible_prs"
            and outcome.get("eligible_count") == 0
            and outcome.get("throttled") is False
        )
        if not no_work and outcome.get("dispatched") is not True:
            return
        key, entry = self.scheduler_wake
        if not self.store.acknowledge(key, entry):
            logger.warning(
                "Closed-event scheduler handoff acknowledgment unconfirmed for PR %s head %s event %s",
                entry["pr_number"],
                entry["head_sha"],
                entry["event"],
            )
            return
        print("::notice::Closed-event dispatcher wake acknowledged after scheduler handoff.")

    def _eligible(self, entry: dict[str, Any], pr: dict[str, Any], repository: str) -> bool:
        head = pr["head"]
        if not isinstance(head.get("ref"), str) or not head["ref"]:
            raise RuntimeError("Live PR branch is unavailable")
        active = is_copilot_session_active_via_agent_task(
            repository,
            entry["pr_number"],
            head_branch=head["ref"],
            pr_id=pr.get("id"),
            head_sha=entry["head_sha"],
            provider=self.provider,
        )
        if active is not False:
            return False
        return entry["pr_number"] in self._eligible_pr_numbers

    @cached_property
    def _eligible_pr_numbers(self) -> set[int]:
        with patch.dict(os.environ, {"AGDT_ALLOW_PRIVILEGED_PATHS": "1"}):
            eligible_prs = self.provider.list_eligible_prs()
        return {candidate.number for candidate in eligible_prs}

    def _current_pr(self, key: str, entry: dict[str, Any], repository: str, token: str) -> dict[str, Any] | None:
        pr = json.loads(_gh_api(f"/repos/{repository}/pulls/{entry['pr_number']}", token=token))
        if not isinstance(pr, dict) or pr.get("state") not in {"open", "closed"}:
            raise RuntimeError("Live PR state is unavailable")
        head = pr.get("head")
        if not isinstance(head, dict) or not isinstance(head.get("sha"), str):
            raise RuntimeError("Live PR head is unavailable")
        if pr["state"] == "closed" and entry["event"].split(":")[1:2] == ["closed"]:
            self.scheduler_wake_required = True
            self.scheduler_wake = (key, entry)
            print("::notice::Closed-event dispatcher wake requires repository scheduler discovery.")
            return None
        if pr["state"] == "closed" or head["sha"] != entry["head_sha"]:
            self.__dict__.pop("_eligible_pr_numbers", None)
            if not self.store.acknowledge(key, entry):
                logger.warning("Obsolete dispatcher wake retirement is unconfirmed")
            print("::notice::Retired stale or closed PR wake without dispatch.")
            return None
        return pr


def main() -> None:
    """Wrap only the existing scheduled watchdog modes; leave all other modes unchanged."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--mode", default="watchdog")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--default-branch", default=os.environ.get("GITHUB_DEFAULT_BRANCH", ""))
    args, unknown = parser.parse_known_args(sys.argv[1:])
    if unknown:
        ai_pr_loop_watchdog_command()
        return
    replay: DispatcherWakeReplay | None = None
    handled = False
    if args.mode in {"watchdog", "due-probe-only"} and args.repo and args.default_branch:
        try:
            provider = GitHubActionsProvider(repo=args.repo)
            replay = DispatcherWakeReplay(provider)
            handled = replay.run(args.repo, args.default_branch)
        except Exception as exc:
            logger.warning(
                "Dispatcher wake replay unavailable; retaining ordinary watchdog behavior: %s", type(exc).__name__
            )
    if replay is not None and replay.persistence_unconfirmed:
        raise SystemExit(1)
    if replay is not None and replay.dispatch_failed is True:
        raise SystemExit(1)
    if handled:
        return
    if replay is not None and (replay.scheduler_wake_required is True or replay.retained_wake_required is True):
        _run_closed_event_scheduler_handoff(replay, args)
        return
    ai_pr_loop_watchdog_command()


def _handoff_throttled(args: argparse.Namespace) -> bool:
    """Apply replay's active-run/cooldown guard without discarding provider errors."""
    throttle = DispatcherThrottle(max_attempts=1, retry_window_seconds=0)
    return bool(throttle._is_throttled(throttle._lookup_last_run(args.repo, args.default_branch)))


def _handle_retained_wake_error(
    replay: DispatcherWakeReplay, wakes: dict[str, dict[str, Any]], error: Exception
) -> None:
    if not wakes:
        raise error
    unconfirmed = False
    for key, entry in wakes.items():
        replay._handle_replay_error(key, entry, error)
        unconfirmed = unconfirmed or replay.persistence_unconfirmed
    if unconfirmed or replay.dispatch_failed:
        raise SystemExit(1) from error


def _run_closed_event_scheduler_handoff(replay: DispatcherWakeReplay, args: argparse.Namespace) -> None:
    wakes = dict(replay.retained_wakes)
    if replay.scheduler_wake is not None:
        key, entry = replay.scheduler_wake
        wakes[key] = entry
    if any(entry.get("resume_at", 0) > time.time() for entry in wakes.values()):
        print("::notice::Retained dispatcher wake deadline blocks watchdog fallback.")
        return
    try:
        throttled = _handoff_throttled(args)
    except Exception as exc:
        _handle_retained_wake_error(replay, wakes, exc)
        return
    if throttled:
        print("::notice::Closed-event dispatcher wake retained; throttler run active or cooling down.")
        return
    argv = sys.argv
    try:
        if args.mode == "due-probe-only":
            sys.argv = [
                argv[0],
                "--mode",
                "watchdog",
                "--repo",
                args.repo,
                "--default-branch",
                args.default_branch,
            ]
        outcome = ai_pr_loop_watchdog_command()
    finally:
        sys.argv = argv
    rate_limit_error = outcome.get("_rate_limit_error") if isinstance(outcome, dict) else None
    if isinstance(rate_limit_error, (ProviderRateLimitError, RetryableError)):
        unconfirmed = False
        for key, entry in wakes.items():
            replay._postpone_rate_limit(key, entry, rate_limit_error)
            unconfirmed = unconfirmed or replay.persistence_unconfirmed
        if unconfirmed:
            raise SystemExit(1)
        return
    replay.acknowledge_scheduler_handoff(outcome)
