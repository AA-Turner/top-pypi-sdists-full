from typing import Any, List

from pydantic import BaseModel

DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS = 100
DEFAULT_MAX_CONCURRENT_EXECUTIONS_PER_WORKER = 100


class ExtraItemParams(BaseModel):
    """Parameters for the extract_item_activity function."""

    extra_params: Any | None = None
    """Extra parameters for the activity."""


class GetItemFromIndexParams(ExtraItemParams):
    """Parameters for the get_item_from_index_activity function."""

    idx: int
    """The index of the item to retrieve."""


class WorkflowResults(BaseModel):
    """Result of the workflow execution."""

    values: List[Any]
    """The results of the items processed (if the activity returns a value)."""


class ListExecutorParams(ExtraItemParams):
    """Parameters for list executor that processes a known list of items."""

    activity_name: str
    """Name of the activity that processes each item."""
    items: List[Any]
    """List of items to process."""
    prev_idx: int = -1
    """The previous index processed (for continuation)."""
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS
    """Maximum number of concurrent workflow tasks."""
    prev_results: WorkflowResults | None = None
    """The results of the items processed (for continuation)."""


class ChainExecutorParams(BaseModel):
    """Parameters for chain executor that processes items sequentially."""

    activity_name: str
    """Name of the activity that processes each item."""
    get_item_from_prev_item_activity_name: str
    """Name of the activity that retrieves the next item from the previous item."""
    prev_idx: int = -1
    """The previous index processed (for continuation)."""
    prev_item: Any | None = None
    """The previous item processed (for continuation)."""
    prev_results: WorkflowResults | None = None
    """The results of the items processed (for continuation)."""


class OffsetPaginationExecutorParams(ExtraItemParams):
    """Parameters for offset pagination executor that processes items by index/page."""

    activity_name: str
    """Name of the activity that processes each item."""
    get_item_from_index_activity_name: str
    """Name of the activity that retrieves an item by index."""
    n_items: int
    """The total number of items to process."""
    prev_idx: int = -1
    """The previous index processed (for continuation)."""
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS
    """Maximum number of concurrent workflow tasks."""
    prev_results: WorkflowResults | None = None
    """The results of the items processed (for continuation)."""
    batch_size: int = 10
    """The number of items to process in each batch."""


class WorkflowParams(BaseModel):
    """Parameters for the workflow execution."""

    params: ListExecutorParams | ChainExecutorParams | OffsetPaginationExecutorParams
    """Parameters for the workflow execution."""


class ExecuteActivityInBatchParams(ExtraItemParams):
    """Parameters for the get_and_run_activity function."""

    activity_name: str
    """Name of the activity that processes each item."""
    get_item_from_index_activity_name: str
    """Name of the activity that retrieves an item by index."""
    idx: int
    """The index of the item to retrieve."""
    batch_size: int
    """The number of items to process in each batch."""


class ExecuteActivityInBatchResult(BaseModel):
    """Result of the get_and_run_activity function."""

    results: dict[int, Any]
    """The results of the items processed (if the activity returns a value)."""
