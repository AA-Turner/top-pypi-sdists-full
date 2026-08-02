"""Time calculation engine for activity tracking.

Reads daily JSONL logs, builds a timeline per session, and computes
time blocks attributed to each context (project/issue/epic).

Time between consecutive events in a session is attributed to the active context.
Gaps exceeding MAX_GAP are considered idle and discarded.
"""

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from .hook import LOG_DIR
from .models import (
    ActivityEvent,
    ContextEvent,
    ContextSnapshot,
    DayActivity,
    FilterOption,
    FilterValues,
    GroupBy,
    GroupedTimeEntry,
    ManualEvent,
    SessionSummary,
    TimeBlock,
    TimelinePoint,
    TimelineSeries,
    parse_event_json,
)

DEFAULT_MAX_GAP_MINUTES = 5

# Root group to strip from displayed project paths (keeps sub-groups visible)
_ROOT_GROUP_PREFIX = "pysae/"


def _short_project_path(path: str) -> str:
    """Strip the root group prefix from a project path, keeping sub-groups.

    Example: ``pysae/shift/app`` → ``shift/app``, ``pysae/api`` → ``api``.
    """
    if path.startswith(_ROOT_GROUP_PREFIX):
        return path[len(_ROOT_GROUP_PREFIX) :]
    return path


# Labels to exclude from grouping and filter options (CI/automation noise)
_IGNORED_LABELS: set[str] = {"augmented"}

# Labels used for smart categorization (order = priority)
_CATEGORY_LABELS: list[str] = [
    "Support 📞",
    "Infra",
    "Security",
    "API",
    "Driver",
    "Op",
    "Editor",
    "Info",
    "Screen",
    "Scheduling",
    "Tooling",
    "CI",
    "Maintenance 🧹",
    "Evolution 💡",
    "Optimization",
    "Test",
]


def _load_events(start_date: date, end_date: date) -> list[ActivityEvent]:
    """Load all events from daily log files in the given date range."""
    events: list[ActivityEvent] = []
    current = start_date
    while current <= end_date:
        log_file = LOG_DIR / f"{current.isoformat()}.jsonl"
        if log_file.exists():
            with open(log_file) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    events.append(parse_event_json(data))
        current += timedelta(days=1)
    return events


def _context_snapshot_from_event(event: ContextEvent) -> ContextSnapshot:
    """Build a ContextSnapshot from a ContextEvent."""
    return ContextSnapshot(
        project_path=event.project_path,
        project_id=event.project_id,
        project_url=event.project_url,
        git_branch=event.git_branch,
        mr_iid=event.mr_iid,
        mr_title=event.mr_title,
        mr_url=event.mr_url,
        mr_source_branch=event.mr_source_branch,
        mr_target_branch=event.mr_target_branch,
        mr_author=event.mr_author,
        issue_iid=event.issue_iid,
        issue_title=event.issue_title,
        issue_url=event.issue_url,
        issue_labels=event.issue_labels,
        mr_labels=event.mr_labels,
        epic_iid=event.epic_iid,
        epic_title=event.epic_title,
        epic_url=event.epic_url,
        project_fallback_labels=event.project_fallback_labels,
    )


def _context_snapshot_from_manual(event: ManualEvent) -> ContextSnapshot:
    """Build a ContextSnapshot from a ManualEvent's embedded context."""
    return ContextSnapshot(
        project_path=event.project_path,
        project_id=event.project_id,
        project_url=event.project_url,
        issue_iid=event.issue_iid,
        issue_title=event.issue_title,
        issue_url=event.issue_url,
        issue_labels=event.issue_labels,
        epic_iid=event.epic_iid,
        epic_title=event.epic_title,
        epic_url=event.epic_url,
    )


def compute_time_blocks(
    start_date: date,
    end_date: date,
    max_gap_minutes: int = DEFAULT_MAX_GAP_MINUTES,
) -> list[TimeBlock]:
    """Compute time blocks from activity logs.

    For each session, walks events chronologically. Time between consecutive
    events is attributed to the active context. Gaps > max_gap are discarded.
    """
    events = _load_events(start_date, end_date)
    max_gap = timedelta(minutes=max_gap_minutes)

    # Group by session
    sessions: dict[str, list[ActivityEvent]] = defaultdict(list)
    for event in events:
        sessions[event.session_id].append(event)

    blocks: list[TimeBlock] = []

    for session_id, session_events in sessions.items():
        session_events.sort(key=lambda e: e.timestamp)

        # Manual context serves as fallback for periods without issue
        manual_ctx_event = next(
            (e for e in session_events if isinstance(e, ContextEvent) and e.source == "manual"),
            None,
        )
        manual_fallback = _context_snapshot_from_event(manual_ctx_event) if manual_ctx_event else None
        current_context = manual_fallback or ContextSnapshot()

        for i in range(len(session_events) - 1):
            event = session_events[i]
            next_event = session_events[i + 1]

            # Update context when we see a context event
            if isinstance(event, ContextEvent):
                if event.source == "manual":
                    pass  # already handled as fallback
                else:
                    auto_ctx = _context_snapshot_from_event(event)
                    # Use auto context if it has issue info, otherwise use manual fallback
                    if auto_ctx.issue_iid or not manual_fallback:
                        current_context = auto_ctx
                    else:
                        current_context = manual_fallback
                continue

            # Manual events carry their own duration and context
            if isinstance(event, ManualEvent):
                try:
                    t_start = datetime.fromisoformat(event.timestamp)
                except ValueError:
                    continue
                duration = event.duration_seconds
                if duration <= 0:
                    continue
                blocks.append(
                    TimeBlock(
                        start=t_start,
                        end=t_start + timedelta(seconds=duration),
                        duration_seconds=duration,
                        context=_context_snapshot_from_manual(event),
                        session_id=session_id,
                    )
                )
                continue

            try:
                t_start = datetime.fromisoformat(event.timestamp)
                t_end = datetime.fromisoformat(next_event.timestamp)
            except ValueError:
                continue

            gap = t_end - t_start
            if gap > max_gap or gap.total_seconds() <= 0:
                continue

            blocks.append(
                TimeBlock(
                    start=t_start,
                    end=t_end,
                    duration_seconds=gap.total_seconds(),
                    context=current_context,
                    session_id=session_id,
                )
            )

    # Handle ManualEvent as last event in a session (not covered by the loop)
    for session_id, session_events in sessions.items():
        if not session_events:
            continue
        last = session_events[-1]
        if isinstance(last, ManualEvent) and last.duration_seconds > 0:
            try:
                t_start = datetime.fromisoformat(last.timestamp)
            except ValueError:
                continue
            blocks.append(
                TimeBlock(
                    start=t_start,
                    end=t_start + timedelta(seconds=last.duration_seconds),
                    duration_seconds=last.duration_seconds,
                    context=_context_snapshot_from_manual(last),
                    session_id=session_id,
                )
            )

    return blocks


def _group_key(ctx: ContextSnapshot, group_by: GroupBy) -> list[tuple[str, str, str]]:
    """Extract (key, label, url) tuples for the given grouping scope.

    Returns a list because label grouping fans out (one block per label).
    """
    if group_by == GroupBy.SMART:
        # 1. Epic if available
        if ctx.epic_iid:
            key = f"epic-{ctx.epic_iid}"
            label = ctx.epic_title or f"Epic #{ctx.epic_iid}"
            return [(key, label, ctx.epic_url)]
        # 2. Category label from issue/MR (first match by priority)
        all_labels = set(ctx.issue_labels + ctx.mr_labels)
        for cat in _CATEGORY_LABELS:
            if cat in all_labels:
                return [(f"cat-{cat}", cat, "")]
        # 3. Project fallback labels — the snapshot's stored labels (resolved from the
        #    repo's config at capture time; empty for a repo without a config).
        if ctx.project_fallback_labels:
            cat = ctx.project_fallback_labels[0]
            return [(f"cat-{cat}", cat, "")]
        # 4. Project short name as last resort
        if ctx.project_path:
            short = _short_project_path(ctx.project_path)
            return [(f"proj-{ctx.project_path}", short, ctx.project_url)]
        return [("(other)", "(autre)", "")]

    if group_by == GroupBy.ISSUE:
        if ctx.issue_iid and ctx.project_path:
            key = f"{ctx.project_path}#{ctx.issue_iid}"
            label = f"#{ctx.issue_iid} {ctx.issue_title}" if ctx.issue_title else key
            return [(key, label, ctx.issue_url)]
        return [("(no issue)", "(no issue)", "")]

    if group_by == GroupBy.EPIC:
        if ctx.epic_iid:
            key = f"epic-{ctx.epic_iid}"
            label = ctx.epic_title or f"Epic #{ctx.epic_iid}"
            return [(key, label, ctx.epic_url)]
        return [("(no epic)", "(no epic)", "")]

    if group_by == GroupBy.LABEL:
        all_labels = set(ctx.issue_labels + ctx.mr_labels) - _IGNORED_LABELS
        if all_labels:
            return [(lbl, lbl, "") for lbl in sorted(all_labels)]
        return [("(no label)", "(no label)", "")]

    if group_by == GroupBy.PROJECT:
        if ctx.project_path:
            return [(ctx.project_path, _short_project_path(ctx.project_path), ctx.project_url)]
        return [("(unknown project)", "(unknown project)", "")]

    return [("(unknown)", "(unknown)", "")]


@dataclass
class _Aggregation:
    label: str
    url: str
    seconds: float


def _group_blocks_by_session(blocks: list[TimeBlock]) -> list[GroupedTimeEntry]:
    """Group time blocks by session_id, with label showing cwd and date range."""

    @dataclass
    class _SessionAgg:
        cwd: str
        seconds: float
        start: datetime
        end: datetime

    aggregated: dict[str, _SessionAgg] = {}
    for block in blocks:
        sid = block.session_id
        if sid not in aggregated:
            aggregated[sid] = _SessionAgg(
                cwd=block.context.project_path or "(unknown)",
                seconds=0.0,
                start=block.start,
                end=block.end,
            )
        agg = aggregated[sid]
        agg.seconds += block.duration_seconds
        if block.start < agg.start:
            agg.start = block.start
        if block.end > agg.end:
            agg.end = block.end

    # Detect if sessions span multiple days
    all_dates = {agg.start.date() for agg in aggregated.values()}
    multi_day = len(all_dates) > 1

    result = []
    for key, agg in aggregated.items():
        start_str = agg.start.strftime("%H:%M")
        end_str = agg.end.strftime("%H:%M")
        short_name = _short_project_path(agg.cwd)
        date_prefix = f"{agg.start.strftime('%m-%d')} " if multi_day else ""
        label = f"{short_name} [{date_prefix}{start_str}\u2013{end_str}]"
        result.append(
            GroupedTimeEntry(
                key=key,
                label=label,
                total_seconds=agg.seconds,
                total_hours=round(agg.seconds / 3600, 2),
            )
        )
    result.sort(key=lambda e: e.total_seconds, reverse=True)
    return result


def group_blocks(
    blocks: list[TimeBlock],
    group_by: GroupBy,
    filters: dict[str, list[str]] | None = None,
) -> list[GroupedTimeEntry]:
    """Group time blocks by the selected scope and return sorted entries."""
    filtered_blocks = apply_filters(blocks, filters) if filters else blocks

    if group_by == GroupBy.SESSION:
        return _group_blocks_by_session(filtered_blocks)

    aggregated: dict[str, _Aggregation] = {}

    for block in filtered_blocks:
        entries = _group_key(block.context, group_by)
        for key, label, url in entries:
            if key not in aggregated:
                aggregated[key] = _Aggregation(label=label, url=url, seconds=0.0)
            aggregated[key].seconds += block.duration_seconds

    result = [
        GroupedTimeEntry(
            key=key,
            label=agg.label,
            total_seconds=agg.seconds,
            total_hours=round(agg.seconds / 3600, 2),
            detail_url=agg.url,
        )
        for key, agg in aggregated.items()
    ]
    result.sort(key=lambda e: e.total_seconds, reverse=True)
    return result


def apply_filters(blocks: list[TimeBlock], filters: dict[str, list[str]]) -> list[TimeBlock]:
    """Filter blocks by the given criteria. All filters must match (AND logic)."""
    result: list[TimeBlock] = []
    for block in blocks:
        ctx = block.context
        if "smart" in filters and filters["smart"]:
            smart_keys = {k for k, _l, _u in _group_key(ctx, GroupBy.SMART)}
            if not smart_keys.intersection(filters["smart"]):
                continue
        if "issue" in filters and filters["issue"]:
            issue_key = f"{ctx.project_path}#{ctx.issue_iid}" if ctx.issue_iid else ""
            if issue_key not in filters["issue"]:
                continue
        if "epic" in filters and filters["epic"]:
            epic_key = f"epic-{ctx.epic_iid}" if ctx.epic_iid else ""
            if epic_key not in filters["epic"]:
                continue
        if "label" in filters and filters["label"]:
            all_labels = set(ctx.issue_labels + ctx.mr_labels)
            if not all_labels.intersection(filters["label"]):
                continue
        if "project" in filters and filters["project"]:
            if ctx.project_path not in filters["project"]:
                continue
        result.append(block)
    return result


def compute_heatmap(
    blocks: list[TimeBlock],
    start_date: date,
    end_date: date,
) -> list[DayActivity]:
    """Compute daily totals from time blocks."""
    daily: dict[date, float] = {}
    current = start_date
    while current <= end_date:
        daily[current] = 0.0
        current += timedelta(days=1)

    for block in blocks:
        day = block.start.date()
        if day in daily:
            daily[day] += block.duration_seconds

    return [
        DayActivity(date=d, total_seconds=secs, total_hours=round(secs / 3600, 2)) for d, secs in sorted(daily.items())
    ]


def collect_filter_values(blocks: list[TimeBlock]) -> FilterValues:
    """Collect all distinct filter values available in the given blocks."""
    smart: dict[str, FilterOption] = {}
    issues: dict[str, FilterOption] = {}
    epics: dict[str, FilterOption] = {}
    labels: set[str] = set()
    projects: set[str] = set()

    for block in blocks:
        ctx = block.context
        # Smart categories
        for key, label, _url in _group_key(ctx, GroupBy.SMART):
            if key not in smart:
                smart[key] = FilterOption(key=key, label=label)
        if ctx.issue_iid and ctx.project_path:
            key = f"{ctx.project_path}#{ctx.issue_iid}"
            if key not in issues:
                label = f"#{ctx.issue_iid} {ctx.issue_title}" if ctx.issue_title else key
                issues[key] = FilterOption(key=key, label=label)
        if ctx.epic_iid:
            key = f"epic-{ctx.epic_iid}"
            if key not in epics:
                label = ctx.epic_title or f"Epic #{ctx.epic_iid}"
                epics[key] = FilterOption(key=key, label=label)
        labels.update(set(ctx.issue_labels + ctx.mr_labels) - _IGNORED_LABELS)
        if ctx.project_path:
            projects.add(ctx.project_path)

    return FilterValues(
        smart=list(smart.values()),
        issues=list(issues.values()),
        epics=list(epics.values()),
        labels=sorted(labels),
        projects=sorted(projects),
    )


def compute_timeline(
    blocks: list[TimeBlock],
    group_by: GroupBy,
    bucket_minutes: int = 5,
) -> tuple[list[str], list[TimelineSeries]]:
    """Compute work density timeline from time blocks, grouped by scope.

    Returns a shared time axis and a list of series (one per group key).
    Each bucket value is the % of the bucket filled with work (100% = continuous).
    """
    if not blocks:
        return [], []

    bucket_secs = bucket_minutes * 60
    min_start = min(b.start for b in blocks)
    max_end = max(b.end for b in blocks)

    # Align to bucket boundaries
    origin = min_start.replace(second=0, microsecond=0)
    origin = origin.replace(minute=(origin.minute // bucket_minutes) * bucket_minutes)

    total_buckets = int((max_end - origin).total_seconds() / bucket_secs) + 1

    # Group blocks by key
    group_buckets: dict[str, tuple[str, list[float]]] = {}  # key -> (label, bucket_work)

    for block in blocks:
        if group_by == GroupBy.SESSION:
            proj = block.context.project_path or block.session_id[:8]
            short = _short_project_path(proj)
            entries = [(block.session_id, short, "")]
        else:
            entries = _group_key(block.context, group_by)
        b_start = (block.start - origin).total_seconds()
        b_end = (block.end - origin).total_seconds()
        first_bucket = int(b_start / bucket_secs)
        last_bucket = int(b_end / bucket_secs)

        for key, label, _url in entries:
            if key not in group_buckets:
                group_buckets[key] = (label, [0.0] * total_buckets)
            bw = group_buckets[key][1]
            for i in range(max(0, first_bucket), min(total_buckets, last_bucket + 1)):
                bucket_start_s = i * bucket_secs
                bucket_end_s = bucket_start_s + bucket_secs
                overlap_start = max(b_start, bucket_start_s)
                overlap_end = min(b_end, bucket_end_s)
                if overlap_end > overlap_start:
                    bw[i] += overlap_end - overlap_start

    # Find range of non-zero buckets across all groups
    any_work = [0.0] * total_buckets
    for _label, bw in group_buckets.values():
        for i in range(total_buckets):
            any_work[i] += bw[i]

    first_active = next((i for i in range(total_buckets) if any_work[i] > 0), 0)
    last_active = next((i for i in range(total_buckets - 1, -1, -1) if any_work[i] > 0), total_buckets - 1)

    # Include one padding bucket on each side
    start_idx = max(0, first_active - 1)
    end_idx = min(total_buckets - 1, last_active + 1)

    times = [(origin + timedelta(seconds=i * bucket_secs)).isoformat() for i in range(start_idx, end_idx + 1)]

    series = []
    for key, (label, bw) in group_buckets.items():
        points = [
            TimelinePoint(time=times[j], percentage=round((bw[i] / bucket_secs) * 100, 1))
            for j, i in enumerate(range(start_idx, end_idx + 1))
        ]
        series.append(TimelineSeries(key=key, label=label, points=points))

    # Sort series by total descending
    series.sort(key=lambda s: sum(p.percentage for p in s.points), reverse=True)

    return times, series


def list_sessions(
    start_date: date,
    end_date: date,
    max_gap_minutes: int = DEFAULT_MAX_GAP_MINUTES,
) -> list[SessionSummary]:
    """List sessions with their context status."""
    blocks = compute_time_blocks(start_date, end_date, max_gap_minutes)
    events = _load_events(start_date, end_date)

    # Find context source per session
    session_ctx: dict[str, tuple[str, ContextEvent | None]] = {}  # session_id -> (source, event)
    for event in events:
        if isinstance(event, ContextEvent):
            sid = event.session_id
            existing_source = session_ctx.get(sid, ("none", None))[0]
            # Manual always wins
            if event.source == "manual" or existing_source != "manual":
                session_ctx[sid] = (event.source, event)

    # Aggregate blocks per session
    @dataclass
    class _SessionAgg:
        seconds: float
        start: datetime
        end: datetime
        cwd: str

    agg: dict[str, _SessionAgg] = {}
    for block in blocks:
        sid = block.session_id
        if sid not in agg:
            agg[sid] = _SessionAgg(seconds=0.0, start=block.start, end=block.end, cwd="")
        a = agg[sid]
        a.seconds += block.duration_seconds
        if block.start < a.start:
            a.start = block.start
        if block.end > a.end:
            a.end = block.end
        if block.context.project_path:
            a.cwd = block.context.project_path

    result = []
    for sid, a in agg.items():
        source, ctx_event = session_ctx.get(sid, ("none", None))
        result.append(
            SessionSummary(
                session_id=sid,
                start=a.start.isoformat(),
                end=a.end.isoformat(),
                total_seconds=a.seconds,
                total_hours=round(a.seconds / 3600, 2),
                cwd=a.cwd,
                project_path=ctx_event.project_path if ctx_event else "",
                issue_iid=ctx_event.issue_iid if ctx_event else "",
                issue_title=ctx_event.issue_title if ctx_event else "",
                epic_iid=ctx_event.epic_iid if ctx_event else "",
                epic_title=ctx_event.epic_title if ctx_event else "",
                context_source=source,
            )
        )
    result.sort(key=lambda s: s.start, reverse=True)
    return result


def get_available_date_range() -> tuple[date | None, date | None]:
    """Return the min and max dates from available log files."""
    if not LOG_DIR.exists():
        return None, None
    dates: list[date] = []
    for f in LOG_DIR.glob("*.jsonl"):
        try:
            dates.append(date.fromisoformat(f.stem))
        except ValueError:
            continue
    if not dates:
        return None, None
    return min(dates), max(dates)
