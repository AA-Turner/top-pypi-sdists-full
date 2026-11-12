from typing import Optional, Union

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.task._private.task_sdk import DEFAULT_MAX_ITEMS, PrivateTaskSDK
from anyscale.task.commands import (
    _AGGREGATE_ARG_DOCSTRINGS,
    _AGGREGATE_EXAMPLE,
    aggregate as aggregate,
)
from anyscale.task.models import TaskAggregateBy, TaskAggregates


class TaskSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateTaskSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_AGGREGATE_EXAMPLE,
        arg_docstrings=_AGGREGATE_ARG_DOCSTRINGS,
    )
    def aggregate(  # noqa: F811, PLR0913
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
        """Group the Ray tasks of a cluster, workspace, job or service by function, job
        or exception, with counts and timings per group."""
        return self._private_sdk.aggregate(
            by=by,
            cluster_id=cluster_id,
            workspace_id=workspace_id,
            job_id=job_id,
            service_id=service_id,
            ray_session=ray_session,
            max_items=max_items,
            start_cluster=start_cluster,
        )
