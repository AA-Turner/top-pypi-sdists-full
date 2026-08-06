from __future__ import annotations

import typing as t
import uuid
from pathlib import Path

import click

from dbt_state.cli.explainer import Explainer
from dbt_state.config import RunCacheConfig
from dbt_state.decision_logger import (
    DecisionLogger,
)
from dbt_state.grpc.client import QueryCacheGrpcClient


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit(0)
    ctx.ensure_object(dict)
    # TODO: Ideally use dbt to get the project root and log path
    # alternative is to parse the dbt project yml file to get log path
    decision_logger = DecisionLogger(
        project_root=Path.cwd(), log_path="logs", config=RunCacheConfig()
    )
    ctx.obj["decision_logger"] = decision_logger


@cli.command()
# TODO: Use dbt model selector to allow full model selection syntax that is supported by dbt
@click.option(
    "-s",
    "--select",
    type=str,
    help="Model selector to filter results by model name (Unix-style wildcards supported)",
    required=False,
)
@click.option("-v", "--verbose", is_flag=True, default=False, help="Enable more detailed output")
@click.option(
    "-l",
    "--log-file",
    type=str,
    help="Name or full path of a specific log file to explain (defaults to most recent)",
    required=False,
)
@click.pass_context
def explain(
    ctx: click.Context,
    verbose: bool,
    select: t.Optional[str] = None,
    log_file: t.Optional[str] = None,
) -> None:
    """Show cache decision explanations from the most recent dbt run"""
    decision_logger: DecisionLogger = ctx.obj["decision_logger"]
    log_files = decision_logger.logs_filepaths()

    if log_file:
        log_file_path = Path(log_file)
        if not log_file_path.is_absolute() and not log_file_path.exists():
            log_file_path = decision_logger.log_dir / log_file_path
        if not log_file_path.exists():
            raise click.ClickException(f"Log file not found: {log_file_path}")
    else:
        if not log_files:
            click.echo("No log files found.")
            return
        log_file_path = log_files[0]

    config = RunCacheConfig()
    query_cache_client = QueryCacheGrpcClient.create(
        run_cache_config=config,
        session_id=str(uuid.uuid4()),
    )

    try:
        Explainer(
            query_cache_client=query_cache_client,
            file_path=log_file_path,
            verbose=verbose,
            node_selector=select,
        ).explain()
    finally:
        query_cache_client.close()


if __name__ == "__main__":
    cli()
