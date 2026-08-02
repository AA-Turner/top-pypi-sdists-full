"""``pysae-ai-tools agent batch-branch`` — temp integration branch for the in-session batch.

The in-session batch skill drives :mod:`batch_branch` through this CLI (the sequential path and
the concurrency>1 Workflow both go through it):

- ``create --project X`` → cut ``staging/autopilot-batch-<ts>`` off the default branch, print its name.
- ``finalize --project X --branch B [--merge]`` → verify the branch CI (union of the repo's
  ``ci_jobs`` + ``post_merge_ci_jobs``) and, with ``--merge``, merge it into the default branch on
  green. Prints ``{"ok": bool, "merged": bool, "reason": str}``.
"""

import json
from datetime import datetime, timezone
from typing import Annotated

import typer

from .autopilot_config import load_autopilot, merge_ci_selections
from .batch_branch import create_integration_branch, finalize_integration_branch, verify_branch_ci
from .common import parse_duration_seconds

app = typer.Typer(no_args_is_help=True, help="Temp integration branch for --batch-branch")


@app.command()
def create(project: Annotated[str, typer.Option("--project")]) -> None:
    """Create the integration branch off the default branch; print its name (empty on failure)."""
    stamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d-%H%M%S")
    branch = create_integration_branch(project, stamp)
    typer.echo(branch or "")


@app.command()
def finalize(
    project: Annotated[str, typer.Option("--project")],
    branch: Annotated[str, typer.Option("--branch")],
    merge: Annotated[bool, typer.Option("--merge", help="Merge the branch into the default branch on green.")] = False,
    timeout: Annotated[str, typer.Option("--timeout")] = "30m",
) -> None:
    """Verify the branch CI (union of ci_jobs + post_merge_ci_jobs); optionally merge it on green.

    With ``--merge`` the check goes through an integration MR (``branch`` → default), so the
    pipeline exists even on MR-gated repos; without it, ``branch`` (the default branch, for the
    report-only ``--ci-at-end`` case) is checked directly.
    """
    autopilot = load_autopilot(project)
    selection = merge_ci_selections(autopilot.ci_jobs, autopilot.post_merge_ci_jobs)
    if merge:
        ok, merged, reason = finalize_integration_branch(
            project, branch, selection, merge=True, timeout=parse_duration_seconds(timeout)
        )
    else:
        ok, reason = verify_branch_ci(project, branch, selection, timeout=parse_duration_seconds(timeout))
        merged = False
    typer.echo(json.dumps({"ok": ok, "merged": merged, "reason": reason}))
