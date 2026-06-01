import asyncio

import temporalio
import temporalio.workflow

from mistralai.workflows.core.activity import get_wrapped_activity
from mistralai.workflows.core.execution.concurrency._execute_activities_in_batch import execute_activity_in_batch
from mistralai.workflows.core.execution.concurrency._utils import (
    dict_to_workflow_results,
    workflow_results_to_dict,
)
from mistralai.workflows.core.execution.concurrency.types import (
    ExecuteActivityInBatchParams,
    OffsetPaginationExecutorParams,
    WorkflowParams,
    WorkflowResults,
)


async def execute_offset_pagination_activities(
    params: OffsetPaginationExecutorParams,
) -> WorkflowParams | WorkflowResults:
    """Execute activities in parallel for offset-paginated items.

    This executor processes items by fetching them using an index/page number.
    Use this for traditional REST API pagination, SQL database chunking,
    or any offset-based fetching (page 1, 2, 3...).

    Args:
        params: Offset pagination executor parameters containing the pagination configuration

    Returns:
        WorkflowResults if processing is complete, or WorkflowParams for continuation
    """
    activity = get_wrapped_activity(params.activity_name)
    get_item_from_index_activity = get_wrapped_activity(params.get_item_from_index_activity_name)

    assert activity is not None
    assert get_item_from_index_activity is not None

    results_as_dict = workflow_results_to_dict(params.prev_results or WorkflowResults(values=[]))

    limit = asyncio.Semaphore(params.max_concurrent_scheduled_tasks)
    idx = params.prev_idx + 1

    default_params = ExecuteActivityInBatchParams(
        activity_name=params.activity_name,
        extra_params=params.extra_params,
        get_item_from_index_activity_name=params.get_item_from_index_activity_name,
        idx=-1,  # This will be set in the loop
        batch_size=-1,  # This will be set in the loop
    )

    async def _execute_activity_in_batch(idx: int) -> None:
        effective_batch_size = min(params.batch_size, params.n_items - idx)
        batch_result = await execute_activity_in_batch(
            ExecuteActivityInBatchParams.model_construct(
                **{**default_params.model_dump(), "idx": idx, "batch_size": effective_batch_size}
            )
        )
        for k, v in batch_result.results.items():
            results_as_dict[k] = v
        limit.release()

    async with asyncio.TaskGroup() as tg:
        while idx < params.n_items:
            await limit.acquire()
            tg.create_task(_execute_activity_in_batch(idx))

            if temporalio.workflow.in_workflow() and temporalio.workflow.info().is_continue_as_new_suggested():
                break

            idx += params.batch_size

    if idx >= params.n_items:
        # No more pages to fetch
        return dict_to_workflow_results(results_as_dict)
    else:
        # Need to continue paginating
        return WorkflowParams(
            params=OffsetPaginationExecutorParams(
                activity_name=params.activity_name,
                get_item_from_index_activity_name=params.get_item_from_index_activity_name,
                n_items=params.n_items,
                batch_size=params.batch_size,
                prev_idx=idx,
                max_concurrent_scheduled_tasks=params.max_concurrent_scheduled_tasks,
                prev_results=dict_to_workflow_results(results_as_dict),
                extra_params=params.extra_params,
            )
        )
