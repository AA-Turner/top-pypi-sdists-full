#!/usr/bin/env python3
"""Pick the best next GitLab issue to work on.

Fetches open issues from the Pysae group and ranks them using a weighted
scoring system across three equally-weighted dimensions:

  1. Board column label  (workflow stage)
  2. Priority label      (P1 > P2 > P3 > none)
  3. User affinity       (created by or assigned to the current user)

Plus bonuses for issue type (bug, support) and age.

Usage:
    python3 next_issue.py [--top N] [--project PROJECT_PATH] [--user NAME]
        [--me] [--p1|--p2|--p3] [--search TERM ...] [--quick-wins]
        [--domain DOMAIN ...] [--exclude-label LABEL ...]
        [--all-projects]

The --user flag accepts a GitLab username, first name, or last name.
It resolves to the matching Pysae group member.
"""

import json
from typing import Annotated, Any

import typer

from ..common.glab.fetch_issues import (
    CommonAllProjects,
    CommonIssueFilters,
    CommonMe,
    CommonProject,
    CommonSearch,
    CommonUser,
    fetch_open_issues,
    get_current_username,
    issue_age_days,
    resolve_issue_filters,
    resolve_username,
)
from ..common.glab.models import GitLabIssue
from ..common.glab.runner import resolve_current_project

# ---------------------------------------------------------------------------
# Scoring parameters -- each dimension is 0-100, final score = sum / 3
# ---------------------------------------------------------------------------

BOARD_SCORES: dict[str, int] = {
    "workflow::To Do": 100,
    "workflow::Ready": 75,
    "workflow::Refinement": 50,
    # Issues without any board label (Open/Backlog)
    "_none": 25,
}

PRIORITY_SCORES: dict[str, int] = {
    "priority::P1": 100,
    "priority::P2": 66,
    "priority::P3": 33,
    "_none": 0,
}

USER_AFFINITY_SCORES: dict[str, int] = {
    "created_and_assigned": 100,
    "assigned": 75,
    "created": 75,
    "_none": 0,
}

TYPE_BONUS: dict[str, int] = {
    "type::bug": 15,
    "Support": 15,
}

# Age bonus: issues older than AGE_THRESHOLD_DAYS get up to AGE_BONUS_MAX points
# Linear interpolation from 0 at threshold to max at AGE_BONUS_CAP_DAYS
AGE_THRESHOLD_DAYS = 21
AGE_BONUS_CAP_DAYS = 180
AGE_BONUS_MAX = 10

# Quick wins: max weight considered a quick win
QUICK_WIN_MAX_WEIGHT = 3

# Labels that indicate the issue is already being worked on -- skip these
SKIP_LABELS: set[str] = {
    "workflow::In progress",
    "workflow::Under review",
    "workflow::To deploy",
}

# Description snippet: max characters to include
SNIPPET_MAX_CHARS = 200

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _issue_priority_level(issue: GitLabIssue) -> int:
    """Return numeric priority level: 1 for P1, 2 for P2, 3 for P3. No label = 2."""
    labels = issue.labels
    for label in labels:
        if label == "priority::P1":
            return 1
        if label == "priority::P2":
            return 2
        if label == "priority::P3":
            return 3
    return 2  # no priority label defaults to P2


def _make_snippet(description: str | None) -> str:
    """Extract a short snippet from the issue description."""
    if not description:
        return ""
    # Strip markdown headers, blank lines, and quick actions
    lines = []
    for line in description.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("/"):
            continue
        if stripped.startswith("<!--"):
            continue
        lines.append(stripped)
    text = " ".join(lines)
    if len(text) > SNIPPET_MAX_CHARS:
        text = text[:SNIPPET_MAX_CHARS].rsplit(" ", 1)[0] + "..."
    return text


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def score_issue(issue: GitLabIssue, username: str | None, stale: bool = False) -> dict[str, Any] | None:
    labels = set(issue.labels)

    # Skip issues already in progress / under review / to deploy
    if labels & SKIP_LABELS:
        return None

    # Dimension 1: board column
    board_score = BOARD_SCORES["_none"]
    for label, score in BOARD_SCORES.items():
        if label != "_none" and label in labels:
            board_score = score
            break

    # Dimension 2: priority
    priority_score = PRIORITY_SCORES["_none"]
    for label, score in PRIORITY_SCORES.items():
        if label != "_none" and label in labels:
            priority_score = score
            break

    # Dimension 3: user affinity (skipped in anonymous mode)
    if username:
        author = issue.author.username
        assignees = [a.username for a in issue.assignees]
        is_created = author == username
        is_assigned = username in assignees

        if is_created and is_assigned:
            affinity_score = USER_AFFINITY_SCORES["created_and_assigned"]
        elif is_assigned:
            affinity_score = USER_AFFINITY_SCORES["assigned"]
        elif is_created:
            affinity_score = USER_AFFINITY_SCORES["created"]
        else:
            affinity_score = USER_AFFINITY_SCORES["_none"]
    else:
        affinity_score = None

    # Bonus for issue type
    type_bonus = sum(v for k, v in TYPE_BONUS.items() if k in labels)

    # Bonus for age: recent by default, old with --stale
    age_days = issue_age_days(issue)
    if not stale:
        if age_days < AGE_BONUS_CAP_DAYS:
            age_bonus = round(AGE_BONUS_MAX * (1 - age_days / AGE_BONUS_CAP_DAYS), 1)
        else:
            age_bonus = 0
    else:
        if age_days > AGE_THRESHOLD_DAYS:
            effective_days = min(age_days - AGE_THRESHOLD_DAYS, AGE_BONUS_CAP_DAYS - AGE_THRESHOLD_DAYS)
            age_bonus = round(AGE_BONUS_MAX * effective_days / (AGE_BONUS_CAP_DAYS - AGE_THRESHOLD_DAYS), 1)
        else:
            age_bonus = 0

    bonus = type_bonus + age_bonus
    if affinity_score is not None:
        total = (board_score + priority_score + affinity_score) / 3 + bonus
    else:
        total = (board_score + priority_score) / 2 + bonus

    return {
        "iid": issue.iid,
        "title": issue.title,
        "web_url": issue.web_url,
        "labels": sorted(labels),
        "assignees": [a.name or a.username for a in issue.assignees],
        "weight": issue.weight,
        "age_days": age_days,
        "snippet": _make_snippet(issue.description),
        "board_score": board_score,
        "priority_score": priority_score,
        "affinity_score": affinity_score,
        "bonus": round(bonus, 1),
        "total_score": round(total, 1),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

cli = typer.Typer()


@cli.command()
def main(
    top: Annotated[int, typer.Option("--top", help="Number of candidates to show (default: 3)")] = 3,
    project: CommonProject = None,
    all_projects: CommonAllProjects = False,
    me: CommonMe = False,
    user: CommonUser = None,
    search: CommonSearch = None,
    p1: Annotated[bool, typer.Option("--p1", help="Only P1 issues")] = False,
    p2: Annotated[bool, typer.Option("--p2", help="P1 and P2 issues (default priority = P2)")] = False,
    p3: Annotated[bool, typer.Option("--p3", help="P1, P2, and P3 issues (default priority = P2)")] = False,
    quick_wins: Annotated[
        bool, typer.Option("--quick-wins", help="Only show issues with weight <= 3 (quick wins)")
    ] = False,
    domain: Annotated[
        list[str] | None,
        typer.Option(
            "--domain",
            help="Filter by domain label: API, OP, DRIVER, EDITOR, INFO, INFRA, Screen (can be repeated)",
        ),
    ] = None,
    exclude_label: Annotated[
        list[str] | None,
        typer.Option("--exclude-label", help="Exclude issues that have this label (can be repeated)"),
    ] = None,
    anonymous: Annotated[
        bool, typer.Option("--anonymous", help="Ignore user affinity in scoring (no user lookup)")
    ] = False,
    stale: Annotated[
        bool, typer.Option("--stale", help="Prefer older issues (bonus increases with age instead of recency)")
    ] = False,
) -> None:
    """Pick the best next GitLab issue to implement, scored and ranked."""
    # Resolve max_priority from mutually exclusive flags
    max_priority: int | None = None
    if p1:
        max_priority = 1
    elif p2:
        max_priority = 2
    elif p3:
        max_priority = 3

    if anonymous:
        username = None
    else:
        username = resolve_username(user) if user else get_current_username()

    # Resolve project: --domain implies --all-projects
    resolved_all_projects = all_projects
    if domain:
        resolved_all_projects = True

    filters = CommonIssueFilters(
        project=project,
        all_projects=resolved_all_projects,
        me=me,
        user=user,
        search=search,
    )
    resolved_project, assignee_username = resolve_issue_filters(filters)

    # Auto-detect project from repo if not explicitly set
    if not resolved_project and not resolved_all_projects:
        resolved_project = resolve_current_project()[1] or None

    # Fetch issues via shared module
    issues = fetch_open_issues(
        project=resolved_project,
        assignee_username=assignee_username,
        search=search,
    )

    if max_priority:
        issues = [i for i in issues if _issue_priority_level(i) <= max_priority]

    if quick_wins:
        issues = [i for i in issues if (i.weight or 0) <= QUICK_WIN_MAX_WEIGHT and i.weight is not None]

    if domain:
        domain_set = {d.upper() for d in domain}
        # Also accept case-insensitive match for labels like "Screen"
        issues = [i for i in issues if any(lbl.upper() in domain_set for lbl in i.labels)]

    if exclude_label:
        exclude_set = set(exclude_label)
        # Also match case-insensitively
        exclude_lower = {lbl.lower() for lbl in exclude_set}
        issues = [i for i in issues if not any(lbl.lower() in exclude_lower for lbl in i.labels)]

    scored = []
    for issue in issues:
        result = score_issue(issue, username, stale=stale)
        if result:
            scored.append(result)

    # In stale mode, exclude issues too recent to have an age bonus
    if stale:
        scored = [s for s in scored if s["age_days"] > AGE_THRESHOLD_DAYS]

    scored.sort(key=lambda x: x["total_score"], reverse=True)
    top_results = scored[:top]

    print(json.dumps(top_results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    cli()
