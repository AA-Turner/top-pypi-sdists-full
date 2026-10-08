"""Tools that restore a platform pipeline's state into the local workspace."""

from __future__ import annotations

# Python internals
from typing import Optional

# Other libraries
from dlt.common.typing import Annotated

# Current package
from dlthub_mcp._access import RESTORE_ACCESS
from dlthub_mcp._client import tool, tool_error, workspace
from dlthub_mcp._restore import RestoredPipeline, restore_pipeline
from dlthub_mcp.telemetry_tools import ACTIVITY_DAYS, _window


def _restore(
    pipeline_name: str, destination: Optional[str], dataset: Optional[str], seen: str
) -> RestoredPipeline:
    if not destination or not dataset:
        raise tool_error(
            f"Telemetry reported no destination and dataset for pipeline"
            f" {pipeline_name!r} in {seen}, so there is nothing to restore from."
        )
    return restore_pipeline(pipeline_name, destination, dataset)


@tool
def dlthub_restore_pipeline_from_run(
    run_id: str, pipeline_name: Optional[str] = None
) -> Annotated[RestoredPipeline, RESTORE_ACCESS]:
    """Restore a pipeline a job run executed, from the destination it used.

    Afterwards dlt's ``pipeline`` and ``dataset`` tools work on it by name. Call
    again to pull a newer remote state; it replaces the local one.

    Args:
        run_id: The job run's uuid, from ``dlthub_list_runs``.
        pipeline_name: Required only when the run executed several pipelines.

    Returns:
        The restored pipeline.

    Raises:
        Exception: A ``ToolError`` naming the run's pipelines when the choice is
            ambiguous, or why the restore failed.
    """
    run = workspace().job_runs.get(id=run_id)
    pipelines = {p.pipeline_name: p for p in run.pipeline_run_summaries}
    if not pipelines:
        raise tool_error(
            f"Run {run_id} executed no pipelines that telemetry reported. A run"
            " still in flight may not have reported yet."
        )
    eligible = ", ".join(sorted(pipelines))
    if pipeline_name is None:
        if len(pipelines) > 1:
            raise tool_error(
                f"Run {run_id} executed several pipelines: {eligible}. Pass"
                " pipeline_name to pick one."
            )
        (summary,) = pipelines.values()
    elif pipeline_name in pipelines:
        summary = pipelines[pipeline_name]
    else:
        raise tool_error(
            f"Run {run_id} executed no pipeline named {pipeline_name!r}. It"
            f" executed: {eligible}."
        )
    return _restore(
        summary.pipeline_name,
        summary.destination_name,
        summary.dataset_name,
        f"run {run_id}",
    )


@tool
def dlthub_restore_pipeline(
    pipeline_name: str, days: int = ACTIVITY_DAYS
) -> Annotated[RestoredPipeline, RESTORE_ACCESS]:
    """Restore a pipeline by name, from the destination its latest run used.

    Afterwards dlt's ``pipeline`` and ``dataset`` tools work on it by name. Call
    again to pull a newer remote state; it replaces the local one.

    Args:
        pipeline_name: The dlt pipeline, as ``dlthub_list_pipelines`` names it.
        days: How far back to look for its latest run, at most 365.

    Returns:
        The restored pipeline.

    Raises:
        Exception: A ``ToolError`` when telemetry saw no run in the window, or
            why the restore failed.
    """
    since, until = _window(days)
    latest = next(
        iter(
            workspace().telemetry.pipeline_runs.list(
                pipeline_name=pipeline_name, since=since, until=until, limit=1
            )
        ),
        None,
    )
    if latest is None:
        raise tool_error(
            f"Telemetry recorded no run of pipeline {pipeline_name!r} in the last"
            f" {days} days. dlthub_list_pipelines names the pipelines it has seen;"
            " dlthub_telemetry_status says whether telemetry is reporting at all."
        )
    return _restore(
        pipeline_name,
        latest.destination_name,
        latest.dataset_name,
        f"pipeline run {latest.id}",
    )


__tools__ = (dlthub_restore_pipeline_from_run, dlthub_restore_pipeline)
