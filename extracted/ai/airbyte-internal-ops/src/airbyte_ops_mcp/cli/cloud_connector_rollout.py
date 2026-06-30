# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""CLI commands for connector rollout autopilot operations.

Commands:
    airbyte-ops cloud connector rollout autopilot auto-start
    airbyte-ops cloud connector rollout autopilot auto-advance
    airbyte-ops cloud connector rollout autopilot auto-promote
    airbyte-ops cloud connector rollout autopilot auto-triage-failed
    airbyte-ops cloud connector rollout autopilot auto-rollback-failed
"""

from __future__ import annotations

from typing import Annotated

from cyclopts import Parameter
from fastmcp_extensions.cli import print_error, print_success, print_warning

from airbyte_ops_mcp.cli._base import App
from airbyte_ops_mcp.cli.cloud import _resolve_cli_cloud_auth, connector_app
from airbyte_ops_mcp.connector_ops.rollouts import (
    AutopilotResult,
    run_auto_advance,
    run_auto_promote,
    run_auto_rollback_failed,
    run_auto_start,
    run_auto_triage_failed,
)

# Hide Python-level members from pdoc
__all__: list[str] = []

# Create the rollout sub-app under connector
rollout_app = App(name="rollout", help="Connector rollout operations.")
connector_app.command(rollout_app)

# Create the autopilot sub-app under rollout
autopilot_app = App(name="autopilot", help="AutoPilot rollout orchestration commands.")
rollout_app.command(autopilot_app)


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

    for error in result.errors:
        tier_label = f" ({error.tier})" if error.tier else ""
        print_error(
            f"  {error.connector_name} {error.rc_version}{tier_label}: {error.message}"
        )


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
    _print_result(result)


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

    Finds rollouts with `automated` strategy that haven't reached their
    target percentage and advances them based on the configured strategy
    pacing (`fast`/`slow`/`default`).
    """
    auth = _resolve_cli_cloud_auth()
    result = run_auto_advance(auth=auth, connector=connector, dry_run=dry_run)
    _print_result(result)


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

    Checks the `autopilotConfig.autoPromoteStages` gate. Currently
    finalizes rollouts at ALL tier as succeeded (GA promotion).
    Cross-tier promotion (TIER_2 -> TIER_1 -> ALL) is not yet implemented.
    """
    auth = _resolve_cli_cloud_auth()
    result = run_auto_promote(auth=auth, connector=connector, dry_run=dry_run)
    _print_result(result)


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
    _print_result(result)


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
    _print_result(result)
