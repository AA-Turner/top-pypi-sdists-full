"""Preserve a PR-bound dispatcher wake before leaving a rate-limited job."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import UTC, datetime
from math import isfinite
from pathlib import Path

from agentic_devtools.cli.ci.cooldown import active_cooldown, persist_cooldown
from agentic_devtools.cli.ci.dispatcher_throttle import DispatcherThrottle
from agentic_devtools.cli.ci.dispatcher_wake_store import DispatcherWakeStore
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider, _get_read_token_pool, _gh_api
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.ci.watchdog_command import _provider_cooldown
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError, calculate_rate_limit_delay

_ACTIONS = frozenset(
    {"opened", "synchronize", "reopened", "labeled", "unlabeled", "ready_for_review", "review_requested", "closed"}
)


def wake_resume_at(
    provider: CIPlatformProvider,
    error: ProviderRateLimitError | RetryableError,
    now: float | None = None,
) -> float:
    """Return the longest provider/default-credential cooldown, not an in-job sleep budget."""
    if not error.is_rate_limit:
        raise ValueError("A confirmed rate limit is required")
    current = time.time() if now is None else now
    retry_after = error.retry_after if isinstance(error, RetryableError) else error.retry_after_seconds
    for value in (retry_after, error.reset_timestamp):
        if value is not None and (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or value < 0
            or value > sys.float_info.max
            or not isfinite(value)
        ):
            raise ValueError("Invalid provider rate-limit timing")
    delay = calculate_rate_limit_delay(
        retry_after_seconds=retry_after,
        reset_timestamp=error.reset_timestamp if error.remaining in (None, 0) else None,
        now=current,
        fallback_delay=60,
        safety_margin=0,
        max_delay=sys.float_info.max,
    )
    resume_at = delay.resume_at
    # A header-derived fallback delay must not hide a known primary reset.
    if error.remaining in (None, 0) and error.reset_timestamp is not None:
        reset = calculate_rate_limit_delay(
            reset_timestamp=error.reset_timestamp,
            now=current,
            fallback_delay=0,
            safety_margin=0,
            max_delay=sys.float_info.max,
        )
        resume_at = max(resume_at, reset.resume_at)
    identities = tuple(
        dict.fromkeys(
            ("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", error.credential_identity or "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT")
        )
    )
    pool = _get_read_token_pool()
    local = pool.active_cooldown_for(identities, now=current) if pool is not None else None
    persisted = active_cooldown(provider, credential_identity=identities, now=current, use_writer_token=True)
    for active in (local, persisted):
        if active is not None:
            resume_at = max(resume_at, active[1].resume_at)
    return resume_at


class DispatcherWakeup:
    """Run a dispatcher step and durably defer only confirmed provider rate limits."""

    def run(self, *, mode: str, default_branch: str) -> None:
        """Check throttle state or POST the throttler dispatch using the default token."""
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        if not re.fullmatch(r"[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("GITHUB_REPOSITORY must use owner/repo format")
        if not default_branch:
            raise ValueError("default_branch must not be empty")
        if mode == "check":
            output_path = os.environ.get("GITHUB_OUTPUT", "")
            if not output_path:
                raise ValueError("GITHUB_OUTPUT must be set")
            if os.environ.get("GITHUB_EVENT_NAME") == "pull_request_target":
                provider = GitHubActionsProvider(repo=repository)
                now = time.time()
                paused = _provider_cooldown(provider, datetime.fromtimestamp(now, UTC))
                if paused is not None:
                    number, sha, event = self._current_wake_identity()
                    store = DispatcherWakeStore(provider)
                    if not store.enqueue(number, sha, event, paused[1].resume_at, now=now):
                        raise RuntimeError(
                            "Dispatcher wake was not preserved; the scheduler wake-up was not handled "
                            f"(reason: {store.last_refusal})"
                        )
                    with open(output_path, "a", encoding="utf-8") as output:
                        output.write("throttled=true\n")
                    print(
                        f"::notice::Dispatcher wake deferred by provider cooldown for PR {number} "
                        f"head {sha} event {event}."
                    )
                    return
            DispatcherThrottle(on_rate_limit=self._preserve, max_attempts=1, retry_window_seconds=0).check(
                repository=repository, default_branch=default_branch, output_path=output_path
            )
        elif mode == "dispatch":
            self._dispatch(repository, default_branch)
        else:
            raise ValueError("mode must be check or dispatch")

    def _dispatch(self, repository: str, default_branch: str) -> None:  # noqa: C901
        wake_candidate: tuple[DispatcherWakeStore, str, dict] | None = None
        if os.environ.get("GITHUB_EVENT_NAME") == "pull_request_target":
            provider = GitHubActionsProvider(repo=repository)
            now = time.time()
            paused = _provider_cooldown(provider, datetime.fromtimestamp(now, UTC))
            if paused is not None:
                number, sha, event = self._current_wake_identity()
                store = DispatcherWakeStore(provider)
                if not store.enqueue(number, sha, event, paused[1].resume_at, now=now):
                    raise RuntimeError(
                        "Dispatcher wake was not preserved; the scheduler wake-up was not handled "
                        f"(reason: {store.last_refusal})"
                    )
                print(
                    f"::notice::Dispatcher wake deferred by provider cooldown for PR {number} head {sha} event {event}."
                )
                return
            wake_store = DispatcherWakeStore(provider)
            try:
                number, sha, event = self._current_wake_identity()
                key = wake_store._key(number, sha, event)
                entry = wake_store.entries().get(key)
                if entry is not None and (
                    entry.get("pr_number"),
                    entry.get("head_sha"),
                    entry.get("event"),
                ) == (number, sha, event):  # pragma: no cover - integration regression covers snapshot matching
                    wake_candidate = (wake_store, key, entry)
            except Exception as exc:  # pragma: no cover - integration regression covers lookup failures
                print(f"::warning::Dispatcher wake snapshot lookup failed ({type(exc).__name__}).")
        try:
            _gh_api(
                f"/repos/{repository}/actions/workflows/ai-pr-loop-throttler.yml/dispatches",
                method="POST",
                body={"ref": default_branch},
                read_pool=False,
            )
        except ProviderRateLimitError as exc:
            if exc.is_rate_limit:
                self._preserve(exc)
            raise
        except RetryableError as exc:
            if not exc.is_rate_limit:
                raise
            error = ProviderRateLimitError(
                retry_after_seconds=exc.retry_after,
                reset_timestamp=exc.reset_timestamp,
                remaining=exc.remaining,
                provider=exc.provider,
                credential_identity=exc.credential_identity,
                source=exc.source,
            )
            self._preserve(error)
            return  # pragma: no cover - _preserve always raises
        if wake_candidate is not None:  # pragma: no cover - workflow regression exercises the handoff
            wake_store, key, expected_entry = wake_candidate
            try:
                if not wake_store.acknowledge(
                    key, expected_entry
                ):  # pragma: no cover - integration regression covers CAS mismatch
                    print("::warning::Dispatcher wake acknowledgement was not applied.")
            except Exception as exc:  # pragma: no cover - integration regression covers acknowledgment failure
                print(f"::warning::Dispatcher wake acknowledgement failed ({type(exc).__name__}).")

    def _preserve(self, error: ProviderRateLimitError) -> None:
        """Persist before any in-job backoff, then fail visibly without dispatching."""
        number, sha, event = self._current_wake_identity()
        provider = GitHubActionsProvider(repo=os.environ["GITHUB_REPOSITORY"])
        now = time.time()
        resume_at = wake_resume_at(provider, error, now)
        shared_error = ProviderRateLimitError(
            reset_timestamp=resume_at,
            remaining=0,
            provider=error.provider,
            credential_identity=error.credential_identity,
            source=error.source or "x-ratelimit-reset",
        )
        try:
            shared_cooldown = persist_cooldown(provider, shared_error, now=now)
            shared_record = shared_cooldown[1] if shared_cooldown is not None else None
            persisted_resume_at = getattr(shared_record, "resume_at", None)
            shared_persisted = (
                isinstance(persisted_resume_at, (int, float))
                and not isinstance(persisted_resume_at, bool)
                and persisted_resume_at >= resume_at
            )
        except Exception as exc:
            shared_persisted = False
            print(f"::warning::Shared provider cooldown persistence failed ({type(exc).__name__}).")
        store = DispatcherWakeStore(provider)
        if not store.enqueue(number, sha, event, resume_at, now=now):
            raise RuntimeError(
                "Dispatcher wake was not preserved; the scheduler wake-up was not handled "
                f"(reason: {store.last_refusal})"
            ) from error
        if not shared_persisted:
            print(
                "::warning::Shared provider cooldown persistence is unconfirmed or shorter than the resolved deadline; "
                "the persisted wake deadline remains a fallback gate."
            )
        print("::notice::Dispatcher wake persisted; throttler dispatch remains pending.")
        raise error

    @staticmethod
    def _current_wake_identity() -> tuple[int, str, str]:
        event_path = os.environ.get("GITHUB_EVENT_PATH", "")
        if not event_path or os.environ.get("GITHUB_EVENT_NAME") != "pull_request_target":
            raise ValueError("A pull_request_target GITHUB_EVENT_PATH is required")
        payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Invalid dispatcher event payload")
        action = payload.get("action")
        pr = payload.get("pull_request")
        if not isinstance(action, str) or action not in _ACTIONS or not isinstance(pr, dict):
            raise ValueError("Invalid dispatcher pull request event")
        number, head = pr.get("number"), pr.get("head")
        sha = head.get("sha") if isinstance(head, dict) else None
        if not isinstance(number, int) or isinstance(number, bool) or number <= 0:
            raise ValueError("Invalid dispatcher pull request number")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-fA-F]{40}", sha):
            raise ValueError("Invalid dispatcher pull request head")
        run_id = os.environ.get("GITHUB_RUN_ID", "")
        if not re.fullmatch(r"[0-9]{1,20}", run_id) or int(run_id) <= 0:
            raise ValueError("GITHUB_RUN_ID must be a positive ASCII decimal run identity")
        return number, sha.lower(), f"pull_request_target:{action}:{int(run_id)}"


def main(argv: list[str] | None = None) -> None:
    """Run the durable dispatcher producer without embedding policy in YAML."""
    parser = argparse.ArgumentParser(description="Run an AI PR Loop dispatcher step with durable rate-limit recovery")
    parser.add_argument("--mode", choices=("check", "dispatch"), required=True)
    parser.add_argument("--default-branch", required=True)
    args = parser.parse_args(argv)
    try:
        DispatcherWakeup().run(mode=args.mode, default_branch=args.default_branch)
    except (OSError, RuntimeError, ValueError, ProviderRateLimitError, RetryableError) as exc:
        print(f"::error::{exc}", file=sys.stderr)
        raise SystemExit(1) from exc
