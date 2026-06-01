import asyncio
import inspect
from types import NoneType

import temporalio
import temporalio.workflow
from pydantic import TypeAdapter

from mistralai.workflows.core.activity import get_wrapped_activity
from mistralai.workflows.core.definition.validation._validator import (
    get_function_signature_type_hints,
)
from mistralai.workflows.core.execution.concurrency._utils import (
    build_required_keys,
    build_type_adapters,
    coerce_multi_params,
    dict_to_workflow_results,
    workflow_results_to_dict,
)
from mistralai.workflows.core.execution.concurrency.types import (
    ExtraItemParams,
    ListExecutorParams,
    WorkflowParams,
    WorkflowResults,
)


async def execute_list_activities(
    params: ListExecutorParams,
) -> WorkflowParams | WorkflowResults:
    """Execute activities in parallel for a list of known items.

    This executor processes a predefined list of items all at once.
    Use this when you have all items available upfront.

    Args:
        params: List executor parameters containing the items to process

    Returns:
        WorkflowResults if processing is complete, or WorkflowParams for continuation
    """
    activity = get_wrapped_activity(params.activity_name)

    assert activity is not None

    _activity_for_hints = getattr(activity, "__original_func__", activity)
    user_params_dict, return_type, has_kwargs = get_function_signature_type_hints(_activity_for_hints, is_method=False)
    is_single_param = len(user_params_dict) == 1 and not has_kwargs
    param_adapter: TypeAdapter | None = None
    is_extra_item_params = False
    if is_single_param:
        param_type = next(iter(user_params_dict.values()))
        param_adapter = TypeAdapter(param_type)
        is_extra_item_params = inspect.isclass(param_type) and issubclass(param_type, ExtraItemParams)
    adapters = build_type_adapters(user_params_dict) if not is_single_param else {}
    required = build_required_keys(_activity_for_hints) if not is_single_param and user_params_dict else None

    results_as_dict = workflow_results_to_dict(params.prev_results or WorkflowResults(values=[]))

    limit = asyncio.Semaphore(params.max_concurrent_scheduled_tasks)
    idx = params.prev_idx + 1

    async def run_activity(relative_idx: int) -> None:
        # this sleep allow us to limit the number of concurrent workflow tasks in order to avoid the following error:
        # `Error while completing workflow activation error=status: InvalidArgument, message: "PendingActivitiesLimitExceeded: the number of pending activities, 2000, has reached the per-workflow limit of 2000"`  # noqa: E501
        if temporalio.workflow.in_workflow():
            await temporalio.workflow.sleep(0)

        limit.release()
        current_item = params.items[relative_idx]
        if is_single_param:
            assert param_adapter is not None
            current_item = param_adapter.validate_python(current_item)
            if is_extra_item_params:
                current_item.extra_params = params.extra_params
            result = await activity(current_item)
        elif user_params_dict or has_kwargs:
            coerced_item = coerce_multi_params(current_item, adapters, required, allow_extra=has_kwargs)
            result = await activity(**coerced_item)
        else:
            result = await activity()
        if return_type is not NoneType:
            results_as_dict[idx + relative_idx] = result

    relative_idx = 0
    async with asyncio.TaskGroup() as tg:
        while relative_idx < len(params.items):
            await limit.acquire()
            tg.create_task(run_activity(relative_idx))

            if temporalio.workflow.in_workflow() and temporalio.workflow.info().is_continue_as_new_suggested():
                break

            relative_idx += 1

    if relative_idx < len(params.items):
        # Need to continue processing remaining items
        return WorkflowParams(
            params=ListExecutorParams(
                activity_name=params.activity_name,
                items=params.items[relative_idx + 1 :],
                prev_idx=idx + relative_idx,
                max_concurrent_scheduled_tasks=params.max_concurrent_scheduled_tasks,
                prev_results=dict_to_workflow_results(results_as_dict),
                extra_params=params.extra_params,
            )
        )
    else:
        # All items processed
        return dict_to_workflow_results(results_as_dict)
