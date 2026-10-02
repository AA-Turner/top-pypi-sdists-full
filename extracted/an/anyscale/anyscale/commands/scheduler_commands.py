from datetime import datetime
from typing import List, Optional

import click

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import (
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    OutputFormat,
    print_output,
)
from anyscale.commands.util import AnyscaleCommand
from anyscale.scheduler.models import (
    MatchExpression,
    Operator,
    ResourceFlavor,
    SchedulerConfig,
    SchedulerConfigVersion,
    SchedulerConfigVersionSummary,
)
from anyscale.util import validate_non_negative_arg


log = BlockLogger()


_CONFIRMATION_PHRASE = "change config"

_NO_CATCH_ALL_RULE_WARNING = (
    "No catch-all scheduling rule is configured (a rule with no selector "
    "matches every workload). Workloads that do not match any scheduling "
    "rule will be rejected and fail."
)


@click.group(
    "scheduler",
    help="Manage the Anyscale Global Resource Scheduler.",
)
def scheduler_cli() -> None:
    pass


@scheduler_cli.group("config", help="Manage scheduler configurations.")
def config_cli() -> None:
    pass


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Apply a scheduler config from a YAML file.",
            command="anyscale scheduler config apply -f scheduler-config.yaml",
            output_raw=command_examples.SCHEDULER_CONFIG_APPLY_EXAMPLE,
        ),
    ],
)
@config_cli.command(
    name="apply",
    short_help="Apply a scheduler config, creating a new active version.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "-f",
    "--config-file",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to a YAML file containing the scheduler config.",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Skip asking for confirmation.",
)
def apply(config_file: str, yes: bool) -> None:
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

    if _should_warn_no_catch_all_rule(config):
        log.warning(_NO_CATCH_ALL_RULE_WARNING)

    if not yes:
        _confirm_config_change("apply")

    try:
        with log.spinner("Applying scheduler config..."):
            version: int = anyscale.scheduler.apply_config(config=config)
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    log.info(f"Applied scheduler config (version {version}).")


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Roll back to scheduler config version 2.",
            command="anyscale scheduler config rollback --version 2",
            output_raw=command_examples.SCHEDULER_CONFIG_ROLLBACK_EXAMPLE,
        ),
    ],
)
@config_cli.command(
    name="rollback",
    short_help="Roll back to a scheduler config version, creating a new active version.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--version",
    "version",
    required=True,
    type=int,
    help="Version whose config is applied as the new active version.",
)
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    default=False,
    help="Skip asking for confirmation.",
)
def rollback(version: int, yes: bool) -> None:
    """Roll back to a scheduler config version, creating a new active version.

    The config of `--version N` is applied as a new version. Version N stays in
    history unchanged, so `config list` keeps every version and a rollback can
    itself be rolled back.
    """
    try:
        with log.spinner(_get_spinner_text(version)):
            source: SchedulerConfigVersion = anyscale.scheduler.get_config(version=version)
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    if _should_warn_no_catch_all_rule(source.config):
        log.warning(_NO_CATCH_ALL_RULE_WARNING)

    if not yes:
        _confirm_config_change("roll back")

    try:
        with log.spinner(f"Rolling back to scheduler config version {version}..."):
            new_version: int = anyscale.scheduler.rollback_config(version=version)
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    log.info(
        f"Rolled back to scheduler config version {version} (applied as version {new_version})."
    )


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.YAML, OutputFormat.JSON],
    examples=[
        CommandExample(
            description="Get the active scheduler config.",
            command="anyscale scheduler config get",
            output_instance=lambda: SchedulerConfigVersion(
                version=3,
                is_active=True,
                created_at=datetime(2026, 4, 25, 10, 0, 0),
                creator_id="usr_abc123",
                config=SchedulerConfig(
                    resource_flavors=[
                        ResourceFlavor(
                            name="spot",
                            selector=[
                                MatchExpression(
                                    key="market", operator=Operator.IN, values=["spot"]
                                )
                            ],
                        )
                    ],
                ),
            ),
        ),
    ],
    output_schema=SchedulerConfigVersion,
)
@config_cli.command(
    name="get",
    short_help="Get the active scheduler config, or a specific version.",
    cls=AnyscaleCommand,
    is_beta=True,
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
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice([OutputFormat.YAML.value, OutputFormat.JSON.value]),
    default=OutputFormat.YAML.value,
    show_default=True,
    help="Output format for the result.",
)
def get(version: Optional[int], output_format: str) -> None:
    """Get the active scheduler config, or a specific version."""
    try:
        with log.spinner(_get_spinner_text(version)):
            result: SchedulerConfigVersion = anyscale.scheduler.get_config(
                version=version,
            )
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    print_output(result, output_format)


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TABLE, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="List scheduler config versions.",
            command="anyscale scheduler config list",
            output_instance=lambda: [
                SchedulerConfigVersionSummary(
                    version=3,
                    created_at=datetime(2026, 4, 25, 10, 0, 0),
                    creator_id="usr_abc123",
                ),
                SchedulerConfigVersionSummary(
                    version=2,
                    created_at=datetime(2026, 4, 20, 8, 30, 0),
                    creator_id="usr_abc123",
                ),
            ],
        ),
    ],
    output_schema=SchedulerConfigVersionSummary,
)
@config_cli.command(
    name="list",
    short_help="List scheduler config versions, newest first.",
    cls=AnyscaleCommand,
    is_beta=True,
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
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice(
        [OutputFormat.TABLE.value, OutputFormat.JSON.value, OutputFormat.YAML.value]
    ),
    default=OutputFormat.TABLE.value,
    show_default=True,
    help="Output format for the result.",
)
def list_versions(
    max_items: int,
    output_format: str,
) -> None:  # noqa: A001
    """List scheduler config versions, newest first.

    Use `config get --version N` to fetch the full config for a version.
    """
    try:
        with log.spinner("Fetching scheduler config versions..."):
            results: List[SchedulerConfigVersionSummary] = anyscale.scheduler.list_config_versions(
                max_items=max_items,
            )
    except (ValueError, RuntimeError) as e:
        raise click.ClickException(str(e)) from None

    if not results and output_format == OutputFormat.TABLE.value:
        log.info("No scheduler config versions found.")
        return

    print_output(results, output_format)


# ---- helpers ----


def _confirm_config_change(action: str) -> None:
    """Gate an org-wide config change behind the typed confirmation phrase.

    `action` completes the sentence "You must type ... to <action>".
    """
    click.echo(
        "\nOnce applied, all workloads in your organization will be admitted, "
        "scheduled, run, or rejected according to this new configuration.\n",
        err=True,
    )
    typed = click.prompt(
        f'Type "{_CONFIRMATION_PHRASE}" to proceed, or press Ctrl+C to cancel',
        type=str,
        # Click re-prompts forever on a blank line unless a default is set.
        default="",
        show_default=False,
        err=True,
    )
    if typed.strip() != _CONFIRMATION_PHRASE:
        raise click.ClickException(
            f'You must type "{_CONFIRMATION_PHRASE}" to {action}. Nothing was applied.'
        )


def _should_warn_no_catch_all_rule(config: SchedulerConfig) -> bool:
    """Whether to warn that the config declares no catch-all scheduling rule.

    A rule with no selector matches every workload, so one anywhere in the list
    means nothing can go unmatched. A config declaring no rules at all admits
    everything, so there is nothing to warn about. Mirrors the console's
    condition.
    """
    rules = config.scheduling_rules
    if not rules:
        return False
    return all(r.selector for r in rules)


def _get_spinner_text(version: Optional[int]) -> str:
    return (
        f"Fetching scheduler config version {version}..."
        if version is not None
        else "Fetching active scheduler config..."
    )
