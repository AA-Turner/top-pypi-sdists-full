# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""CLI commands for connector rollout operations.

Commands (autopilot subcommands are listed in cron execution order):
    airbyte-ops cloud connector rollout list
    airbyte-ops cloud connector rollout autopilot auto-triage-failed
    airbyte-ops cloud connector rollout autopilot auto-rollback-failed
    airbyte-ops cloud connector rollout autopilot auto-close
    airbyte-ops cloud connector rollout autopilot auto-start
    airbyte-ops cloud connector rollout autopilot auto-advance
    airbyte-ops cloud connector rollout autopilot auto-promote
"""

from __future__ import annotations

import os
import sys
from typing import Annotated

from cyclopts import Parameter
from fastmcp_extensions.cli import (
    print_error,
    print_json,
    print_success,
    print_warning,
)

from airbyte_ops_mcp.cli._base import App
from airbyte_ops_mcp.cli.cloud import _resolve_cli_cloud_auth, connector_app
from airbyte_ops_mcp.connector_ops.rollouts import (
    AutopilotResult,
    run_auto_advance,
    run_auto_close,
    run_auto_promote,
    run_auto_rollback_failed,
    run_auto_start,
    run_auto_triage_failed,
)
from airbyte_ops_mcp.connector_ops.rollouts.audit import post_autopilot_audit
from airbyte_ops_mcp.prod_db_access.queries import query_connector_rollouts
from airbyte_ops_mcp.regression_tests.ci_output import write_github_summary

# Hide Python-level members from pdoc
__all__: list[str] = []

# Create the rollout sub-app under connector
rollout_app = App(name="rollout", help="Connector rollout operations.")
connector_app.command(rollout_app)

# Create the autopilot sub-app under rollout
autopilot_app = App(name="autopilot", help="AutoPilot rollout orchestration commands.")
rollout_app.command(autopilot_app)


@rollout_app.command(name="list")
def rollout_list(
    *,
    include_inactive: Annotated[
        bool,
        Parameter(
            help="Include terminal (canceled/succeeded/errored) rollouts. Requires --limit.",
        ),
    ] = False,
    limit: Annotated[
        int,
        Parameter(
            help="Maximum number of rollouts to return. Required when --include-inactive is set.",
        ),
    ] = 0,
) -> None:
    """List connector rollouts from the production database."""
    if include_inactive and limit == 0:
        print(
            "Error: --limit is required when --include-inactive is set.",
            file=sys.stderr,
        )
        sys.exit(1)

    rows = query_connector_rollouts(
        active_only=not include_inactive,
        limit=limit if limit > 0 else None,
    )
    # Format output as a list of dicts with the most relevant fields
    results = []
    for row in rows:
        docker_repo = row.get("rc_docker_repository", "")
        connector_name = (
            docker_repo.split("/", 1)[1] if "/" in docker_repo else docker_repo
        )
        results.append(
            {
                "connector": connector_name,
                "rollout_id": str(row["rollout_id"]),
                "actor_definition_id": str(row["actor_definition_id"]),
                "state": row["state"],
                "version": row.get("rc_docker_image_tag"),
                "current_target_rollout_pct": row.get("current_target_rollout_pct"),
                "created_at": str(row["created_at"]) if row.get("created_at") else None,
                "updated_at": str(row["updated_at"]) if row.get("updated_at") else None,
            }
        )
    print_json(results)


def _print_result(result: AutopilotResult) -> None:
    """Print an autopilot result summary to the console."""
    print_success(result.summary)

    for action in result.actions:
        prefix = "[DRY RUN] " if result.dry_run else ""
        tier_label = f" ({action.tier})" if action.tier else ""
        print_success(
            f"  {prefix}{action.connector_name} {action.rc_version}{tier_label}: {action.message}"
        )

    for skip in result.skipped:
        tier_label = f" ({skip.tier})" if skip.tier else ""
        print_warning(
            f"  {skip.connector_name} {skip.rc_version}{tier_label}: {skip.message}"
        )

    for warning in result.warnings:
        tier_label = f" ({warning.tier})" if warning.tier else ""
        print_warning(
            f"  {warning.connector_name} {warning.rc_version}{tier_label}: "
            f"{warning.message}"
        )

    for hold in result.holds:
        tier_label = f" ({hold.tier})" if hold.tier else ""
        print_warning(
            f"  {hold.connector_name} {hold.rc_version}{tier_label}: {hold.message}"
        )

    for error in result.errors:
        tier_label = f" ({error.tier})" if error.tier else ""
        print_error(
            f"  {error.connector_name} {error.rc_version}{tier_label}: {error.message}"
        )


def _render_step_summary(result: AutopilotResult) -> str:
    """Render the console result as a Markdown GitHub Step Summary."""
    sections = [
        ("Actions", result.actions),
        ("Skipped", result.skipped),
        ("Warnings", result.warnings),
        ("Holds", result.holds),
        ("Errors", result.errors),
    ]
    lines = [
        f"## Rollout AutoPilot: `{result.command}`",
        "",
        f"**Summary:** {result.summary}",
        "",
    ]
    for label, entries in sections:
        lines.extend([f"### {label} ({len(entries)})", ""])
        if not entries:
            lines.append("_None._")
        else:
            for entry in entries:
                tier = f" ({entry.tier})" if entry.tier else ""
                lines.append(
                    f"- `{entry.connector_name}` `{entry.rc_version}`{tier}: "
                    f"{entry.message}"
                )
        lines.append("")
    return "\n".join(lines)


def _write_step_summary(result: AutopilotResult) -> None:
    """Write the AutoPilot result to the GitHub Step Summary when configured."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    try:
        write_github_summary(_render_step_summary(result))
    except OSError as exc:
        print_warning(f"Could not write GitHub Step Summary: {exc}")


def _present_result(result: AutopilotResult) -> None:
    """Present an AutoPilot result on all configured output surfaces."""
    _print_result(result)
    _write_step_summary(result)
    post_autopilot_audit(result)


@autopilot_app.command(name="auto-start")
def auto_start(
    connector: Annotated[
        str | None,
        Parameter(
            help="Filter to a specific connector by canonical name (e.g., 'source-github')."
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        Parameter(help="Preview actions without executing them."),
    ] = False,
) -> None:
    """Start INITIALIZED rollouts that have autopilot auto-start enabled.

    Queries the prod DB for rollouts in `initialized` state, checks the
    connector's `autopilotConfig.autoStart` gate, and starts eligible
    rollouts via the Cloud Config API.
    """
    auth = _resolve_cli_cloud_auth()
    result = run_auto_start(auth=auth, connector=connector, dry_run=dry_run)
    _present_result(result)


@autopilot_app.command(name="auto-advance")
def auto_advance(
    connector: Annotated[
        str | None,
        Parameter(
            help="Filter to a specific connector by canonical name (e.g., 'source-github')."
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        Parameter(help="Preview actions without executing them."),
    ] = False,
) -> None:
    """Advance IN_PROGRESS rollouts within their current tier.

    Advances `in_progress` rollouts that haven't reached their target
    percentage based on the configured strategy pacing
    (`fast`/`slow`/`default`).

    Also recovers `workflow_started` rollouts: a rollout confirmed to have
    zero eligible actors is finalized as `succeeded` (0-of-0 eligible is
    complete, not stuck — promoting the RC to GA) instead of being left
    wedged; one with a positive estimate is re-driven; an unavailable
    estimate is skipped for a later retry.
    """
    auth = _resolve_cli_cloud_auth()
    result = run_auto_advance(auth=auth, connector=connector, dry_run=dry_run)
    _present_result(result)


@autopilot_app.command(name="auto-promote")
def auto_promote(
    connector: Annotated[
        str | None,
        Parameter(
            help="Filter to a specific connector by canonical name (e.g., 'source-github')."
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        Parameter(help="Preview actions without executing them."),
    ] = False,
) -> None:
    """Promote rollouts when at 100% of current tier.

    Checks the `autopilotConfig.autoPromoteStages` gate, then scans the tier
    order forward for the next tier that has eligible actors and starts a
    rollout there, skipping empty intermediate tiers. If no later customer
    tier has actors (or the current tier is `ALL`), the current tier is
    finalized as `succeeded` (GA promotion).
    """
    auth = _resolve_cli_cloud_auth()
    result = run_auto_promote(auth=auth, connector=connector, dry_run=dry_run)
    _present_result(result)


@autopilot_app.command(name="auto-triage-failed")
def auto_triage_failed(
    connector: Annotated[
        str | None,
        Parameter(
            help="Filter to a specific connector by canonical name (e.g., 'source-github')."
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        Parameter(help="Preview actions without executing them."),
    ] = False,
) -> None:
    """Triage failed rollouts: log all failures, check unpin eligibility.

    Finds rollouts in `errored` or `paused` state. Logs every failure
    unconditionally. Checks safe-to-downgrade eligibility per
    `unsafeDowngrades`. Actor-level unpinning is not yet implemented.
    """
    auth = _resolve_cli_cloud_auth()
    result = run_auto_triage_failed(auth=auth, connector=connector, dry_run=dry_run)
    _present_result(result)


@autopilot_app.command(name="auto-close")
def auto_close(
    connector: Annotated[
        str | None,
        Parameter(
            help="Filter to a specific connector by canonical name (e.g., 'source-github')."
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        Parameter(help="Preview actions without executing them."),
    ] = False,
) -> None:
    """Close obsolete rollouts so only a connector's active candidate remains.

    Closes a rollout when a newer RC supersedes it, when its RC is already the
    registry GA default, or when its RC is not the highest advertised release
    candidate for the connector. Uses `retain_pins_on_cancellation=True` so
    pinned actors are left undisturbed.
    """
    auth = _resolve_cli_cloud_auth()
    result = run_auto_close(auth=auth, connector=connector, dry_run=dry_run)
    _present_result(result)


@autopilot_app.command(name="auto-rollback-failed")
def auto_rollback_failed(
    connector: Annotated[
        str | None,
        Parameter(
            help="Filter to a specific connector by canonical name (e.g., 'source-github')."
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        Parameter(help="Preview actions without executing them."),
    ] = False,
) -> None:
    """Full rollback/cancel of failed rollouts when safe to downgrade.

    Finds rollouts in `errored` state. Checks the `unsafeDowngrades` gate.
    If the version is safe to downgrade, calls `finalize_connector_rollout`
    with state `failed_rolled_back` to cancel the entire rollout.
    """
    auth = _resolve_cli_cloud_auth()
    result = run_auto_rollback_failed(auth=auth, connector=connector, dry_run=dry_run)
    _present_result(result)
