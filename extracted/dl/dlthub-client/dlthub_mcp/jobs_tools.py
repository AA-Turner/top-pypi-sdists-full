"""Read-only tools over the jobs a workspace deploys and the runs they produced.

A **job** is one deployed unit of work — what the platform API calls a script. A
**run** is one execution of a job.
"""

from __future__ import annotations

# Python internals
from typing import Optional

# Other libraries
from dlt.common.typing import Annotated

# Current package
from dlthub_mcp._access import CONTEXT_READ
from dlthub_mcp._client import tool, workspace
from dlthub_mcp._paging import PAGE_SIZE, page, skip
from dlthub_sdk import Job, JobRun, Sync


@tool
def dlthub_list_jobs(
    archived: bool = False, limit: int = PAGE_SIZE, offset: int = 0
) -> Annotated[list[Job[Sync]], CONTEXT_READ]:
    """List the jobs deployed in this workspace.

    Reach for this to learn what the workspace is *meant* to do, including jobs
    that have never run; comparing it against ``dlthub_list_runs`` is how a job
    that went quiet shows up. Page with ``offset``; fewer rows than ``limit``
    means there are no more.

    Args:
        archived: List archived jobs instead of live ones. A module deploy
            archives a job its manifest no longer names.
        limit: How many jobs to return, at most 100.
        offset: How many jobs to skip, for paging.

    Returns:
        Jobs with their ref, type, paused state and version.
    """
    return list(
        workspace().jobs.list(archived=archived, limit=page(limit), offset=skip(offset))
    )


@tool
def dlthub_get_job(job_ref: str) -> Annotated[Job[Sync], CONTEXT_READ]:
    """One job in full, definition included.

    Reach for this once a listing or a run names a job worth understanding: it
    carries the triggers the platform computed, when the schedule fires next, and
    the job definition exactly as the manifest deployed it. Costs one call per
    job, so call it for the jobs you will actually reason about.

    Args:
        job_ref: The ``job_ref`` a job or run carries, or the job's uuid.

    Returns:
        The job, with its triggers, next scheduled run and definition.
    """
    return workspace().jobs.get(ref=job_ref)


@tool
def dlthub_list_runs(
    job: Optional[str] = None, limit: int = PAGE_SIZE, offset: int = 0
) -> Annotated[list[JobRun[Sync]], CONTEXT_READ]:
    """List this workspace's runs, newest first.

    The cheapest overview of what actually happened, and where a run id comes
    from. Page with ``offset``; fewer rows than ``limit`` means there are no
    more.

    Args:
        job: Limit to one job, by the ``job_ref`` from ``dlthub_list_jobs``.
            Omit for every job in the workspace.
        limit: How many runs to return, at most 100.
        offset: How many runs to skip, for paging.

    Returns:
        Runs with their number, status, trigger and timings.
    """
    runs = workspace().jobs.get(ref=job).runs if job else workspace().job_runs
    return list(runs.list(limit=page(limit), offset=skip(offset)))


@tool
def dlthub_get_run(run_id: str) -> Annotated[JobRun[Sync], CONTEXT_READ]:
    """One run in full: status, timings, trigger and the pipelines it executed.

    Reach for this for the runs you will actually mention, not for every row of a
    listing — it costs one call each. A run is addressed by uuid and nothing
    else; the platform offers no lookup by number, so take the id from
    ``dlthub_list_runs``.

    Args:
        run_id: The run's uuid, from ``dlthub_list_runs``.

    Returns:
        The run, with its number, status, trigger, timings, data interval, and
        the dlt pipelines it executed with their dataset, destination and row
        counts. Telemetry fills the pipelines in after they report, so a run
        still in flight may show none.
    """
    return workspace().job_runs.get(id=run_id)


__tools__ = (dlthub_list_jobs, dlthub_get_job, dlthub_list_runs, dlthub_get_run)
