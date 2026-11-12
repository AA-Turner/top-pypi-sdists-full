from typing import Optional, Union

from anyscale._private.sdk import sdk_command
from anyscale.gpus.commands import _RESOURCE_ARG_DOCSTRINGS
from anyscale.task._private.task_sdk import DEFAULT_MAX_ITEMS, PrivateTaskSDK
from anyscale.task.models import TaskAggregateBy, TaskAggregates


_TASK_SDK_SINGLETON_KEY = "task_sdk"

_AGGREGATE_EXAMPLE = """
import anyscale

groups = anyscale.task.aggregate(by="exception", job_id="prodjob_abc123")
print(f"{len(groups.results)} of {groups.total} groups")
for group in groups.results:
    print(group.exception_type, group.metrics.count_failed)
"""

_AGGREGATE_ARG_DOCSTRINGS = {
    "by": "How to group the tasks: FUNCTION, JOB or EXCEPTION (case-insensitive); see "
    "TaskAggregateBy.",
    # The cluster whose tasks to read: exactly one of these, the same four the node and
    # GPU commands take.
    **_RESOURCE_ARG_DOCSTRINGS,
    "ray_session": "Name of a Ray session: only its tasks. None means every recent "
    "session of the cluster.",
    "max_items": "How many groups to return at most (default 100). `total` in the result "
    "says how many there are.",
    "start_cluster": "Start the cloud's system cluster when it is not running (default "
    "True), waiting up to ten minutes for it. With False, a cluster that is not running "
    "is an error instead.",
}


@sdk_command(
    _TASK_SDK_SINGLETON_KEY,
    PrivateTaskSDK,
    doc_py_example=_AGGREGATE_EXAMPLE,
    arg_docstrings=_AGGREGATE_ARG_DOCSTRINGS,
)
def aggregate(  # noqa: PLR0913
    *,
    by: Union[str, TaskAggregateBy],
    cluster_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    job_id: Optional[str] = None,
    service_id: Optional[str] = None,
    ray_session: Optional[str] = None,
    max_items: int = DEFAULT_MAX_ITEMS,
    start_cluster: bool = True,
    _private_sdk: Optional[PrivateTaskSDK] = None,
) -> TaskAggregates:
    """Group the Ray tasks of a cluster, workspace, job or service by function, job or
    exception, with counts and timings per group."""
    return _private_sdk.aggregate(  # type: ignore
        by=by,
        cluster_id=cluster_id,
        workspace_id=workspace_id,
        job_id=job_id,
        service_id=service_id,
        ray_session=ray_session,
        max_items=max_items,
        start_cluster=start_cluster,
    )
