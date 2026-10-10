# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""MCP tools for Airbyte data team operations (the data warehouse, `airbytehq/airbyte-warehouse`).

This module exposes tools for running on-demand dbt workflows in the warehouse repository.
These tools target the analytics warehouse, not Airbyte Cloud's operational database (`prod_db_ops`).

## MCP reference

.. include:: ../../../docs/mcp-generated/data_ops.md
    :start-line: 2
"""

# NOTE: We intentionally do NOT use `from __future__ import annotations` here.
# FastMCP has issues resolving forward references when PEP 563 deferred
# annotations are used. See: https://github.com/jlowin/fastmcp/issues/905

__all__: list[str] = []

from typing import Annotated

from fastmcp import FastMCP
from fastmcp_extensions import mcp_tool, register_mcp_tools
from pydantic import Field

from airbyte_ops_mcp.mcp.github_ops import (
    TriggerCIWorkflowResult,
    trigger_ci_workflow,
)

WAREHOUSE_DBT_ON_DEMAND_WORKFLOW_FILE = "dbt-run-command.yml"


@mcp_tool(read_only=False, idempotent=False, open_world=True)
def run_bigquery_dbt_job(
    select: Annotated[
        str | None,
        Field(description="dbt `--select` value; `None` runs the whole project."),
    ] = None,
    exclude: Annotated[
        str | None,
        Field(description="dbt `--exclude` value."),
    ] = None,
    seed: Annotated[
        bool,
        Field(description="Run `dbt seed` for all seeds; selectors are ignored."),
    ] = False,
    run: Annotated[bool, Field(description="Run selected dbt models.")] = True,
    snapshot: Annotated[
        bool,
        Field(description="Run selected dbt snapshots."),
    ] = False,
    test: Annotated[
        bool,
        Field(description="Run selected dbt tests."),
    ] = False,
    full_refresh: Annotated[
        bool,
        Field(
            description="Pass `--full-refresh` to seed and run, rebuilding "
            "incremental models from scratch (e.g. after adding a column)."
        ),
    ] = False,
    pr: Annotated[
        int | None,
        Field(
            description="Optional airbyte-warehouse PR number. When set, runs that "
            "PR's dbt code into the non-prod `airbyte-data-dev.dbt_run_pr_<N>_*` "
            "datasets (unselected upstream models are deferred to prod). When "
            "omitted, runs `main` against prod."
        ),
    ] = None,
    wait_for_completion: Annotated[
        bool,
        Field(
            description="Wait for the workflow to complete before returning. "
            "Set `False` to return after dispatch."
        ),
    ] = True,
    max_wait_seconds: Annotated[
        int,
        Field(description="Maximum time to wait for workflow completion in seconds."),
    ] = 600,
) -> TriggerCIWorkflowResult:
    """Run dbt on demand in the `airbytehq/airbyte-warehouse` repository.

    Uses the `dbt Run (On Demand)` GitHub Actions workflow on `main`. Without `pr`,
    it runs `main` against production. With `pr`, it checks out that PR's dbt code
    and runs into non-prod `airbyte-data-dev.dbt_run_pr_<N>_*` datasets, deferring
    unselected upstream models to production. Steps run in order: seed → run →
    snapshot → test. `seed` runs all seeds; `select` and `exclude` are ignored for
    seeds.

    `full_refresh` adds `--full-refresh` to seed and run.

    Requires a token with `actions:write` on `airbyte-warehouse`.
    """
    if pr is not None and pr <= 0:
        raise ValueError("PR number must be a positive integer.")

    if not (seed or run or snapshot or test):
        raise ValueError(
            "At least one of seed, run, snapshot, or test must be enabled."
        )

    inputs = {
        "seed": str(seed).lower(),
        "run": str(run).lower(),
        "snapshot": str(snapshot).lower(),
        "test": str(test).lower(),
        "full_refresh": str(full_refresh).lower(),
    }
    if pr is not None:
        inputs["pr"] = str(pr)
    if select and select.strip():
        inputs["select"] = select
    if exclude and exclude.strip():
        inputs["exclude"] = exclude

    return trigger_ci_workflow(
        owner="airbytehq",
        repo="airbyte-warehouse",
        workflow_file=WAREHOUSE_DBT_ON_DEMAND_WORKFLOW_FILE,
        workflow_definition_ref="main",
        inputs=inputs,
        wait_for_completion=wait_for_completion,
        max_wait_seconds=max_wait_seconds,
    )


def register_data_ops_tools(app: FastMCP) -> None:
    """Register data_ops tools with the FastMCP app."""
    register_mcp_tools(app, mcp_module=__name__)
