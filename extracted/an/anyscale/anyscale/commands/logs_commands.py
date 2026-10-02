"""
This file holds all of the CLI commands for the "anyscale logs" path. Note that
most of the implementation for this command is in the controller to make the controller
accessible to the SDK in the future.

TODO (shomilj): Bring the controller to feature parity with the CLI.
"""

from datetime import timedelta
import math
from typing import Optional

import click
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from anyscale.api_utils.exceptions.job_errors import NoJobRunError
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import LogFilter
from anyscale.client.openapi_client.models.node_type import NodeType
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import OutputFormat
from anyscale.commands.util import AnyscaleCommand
from anyscale.controllers.logs_controller import (
    DEFAULT_PAGE_SIZE,
    DEFAULT_PARALLELISM,
    DEFAULT_READ_TIMEOUT,
    DEFAULT_TIMEOUT,
    DEFAULT_TTL,
    LogsController,
)


log = BlockLogger()

# Options to configure core functionality. These are mutually exclusive.
option_download = click.option(
    "-d",
    "--download",
    is_flag=True,
    default=False,
    help="Download logs to the current working directory, or a specified path.",
)
option_tail = click.option(
    "-t", "--tail", type=int, default=-1, help="Read the last N lines of logs."
)

# The "glob" is an optional argument.
# e.g. anyscale logs cluster --cluster-id <cluster-id> [GLOB]
argument_glob = click.argument("glob", type=str, default=None, required=False)

# Options to filter beyond what the subcommand already filters to.
option_node_ip = click.option(
    "-ip", "--node-ip", type=str, default=None, help="Filter logs by a node IP."
)
option_instance_id = click.option(
    "--instance-id", type=str, default=None, help="Filter logs by an instance ID."
)
option_worker_only = click.option(
    "--worker-only", is_flag=True, help="Download logs of only the worker nodes."
)
option_head_only = click.option(
    "--head-only", is_flag=True, help="Download logs of only the head node."
)
# Only "anyscale logs job" needs this. The other subcommands return all the cluster
# logs already, so the flag would do nothing there.
option_all_logs = click.option(
    "--all",
    "all_logs",
    is_flag=True,
    default=False,
    help=(
        "Fetch every log file of the cluster that ran the job. Without this flag "
        "the command returns only the driver log."
    ),
)
option_unpack_combined_logs = click.option(
    "--unpack/--no-unpack",
    default=True,
    help="Whether to unpack the combined-worker.log after downloading.",
    hidden=True,
)

option_ttl = click.option(
    "--ttl",
    type=int,
    default=DEFAULT_TTL,
    hidden=True,
    help="TTL in seconds to pass to the service that generates presigned URL's (default: 4h).",
)
option_parallelism = click.option(
    "--parallelism",
    type=int,
    default=DEFAULT_PARALLELISM,
    hidden=True,
    help="Number of files to download in parallel at a time.",
)

# ADVANCED: Configure the download behavior, only useful if --download enabled.
option_download_dir = click.option(
    "--download-dir", type=str, default=None, help="Directory to download logs into."
)


@click.group(
    "logs",
    help="Print or download Ray logs for an Anyscale job, service, or cluster.",
)
def log_cli() -> None:
    pass


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Download the logs of a cluster.",
            command="anyscale logs cluster --id ses_abc123 --download",
        ),
    ],
)
@log_cli.command(
    name="cluster",
    short_help="Access log files of a cluster.",
    help="Access log files of a cluster.",
    cls=AnyscaleCommand,
)
@click.option("--cluster-id", "--id", "id", type=str, required=True, help="Provide a cluster ID.")
@option_download
@option_tail
@argument_glob
@option_node_ip
@option_instance_id
@option_worker_only
@option_head_only
@option_unpack_combined_logs
@option_download_dir
@option_ttl
@option_parallelism
def anyscale_logs_cluster(  # noqa: PLR0913
    id: str,  # noqa: A002
    download: bool,
    tail: int,
    # filters
    glob: Optional[str],
    node_ip: Optional[str],
    instance_id: Optional[str],
    worker_only: bool,
    head_only: bool,
    unpack: bool,
    # list files config
    ttl: int,
    # download files config
    download_dir: Optional[str],
    parallelism: int,
) -> None:
    logs_controller = LogsController()
    execute_anyscale_logs_cluster(
        logs_controller=logs_controller,
        cluster_id=id,
        download=download,
        tail=tail,
        glob=glob,
        node_ip=node_ip,
        instance_id=instance_id,
        worker_only=worker_only,
        head_only=head_only,
        unpack=unpack,
        ttl=ttl,
        download_dir=download_dir,
        parallelism=parallelism,
    )


def execute_anyscale_logs_cluster(  # noqa: PLR0913
    logs_controller: LogsController,
    cluster_id: str,
    download: bool,
    tail: int,
    glob: Optional[str],
    node_ip: Optional[str],
    instance_id: Optional[str],
    worker_only: bool,
    head_only: bool,
    unpack: bool,  # list files config
    ttl: int,
    # download files config
    download_dir: Optional[str],
    parallelism: int,
    resource_id: Optional[str] = None,
):

    node_type: Optional[NodeType] = None
    if worker_only and head_only:
        raise click.ClickException("Cannot specify both --worker-only and --head-only.")
    if worker_only:
        node_type = NodeType.WORKER_NODES
    elif head_only:
        node_type = NodeType.HEAD_NODE

    filter = LogFilter(  # noqa: A001
        cluster_id=cluster_id,
        glob=glob,
        node_ip=node_ip,
        instance_id=instance_id,
        node_type=node_type,
    )

    if download:
        logs_controller.download_logs(
            filter=filter,
            page_size=DEFAULT_PAGE_SIZE,
            timeout=timedelta(seconds=DEFAULT_TIMEOUT),
            read_timeout=timedelta(seconds=DEFAULT_READ_TIMEOUT),
            ttl_seconds=ttl,
            download_dir=download_dir,
            parallelism=parallelism,
            unpack=unpack,
            resource_id=resource_id,
        )

    else:
        # This is for both tailing logs AND for the default behavior (no -t/-d/-f => rendering them in UI).
        console = Console()
        log_group = logs_controller.get_log_group(
            filter=filter,
            page_size=DEFAULT_PAGE_SIZE,
            timeout=timedelta(seconds=DEFAULT_TIMEOUT),
            ttl_seconds=ttl,
        )
        if len(log_group.get_files()) == 0:
            console.print("No results found.")
        elif len(log_group.get_files()) > 1:
            console.print(
                "These are the available log files. To download all files, use --download. To render a specific file, just paste the filename after this command."
            )
            click.echo()
            for session in log_group.get_sessions():
                click.echo()
                renderables = []

                for node in session.get_nodes():
                    table = Table()
                    table.add_column("File Name", justify="left", style="green")
                    table.add_column("Size")
                    for log_file in node.get_files():
                        table.add_row(
                            log_file.file_name,
                            convert_size(log_file.get_size()),
                        )
                    prefix = "Head Node" if node.node_type == NodeType.HEAD_NODE else "Worker Node"
                    # TODO (shomilj): When we support GCE, clean this up.
                    instance_id = (
                        f"EC2 Instance ID: {node.instance_id}"
                        if node.instance_id.startswith("i-")
                        else node.instance_id
                    )
                    renderables.append(
                        Panel(
                            Group(table),
                            title=f"{prefix}: {node.node_ip} ({instance_id})",
                            title_align="left",
                        )
                    )
                group = Group(*renderables)
                console.print(
                    Panel(
                        group,
                        title=f"Session: {session.session_id}",
                        title_align="left",
                        padding=(1, 1),
                    )
                )

        else:
            logs_controller.render_logs(
                log_group=log_group,
                parallelism=parallelism,
                read_timeout=timedelta(seconds=DEFAULT_READ_TIMEOUT),
                tail=tail,
            )

        click.echo()


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Print the driver logs of a job.",
            command="anyscale logs job --id prodjob_abc123",
        ),
        CommandExample(
            description="Download every log file of the job's cluster.",
            command="anyscale logs job --id prodjob_abc123 --all --download",
        ),
    ],
)
@log_cli.command(
    name="job",
    short_help="Access log files of a production job.",
    cls=AnyscaleCommand,
    help=(
        "Access log files of a production job. By default, this command returns "
        "only the driver log of the last job attempt.\n\n"
        "Give --all to get every log file of that cluster. The full set includes "
        "the Ray session logs, the worker logs, the dmesg log, and the cluster "
        "startup output.\n\n"
        "The GLOB argument selects the cluster logs by file name. Put the glob "
        "in quotes, or the shell expands it before the CLI reads it. --all is "
        "the same as the glob '*'.\n\n"
        "--head-only, --worker-only, --node-ip, and --instance-id also read the "
        "cluster logs. Each one limits the result to the nodes that agree with "
        "the filter.\n\n"
        "A job on KubeRay has one log set. --all returns the same files there, "
        "and the other filters are not available."
    ),
)
@click.option(
    "--job-id",
    "--id",
    "id",
    type=str,
    required=True,
    help="Provide a production job ID.",
)
@option_download
@option_tail
@argument_glob
@option_all_logs
@option_node_ip
@option_instance_id
@option_worker_only
@option_head_only
@option_unpack_combined_logs
@option_download_dir
@option_ttl
@option_parallelism
def anyscale_logs_job(  # noqa: PLR0913
    id: str,  # noqa: A002
    download: bool,
    tail: int,
    # filters
    glob: Optional[str],
    all_logs: bool,
    node_ip: Optional[str],
    instance_id: Optional[str],
    worker_only: bool,
    head_only: bool,
    unpack: bool,
    # list files config
    ttl: int,
    # download files config
    download_dir: Optional[str],
    parallelism: int,
) -> None:
    if all_logs and glob:
        raise click.ClickException(
            "Pass either --all or a glob, not both. --all is the same as the glob '*'."
        )

    logs_controller = LogsController()
    cluster_id: Optional[str] = None
    is_kuberay_job = False
    try:
        (
            cluster_id,
            job_run_id,
        ) = logs_controller.get_cluster_id_and_last_job_run_id_for_prodjob(prodjob_id=id)
    except NoJobRunError:
        # An imported KubeRay workload has no job-run row, so there is no run id or
        # cluster id to resolve. Its logs are addressed by the production job id
        # instead. Re-raise for a genuinely un-run Anyscale job.
        if not logs_controller.get_kuberay_cr_id_for_prodjob(prodjob_id=id):
            raise
        is_kuberay_job = True
        job_run_id = id

    if is_kuberay_job and any([glob, node_ip, instance_id, worker_only, head_only]):
        # The cluster-log path needs a cluster id, which KubeRay has none of; these
        # filters would silently apply to nothing.
        raise click.ClickException(
            "A glob, --node-ip, --instance-id, --worker-only and --head-only are not "
            "supported for KubeRay jobs. Re-run without them to fetch the driver logs."
        )

    if is_kuberay_job and all_logs:
        # The narrowing filters above are an error because they would apply to
        # nothing. --all only widens, and the driver path already returns every file
        # Anyscale keeps for a KubeRay workload, so say so and go on.
        log.warning(
            "This job runs on KubeRay. Anyscale keeps one log set for it, so --all "
            "returns the same files as the default."
        )

    # --all is the same request as the glob that matches every file. KubeRay has no
    # cluster to glob over, so it stays on the driver path.
    effective_glob = "*" if all_logs and not is_kuberay_job else glob

    use_job_logs = job_run_id and not any(
        [effective_glob, node_ip, instance_id, worker_only, head_only]
    )
    if use_job_logs:
        if not is_kuberay_job:
            # Before version 0.26.102 this command gave all the cluster logs. Users
            # read the smaller result as a fault, so name the logs that came back.
            # A KubeRay job keeps one log set, so the note has nothing to offer it.
            log.info(
                "Fetched the driver log only. Pass --all for every log file of the "
                "cluster that ran this job."
            )
        if ttl != DEFAULT_TTL:
            log.warning(
                "--ttl is ignored when fetching job-scoped logs; pass --all, "
                "--head-only, --worker-only, --node-ip, --instance-id, or a "
                "glob to fall back to the cluster-log path which honors --ttl."
            )
        if download:
            logs_controller.download_job_logs(
                job_run_id=job_run_id,
                page_size=DEFAULT_PAGE_SIZE,
                timeout=timedelta(seconds=DEFAULT_TIMEOUT),
                read_timeout=timedelta(seconds=DEFAULT_READ_TIMEOUT),
                download_dir=download_dir,
                parallelism=parallelism,
                unpack=unpack,
                resource_id=id,
                is_kuberay_job=is_kuberay_job,
            )
        else:
            log_group = logs_controller.get_job_log_group(
                job_run_id=job_run_id,
                page_size=DEFAULT_PAGE_SIZE,
                timeout=timedelta(seconds=DEFAULT_TIMEOUT),
                is_kuberay_job=is_kuberay_job,
            )
            if len(log_group.get_chunks()) == 0:
                Console().print("No results found.")
            else:
                logs_controller.render_logs(
                    log_group=log_group,
                    parallelism=parallelism,
                    read_timeout=timedelta(seconds=DEFAULT_READ_TIMEOUT),
                    tail=tail,
                )
            click.echo()
        return

    # Unreachable for KubeRay: without cluster-scoped filters `use_job_logs` is true and
    # returns above, and with them we raised. Asserted so the invariant fails loudly
    # rather than passing None into the cluster-log path.
    assert cluster_id is not None
    execute_anyscale_logs_cluster(
        logs_controller=logs_controller,
        cluster_id=cluster_id,
        download=download,
        tail=tail,
        glob=effective_glob,
        node_ip=node_ip,
        instance_id=instance_id,
        worker_only=worker_only,
        head_only=head_only,
        unpack=unpack,
        ttl=ttl,
        download_dir=download_dir,
        parallelism=parallelism,
        resource_id=id if download else None,
    )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Download the logs of a workspace.",
            command="anyscale logs workspace --id expwrk_abc123 --download",
        ),
    ],
)
@log_cli.command(
    name="workspace",
    short_help="Access log files of a workspace.",
    help="Access log files of a workspace.",
    cls=AnyscaleCommand,
)
@click.option(
    "--workspace-id",
    "--id",
    "id",
    type=str,
    required=True,
    help="Provide a workspace ID.",
)
@option_download
@option_tail
@argument_glob
@option_node_ip
@option_instance_id
@option_worker_only
@option_head_only
@option_unpack_combined_logs
@option_download_dir
@option_ttl
@option_parallelism
def anyscale_logs_workspace(  # noqa: PLR0913
    id: str,  # noqa: A002
    download: bool,
    tail: int,
    # filters
    glob: Optional[str],
    node_ip: Optional[str],
    instance_id: Optional[str],
    worker_only: bool,
    head_only: bool,
    unpack: bool,
    # list files config
    ttl: int,
    # download files config
    download_dir: Optional[str],
    parallelism: int,
) -> None:
    logs_controller = LogsController()
    cluster_id = logs_controller.get_cluster_id_for_workspace(workspace_id=id)
    execute_anyscale_logs_cluster(
        logs_controller=logs_controller,
        cluster_id=cluster_id,
        download=download,
        tail=tail,
        glob=glob,
        node_ip=node_ip,
        instance_id=instance_id,
        worker_only=worker_only,
        head_only=head_only,
        unpack=unpack,
        ttl=ttl,
        download_dir=download_dir,
        parallelism=parallelism,
        resource_id=id if download else None,
    )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Print the logs of a service version.",
            command="anyscale logs service --id service2_abc123",
        ),
    ],
)
@log_cli.command(
    name="service",
    short_help="Access log files of a service for a single service version.",
    help="Access log files of a service for a single service version.",
    cls=AnyscaleCommand,
)
@click.option("--service-id", "--id", "id", type=str, required=True, help="Provide a service ID.")
@click.option(
    "--version",
    type=str,
    required=False,
    help="Service version name or ID to get logs from. If not specified, uses the latest running version.",
)
@option_download
@option_tail
@argument_glob
@option_node_ip
@option_instance_id
@option_worker_only
@option_head_only
@option_unpack_combined_logs
@option_download_dir
@option_ttl
@option_parallelism
def anyscale_logs_service(  # noqa: PLR0913
    id: str,  # noqa: A002
    version: Optional[str],
    download: bool,
    tail: int,
    # filters
    glob: Optional[str],
    node_ip: Optional[str],
    instance_id: Optional[str],
    worker_only: bool,
    head_only: bool,
    unpack: bool,
    # list files config
    ttl: int,
    # download files config
    download_dir: Optional[str],
    parallelism: int,
) -> None:
    logs_controller = LogsController()
    cluster_id = logs_controller.get_cluster_id_for_service(
        service_id=id, version_name_or_id=version
    )
    execute_anyscale_logs_cluster(
        logs_controller=logs_controller,
        cluster_id=cluster_id,
        download=download,
        tail=tail,
        glob=glob,
        node_ip=node_ip,
        instance_id=instance_id,
        worker_only=worker_only,
        head_only=head_only,
        unpack=unpack,
        ttl=ttl,
        download_dir=download_dir,
        parallelism=parallelism,
        resource_id=id if download else None,
    )


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = math.floor(math.log(size_bytes, 1024))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"
