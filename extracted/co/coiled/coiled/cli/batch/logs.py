from __future__ import annotations

import click

from ..cluster.better_logs import better_logs
from ..utils import CONTEXT_SETTINGS
from .status import get_job_status


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("cluster", default="", required=False)
@click.option(
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified).",
)
@click.option(
    "--task",
    type=int,
    default=None,
)
def batch_logs_cli(
    cluster,
    workspace,
    task,
):
    get_logs(cluster, workspace, task, print_logs=True)


def get_logs(cluster: str | int, workspace: str | None = None, task: int | None = None, print_logs: bool = False):
    jobs, cluster_id = get_job_status(cluster=cluster, workspace=workspace)
    instance_labels_dict = {}
    show_all_instances = task is not None

    if not jobs:
        raise ValueError(f"No jobs assigned to cluster {cluster}")

    if task is not None:
        job_id = None
        vm_id = None

        for job in jobs:
            for job_task in job.get("tasks", []):
                if job_task.get("array_task_id") == task:
                    job_id = job["id"]
                    vm_id = job_task.get("assigned_to_id")
                    instance_labels_dict[vm_id] = {"label": f"Task {job_task['array_task_id']}", "color": "blue"}
                    break
            if vm_id:
                break

        if not vm_id:
            raise ValueError(f"Task {task} was not found or is not yet running")

        log_filter = f"__BATCH {job_id}.{task}__"
    else:
        job_id = jobs[0]["id"]
        log_filter = f"__BATCH {job_id}."

    return better_logs(
        cluster_id=cluster_id,
        instance_labels_dict=instance_labels_dict,
        show_label=not show_all_instances,
        show_all_instances=show_all_instances,
        filter=log_filter,
        capture_text=not print_logs,
        color=print_logs,
    )
