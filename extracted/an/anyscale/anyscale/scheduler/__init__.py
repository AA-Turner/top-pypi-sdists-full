"""Alpha SDK for the Anyscale Global Resource Scheduler.

Exposed as ``anyscale.scheduler`` and ``Anyscale().scheduler``.
"""

from typing import Any, Dict, List, Optional, Union

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.scheduler._private.scheduler_sdk import (
    DEFAULT_MAX_CONSUMERS,
    DEFAULT_MAX_QUEUES,
    DEFAULT_MAX_WORKLOADS,
    PrivateSchedulerSDK,
)
from anyscale.scheduler.commands import (
    _APPLY_CONFIG_DOCSTRINGS,
    _APPLY_CONFIG_EXAMPLE,
    _GET_CONFIG_DOCSTRINGS,
    _GET_CONFIG_EXAMPLE,
    _GET_OVERVIEW_EXAMPLE,
    _GET_QUEUE_DOCSTRINGS,
    _GET_QUEUE_EXAMPLE,
    _LIST_CONFIG_VERSIONS_DOCSTRINGS,
    _LIST_CONFIG_VERSIONS_EXAMPLE,
    _LIST_QUEUE_WORKLOADS_DOCSTRINGS,
    _LIST_QUEUE_WORKLOADS_EXAMPLE,
    _LIST_QUEUES_DOCSTRINGS,
    _LIST_QUEUES_EXAMPLE,
    _LIST_TOP_CONSUMERS_DOCSTRINGS,
    _LIST_TOP_CONSUMERS_EXAMPLE,
    _ROLLBACK_CONFIG_DOCSTRINGS,
    _ROLLBACK_CONFIG_EXAMPLE,
    apply_config as apply_config,
    get_config as get_config,
    get_overview as get_overview,
    get_queue as get_queue,
    list_config_versions as list_config_versions,
    list_queue_workloads as list_queue_workloads,
    list_queues as list_queues,
    list_top_consumers as list_top_consumers,
    rollback_config as rollback_config,
)
from anyscale.scheduler.models import (
    QueueWorkloadList,
    ResourceQueueStatus,
    ResourceQueueStatusPage,
    SchedulerConfig,
    SchedulerConfigVersion,
    SchedulerConfigVersionSummary,
    SchedulerOverview,
    TopConsumer,
    WorkloadState,
)


class SchedulerSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateSchedulerSDK(
            client=client,
            logger=logger,
            timer=timer,
        )

    @sdk_docs(
        doc_py_example=_APPLY_CONFIG_EXAMPLE,
        arg_docstrings=_APPLY_CONFIG_DOCSTRINGS,
    )
    def apply_config(  # noqa: F811
        self,
        config: Union[SchedulerConfig, Dict[str, Any]],
    ) -> int:
        """Apply a scheduler config (creates a new active version). Returns the new version number."""
        return self._private_sdk.apply_config(config)

    @sdk_docs(
        doc_py_example=_ROLLBACK_CONFIG_EXAMPLE,
        arg_docstrings=_ROLLBACK_CONFIG_DOCSTRINGS,
    )
    def rollback_config(  # noqa: F811
        self,
        version: int,
    ) -> int:
        """Roll back to an existing config version. Returns the new version number."""
        return self._private_sdk.rollback_config(version=version)

    @sdk_docs(
        doc_py_example=_GET_CONFIG_EXAMPLE,
        arg_docstrings=_GET_CONFIG_DOCSTRINGS,
    )
    def get_config(  # noqa: F811
        self,
        version: Optional[int] = None,
    ) -> SchedulerConfigVersion:
        """Get the active scheduler config (or a specific version)."""
        return self._private_sdk.get_config(version=version)

    @sdk_docs(
        doc_py_example=_LIST_CONFIG_VERSIONS_EXAMPLE,
        arg_docstrings=_LIST_CONFIG_VERSIONS_DOCSTRINGS,
    )
    def list_config_versions(  # noqa: F811
        self,
        max_items: int = 10,
    ) -> List[SchedulerConfigVersionSummary]:
        """List scheduler config version history (newest first)."""
        return self._private_sdk.list_config_versions(max_items=max_items)

    @sdk_docs(
        doc_py_example=_LIST_QUEUES_EXAMPLE,
        arg_docstrings=_LIST_QUEUES_DOCSTRINGS,
    )
    def list_queues(  # noqa: F811
        self,
        *,
        max_items: int = DEFAULT_MAX_QUEUES,
        page_token: Optional[str] = None,
    ) -> ResourceQueueStatusPage:
        """List the active resource queues with their live state, one page at a time."""
        return self._private_sdk.list_queues(max_items=max_items, page_token=page_token)

    @sdk_docs(
        doc_py_example=_GET_QUEUE_EXAMPLE,
        arg_docstrings=_GET_QUEUE_DOCSTRINGS,
    )
    def get_queue(  # noqa: F811
        self,
        name: str,
    ) -> ResourceQueueStatus:
        """Get the live state of one active resource queue, by name."""
        return self._private_sdk.get_queue(name)

    @sdk_docs(
        doc_py_example=_LIST_QUEUE_WORKLOADS_EXAMPLE,
        arg_docstrings=_LIST_QUEUE_WORKLOADS_DOCSTRINGS,
    )
    def list_queue_workloads(  # noqa: F811, PLR0913
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
        """List the pending or running workloads of a resource queue."""
        return self._private_sdk.list_queue_workloads(
            name,
            state=state,
            max_items=max_items,
            cluster_id=cluster_id,
            workspace_id=workspace_id,
            job_id=job_id,
            service_id=service_id,
        )

    @sdk_docs(
        doc_py_example=_GET_OVERVIEW_EXAMPLE,
        arg_docstrings={},
    )
    def get_overview(self) -> SchedulerOverview:  # noqa: F811
        """Get the organization-wide scheduler rollup."""
        return self._private_sdk.get_overview()

    @sdk_docs(
        doc_py_example=_LIST_TOP_CONSUMERS_EXAMPLE,
        arg_docstrings=_LIST_TOP_CONSUMERS_DOCSTRINGS,
    )
    def list_top_consumers(  # noqa: F811
        self,
        *,
        max_items: int = DEFAULT_MAX_CONSUMERS,
        queue: Optional[str] = None,
    ) -> List[TopConsumer]:
        """List the clusters that hold the most nodes, largest first."""
        return self._private_sdk.list_top_consumers(max_items=max_items, queue=queue)
