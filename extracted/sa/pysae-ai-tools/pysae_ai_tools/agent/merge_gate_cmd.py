"""``pysae-ai-tools agent merge-gate`` — merge one ready_to_merge outcome, re-validated.

Reads a ``ready_to_merge`` :class:`~pysae_ai_tools.agent.models.Outcome` on stdin, runs the
serial merge-gate (rebase + re-CI + merge, or merge train) and emits the updated outcome
(``success`` merged, or ``escalated``). Strategy defaults to the repo's ``autopilot.merge_strategy``;
``--strategy`` overrides. The caller invokes this **one MR at a time**.
"""

import json
import sys
from typing import Annotated

import typer

from .autopilot_config import load_autopilot, resolve_ci_selection
from .common import parse_duration_seconds
from .merge_gate import run_merge_gate
from .models import Outcome


def main(
    strategy: Annotated[str | None, typer.Option("--strategy", help="rebase | train (default: repo config).")] = None,
    timeout: Annotated[str, typer.Option("--timeout")] = "30m",
    no_ci: Annotated[bool, typer.Option("--no-ci", help="Skip the pre-merge CI gate (merge without re-CI).")] = False,
) -> None:
    """Merge the ready_to_merge outcome on stdin; emit the updated outcome as JSON.

    The pre-merge CI gate honours the repo's ``autopilot.ci_jobs`` (None = whole pipeline,
    list = those jobs, False/[] = none); ``--no-ci`` forces it off for this call.
    """
    try:
        outcome = Outcome.model_validate(json.loads(sys.stdin.read()))
    except (json.JSONDecodeError, ValueError) as exc:
        typer.echo(f"invalid Outcome JSON on stdin: {exc}", err=True)
        raise typer.Exit(code=1) from None
    autopilot = load_autopilot(outcome.project_path)
    resolved = strategy or autopilot.merge_strategy
    ci_jobs = [] if no_ci else resolve_ci_selection(autopilot.ci_jobs)
    result = run_merge_gate(outcome, strategy=resolved, ci_jobs=ci_jobs, timeout=parse_duration_seconds(timeout))
    typer.echo(result.model_dump_json())
