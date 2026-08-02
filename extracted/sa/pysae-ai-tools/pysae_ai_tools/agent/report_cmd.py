"""``pysae-ai-tools agent report`` — render the batch summary from outcomes.

Reads a JSON list of :class:`~pysae_ai_tools.agent.models.Outcome` on stdin
(the in-session skill collects one per processed ticket) and delegates to
:func:`pysae_ai_tools.agent.report.publish`, which prints the ASCII table and
posts to Slack unless ``--no-slack``.
"""

import json
import sys
from typing import Annotated, Any

import typer

from .models import Outcome, RunConfig, RunResult
from .report import publish


def main(
    run_id: Annotated[str, typer.Option("--run-id")] = "manual",
    max_tickets: Annotated[int, typer.Option("--max-tickets")] = 5,
    max_tokens: Annotated[int, typer.Option("--max-tokens")] = 100_000_000,
    slack_channel: Annotated[str, typer.Option("--slack-channel")] = "#tech-ci-agent-autopilot",
    slack_channel_map: Annotated[
        str, typer.Option("--slack-channel-map", help="JSON {project_path: channel} for per-project routing.")
    ] = "",
    per_project_slack: Annotated[
        bool,
        typer.Option(
            "--per-project-slack",
            help="Route each outcome to its repo's slack.tech_channel (else all land on --slack-channel).",
        ),
    ] = False,
    no_slack: Annotated[bool, typer.Option("--no-slack")] = False,
) -> None:
    """Render the batch summary table from outcomes on stdin; post to Slack unless --no-slack."""
    try:
        raw: list[dict[str, Any]] = json.loads(sys.stdin.read() or "[]")
        channel_map: dict[str, str] = json.loads(slack_channel_map) if slack_channel_map else {}
    except json.JSONDecodeError as exc:
        typer.echo(f"invalid JSON on stdin/--slack-channel-map: {exc}", err=True)
        raise typer.Exit(code=1) from None

    result = RunResult(run_id=run_id, outcomes=[Outcome.model_validate(o) for o in raw])
    cfg = RunConfig(
        projects=[],
        slack_channel=slack_channel,
        slack_channel_map=channel_map,
        slack_per_project=per_project_slack,
        slack_enabled=not no_slack,
        max_tickets=max_tickets,
        max_tokens=max_tokens,
    )
    publish(result, cfg)
