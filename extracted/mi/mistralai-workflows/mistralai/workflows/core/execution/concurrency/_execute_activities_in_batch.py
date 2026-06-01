import asyncio
from types import NoneType
from typing import Any, Dict

from mistralai.workflows.core.activity import activity, get_wrapped_activity
from mistralai.workflows.core.definition.validation._validator import get_function_signature_type_hints
from mistralai.workflows.core.execution.concurrency._utils import (
    build_required_keys,
    build_type_adapters,
    coerce_multi_params,
)
from mistralai.workflows.core.execution.concurrency.types import (
    ExecuteActivityInBatchParams,
    ExecuteActivityInBatchResult,
    GetItemFromIndexParams,
)


@activity(name="__internal_execute_activity_in_batch")
async def execute_activity_in_batch(params: ExecuteActivityInBatchParams) -> ExecuteActivityInBatchResult:
    """Get the activity and run it."""

    activity = get_wrapped_activity(params.activity_name)
    get_item_from_index_activity = get_wrapped_activity(params.get_item_from_index_activity_name)

    assert activity is not None
    assert get_item_from_index_activity is not None

    _activity_for_hints = getattr(activity, "__original_func__", activity)
    user_params_dict, return_type, has_kwargs = get_function_signature_type_hints(_activity_for_hints, is_method=False)
    is_single_param = len(user_params_dict) == 1 and not has_kwargs
    adapters = build_type_adapters(user_params_dict) if not is_single_param else {}
    required = build_required_keys(_activity_for_hints) if not is_single_param and user_params_dict else None

    results_as_dict: Dict[int, Any] = {}

    async def get_and_run_activity(idx: int) -> None:
        current_item = await get_item_from_index_activity(
            GetItemFromIndexParams(idx=idx, extra_params=params.extra_params)
        )
        if is_single_param:
            result = await activity(current_item)
        elif user_params_dict or has_kwargs:
            coerced_item = coerce_multi_params(current_item, adapters, required, allow_extra=has_kwargs)
            result = await activity(**coerced_item)
        else:
            result = await activity()
        if return_type is not NoneType:
            results_as_dict[idx] = result

    await asyncio.gather(*[get_and_run_activity(idx) for idx in range(params.idx, params.idx + params.batch_size)])

    return ExecuteActivityInBatchResult(results=results_as_dict)
