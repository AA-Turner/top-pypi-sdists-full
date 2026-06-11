from datetime import datetime
import json as json_module
from typing import Any, Dict, List, Optional

import click
import tabulate
import yaml

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand
from anyscale.scheduler.models import (
    SchedulerConfig,
    SchedulerConfigVersion,
    SchedulerConfigVersionSummary,
)
from anyscale.util import validate_non_negative_arg


log = BlockLogger()


_OUTPUT_CHOICES_FULL = ["table", "json", "yaml"]
_OUTPUT_CHOICES_SINGLE = ["json", "yaml"]


@click.group(
    "scheduler", help="Manage the Anyscale Global Resource Scheduler.", hidden=True,
)
def scheduler_cli() -> None:
    pass


@scheduler_cli.group("config", help="Manage scheduler configurations.")
def config_cli() -> None:
    pass


@config_cli.command(
    name="apply",
    cls=AnyscaleCommand,
    is_beta=True,
    example=command_examples.SCHEDULER_CONFIG_APPLY_EXAMPLE,
)
@click.option(
    "-f",
    "--config-file",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to a YAML file containing the scheduler config.",
)
def apply(config_file: str) -> None:
    """Apply a scheduler config, creating a new active version.

    The previous active version becomes inactive but remains queryable with
    `config list` and `config get --version N`.
    """
    try:
        config = SchedulerConfig.from_yaml(config_file)
    except Exception as e:  # noqa: BLE001 - YAML parse / schema validation surfaces here
        raise click.ClickException(
            f"Failed to load scheduler config from '{config_file}': {e}"
        ) from None

    try:
        with log.spinner("Applying scheduler config..."):
            version: int = anyscale.scheduler.apply_config(config=config)
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    log.info(f"Applied scheduler config (version {version}).")


@config_cli.command(
    name="get",
    cls=AnyscaleCommand,
    is_beta=True,
    example=command_examples.SCHEDULER_CONFIG_GET_EXAMPLE,
)
@click.option(
    "--version",
    "version",
    required=False,
    default=None,
    type=int,
    help="Version to fetch. Omit to fetch the active config.",
)
@click.option(
    "-o",
    "--output",
    "output",
    type=click.Choice(_OUTPUT_CHOICES_SINGLE, case_sensitive=False),
    default="yaml",
    show_default=True,
    help="Output format.",
)
def get(version: Optional[int], output: str) -> None:
    """Get the active scheduler config, or a specific version."""
    try:
        with log.spinner(_get_spinner_text(version)):
            result: SchedulerConfigVersion = anyscale.scheduler.get_config(
                version=version,
            )
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    payload = _version_to_dict(result)
    click.echo(_render(payload, output))


@config_cli.command(
    name="list",
    cls=AnyscaleCommand,
    is_beta=True,
    example=command_examples.SCHEDULER_CONFIG_LIST_EXAMPLE,
)
@click.option(
    "--max-items",
    required=False,
    default=10,
    type=int,
    show_default=True,
    callback=validate_non_negative_arg,
    help="Maximum number of versions to return.",
)
@click.option(
    "-o",
    "--output",
    "output",
    type=click.Choice(_OUTPUT_CHOICES_FULL, case_sensitive=False),
    default="table",
    show_default=True,
    help="Output format.",
)
def list_versions(max_items: int, output: str,) -> None:  # noqa: A001
    """List scheduler config versions, newest first.

    Use `config get --version N` to fetch the full config for a version.
    """
    try:
        with log.spinner("Fetching scheduler config versions..."):
            results: List[
                SchedulerConfigVersionSummary
            ] = anyscale.scheduler.list_config_versions(max_items=max_items,)
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    if output == "table":
        click.echo(_render_versions_table(results))
        return

    payload = [_summary_to_dict(s) for s in results]
    click.echo(_render(payload, output))


# ---- helpers ----


def _get_spinner_text(version: Optional[int]) -> str:
    return (
        f"Fetching scheduler config version {version}..."
        if version is not None
        else "Fetching active scheduler config..."
    )


def _version_to_dict(v: SchedulerConfigVersion) -> Dict[str, Any]:
    return {
        "version": v.version,
        "is_active": v.is_active,
        "created_at": _iso(v.created_at),
        "creator_id": v.creator_id,
        "config": v.config.to_dict(exclude_none=True),
    }


def _summary_to_dict(s: SchedulerConfigVersionSummary) -> Dict[str, Any]:
    return {
        "version": s.version,
        "created_at": _iso(s.created_at),
    }


def _iso(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _render(payload: Any, output: str) -> str:
    if output == "json":
        return json_module.dumps(payload, indent=2, sort_keys=False, default=str)
    if output == "yaml":
        return yaml.safe_dump(payload, sort_keys=False).rstrip()
    raise click.UsageError(f"Unsupported output format: {output}")


def _render_versions_table(results: List[SchedulerConfigVersionSummary]) -> str:
    if not results:
        return "No scheduler config versions found."
    rows = [[s.version, _iso(s.created_at)] for s in results]
    return tabulate.tabulate(rows, headers=["VERSION", "CREATED AT"], tablefmt="plain",)
