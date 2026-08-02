"""Typer entry point: `pysae-ai-tools agent design-run`."""

import sys
from typing import Annotated

import typer

from ..common import detect_current_project, parse_duration_seconds
from ..models import RunConfig
from ..projects import resolve_projects
from .pipeline import run_design_pipeline

app = typer.Typer(help="Design autopilot batch: auto-eligibility gate + headless /design-generate")


@app.callback(invoke_without_command=True)
def run(
    ctx: typer.Context,
    project: Annotated[
        list[str] | None,
        typer.Option("--project", help="Project (full path or short form). Repeatable."),
    ] = None,
    max_tickets: Annotated[int, typer.Option("--max-tickets")] = 5,
    max_tokens: Annotated[int, typer.Option("--max-tokens")] = 100_000_000,
    timeout: Annotated[str, typer.Option("--timeout")] = "2h",
    per_ticket_timeout: Annotated[str, typer.Option("--per-ticket-timeout")] = "1h",
    orphan_timeout: Annotated[str, typer.Option("--orphan-timeout")] = "2h",
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    tickets: Annotated[str | None, typer.Option("--tickets", help="Comma-separated URLs (bypass the pull).")] = None,
    threshold: Annotated[
        int,
        typer.Option("--threshold", help="Min Haiku confidence (0-100) to fast-path a commodity-UI ticket."),
    ] = 70,
    skip_llm_rank: Annotated[
        bool,
        typer.Option("--skip-llm-rank", help="Deterministic prefilter only (no Haiku eligibility call)."),
    ] = False,
    slack_channel: Annotated[str, typer.Option("--slack-channel")] = "#tech-ci-agent-autopilot",
    no_slack: Annotated[bool, typer.Option("--no-slack")] = False,
) -> None:
    """Run a batch of workflow::Ready UI tickets through auto-eligibility + /design-generate."""
    if ctx.invoked_subcommand is not None:
        return
    if project:
        projects = resolve_projects(project)
    else:
        current = detect_current_project()
        if not current:
            raise typer.BadParameter("no --project given and current repo not detected. Pass --project explicitly.")
        projects = [current]

    cfg = RunConfig(
        projects=projects,
        max_tickets=max_tickets,
        max_tokens=max_tokens,
        timeout_seconds=parse_duration_seconds(timeout),
        per_ticket_timeout_seconds=parse_duration_seconds(per_ticket_timeout),
        orphan_timeout_seconds=parse_duration_seconds(orphan_timeout),
        dry_run=dry_run,
        skip_llm_rank=skip_llm_rank,
        slack_channel=slack_channel,
        slack_enabled=not no_slack,
        explicit_tickets=[s.strip() for s in tickets.split(",")] if tickets else [],
        watch_post_merge_deploy=False,
        check_completeness=False,
        design_eligibility_threshold=threshold,
    )

    result = run_design_pipeline(cfg)
    sys.exit(1 if result.escalations > 0 else 0)
