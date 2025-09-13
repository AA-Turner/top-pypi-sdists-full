from __future__ import annotations

import itertools
import time
from collections import Counter

import click
from rich.align import Align
from rich.console import Console, Group
from rich.progress import BarColumn, TextColumn
from rich.status import Status

import coiled

from ..cluster.utils import find_cluster
from ..utils import CONTEXT_SETTINGS

console = Console(width=80)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", default="", required=False)
@click.option(
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified).",
)
@click.option(
    "--download",
    default=None,
)
def batch_wait_cli(
    cluster: str,
    workspace: str | None,
    download: str | None,
):
    """Monitor the progress of a Coiled Batch job."""
    with coiled.Cloud(workspace=workspace) as cloud:
        cluster_info = find_cluster(cloud, cluster)
        cluster_id = cluster_info["id"]
        jobs = coiled.batch.status(cluster=cluster_id, workspace=workspace)
        if not jobs:
            print(f"No batch jobs for cluster {cluster_id}")
            return
    batch_job_wait(cluster_id=cluster_id, workspace=workspace, download=download)


def batch_job_wait(cluster_id: int, workspace: str | None, download: str | None):
    cluster_errored = False
    with coiled.utils.SimpleRichProgressPanel(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="progress.remaining"),
        TextColumn("[progress.percentage]{task.completed}"),
        console=console,
        batch_title="",
    ) as progress:
        progress_tasks = {
            "pending": progress.add_task("[yellow]Pending"),
            "running": progress.add_task("[green]Processing"),
            "done": progress.add_task("[blue]Done"),
            "error": progress.add_task("[red]Error"),
        }
        done = False
        while not done:
            jobs = coiled.batch.status(cluster=cluster_id, workspace=workspace)
            progress.batch_title = format_batch_title(jobs)  # type: ignore
            tasks = list(itertools.chain.from_iterable(job["tasks"] for job in jobs))
            states = [task["state"] if not task["exit_code"] else "error" for task in tasks]
            counts = Counter(states)
            for state, task in progress_tasks.items():
                # show both "running" and "assigned" as "Processing..."
                state_to_show = "running" if state == "assigned" else state

                progress.update(task, total=len(tasks), completed=counts[state_to_show], refresh=True)

            all_tasks_completed = (counts["done"] + counts["error"]) == len(tasks)
            cluster_errored = jobs[0]["cluster_state"] == "error"
            done = all_tasks_completed or cluster_errored
            if not done:
                time.sleep(2)

    if download and not cluster_errored:
        attachments = coiled.filestore.wait_until_complete(cluster_id)

        if not attachments:
            print("No filestores found for this job")
            return

        for attachment in attachments:
            if attachment["output"] and attachment["primary"]:
                coiled.filestore.download_from_filestore_with_ui(
                    fs=attachment["filestore"],
                    into=download,
                )

        coiled.filestore.clear_filestores_with_ui([a["filestore"] for a in attachments if a["primary"]])


def format_batch_title(jobs):
    cluster_id = jobs[0]["cluster_id"]
    cluster_state = jobs[0]["cluster_state"]
    user_command = jobs[0]["user_command"]
    return Group(
        Align.center(
            Status(f"Monitoring jobs for cluster {cluster_id} ([bold]{cluster_state}[/bold])", spinner="dots")
        ),
        Align.center(f"[bold]Command:[/bold] [green]{user_command}[/green]"),
    )
