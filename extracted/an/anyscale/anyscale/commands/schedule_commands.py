from io import StringIO
import pathlib
from typing import Any, Dict, List, Optional, Tuple

import click
from rich.console import Console
from rich.table import Table
import tabulate
import yaml

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.list_util import (
    create_table,
    display_list,
    NON_INTERACTIVE_DEFAULT_MAX_ITEMS,
    validate_page_size,
)
from anyscale.commands.output_format import (
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    OutputFormat,
    print_output,
    resolve_output_format,
)
from anyscale.commands.util import AnyscaleCommand
from anyscale.controllers.schedule_controller import ScheduleController
from anyscale.schedule.models import (
    JobConfig,
    ScheduleConfig,
    ScheduleSortField,
    ScheduleState,
    ScheduleStatus,
)
from anyscale.util import get_endpoint, validate_non_negative_arg


log = BlockLogger()  # CLI Logger


def _parse_sort_option(sort_str: Optional[str]) -> Tuple[Optional[str], str]:
    """Parse sort string like '-created_at' into (field, order).

    Args:
        sort_str: Sort option string. Prefix with '-' for descending order.

    Returns:
        Tuple of (sort_field, sort_order) where sort_order is "ASC" or "DESC".

    Raises:
        click.BadParameter: If the sort field is not valid.
    """
    if not sort_str:
        return None, "ASC"

    # Build case-insensitive map of allowed fields
    allowed = {f.value.lower(): f.value for f in ScheduleSortField.__members__.values()}

    # Detect leading '-' for descending
    if sort_str.startswith("-"):
        raw = sort_str[1:]
        order = "DESC"
    else:
        raw = sort_str
        order = "ASC"

    key = raw.lower()
    if key not in allowed:
        raise click.BadParameter(
            f"Invalid sort field '{raw}'. Allowed: {', '.join(allowed.values())}",
            param_hint="'--sort'",
        )
    return allowed[key], order


@click.group("schedule", help="Create and manage Anyscale Schedules.")
def schedule_cli() -> None:
    pass


def _read_identifiers_from_config_file(path: str):
    """Read the 'name', 'cloud', and 'project' properties from the config file at `path`.

    Return the identifers as a ScheduleIdentifiers object.
    """
    if not pathlib.Path(path).is_file():
        raise click.ClickException(f"Config file not found at path: '{path}'.")

    with open(path) as f:
        config = yaml.safe_load(f)

    if config is None or "job_config" not in config:
        raise click.ClickException(
            f"No 'job_config' property found in config file '{path}'."
        )

    job_config = config.get("job_config")
    name = job_config.get("name", None)
    cloud = job_config.get("cloud", None)
    project = job_config.get("project", None)

    return name, cloud, project


def _validate_schedule_identifiers(
    name: Optional[str], id: Optional[str], config_file: Optional[str]  # noqa: A002
):
    num_passed = sum(val is not None for val in [name, id, config_file])
    if num_passed == 0:
        raise click.ClickException(
            "One of '--name', '--id', or '--config-file' must be provided."
        )

    if num_passed > 1:
        raise click.ClickException(
            "Only one of '--name', '--id', and '--config-file' can be provided."
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Apply a schedule from a YAML config file.",
            command="anyscale schedule apply -n my-schedule -f my-schedule.yaml",
            output_raw=command_examples.SCHEDULE_APPLY_EXAMPLE,
        ),
    ],
)
@schedule_cli.command(
    name="apply", short_help="Create or update a schedule.", cls=AnyscaleCommand,
)
@click.option(
    "--config-file",
    "-f",
    required=True,
    type=str,
    help="Path to a YAML config file to use for this schedule. Command-line flags will overwrite values read from the file.",
)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
def apply(config_file: str, name: Optional[str],) -> None:
    """Create or update a schedule.

    The schedule should be specified in a YAML config file.
    """
    if not pathlib.Path(config_file).is_file():
        raise click.ClickException(f"Schedule config file '{config_file}' not found.")

    config = ScheduleConfig.from_yaml(config_file)

    if name is not None:
        assert isinstance(config.job_config, JobConfig)
        config = config.options(job_config=config.job_config.options(name=name),)

    log.info(f"Applying schedule with config {config}.")
    anyscale.schedule.apply(config)


def _create_schedules_table_v2(is_first: bool) -> Table:
    """Create a Rich Table for displaying schedules in v2 mode.

    Args:
        is_first: Whether this is the first page (controls header display).

    Returns:
        Rich Table configured for schedule display.
    """
    columns = [
        ("ID", "cyan", True),
        ("Name", None, False),
        ("State", "green", False),
        ("Cron Expression", None, False),
        ("Timezone", None, False),
        ("Project", None, False),
    ]
    return create_table(columns, is_first)


def _format_schedule_row_v2(schedule: ScheduleStatus) -> Dict[str, Any]:
    """Format a ScheduleStatus for table row or JSON output.

    Args:
        schedule: The ScheduleStatus object to format.

    Returns:
        Dictionary with formatted schedule data.
    """
    return {
        "id": schedule.id or "",
        "name": schedule.name or "",
        "state": str(schedule.state) if schedule.state else "",
        "cron_expression": schedule.config.cron_expression if schedule.config else "",
        "timezone": schedule.config.timezone if schedule.config else "",
        "project": schedule.config.job_config.project
        if schedule.config and schedule.config.job_config
        else "",
    }


def _display_schedules_table(schedules: List[ScheduleStatus]) -> None:
    """Display schedules in a tabulated format."""
    if not schedules:
        print("No schedules found.")
        return

    schedules_table = [
        [
            schedule.name,
            schedule.id,
            str(schedule.state) if schedule.state else None,
            schedule.config.cron_expression if schedule.config else None,
            schedule.config.timezone if schedule.config else None,
        ]
        for schedule in schedules
    ]

    table = tabulate.tabulate(
        schedules_table,
        headers=["NAME", "ID", "STATE", "CRON", "TIMEZONE"],
        tablefmt="plain",
    )
    print(f"SCHEDULES:\n{table}")

    endpoint = get_endpoint("")
    print(f"\nView your schedules at: {endpoint}schedules")


def _print_schedule_list_diagnostics(  # noqa: PLR0913
    stderr: Console,
    name: Optional[str],
    schedule_id: Optional[str],
    project: Optional[str],
    cloud: Optional[str],
    creator_id: Optional[str],
    include_all_users: bool,
    interactive: bool,
    page_size: int,
    effective_max: Optional[int],
    sort: Optional[str] = None,
) -> None:
    """Prints diagnostic information for the list command."""
    stderr.print("[bold]Listing schedules with:[/]")
    stderr.print(f"• name            = {name or '<any>'}")
    stderr.print(f"• id              = {schedule_id or '<any>'}")
    stderr.print(f"• project         = {project or '<any>'}")
    stderr.print(f"• cloud           = {cloud or '<any>'}")
    stderr.print(f"• creator_id      = {creator_id or '<any>'}")
    stderr.print(f"• include_all     = {include_all_users}")
    stderr.print(f"• sort            = {sort or '-created_at'}")
    stderr.print(f"• mode            = {'interactive' if interactive else 'batch'}")
    stderr.print(f"• per-page limit  = {page_size}")
    stderr.print(f"• max-items total = {effective_max if effective_max else 'all'}")
    stderr.print(f"\nView your Schedules in the UI at {get_endpoint('/schedules')}\n")


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    # TODO(MLDX-1486): flip to [TEXT, JSON] when -o is unhidden.
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="List schedules matching a name.",
            command="anyscale schedule list --v2 -n my-schedule",
            output_raw=command_examples.SCHEDULE_LIST_EXAMPLE,
            output_instance=[
                {
                    "id": "cronjob_vrjrbwcnfjjid7fsld3sfkn8jz",
                    "name": "my-schedule",
                    "state": "ENABLED",
                    "cron_expression": "0 0 * * * *",
                    "timezone": "UTC",
                    "project": "default",
                }
            ],
        ),
    ],
)
@schedule_cli.command(
    name="list", short_help="List schedules.", cls=AnyscaleCommand,
)
@click.option(
    "--v2",
    is_flag=True,
    default=False,
    help="[RECOMMENDED] Enable extended filtering options. Needs migration to match return values.",
)
@click.option(
    "--name",
    "-n",
    required=False,
    default=None,
    help="Filter by the name of the schedule.",
)
@click.option("--id", "-i", required=False, default=None, help="Id of the schedule.")
@click.option(
    "--project",
    required=False,
    default=None,
    help="The named Anyscale Project for the schedule. If not provided, the organization default will be used (or, if running in a workspace, the project of the workspace). Only with --v2 flag.",
)
@click.option(
    "--cloud",
    required=False,
    default=None,
    help="The named Anyscale Cloud for the schedule. If not provided, the organization default will be used (or,if running in a workspace, the cloud of the workspace). Only with --v2 flag.",
)
@click.option(
    "--creator-id",
    required=False,
    default=None,
    help="Filter by creator ID. Only with --v2 flag.",
)
@click.option(
    "--max-items",
    type=int,
    callback=validate_non_negative_arg,
    help="Max total items (only with --no-interactive).",
)
@click.option(
    "--page-size",
    required=False,
    default=None,
    type=int,
    help="Number of items per page (1-50). Only with --v2.",
    callback=validate_page_size,
)
@click.option(
    "--sort",
    required=False,
    default=None,
    help=(
        "Sort by field. Prefix with '-' for descending order. Defaults to -created_at. "
        f"Allowed: {', '.join(f.value for f in ScheduleSortField.__members__.values())}. "
        "Only with --v2."
    ),
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice([OutputFormat.TEXT.value, OutputFormat.JSON.value]),
    default=OutputFormat.TEXT.value,
    show_default=True,
    hidden=True,
    help="Output format for the result. Only with --v2.",
)
@click.option(
    "--json",
    "-j",
    "json_output",
    is_flag=True,
    default=False,
    help="Output results as JSON. Only with --v2.",
)
@click.option(
    "--interactive/--no-interactive",
    default=True,
    show_default=True,
    help="Enable interactive pagination. Only with --v2.",
)
@click.option(
    "--include-all-users/--only-mine",
    default=False,
    help="Include schedules from all users. Only with --v2.",
)
def list(  # noqa: A001 PLR0913
    v2: bool,
    name: Optional[str] = None,
    id: Optional[str] = None,  # noqa: A002
    project: Optional[str] = None,
    cloud: Optional[str] = None,
    creator_id: Optional[str] = None,
    max_items: Optional[int] = None,
    page_size: Optional[int] = None,
    sort: Optional[str] = None,
    output_format: str = OutputFormat.TEXT.value,
    json_output: bool = False,
    interactive: bool = True,
    include_all_users: bool = False,
) -> None:
    """List schedules.

    You can optionally filter schedules by name, project, cloud, or creator.
    """
    json_output = json_output or output_format == OutputFormat.JSON.value

    if v2:
        # Validate max_items only allowed with --no-interactive (v2 only)
        if max_items is not None and interactive:
            raise click.UsageError("--max-items only allowed with --no-interactive")
        # New SDK path with pagination and output options

        # Apply defaults for v2-only options
        effective_page_size = page_size if page_size is not None else 10
        effective_sort = sort if sort is not None else "-created_at"

        # Parse sort option
        sort_field, sort_order = _parse_sort_option(effective_sort)

        # Compute effective max_items for non-interactive mode
        effective_max = max_items
        if not interactive and effective_max is None:
            effective_max = NON_INTERACTIVE_DEFAULT_MAX_ITEMS

        # Print diagnostics header (not in JSON mode)
        if not json_output:
            stderr = Console(stderr=True)
            _print_schedule_list_diagnostics(
                stderr=stderr,
                name=name,
                schedule_id=id,
                project=project,
                cloud=cloud,
                creator_id=creator_id,
                include_all_users=include_all_users,
                interactive=interactive,
                page_size=effective_page_size,
                effective_max=effective_max if not interactive else None,
                sort=effective_sort,
            )

        iterator = anyscale.schedule.list(
            name=name,
            schedule_id=id,
            project=project,
            cloud=cloud,
            creator_id=creator_id,
            include_all_users=include_all_users,
            page_size=effective_page_size,
            max_items=effective_max if not interactive else None,
            sort_field=sort_field,
            sort_order=sort_order,
        )

        console = Console()
        total = display_list(
            iterator=iterator,
            item_formatter=_format_schedule_row_v2,
            table_creator=_create_schedules_table_v2,
            json_output=json_output,
            page_size=effective_page_size,
            interactive=interactive,
            max_items=effective_max if not interactive else None,
            console=console,
        )
        if not json_output:
            if total:
                stderr.print(f"\nFetched {total} schedule(s).")
            else:
                stderr.print("\nNo schedules found.")
    else:
        # Legacy path with deprecation warning
        # Check if v2-only options are being used without --v2
        if any(
            [
                project,
                cloud,
                creator_id,
                max_items is not None,
                page_size is not None,
                sort is not None,
                json_output,
                include_all_users,
                not interactive,
            ]
        ):
            click.echo(
                "ERROR: Options --project, --cloud, --creator-id, --max-items, "
                "--page-size, --sort, --json, --include-all-users, and --no-interactive require --v2 flag.\n"
                "Use: anyscale schedule list --v2 [options]",
                err=True,
            )
            raise click.exceptions.Exit(1)

        job_controller = ScheduleController()
        job_controller.list(name=name, id=id)


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Pause a schedule by name.",
            command="anyscale schedule pause -n my-schedule",
            output_raw=command_examples.SCHEDULE_PAUSE_EXAMPLE,
        ),
    ],
)
@schedule_cli.command(
    name="pause", short_help="Pause a schedule.", cls=AnyscaleCommand,
)
@click.option(
    "--config-file",
    "-f",
    required=False,
    type=str,
    help="Path to a YAML config file to use for this schedule.",
)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
@click.option("--id", "-i", required=False, default=None, help="Id of the schedule.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The named Anyscale Cloud for the schedule. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the schedule. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
def pause(
    config_file: str, name: str, cloud: str, project: str, id: str  # noqa: A002
) -> None:
    """Pause a Schedule.

    You can pause a schedule by config file, name, or id.

    To specify the schedule by name, use the --name flag. You can specify the cloud with --cloud and the project with --project.

    To specify the schedule by id, use the --id flag.

    To specify the schedule by config file, use --config-file. Ensure that name and optionally cloud and project are specified in the
    config file's job config.
    """
    _validate_schedule_identifiers(name=name, id=id, config_file=config_file)

    if id is not None:
        anyscale.schedule.set_state(id=id, state=ScheduleState.DISABLED)
    else:
        if config_file is not None:
            name, cloud, project = _read_identifiers_from_config_file(config_file)

        anyscale.schedule.set_state(
            name=name, cloud=cloud, project=project, state=ScheduleState.DISABLED
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Resume a schedule by name.",
            command="anyscale schedule resume -n my-schedule",
            output_raw=command_examples.SCHEDULE_RESUME_EXAMPLE,
        ),
    ],
)
@schedule_cli.command(
    name="resume", short_help="Resume a paused schedule.", cls=AnyscaleCommand,
)
@click.option(
    "--config-file",
    "-f",
    required=False,
    type=str,
    help="Path to a YAML config file to use for this schedule.",
)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
@click.option("--id", "-i", required=False, default=None, help="Id of the schedule.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The named Anyscale Cloud for the schedule. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the schedule. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
def resume(
    config_file: str, name: str, cloud: str, project: str, id: str  # noqa: A002
) -> None:
    """Resume a schedule.

    You can resume a schedule by config file, name, or id.

    To specify the schedule by name, use the --name flag. You can specify the cloud with --cloud and the project with --project.

    To specify the schedule by id, use the --id flag.

    To specify the schedule by config file, use --config-file. Ensure that name and optionally cloud and project are specified in the
    config file's job config.
    """
    _validate_schedule_identifiers(name=name, id=id, config_file=config_file)

    if id is not None:
        anyscale.schedule.set_state(id=id, state=ScheduleState.ENABLED)
    else:
        if config_file is not None:
            name, cloud, project = _read_identifiers_from_config_file(config_file)

        anyscale.schedule.set_state(
            name=name, cloud=cloud, project=project, state=ScheduleState.ENABLED
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    # TODO(MLDX-1486): flip to all OutputFormat values when -o is unhidden.
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Query the status of a schedule by name.",
            command="anyscale schedule status -n my-schedule",
            output_raw=command_examples.SCHEDULE_STATUS_EXAMPLE,
            output_instance=lambda: ScheduleStatus(
                id="cronjob_vrjrbwcnfjjid7fsld3sfkn8jz",
                name="my-schedule",
                state=ScheduleState.ENABLED,
                config=ScheduleConfig(
                    job_config=JobConfig(
                        name="my-schedule", entrypoint="python main.py"
                    ),
                    cron_expression="0 0 * * * *",
                    timezone="UTC",
                ),
            ),
        ),
    ],
    output_schema=ScheduleStatus,
)
@schedule_cli.command(
    name="status", short_help="Get the status of a schedule.", cls=AnyscaleCommand,
)
@click.option(
    "--config-file",
    "-f",
    required=False,
    type=str,
    help="Path to a YAML config file to use for this schedule.",
)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
@click.option("--id", "-i", required=False, default=None, help="Id of the schedule.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The named Anyscale Cloud for the schedule. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the schedule. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice([f.value for f in OutputFormat]),
    default=OutputFormat.TEXT.value,
    show_default=True,
    hidden=True,
    help="Output format for the result.",
)
@click.option(
    "--json",
    "-j",
    is_flag=True,
    default=False,
    help="Output the status in a structured JSON format.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Include verbose details in the status.",
)
def status(
    config_file: str,
    name: str,
    cloud: str,
    project: str,
    id: str,  # noqa: A002
    output_format: str,
    json: bool,
    verbose: bool,
) -> None:
    """Query the status of a Schedule.

    You can query the status of a schedule by config file, name, or id.

    To specify the schedule by name, use the --name flag. You can specify the cloud with --cloud and the project with --project.

    To specify the schedule by id, use the --id flag.

    To specify the schedule by config file, use --config-file. Ensure that name and optionally cloud and project are specified in the
    config file's job config.
    """
    _validate_schedule_identifiers(name=name, id=id, config_file=config_file)

    if id is not None:
        status = anyscale.schedule.status(id=id)
    else:
        if config_file is not None:
            name, cloud, project = _read_identifiers_from_config_file(config_file)

        status = anyscale.schedule.status(name=name, cloud=cloud, project=project)

    status_dict = status.to_dict()
    if not verbose:
        status_dict.pop("config", None)

    resolved = resolve_output_format(output_format, json)
    if resolved != OutputFormat.TEXT.value:
        print_output(status_dict, resolved)
    else:
        stream = StringIO()
        yaml.dump(status_dict, stream, sort_keys=False)
        print(stream.getvalue(), end="")


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Trigger an immediate run of a schedule by name.",
            command="anyscale schedule run -n my-schedule",
            output_raw=command_examples.SCHEDULE_RUN_EXAMPLE,
        ),
    ],
)
@schedule_cli.command(
    name="run", short_help="Manually run a schedule now.", cls=AnyscaleCommand,
)
@click.option(
    "--config-file",
    "-f",
    required=False,
    type=str,
    help="Path to a YAML config file to use for this schedule.",
)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
@click.option("--id", "-i", required=False, default=None, help="Id of the schedule.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The named Anyscale Cloud for the schedule. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the schedule. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
def trigger(
    config_file: str, name: str, id: str, cloud: str, project: str  # noqa: A002
) -> None:
    """Manually run a schedule now.

    This function takes an existing schedule and runs it now.
    You can specify the schedule by name or id.
    You can also pass in a YAML file as a convenience. This is equivalent to passing in the name specified in the YAML file.
    IMPORTANT: If you pass in a YAML definition that differs from the schedule definition, the schedule will NOT be updated.
    Please use the `anyscale schedule apply` command to update the configuration of your schedule
    or use the `anyscale job submit` command to submit a one off job that is not a part of a schedule.
    """

    _validate_schedule_identifiers(name=name, id=id, config_file=config_file)

    if id is not None:
        anyscale.schedule.trigger(id=id)
    else:
        if config_file is not None:
            name, cloud, project = _read_identifiers_from_config_file(config_file)

        anyscale.schedule.trigger(
            name=name, cloud=cloud, project=project,
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Get the console URL of a schedule by name.",
            command="anyscale schedule url -n my-schedule",
            output_raw=command_examples.SCHEDULE_URL_EXAMPLE,
        ),
    ],
)
@schedule_cli.command(
    name="url", short_help="Get the console URL of a schedule.", cls=AnyscaleCommand,
)
@click.argument("schedule_config_file", required=False)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
@click.option("--id", "-i", required=False, default=None, help="Id of the schedule.")
@click.option("--v2", is_flag=True, help="Use new SDK-based implementation")
@click.option("--cloud", help="Cloud name (required with --name in v2 mode)")
@click.option("--project", help="Project name (required with --name in v2 mode)")
def url(
    schedule_config_file: str,
    id: str,  # noqa: A002
    name: str,
    v2: bool,
    cloud: Optional[str],
    project: Optional[str],
) -> None:
    """Get the console URL of a schedule.

    This function accepts 1 argument, a path to a YAML config file that defines this schedule.
    You can also specify the schedule by name or id.
    """
    if v2:
        result_url = anyscale.schedule.url(
            id=id, name=name, cloud=cloud, project=project,
        )
        click.echo(f"View your schedule at {result_url}")
    else:
        job_controller = ScheduleController()
        resolved_id = job_controller.resolve_file_name_or_id(
            schedule_config_file=schedule_config_file, id=id, name=name
        )
        job_controller.url(resolved_id)


def _validate_delete_identifiers(
    name: Optional[str],
    id: Optional[str],  # noqa: A002
    cloud: Optional[str],
    project: Optional[str],
):
    """Validate identifiers for the delete command.

    Either --id OR --name must be provided.
    When --name is used, --cloud and --project are also required.
    When --id is used, --cloud and --project cannot be used.
    """
    if name is None and id is None:
        raise click.ClickException("One of '--name' or '--id' must be provided.")

    if name is not None and id is not None:
        raise click.ClickException("Only one of '--name' or '--id' can be provided.")

    if id is not None and (cloud is not None or project is not None):
        raise click.ClickException(
            "'--cloud' and '--project' cannot be used with '--id'."
        )

    if name is not None and (cloud is None or project is None):
        raise click.ClickException(
            "'--cloud' and '--project' are required when using '--name'."
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Delete a schedule by ID or by name.",
            command="anyscale schedule delete --id cronjob_vrjrbwcnfjjid7fsld3sfkn8jz",
            output_raw=command_examples.SCHEDULE_DELETE_EXAMPLE,
        ),
    ],
)
@schedule_cli.command(
    name="delete", short_help="Delete a schedule.", cls=AnyscaleCommand,
)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
@click.option("--id", "-i", required=False, default=None, help="Id of the schedule.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The named Anyscale Cloud for the schedule (required with --name).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project for the schedule (required with --name).",
)
def delete(
    name: Optional[str],
    id: Optional[str],  # noqa: A002
    cloud: Optional[str],
    project: Optional[str],
) -> None:
    """Delete a Schedule.

    If the schedule is active, it will be automatically paused before deletion.
    The schedule must have no active triggered jobs.

    To specify the schedule by id, use the --id flag.

    To specify the schedule by name, use the --name flag along with --cloud and --project.
    """
    _validate_delete_identifiers(name=name, id=id, cloud=cloud, project=project)

    if id is not None:
        anyscale.schedule.delete(id=id)
    else:
        anyscale.schedule.delete(name=name, cloud=cloud, project=project)
