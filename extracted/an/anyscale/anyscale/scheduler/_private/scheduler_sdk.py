from typing import Any, Dict, List, Optional, Union

from anyscale._private.models.model_base import ResultIterator
from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale._private.workload.cluster_id import resolve_cluster_id
from anyscale.client.openapi_client.models.apply_scheduler_config_request import (
    ApplySchedulerConfigRequest,
)
from anyscale.client.openapi_client.models.consumer_response import ConsumerResponse
from anyscale.client.openapi_client.models.overview_response import OverviewResponse
from anyscale.client.openapi_client.models.queue_row_response import QueueRowResponse
from anyscale.client.openapi_client.models.rollback_scheduler_config_request import (
    RollbackSchedulerConfigRequest,
)
from anyscale.client.openapi_client.models.scheduler_config import (
    SchedulerConfig as APISchedulerConfig,
)
from anyscale.client.openapi_client.models.scheduler_config_response import (
    SchedulerConfigResponse,
)
from anyscale.client.openapi_client.models.scheduler_config_version_summary import (
    SchedulerConfigVersionSummary as APISchedulerConfigVersionSummary,
)
from anyscale.client.openapi_client.models.workload_response import WorkloadResponse
from anyscale.scheduler.models import (
    QueueWorkload,
    QueueWorkloadList,
    ResourceQueueStatus,
    ResourceQueueStatusPage,
    SchedulerConfig,
    SchedulerConfigVersion,
    SchedulerConfigVersionSummary,
    SchedulerOverview,
    TopConsumer,
    WorkloadState,
    WorkloadStatus,
)


# Backend per-page cap; the API rejects count > 50.
_PAGE_SIZE_CAP = 50

# The queue read APIs: the backend's own page size when none is sent, and its cap.
DEFAULT_MAX_QUEUES = 50
MAX_QUEUES = 200
DEFAULT_MAX_WORKLOADS = 100
MAX_WORKLOADS = 1000
DEFAULT_MAX_CONSUMERS = 10
MAX_CONSUMERS = 100

_WORKLOAD_ID_ARGS = "cluster_id, workspace_id, job_id or service_id"


class PrivateSchedulerSDK(BaseSDK):
    def apply_config(
        self,
        config: Union[SchedulerConfig, Dict[str, Any]],
    ) -> int:
        request = ApplySchedulerConfigRequest(
            config=_to_api_config(config),
        )
        response = self.client.apply_scheduler_config(request)
        return response.version

    def rollback_config(
        self,
        version: int,
    ) -> int:
        request = RollbackSchedulerConfigRequest(version=version)
        response = self.client.rollback_scheduler_config(request)
        return response.version

    def get_config(
        self,
        version: Optional[int] = None,
    ) -> SchedulerConfigVersion:
        if version is None:
            response = self.client.get_active_scheduler_config()
        else:
            response = self.client.get_scheduler_config_version(version)
        return _from_api_response(response)

    def list_config_versions(
        self,
        max_items: int = 10,
    ) -> List[SchedulerConfigVersionSummary]:
        page_size = min(max_items, _PAGE_SIZE_CAP) if max_items > 0 else 0

        def _fetch_page(token: Optional[str]):
            return self.client.list_scheduler_config_versions(
                count=page_size,
                paging_token=token,
            )

        return list(
            ResultIterator(
                page_token=None,
                max_items=max_items,
                fetch_page=_fetch_page,
                parse_fn=_from_api_summary,
            )
        )

    # ---- Queues (live state) ----

    def list_queues(
        self,
        *,
        max_items: int = DEFAULT_MAX_QUEUES,
        page_token: Optional[str] = None,
    ) -> ResourceQueueStatusPage:
        """One page of the org's active queues, and the token for the next page."""
        _check_max_items(max_items, MAX_QUEUES)
        raw = self.client.list_scheduler_queues(limit=max_items, paging_token=page_token)
        return ResourceQueueStatusPage(
            results=[_to_queue(queue) for queue in raw.results or []],
            next_page_token=_next_paging_token(raw),
        )

    def get_queue(self, name: str) -> ResourceQueueStatus:
        """The active queue with this name.

        The API addresses a queue by ID, and the ID is only in the queue list, so the name
        is looked up there. A name belongs to at most one of an org's active queues. The
        row of the list is returned as it is: it carries everything the API's single-queue
        read does, plus the queue's cohort and quota use.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string.")
        page_token: Optional[str] = None
        seen_tokens = set()
        while True:
            raw = self.client.list_scheduler_queues(limit=MAX_QUEUES, paging_token=page_token)
            for queue in raw.results or []:
                if queue.queue == name:
                    return _to_queue(queue)
            page_token = _next_paging_token(raw)
            # A token the backend already gave would loop forever.
            if page_token is None or page_token in seen_tokens:
                break
            seen_tokens.add(page_token)
        raise ValueError(
            f"Resource queue '{name}' not found. Run `anyscale scheduler queue list` to see "
            "the active queues."
        )

    def list_queue_workloads(  # noqa: PLR0913
        self,
        name: str,
        *,
        state: Union[WorkloadState, str],
        max_items: int = DEFAULT_MAX_WORKLOADS,
        cluster_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        job_id: Optional[str] = None,
        service_id: Optional[str] = None,
    ) -> QueueWorkloadList:
        """The pending or running workloads of a queue, in the scheduler's order.

        With one of the four IDs, only the rows of that workload's cluster. The API
        identifies a workload by its cluster and has no filter, so the cluster is looked up
        (see resolve_cluster_id) and the rows are matched here.

        The API returns at most MAX_WORKLOADS rows and has no cursor. When the queue holds
        more and the workload is not among the rows read, this raises RuntimeError: the
        workload may be in the rows that cannot be read, so an empty list would be wrong.

        When the result holds fewer workloads than `total`, a warning says so.
        """
        _check_max_items(max_items, MAX_WORKLOADS)
        wire_state = WorkloadState.validate(state).value
        ids = {
            "cluster_id": cluster_id,
            "workspace_id": workspace_id,
            "job_id": job_id,
            "service_id": service_id,
        }
        # Given means "not None". An empty ID is an error, not "no filter": a caller whose
        # ID variable is unset must not get the whole queue back.
        given = {key: value for key, value in ids.items() if value is not None}
        if len(given) > 1:
            raise ValueError(f"At most one of {_WORKLOAD_ID_ARGS} can be given.")
        for key, value in given.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{key} must be a non-empty string.")
        queue = self.get_queue(name)

        if not given:
            raw = self.client.list_scheduler_queue_workloads(
                queue.queue_id, state=wire_state, limit=max_items
            )
            results = [_to_workload(workload) for workload in raw.results or []]
            page = QueueWorkloadList(results=results, total=_total(raw, len(results)))
            self._warn_if_cut(page, name, wire_state, max_items)
            return page

        target = resolve_cluster_id(self.client, **given)
        # The API has no cursor either: its cap is all that can be read, so read that much.
        raw = self.client.list_scheduler_queue_workloads(
            queue.queue_id, state=wire_state, limit=MAX_WORKLOADS
        )
        rows = raw.results or []
        in_queue = _total(raw, len(rows))
        matches = [_to_workload(workload) for workload in rows if workload.cluster_id == target]
        if in_queue > len(rows):
            if not matches:
                # The workload may be in the rows past the cap, which cannot be read. An
                # empty list would say "not in this queue", and that is not known.
                raise RuntimeError(
                    f"Queue '{name}' has {in_queue} {wire_state} workloads, more than the "
                    f"{len(rows)} the API returns. The workload is not in the first "
                    f"{len(rows)}, and the rest cannot be searched."
                )
            self.logger.warning(
                f"Queue '{name}' has {in_queue} {wire_state} workloads. Only the first "
                f"{len(rows)} were searched."
            )
        page = QueueWorkloadList(results=matches[:max_items], total=len(matches))
        self._warn_if_cut(page, name, wire_state, max_items)
        return page

    def _warn_if_cut(
        self, page: QueueWorkloadList, name: str, wire_state: str, max_items: int
    ) -> None:
        """Warn when the result holds fewer workloads than there are.

        `total` already carries the full count. The warning is for a caller that reads
        only `results`, and it is what the CLI shows on stderr in every output format.
        """
        if page.total <= len(page.results):
            return
        more = (
            " Raise max_items to see more."
            if max_items < MAX_WORKLOADS
            else f" At most {MAX_WORKLOADS} can be returned."
        )
        self.logger.warning(
            f"Showing {len(page.results)} of {page.total} {wire_state} workloads of queue "
            f"'{name}'.{more}"
        )

    def get_overview(self) -> SchedulerOverview:
        """The org-wide rollup: totals, quota use, per-cloud totals and topology."""
        return _to_overview(self.client.get_scheduler_overview())

    def list_top_consumers(
        self,
        *,
        max_items: int = DEFAULT_MAX_CONSUMERS,
        queue: Optional[str] = None,
    ) -> List[TopConsumer]:
        """The clusters that hold the most nodes, org-wide or in the queue named `queue`."""
        _check_max_items(max_items, MAX_CONSUMERS)
        queue_id = self.get_queue(queue).queue_id if queue is not None else None
        raw = self.client.list_scheduler_top_consumers(limit=max_items, queue_id=queue_id)
        return [_to_consumer(consumer) for consumer in raw or []]


def _to_api_config(
    config: Union[SchedulerConfig, Dict[str, Any]],
) -> APISchedulerConfig:
    if isinstance(config, SchedulerConfig):
        return APISchedulerConfig(**config.to_dict(exclude_none=True))
    if isinstance(config, dict):
        # Validate locally before sending; raises on schema errors with field path.
        return APISchedulerConfig(**SchedulerConfig.from_dict(config).to_dict(exclude_none=True))
    raise TypeError(f"config must be SchedulerConfig or dict, got {type(config).__name__}.")


def _from_api_response(response: SchedulerConfigResponse) -> SchedulerConfigVersion:
    config_dict = (
        response.config.to_dict() if hasattr(response.config, "to_dict") else response.config
    )
    return SchedulerConfigVersion(
        version=response.version,
        is_active=response.is_active,
        created_at=response.created_at,
        creator_id=response.creator_id,
        config=SchedulerConfig.from_api_dict(config_dict),
    )


def _from_api_summary(
    summary: APISchedulerConfigVersionSummary,
) -> SchedulerConfigVersionSummary:
    return SchedulerConfigVersionSummary(
        version=summary.version,
        created_at=summary.created_at,
        creator_id=summary.creator_id,
    )


def _check_max_items(max_items: int, cap: int) -> None:
    if isinstance(max_items, bool) or not isinstance(max_items, int):
        raise ValueError("max_items must be an int.")
    if not 1 <= max_items <= cap:
        raise ValueError(f"max_items must be between 1 and {cap}.")


def _next_paging_token(raw: Any) -> Optional[str]:
    # The backend sends no token, or an empty one, on the last page.
    return (raw.metadata.next_paging_token if raw.metadata else None) or None


def _total(raw: Any, fallback: int) -> int:
    total = raw.metadata.total if raw.metadata else None
    return total if total is not None else fallback


def _to_queue(raw: QueueRowResponse) -> ResourceQueueStatus:
    return ResourceQueueStatus.from_dict(raw.to_dict())


def _to_workload(raw: WorkloadResponse) -> QueueWorkload:
    plain = raw.to_dict()
    plain["status"] = _to_status(plain.get("status"))
    return QueueWorkload.from_dict(plain)


def _to_status(value: Any) -> WorkloadStatus:
    # The backend reports a status it does not know as UNSPECIFIED. A status this CLI
    # does not know yet is read the same way, so a newer backend does not break the list.
    try:
        return WorkloadStatus.validate(str(value))
    except ValueError:
        return WorkloadStatus.UNSPECIFIED


def _to_overview(raw: OverviewResponse) -> SchedulerOverview:
    return SchedulerOverview.from_dict(raw.to_dict())


def _to_consumer(raw: ConsumerResponse) -> TopConsumer:
    return TopConsumer.from_dict(raw.to_dict())
