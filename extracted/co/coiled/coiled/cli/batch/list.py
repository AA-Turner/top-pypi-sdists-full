from __future__ import annotations

from typing import Literal

import click
from rich import print, table

import coiled
from coiled.cli.curl import sync_request

from ..utils import CONTEXT_SETTINGS, format_dt

STATE_COLORS = {
    "pending": "yellow",
    "assigned": "green",
    "error": "red",
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified).",
)
@click.option("--format", default="table", type=click.Choice(["json", "table"]))
@click.option("--limit", default=10, type=int)
def batch_list_cli(
    workspace: str | None,
    format: Literal["table", "json"],
    limit: int,
):
    """List Coiled Batch jobs in a workspace."""
    jobs = get_job_list(workspace=workspace, limit=limit)
    print_job_list(jobs=jobs, format=format)


def print_job_list(jobs: list[dict], format: Literal["table", "json"]) -> None:
    if format == "json":
        print(jobs)
    else:
        if not jobs:
            print("No batch jobs found")
            return

        show_workspace = len({job["workspace_name"] for job in jobs}) > 1

        t = table.Table()
        t.add_column(
            "ID",
        )
        if show_workspace:
            t.add_column("Workspace")
        t.add_column("State", justify="center")
        t.add_column("Tasks Done", justify="right")
        t.add_column("Submitted", justify="right")
        # t.add_column("Started", justify="right")
        t.add_column("Finished", justify="right")
        t.add_column("Approx Cloud Cost", justify="right")
        t.add_column("Command")

        for job in jobs:
            if job["n_tasks_failed"]:
                if job["n_tasks_succeeded"]:
                    tasks_done = f"{job['n_tasks_succeeded']} + [red]{job['n_tasks_failed']}[/red]"
                    tasks_done = f"{tasks_done:4}"
                else:
                    tasks_done = f"[red]{job['n_tasks_failed']:4}[/red]"
            else:
                tasks_done = f"{job['n_tasks_succeeded']:4}"

            tasks_done = f"{tasks_done} /{job['n_tasks']:4}"
            if job["n_tasks_succeeded"] == job["n_tasks"]:
                tasks_done = f"[green]{tasks_done}[/green]"

            row_data = [str(job["cluster_id"] or "")]

            if show_workspace:
                row_data.append(str(job["workspace_name"] or ""))

            row_data.extend([
                str(job["state"] or ""),
                tasks_done,
                format_dt(job["created"]),
                format_dt(job["completed"]),
                f"${job['approximate_cloud_total_cost']:.2f}" if job["approximate_cloud_total_cost"] else "",
                job["user_command"],
            ])

            t.add_row(*row_data)
        print(t)


def get_job_list(workspace: str | None, limit: int) -> list[dict]:
    with coiled.Cloud(workspace=workspace) as cloud:
        url = f"{cloud.server}/api/v2/jobs/?workspace={workspace or ''}&limit={limit or ''}"
        response = sync_request(
            cloud=cloud,
            url=url,
            method="get",
            data=None,
            json_output=True,
        )
        if not response:
            return []
        else:
            return response.get("items", [])
