from io import StringIO
from json import dumps as json_dumps
import pathlib
from subprocess import list2cmdline
from typing import List, Optional, Tuple

import click
from rich.console import Console
import yaml

import anyscale
from anyscale._private.models.image_uri import ImageURI
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models.ha_job_states import HaJobStates
from anyscale.commands import command_examples
from anyscale.commands.util import (
    AnyscaleCommand,
    build_kv_table,
    convert_kv_strings_to_dict,
    override_env_vars,
    parse_repeatable_tags_to_dict,
    parse_tags_kv_to_str_map,
)
from anyscale.controllers.job_controller import JobController
from anyscale.job.models import JobConfig, JobLogMode, JobState, JobStatus
from anyscale.util import validate_list_jobs_state_filter, validate_non_negative_arg


log = BlockLogger()  # CLI Logger


def _validate_job_name_and_id(name: Optional[str], id: Optional[str]):  # noqa: A002
    if name is None and id is None:
        raise click.ClickException("One of '--name' and '--id' must be provided.")

    if name is not None and id is not None:
        raise click.ClickException("Only one of '--name' and '--id' can be provided.")


def _check_for_new_format_fields(config_file: str) -> None:
    """Check if a config file contains new-format fields that require using -f flag.

    Raises a ClickException if new-format fields are detected, suggesting the user
    should use the --config-file/-f flag instead.
    """
    # Fields that are specific to the new job submission API
    NEW_FORMAT_FIELDS = {
        "image_uri",
        "containerfile",
        "working_dir",
        "requirements",
        "env_vars",
        "py_modules",
        "excludes",
        "ray_version",
        "registry_login_secret",
        "timeout_s",
        "tags",
    }

    try:
        with open(config_file) as f:
            config_dict = yaml.safe_load(f) or {}
    except Exception:  # noqa: BLE001
        # If we can't read the file, let the normal flow handle the error
        return

    if not isinstance(config_dict, dict):
        return

    found_fields = [field for field in NEW_FORMAT_FIELDS if field in config_dict]

    if found_fields:
        fields_str = ", ".join(f"'{field}'" for field in found_fields)
        raise click.ClickException(
            f"Your config file contains fields that require the new job submission API: {fields_str}\n\n"
            f"Please use the '--config-file' or '-f' flag instead:\n"
            f"  anyscale job submit -f {config_file}\n\n"
            f"Alternatively, update your config to use the legacy format.\n"
            f"See https://docs.anyscale.com/reference/job-api/ for more information."
        )


@click.group("job", help="Interact with production jobs running on Anyscale.")
def job_cli() -> None:
    pass


@job_cli.command(
    name="submit",
    short_help="Submit a job.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_SUBMIT_EXAMPLE,
)
@click.option("-n", "--name", required=False, default=None, help="Name of the job.")
@click.option(
    "-w",
    "--wait",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Block this CLI command and print logs until the job finishes.",
)
@click.option(
    "--config-file",
    "-f",
    required=False,
    default=None,
    type=str,
    help="Path to a YAML config file to use for this job. Command-line flags will overwrite values read from the file.",
)
@click.option(
    "--compute-config",
    required=False,
    default=None,
    type=str,
    help="Named compute configuration to use for the job. This defaults to the compute configuration of the workspace.",
)
@click.option(
    "--image-uri",
    required=False,
    default=None,
    type=str,
    help="Container image to use for this job. When running in a workspace, this defaults to the image of the workspace.",
)
@click.option(
    "--registry-login-secret",
    required=False,
    default=None,
    type=str,
    help="Name or identifier of the secret containing credentials to authenticate to the docker registry hosting the image. "
    "This can only be used when 'image_uri' is specified and the image is not hosted on Anyscale.",
)
@click.option(
    "--containerfile",
    required=False,
    default=None,
    type=str,
    help="Path to a containerfile to build the image to use for the job.",
)
@click.option(
    "--env",
    required=False,
    multiple=True,
    type=str,
    help="Environment variables to set for the job. The format is 'key=value'. This argument can be specified multiple times. When the same key is also specified in the config file, the value from the command-line flag will overwrite the value from the config file.",
)
@click.option(
    "--working-dir",
    required=False,
    default=None,
    type=str,
    help="Path to a local directory or a remote URI to a .zip file (S3, GS, HTTP) that will be the working directory for the job. The files in the directory will be automatically uploaded to cloud storage. When running in a workspace, this defaults to the current working directory.",
)
@click.option(
    "-e",
    "--exclude",
    required=False,
    type=str,
    multiple=True,
    help="File pattern to exclude when uploading local directories. This argument can be specified multiple times and the patterns will be appended to the 'excludes' list in the config file (if any).",
)
@click.option(
    "-r",
    "--requirements",
    required=False,
    default=None,
    type=str,
    help="Path to a requirements.txt file containing dependencies for the job. Anyscale installs these dependencies on top of the image. If you run a job from a workspace, the default is to use the workspace dependencies, but specifying this option overrides them.",
)
@click.option(
    "--py-module",
    required=False,
    default=None,
    multiple=True,
    type=str,
    help="Python modules to be available for import in the Ray workers. Each entry must be a path to a local directory.",
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="Tag in key=value (or key:value) format. Repeat to add multiple.",
)
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
@click.option(
    "--ray-version",
    required=False,
    default=None,
    type=str,
    help="The Ray version (X.Y.Z) to the image specified by --image-uri. This is only used when --image-uri is provided. If you don't specify a Ray version, Anyscale defaults to the latest Ray version available at the time of the Anyscale CLI/SDK release.",
)
@click.option(
    "--max-retries",
    required=False,
    default=None,
    type=int,
    help="Maximum number of retries to attempt before failing the entire job.",
)
@click.option(
    "--timeout-s",
    "--timeout",
    "-t",
    required=False,
    default=None,
    type=int,
    help="The timeout in seconds for each job run. Set to None for no limit to be set.",
)
@click.argument("entrypoint", required=False, nargs=-1, type=click.UNPROCESSED)
def submit(  # noqa: PLR0912 PLR0913 C901
    entrypoint: Tuple[str],
    name: Optional[str],
    wait: Optional[bool],
    config_file: Optional[str],
    compute_config: Optional[str],
    image_uri: Optional[str],
    ray_version: Optional[str],
    registry_login_secret: Optional[str],
    containerfile: Optional[str],
    env: Tuple[str],
    working_dir: Optional[str],
    exclude: Tuple[str],
    requirements: Optional[str],
    py_module: Tuple[str],
    tags: Tuple[str],
    cloud: Optional[str],
    project: Optional[str],
    max_retries: Optional[int],
    timeout_s: Optional[int],
):
    """Submit a job.

    The job config can be specified in one of the following ways:

    * Job config file can be specified as a single positional argument. E.g. `anyscale job submit config.yaml`.

    * Job config can also be specified with command-line arguments. In this case, the entrypoint should be specified
as the positional arguments starting with `--`. Other arguments can be specified with command-line flags. E.g.

      * `anyscale job submit -- python main.py`: submit a job with the entrypoint `python main.py`.

      * `anyscale job submit --name my-job -- python main.py`: submit a job with the name `my-job` and the
entrypoint `python main.py`.

    * [Experimental] If you want to specify a config file and override some arguments with the commmand-line flags,
use the `--config-file` flag. E.g.

      * `anyscale job submit --config-file config.yaml`: submit a job with the config in `config.yaml`.

      * `anyscale job submit --config-file config.yaml -- python main.py`: submit a job with the config in `config.yaml`
and override the entrypoint with `python main.py`.

    Either containerfile or image-uri should be used, specifying both will result in an error.

    By default, this command submits the job asynchronously and exits. To wait for the job to complete, use the `--wait` flag.
    """

    job_controller = JobController()
    if len(entrypoint) == 1 and (
        pathlib.Path(entrypoint[0]).is_file() or entrypoint[0].endswith(".yaml")
    ):
        # If entrypoint is a single string that ends with .yaml, e.g. `anyscale job submit config.yaml`,
        # treat it as a config file, and use the old job submission API.
        if config_file is not None:
            raise click.ClickException(
                "`--config-file` should not be used when providing a config file as the entrypoint."
            )
        if image_uri:
            raise click.ClickException(
                "`--image-uri` should not be used when providing a config file as the entrypoint."
            )
        if registry_login_secret:
            raise click.ClickException(
                "`--registry-login-secret` should not be used when providing a config file as the entrypoint."
            )
        if containerfile:
            raise click.ClickException(
                "`--containerfile` should not be used when providing a config file as the entrypoint."
            )
        if env:
            raise click.ClickException(
                "`--env` should not be used when providing a config file as the entrypoint."
            )

        config_file = entrypoint[0]
        if not pathlib.Path(config_file).is_file():
            raise click.ClickException(f"Job config file '{config_file}' not found.")

        # Check if the config file contains new-format fields that require using -f
        _check_for_new_format_fields(config_file)

        log.info(f"Submitting job from config file {config_file}.")

        job_id = job_controller.submit(config_file, name=name)
    else:
        # Otherwise, use the new job submission API. E.g.
        # `anyscale job submit -- python main.py`,
        # or `anyscale job submit --config-file config.yaml`.
        if len(entrypoint) == 0 and config_file is None:
            raise click.ClickException(
                "Either a config file or an inlined entrypoint must be provided."
            )
        if config_file is not None and not pathlib.Path(config_file).is_file():
            raise click.ClickException(f"Job config file '{config_file}' not found.")

        args = {}
        if len(entrypoint) > 0:
            args["entrypoint"] = list2cmdline(entrypoint)
        if name:
            args["name"] = name

        if containerfile and image_uri:
            raise click.ClickException(
                "Only one of '--containerfile' and '--image-uri' can be provided."
            )

        if registry_login_secret and (
            not image_uri or ImageURI.from_str(image_uri).is_cluster_env_image()
        ):
            raise click.ClickException(
                "Registry login secret can only be used with an image that is not hosted on Anyscale.",
            )

        if ray_version and (not image_uri and not containerfile):
            raise click.ClickException(
                "Ray version can only be used with an image or containerfile.",
            )

        if image_uri:
            args["image_uri"] = image_uri

        if registry_login_secret:
            args["registry_login_secret"] = registry_login_secret

        if containerfile:
            args["containerfile"] = containerfile

        if ray_version:
            args["ray_version"] = ray_version

        if working_dir:
            args["working_dir"] = working_dir

        if config_file is not None:
            config = JobConfig.from_yaml(config_file, **args)
        else:
            config = JobConfig.from_dict(args)

        if compute_config is not None:
            config = config.options(compute_config=compute_config)

        if exclude:
            config = config.options(excludes=[e for e in exclude])

        if requirements is not None:
            if not pathlib.Path(requirements).is_file():
                raise click.ClickException(
                    f"Requirements file '{requirements}' not found."
                )
            config = config.options(requirements=requirements)

        if env:
            config = override_env_vars(config, convert_kv_strings_to_dict(env))

        if py_module:
            for module in py_module:
                if not pathlib.Path(module).is_dir():
                    raise click.ClickException(
                        f"Python module path '{module}' does not exist or is not a directory."
                    )
            config = config.options(py_modules=[*py_module])

        if cloud is not None:
            config = config.options(cloud=cloud)
        if project is not None:
            config = config.options(project=project)

        if max_retries is not None:
            config = config.options(max_retries=max_retries)

        if timeout_s is not None:
            config = config.options(timeout_s=timeout_s)

        if tags:
            tag_map = parse_tags_kv_to_str_map(tags)
            if tag_map:
                config = config.options(tags=tag_map)

        log.info(f"Submitting job with config {config}.")
        job_id = anyscale.job.submit(config)

    if wait:
        log.info(
            "Waiting for the job to run. Interrupting this command will not cancel the job."
        )
        anyscale.job.wait(id=job_id, follow=True)
    else:
        log.info("Use `--wait` to wait for the job to run and stream logs.")


# TODO(mowen): Add cloud support for this when we refactor to new SDK method
@job_cli.command(
    name="list",
    help="Display information about existing jobs.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_LIST_EXAMPLE,
)
@click.option("--name", "-n", required=False, default=None, help="Filter by job name.")
@click.option(
    "--id", "--job-id", required=False, default=None, help="Filter by job id."
)
@click.option(
    "--project-id", required=False, default=None, help="Filter by project id."
)
@click.option(
    "--include-all-users",
    is_flag=True,
    default=False,
    help="Include jobs not created by current user.",
)
@click.option(
    "--include-archived",
    is_flag=True,
    default=False,
    help=(
        "List archived jobs as well as unarchived jobs."
        "If not provided, defaults to listing only unarchived jobs."
    ),
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help=(
        "This option can be repeated to filter by multiple tags. "
        "Tags with the same key are ORed, whereas tags with different keys are ANDed. "
        "Example: --tag team:mlops --tag team:infra --tag env:prod. "
        "Filters with team: (mlops OR infra) AND env:prod."
    ),
)
@click.option(
    "--max-items",
    required=False,
    default=10,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
)
@click.option(
    "--state",
    "-s",
    "states",
    required=False,
    multiple=True,
    help=f"Filter jobs by state. Accepts one or more states. Allowed states: {', '.join(HaJobStates.allowable_values)}",
    callback=validate_list_jobs_state_filter,
)
def list(  # noqa: A001 PLR0913
    name: Optional[str],
    id: Optional[str],  # noqa: A002
    project_id: Optional[str],
    include_all_users: bool,
    include_archived: bool,
    max_items: int,
    states: List[HaJobStates],
    tags: List[str],
) -> None:
    job_controller = JobController()
    job_controller.list(
        name=name,
        job_id=id,
        project_id=project_id,
        include_all_users=include_all_users,
        include_archived=include_archived,
        max_items=max_items,
        states=states,
        tags=parse_repeatable_tags_to_dict(tags) if tags else None,
    )


@job_cli.command(
    name="archive",
    short_help="Archive a job.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_ARCHIVE_EXAMPLE,
)
@click.option("--id", "--job-id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
def archive(
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
) -> None:
    """Archive a job.

    To specify the job by name, use the --name flag. To specify the job by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.

    If job is specified by name and there are multiple jobs with the specified name, the most recently created job
status will be archived.
    """
    _validate_job_name_and_id(name=name, id=id)
    anyscale.job.archive(id=id, name=name, cloud=cloud, project=project)


@job_cli.command(
    name="terminate",
    short_help="Terminate a job.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_TERMINATE_EXAMPLE,
)
@click.option("--id", "--job-id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
def terminate(
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
) -> None:
    """Terminate a job.

    To specify the job by name, use the --name flag. To specify the job by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.

    If job is specified by name and there are multiple jobs with the specified name, the most recently created job
status will be terminated.
    """
    _validate_job_name_and_id(name=name, id=id)
    anyscale.job.terminate(name=name, id=id, cloud=cloud, project=project)
    if id is not None:
        log.info(f"Query the status of the job with `anyscale job status --id {id}`.")
    else:
        log.info(
            f"Query the status of the job with `anyscale job status --name {name}`."
        )


# TODO(mowen): Add project and cloud support when updating this.
@job_cli.command(
    name="logs", cls=AnyscaleCommand, example=command_examples.JOB_LOGS_EXAMPLE
)
@click.option("--id", "--job-id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option("--run", required=False, help="Name of the job run.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
@click.option(
    "--head",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Used with --max-lines to get `max-lines` lines from the head of the log.",
)
@click.option(
    "--tail",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Used with --max-lines to get `max-lines` lines from the tail of the log.",
)
@click.option(
    "--max-lines",
    required=False,
    default=None,
    type=int,
    help="Used with --head or --tail to limit the number of lines output.",
)
@click.option(
    "--follow",
    "-f",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Whether to follow the log.",
)
@click.option(
    "--all-attempts",
    is_flag=True,
    default=False,
    help="DEPRECATED: Listing logs from all attempts no longer supported, instead list jobs by run name.",
)
def logs(  # noqa: PLR0913
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    run: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
    head: bool,
    tail: bool,
    max_lines: Optional[int],
    follow: bool = False,
    all_attempts: bool = False,
) -> None:
    """Print the logs of a job.

    By default from the latest job attempt.
    """
    if all_attempts:
        raise click.ClickException(
            "Listing logs from all attempts no longer supported, instead list jobs by run name."
        )
    if follow:
        job_controller = JobController(raise_structured_exception=True)
        job_controller.logs(
            job_id=id, job_name=name, should_follow=True, all_attempts=all_attempts,
        )
    else:
        _validate_job_name_and_id(name=name, id=id)
        if head and tail:
            raise click.ClickException(
                "Only one of '--head' and '--tail' can be provided."
            )
        if max_lines is not None and not (head or tail):
            raise click.ClickException(
                "'--max-lines' must be used with either '--head' or '--tail'"
            )
        mode = JobLogMode.TAIL
        if head:
            mode = JobLogMode.HEAD

        logs = anyscale.job.get_logs(
            id=id,
            name=name,
            run=run,
            cloud=cloud,
            project=project,
            mode=mode,
            max_lines=max_lines,
        )
        print(logs)


@job_cli.command(
    name="wait",
    short_help="Wait for a job to enter a specific state.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_WAIT_EXAMPLE,
)
@click.option(
    "--id", "--job-id", required=False, help="Unique ID of the job.",
)
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
)
@click.option(
    "--state",
    "-s",
    required=False,
    default=JobState.SUCCEEDED,
    help="The state to wait for this job to enter",
)
@click.option(
    "--timeout-s",
    "--timeout",
    "-t",
    required=False,
    default=1800,
    type=float,
    help="The timeout in seconds after which this command will exit.",
)
def wait(
    id: Optional[str],  # noqa: A002
    name: Optional[str],
    cloud: Optional[str],
    project: Optional[str],
    state: str = JobState.SUCCEEDED,
    timeout_s=None,
) -> None:
    """Wait for a job to enter a specific state (default: SUCCEEDED).

    To specify the job by name, use the --name flag. To specify the job by id, use the --id flag.

    If the job reaches the target state, the command will exit successfully.

    If the job reaches a terminal state other than the target state, the command will exit with an error.

    If the command reaches the timeout, the command will exit with an error but job execution will continue.
    """
    try:
        state = JobState.validate(state)
    except ValueError as e:
        raise click.ClickException(str(e))
    try:
        anyscale.job.wait(
            name=name,
            id=id,
            cloud=cloud,
            project=project,
            state=state,
            timeout_s=timeout_s,  # type: ignore
        )
    except Exception as e:  # noqa: BLE001
        raise click.ClickException(str(e)) from None


@job_cli.command(
    name="status",
    short_help="Get the status of a job.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_STATUS_EXAMPLE,
)
@click.option(
    "--id", "--job-id", required=False, default=None, help="Unique ID of the job."
)
@click.option("--name", "-n", required=False, default=None, help="Name of the job.")
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
)
@click.option(
    "--project",
    required=False,
    default=None,
    type=str,
    help="Named project to use for the job. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
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
    name: Optional[str],
    id: Optional[str],  # noqa: A002
    cloud: Optional[str],
    project: Optional[str],
    json: bool,
    verbose: bool,
):
    """Query the status of a job.

    To specify the job by name, use the --name flag. To specify the job by id, use the --id flag. Either name or
id should be used, specifying both will result in an error.

    If job is specified by name and there are multiple jobs with the specified name, the most recently created job
status will be returned.
    """
    _validate_job_name_and_id(name=name, id=id)

    status: JobStatus = anyscale.job.status(
        name=name, id=id, cloud=cloud, project=project
    )
    status_dict = status.to_dict()

    if not verbose:
        status_dict.pop("config", None)

    if json:
        print(json_dumps(status_dict, indent=4, sort_keys=False))
    else:
        stream = StringIO()
        yaml.dump(status_dict, stream, sort_keys=False)
        print(stream.getvalue(), end="")


@job_cli.group("tags", help="Manage tags for jobs.")
def job_tags_cli() -> None:
    pass


@job_tags_cli.command(
    name="add",
    help="Add or update tags on a job.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_TAGS_ADD_EXAMPLE,
)
@click.option("--id", "job_id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="Tag in key=value (or key:value) format. Repeat to add multiple.",
)
def add_tags(job_id: Optional[str], name: Optional[str], tags: Tuple[str]) -> None:
    if not job_id and not name:
        raise click.ClickException("Provide either --id or --name.")
    tag_map = parse_tags_kv_to_str_map(tags)
    if not tag_map:
        raise click.ClickException("Provide at least one --tag key=value.")
    anyscale.job.add_tags(job_id=job_id, name=name, tags=tag_map)
    stderr = Console(stderr=True)
    ident = job_id or name or "<unknown>"
    stderr.print(f"Tags updated for job '{ident}'.")


@job_tags_cli.command(
    name="remove",
    help="Remove tags by key from a job.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_TAGS_REMOVE_EXAMPLE,
)
@click.option("--id", "job_id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option("--key", "keys", multiple=True, help="Tag key to remove. Repeatable.")
def remove_tags(job_id: Optional[str], name: Optional[str], keys: Tuple[str]) -> None:
    if not job_id and not name:
        raise click.ClickException("Provide either --id or --name.")
    key_list = [k for k in keys if k and k.strip()]
    if not key_list:
        raise click.ClickException("Provide at least one --key to remove.")
    anyscale.job.remove_tags(job_id=job_id, name=name, keys=key_list)
    stderr = Console(stderr=True)
    ident = job_id or name or "<unknown>"
    stderr.print(f"Removed tag keys {key_list} from job '{ident}'.")


@job_tags_cli.command(
    name="list",
    help="List tags for a job.",
    cls=AnyscaleCommand,
    example=command_examples.JOB_TAGS_LIST_EXAMPLE,
)
@click.option("--id", "job_id", required=False, help="Unique ID of the job.")
@click.option("--name", "-n", required=False, help="Name of the job.")
@click.option("--json", "json_output", is_flag=True, default=False, help="JSON output.")
def list_tags(job_id: Optional[str], name: Optional[str], json_output: bool) -> None:
    if not job_id and not name:
        raise click.ClickException("Provide either --id or --name.")
    tag_map = anyscale.job.list_tags(job_id=job_id, name=name)
    if json_output:
        Console().print_json(json=json_dumps(tag_map, indent=2))
    else:
        stderr = Console(stderr=True)
        if not tag_map:
            stderr.print("No tags found.")
            return
        pairs = tag_map.items()
        stderr.print(build_kv_table(pairs, title="Tags"))
