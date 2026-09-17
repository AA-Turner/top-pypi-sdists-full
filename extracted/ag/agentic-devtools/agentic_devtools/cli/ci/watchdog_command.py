"""CLI entry point for restarting a stalled AI PR loop."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import sys
import time
from datetime import UTC, datetime, timedelta
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
from agentic_devtools.cli.ci.credential_roles import (
    DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,
    require_default_repo_workflow_token,
)
from agentic_devtools.cli.ci.due_probe_wakeup import run_due_probe_wakeup
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider, _gh_api
from agentic_devtools.cli.ci.logging_config import setup_logging
from agentic_devtools.cli.ci.pipeline.session_detector import is_copilot_session_active_via_agent_task
from agentic_devtools.cli.ci.reconciliation.models import CooldownProbe, CooldownState, ProbeStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import QueueStore, QueueStoreError
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo

logger = logging.getLogger(__name__)

THROTTLER_WORKFLOW = "ai-pr-loop-throttler.yml"
REDISPATCH_WORKFLOW = "ai-pr-loop-redispatch.yml"
COOLDOWN_SECONDS = 60
REDISPATCH_COOLDOWN_SECONDS = 65
REDISPATCH_MAX_HORIZON_SECONDS = 300
REDISPATCH_MAX_OPEN_PR_PAGES = 5
REDISPATCH_MAX_CLOSED_PR_PAGES = 5
AUTHORIZATION_STATUS_PATTERN = re.compile(
    r"(^|[^A-Za-z0-9])HTTP(/[0-9]+(\.[0-9]+)?)?\s+(401|403)([^0-9]|$)",
    re.IGNORECASE,
)


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


def _is_authorization_failure(error_text: str) -> bool:
    lowered = error_text.lower()
    return (
        AUTHORIZATION_STATUS_PATTERN.search(error_text) is not None
        or "resource not accessible by personal access token" in lowered
        or "repository.pullrequests" in lowered
    )


def _token_from_env(name: str) -> str:
    return os.environ.get(name, "").strip()


def _dispatch_with_token(workflow: str, repo: str, default_branch: str, token: str) -> tuple[int, str]:
    try:
        _gh_api(
            f"/repos/{repo}/actions/workflows/{quote(workflow, safe='')}/dispatches",
            method="POST",
            body={"ref": default_branch},
            token=token,
        )
    except RetryableError as exc:
        return 2, str(exc)
    except RuntimeError as exc:
        message = str(exc)
        if _is_authorization_failure(message):
            return 1, message
        return 2, message
    return 0, ""


def auto_approve_waiting_runs(repo: str, token: str) -> int:
    """Approve same-repository workflow runs waiting for manual approval."""
    approved_count = 0
    try:
        response = _gh_api(f"/repos/{repo}/actions/runs?status=waiting", token=token)
        data = json.loads(response)
        workflow_runs = data.get("workflow_runs", [])
        if not isinstance(workflow_runs, list):
            raise ValueError("waiting workflow response did not contain a list")
    except Exception as exc:
        logger.warning("Could not list waiting workflow runs for %s: %s", repo, exc)
        return 0

    for run in workflow_runs:
        if not isinstance(run, dict):
            continue
        head_repository = run.get("head_repository")
        if not isinstance(head_repository, dict) or head_repository.get("full_name") != repo:
            continue
        run_id = run.get("id")
        if not isinstance(run_id, int) or isinstance(run_id, bool) or run_id <= 0:
            logger.warning("Skipping waiting workflow run with invalid id: %r", run_id)
            continue
        try:
            _gh_api(
                f"/repos/{repo}/actions/runs/{run_id}/approve",
                method="POST",
                token=token,
            )
        except Exception as exc:
            logger.warning("Could not approve waiting workflow run %s: %s", run_id, exc)
            continue
        approved_count += 1
        logger.info("Approved waiting workflow run %s for %s", run_id, repo)
        print(f"::notice::Approved waiting workflow run {run_id}")
    return approved_count


def _review_has_comments(provider: GitHubActionsProvider, pr_number: int, review: Any) -> bool:
    """Return whether a COMMENTED review contains body or inline comments."""
    if isinstance(getattr(review, "body", None), str) and review.body.strip():
        return True
    review_id = getattr(review, "id", 0)
    if not isinstance(review_id, int) or isinstance(review_id, bool) or review_id <= 0:
        return False
    try:
        return bool(provider.list_review_comments(pr_number, review_id))
    except Exception as exc:
        logger.warning(
            "Could not inspect comments for PR #%d review %s: %s",
            pr_number,
            review_id,
            exc,
        )
        return False


def _workflow_run_pr_number(run: Any) -> int:
    if isinstance(run, dict):
        pull_requests = run.get("pull_requests")
        if isinstance(pull_requests, list):
            for pull_request in pull_requests:
                if isinstance(pull_request, dict) and isinstance(pull_request.get("number"), int):
                    return pull_request["number"]
        value = run.get("pr_number")
    else:
        value = getattr(run, "pr_number", 0)
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def _active_workflow_prs(provider: GitHubActionsProvider) -> set[int] | None:
    try:
        try:
            runs = provider.list_workflow_runs(
                "ai-pr-loop.yml",
                window_hours=24,
                include_dispatch_inputs=True,
            )
        except TypeError:
            runs = provider.list_workflow_runs("ai-pr-loop.yml", window_hours=24)
    except Exception as exc:
        logger.warning("Could not inspect active AI PR loop workflow runs: %s", exc)
        return None

    active_prs: set[int] = set()
    active_statuses = {"queued", "in_progress", "waiting", "requested"}
    for run in runs:
        if isinstance(run, dict):
            status = run.get("status", "")
            conclusion = run.get("conclusion")
        else:
            status = getattr(run, "status", "")
            conclusion = getattr(run, "conclusion", "")
        is_active = status in active_statuses or not conclusion
        pr_number = _workflow_run_pr_number(run)
        if is_active and pr_number > 0:
            active_prs.add(pr_number)
    return active_prs


def find_stalled_unaddressed_reviews(
    provider: GitHubActionsProvider,
    repo: str,
    token: str,
    max_age_minutes: int = 15,
) -> list[int]:
    """Find open PRs whose old actionable reviews have no active processing."""
    if max_age_minutes < 0:
        raise ValueError("max_age_minutes must be non-negative")
    try:
        eligible_prs = provider.list_eligible_prs(max_prs=None)
    except Exception as exc:
        logger.warning("Could not inspect eligible PRs for stalled reviews: %s", exc)
        return []

    cutoff = _utc_now() - timedelta(minutes=max_age_minutes)
    candidates: list[int] = []
    for eligible_pr in eligible_prs:
        pr_number = getattr(eligible_pr, "number", 0)
        if not isinstance(pr_number, int) or isinstance(pr_number, bool) or pr_number <= 0:
            continue
        try:
            reviews = provider.list_reviews(pr_number)
        except Exception as exc:
            logger.warning("Could not inspect reviews for PR #%d: %s", pr_number, exc)
            continue
        has_stalled_review = False
        for review in reviews:
            state = getattr(review, "state", "")
            if state not in {"CHANGES_REQUESTED", "COMMENTED"}:
                continue
            submitted_at = _parse_timestamp(getattr(review, "submitted_at", ""))
            if submitted_at is None or submitted_at >= cutoff:
                continue
            if state == "COMMENTED" and not _review_has_comments(provider, pr_number, review):
                continue
            has_stalled_review = True
            break
        if has_stalled_review:
            candidates.append(pr_number)

    if not candidates:
        return []
    active_workflow_prs = _active_workflow_prs(provider)
    if active_workflow_prs is None:
        return []
    stalled: list[int] = []
    for pr_number in candidates:
        try:
            active_task = is_copilot_session_active_via_agent_task(repo, pr_number, provider=provider)
        except Exception as exc:
            logger.warning("Could not inspect active agent task for PR #%d: %s", pr_number, exc)
            active_task = None
        if active_task is not False or pr_number in active_workflow_prs:
            continue
        stalled.append(pr_number)
    return stalled


def _dispatch_throttler_for_redispatch(repo: str, default_branch: str) -> int:
    try:
        token = require_default_repo_workflow_token("dispatch the throttler workflow")
    except RuntimeError as exc:
        print(f"::warning::{exc}")
        return 2
    dispatch_status, message = _dispatch_with_token(THROTTLER_WORKFLOW, repo, default_branch, token)
    if dispatch_status != 0 and message:
        print(f"::warning::Default repository-workflow credential dispatch failed: {message}")
    return dispatch_status


def _dispatch_redispatch_from_loop(repo: str, default_branch: str) -> int:
    try:
        token = require_default_repo_workflow_token("dispatch the redispatch workflow")
    except RuntimeError as exc:
        print(f"::warning::{exc}")
        return 2
    dispatch_status, message = _dispatch_with_token(REDISPATCH_WORKFLOW, repo, default_branch, token)
    if dispatch_status != 0 and message:
        print(f"::warning::Default repository-workflow credential dispatch failed: {message}")
    return dispatch_status


def _resolve_default_branch_for_throttler_dispatch(repo: str) -> str:
    token = require_default_repo_workflow_token("resolve the repository default branch")
    return _get_default_branch(repo, token=token)


def _resolve_default_branch_for_redispatch_dispatch(repo: str) -> str:
    token = require_default_repo_workflow_token("resolve the repository default branch")
    return _get_default_branch(repo, token=token)


def _read_open_pr_page(repo: str, token: str, page: int) -> list[dict[str, Any]]:
    response = _gh_api(
        f"/repos/{repo}/pulls?state=open&per_page=100&page={page}",
        token=token,
    )
    try:
        data = json.loads(response)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Open pull-request inventory was malformed; refusing redispatch.") from exc
    if not isinstance(data, list):
        raise RuntimeError("Open pull-request inventory was malformed; refusing redispatch.")
    if not all(isinstance(item, dict) for item in data):
        raise RuntimeError("Open pull-request inventory was malformed; refusing redispatch.")
    return data


def _is_cross_repository_pull_request(pr_payload: dict[str, Any], repo: str) -> bool:
    base = pr_payload.get("base")
    head = pr_payload.get("head")
    if not isinstance(base, dict) or not isinstance(head, dict):
        return True
    base_repo = base.get("repo")
    head_repo = head.get("repo")
    if not isinstance(base_repo, dict) or not isinstance(head_repo, dict):
        return True
    base_full_name = str(base_repo.get("full_name", "")).strip()
    head_full_name = str(head_repo.get("full_name", "")).strip()
    if not base_full_name or not head_full_name:
        return True
    return base_full_name != head_full_name or base_full_name != repo


def _eligible_open_pr_count(repo: str, token: str) -> int:
    eligible_count = 0
    for page in range(1, REDISPATCH_MAX_OPEN_PR_PAGES + 1):
        open_prs = _read_open_pr_page(repo, token, page)
        for pr in open_prs:
            if _is_cross_repository_pull_request(pr, repo):
                continue
            labels = pr.get("labels")
            if not isinstance(labels, list):
                raise RuntimeError("Open pull-request inventory was malformed; refusing redispatch.")
            label_names: list[str] = []
            for label in labels:
                if not isinstance(label, dict):
                    raise RuntimeError("Open pull-request inventory was malformed; refusing redispatch.")
                label_name = label.get("name")
                if not isinstance(label_name, str) or not label_name.strip():
                    raise RuntimeError("Open pull-request inventory was malformed; refusing redispatch.")
                label_names.append(label_name)
            if "ai-pr-loop-ignore" in label_names:
                continue
            eligible_count += 1
        if len(open_prs) < 100:
            break
    return eligible_count


def _latest_merged_at(repo: str, default_branch: str, token: str) -> str | None:
    latest_merge_time: datetime | None = None
    latest_merge_raw: str | None = None
    for page in range(1, REDISPATCH_MAX_CLOSED_PR_PAGES + 1):
        response = _gh_api(
            (
                f"/repos/{repo}/pulls?state=closed&base={quote(default_branch, safe='')}"
                f"&sort=updated&direction=desc&per_page=100&page={page}"
            ),
            token=token,
        )
        try:
            data = json.loads(response)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Merged pull-request inventory was malformed; refusing redispatch.") from exc
        if not isinstance(data, list):
            raise RuntimeError("Merged pull-request inventory was malformed; refusing redispatch.")
        if not data:
            break

        oldest_updated_at_in_page: datetime | None = None
        for item in data:
            if not isinstance(item, dict):
                raise RuntimeError("Merged pull-request inventory was malformed; refusing redispatch.")
            updated_at = item.get("updated_at")
            if not isinstance(updated_at, str) or not updated_at.strip():
                raise RuntimeError("Merged pull-request inventory was malformed; refusing redispatch.")
            parsed_updated_at = _parse_timestamp(updated_at)
            if parsed_updated_at is None:
                raise RuntimeError(
                    "Merged pull-request inventory returned an invalid update date; refusing redispatch."
                )
            if oldest_updated_at_in_page is None or parsed_updated_at < oldest_updated_at_in_page:
                oldest_updated_at_in_page = parsed_updated_at

            merged_at = item.get("merged_at")
            if merged_at is None:
                continue
            if not isinstance(merged_at, str) or not merged_at.strip():
                raise RuntimeError("Merged pull-request inventory was malformed; refusing redispatch.")
            parsed_merged_at = _parse_timestamp(merged_at)
            if parsed_merged_at is None:
                raise RuntimeError("Merged pull-request inventory returned an invalid merge date; refusing redispatch.")
            if latest_merge_time is None or parsed_merged_at > latest_merge_time:
                latest_merge_time = parsed_merged_at
                latest_merge_raw = merged_at.strip()

        if len(data) < 100:
            break
        if (
            latest_merge_time is not None
            and oldest_updated_at_in_page is not None
            and oldest_updated_at_in_page <= latest_merge_time
        ):
            break
    return latest_merge_raw


def _select_pr_read_token(repo: str) -> str:
    token = require_default_repo_workflow_token("read repository pull requests")
    try:
        probe = _gh_api(f"/repos/{repo}/pulls?state=open&per_page=1", token=token)
    except RetryableError as exc:
        raise RuntimeError(
            "Pull-request inventory probe failed for the default repository-workflow credential; "
            "refusing redispatch because the inventory is unavailable."
        ) from exc
    except RuntimeError as exc:
        raise RuntimeError(
            "Pull-request inventory probe failed for the default repository-workflow credential; "
            "refusing redispatch because the inventory is unavailable."
        ) from exc
    try:
        decoded = json.loads(probe)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Pull-request inventory probe returned a malformed response for the default "
            "repository-workflow credential; refusing redispatch."
        ) from exc
    if not isinstance(decoded, list):
        raise RuntimeError(
            "Pull-request inventory probe returned a malformed response for the default "
            "repository-workflow credential; refusing redispatch."
        )
    return token


def _run_redispatch_stop_conditions(repo: str, default_branch: str | None) -> None:
    should_dispatch = False
    output: dict[str, Any] = {"should_dispatch": False}
    try:
        pr_read_token = _select_pr_read_token(repo)
        resolved_default_branch = default_branch or _get_default_branch(repo, token=pr_read_token)
        eligible_count = _eligible_open_pr_count(repo, pr_read_token)
        if eligible_count == 0:
            print("No eligible open PRs — stopping loop.")
            _write_github_output({"should_dispatch": False})
            print(json.dumps(output))
            return
        merged_at = _latest_merged_at(repo, resolved_default_branch, pr_read_token)
        if merged_at is None:
            print("Could not determine last merge date — stopping loop (fail-safe).")
            _write_github_output({"should_dispatch": False})
            print(json.dumps(output))
            return
        last_merge_dt = _parse_timestamp(merged_at)
        if last_merge_dt is None:
            raise RuntimeError("Merged pull-request inventory returned an invalid merge date; refusing redispatch.")
        now_utc = _utc_now()
        elapsed_seconds = max(0, int((now_utc - last_merge_dt).total_seconds()))
        hours_since_merge = elapsed_seconds // 3600
        if hours_since_merge >= 24:
            print(
                f"No merges to main in {hours_since_merge}h — stopping loop "
                "(likely stuck PRs needing human intervention)."
            )
            _write_github_output({"should_dispatch": False})
            print(json.dumps(output))
            return
        print(f"Eligible open PRs: {eligible_count}")
        print(f"Last merge to main was {hours_since_merge}h ago — continuing loop.")
        should_dispatch = True
        output = {
            "should_dispatch": True,
            "eligible_open_pr_count": eligible_count,
            "hours_since_merge": hours_since_merge,
            "default_branch": resolved_default_branch,
        }
    except (RuntimeError, RetryableError) as exc:
        print(f"::error::{exc}")
    _write_github_output({"should_dispatch": should_dispatch})
    print(json.dumps(output))


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
    token = require_default_repo_workflow_token("dispatch the throttler workflow")
    _gh_api(
        f"/repos/{repo}/actions/workflows/{quote(THROTTLER_WORKFLOW, safe='')}/dispatches",
        method="POST",
        body={"ref": default_branch},
        token=token,
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


def _cooldown_state_from_record(key: str, record: CooldownRecord) -> CooldownState:
    """Convert a shared cooldown record into persisted due-probe state."""
    provider_identity, _, credential_identity = key.partition(":")
    return CooldownState(
        provider_identity=provider_identity or "github",
        credential_identity=credential_identity or "GH_TOKEN",
        cooldown_generation_id=(
            f"{provider_identity or 'github'}:{credential_identity or 'GH_TOKEN'}:{int(record.resume_at)}"
        ),
        resume_at=datetime.fromtimestamp(record.resume_at, UTC),
        reason=record.reason,
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


def _cooldown_availability(repo: str) -> tuple[bool, str]:
    """Return whether persisted cooldown probes establish provider availability."""
    state = QueueStore(repo=repo).load()
    for probe in _latest_probe_generation_candidates(state.probes):
        if probe.status in {ProbeStatus.PENDING, ProbeStatus.IN_PROGRESS, ProbeStatus.FAILED, ProbeStatus.ALERTABLE}:
            return False, f"cooldown_{probe.status.value}"
    return True, "available"


def _load_cooldown_state(repo: str) -> CooldownState | None:
    """Load the shared cooldown contract represented by the persisted probe."""
    try:
        state = QueueStore(repo=repo).load()
    except (QueueStoreError, RuntimeError) as exc:
        logger.warning("Cooldown state unavailable while preparing probe wake-up: %s", exc)
        return None
    candidates = _latest_probe_generation_candidates(state.probes)
    for probe in sorted(
        candidates,
        key=lambda item: (item.resume_at or item.next_probe_at or item.scheduled_at, item.cooldown_generation_id),
        reverse=True,
    ):
        if probe.status in {ProbeStatus.PENDING, ProbeStatus.IN_PROGRESS, ProbeStatus.FAILED, ProbeStatus.ALERTABLE}:
            return CooldownState(
                provider_identity=probe.provider_identity,
                credential_identity=probe.credential_identity,
                cooldown_generation_id=probe.cooldown_generation_id,
                resume_at=probe.resume_at or probe.scheduled_at,
                probe_status=probe.status,
                retry_count=probe.retry_count,
                next_probe_at=probe.next_probe_at,
                reason=probe.alert_reason,
            )
    return None


def _latest_probe_generation_candidates(probes: list[CooldownProbe]) -> list[CooldownProbe]:
    latest: dict[tuple[str, str], CooldownProbe] = {}
    for probe in probes:
        key = (probe.provider_identity, probe.credential_identity)
        current = latest.get(key)
        if current is None:
            latest[key] = probe
            continue
        current_time = current.resume_at or current.next_probe_at or current.scheduled_at
        probe_time = probe.resume_at or probe.next_probe_at or probe.scheduled_at
        if (probe_time, probe.cooldown_generation_id) >= (current_time, current.cooldown_generation_id):
            latest[key] = probe
    return list(latest.values())


def _seed_cooldown_state(latest_run: dict[str, Any] | None, now_utc: datetime) -> CooldownState | None:
    """Create the initial shared cooldown record from the latest throttler run."""
    throttled, reason, _ = _build_throttle_state(latest_run, now_utc)
    if not throttled or reason != "cooldown" or latest_run is None:
        return None
    updated_at = _parse_timestamp(str(latest_run.get("updated_at", "")))
    run_id = latest_run.get("id")
    if updated_at is None or not isinstance(run_id, int) or isinstance(run_id, bool):
        return None
    return CooldownState(
        provider_identity="github_actions",
        credential_identity=os.environ.get(
            "AGDT_COOLDOWN_CREDENTIAL_IDENTITY",
            DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,
        ),
        cooldown_generation_id=f"throttler-{run_id}",
        resume_at=updated_at + timedelta(seconds=COOLDOWN_SECONDS),
        reason="throttler_cooldown",
    )


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
    if paused is not None:
        return _build_redispatch_timing_output(None, paused, now_utc)
    token = require_default_repo_workflow_token("read repository workflow runs")
    default_branch = default_branch_hint
    if default_branch is None:
        default_branch = _get_default_branch(repo, token=token)
    latest_run: dict[str, Any] | None = None
    if default_branch is not None:
        latest_run = _get_latest_throttler_run(repo, default_branch, token=token)
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


def _run_due_probe_only(
    provider: GitHubActionsProvider,
    repo: str,
    *,
    default_branch_hint: str | None,
    now_utc: datetime,
) -> dict[str, Any]:
    """Evaluate only persisted due probes and skip scheduler dispatch work."""
    paused = _provider_cooldown(provider, now_utc)
    if paused is not None:
        key, record = paused
        due_probe_count = run_due_probe_wakeup(
            repo=repo,
            cooldown_state=_cooldown_state_from_record(key, record),
        )
        return {
            "repo": repo,
            "default_branch": default_branch_hint,
            "decision": "due_probe_only",
            "due_probe_count": due_probe_count,
            "cooldown_active": True,
            "cooldown_key": key,
            "cooldown_source": record.source,
            "cooldown_resume_at": format_resume_at(record.resume_at),
            "cooldown_remaining_seconds": max(0, int(record.resume_at - now_utc.timestamp())),
        }
    token = require_default_repo_workflow_token("read repository workflow runs")
    default_branch = default_branch_hint or _get_default_branch(repo, token=token)
    latest_run = _get_latest_throttler_run(repo, default_branch, token=token)
    approved_waiting_runs = auto_approve_waiting_runs(repo, token)
    cooldown_state = _load_cooldown_state(repo)
    if cooldown_state is None:
        cooldown_state = _seed_cooldown_state(latest_run, now_utc)
    if cooldown_state is None:
        due_probe_count = run_due_probe_wakeup(repo=repo)
    else:
        due_probe_count = run_due_probe_wakeup(repo=repo, cooldown_state=cooldown_state)
    return {
        "repo": repo,
        "default_branch": default_branch,
        "decision": "due_probe_only",
        "due_probe_count": due_probe_count,
        "approved_waiting_runs": approved_waiting_runs,
        "cooldown_active": False,
    }


def ai_pr_loop_watchdog_command() -> None:
    """CLI entry point for agdt-ai-pr-loop-watchdog."""
    setup_logging()

    parser = argparse.ArgumentParser(description="Restart ai-pr-loop throttler when eligible PRs exist")
    parser.add_argument(
        "--mode",
        choices=(
            "watchdog",
            "due-probe-only",
            "cooldown-gate",
            "redispatch-timing",
            "redispatch-recheck",
            "redispatch-wait",
            "redispatch-stop-conditions",
            "redispatch-dispatch-throttler",
            "redispatch-dispatch-redispatch",
        ),
        default="watchdog",
        help=(
            "Command mode: normal watchdog dispatch, redispatch cooldown evaluation, "
            "stop-condition checks, or redispatch workflow dispatch."
        ),
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
        if args.mode == "redispatch-stop-conditions":
            _run_redispatch_stop_conditions(repo, args.default_branch)
            return
        if args.mode == "redispatch-dispatch-throttler":
            default_branch = args.default_branch or _resolve_default_branch_for_throttler_dispatch(repo)
            dispatch_status = _dispatch_throttler_for_redispatch(repo, default_branch)
            if dispatch_status != 0:
                print(
                    "::warning::Could not dispatch ai-pr-loop-throttler.yml "
                    "(workflow may be disabled); watchdog will retry."
                )
            print(json.dumps({"dispatch_status": dispatch_status, "workflow": THROTTLER_WORKFLOW}))
            if dispatch_status != 0:
                sys.exit(dispatch_status)
            return
        if args.mode == "redispatch-dispatch-redispatch":
            default_branch = args.default_branch or _resolve_default_branch_for_redispatch_dispatch(repo)
            dispatch_status = _dispatch_redispatch_from_loop(repo, default_branch)
            if dispatch_status != 0:
                print("::warning::Failed to dispatch ai-pr-loop-redispatch.yml; continuing")
            print(json.dumps({"dispatch_status": dispatch_status, "workflow": REDISPATCH_WORKFLOW}))
            if dispatch_status != 0:
                sys.exit(dispatch_status)
            return
        if args.mode == "redispatch-recheck":
            now_utc = _utc_now()
            paused = _provider_cooldown(provider, now_utc)
            default_branch = args.default_branch
            recheck_latest_run: dict[str, Any] | None = None
            if paused is None:
                token = require_default_repo_workflow_token("read repository workflow runs")
                if default_branch is None:
                    default_branch = _get_default_branch(repo, token=token)
                recheck_latest_run = _get_latest_throttler_run(repo, default_branch, token=token)
            output = _build_redispatch_recheck_output(paused, recheck_latest_run, now_utc)
            _write_github_output({"should_dispatch": bool(output["should_dispatch"])})
            print(json.dumps(output))
            return
        if args.mode == "due-probe-only":
            output = _run_due_probe_only(
                provider,
                repo,
                default_branch_hint=args.default_branch,
                now_utc=_utc_now(),
            )
            if output["due_probe_count"] > 0:
                print(f"::notice::ai-pr-loop-watchdog evaluated {output['due_probe_count']} due probe(s)")
            print(json.dumps(output))
            return

        now_utc = _utc_now()
        paused = _provider_cooldown(provider, now_utc)
        if paused is not None:
            key, record = paused
            due_probe_count = 0
            try:
                due_probe_count = run_due_probe_wakeup(
                    repo=repo, cooldown_state=_cooldown_state_from_record(key, record)
                )
            except (QueueStoreError, RuntimeError) as exc:
                logger.warning("Due-probe wake-up unavailable during active cooldown; continuing: %s", exc)
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
                        "due_probe_count": due_probe_count,
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

        token = require_default_repo_workflow_token("read repository workflow runs")
        default_branch = args.default_branch or _get_default_branch(repo, token=token)
        latest_run = _get_latest_throttler_run(repo, default_branch, token=token)
        approved_waiting_runs = 0

        due_probe_count = 0
        availability_established = False
        availability_reason = "cooldown_state_unknown"
        try:
            cooldown_state = _load_cooldown_state(repo)
            if cooldown_state is None:
                cooldown_state = _seed_cooldown_state(latest_run, now_utc)
            if cooldown_state is None:
                due_probe_count = run_due_probe_wakeup(repo=repo)
            else:
                due_probe_count = run_due_probe_wakeup(repo=repo, cooldown_state=cooldown_state)
        except (QueueStoreError, RuntimeError) as exc:
            logger.warning("Due-probe wake-up unavailable; continuing: %s", exc)
        else:
            try:
                availability_established, availability_reason = _cooldown_availability(repo)
            except (QueueStoreError, RuntimeError) as exc:
                logger.warning("Cooldown availability state unavailable; continuing: %s", exc)
        if not availability_established:
            approved_waiting_runs = auto_approve_waiting_runs(repo, token)
            print(f"::notice::ai-pr-loop-watchdog dispatch blocked ({availability_reason})")
            print(
                json.dumps(
                    {
                        "repo": repo,
                        "decision": "cooldown_blocked",
                        "throttled": False,
                        "throttle_reason": "cooldown_state_unknown",
                        "elapsed_seconds": None,
                        "due_probe_count": due_probe_count,
                        "eligible_count": None,
                        "dispatched": False,
                        "availability_established": False,
                        "availability_reason": availability_reason,
                    }
                )
            )
            return

        throttled, throttle_reason, elapsed_seconds = _build_throttle_state(latest_run, now_utc)
        if due_probe_count > 0:
            print(f"::notice::ai-pr-loop-watchdog evaluated {due_probe_count} due probe(s)")

        stalled_prs = find_stalled_unaddressed_reviews(provider, repo, token)
        if stalled_prs:
            approved_waiting_runs = auto_approve_waiting_runs(repo, token)
            _dispatch_throttler(repo, default_branch)
            print(
                "::notice::ai-pr-loop-watchdog dispatched ai-pr-loop-throttler.yml "
                f"for stalled review PRs: {', '.join(str(pr) for pr in stalled_prs)}"
            )
            print(
                json.dumps(
                    {
                        "repo": repo,
                        "default_branch": default_branch,
                        "decision": "stalled_unaddressed_reviews",
                        "throttled": False,
                        "throttle_reason": throttle_reason,
                        "elapsed_seconds": elapsed_seconds,
                        "due_probe_count": due_probe_count,
                        "approved_waiting_runs": approved_waiting_runs,
                        "stalled_prs": stalled_prs,
                        "eligible_count": len(stalled_prs),
                        "dispatched": True,
                        "availability_established": availability_established,
                        "availability_reason": availability_reason,
                    }
                )
            )
            return

        if throttled:
            approved_waiting_runs = auto_approve_waiting_runs(repo, token)
            print(f"::notice::ai-pr-loop-watchdog throttled ({throttle_reason})")
            output = {
                "repo": repo,
                "default_branch": default_branch,
                "decision": "throttled",
                "throttled": True,
                "throttle_reason": throttle_reason,
                "elapsed_seconds": elapsed_seconds,
                "due_probe_count": due_probe_count,
                "approved_waiting_runs": approved_waiting_runs,
                "eligible_count": None,
                "dispatched": False,
                "availability_established": availability_established,
                "availability_reason": availability_reason,
            }
            print(json.dumps(output))
            return

        eligible = provider.list_eligible_prs(max_prs=1)
        eligible_count = len(eligible)
        if eligible_count == 0:
            approved_waiting_runs = auto_approve_waiting_runs(repo, token)
            print("::notice::ai-pr-loop-watchdog no eligible scheduler PRs")
            output = {
                "repo": repo,
                "default_branch": default_branch,
                "decision": "no_eligible_prs",
                "throttled": False,
                "throttle_reason": throttle_reason,
                "elapsed_seconds": elapsed_seconds,
                "due_probe_count": due_probe_count,
                "approved_waiting_runs": approved_waiting_runs,
                "eligible_count": 0,
                "dispatched": False,
                "availability_established": availability_established,
                "availability_reason": availability_reason,
            }
            print(json.dumps(output))
            return

        _dispatch_throttler(repo, default_branch)
        approved_waiting_runs = auto_approve_waiting_runs(repo, token)
        print("::notice::ai-pr-loop-watchdog dispatched ai-pr-loop-throttler.yml")
        output = {
            "repo": repo,
            "default_branch": default_branch,
            "decision": "dispatched",
            "throttled": False,
            "throttle_reason": throttle_reason,
            "elapsed_seconds": elapsed_seconds,
            "due_probe_count": due_probe_count,
            "approved_waiting_runs": approved_waiting_runs,
            "eligible_count": eligible_count,
            "dispatched": True,
            "availability_established": availability_established,
            "availability_reason": availability_reason,
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
                    "due_probe_count": 0,
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
                    "due_probe_count": 0,
                }
            )
        )
    except Exception as exc:
        logger.exception("AI PR loop watchdog failed: %s", exc)
        sys.exit(1)
