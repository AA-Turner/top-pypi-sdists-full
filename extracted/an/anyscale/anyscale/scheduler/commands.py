from typing import Any, Dict, List, Optional, Union

from anyscale._private.sdk import sdk_command
from anyscale.scheduler._private.scheduler_sdk import (
    DEFAULT_MAX_CONSUMERS,
    DEFAULT_MAX_QUEUES,
    DEFAULT_MAX_WORKLOADS,
    PrivateSchedulerSDK,
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


_SCHEDULER_SDK_SINGLETON_KEY = "scheduler_sdk"

_APPLY_CONFIG_EXAMPLE = """
import anyscale
from anyscale.scheduler.models import SchedulerConfig

# Load from a YAML file (recommended).
config = SchedulerConfig.from_yaml("scheduler-config.yaml")
version = anyscale.scheduler.apply_config(config)
print(f"Applied scheduler config version {version}")

# Or pass a dict directly.
anyscale.scheduler.apply_config({
    "resource_flavors": [...],
    "resource_queues": [...],
    "scheduling_rules": [...],
})
"""

_APPLY_CONFIG_DOCSTRINGS = {
    "config": (
        "Scheduler config to apply. Either a SchedulerConfig dataclass or a dict "
        "matching the API schema."
    ),
}


_ROLLBACK_CONFIG_EXAMPLE = """
import anyscale

# Re-apply the contents of version 3 as a new version.
new_version = anyscale.scheduler.rollback_config(version=3)
print(f"Rolled back to version 3, applied as version {new_version}")
"""

_ROLLBACK_CONFIG_DOCSTRINGS = {
    "version": "Existing config version whose contents are applied as a new version.",
}


_GET_CONFIG_EXAMPLE = """
import anyscale

# Active config (default).
active = anyscale.scheduler.get_config()
print(active.version, active.config)

# A specific historical version.
v3 = anyscale.scheduler.get_config(version=3)
"""

_GET_CONFIG_DOCSTRINGS = {
    "version": "Specific version to fetch. Omit to fetch the active config.",
}


_LIST_CONFIG_VERSIONS_EXAMPLE = """
import anyscale

# Default: 10 most recent versions.
for summary in anyscale.scheduler.list_config_versions():
    print(summary.version, summary.created_at, summary.creator_id)

# Fetch any number; the SDK paginates internally.
recent = anyscale.scheduler.list_config_versions(max_items=200)
"""

_LIST_CONFIG_VERSIONS_DOCSTRINGS = {
    "max_items": "Maximum number of versions to return. Defaults to 10.",
}


_LIST_QUEUES_EXAMPLE = """
import anyscale

page = anyscale.scheduler.list_queues()
for queue in page.results:
    print(queue.queue, queue.workloads.running, queue.workloads.pending)

# The next page, when there is one.
if page.next_page_token is not None:
    page = anyscale.scheduler.list_queues(page_token=page.next_page_token)
"""

_LIST_QUEUES_DOCSTRINGS = {
    "max_items": "How many queues to return at most, from 1 to 200. Defaults to 50.",
    "page_token": "The next_page_token of an earlier call, to continue after its last "
    "queue. None starts from the first queue.",
}


_GET_QUEUE_EXAMPLE = """
import anyscale

queue = anyscale.scheduler.get_queue("research")
print(queue.workloads.pending, queue.nodes.running)
for usage in queue.quota:
    print(usage.flavor, usage.resource, usage.used, usage.ceiling)
"""

_GET_QUEUE_DOCSTRINGS = {
    "name": "Name of the resource queue, as in the scheduler config.",
}


_LIST_QUEUE_WORKLOADS_EXAMPLE = """
import anyscale

# What is waiting in the queue, next to be admitted first.
page = anyscale.scheduler.list_queue_workloads("research", state="pending")
for workload in page.results:
    print(workload.queue_position, workload.name, workload.requested_resources)

# Where one job is in that line.
mine = anyscale.scheduler.list_queue_workloads(
    "research", state="pending", job_id="prodjob_abc123"
)
"""

_LIST_QUEUE_WORKLOADS_DOCSTRINGS = {
    "name": "Name of the resource queue, as in the scheduler config.",
    "state": "Which workloads to list: pending (waiting for admission) or running "
    "(holding capacity).",
    "max_items": "How many workloads to return at most, from 1 to 1000. Defaults to 100. "
    "`total` in the result says how many there are.",
    "cluster_id": "Only the workload on this cluster. Pass at most one of cluster_id, "
    "workspace_id, job_id or service_id.",
    "workspace_id": "Only this workspace. Its cluster is looked up and matched.",
    "job_id": "Only this job. The cluster of its latest run is looked up and matched.",
    "service_id": "Only this service. The cluster of its primary version is looked up "
    "and matched.",
}


_GET_OVERVIEW_EXAMPLE = """
import anyscale

overview = anyscale.scheduler.get_overview()
print(overview.totals.nodes.running, overview.totals.workloads.pending)
for cloud in overview.clouds:
    print(cloud.cloud_id, cloud.nodes.running)
"""


_LIST_TOP_CONSUMERS_EXAMPLE = """
import anyscale

for consumer in anyscale.scheduler.list_top_consumers(max_items=5):
    print(consumer.cluster_id, consumer.name, consumer.nodes)

# The same, for one queue.
research = anyscale.scheduler.list_top_consumers(queue="research")
"""

_LIST_TOP_CONSUMERS_DOCSTRINGS = {
    "max_items": "How many clusters to return at most, from 1 to 100. Defaults to 10.",
    "queue": "Name of a resource queue, to count only its clusters. None counts the "
    "whole organization.",
}


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_APPLY_CONFIG_EXAMPLE,
    arg_docstrings=_APPLY_CONFIG_DOCSTRINGS,
)
def apply_config(
    config: Union[SchedulerConfig, Dict[str, Any]],
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> int:
    """Apply a scheduler config (creates a new active version). Returns the new version number.

    The previous active version becomes inactive but remains queryable via
    list_config_versions and get_config(version=N). Schema is validated locally
    before the API call; cross-reference checks (queue refs, flavor refs)
    happen on the server.
    """
    return _private_sdk.apply_config(config)  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_ROLLBACK_CONFIG_EXAMPLE,
    arg_docstrings=_ROLLBACK_CONFIG_DOCSTRINGS,
)
def rollback_config(
    version: int,
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> int:
    """Roll back to an existing config version. Returns the new version number.

    The config stored at `version` is applied as a new active version. `version`
    itself stays in history unchanged, so a rollback is itself reversible.
    """
    return _private_sdk.rollback_config(version=version)  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_GET_CONFIG_EXAMPLE,
    arg_docstrings=_GET_CONFIG_DOCSTRINGS,
)
def get_config(
    version: Optional[int] = None,
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> SchedulerConfigVersion:
    """Get the active scheduler config (or a specific version).

    Returns the version number, active flag, creator, created_at, and the full
    SchedulerConfig.
    """
    return _private_sdk.get_config(version=version)  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_LIST_CONFIG_VERSIONS_EXAMPLE,
    arg_docstrings=_LIST_CONFIG_VERSIONS_DOCSTRINGS,
)
def list_config_versions(
    max_items: int = 10,
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> List[SchedulerConfigVersionSummary]:
    """List scheduler config version history (newest first).

    Returns metadata (version, created_at, creator_id) without the config blob.
    Use get_config(version=N) to fetch the full config for a specific version.
    """
    return _private_sdk.list_config_versions(max_items=max_items)  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_LIST_QUEUES_EXAMPLE,
    arg_docstrings=_LIST_QUEUES_DOCSTRINGS,
)
def list_queues(
    *,
    max_items: int = DEFAULT_MAX_QUEUES,
    page_token: Optional[str] = None,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> ResourceQueueStatusPage:
    """List the active resource queues with their live state, one page at a time.

    Each queue carries its running and pending workloads, its nodes and its quota use.
    This is the state of the queues, not their definition: get_config returns that.
    """
    return _private_sdk.list_queues(max_items=max_items, page_token=page_token)  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_GET_QUEUE_EXAMPLE,
    arg_docstrings=_GET_QUEUE_DOCSTRINGS,
)
def get_queue(
    name: str,
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> ResourceQueueStatus:
    """Get the live state of one active resource queue, by name.

    Raises ValueError when no active queue has that name.
    """
    return _private_sdk.get_queue(name)  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_LIST_QUEUE_WORKLOADS_EXAMPLE,
    arg_docstrings=_LIST_QUEUE_WORKLOADS_DOCSTRINGS,
)
def list_queue_workloads(  # noqa: PLR0913
    name: str,
    *,
    state: Union[WorkloadState, str],
    max_items: int = DEFAULT_MAX_WORKLOADS,
    cluster_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    job_id: Optional[str] = None,
    service_id: Optional[str] = None,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> QueueWorkloadList:
    """List the pending or running workloads of a resource queue.

    The pending list is in admission order and has one row per queued request. The
    running list has one row per cluster. With one of the four IDs, only the rows of that
    workload are returned, which answers where a job, service or workspace is in line.
    """
    return _private_sdk.list_queue_workloads(  # type: ignore
        name,
        state=state,
        max_items=max_items,
        cluster_id=cluster_id,
        workspace_id=workspace_id,
        job_id=job_id,
        service_id=service_id,
    )


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_GET_OVERVIEW_EXAMPLE,
    arg_docstrings={},
)
def get_overview(
    *,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> SchedulerOverview:
    """Get the organization-wide scheduler rollup.

    Returns node and workload totals, quota use per flavor and resource, the same totals
    per cloud, and how many queues, flavors, rules and cohorts the active config defines.
    """
    return _private_sdk.get_overview()  # type: ignore


@sdk_command(
    _SCHEDULER_SDK_SINGLETON_KEY,
    PrivateSchedulerSDK,
    doc_py_example=_LIST_TOP_CONSUMERS_EXAMPLE,
    arg_docstrings=_LIST_TOP_CONSUMERS_DOCSTRINGS,
)
def list_top_consumers(
    *,
    max_items: int = DEFAULT_MAX_CONSUMERS,
    queue: Optional[str] = None,
    _private_sdk: Optional[PrivateSchedulerSDK] = None,
) -> List[TopConsumer]:
    """List the clusters that hold the most nodes, largest first.

    Counts the whole organization, or one resource queue when `queue` is given.
    """
    return _private_sdk.list_top_consumers(max_items=max_items, queue=queue)  # type: ignore
