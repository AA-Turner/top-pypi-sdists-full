from typing import Any, Dict, Optional, Union

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale._private.workload.cluster_id import resolve_cluster_id
from anyscale._private.workload.observability_api import fetch_observability_api_json
from anyscale.actor.models import (
    ActorAggregate,
    ActorAggregateBy,
    ActorAggregateMetrics,
    ActorAggregates,
    ActorExitDetailAggregate,
    ActorJobAggregate,
    ActorNameAggregate,
)


# The design's default. The API does not page actors: it returns every group, and the
# SDK keeps the first `max_items`.
DEFAULT_MAX_ITEMS = 100

# The observability API path of each grouping, under /clusters/{cluster_id}/.
_PATHS = {
    ActorAggregateBy.NAME: "get_actor_name_aggregates",
    ActorAggregateBy.JOB: "get_actor_job_aggregates",
    ActorAggregateBy.EXIT_DETAIL: "get_actor_exit_detail_aggregates",
}


class PrivateActorSDK(BaseSDK):
    def aggregate(  # noqa: PLR0913
        self,
        *,
        by: Union[str, ActorAggregateBy],
        cluster_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        job_id: Optional[str] = None,
        service_id: Optional[str] = None,
        ray_session: Optional[str] = None,
        max_items: int = DEFAULT_MAX_ITEMS,
        start_cluster: bool = True,
    ) -> ActorAggregates:
        """The first `max_items` actor groups of the cluster, plus how many there are.

        The cluster is named by exactly one of the four IDs; see resolve_cluster_id. The
        data is read from the cloud's system cluster, started first when `start_cluster`
        (see observability_api). One request: the API groups every actor of the cluster,
        or of `ray_session` alone, and returns all of the groups.
        """
        grouping = ActorAggregateBy.validate(by)
        if isinstance(max_items, bool) or not isinstance(max_items, int) or max_items < 1:
            raise ValueError("max_items must be a positive int.")
        resolved = resolve_cluster_id(
            self.client,
            cluster_id=cluster_id,
            workspace_id=workspace_id,
            job_id=job_id,
            service_id=service_id,
        )
        params: Dict[str, Any] = {}
        if ray_session is not None:
            params["ray_session_name"] = ray_session
        raw = fetch_observability_api_json(
            self.client,
            self.logger,
            self.timer,
            cluster_id=resolved,
            path=_PATHS[grouping],
            params=params,
            start_cluster=start_cluster,
        )
        groups = [_to_group(grouping, item) for item in raw.get("results") or []]
        return ActorAggregates(
            by=grouping,
            results=groups[:max_items],
            total=len(groups),
            warning=raw.get("warning"),
        )


def _to_group(by: ActorAggregateBy, raw: Dict[str, Any]) -> ActorAggregate:
    metrics = ActorAggregateMetrics(**(raw.get("metrics") or {}))
    session = raw.get("ray_session_name") or ""
    if by == ActorAggregateBy.NAME:
        return ActorNameAggregate(
            name=raw.get("name"),
            class_name=raw.get("class_name"),
            ray_session_name=session,
            metrics=metrics,
        )
    if by == ActorAggregateBy.JOB:
        return ActorJobAggregate(
            job_id=raw.get("job_id") or "", ray_session_name=session, metrics=metrics
        )
    return ActorExitDetailAggregate(
        death_reason=raw.get("death_reason") or "",
        error_message=raw.get("error_message") or "",
        ray_session_name=session,
        metrics=metrics,
    )
