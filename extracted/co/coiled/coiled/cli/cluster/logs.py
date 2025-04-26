import shutil
import subprocess
import sys
from datetime import datetime
from typing import Optional

import click
from rich import print

import coiled

from ..utils import CONTEXT_SETTINGS


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster")
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
@click.option(
    "--scheduler",
    default=False,
    is_flag=True,
    help="Get scheduler logs",
)
@click.option(
    "--workers",
    help="Get worker logs ('any', 'all', or comma-delimited list of names, states, or internal IP addresses)",
)
@click.option(
    "--follow",
    default=False,
    is_flag=True,
    help="Passed directly to `aws logs tail`, see aws cli docs for details.",
)
@click.option(
    "--filter",
    default=None,
    help="Passed directly to `aws logs tail`, see aws cli docs for details.",
)
@click.option(
    "--since",
    default=None,
    help="For follow, uses `aws logs tail` default (10m), otherwise defaults to start time of cluster.",
)
@click.option(
    "--format",
    default=None,
    help="Passed directly to `aws logs tail`, see aws cli docs for details.",
)
@click.option(
    "--profile",
    default=None,
    help="Passed directly to `aws logs tail`, see aws cli docs for details.",
)
def logs(
    cluster: str,
    account: Optional[str],
    scheduler: bool,
    workers: Optional[str],
    follow: bool,
    filter: Optional[str],
    since: Optional[str],
    format: Optional[str],
    profile: Optional[str],
):
    do_logs(cluster, account, scheduler, workers, follow, filter, since, format, profile)


def do_logs(
    cluster: str,
    account: Optional[str],
    scheduler: bool,
    workers: Optional[str],
    follow: bool,
    filter: Optional[str],
    since: Optional[str],
    format: Optional[str],
    profile: Optional[str],
    capture: bool = False,
):
    aws_path = shutil.which("aws")
    if not aws_path:
        raise click.ClickException("`coiled cluster logs` relies on AWS CLI.")

    with coiled.Cloud(account=account) as cloud:
        if cluster.isnumeric():
            cluster_id = int(cluster)
        else:
            try:
                clusters = cloud.get_clusters_by_name(name=cluster)
                if clusters:
                    recent_cluster = clusters[-1]
                else:
                    raise click.ClickException(f"Unable to find cluster with name '{cluster}'")

                if follow and recent_cluster["current_state"]["state"] in (
                    "stopped",
                    "error",
                ):
                    follow = False
                    print(
                        f"[red]Cluster state is {recent_cluster['current_state']['state']} so not following.[/red]",
                        file=sys.stderr,
                    )

                cluster_id = recent_cluster["id"]

            except coiled.errors.DoesNotExist:
                cluster_id = None

        if not cluster_id:
            raise click.ClickException(f"Unable to find cluster `{cluster}`")

        cluster_info = cloud.cluster_details(cluster_id)

        # for tailing, use aws default (10m) but allow "start"; for non-tailing, default to start of cluster
        if (since is None and not follow) or since == "start":
            cluster_start_ts = datetime.fromisoformat(cluster_info["created"]).timestamp()
            since = str(int(cluster_start_ts))

        if workers:
            worker_attrs_to_match = workers.split(",")

            def filter_worker(idx, worker):
                if workers == "all":
                    return True
                elif workers == "any":
                    if idx == 0:
                        return True
                else:
                    if worker.get("name") and worker["name"] in worker_attrs_to_match:
                        return True
                    elif (
                        worker.get("instance", {}).get("private_ip_address")
                        and worker["instance"]["private_ip_address"] in worker_attrs_to_match
                    ):
                        return True
                    elif (
                        worker.get("current_state", {}).get("state")
                        and worker["current_state"]["state"] in worker_attrs_to_match
                    ):
                        return True

                return False

            worker_names = [
                worker["name"] for i, worker in enumerate(cluster_info["workers"]) if filter_worker(i, worker)
            ]
        else:
            worker_names = []

        log_info = cloud.get_cluster_log_info(cluster_id)

        if log_info["type"] == "vm_aws":
            group_name = log_info["log_group"]
            region = log_info["region"]

            stream_names = []

            if not group_name:
                raise click.ClickException("Unable to find CloudWatch Log Group for this cluster.")

            if scheduler:
                stream_names.append(log_info["scheduler_stream"])

            if workers:
                worker_stream_name = [log_info["worker_streams"][worker_name] for worker_name in worker_names]
                stream_names.extend(worker_stream_name)

            if not stream_names:
                raise click.ClickException(
                    "No CloudWatch Log Streams to show, use `--scheduler` or `--workers` to select streams."
                )  # FIXME better error

            streams = " ".join(stream_names)

            command = [aws_path, "logs", "tail", group_name, "--region", region, "--log-stream-names", streams]
            if follow:
                command.append("--follow")
            if filter:
                command += ["--filter", filter]
            if since:
                command += ["--since", since]
            if format:
                command += ["--format", format]
            if profile:
                command += ["--profile", profile]

            return subprocess.run(command, capture_output=capture)

            # TODO `aws logs tail` gives ResourceNotFoundException error ("The specified log stream does not exist.")
            #   when *any* of the log streams doesn't exist. We should query to see which exist before trying to tail.

        else:
            raise click.ClickException(f"Cluster backend type is {log_info['type']}, only AWS is currently supported.")
