"""Generate activity report from daily log.

Reads the daily JSONL file (~/.claude/pysae-ai-tools/activity-log/{YYYY-MM-DD}.jsonl)
and outputs a structured JSON summary grouped by session and project.
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Annotated

import typer

from .hook import LOG_DIR
from .models import (
    ActivityEvent,
    FileEvent,
    GitEvent,
    GlabEvent,
    SkillEvent,
    parse_event_json,
)


@dataclass
class SessionSummary:
    session_id: str
    projects: set[str] = field(default_factory=set)
    git_actions: list[GitEvent] = field(default_factory=list)
    glab_actions: list[GlabEvent] = field(default_factory=list)
    files_edited: set[str] = field(default_factory=set)
    skills_used: list[str] = field(default_factory=list)
    first_event: str = ""
    last_event: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "time_range": {"start": self.first_event, "end": self.last_event},
            "projects": sorted(self.projects),
            "git_actions": [{"action": e.action, "command": e.command, "ref": e.ref} for e in self.git_actions],
            "glab_actions": [{"action": e.action, "command": e.command, "iid": e.iid} for e in self.glab_actions],
            "files_edited": sorted(self.files_edited),
            "skills_used": self.skills_used,
        }


def _load_events(target_date: date) -> dict[str, list[ActivityEvent]]:
    """Load all events from the daily log file, grouped by session_id."""
    sessions: dict[str, list[ActivityEvent]] = defaultdict(list)
    log_file = LOG_DIR / f"{target_date.isoformat()}.jsonl"
    if not log_file.exists():
        return sessions

    with open(log_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            event = parse_event_json(data)
            sessions[event.session_id].append(event)

    return sessions


def _summarize_session(session_id: str, events: list[ActivityEvent]) -> SessionSummary:
    """Summarize a session's events."""
    summary = SessionSummary(session_id=session_id)

    for event in sorted(events, key=lambda e: e.timestamp):
        if not summary.first_event:
            summary.first_event = event.timestamp
        summary.last_event = event.timestamp

        summary.projects.add(event.cwd)

        if isinstance(event, GitEvent):
            summary.git_actions.append(event)
        elif isinstance(event, GlabEvent):
            summary.glab_actions.append(event)
        elif isinstance(event, FileEvent):
            if event.file_path:
                summary.files_edited.add(event.file_path)
        elif isinstance(event, SkillEvent):
            if event.skill:
                summary.skills_used.append(event.skill)

    return summary


def generate_report(target_date: date) -> dict[str, object]:
    """Generate a structured report for a given date."""
    sessions = _load_events(target_date)
    summaries = [_summarize_session(sid, events) for sid, events in sessions.items()]
    summaries.sort(key=lambda s: s.first_event)

    total_events = sum(len(events) for events in sessions.values())
    all_projects: set[str] = set()
    all_issues: set[str] = set()
    all_mrs: set[str] = set()

    for _sid, events in sessions.items():
        for event in events:
            all_projects.add(event.cwd)
            if isinstance(event, GlabEvent) and event.iid:
                if "issue" in event.action:
                    all_issues.add(event.iid)
                elif "mr" in event.action:
                    all_mrs.add(event.iid)

    return {
        "date": target_date.isoformat(),
        "total_sessions": len(summaries),
        "total_events": total_events,
        "projects": sorted(all_projects),
        "issues_touched": sorted(all_issues),
        "mrs_touched": sorted(all_mrs),
        "sessions": [s.to_dict() for s in summaries],
    }


def report(
    day: Annotated[
        str,
        typer.Argument(help="Date au format YYYY-MM-DD (défaut: aujourd'hui)"),
    ] = "",
) -> None:
    """Generate an activity report for a given day (default: today)."""
    if day:
        target_date = date.fromisoformat(day)
    else:
        target_date = date.today()

    result = generate_report(target_date)
    print(json.dumps(result, indent=2, ensure_ascii=False))
