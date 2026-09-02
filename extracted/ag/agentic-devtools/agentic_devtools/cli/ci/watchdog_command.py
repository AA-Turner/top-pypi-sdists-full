"""CLI entry point for restarting a stalled AI PR loop."""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import sys
import time
from datetime import UTC, datetime
from math import ceil
from typing import Any
from urllib.parse import quote

from agentic_devtools.cli.ci.cooldown import (
    CooldownRecord,
    active_cooldown,
    ai_pr_loop_credential_identities,
    format_resume_at,
    persist_cooldown,
)
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider, _gh_api
from agentic_devtools.cli.ci.logging_config import setup_logging
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo

logger = logging.getLogger(__name__)

THROTTLER_WORKFLOW = "ai-pr-loop-throttler.yml"
COOLDOWN_SECONDS = 60
REDISPATCH_COOLDOWN_SECONDS = 65
REDISPATCH_MAX_HORIZON_SECONDS = 300


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _parse_timestamp(value: str) -> datetime | None:
    raw = value.strip()
    if not raw:
        return None
    normalized = raw.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _writer_token() -> str | None:
    token = os.environ.get("REPO_VARIABLE_WRITER_PAT", "").strip()
    return token or None


def _get_default_branch(repo: str, *, token: str | None = None) -> str:
    response = _gh_api(f"/repos/{repo}", token=token)
    data = json.loads(response)
    default_branch = data.get("default_branch")
    if not isinstance(default_branch, str) or not default_branch.strip():
        raise RuntimeError(f"Could not resolve default_branch for repository {repo!r}")
    return default_branch.strip()


def _get_latest_throttler_run(repo: str, default_branch: str, *, token: str | None = None) -> dict[str, Any] | None:
    endpoint = (
        f"/repos/{repo}/actions/workflows/{quote(THROTTLER_WORKFLOW, safe='')}/runs"
        f"?per_page=1&branch={quote(default_branch, safe='')}"
    )
    response = _gh_api(endpoint, token=token)
    data = json.loads(response)
    runs = data.get("workflow_runs")
    if not isinstance(runs, list) or not runs:
        return None
    run = runs[0]
    if not isinstance(run, dict):
        return None
    return run


def _dispatch_throttler(repo: str, default_branch: str) -> None:
    _gh_api(
        f"/repos/{repo}/actions/workflows/{quote(THROTTLER_WORKFLOW, safe='')}/dispatches",
        method="POST",
        body={"ref": default_branch},
    )


def _prefer_writer_token() -> bool:
    return _writer_token() is not None


def _provider_cooldown(
    provider: GitHubActionsProvider,
    now_utc: datetime,
) -> tuple[str, CooldownRecord] | None:
    return active_cooldown(
        provider,
        credential_identity=ai_pr_loop_credential_identities(),
        now=now_utc.timestamp(),
        use_writer_token=_prefer_writer_token(),
    )


def _cooldown_gate_output(
    paused: tuple[str, CooldownRecord] | None,
    now_utc: datetime,
) -> dict[str, Any]:
    """Build serialized cooldown-gate output for workflow consumers."""
    output: dict[str, Any] = {"cooldown_active": False}
    if paused is None:
        return output
    key, record = paused
    provider_name, _, credential_identity = key.partition(":")
    remaining = max(0, ceil(record.resume_at - now_utc.timestamp()))
    output.update(
        {
            "cooldown_active": True,
            "cooldown_key": key,
            "cooldown_provider": provider_name or "github",
            "cooldown_credential": credential_identity or "unknown",
            "cooldown_reason": record.reason,
            "cooldown_source": record.source,
            "cooldown_resume_at": format_resume_at(record.resume_at),
            "cooldown_remaining_seconds": remaining,
        }
    )
    return output


def _write_github_output(values: dict[str, bool | int]) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT", "")
    if not output_path:
        return
    try:
        with open(output_path, "a", encoding="utf-8") as handle:
            for key, value in values.items():
                rendered = str(value).lower() if isinstance(value, bool) else str(value)
                handle.write(f"{key}={rendered}\n")
    except OSError as exc:
        logger.warning("Could not write GITHUB_OUTPUT to %r: %s", output_path, exc)


def _build_throttle_state(latest_run: dict[str, Any] | None, now_utc: datetime) -> tuple[bool, str, int | None]:
    if latest_run is None:
        return False, "no_prior_run", None

    status = latest_run.get("status")
    conclusion = latest_run.get("conclusion")
    updated_at = latest_run.get("updated_at")

    if isinstance(status, str) and status and status != "completed":
        return True, "in_progress", None

    if isinstance(conclusion, str) and conclusion and conclusion != "success":
        return False, "last_run_not_success", None

    updated_at_text = updated_at if isinstance(updated_at, str) else ""
    updated_at_dt = _parse_timestamp(updated_at_text)
    if updated_at_dt is None:
        return False, "no_prior_run", None

    elapsed_seconds = max(0, int((now_utc - updated_at_dt).total_seconds()))
    if elapsed_seconds < COOLDOWN_SECONDS:
        return True, "cooldown", elapsed_seconds
    return False, "not_throttled", elapsed_seconds


def _build_redispatch_timing_output(
    latest_run: dict[str, Any] | None,
    paused: tuple[str, CooldownRecord] | None,
    now_utc: datetime,
) -> dict[str, Any]:
    output: dict[str, Any] = {
        "decision": "dispatch",
        "should_dispatch": True,
        "sleep_seconds": 0,
        "throttle_reason": "no_prior_run",
        "cooldown_key": None,
        "cooldown_source": None,
        "cooldown_resume_at": None,
        "cooldown_remaining_seconds": None,
    }

    if latest_run is not None:
        status = latest_run.get("status")
        conclusion = latest_run.get("conclusion")
        updated_at = latest_run.get("updated_at")
        if isinstance(status, str) and status and status != "completed":
            output.update(
                {
                    "decision": "defer_to_watchdog",
                    "should_dispatch": False,
                    "throttle_reason": "in_progress",
                    "sleep_seconds": 0,
                }
            )
            return output
        if isinstance(conclusion, str) and conclusion and conclusion != "success":
            output["throttle_reason"] = "last_run_not_success"
        else:
            updated_at_dt = _parse_timestamp(updated_at if isinstance(updated_at, str) else "")
            if updated_at_dt is not None:
                elapsed_seconds = max(0, int((now_utc - updated_at_dt).total_seconds()))
                output["sleep_seconds"] = max(0, REDISPATCH_COOLDOWN_SECONDS - elapsed_seconds)
                output["throttle_reason"] = "cooldown"

    if paused is not None:
        key, record = paused
        remaining = max(0, ceil(record.resume_at - now_utc.timestamp()))
        output.update(
            {
                "cooldown_key": key,
                "cooldown_source": record.source,
                "cooldown_resume_at": format_resume_at(record.resume_at),
                "cooldown_remaining_seconds": remaining,
            }
        )
        if remaining > output["sleep_seconds"]:
            output["sleep_seconds"] = remaining
            output["throttle_reason"] = "provider_cooldown"

    if output["sleep_seconds"] > REDISPATCH_MAX_HORIZON_SECONDS:
        output.update(
            {
                "decision": "defer_to_watchdog",
                "should_dispatch": False,
                "sleep_seconds": 0,
            }
        )
    return output


def _build_redispatch_recheck_output(
    paused: tuple[str, CooldownRecord] | None,
    latest_run: dict[str, Any] | None,
    now_utc: datetime,
) -> dict[str, Any]:
    if paused is not None:
        key, record = paused
        return {
            "decision": "defer_to_watchdog",
            "should_dispatch": False,
            "throttle_reason": "provider_cooldown",
            "cooldown_key": key,
            "cooldown_source": record.source,
            "cooldown_resume_at": format_resume_at(record.resume_at),
            "cooldown_remaining_seconds": max(0, ceil(record.resume_at - now_utc.timestamp())),
        }

    throttled, throttle_reason, elapsed_seconds = _build_throttle_state(latest_run, now_utc)
    if throttled:
        return {
            "decision": "defer_to_watchdog",
            "should_dispatch": False,
            "throttle_reason": throttle_reason,
            "elapsed_seconds": elapsed_seconds,
            "cooldown_key": None,
            "cooldown_source": None,
            "cooldown_resume_at": None,
            "cooldown_remaining_seconds": None,
        }
    return {
        "decision": "dispatch",
        "should_dispatch": True,
        "throttle_reason": throttle_reason,
        "elapsed_seconds": elapsed_seconds,
        "cooldown_key": None,
        "cooldown_source": None,
        "cooldown_resume_at": None,
        "cooldown_remaining_seconds": None,
    }


def _calculate_redispatch_timing(
    provider: GitHubActionsProvider,
    repo: str,
    default_branch_hint: str | None,
    now_utc: datetime,
) -> dict[str, Any]:
    """Calculate the current redispatch timing decision and cooldown state."""
    paused = _provider_cooldown(provider, now_utc)
    preferred_token = _writer_token() if paused is not None else None
    default_branch = default_branch_hint
    if default_branch is None and (paused is None or preferred_token is not None):
        default_branch = _get_default_branch(repo, token=preferred_token)
    latest_run: dict[str, Any] | None = None
    if default_branch is not None and (paused is None or preferred_token is not None):
        latest_run = _get_latest_throttler_run(repo, default_branch, token=preferred_token)
    return _build_redispatch_timing_output(latest_run, paused, now_utc)


def _run_redispatch_wait(
    provider: GitHubActionsProvider,
    repo: str,
    default_branch_hint: str | None,
) -> None:
    """Wait in bounded intervals and recheck redispatch eligibility in Python."""
    call_start = time.monotonic()
    output = _calculate_redispatch_timing(provider, repo, default_branch_hint, _utc_now())
    remaining = max(0, int(output["sleep_seconds"]))
    while output["should_dispatch"] and remaining > 0:
        elapsed = time.monotonic() - call_start
        budget_left = max(0.0, REDISPATCH_MAX_HORIZON_SECONDS - elapsed)
        if remaining > budget_left:
            # Remaining cooldown exceeds the wait budget; defer to the scheduled watchdog
            output = {**output, "decision": "defer_to_watchdog", "should_dispatch": False}
            remaining = 0
            break
        time.sleep(min(remaining, 60))
        output = _calculate_redispatch_timing(provider, repo, default_branch_hint, _utc_now())
        remaining = max(0, int(output["sleep_seconds"]))
    output["sleep_seconds"] = remaining
    _write_github_output({"should_dispatch": bool(output["should_dispatch"]), "sleep_seconds": remaining})
    print(json.dumps(output))


def ai_pr_loop_watchdog_command() -> None:
    """CLI entry point for agdt-ai-pr-loop-watchdog."""
    setup_logging()

    parser = argparse.ArgumentParser(description="Restart ai-pr-loop throttler when eligible PRs exist")
    parser.add_argument(
        "--mode",
        choices=("watchdog", "cooldown-gate", "redispatch-timing", "redispatch-recheck", "redispatch-wait"),
        default="watchdog",
        help="Command mode: normal watchdog dispatch or redispatch cooldown evaluation.",
    )
    parser.add_argument("--repo", type=str, default=None, help="Repository (owner/repo)")
    parser.add_argument("--default-branch", type=str, default=None, help="Default branch override")
    args = parser.parse_args()

    if shutil.which("gh") is None:
        print("Error: 'gh' CLI not found on PATH.", file=sys.stderr)
        sys.exit(10)

    repo_hint = args.repo or os.environ.get("GITHUB_REPOSITORY")
    repo = resolve_github_repo(repo_hint)
    provider = GitHubActionsProvider(repo=repo)
    branch_hint = args.default_branch or os.environ.get("GITHUB_DEFAULT_BRANCH", "")

    try:
        if args.mode == "cooldown-gate":
            now_utc = _utc_now()
            output = _cooldown_gate_output(_provider_cooldown(provider, now_utc), now_utc)
            _write_github_output(
                {
                    "cooldown_active": bool(output["cooldown_active"]),
                    "cooldown_remaining_seconds": int(output.get("cooldown_remaining_seconds") or 0),
                }
            )
            if output["cooldown_active"]:
                print(
                    "::notice::Provider cooldown active; "
                    f"provider={output['cooldown_provider']} "
                    f"credential={output['cooldown_credential']} "
                    f"reason={output['cooldown_reason']} "
                    f"source={output['cooldown_source']} "
                    f"resume_at={output['cooldown_resume_at']} "
                    f"remaining_delay={output['cooldown_remaining_seconds']}s. "
                    "Skipping provider work."
                )
            print(json.dumps(output))
            return
        if args.mode == "redispatch-timing":
            output = _calculate_redispatch_timing(provider, repo, args.default_branch, _utc_now())
            _write_github_output(
                {"should_dispatch": bool(output["should_dispatch"]), "sleep_seconds": int(output["sleep_seconds"])}
            )
            print(json.dumps(output))
            return
        if args.mode == "redispatch-wait":
            _run_redispatch_wait(provider, repo, args.default_branch)
            return
        if args.mode == "redispatch-recheck":
            now_utc = _utc_now()
            paused = _provider_cooldown(provider, now_utc)
            default_branch = args.default_branch
            recheck_latest_run: dict[str, Any] | None = None
            if paused is None:
                if default_branch is None:
                    default_branch = _get_default_branch(repo)
                recheck_latest_run = _get_latest_throttler_run(repo, default_branch)
            output = _build_redispatch_recheck_output(paused, recheck_latest_run, now_utc)
            _write_github_output({"should_dispatch": bool(output["should_dispatch"])})
            print(json.dumps(output))
            return

        now_utc = _utc_now()
        paused = _provider_cooldown(provider, now_utc)
        if paused is not None:
            key, record = paused
            remaining = max(0, int(record.resume_at - now_utc.timestamp()))
            print(
                f"::notice::ai-pr-loop-watchdog provider cooldown active "
                f"(key={key}, source={record.source}, resume_at={format_resume_at(record.resume_at)}, "
                f"remaining_delay={remaining}s)"
            )
            print(
                json.dumps(
                    {
                        "repo": repo,
                        "default_branch": branch_hint,
                        "decision": "rate_limit_paused",
                        "throttled": False,
                        "throttle_reason": "provider_cooldown",
                        "elapsed_seconds": None,
                        "eligible_count": None,
                        "dispatched": False,
                        "cooldown_key": key,
                        "cooldown_source": record.source,
                        "cooldown_resume_at": format_resume_at(record.resume_at),
                        "cooldown_remaining_seconds": remaining,
                    }
                )
            )
            return

        default_branch = args.default_branch or _get_default_branch(repo)
        latest_run = _get_latest_throttler_run(repo, default_branch)
        throttled, throttle_reason, elapsed_seconds = _build_throttle_state(latest_run, now_utc)

        if throttled:
            print(f"::notice::ai-pr-loop-watchdog throttled ({throttle_reason})")
            output = {
                "repo": repo,
                "default_branch": default_branch,
                "decision": "throttled",
                "throttled": True,
                "throttle_reason": throttle_reason,
                "elapsed_seconds": elapsed_seconds,
                "eligible_count": None,
                "dispatched": False,
            }
            print(json.dumps(output))
            return

        eligible = provider.list_eligible_prs(max_prs=1)
        eligible_count = len(eligible)
        if eligible_count == 0:
            print("::notice::ai-pr-loop-watchdog no eligible scheduler PRs")
            output = {
                "repo": repo,
                "default_branch": default_branch,
                "decision": "no_eligible_prs",
                "throttled": False,
                "throttle_reason": throttle_reason,
                "elapsed_seconds": elapsed_seconds,
                "eligible_count": 0,
                "dispatched": False,
            }
            print(json.dumps(output))
            return

        _dispatch_throttler(repo, default_branch)
        print("::notice::ai-pr-loop-watchdog dispatched ai-pr-loop-throttler.yml")
        output = {
            "repo": repo,
            "default_branch": default_branch,
            "decision": "dispatched",
            "throttled": False,
            "throttle_reason": throttle_reason,
            "elapsed_seconds": elapsed_seconds,
            "eligible_count": eligible_count,
            "dispatched": True,
        }
        print(json.dumps(output))
    except RetryableError as exc:
        if not exc.is_rate_limit:
            logger.exception("AI PR loop watchdog failed: %s", exc)
            sys.exit(1)
        rate_limit_exc = ProviderRateLimitError(
            retry_after_seconds=exc.retry_after,
            reset_timestamp=exc.reset_timestamp,
            remaining=exc.remaining,
            provider=exc.provider,
            credential_identity=exc.credential_identity,
            source=exc.source,
            is_rate_limit=True,
        )
        paused = persist_cooldown(provider, rate_limit_exc)
        key = ""
        source = rate_limit_exc.source
        resume_at = ""
        remaining = 0
        if paused is not None:
            key, record = paused
            source = record.source
            resume_at = format_resume_at(record.resume_at)
            remaining = max(0, int(record.resume_at - _utc_now().timestamp()))
        logger.warning(
            "Watchdog paused after provider rate-limit: "
            "provider=%s credential=%s source=%s resume_at=%s remaining_delay=%ss",
            rate_limit_exc.provider or "github",
            rate_limit_exc.credential_identity or "unknown",
            source or "unknown",
            resume_at or "unknown",
            remaining,
        )
        print(
            json.dumps(
                {
                    "repo": repo,
                    "default_branch": branch_hint,
                    "decision": "rate_limit_paused",
                    "throttled": False,
                    "throttle_reason": "provider_cooldown",
                    "elapsed_seconds": None,
                    "eligible_count": None,
                    "dispatched": False,
                    "cooldown_key": key,
                    "cooldown_source": source,
                    "cooldown_resume_at": resume_at,
                    "cooldown_remaining_seconds": remaining,
                }
            )
        )
    except ProviderRateLimitError as exc:
        if not exc.is_rate_limit:
            logger.exception("AI PR loop watchdog failed: %s", exc)
            sys.exit(1)
        paused = persist_cooldown(provider, exc)
        key = ""
        source = exc.source
        resume_at = ""
        remaining = 0
        if paused is not None:
            key, record = paused
            source = record.source
            resume_at = format_resume_at(record.resume_at)
            remaining = max(0, int(record.resume_at - _utc_now().timestamp()))
        logger.warning(
            "Watchdog paused after provider rate-limit: "
            "provider=%s credential=%s source=%s resume_at=%s remaining_delay=%ss",
            exc.provider or "github",
            exc.credential_identity or "unknown",
            source or "unknown",
            resume_at or "unknown",
            remaining,
        )
        print(
            json.dumps(
                {
                    "repo": repo,
                    "default_branch": branch_hint,
                    "decision": "rate_limit_paused",
                    "throttled": False,
                    "throttle_reason": "provider_cooldown",
                    "elapsed_seconds": None,
                    "eligible_count": None,
                    "dispatched": False,
                    "cooldown_key": key,
                    "cooldown_source": source,
                    "cooldown_resume_at": resume_at,
                    "cooldown_remaining_seconds": remaining,
                }
            )
        )
    except Exception as exc:
        logger.exception("AI PR loop watchdog failed: %s", exc)
        sys.exit(1)
