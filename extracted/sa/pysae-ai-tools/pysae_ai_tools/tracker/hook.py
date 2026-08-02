"""PostToolUse hook handler — extracts activity events and appends to daily log.

Called by Claude Code after each tool use. Reads JSON from stdin, extracts
relevant activity (git, glab, file edits, skill invocations), and stores
in the XDG data dir under activity-log/{YYYY-MM-DD}.jsonl.

On the first event of a session (or when cwd changes), runs detect_context --cached
to capture project/branch context and stores it as a "context" event.
"""

import json
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path

from ..common.project_config import ProjectConfigError, load_project_config
from ..config import DATA_DIR
from .models import (
    ActivityEvent,
    AgentEvent,
    ContextEvent,
    FileEvent,
    GitEvent,
    GlabEvent,
    ManualEvent,
    ReadEvent,
    SessionEvent,
    SkillEvent,
)

LOG_DIR = DATA_DIR / "activity-log"

# Historical location, under Claude's own dir before the XDG move.
_LEGACY_LOG_DIR = Path.home() / ".claude" / "pysae-ai-tools" / "activity-log"


def migrate_legacy() -> None:
    """Relocate the activity log from ``~/.claude`` to the XDG data dir, once. Best-effort."""
    try:
        if _LEGACY_LOG_DIR.is_dir() and not LOG_DIR.exists():
            LOG_DIR.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(_LEGACY_LOG_DIR), str(LOG_DIR))
    except OSError:
        pass


# Fields from detect_context that are too heavy or irrelevant for activity tracking
_CONTEXT_EXCLUDED_FIELDS: set[str] = {
    "issue_description",
    "epic_description",
    "mr_description",
    "tech_slack_channel",
    "tech_slack_channel_id",
    "public_slack_channel",
    "public_slack_channel_id",
    "detection_sources",
    "warnings",
    "git_sha",
    "git_prod_version",
    "is_ci",
    "default_branch",
}

# Patterns that indicate interesting glab activity
_GLAB_PATTERNS: dict[str, re.Pattern[str]] = {
    "issue_view": re.compile(r"glab\s+(?:api\s+)?.*issues?[/ ](\d+)"),
    "mr_view": re.compile(r"glab\s+(?:api\s+)?.*merge.requests?[/ ](\d+)"),
    "issue_list": re.compile(r"glab\s+issue\s+list"),
    "mr_list": re.compile(r"glab\s+mr\s+list"),
    "issue_create": re.compile(r"glab\s+issue\s+create"),
    "mr_create": re.compile(r"glab\s+mr\s+create"),
    "mr_merge": re.compile(r"glab\s+mr\s+merge"),
    "mr_approve": re.compile(r"glab\s+mr\s+approve"),
}

# Git patterns
_GIT_PATTERNS: dict[str, re.Pattern[str]] = {
    "commit": re.compile(r"git\s+commit"),
    "push": re.compile(r"git\s+push"),
    "checkout": re.compile(r"git\s+(?:checkout|switch)\s+(\S+)"),
    "merge": re.compile(r"git\s+merge"),
    "rebase": re.compile(r"git\s+rebase"),
    "tag": re.compile(r"git\s+tag"),
}


def _today_log_path() -> Path:
    """Return the log file path for today."""
    return LOG_DIR / f"{date.today().isoformat()}.jsonl"


def _get_known_cwds(session_id: str, log_file: Path) -> set[str]:
    """Read the daily log and return cwds that already have a context event for this session."""
    if not log_file.exists():
        return set()
    cwds: set[str] = set()
    with open(log_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if data.get("tool") == "context" and data.get("session_id") == session_id:
                cwds.add(data.get("cwd", ""))
    return cwds


def _detect_context_cached(cwd: str) -> dict[str, str | list[str]] | None:
    """Run detect_context --cached and return the parsed JSON output.

    Returns None if detect_context fails or returns no data.
    """
    try:
        result = subprocess.run(
            ["pysae-ai-tools", "internal", "detect-context", "--cached"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            cwd=cwd,
        )
        if result.returncode == 0 and result.stdout.strip():
            data: dict[str, object] = json.loads(result.stdout)
            filtered: dict[str, str | list[str]] = {}
            for k, v in data.items():
                if not v or k in _CONTEXT_EXCLUDED_FIELDS:
                    continue
                if isinstance(v, list):
                    filtered[k] = [str(item) for item in v]
                elif isinstance(v, (str, int, float, bool)):
                    filtered[k] = str(v)
            return filtered if filtered else None
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        pass
    return None


def _build_context_event(
    session_id: str, cwd: str, timestamp: str, ctx_data: dict[str, str | list[str]]
) -> ContextEvent:
    """Build a ContextEvent from detect_context output."""

    def _str(key: str) -> str:
        v = ctx_data.get(key, "")
        return str(v) if not isinstance(v, list) else ""

    def _list(key: str) -> list[str]:
        v = ctx_data.get(key, [])
        return v if isinstance(v, list) else []

    # Domain labels are stable config (no longer carried by detect-context). Resolve them
    # here, at capture time, from the repo's local .pysae-ai-tools.yaml. There is no
    # hardcoded fallback: an absent or malformed config simply yields no labels.
    try:
        local_cfg = load_project_config(Path(cwd))
    except ProjectConfigError:
        local_cfg = None
    fallback_labels = list(local_cfg.project.labels) if local_cfg is not None else []

    return ContextEvent(
        timestamp=timestamp,
        session_id=session_id,
        cwd=cwd,
        project_path=_str("project_path"),
        project_id=_str("project_id"),
        project_url=_str("project_url"),
        git_branch=_str("git_branch"),
        mr_iid=_str("mr_iid"),
        mr_title=_str("mr_title"),
        mr_url=_str("mr_url"),
        mr_source_branch=_str("mr_source_branch"),
        mr_target_branch=_str("mr_target_branch"),
        mr_author=_str("mr_author"),
        issue_iid=_str("issue_iid"),
        issue_title=_str("issue_title"),
        issue_url=_str("issue_url"),
        issue_labels=_list("issue_labels"),
        mr_labels=_list("mr_labels"),
        epic_iid=_str("epic_iid"),
        epic_title=_str("epic_title"),
        epic_url=_str("epic_url"),
        project_fallback_labels=fallback_labels,
    )


def _maybe_emit_context(session_id: str, cwd: str, timestamp: str, log_file: Path) -> ContextEvent | None:
    """Emit a context event if this cwd hasn't been seen in this session yet."""
    known = _get_known_cwds(session_id, log_file)
    if cwd in known:
        return None
    ctx_data = _detect_context_cached(cwd)
    if not ctx_data:
        return None
    return _build_context_event(session_id, cwd, timestamp, ctx_data)


def _session_exists(session_id: str, log_file: Path) -> bool:
    """Check if any event for this session_id already exists in today's log."""
    if not log_file.exists():
        return False
    with open(log_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if data.get("session_id") == session_id:
                return True
    return False


def _maybe_emit_session_start(session_id: str, cwd: str, timestamp: str, log_file: Path) -> SessionEvent | None:
    """Emit a session start event if this is the first event of the session."""
    if _session_exists(session_id, log_file):
        return None
    return SessionEvent(timestamp=timestamp, session_id=session_id, cwd=cwd, action="start")


def _extract_bash_events(command: str, session_id: str, cwd: str, timestamp: str) -> list[ActivityEvent]:
    """Extract activity events from a Bash command string."""
    events: list[ActivityEvent] = []

    for action, pattern in _GLAB_PATTERNS.items():
        m = pattern.search(command)
        if m:
            events.append(
                GlabEvent(
                    timestamp=timestamp,
                    session_id=session_id,
                    cwd=cwd,
                    action=action,
                    command=command.strip()[:200],
                    iid=m.group(1) if m.lastindex else "",
                )
            )

    for action, pattern in _GIT_PATTERNS.items():
        m = pattern.search(command)
        if m:
            events.append(
                GitEvent(
                    timestamp=timestamp,
                    session_id=session_id,
                    cwd=cwd,
                    action=action,
                    command=command.strip()[:200],
                    ref=m.group(1) if m.lastindex else "",
                )
            )

    return events


def parse_hook_event(payload: dict[str, object]) -> list[ActivityEvent]:
    """Parse a PostToolUse hook payload and return relevant activity events."""
    session_id = str(payload.get("session_id", ""))
    cwd = str(payload.get("cwd", ""))
    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        tool_input = {}

    now = datetime.now(timezone.utc).isoformat()

    if tool_name == "Bash":
        command = str(tool_input.get("command", ""))
        return _extract_bash_events(command, session_id, cwd, now)

    if tool_name in ("Edit", "Write"):
        return [
            FileEvent(
                timestamp=now,
                session_id=session_id,
                cwd=cwd,
                file_path=str(tool_input.get("file_path", "")),
            )
        ]

    if tool_name == "Skill":
        return [
            SkillEvent(
                timestamp=now,
                session_id=session_id,
                cwd=cwd,
                skill=str(tool_input.get("skill", "")),
            )
        ]

    if tool_name == "Agent":
        return [
            AgentEvent(
                timestamp=now,
                session_id=session_id,
                cwd=cwd,
                description=str(tool_input.get("description", "")),
                subagent_type=str(tool_input.get("subagent_type", "")),
            )
        ]

    if tool_name == "Read":
        return [
            ReadEvent(
                timestamp=now,
                session_id=session_id,
                cwd=cwd,
                file_path=str(tool_input.get("file_path", "")),
            )
        ]

    return []


def append_events(events: Sequence[ActivityEvent], log_file: Path) -> None:
    """Append activity events to the daily log file."""
    if not events:
        return
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a") as f:
        for event in events:
            f.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")


def hook() -> None:
    """PostToolUse hook handler — reads JSON from stdin, logs activity events."""
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return

    session_id = str(payload.get("session_id", "unknown"))
    cwd = str(payload.get("cwd", ""))
    now = datetime.now(timezone.utc).isoformat()
    log_file = _today_log_path()

    # Emit session start on first event of this session
    session_start = _maybe_emit_session_start(session_id, cwd, now, log_file)
    if session_start:
        append_events([session_start], log_file)

    # Emit context event on first encounter of this cwd in the session
    context_event = _maybe_emit_context(session_id, cwd, now, log_file)
    if context_event:
        append_events([context_event], log_file)

    # Extract and log activity events
    events = parse_hook_event(payload)
    append_events(events, log_file)


def stop_hook() -> None:
    """Stop hook handler — emits a session end event."""
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return

    session_id = str(payload.get("session_id", "unknown"))
    cwd = str(payload.get("cwd", ""))
    now = datetime.now(timezone.utc).isoformat()
    log_file = _today_log_path()

    event = SessionEvent(timestamp=now, session_id=session_id, cwd=cwd, action="end")
    append_events([event], log_file)


def log_context_manual(
    session_id: str,
    project_path: str = "",
    project_id: str = "",
    project_url: str = "",
    issue_iid: str = "",
    issue_title: str = "",
    issue_url: str = "",
    issue_labels: list[str] | None = None,
    epic_iid: str = "",
    epic_title: str = "",
    epic_url: str = "",
    target_date: date | None = None,
) -> str:
    """Insert a manual ContextEvent for a session.

    Scans log files to find the session if target_date is not provided.
    The event is timestamped just before the session's first event so
    the time engine uses it as the initial context for the entire session.
    Returns a status message.
    """
    # Find the log file containing the session
    if target_date:
        log_file = LOG_DIR / f"{target_date.isoformat()}.jsonl"
        if not log_file.exists():
            return f"ERROR: no log file for {target_date}"
    else:
        found = _find_session_log(session_id)
        if not found:
            return f"ERROR: session {session_id} not found in any log file"
        log_file = found

    # Find the session's first event timestamp and cwd
    first_ts, first_cwd = _find_session_start(session_id, log_file)
    if not first_ts:
        return f"ERROR: no events for session {session_id} in {log_file.name}"

    event = ContextEvent(
        timestamp=first_ts,
        session_id=session_id,
        cwd=first_cwd,
        source="manual",
        project_path=project_path,
        project_id=project_id,
        project_url=project_url,
        issue_iid=issue_iid,
        issue_title=issue_title,
        issue_url=issue_url,
        issue_labels=issue_labels or [],
        epic_iid=epic_iid,
        epic_title=epic_title,
        epic_url=epic_url,
    )
    append_events([event], log_file)

    parts = [f"session {session_id[:8]}…"]
    if issue_iid:
        parts.append(f"issue #{issue_iid}")
    if epic_iid:
        parts.append(f"epic #{epic_iid}")
    if project_path:
        parts.append(project_path)
    return f"CONTEXT: {' — '.join(parts)}"


def _find_session_log(session_id: str) -> Path | None:
    """Find the most recent log file containing events for the given session."""
    if not LOG_DIR.exists():
        return None
    for log_file in sorted(LOG_DIR.glob("*.jsonl"), reverse=True):
        with open(log_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if data.get("session_id") == session_id:
                    return log_file
    return None


def _find_session_start(session_id: str, log_file: Path) -> tuple[str, str]:
    """Find the timestamp and cwd of the first non-context event in a session."""
    first_ts = ""
    first_cwd = ""
    with open(log_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            if data.get("session_id") == session_id and data.get("tool") != "context":
                ts = str(data.get("timestamp", ""))
                if not first_ts or ts < first_ts:
                    first_ts = ts
                    first_cwd = str(data.get("cwd", ""))
    return first_ts, first_cwd


def log_manual(
    duration_seconds: float,
    description: str = "",
    project_path: str = "",
    project_id: str = "",
    project_url: str = "",
    issue_iid: str = "",
    issue_title: str = "",
    issue_url: str = "",
    issue_labels: list[str] | None = None,
    epic_iid: str = "",
    epic_title: str = "",
    epic_url: str = "",
    target_date: date | None = None,
) -> None:
    """Log a manual time entry to the activity log.

    If target_date is provided, writes to that day's log file instead of today's.
    """
    log_file = LOG_DIR / f"{(target_date or date.today()).isoformat()}.jsonl"
    now = datetime.now(timezone.utc).isoformat()

    event = ManualEvent(
        timestamp=now,
        session_id="manual",
        cwd="",
        duration_seconds=duration_seconds,
        description=description,
        project_path=project_path,
        project_id=project_id,
        project_url=project_url,
        issue_iid=issue_iid,
        issue_title=issue_title,
        issue_url=issue_url,
        issue_labels=issue_labels or [],
        epic_iid=epic_iid,
        epic_title=epic_title,
        epic_url=epic_url,
    )
    append_events([event], log_file)
    hours = duration_seconds / 3600
    parts = [f"{hours:.1f}h"]
    if description:
        parts.append(f"« {description} »")
    if issue_iid:
        parts.append(f"issue #{issue_iid}")
    if epic_iid:
        parts.append(f"epic #{epic_iid}")
    if project_path:
        parts.append(project_path)
    print(f"MANUAL: {' — '.join(parts)}")
