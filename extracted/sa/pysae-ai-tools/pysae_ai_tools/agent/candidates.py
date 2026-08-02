"""``pysae-ai-tools agent candidates`` — the deterministic candidate pool.

Reclaims WIP orphans (optional), pulls ``agent::ready`` tickets — or, with
``--tickets``, a hand-picked URL list — computes the business score and the
sensitive-path (regex) flag, and emits the pool as JSON sorted by business score.
**No LLM call**: the in-session orchestration skill scores each candidate with
parallel subagents, then feeds them to ``agent rank``.
"""

import json
from typing import Annotated, Any

import typer

from ..glab.issue_ready_check.cli import evaluate_for_batch
from .common import detect_current_project, parse_duration_seconds, resolve_explicit_tickets
from .guards import has_override, has_sensitive_keywords
from .labels import CommentPostError, LabelTransitionError, mark_blocked
from .models import Ticket
from .orphan import find_orphans
from .projects import resolve_projects
from .pull import fetch_ready_tickets, fetch_wip_tickets
from .score import business_score


def _format_violation_line(v: Any) -> str:
    """Render a ReadyCheck Violation as a single-line human-readable string.

    Output matches the per-line style of ``issue_ready_check.actions._format_violation``
    minus the leading bullet.
    """
    if hasattr(v, "section"):
        return f"Section `{v.section}` : {v.reason}"
    if hasattr(v, "checkbox"):
        return f'Checkbox "{v.checkbox}" : {v.reason}'
    return str(v)


def _pool_entry(t: Ticket) -> dict[str, Any]:
    structural = evaluate_for_batch(description=t.description or "", labels=t.labels)
    return {
        "iid": t.iid,
        "project_path": t.project_path,
        "web_url": t.web_url,
        "title": t.title,
        "description": t.description or "",
        "labels": t.labels,
        "author_username": t.author_username,
        "business_score": business_score(t),
        "sensitive_path": has_sensitive_keywords(t) and not has_override(t),
        "structural_ready": structural.ready,
        "structural_violations": [_format_violation_line(v) for v in structural.violations],
    }


def main(
    project: Annotated[
        list[str] | None, typer.Option("--project", help="Project (full path or short form). Repeatable.")
    ] = None,
    reclaim_orphans: Annotated[
        bool, typer.Option("--reclaim-orphans", help="Escalate agent::wip tickets stuck beyond --orphan-timeout.")
    ] = False,
    orphan_timeout: Annotated[str, typer.Option("--orphan-timeout")] = "2h",
    run_id: Annotated[str, typer.Option("--run-id", help="Run id recorded in escalation comments.")] = "manual",
    tickets: Annotated[
        str | None,
        typer.Option(
            "--tickets",
            help="Comma-separated full GitLab issue URLs — build the pool from these instead "
            "of pulling agent::ready (hand-picked mode; skips orphan reclaim).",
        ),
    ] = None,
) -> None:
    """Emit the deterministic candidate pool as JSON (business-scored, no LLM).

    Default: pull the ``agent::ready`` tickets across the resolved projects. With ``--tickets``,
    build the pool from an explicit URL list instead (the tickets carry their own project).
    """
    if tickets:
        resolved, failures = resolve_explicit_tickets([s.strip() for s in tickets.split(",") if s.strip()])
        for f in failures:
            typer.echo(f"skipped --tickets ref {f.project_path}: {f.escalation_reason}", err=True)
        pool = [_pool_entry(t) for t in resolved]
        pool.sort(key=lambda c: c["business_score"], reverse=True)
        typer.echo(json.dumps(pool, ensure_ascii=False))
        return

    if project:
        projects = resolve_projects(project)
    else:
        current = detect_current_project()
        if not current:
            typer.echo("no --project given and current repo not detected", err=True)
            raise typer.Exit(code=1)
        projects = [current]

    if reclaim_orphans:
        timeout_seconds = parse_duration_seconds(orphan_timeout)
        reason = f"WIP orphelin (>{timeout_seconds}s), agent crashé probable"
        for ticket in find_orphans(fetch_wip_tickets(projects), timeout_seconds):
            # Swallow per-orphan failures: a single label/comment error must not abort the pull.
            try:
                mark_blocked(ticket, reason, run_id)
            except (LabelTransitionError, CommentPostError):
                pass

    pool = [_pool_entry(t) for t in fetch_ready_tickets(projects)]
    pool.sort(key=lambda c: c["business_score"], reverse=True)
    typer.echo(json.dumps(pool, ensure_ascii=False))
