"""Inspect Hydra workflows and produce a Slack alert payload."""

from __future__ import annotations

import json
import logging
import os
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from zoneinfo import ZoneInfo

from airbyte_ops_mcp.slack_api import lookup_slack_usergroup

NOTICE_AFTER_MIN = 60
PAGE_AFTER_MIN = 120
RATE_THRESHOLD = 0.25
WINDOW_FALLBACK_H = 6
DAILY_AT_HOUR_PT = 9
HEARTBEAT_WEEKDAYS = {0}  # Monday
SELF_WORKFLOW_FILE = "cron-watchdog.yml"
ONCALL_HANDLE = "oc-hydra"

WATCHED = [
    (
        "airbytehq/airbyte-ops-mcp",
        "devin-reminders.yml",
        "Devin Reminders",
        120,
        frozenset({"schedule"}),
    ),
    (
        "airbytehq/airbyte-ops-mcp",
        "rollout-autopilot-cron.yml",
        "Rollout AutoPilot",
        120,
        frozenset({"schedule"}),
    ),
    (
        "airbytehq/ai-skills",
        "devin-knowledge-sync.yml",
        "Knowledge Sync",
        None,
        frozenset({"push", "schedule"}),
    ),
    (
        "airbytehq/airbyte-ops-mcp",
        SELF_WORKFLOW_FILE,
        "Cron Watchdog",
        120,
        frozenset({"schedule"}),
    ),
]

GITHUB_API = "https://api.github.com"
PACIFIC = ZoneInfo("America/Los_Angeles")
IGNORED_CONCLUSIONS = {"cancelled", "skipped"}
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class WatchedWorkflow:
    """Configuration for one workflow monitored by the watchdog."""

    repo: str
    workflow: str
    label: str
    stall_grace_min: int | None
    health_events: frozenset[str]


@dataclass(frozen=True)
class Run:
    """The health-relevant fields from a GitHub Actions run."""

    conclusion: str
    timestamp: datetime
    html_url: str
    event: str
    name: str

    @property
    def failed(self) -> bool:
        """Return whether this run represents a failed result."""
        return self.conclusion.lower() not in {"success", *IGNORED_CONCLUSIONS}


@dataclass
class WorkflowStatus:
    """Derived health information for one watched workflow."""

    config: WatchedWorkflow
    state: str
    runs: list[Run]
    fetched_run_count: int = 0
    unhealthy_since: datetime | None = None
    recovery_at: datetime | None = None
    recovery_duration: timedelta | None = None
    error: str | None = None

    @property
    def latest_run(self) -> Run | None:
        """Return the newest relevant run."""
        return self.runs[0] if self.runs else None

    def failure_rate(self, now: datetime) -> float:
        """Return the failed-run share among the last 24 hours of runs."""
        cutoff = now - timedelta(hours=24)
        recent = [run for run in self.runs if run.timestamp >= cutoff]
        if not recent:
            return 0.0
        return sum(run.failed for run in recent) / len(recent)

    @property
    def disabled(self) -> bool:
        """Return whether GitHub has disabled this workflow."""
        return self.state != "active"


@dataclass(frozen=True)
class WatchdogResult:
    """The alert payload and status report produced by one watchdog run."""

    should_post: bool
    ping_oncall: bool
    blocks: list[dict[str, Any]]
    fallback_text: str
    summary: str
    statuses: list[WorkflowStatus]


@dataclass(frozen=True)
class WatchdogHistory:
    """The previous watchdog run, and whether history could be read at all."""

    previous_start: datetime | None
    known: bool


def _parse_timestamp(value: str | None) -> datetime:
    if not value:
        raise ValueError("run has no timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _as_config(
    item: tuple[str, str, str, int | None, frozenset[str]],
) -> WatchedWorkflow:
    return WatchedWorkflow(*item)


def _self_config() -> WatchedWorkflow:
    """Return the watchdog's own entry in `WATCHED`."""
    for item in WATCHED:
        config = _as_config(item)
        if config.workflow == SELF_WORKFLOW_FILE:
            return config
    raise ValueError(f"`{SELF_WORKFLOW_FILE}` is missing from `WATCHED`")


def _parse_run(data: dict[str, Any]) -> Run | None:
    conclusion = data.get("conclusion")
    if not conclusion or conclusion.lower() in IGNORED_CONCLUSIONS:
        return None
    timestamp = (
        data.get("created_at") or data.get("run_started_at") or data.get("updated_at")
    )
    try:
        parsed_timestamp = _parse_timestamp(timestamp)
    except (TypeError, ValueError):
        return None
    return Run(
        conclusion=conclusion,
        timestamp=parsed_timestamp,
        html_url=data.get("html_url", ""),
        event=data.get("event", ""),
        name=data.get("name", ""),
    )


def _workflow_created_anchor(workflow_data: dict[str, Any], now: datetime) -> datetime:
    """Return the workflow's creation time, or `now` when it is unusable."""
    try:
        return _parse_timestamp(workflow_data.get("created_at"))
    except (AttributeError, TypeError, ValueError):
        return now


def _newest_health_relevant_anchor(
    runs_data: list[dict[str, Any]], health_events: frozenset[str]
) -> datetime | None:
    """Return the newest parseable timestamp from health-relevant runs."""
    anchors: list[datetime] = []
    for data in runs_data:
        if data.get("event") not in health_events:
            continue
        for field in ("created_at", "run_started_at", "updated_at"):
            timestamp = data.get(field)
            if not timestamp:
                continue
            try:
                anchors.append(_parse_timestamp(timestamp))
            except (AttributeError, TypeError, ValueError):
                continue
            break
    return max(anchors) if anchors else None


def derive_status(
    config: WatchedWorkflow,
    workflow_data: dict[str, Any],
    runs_data: list[dict[str, Any]],
    now: datetime,
    *,
    is_self: bool = False,
) -> WorkflowStatus:
    """Derive health and recovery information from GitHub API responses.

    Args:
        config: Workflow configuration.
        workflow_data: Response from the workflow metadata endpoint.
        runs_data: Response entries from the workflow runs endpoint.
        now: Current UTC timestamp used for stall detection.
        is_self: Whether this is the currently executing workflow.

    Returns:
        Derived workflow status.
    """
    runs = sorted(
        (
            run
            for data in runs_data
            if data.get("event") in config.health_events
            and (run := _parse_run(data)) is not None
        ),
        key=lambda run: run.timestamp,
        reverse=True,
    )
    status = WorkflowStatus(
        config=config,
        state=workflow_data.get("state", ""),
        runs=runs,
        fetched_run_count=len(runs_data),
    )
    if status.disabled:
        status.unhealthy_since = now
        return status
    if not runs:
        if not is_self:
            has_health_relevant_data = any(
                data.get("event") in config.health_events for data in runs_data
            )
            if has_health_relevant_data:
                status.unhealthy_since = _newest_health_relevant_anchor(
                    runs_data, config.health_events
                ) or _workflow_created_anchor(workflow_data, now)
            elif config.stall_grace_min is not None:
                status.unhealthy_since = _workflow_created_anchor(workflow_data, now)
        return status

    newest = runs[0]
    if newest.failed:
        oldest_failure = newest
        for run in runs[1:]:
            if not run.failed:
                break
            oldest_failure = run
        status.unhealthy_since = oldest_failure.timestamp
    elif len(runs) > 1 and runs[1].failed:
        oldest_failure = runs[1]
        for run in runs[2:]:
            if not run.failed:
                break
            oldest_failure = run
        status.recovery_at = newest.timestamp
        status.recovery_duration = newest.timestamp - oldest_failure.timestamp

    if config.stall_grace_min is not None and not is_self:
        last_run_age = now - newest.timestamp
        if last_run_age > timedelta(minutes=config.stall_grace_min):
            status.unhealthy_since = newest.timestamp + timedelta(
                minutes=config.stall_grace_min
            )
            status.recovery_at = None
            status.recovery_duration = None
    return status


def _within_window(
    timestamp: datetime | None, window_start: datetime, now: datetime
) -> bool:
    return timestamp is not None and window_start <= timestamp <= now


def _is_current_workflow(config: WatchedWorkflow) -> bool:
    """Return whether `config` matches the currently executing workflow."""
    workflow_ref = os.getenv("GITHUB_WORKFLOW_REF")
    if not workflow_ref:
        return False
    owner_repo, marker, workflow_and_ref = workflow_ref.partition("/.github/workflows/")
    workflow, separator, git_ref = workflow_and_ref.partition("@")
    if (
        not marker
        or not owner_repo
        or not workflow
        or not separator
        or not git_ref.startswith("refs/")
    ):
        return False
    return owner_repo == config.repo and workflow == config.workflow


def _format_duration(duration: timedelta | None) -> str:
    if duration is None:
        return "unknown duration"
    total_minutes = max(0, int(duration.total_seconds() // 60))
    days, remainder = divmod(total_minutes, 1440)
    hours, minutes = divmod(remainder, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes or not parts:
        parts.append(f"{minutes}m")
    return " ".join(parts)


def _is_first_daily_tick(
    now: datetime, previous_watchdog_start: datetime | None
) -> bool:
    local_now = now.astimezone(PACIFIC)
    if local_now.hour < DAILY_AT_HOUR_PT:
        return False
    if previous_watchdog_start is None:
        return True
    local_previous = previous_watchdog_start.astimezone(PACIFIC)
    return (
        local_previous.date() != local_now.date()
        or local_previous.hour < DAILY_AT_HOUR_PT
    )


def _oncall_mention(group_id: str | None) -> str:
    if group_id:
        return f"<!subteam^{group_id}|@oc-hydra>"
    return "@oc-hydra"


def _resolve_oncall_group_id() -> str | None:
    """Resolve the on-call usergroup ID for Slack mentions."""
    try:
        matches = lookup_slack_usergroup(ONCALL_HANDLE)
    except Exception as exc:
        logger.warning("Could not resolve Slack usergroup %s: %s", ONCALL_HANDLE, exc)
        return None
    exact_matches = [
        usergroup
        for usergroup in matches
        if usergroup.handle.casefold() == ONCALL_HANDLE.casefold()
    ]
    if len(exact_matches) != 1:
        logger.warning(
            "Expected exactly one Slack usergroup with handle %s, found %d",
            ONCALL_HANDLE,
            len(exact_matches),
        )
        return None
    return exact_matches[0].id


def _status_line(status: WorkflowStatus, now: datetime) -> str:
    latest = status.latest_run
    if status.disabled:
        condition = f"workflow disabled (`{status.state}`)"
    elif status.unhealthy_since is not None:
        condition = f"unhealthy for {_format_duration(now - status.unhealthy_since)}"
    else:
        condition = "healthy"
    latest_text = (
        f"no finished runs in the last {status.fetched_run_count} fetched runs"
    )
    if latest is not None:
        latest_text = f"{latest.conclusion} ({latest.event or 'unknown trigger'})"
        if latest.html_url:
            latest_text += f" — <{latest.html_url}|run>"
    trigger_note = ""
    if status.config.label == "Devin Reminders" and latest is not None:
        trigger_note = f"; trigger `{latest.event or 'unknown'}`"
    return (
        f"*{status.config.label}* (`{status.config.repo}`) — {condition}; "
        f"latest: {latest_text}{trigger_note}"
    )


def _make_blocks(
    lines: list[str],
    *,
    ping_oncall: bool,
    oncall_group_id: str | None,
) -> list[dict[str, Any]]:
    text = "\n".join(lines)
    if ping_oncall:
        text = f"{_oncall_mention(oncall_group_id)}\n{text}"
    return [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "Hydra cron watchdog"},
        },
        {"type": "section", "text": {"type": "mrkdwn", "text": text}},
    ]


def decide(
    statuses: list[WorkflowStatus],
    *,
    now: datetime,
    previous_watchdog_start: datetime | None,
    history_known: bool = True,
    oncall_group_id: str | None = None,
) -> WatchdogResult:
    """Apply the alert ladder and build one combined Slack payload.

    Args:
        statuses: Derived statuses for each watched workflow.
        now: Current UTC timestamp.
        previous_watchdog_start: Start timestamp of the prior watchdog run.
        history_known: Whether the previous watchdog run history was read
            successfully.
        oncall_group_id: Slack user-group ID, when configured.

    Returns:
        A `WatchdogResult` containing alert and summary outputs.
    """
    window_start = (
        previous_watchdog_start - timedelta(minutes=10)
        if previous_watchdog_start is not None
        else now - timedelta(hours=WINDOW_FALLBACK_H)
    )
    first_daily_tick = history_known and _is_first_daily_tick(
        now, previous_watchdog_start
    )
    daily_unhealthy = [
        status
        for status in statuses
        if status.disabled
        or (
            status.unhealthy_since is not None
            and now - status.unhealthy_since >= timedelta(minutes=NOTICE_AFTER_MIN)
        )
    ]
    high_rate = [
        status for status in statuses if status.failure_rate(now) > RATE_THRESHOLD
    ]
    lines: list[str] = []
    ping_oncall = False

    if first_daily_tick and (daily_unhealthy or high_rate):
        lines.append("📊 Daily health summary")
        ping_oncall = True
        if high_rate:
            labels = ", ".join(
                f"{status.config.label} ({status.failure_rate(now):.0%})"
                for status in high_rate
            )
            lines.append(f"24h failure rate over {RATE_THRESHOLD:.0%}: {labels}")
    elif first_daily_tick and now.astimezone(PACIFIC).weekday() in HEARTBEAT_WEEKDAYS:
        lines.append("✅ Monday heartbeat — watchdog alive")

    for status in statuses:
        if status.error:
            lines.append(f"⚠️ could not check *{status.config.label}*: {status.error}")
            continue
        if status.disabled:
            if first_daily_tick:
                lines.append(
                    f"🚨 *{status.config.label}* is disabled (`{status.state}`)"
                )
                ping_oncall = True
            continue
        elif status.recovery_at is not None:
            if (
                status.recovery_duration is not None
                and status.recovery_duration >= timedelta(minutes=NOTICE_AFTER_MIN)
                and _within_window(status.recovery_at, window_start, now)
            ):
                lines.append(
                    f"✅ *{status.config.label}* recovered after "
                    f"{_format_duration(status.recovery_duration)}"
                )
        elif status.unhealthy_since is not None:
            notice_at = status.unhealthy_since + timedelta(minutes=NOTICE_AFTER_MIN)
            page_at = status.unhealthy_since + timedelta(minutes=PAGE_AFTER_MIN)
            if _within_window(page_at, window_start, now):
                lines.append(
                    f"🚨 *{status.config.label}* has been unhealthy for "
                    f"{_format_duration(now - status.unhealthy_since)}"
                )
                ping_oncall = True
            elif _within_window(notice_at, window_start, now):
                lines.append(
                    f"⚠️ *{status.config.label}* has been unhealthy for "
                    f"{_format_duration(now - status.unhealthy_since)}"
                )

    heartbeat_only = (
        first_daily_tick
        and len(lines) == 1
        and lines[0].startswith("✅ Monday heartbeat")
    )
    if lines and not heartbeat_only:
        lines.extend(
            _status_line(status, now) for status in statuses if status.error is None
        )

    should_post = bool(lines)
    fallback_text = "\n".join(lines)
    if ping_oncall:
        fallback_text = f"{_oncall_mention(oncall_group_id)}\n{fallback_text}"
    blocks = _make_blocks(
        lines, ping_oncall=ping_oncall, oncall_group_id=oncall_group_id
    )
    summary_lines = [
        "## Hydra cron watchdog",
        "",
        "| Workflow | State | Latest conclusion | Unhealthy since | 24h failure rate |",
        "| --- | --- | --- | --- | --- |",
    ]
    for status in statuses:
        latest = status.latest_run.conclusion if status.latest_run else "none"
        unhealthy_since = (
            status.unhealthy_since.isoformat() if status.unhealthy_since else "—"
        )
        summary_lines.append(
            f"| {status.config.label} | {status.state or 'unknown'} | {latest} | "
            f"{unhealthy_since} | {status.failure_rate(now):.0%} |"
        )
        if status.error:
            summary_lines.append(f"| ⚠️ Error: {status.error} | | | | |")
    return WatchdogResult(
        should_post=should_post,
        ping_oncall=ping_oncall,
        blocks=blocks,
        fallback_text=fallback_text,
        summary="\n".join(summary_lines) + "\n",
        statuses=statuses,
    )


def github_json(
    url: str,
    token: str,
    *,
    opener: Callable[..., Any] = urlopen,
) -> dict[str, Any]:
    """Fetch a JSON object from GitHub's REST API."""
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "airbyte-hydra-cron-watchdog",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with opener(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"GitHub API request failed: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"GitHub API returned unexpected data for {url}")
    return payload


def collect_statuses(
    token: str,
    *,
    now: datetime,
    fetch: Callable[[str, str], dict[str, Any]] = github_json,
) -> list[WorkflowStatus]:
    """Fetch and derive statuses, retaining individual API errors."""
    statuses: list[WorkflowStatus] = []
    for item in WATCHED:
        config = _as_config(item)
        base = f"{GITHUB_API}/repos/{config.repo}/actions/workflows/{config.workflow}"
        try:
            workflow_data = fetch(base, token)
            runs_response = fetch(f"{base}/runs?per_page=100", token)
            runs_data = runs_response.get("workflow_runs", [])
            if not isinstance(runs_data, list):
                raise RuntimeError("workflow runs response was not a list")
            statuses.append(
                derive_status(
                    config,
                    workflow_data,
                    runs_data,
                    now,
                    is_self=_is_current_workflow(config),
                )
            )
        except Exception as exc:
            statuses.append(
                WorkflowStatus(config=config, state="", runs=[], error=str(exc))
            )
    return statuses


def _previous_watchdog_start(
    token: str, *, now: datetime, fetch: Callable[[str, str], dict[str, Any]]
) -> WatchdogHistory:
    """Read the previous scheduled watchdog run, if history is available.

    Args:
        token: GitHub API token.
        now: Current UTC timestamp used to exclude future runs.
        fetch: GitHub JSON fetcher.

    Returns:
        Watchdog history, including whether the API response was readable.
    """
    config = _self_config()
    url = (
        f"{GITHUB_API}/repos/{config.repo}/actions/workflows/"
        f"{config.workflow}/runs?per_page=10"
    )
    try:
        data = fetch(url, token)
        current_id = os.getenv("GITHUB_RUN_ID")
        candidates = data.get("workflow_runs", [])
        for candidate in candidates:
            if str(candidate.get("id")) == current_id:
                continue
            # Only scheduled runs are delivery-eligible.
            if candidate.get("event") != "schedule":
                continue
            timestamp = candidate.get("run_started_at") or candidate.get("created_at")
            if not timestamp:
                continue
            try:
                parsed = _parse_timestamp(timestamp)
            except (AttributeError, TypeError, ValueError):
                continue
            if parsed <= now:
                return WatchdogHistory(parsed, known=True)
    except Exception as exc:
        logger.warning("Could not read previous watchdog history: %s", exc)
        return WatchdogHistory(None, known=False)
    return WatchdogHistory(None, known=True)


def _write_github_output(result: WatchdogResult) -> None:
    output_name = os.getenv("GITHUB_OUTPUT")
    if not output_name:
        return
    path = Path(output_name)
    existing = path.read_text() if path.exists() else ""
    delimiter = f"EOF_{uuid.uuid4().hex}"
    output = (
        f"should_post={'true' if result.should_post else 'false'}\n"
        f"blocks_json={json.dumps(result.blocks, separators=(',', ':'))}\n"
        f"fallback_text<<{delimiter}\n"
        f"{result.fallback_text}\n"
        f"{delimiter}\n"
    )
    path.write_text(existing + output)


def _write_summary(summary: str) -> None:
    summary_name = os.getenv("GITHUB_STEP_SUMMARY")
    if not summary_name:
        return
    path = Path(summary_name)
    existing = path.read_text() if path.exists() else ""
    path.write_text(existing + summary)


def run_watchdog(
    *,
    now: datetime | None = None,
    token: str | None = None,
    fetch: Callable[[str, str], dict[str, Any]] = github_json,
) -> WatchdogResult:
    """Run the watchdog and write GitHub Actions outputs."""
    current = now or datetime.now(timezone.utc)
    github_token = token or os.getenv("GITHUB_TOKEN", "")
    if not github_token:
        raise RuntimeError("GITHUB_TOKEN is required")
    history = _previous_watchdog_start(github_token, now=current, fetch=fetch)
    statuses = collect_statuses(github_token, now=current, fetch=fetch)
    result = decide(
        statuses,
        now=current,
        previous_watchdog_start=history.previous_start,
        history_known=history.known,
    )
    dry_run = os.getenv("DRY_RUN", "").lower() == "true"
    oncall_group_id = None
    if dry_run or result.ping_oncall:
        oncall_group_id = _resolve_oncall_group_id()
        if dry_run:
            if oncall_group_id is None:
                logger.info(
                    "Dry-run Slack usergroup lookup unresolved for %s; "
                    "using plain-text fallback",
                    ONCALL_HANDLE,
                )
            else:
                logger.info(
                    "Dry-run Slack usergroup lookup resolved %s to %s",
                    ONCALL_HANDLE,
                    oncall_group_id,
                )
    if result.ping_oncall and oncall_group_id is not None:
        result = decide(
            statuses,
            now=current,
            previous_watchdog_start=history.previous_start,
            history_known=history.known,
            oncall_group_id=oncall_group_id,
        )
    _write_github_output(result)
    _write_summary(result.summary)
    if dry_run:
        print(json.dumps({"blocks": result.blocks, "text": result.fallback_text}))
    return result


def main() -> int:
    """Run the watchdog CLI entrypoint."""
    try:
        result = run_watchdog()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if all(status.error for status in result.statuses):
        print("All watched workflow checks failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
