from typing import Optional, Union

from anyscale._private.sdk import sdk_command
from anyscale.actor._private.actor_sdk import DEFAULT_MAX_ITEMS, PrivateActorSDK
from anyscale.actor.models import ActorAggregateBy, ActorAggregates
from anyscale.gpus.commands import _RESOURCE_ARG_DOCSTRINGS


_ACTOR_SDK_SINGLETON_KEY = "actor_sdk"

_AGGREGATE_EXAMPLE = """
import anyscale

groups = anyscale.actor.aggregate(by="exit_detail", job_id="prodjob_abc123")
print(f"{len(groups.results)} of {groups.total} groups")
for group in groups.results:
    print(group.death_reason, group.metrics.count_dead)
"""

_AGGREGATE_ARG_DOCSTRINGS = {
    "by": "How to group the actors: NAME, JOB or EXIT_DETAIL (case-insensitive); see "
    "ActorAggregateBy.",
    # The cluster whose actors to read: exactly one of these, the same four the node and
    # GPU commands take.
    **_RESOURCE_ARG_DOCSTRINGS,
    "ray_session": "Name of a Ray session: only its actors. None means every recent "
    "session of the cluster.",
    "max_items": "How many groups to return at most (default 100). `total` in the result "
    "says how many there are.",
    "start_cluster": "Start the cloud's system cluster when it is not running (default "
    "True), waiting up to ten minutes for it. With False, a cluster that is not running "
    "is an error instead.",
}


@sdk_command(
    _ACTOR_SDK_SINGLETON_KEY,
    PrivateActorSDK,
    doc_py_example=_AGGREGATE_EXAMPLE,
    arg_docstrings=_AGGREGATE_ARG_DOCSTRINGS,
)
def aggregate(  # noqa: PLR0913
    *,
    by: Union[str, ActorAggregateBy],
    cluster_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    job_id: Optional[str] = None,
    service_id: Optional[str] = None,
    ray_session: Optional[str] = None,
    max_items: int = DEFAULT_MAX_ITEMS,
    start_cluster: bool = True,
    _private_sdk: Optional[PrivateActorSDK] = None,
) -> ActorAggregates:
    """Group the Ray actors of a cluster, workspace, job or service by name, job or exit
    detail, with counts per state."""
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
