from __future__ import annotations

from datetime import datetime
from typing import Literal

import click
from rich import print, table

import coiled
from coiled.cli.curl import sync_request

from ..cluster.utils import find_cluster
from ..utils import CONTEXT_SETTINGS, format_dt

STATE_COLORS = {
    "pending": "yellow",
    "assigned": "green",
    "error": "red",
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", default="", required=False)
@click.option(
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified).",
)
@click.option("--format", default="table", type=click.Choice(["json", "table"]))
@click.option("--sort", default=None)
def batch_status_cli(
    cluster: str,
    workspace: str | None,
    format: Literal["table", "json"],
    sort: str,
):
    """Check the status of a Coiled Batch job."""
    jobs, cluster_id = get_job_status(cluster=cluster, workspace=workspace)
    print_job_status(jobs=jobs, format=format, cluster=cluster or cluster_id, sort=sort.split(",") if sort else None)


def format_duration_seconds(n):
    if n > 24 * 60 * 60 * 2:
        d = int(n / 3600 / 24)
        h = int((n - d * 3600 * 24) / 3600)
        return f"{d}d {h}hr"
    if n > 60 * 60 * 2:
        h = int(n / 3600)
        m = int((n - h * 3600) / 60)
        return f"{h}hr {m}m"
    if n > 60 * 10:
        m = int(n / 60)
        s = int(n - m * 60)
        return f"{m}m {s}s"

    return f"{n}s"


def print_job_status(jobs: list[dict], format: Literal["table", "json"], cluster: str | int, sort=None) -> None:
    if sort:
        for job in jobs:
            job["tasks"].sort(key=lambda task: [task.get(sort_key) for sort_key in sort])

    if format == "json":
        print(jobs)
    else:
        if not jobs:
            print(f"No batch jobs for cluster {cluster}")
            return

        cluster_state = jobs[0]["cluster_state"]
        user_command = jobs[0]["user_command"]

        t = table.Table(
            title=(
                f"Batch Jobs for Cluster {cluster} ([bold]{cluster_state}[/bold])\n"
                f"[bold]Command:[/bold] [green]{user_command}[/green]"
            )
        )
        t.add_column("Array ID")
        t.add_column("Assigned To")
        t.add_column("State")
        t.add_column("Start Time")
        t.add_column("Stop Time")
        t.add_column("Duration")
        t.add_column("Exit Code")

        for job in jobs:
            for task in job["tasks"]:
                if task["start"] and task["stop"]:
                    start = datetime.fromisoformat(task["start"])
                    stop = datetime.fromisoformat(task["stop"])
                    duration = format_duration_seconds(int((stop - start).total_seconds()))
                else:
                    duration = ""

                state_color = STATE_COLORS.get(task["state"])
                if task["exit_code"]:
                    state_color = "red"

                state = f"[{state_color}]{task['state']}[/{state_color}]" if state_color else task["state"]
                exit_code = (
                    ""
                    if task["exit_code"] is None
                    else (f"[red]{task['exit_code']}[/red]" if task["exit_code"] else str(task["exit_code"]))
                )

                t.add_row(
                    str(task["array_task_id"]),
                    task["assigned_to"]["private_ip_address"] if task["assigned_to"] else "",
                    state,
                    format_dt(task["start"]),
                    format_dt(task["stop"]),
                    duration,
                    exit_code,
                )
        print(t)


def get_job_status(cluster: str | int, workspace: str | None):
    with coiled.Cloud(workspace=workspace) as cloud:
        cluster_info = find_cluster(cloud, cluster)
        cluster_id = cluster_info["id"]

        url = f"{cloud.server}/api/v2/jobs/cluster/{cluster_id}"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="get",
            data=None,
            json_output=True,
        )
        return response or [], cluster_id
