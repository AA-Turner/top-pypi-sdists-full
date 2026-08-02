"""Fetch child issues of a GitLab epic and output a structured summary.

The SKILL.md uses this output to draft an epic description via Claude.

Usage:
    pysae-ai-tools glab epic-from-issues --epic 42
"""

import json
import sys
from collections import Counter
from typing import Annotated, Any

import typer

from ..common.glab.fetch_issues import glab_api_paginated, run_glab
from ..common.group import resolve_group_id

cli = typer.Typer(help="Summarize child issues of a GitLab epic")


def _resolve_project_name(project_id: int, cache: dict[int, str]) -> str:
    """Resolve a project ID to its short path name."""
    if project_id in cache:
        return cache[project_id]
    raw = run_glab("api", f"projects/{project_id}", allow_fail=True)
    if raw:
        data = json.loads(raw)
        name: str = data.get("path", str(project_id))
        cache[project_id] = name
        return name
    cache[project_id] = str(project_id)
    return str(project_id)


@cli.command()
def main(
    epic: Annotated[
        int,
        typer.Option("--epic", help="Epic IID in the pysae group"),
    ],
) -> None:
    """Fetch all child issues of an epic and output a structured JSON summary."""
    try:
        group_id = resolve_group_id()
    except RuntimeError as exc:
        print(f"✗ {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from None
    # Fetch epic metadata
    print(f"Récupération de l'epic #{epic}...", file=sys.stderr)
    epic_raw = run_glab("api", f"groups/{group_id}/epics/{epic}")
    epic_data = json.loads(epic_raw)

    # Fetch child issues (all states)
    print("Récupération des tickets rattachés...", file=sys.stderr)
    child_issues_raw = glab_api_paginated(f"groups/{group_id}/epics/{epic}/issues?per_page=100")
    print(f"  {len(child_issues_raw)} tickets trouvés", file=sys.stderr)

    # Resolve project names
    project_cache: dict[int, str] = {}
    issues: list[dict[str, Any]] = []
    for raw in child_issues_raw:
        pid = raw.get("project_id", 0)
        issues.append(
            {
                "iid": raw.get("iid", 0),
                "project_id": pid,
                "project_name": _resolve_project_name(pid, project_cache),
                "title": raw.get("title", ""),
                "state": raw.get("state", ""),
                "labels": raw.get("labels", []),
                "weight": raw.get("weight"),
                "description": (raw.get("description") or "")[:500],
                "web_url": raw.get("web_url", ""),
            }
        )

    # Compute stats
    open_count = sum(1 for i in issues if i["state"] == "opened")
    closed_count = sum(1 for i in issues if i["state"] == "closed")
    total_weight = sum(i["weight"] or 0 for i in issues)
    closed_weight = sum(i["weight"] or 0 for i in issues if i["state"] == "closed")

    # Labels breakdown
    label_counter: Counter[str] = Counter()
    for i in issues:
        for lbl in i["labels"]:
            label_counter[lbl] += 1

    # Projects breakdown
    project_counter: Counter[str] = Counter()
    for i in issues:
        project_counter[i["project_name"]] += 1

    output: dict[str, Any] = {
        "epic": {
            "iid": epic_data.get("iid", 0),
            "title": epic_data.get("title", ""),
            "description": epic_data.get("description") or "",
            "labels": epic_data.get("labels", []),
            "web_url": epic_data.get("web_url", ""),
        },
        "issues": issues,
        "stats": {
            "total": len(issues),
            "open": open_count,
            "closed": closed_count,
            "total_weight": total_weight,
            "closed_weight": closed_weight,
            "completion_pct": round(closed_count / len(issues) * 100) if issues else 0,
            "weight_completion_pct": round(closed_weight / total_weight * 100) if total_weight else 0,
            "labels": dict(label_counter.most_common(20)),
            "projects": dict(project_counter.most_common()),
        },
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    cli()
