# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""CLI commands for the Project Lighthouse daily job."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated

from cyclopts import Parameter

from airbyte_ops_mcp.cli._base import App, app
from airbyte_ops_mcp.lighthouse.job import run_lighthouse

lighthouse_app = App(name="lighthouse", help="Project Lighthouse outreach job.")
app.command(lighthouse_app)


@lighthouse_app.command(name="run")
def lighthouse_run(
    run_date: Annotated[
        date | None,
        Parameter(name="--date", help="UTC fire date in YYYY-MM-DD format."),
    ] = None,
    live: Annotated[
        bool,
        Parameter(help="Enable Zendesk and Slack writes; default is dry-run."),
    ] = False,
) -> None:
    """Plan or execute the Project Lighthouse daily job."""
    target_date = run_date or (datetime.now(timezone.utc).date() - timedelta(days=1))
    result = run_lighthouse(
        target_date,
        live=live,
        plan_path=Path("lighthouse_plan.json"),
    )
    print(result.markdown)
    print(f"\nPlan written to {result.plan_path}")
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"- {error}")
        raise SystemExit(1)
