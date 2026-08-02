"""Data models for the activity tracker.

ActivityEvent is a dataclass used throughout the tracker (hook, report, time_engine).
API response models are Pydantic BaseModel subclasses used by the dashboard server.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel


@dataclass
class BaseEvent:
    """Common fields for all activity events."""

    timestamp: str
    session_id: str
    cwd: str


@dataclass
class ContextEvent(BaseEvent):
    """Emitted once per session+cwd, captures project/branch/issue/epic context."""

    tool: str = "context"
    action: str = "detect"
    source: str = "auto"  # "auto" (detect_context) or "manual" (user-assigned)
    project_path: str = ""
    project_id: str = ""
    project_url: str = ""
    git_branch: str = ""
    mr_iid: str = ""
    mr_title: str = ""
    mr_url: str = ""
    mr_source_branch: str = ""
    mr_target_branch: str = ""
    mr_author: str = ""
    issue_iid: str = ""
    issue_title: str = ""
    issue_url: str = ""
    issue_labels: list[str] = field(default_factory=list)
    mr_labels: list[str] = field(default_factory=list)
    epic_iid: str = ""
    epic_title: str = ""
    epic_url: str = ""
    project_fallback_labels: list[str] = field(default_factory=list)


@dataclass
class GitEvent(BaseEvent):
    """Git command tracked by the hook (commit, push, checkout, etc.)."""

    tool: str = "git"
    action: str = ""
    command: str = ""
    ref: str = ""


@dataclass
class GlabEvent(BaseEvent):
    """glab CLI command tracked by the hook (issue/MR view, create, merge, etc.)."""

    tool: str = "glab"
    action: str = ""
    command: str = ""
    iid: str = ""


@dataclass
class FileEvent(BaseEvent):
    """File edit/write tracked by the hook."""

    tool: str = "file"
    action: str = "edit"
    file_path: str = ""


@dataclass
class SkillEvent(BaseEvent):
    """Skill invocation tracked by the hook."""

    tool: str = "skill"
    action: str = "invoke"
    skill: str = ""


@dataclass
class AgentEvent(BaseEvent):
    """Sub-agent launch tracked by the hook."""

    tool: str = "agent"
    action: str = "launch"
    description: str = ""
    subagent_type: str = ""


@dataclass
class ReadEvent(BaseEvent):
    """File read tracked by the hook."""

    tool: str = "read"
    action: str = "read"
    file_path: str = ""


@dataclass
class SessionEvent(BaseEvent):
    """Session lifecycle event (start/end)."""

    tool: str = "session"
    action: str = ""  # "start" or "end"


@dataclass
class ManualEvent(BaseEvent):
    """Manual time entry logged by the user."""

    tool: str = "manual"
    action: str = "log"
    duration_seconds: float = 0.0
    description: str = ""
    project_path: str = ""
    project_id: str = ""
    project_url: str = ""
    issue_iid: str = ""
    issue_title: str = ""
    issue_url: str = ""
    issue_labels: list[str] = field(default_factory=list)
    epic_iid: str = ""
    epic_title: str = ""
    epic_url: str = ""


ActivityEvent = (
    ContextEvent | GitEvent | GlabEvent | FileEvent | SkillEvent | AgentEvent | ReadEvent | SessionEvent | ManualEvent
)


def parse_event_json(data: dict[str, object]) -> ActivityEvent:
    """Reconstruct a typed ActivityEvent from a flat JSON dict (JSONL line)."""
    tool = str(data.get("tool", ""))
    base = {
        "timestamp": str(data.get("timestamp", "")),
        "session_id": str(data.get("session_id", "")),
        "cwd": str(data.get("cwd", "")),
    }

    if tool == "context":
        labels_raw = data.get("issue_labels", [])
        mr_labels_raw = data.get("mr_labels", [])
        return ContextEvent(
            **base,
            source=str(data.get("source", "auto")),
            project_path=str(data.get("project_path", "")),
            project_id=str(data.get("project_id", "")),
            project_url=str(data.get("project_url", "")),
            git_branch=str(data.get("git_branch", "")),
            mr_iid=str(data.get("mr_iid", "")),
            mr_title=str(data.get("mr_title", "")),
            mr_url=str(data.get("mr_url", "")),
            mr_source_branch=str(data.get("mr_source_branch", "")),
            mr_target_branch=str(data.get("mr_target_branch", "")),
            mr_author=str(data.get("mr_author", "")),
            issue_iid=str(data.get("issue_iid", "")),
            issue_title=str(data.get("issue_title", "")),
            issue_url=str(data.get("issue_url", "")),
            issue_labels=labels_raw if isinstance(labels_raw, list) else [],
            mr_labels=mr_labels_raw if isinstance(mr_labels_raw, list) else [],
            epic_iid=str(data.get("epic_iid", "")),
            epic_title=str(data.get("epic_title", "")),
            epic_url=str(data.get("epic_url", "")),
            project_fallback_labels=fb_raw if isinstance(fb_raw := data.get("project_fallback_labels"), list) else [],
        )

    if tool == "git":
        return GitEvent(
            **base,
            action=str(data.get("action", "")),
            command=str(data.get("command", "")),
            ref=str(data.get("ref", "")),
        )

    if tool == "glab":
        return GlabEvent(
            **base,
            action=str(data.get("action", "")),
            command=str(data.get("command", "")),
            iid=str(data.get("iid", "")),
        )

    if tool == "file":
        return FileEvent(**base, file_path=str(data.get("file_path", "")))

    if tool == "skill":
        return SkillEvent(**base, skill=str(data.get("skill", "")))

    if tool == "agent":
        return AgentEvent(
            **base,
            description=str(data.get("description", "")),
            subagent_type=str(data.get("subagent_type", "")),
        )

    if tool == "read":
        return ReadEvent(**base, file_path=str(data.get("file_path", "")))

    if tool == "session":
        return SessionEvent(**base, action=str(data.get("action", "")))

    if tool == "manual":
        labels_raw = data.get("issue_labels", [])
        return ManualEvent(
            **base,
            duration_seconds=float(str(data.get("duration_seconds", 0))),
            description=str(data.get("description", "")),
            project_path=str(data.get("project_path", "")),
            project_id=str(data.get("project_id", "")),
            project_url=str(data.get("project_url", "")),
            issue_iid=str(data.get("issue_iid", "")),
            issue_title=str(data.get("issue_title", "")),
            issue_url=str(data.get("issue_url", "")),
            issue_labels=labels_raw if isinstance(labels_raw, list) else [],
            epic_iid=str(data.get("epic_iid", "")),
            epic_title=str(data.get("epic_title", "")),
            epic_url=str(data.get("epic_url", "")),
        )

    # Fallback: treat unknown tools as git events with minimal data
    return GitEvent(**base, action=str(data.get("action", "")))


class GroupBy(StrEnum):
    SMART = "smart"
    ISSUE = "issue"
    EPIC = "epic"
    LABEL = "label"
    PROJECT = "project"
    SESSION = "session"


class ContextSnapshot(BaseModel):
    """Typed representation of a context event's details."""

    project_path: str = ""
    project_id: str = ""
    project_url: str = ""
    git_branch: str = ""
    mr_iid: str = ""
    mr_title: str = ""
    mr_url: str = ""
    mr_source_branch: str = ""
    mr_target_branch: str = ""
    mr_author: str = ""
    issue_iid: str = ""
    issue_title: str = ""
    issue_url: str = ""
    issue_labels: list[str] = []
    mr_labels: list[str] = []
    epic_iid: str = ""
    epic_title: str = ""
    epic_url: str = ""
    project_fallback_labels: list[str] = []


class TimeBlock(BaseModel):
    """A contiguous block of time attributed to a single context."""

    start: datetime
    end: datetime
    duration_seconds: float
    context: ContextSnapshot
    session_id: str


class GroupedTimeEntry(BaseModel):
    """One row in the dashboard: a scope key + aggregated time."""

    key: str
    label: str
    total_seconds: float
    total_hours: float
    percentage: float = 0.0
    detail_url: str = ""


class DashboardResponse(BaseModel):
    start_date: date
    end_date: date
    group_by: GroupBy
    total_seconds: float
    total_hours: float
    entries: list[GroupedTimeEntry]


class DayActivity(BaseModel):
    date: date
    total_seconds: float
    total_hours: float


class HeatmapResponse(BaseModel):
    start_date: date
    end_date: date
    days: list[DayActivity]


class FilterOption(BaseModel):
    """A selectable filter value with a machine key and a human label."""

    key: str
    label: str


class FilterValues(BaseModel):
    smart: list[FilterOption]
    issues: list[FilterOption]
    epics: list[FilterOption]
    labels: list[str]
    projects: list[str]


class TimelinePoint(BaseModel):
    """A single point in the work density timeline."""

    time: str  # ISO timestamp of the bucket start
    percentage: float  # work density: 100 = 1 session continuous, 200 = 2 overlapping, etc.


class TimelineSeries(BaseModel):
    """One series in the stacked timeline (one per group key)."""

    key: str
    label: str
    points: list[TimelinePoint]


class TimelineResponse(BaseModel):
    start_date: date
    end_date: date
    bucket_minutes: int
    times: list[str]  # shared time axis (ISO timestamps)
    series: list[TimelineSeries]


class ContextualizeRequest(BaseModel):
    """Request body for POST /api/contextualize."""

    session_id: str
    target_date: date | None = None
    project_path: str = ""
    project_id: str = ""
    project_url: str = ""
    issue_iid: str = ""
    issue_title: str = ""
    issue_url: str = ""
    issue_labels: list[str] = []
    epic_iid: str = ""
    epic_title: str = ""
    epic_url: str = ""


class SessionSummary(BaseModel):
    """Summary of a session for the sessions list endpoint."""

    session_id: str
    start: str
    end: str
    total_seconds: float
    total_hours: float
    cwd: str
    project_path: str
    issue_iid: str
    issue_title: str
    epic_iid: str
    epic_title: str
    context_source: str  # "auto", "manual", or "none"


class SessionsResponse(BaseModel):
    start_date: date
    end_date: date
    sessions: list[SessionSummary]


class GitLabIssueOption(BaseModel):
    """An open GitLab issue available for assignment."""

    iid: str
    title: str
    web_url: str
    labels: list[str]
    project_path: str
    project_id: str


class GitLabIssuesResponse(BaseModel):
    priority_issues: list[GitLabIssueOption]  # same project, workflow-labeled first
    other_issues: list[GitLabIssueOption]  # other projects


class DateRangeResponse(BaseModel):
    min_date: date | None
    max_date: date | None
