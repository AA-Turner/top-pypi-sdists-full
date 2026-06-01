import asyncio
from types import NoneType
from typing import Any

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
from mistralai.workflows.core.execution.concurrency.types import ChainExecutorParams, WorkflowParams, WorkflowResults


async def execute_chain_activities(
    params: ChainExecutorParams,
) -> WorkflowParams | WorkflowResults:
    """Execute activities in parallel for a chain of items.

    This executor processes items sequentially by fetching the next item
    from the previous one. Use this for token-based pagination (S3, DynamoDB)
    where each response contains the key to get the next batch.

    Args:
        params: Chain executor parameters containing the chain configuration

    Returns:
        WorkflowResults if processing is complete, or WorkflowParams for continuation
    """
    activity = get_wrapped_activity(params.activity_name)
    get_item_from_prev_item_activity = get_wrapped_activity(params.get_item_from_prev_item_activity_name)

    assert activity is not None
    assert get_item_from_prev_item_activity is not None

    _activity_for_hints = getattr(activity, "__original_func__", activity)
    user_params_dict, return_type, has_kwargs = get_function_signature_type_hints(_activity_for_hints, is_method=False)
    is_single_param = len(user_params_dict) == 1 and not has_kwargs
    adapters = build_type_adapters(user_params_dict) if not is_single_param else {}
    required = build_required_keys(_activity_for_hints) if not is_single_param and user_params_dict else None

    current_item = params.prev_item
    if current_item is not None and is_single_param:
        param_type = next(iter(user_params_dict.values()))
        current_item = TypeAdapter(param_type).validate_python(current_item)

    results_as_dict = workflow_results_to_dict(params.prev_results or WorkflowResults(values=[]))
    idx = params.prev_idx + 1
    done = False

    async def run_activity(idx: int, item: Any) -> None:
        if is_single_param:
            result = await activity(item)
        elif user_params_dict or has_kwargs:
            result = await activity(**item)
        else:
            result = await activity()
        if return_type is not NoneType:
            results_as_dict[idx] = result

    async with asyncio.TaskGroup() as tg:
        while True:
            current_item = await get_item_from_prev_item_activity(current_item)

            if current_item is None:
                done = True
                break

            # Coerce multi-param items before creating the task so validation
            # errors raise directly instead of being wrapped by TaskGroup.
            # Use a separate variable to preserve the raw item for the chain provider.
            activity_item = (
                coerce_multi_params(current_item, adapters, required, allow_extra=has_kwargs)
                if not is_single_param and (user_params_dict or has_kwargs)
                else current_item
            )

            tg.create_task(run_activity(idx, activity_item))

            if temporalio.workflow.in_workflow() and temporalio.workflow.info().is_continue_as_new_suggested():
                break

            idx += 1

    if done:
        # Stream is exhausted
        return dict_to_workflow_results(results_as_dict)
    else:
        # Need to continue streaming
        return WorkflowParams(
            params=ChainExecutorParams(
                activity_name=params.activity_name,
                get_item_from_prev_item_activity_name=params.get_item_from_prev_item_activity_name,
                prev_idx=idx,
                prev_item=current_item,
                prev_results=dict_to_workflow_results(results_as_dict),
            )
        )
