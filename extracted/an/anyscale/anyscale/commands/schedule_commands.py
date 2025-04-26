from io import StringIO
from json import dumps as json_dumps
import pathlib
from typing import Optional

import click
import yaml

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand, LegacyAnyscaleCommand
from anyscale.controllers.schedule_controller import ScheduleController
from anyscale.schedule.models import JobConfig, ScheduleConfig, ScheduleState


log = BlockLogger()  # CLI Logger


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


@schedule_cli.command(
    name="apply", cls=AnyscaleCommand, example=command_examples.SCHEDULE_APPLY_EXAMPLE
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
    """ Create or Update a Schedule

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


@schedule_cli.command(
    name="create",
    cls=LegacyAnyscaleCommand,
    new_prefix="anyscale schedule",
    new_cli=apply,
)
@click.argument("schedule_config_file", required=True)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
@click.option(
    "--description", required=False, default=None, help="Description of schedule."
)
def create(
    schedule_config_file: str, name: Optional[str], description: Optional[str],
) -> None:
    """ Create or Update a Schedule

    This function accepts 1 argument, a path to a YAML config file that defines this schedule.

    Note: if a schedule with the name exists in the specified project, it will be updated instead.
    """
    log.warning("DEPRECATED: Use `anyscale schedule apply` instead.")
    job_controller = ScheduleController()
    job_controller.apply(
        schedule_config_file, name, description,
    )


@schedule_cli.command(
    name="update",
    cls=LegacyAnyscaleCommand,
    new_prefix="anyscale schedule",
    new_cli=apply,
)
@click.argument("schedule_config_file", required=True)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
@click.option(
    "--description", required=False, default=None, help="Description of schedule."
)
def update(
    schedule_config_file: str, name: Optional[str], description: Optional[str],
) -> None:
    """ Create or Update a Schedule

    This function accepts 1 argument, a path to a YAML config file that defines this schedule.
    """
    log.warning("DEPRECATED: Use `anyscale schedule apply` instead.")
    job_controller = ScheduleController()
    job_controller.apply(
        schedule_config_file, name, description,
    )


@schedule_cli.command(
    name="list", cls=AnyscaleCommand, example=command_examples.SCHEDULE_LIST_EXAMPLE
)
@click.option(
    "--name", "-n", required=False, default=None, help="Filter by the name of the job"
)
@click.option("--id", "-i", required=False, default=None, help="Id of the schedule.")
def list(  # noqa: A001
    name: Optional[str] = None, id: Optional[str] = None  # noqa: A002
) -> None:
    """ List Schedules

    You can optionally filter schedules by rowname.
    """
    job_controller = ScheduleController()
    job_controller.list(name=name, id=id)


@schedule_cli.command(
    name="pause", cls=AnyscaleCommand, example=command_examples.SCHEDULE_PAUSE_EXAMPLE
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


@schedule_cli.command(
    name="resume", cls=AnyscaleCommand, example=command_examples.SCHEDULE_RESUME_EXAMPLE
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
    """ Resume a Schedule

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


@schedule_cli.command(
    name="status", cls=AnyscaleCommand, example=command_examples.SCHEDULE_STATUS_EXAMPLE
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

    if json:
        print(json_dumps(status_dict, indent=4, sort_keys=False))
    else:
        stream = StringIO()
        yaml.dump(status_dict, stream, sort_keys=False)
        print(stream.getvalue(), end="")


@schedule_cli.command(
    name="run", cls=AnyscaleCommand, example=command_examples.SCHEDULE_RUN_EXAMPLE
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
    """ Manually run a Schedule

    This function takes an existing schedule and runs it now.
    You can specify the schedule by name or id.
    You can also pass in a YAML file as a convinience. This is equivalent to passing in the name specified in the YAML file.
    IMPORTANT: if you pass in a YAML definition that differs from the Schedule defition, the Schedule will NOT be updated.
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


@schedule_cli.command(
    name="url", cls=AnyscaleCommand, example=command_examples.SCHEDULE_URL_EXAMPLE
)
@click.argument("schedule_config_file", required=False)
@click.option(
    "--name", "-n", required=False, default=None, help="Name of the schedule."
)
@click.option("--id", "-i", required=False, default=None, help="Id of the schedule.")
def url(schedule_config_file: str, id: str, name: str) -> None:  # noqa: A002
    """ Get a Schedule URL

    This function accepts 1 argument, a path to a YAML config file that defines this schedule.
    You can also specify the schedule by name or id.
    """

    job_controller = ScheduleController()
    id = job_controller.resolve_file_name_or_id(  # noqa: A001
        schedule_config_file=schedule_config_file, id=id, name=name
    )
    job_controller.url(id)
