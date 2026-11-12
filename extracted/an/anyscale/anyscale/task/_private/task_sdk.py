from typing import Any, Dict, Optional, Union

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale._private.workload.cluster_id import resolve_cluster_id
from anyscale._private.workload.observability_api import fetch_observability_api_json
from anyscale.task.models import (
    TaskAggregate,
    TaskAggregateBy,
    TaskAggregateMetrics,
    TaskAggregates,
    TaskExceptionAggregate,
    TaskFunctionAggregate,
    TaskJobAggregate,
)


# The design's default; the console's tab reads 20 per page.
DEFAULT_MAX_ITEMS = 100

# The observability API path of each grouping, under /clusters/{cluster_id}/.
_PATHS = {
    TaskAggregateBy.FUNCTION: "get_task_function_aggregates",
    TaskAggregateBy.JOB: "get_task_job_aggregates",
    TaskAggregateBy.EXCEPTION: "get_task_exception_aggregates",
}


class PrivateTaskSDK(BaseSDK):
    def aggregate(  # noqa: PLR0913
        self,
        *,
        by: Union[str, TaskAggregateBy],
        cluster_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        job_id: Optional[str] = None,
        service_id: Optional[str] = None,
        ray_session: Optional[str] = None,
        max_items: int = DEFAULT_MAX_ITEMS,
        start_cluster: bool = True,
    ) -> TaskAggregates:
        """The first `max_items` task groups of the cluster, plus how many there are.

        The cluster is named by exactly one of the four IDs; see resolve_cluster_id. The
        data is read from the cloud's system cluster, started first when `start_cluster`
        (see observability_api). One request: the API groups every task attempt of the
        cluster, or of `ray_session` alone, and returns the first page.
        """
        grouping = TaskAggregateBy.validate(by)
        if isinstance(max_items, bool) or not isinstance(max_items, int) or max_items < 1:
            raise ValueError("max_items must be a positive int.")
        resolved = resolve_cluster_id(
            self.client,
            cluster_id=cluster_id,
            workspace_id=workspace_id,
            job_id=job_id,
            service_id=service_id,
        )
        params: Dict[str, Any] = {"offset": 0, "page_size": max_items}
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
        results = [_to_group(grouping, item) for item in raw.get("results") or []]
        total = raw.get("total")
        return TaskAggregates(
            by=grouping,
            results=results,
            total=total if total is not None else len(results),
            warning=raw.get("warning"),
        )


def _to_group(by: TaskAggregateBy, raw: Dict[str, Any]) -> TaskAggregate:
    metrics = TaskAggregateMetrics(**(raw.get("metrics") or {}))
    session = raw.get("ray_session_name") or ""
    if by == TaskAggregateBy.FUNCTION:
        return TaskFunctionAggregate(
            function_name=raw.get("function_name"),
            task_type=raw["task_type"],
            ray_session_name=session,
            metrics=metrics,
        )
    if by == TaskAggregateBy.JOB:
        return TaskJobAggregate(
            job_id=raw.get("job_id") or "", ray_session_name=session, metrics=metrics
        )
    return TaskExceptionAggregate(
        exception_type=raw.get("exception_type") or "",
        ray_session_name=session,
        metrics=metrics,
    )
