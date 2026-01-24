from typing import Dict, List, Optional

from anyscale._private.models.model_base import ResultIterator
from anyscale._private.workload import WorkloadSDK
from anyscale.client.openapi_client.models.decorated_job_queue import DecoratedJobQueue
from anyscale.client.openapi_client.models.decoratedjobqueue_list_response import (
    DecoratedjobqueueListResponse,
)
from anyscale.client.openapi_client.models.job_queue_sort_directive import (
    JobQueueSortDirective,
)
from anyscale.client.openapi_client.models.list_response_metadata import (
    ListResponseMetadata,
)
from anyscale.client.openapi_client.models.resource_tag_resource_type import (
    ResourceTagResourceType,
)
from anyscale.client.openapi_client.models.session_state import SessionState
from anyscale.job_queue.models import JobQueueStatus


class PrivateJobQueueSDK(WorkloadSDK):
    """Internal SDK logic for Job Queue operations."""

    def list(
        self,
        *,
        job_queue_id: Optional[str] = None,
        name: Optional[str] = None,
        creator_id: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        cluster_status: Optional[SessionState] = None,
        tags_filter: Optional[Dict[str, List[str]]] = None,
        page_size: Optional[int] = None,
        max_items: Optional[int] = None,
        sorting_directives: Optional[List[JobQueueSortDirective]] = None,
    ) -> ResultIterator[JobQueueStatus]:
        """List job queues based on specified filters and pagination.

        If job_queue_id is provided, fetches only that specific job queue.
        """

        if job_queue_id is not None:
            raw = self._resolve_to_job_queue_model(job_queue_id=job_queue_id)

            def _fetch_single_page(
                _token: Optional[str],
            ) -> DecoratedjobqueueListResponse:
                # Only return data on the first call (token=None), simulate single-item page
                if _token is None and raw is not None:
                    results = [raw]
                    metadata = ListResponseMetadata(total=1, next_paging_token=None)
                else:
                    results = []
                    metadata = ListResponseMetadata(total=0, next_paging_token=None)

                return DecoratedjobqueueListResponse(
                    results=results, metadata=metadata,
                )

            return ResultIterator(
                page_token=None,
                max_items=1,  # Return the single fetched item
                fetch_page=_fetch_single_page,
                parse_fn=_parse_decorated_jq_to_status,
            )

        def _fetch_page(token: Optional[str]) -> DecoratedjobqueueListResponse:
            return self.client.list_job_queues(
                name=name,
                creator_id=creator_id,
                cloud=cloud,
                project=project,
                cluster_status=cluster_status,
                tags_filter=tags_filter,
                count=page_size,
                paging_token=token,
                sorting_directives=sorting_directives,
            )

        return ResultIterator(
            page_token=None,
            max_items=max_items,
            fetch_page=_fetch_page,
            parse_fn=_parse_decorated_jq_to_status,
        )

    def status(self, job_queue_id: str) -> JobQueueStatus:
        """Get the status and details for a specific job queue."""
        raw = self._resolve_to_job_queue_model(job_queue_id=job_queue_id)
        return _parse_decorated_jq_to_status(raw)

    def update(
        self,
        *,
        job_queue_id: Optional[str] = None,
        job_queue_name: Optional[str] = None,
        max_concurrency: Optional[int] = None,
        idle_timeout_s: Optional[int] = None,
    ) -> JobQueueStatus:
        """Update a job queue."""

        if max_concurrency is None and idle_timeout_s is None:
            raise ValueError("No fields to update")

        jq = self._resolve_to_job_queue_model(
            job_queue_id=job_queue_id, name=job_queue_name
        )

        assert jq.id is not None
        updated_jq = self.client.update_job_queue(
            job_queue_id=jq.id,
            max_concurrency=max_concurrency,
            idle_timeout_s=idle_timeout_s,
        )

        return _parse_decorated_jq_to_status(updated_jq)

    def add_tags(
        self,
        *,
        job_queue_id: Optional[str] = None,
        name: Optional[str] = None,
        tags: Dict[str, str],
    ) -> None:
        if not tags:
            raise ValueError("At least one tag must be provided.")

        if job_queue_id is not None:
            resource_id = job_queue_id
        else:
            if name is None:
                raise ValueError("Either 'job_queue_id' or 'name' must be provided.")
            jq = self._resolve_to_job_queue_model(job_queue_id=None, name=name)
            if jq.id is None:
                raise RuntimeError(f"Job queue with name '{name}' has no ID.")
            resource_id = jq.id

        self.client.upsert_resource_tags(
            ResourceTagResourceType.JOB_QUEUE, resource_id, tags
        )

    def remove_tags(
        self,
        *,
        job_queue_id: Optional[str] = None,
        name: Optional[str] = None,
        keys: List[str],
    ) -> None:
        if not keys:
            raise ValueError("At least one tag key must be provided.")

        if job_queue_id is not None:
            resource_id = job_queue_id
        else:
            if name is None:
                raise ValueError("Either 'job_queue_id' or 'name' must be provided.")
            jq = self._resolve_to_job_queue_model(job_queue_id=None, name=name)
            if jq.id is None:
                raise RuntimeError(f"Job queue with name '{name}' has no ID.")
            resource_id = jq.id

        self.client.delete_resource_tags(
            ResourceTagResourceType.JOB_QUEUE, resource_id, keys
        )

    def _resolve_to_job_queue_model(
        self, *, job_queue_id: Optional[str] = None, name: Optional[str] = None,
    ) -> DecoratedJobQueue:
        """Finds the specific Job Queue API model by ID or name.
        """
        if job_queue_id is None and name is None:
            raise ValueError("Either 'job_queue_id' or 'name' must be provided.")

        if job_queue_id:
            job_queue = self.client.get_job_queue(job_queue_id)
            if job_queue is None:
                raise ValueError(f"Job Queue with ID '{job_queue_id}' not found.")
            return job_queue
        else:
            job_queues_response = self.client.list_job_queues(name=name, count=1)
            if len(job_queues_response.results) == 0:
                raise ValueError(f"Job Queue with name '{name}' not found.")
            return job_queues_response.results[0]

    def list_tags(
        self, *, job_queue_id: Optional[str] = None, name: Optional[str] = None,
    ) -> Dict[str, str]:
        """List tags for a job queue as a key/value mapping."""
        if job_queue_id is not None:
            resource_id = job_queue_id
        else:
            jq = self._resolve_to_job_queue_model(job_queue_id=None, name=name)
            if jq.id is None:
                raise RuntimeError(f"Job queue with name '{name}' has no ID.")
            resource_id = jq.id
        records = self.client.list_resource_tags(
            ResourceTagResourceType.JOB_QUEUE, resource_id
        )
        return {r.key: r.value for r in records if r and r.key is not None}


def _parse_decorated_jq_to_status(decorated_jq: DecoratedJobQueue) -> JobQueueStatus:
    """Helper to convert API model to SDK model."""

    if decorated_jq.id is None or decorated_jq.current_job_queue_state is None:
        raise ValueError("Job Queue ID or state is missing.")

    return JobQueueStatus(
        id=decorated_jq.id,
        name=decorated_jq.name,
        state=decorated_jq.current_job_queue_state,
        creator_email=decorated_jq.creator_email,
        project_id=decorated_jq.project_id,
        created_at=decorated_jq.created_at,
        max_concurrency=decorated_jq.max_concurrency,
        idle_timeout_s=decorated_jq.idle_timeout_sec,
        creator_id=decorated_jq.creator_id,
        cloud_id=decorated_jq.cloud_id,
        user_provided_id=decorated_jq.user_provided_id,
        execution_mode=decorated_jq.execution_mode,
        total_jobs=decorated_jq.total_jobs,
        active_jobs=decorated_jq.active_jobs,
        successful_jobs=decorated_jq.successful_jobs,
        failed_jobs=decorated_jq.failed_jobs,
    )
