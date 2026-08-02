"""Shared GitLab issue fetching logic for Pysae skills.

Provides common functions for:
- Resolving usernames (fuzzy match by name)
- Fetching open issues with filters (project, assignee, search)
- Shared typer Options for --me, --user, --project, --all-projects, --search

Used by glab-issue-audit and glab-find-issue.
"""

import json
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated

import typer

from ..group import ensure_group_namespace, resolve_group, resolve_group_id
from .models import GitLabIssue
from .runner import glab_api_paginated as glab_api_paginated
from .runner import run_glab as _run_glab


def run_glab(*args: str, allow_fail: bool = False) -> str:
    """Run ``glab`` and return stdout, exiting the process on failure.

    Convenience wrapper over the shared :func:`..glab.runner.run_glab` for the
    issue-audit / find-issue commands, which want a plain ``str`` and to abort
    on error. ``allow_fail`` returns ``""`` instead of exiting.
    """
    res = _run_glab(*args)
    if not res.ok:
        if allow_fail:
            return ""
        print(f"glab error: {res.stderr}", file=sys.stderr)
        sys.exit(1)
    return res.stdout


# ---------------------------------------------------------------------------
# Username resolution
# ---------------------------------------------------------------------------


def _normalize(text: str) -> str:
    """Lowercase and strip accents for fuzzy matching."""
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def get_current_username() -> str:
    data = json.loads(run_glab("api", "user"))
    return str(data["username"])


def get_current_user_id() -> int:
    """Numeric GitLab id of the authenticated user (for ``assignee_ids`` payloads)."""
    data = json.loads(run_glab("api", "user"))
    return int(data["id"])


def resolve_username(name: str) -> str:
    """Resolve a name (username, first name, or last name) to a GitLab username.

    Searches Pysae group members and matches case-insensitively (accent-insensitive)
    against username, name (display name), or individual words in the display name.
    """
    members_raw = run_glab("api", f"groups/{resolve_group()}/members/all?per_page=100")
    members = json.loads(members_raw)
    query = _normalize(name)

    # Exact username match first
    for m in members:
        if _normalize(m["username"]) == query:
            return str(m["username"])

    # Exact word match in display name
    candidates = []
    for m in members:
        parts = [_normalize(p) for p in m.get("name", "").split()]
        if query in parts:
            candidates.append(m)
    if len(candidates) == 1:
        return str(candidates[0]["username"])

    # Substring match on display name and username
    if not candidates:
        for m in members:
            norm_display = _normalize(m.get("name", ""))
            norm_user = _normalize(m["username"])
            if query in norm_display or query in norm_user:
                candidates.append(m)

    if len(candidates) == 1:
        return str(candidates[0]["username"])
    elif len(candidates) > 1:
        names = ", ".join(f"{c['name']} (@{c['username']})" for c in candidates)
        print(f"Ambiguous name '{name}', matches: {names}", file=sys.stderr)
        sys.exit(1)

    print(f"No Pysae group member matching '{name}'", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Shared typer Options (replaces add_common_issue_args)
# ---------------------------------------------------------------------------

CommonProject = Annotated[
    str | None,
    typer.Option(
        "--project",
        help="Audit a specific project (e.g. pysae/api or just api). Default: all group projects",
    ),
]

CommonAllProjects = Annotated[
    bool,
    typer.Option(
        "--all-projects",
        help="Fetch issues from all group projects (overrides --project)",
    ),
]

CommonMe = Annotated[
    bool,
    typer.Option(
        "--me",
        help="Only fetch issues assigned to the current user",
    ),
]

CommonUser = Annotated[
    str | None,
    typer.Option(
        "--user",
        help="Only fetch issues assigned to a specific user (fuzzy name match)",
    ),
]

CommonSearch = Annotated[
    list[str] | None,
    typer.Option(
        "--search",
        help="Search term to filter issues by title/description (can be repeated)",
    ),
]


@dataclass
class CommonIssueFilters:
    """Resolved common issue filter arguments."""

    project: str | None
    all_projects: bool
    me: bool
    user: str | None
    search: list[str] | None


# ---------------------------------------------------------------------------
# Issue fetching
# ---------------------------------------------------------------------------


def resolve_issue_filters(filters: CommonIssueFilters) -> tuple[str | None, str | None]:
    """Resolve project and assignee from common issue filters.

    Returns (project_path, assignee_username).
    """
    # Resolve project
    project = None
    if filters.all_projects:
        project = None
    elif filters.project:
        project = ensure_group_namespace(filters.project)
    # else: None = all group projects

    # Resolve assignee
    assignee_username = None
    if filters.me:
        assignee_username = get_current_username()
        print(f"Filtrage par assignee : {assignee_username} (--me)", file=sys.stderr)
    elif filters.user:
        assignee_username = resolve_username(filters.user)
        print(f"Filtrage par assignee : {assignee_username} (--user {filters.user})", file=sys.stderr)

    return project, assignee_username


def issue_age_days(issue: GitLabIssue) -> int:
    """Return the age of a GitLab issue in days."""
    if not issue.created_at:
        return 0
    dt = datetime.fromisoformat(issue.created_at.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def fetch_open_issues(
    project: str | None = None,
    assignee_username: str | None = None,
    search: list[str] | None = None,
) -> list[GitLabIssue]:
    """Fetch open issues from GitLab with optional filters.

    Args:
        project: GitLab project path (e.g. 'pysae/api'). None = all group issues.
        assignee_username: Filter by assignee username. None = no filter.
        search: List of search terms. None = no search filter.
               When multiple terms are provided, results are merged and deduplicated.
    """
    base = (
        f"projects/{project.replace('/', '%2F')}/issues?state=opened"
        if project
        else f"groups/{resolve_group_id()}/issues?state=opened"
    )

    if assignee_username:
        base += f"&assignee_username={assignee_username}"

    if search:
        seen: set[tuple[int, int]] = set()
        issues: list[GitLabIssue] = []
        for term in search:
            for raw in glab_api_paginated(f"{base}&search={term}&in=title,description"):
                issue = GitLabIssue.from_api(raw)
                iid_key = (issue.project_id, issue.iid)
                if iid_key not in seen:
                    seen.add(iid_key)
                    issues.append(issue)
        return issues

    return [GitLabIssue.from_api(raw) for raw in glab_api_paginated(base)]
