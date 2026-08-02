"""FastAPI server for the activity dashboard.

Usage:
    pysae-ai-tools tracker dashboard [--port PORT]
"""

import importlib.resources
import json
import logging
import os
import signal
from datetime import date
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Annotated

import typer
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response

from ..common.glab.runner import run_glab
from ..common.local_server import LocalServer
from ..common.paths import temp_path
from .models import (
    ContextualizeRequest,
    DashboardResponse,
    DateRangeResponse,
    FilterValues,
    GitLabIssueOption,
    GitLabIssuesResponse,
    GroupBy,
    HeatmapResponse,
    SessionsResponse,
    TimelineResponse,
)
from .time_engine import (
    apply_filters,
    collect_filter_values,
    compute_heatmap,
    compute_time_blocks,
    compute_timeline,
    get_available_date_range,
    group_blocks,
    list_sessions,
)

SHUTDOWN_TIMEOUT = 10 * 60
PID_FILE = temp_path("pysae-activity-dashboard.pid")

app = FastAPI(title="Pysae Activity Dashboard")

_server = LocalServer(
    app=app,
    module="pysae_ai_tools.tracker.server",
    pid_file=PID_FILE,
    health_path="/api/date-range",
    healthy_statuses={200},
    shutdown_timeout=SHUTDOWN_TIMEOUT,
)
_schedule_shutdown = _server.schedule_shutdown


def _templates_dir() -> Traversable:
    return importlib.resources.files("pysae_ai_tools.tracker.templates")


# ---------------------------------------------------------------------------
# Static / HTML
# ---------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    tpl = _templates_dir().joinpath("dashboard.html")
    return HTMLResponse(
        tpl.read_text(encoding="utf-8"), headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )


@app.get("/static/{filename}")
async def static_file(filename: str) -> Response:
    path = _templates_dir().joinpath(filename)
    if not path.is_file():
        return JSONResponse({"error": "not found"}, status_code=404)
    content_types = {".css": "text/css", ".js": "application/javascript"}
    return FileResponse(
        str(path),
        media_type=content_types.get(Path(filename).suffix, "text/plain"),
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
    )


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------


@app.get("/api/dashboard")
async def dashboard(
    start_date: Annotated[date, Query(description="Start date (YYYY-MM-DD)")],
    end_date: Annotated[date, Query(description="End date (YYYY-MM-DD)")],
    group_by: Annotated[GroupBy, Query(description="Grouping scope")] = GroupBy.ISSUE,
    max_gap_minutes: Annotated[int, Query(description="Max idle gap in minutes", ge=1, le=120)] = 15,
    filter_smart: Annotated[list[str], Query(description="Filter by smart categories")] = [],  # noqa: B006
    filter_issue: Annotated[list[str], Query(description="Filter by issue keys")] = [],  # noqa: B006
    filter_epic: Annotated[list[str], Query(description="Filter by epic keys")] = [],  # noqa: B006
    filter_label: Annotated[list[str], Query(description="Filter by labels")] = [],  # noqa: B006
    filter_project: Annotated[list[str], Query(description="Filter by projects")] = [],  # noqa: B006
) -> DashboardResponse:
    _schedule_shutdown()

    filters: dict[str, list[str]] = {}
    if filter_smart:
        filters["smart"] = filter_smart
    if filter_issue:
        filters["issue"] = filter_issue
    if filter_epic:
        filters["epic"] = filter_epic
    if filter_label:
        filters["label"] = filter_label
    if filter_project:
        filters["project"] = filter_project

    blocks = compute_time_blocks(start_date, end_date, max_gap_minutes)
    entries = group_blocks(blocks, group_by, filters or None)
    total_seconds = sum(e.total_seconds for e in entries)

    # Compute percentages
    for entry in entries:
        entry.percentage = round(entry.total_seconds / total_seconds * 100, 1) if total_seconds > 0 else 0.0

    return DashboardResponse(
        start_date=start_date,
        end_date=end_date,
        group_by=group_by,
        total_seconds=total_seconds,
        total_hours=round(total_seconds / 3600, 2),
        entries=entries,
    )


@app.get("/api/heatmap")
async def heatmap(
    start_date: Annotated[date, Query(description="Start date (YYYY-MM-DD)")],
    end_date: Annotated[date, Query(description="End date (YYYY-MM-DD)")],
    max_gap_minutes: Annotated[int, Query(description="Max idle gap in minutes", ge=1, le=120)] = 15,
) -> HeatmapResponse:
    _schedule_shutdown()
    blocks = compute_time_blocks(start_date, end_date, max_gap_minutes)
    days = compute_heatmap(blocks, start_date, end_date)
    return HeatmapResponse(start_date=start_date, end_date=end_date, days=days)


@app.get("/api/filters")
async def filters(
    start_date: Annotated[date, Query(description="Start date (YYYY-MM-DD)")],
    end_date: Annotated[date, Query(description="End date (YYYY-MM-DD)")],
    max_gap_minutes: Annotated[int, Query(description="Max idle gap in minutes", ge=1, le=120)] = 15,
) -> FilterValues:
    _schedule_shutdown()
    blocks = compute_time_blocks(start_date, end_date, max_gap_minutes)
    return collect_filter_values(blocks)


@app.get("/api/timeline")
async def timeline(
    start_date: Annotated[date, Query(description="Start date (YYYY-MM-DD)")],
    end_date: Annotated[date, Query(description="End date (YYYY-MM-DD)")],
    group_by: Annotated[GroupBy, Query(description="Grouping scope")] = GroupBy.PROJECT,
    max_gap_minutes: Annotated[int, Query(description="Max idle gap in minutes", ge=1, le=120)] = 15,
    bucket_minutes: Annotated[int, Query(description="Bucket size in minutes", ge=1, le=60)] = 5,
    filter_smart: Annotated[list[str], Query(description="Filter by smart categories")] = [],  # noqa: B006
    filter_issue: Annotated[list[str], Query(description="Filter by issue keys")] = [],  # noqa: B006
    filter_epic: Annotated[list[str], Query(description="Filter by epic keys")] = [],  # noqa: B006
    filter_label: Annotated[list[str], Query(description="Filter by labels")] = [],  # noqa: B006
    filter_project: Annotated[list[str], Query(description="Filter by projects")] = [],  # noqa: B006
) -> TimelineResponse:
    _schedule_shutdown()
    blocks = compute_time_blocks(start_date, end_date, max_gap_minutes)

    filters: dict[str, list[str]] = {}
    if filter_smart:
        filters["smart"] = filter_smart
    if filter_issue:
        filters["issue"] = filter_issue
    if filter_epic:
        filters["epic"] = filter_epic
    if filter_label:
        filters["label"] = filter_label
    if filter_project:
        filters["project"] = filter_project

    if filters:
        blocks = apply_filters(blocks, filters)

    times, series = compute_timeline(blocks, group_by, bucket_minutes)
    return TimelineResponse(
        start_date=start_date,
        end_date=end_date,
        bucket_minutes=bucket_minutes,
        times=times,
        series=series,
    )


@app.get("/api/sessions")
async def sessions(
    start_date: Annotated[date, Query(description="Start date (YYYY-MM-DD)")],
    end_date: Annotated[date, Query(description="End date (YYYY-MM-DD)")],
    max_gap_minutes: Annotated[int, Query(description="Max idle gap in minutes", ge=1, le=120)] = 15,
) -> SessionsResponse:
    _schedule_shutdown()
    session_list = list_sessions(start_date, end_date, max_gap_minutes)
    return SessionsResponse(start_date=start_date, end_date=end_date, sessions=session_list)


@app.post("/api/contextualize")
async def contextualize(req: ContextualizeRequest) -> dict[str, str]:
    _schedule_shutdown()
    from .hook import log_context_manual

    result = log_context_manual(
        session_id=req.session_id,
        project_path=req.project_path,
        project_id=req.project_id,
        project_url=req.project_url,
        issue_iid=req.issue_iid,
        issue_title=req.issue_title,
        issue_url=req.issue_url,
        issue_labels=req.issue_labels,
        epic_iid=req.epic_iid,
        epic_title=req.epic_title,
        epic_url=req.epic_url,
        target_date=req.target_date,
    )
    if result.startswith("ERROR"):
        return {"status": "error", "message": result}
    return {"status": "ok", "message": result}


_logger = logging.getLogger(__name__)


def _parse_glab_issues(raw: list[dict[str, object]], fallback_project: str = "") -> list[GitLabIssueOption]:
    """Parse raw JSON issue objects from glab into GitLabIssueOption list."""
    issues = []
    for item in raw:
        refs = item.get("references", {})
        full_ref = refs.get("full", "") if isinstance(refs, dict) else ""
        proj = full_ref.rsplit("#", 1)[0] if "#" in full_ref else fallback_project
        issues.append(
            GitLabIssueOption(
                iid=str(item.get("iid", "")),
                title=str(item.get("title", "")),
                web_url=str(item.get("web_url", "")),
                labels=item.get("labels", []) if isinstance(item.get("labels"), list) else [],
                project_path=proj,
                project_id=str(item.get("project_id", "")),
            )
        )
    return issues


def _fetch_project_issues(project_path: str, search: str = "") -> list[GitLabIssueOption]:
    """Fetch open issues for a specific project via glab CLI."""
    args = ["issue", "list", "--output", "json", "--per-page", "50", "--repo", project_path]
    if search:
        args.extend(["--search", search])
    res = run_glab(*args, timeout=15)
    if not res.ok:
        _logger.warning("glab issue list failed for %s: %s", project_path, res.stderr[:200])
        return []
    try:
        raw = json.loads(res.stdout) if res.stdout else []
    except json.JSONDecodeError as exc:
        _logger.warning("glab issue list error for %s: %s", project_path, exc)
        return []
    return _parse_glab_issues(raw, project_path)


def _search_group_issues(search: str, group: str = "pysae") -> list[GitLabIssueOption]:
    """Search open issues across the entire GitLab group via API."""
    res = run_glab(
        "api",
        f"groups/{group}/issues",
        "-X",
        "GET",
        "-f",
        "state=opened",
        "-f",
        "per_page=30",
        "-f",
        f"search={search}",
        timeout=15,
    )
    if not res.ok:
        _logger.warning("glab api group issues failed: %s", res.stderr[:200])
        return []
    try:
        raw = json.loads(res.stdout) if res.stdout else []
    except json.JSONDecodeError as exc:
        _logger.warning("glab api group issues error: %s", exc)
        return []
    return _parse_glab_issues(raw)


@app.get("/api/gitlab-issues")
async def gitlab_issues(
    project_path: Annotated[str, Query(description="Project path for priority issues")] = "",
    other_projects: Annotated[list[str], Query(description="Other project paths to search")] = [],  # noqa: B006
    search: Annotated[str, Query(description="Search keyword")] = "",
) -> GitLabIssuesResponse:
    _schedule_shutdown()

    priority: list[GitLabIssueOption] = []
    other: list[GitLabIssueOption] = []

    if project_path:
        priority = _fetch_project_issues(project_path, search)
        # Sort: workflow::* labels first
        priority.sort(key=lambda i: (0 if any(lbl.startswith("workflow::") for lbl in i.labels) else 1, i.title))

    # Fetch issues from other projects
    if search:
        # Search across the entire GitLab group
        all_issues = _search_group_issues(search)
        seen = {i.iid + i.project_path for i in priority}
        other = [i for i in all_issues if (i.iid + i.project_path) not in seen]
    else:
        for proj in other_projects:
            if proj != project_path:
                other.extend(_fetch_project_issues(proj))

    return GitLabIssuesResponse(priority_issues=priority, other_issues=other)


@app.get("/api/date-range")
async def date_range() -> DateRangeResponse:
    _schedule_shutdown()
    min_d, max_d = get_available_date_range()
    return DateRangeResponse(min_date=min_d, max_date=max_d)


@app.post("/api/keepalive")
async def keepalive() -> dict[str, str]:
    _schedule_shutdown()
    return {"status": "ok"}


@app.post("/api/shutdown")
async def shutdown() -> dict[str, str]:
    os.kill(os.getpid(), signal.SIGTERM)
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Server lifecycle
# ---------------------------------------------------------------------------

ensure_server = _server.ensure


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

cli = typer.Typer()


@cli.command()
def main(
    port: Annotated[int, typer.Option("--port", help="Port to run the server on")] = 0,
) -> None:
    """Run the dashboard server (used internally by ensure_server)."""
    if not port:
        port = LocalServer.find_free_port()
    _server.run(port)


if __name__ == "__main__":
    cli()
