import inspect
from types import NoneType
from typing import Any, Awaitable, Callable, Dict, List, TypeVar, cast, get_origin, overload

import structlog
from pydantic import TypeAdapter
from temporalio.exceptions import ApplicationError

from mistralai.workflows.core.activity import check_is_activity
from mistralai.workflows.core.definition.validation._schema_generator import generate_pydantic_model_from_params
from mistralai.workflows.core.definition.validation._validator import (
    extract_origin_type,
    get_function_signature_type_hints,
)
from mistralai.workflows.core.execution.concurrency._concurrency_workflow import ParallelExecutionWorkflow
from mistralai.workflows.core.execution.concurrency.run_in_batches import run_in_batches
from mistralai.workflows.core.execution.concurrency.types import (
    DEFAULT_MAX_CONCURRENT_EXECUTIONS_PER_WORKER,
    DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
    ChainExecutorParams,
    GetItemFromIndexParams,
    ListExecutorParams,
    OffsetPaginationExecutorParams,
    WorkflowParams,
    WorkflowResults,
)
from mistralai.workflows.core.workflow import workflow

T = TypeVar("T")
U = TypeVar("U")


logger = structlog.get_logger(__name__)


def _resolve_class(t: Any) -> type | None:
    """Resolve a type annotation to its base class, handling generic aliases.

    For generic aliases like ``list[str]`` or ``dict[str, Any]``, returns the
    origin class (``list``, ``dict``).  For plain classes returns them directly.
    Returns ``None`` for anything else (e.g. ``Union``, ``None``).
    """
    origin = get_origin(t)
    if origin is not None and inspect.isclass(origin):
        return cast(type, origin)
    if inspect.isclass(t):
        return t
    return None


def _type_name(t: Any) -> str:
    """Return a human-readable name for a type annotation."""
    return getattr(t, "__name__", str(t))


def _validate_items(
    items: List[Any],
    user_params_dict: Dict[str, Any],
    is_single_param: bool,
    activity_name: str,
    activity_func: Callable | None = None,
    has_kwargs: bool = False,
) -> None:
    """Validate items against the activity's parameter types before execution.

    For single-param activities, each item is validated against the param type directly.
    For multi-param activities, each item must be a dict whose keys and value types
    match the activity's parameters.
    """
    if is_single_param:
        param_type = next(iter(user_params_dict.values()))
        adapter = TypeAdapter(param_type)
        for i, item in enumerate(items):
            try:
                adapter.validate_python(item)
            except Exception as e:
                raise ApplicationError(
                    f"Item at index {i} is not compatible with activity "
                    f"'{activity_name}' parameter type {param_type}: {e}",
                    non_retryable=True,
                ) from e
    elif user_params_dict:
        input_model = generate_pydantic_model_from_params(
            activity_name, user_params_dict, func=activity_func, allow_extra=has_kwargs
        )
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                raise ApplicationError(
                    f"Item at index {i} must be a dict mapping parameter names to values "
                    f"for multi-parameter activity '{activity_name}', got {type(item).__name__}",
                    non_retryable=True,
                )
            try:
                input_model.model_validate(item)
            except Exception as e:
                raise ApplicationError(
                    f"Item at index {i} is not compatible with activity "
                    f"'{activity_name}' parameters {list(user_params_dict.keys())}: {e}",
                    non_retryable=True,
                ) from e
    elif has_kwargs:
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                raise ApplicationError(
                    f"Item at index {i} must be a dict mapping keyword names to values "
                    f"for kwargs activity '{activity_name}', got {type(item).__name__}",
                    non_retryable=True,
                )


# Single-param Batch Executor Overloads
@overload
async def execute_activities_in_parallel(  # type: ignore[overload-overlap]
    activity: Callable[[T], Awaitable[None]],
    *,
    items: List[T],
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
) -> None: ...


@overload
async def execute_activities_in_parallel(
    activity: Callable[[T], Awaitable[U]],
    *,
    items: List[T],
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
) -> List[U]: ...


# Multi-param Batch Executor Overloads
@overload
async def execute_activities_in_parallel(  # type: ignore[overload-overlap]
    activity: Callable[..., Awaitable[None]],
    *,
    items: List[Dict[str, Any]],
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
) -> None: ...


@overload
async def execute_activities_in_parallel(
    activity: Callable[..., Awaitable[U]],
    *,
    items: List[Dict[str, Any]],
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
) -> List[U]: ...


# Single-param Stream Executor Overloads
@overload
async def execute_activities_in_parallel(  # type: ignore[overload-overlap]
    activity: Callable[[T], Awaitable[None]],
    *,
    get_item_from_prev_item_activity: Callable[[T | None], Awaitable[T | None]],
    extra_params: Dict[str, Any] | None = None,
) -> None: ...


@overload
async def execute_activities_in_parallel(  # type: ignore[overload-overlap]
    activity: Callable[[T], Awaitable[U]],
    *,
    get_item_from_prev_item_activity: Callable[[T | None], Awaitable[T | None]],
    extra_params: Dict[str, Any] | None = None,
) -> List[U]: ...


# Multi-param Stream Executor Overloads
@overload
async def execute_activities_in_parallel(  # type: ignore[overload-overlap]
    activity: Callable[..., Awaitable[None]],
    *,
    get_item_from_prev_item_activity: Callable[[Dict[str, Any] | None], Awaitable[Dict[str, Any] | None]],
    extra_params: Dict[str, Any] | None = None,
) -> None: ...


@overload
async def execute_activities_in_parallel(
    activity: Callable[..., Awaitable[U]],
    *,
    get_item_from_prev_item_activity: Callable[[Dict[str, Any] | None], Awaitable[Dict[str, Any] | None]],
    extra_params: Dict[str, Any] | None = None,
) -> List[U]: ...


# Single-param Paginated Executor Overloads
@overload
async def execute_activities_in_parallel(  # type: ignore[overload-overlap]
    activity: Callable[[T], Awaitable[None]],
    *,
    get_item_from_index_activity: Callable[[GetItemFromIndexParams], Awaitable[T]],
    n_items: int,
    max_concurrent_executions_per_worker: int = DEFAULT_MAX_CONCURRENT_EXECUTIONS_PER_WORKER,
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
    extra_params: Dict[str, Any] | None = None,
) -> None: ...


@overload
async def execute_activities_in_parallel(
    activity: Callable[[T], Awaitable[U]],
    *,
    get_item_from_index_activity: Callable[[GetItemFromIndexParams], Awaitable[T]],
    n_items: int,
    max_concurrent_executions_per_worker: int = DEFAULT_MAX_CONCURRENT_EXECUTIONS_PER_WORKER,
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
    extra_params: Dict[str, Any] | None = None,
) -> List[U]: ...


# Multi-param Paginated Executor Overloads
@overload
async def execute_activities_in_parallel(  # type: ignore[overload-overlap]
    activity: Callable[..., Awaitable[None]],
    *,
    get_item_from_index_activity: Callable[[GetItemFromIndexParams], Awaitable[Dict[str, Any]]],
    n_items: int,
    max_concurrent_executions_per_worker: int = DEFAULT_MAX_CONCURRENT_EXECUTIONS_PER_WORKER,
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
    extra_params: Dict[str, Any] | None = None,
) -> None: ...


@overload
async def execute_activities_in_parallel(
    activity: Callable[..., Awaitable[U]],
    *,
    get_item_from_index_activity: Callable[[GetItemFromIndexParams], Awaitable[Dict[str, Any]]],
    n_items: int,
    max_concurrent_executions_per_worker: int = DEFAULT_MAX_CONCURRENT_EXECUTIONS_PER_WORKER,
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
    extra_params: Dict[str, Any] | None = None,
) -> List[U]: ...


async def execute_activities_in_parallel(
    activity: Callable[..., Awaitable[None | U]],
    *,
    get_item_from_prev_item_activity: Callable[..., Awaitable[Any]] | None = None,
    get_item_from_index_activity: Callable[[GetItemFromIndexParams], Awaitable[Any]] | None = None,
    items: List[Any] | None = None,
    n_items: int | None = None,
    max_concurrent_scheduled_tasks: int = DEFAULT_MAX_CONCURRENT_SCHEDULED_TASKS,
    max_concurrent_executions_per_worker: int = DEFAULT_MAX_CONCURRENT_EXECUTIONS_PER_WORKER,
    extra_params: Dict[str, Any] | None = None,
) -> None | List[U]:
    """Execute activities in parallel using one of three execution patterns.

    **Batch Executor**: Process a known list of items
    ```python
    results = await execute_activities_in_parallel(
        my_activity,
        items=[item1, item2, item3]
    )
    ```

    **Stream Executor**: Process items from a stream/queue
    ```python
    results = await execute_activities_in_parallel(
        my_activity,
        get_item_from_prev_item_activity=get_next_item
    )
    ```

    **Paginated Executor**: Process items by fetching pages/chunks
    ```python
    results = await execute_activities_in_parallel(
        my_activity,
        get_item_from_index_activity=get_page,
        n_items=1000
    )
    ```

    Args:
        activity: The activity function to execute on each item
        items: List of items to process (Batch Executor)
        get_item_from_prev_item_activity: Function to get next item from previous (Stream Executor)
        get_item_from_index_activity: Function to get item by index (Paginated Executor)
        max_concurrent_scheduled_tasks: Maximum concurrent scheduled tasks
        max_concurrent_executions_per_worker: Maximum concurrent executions per worker
        extra_params: Extra parameters to pass to the activity

    Returns:
        None if activity returns None, otherwise List of results

    Raises:
        ApplicationError (non-retryable): If activity is not decorated with @workflows.activity
        ApplicationError (non-retryable): If items contain types incompatible with the activity's expected input type
        ApplicationError (non-retryable): If provider return type is incompatible with activity input
        ApplicationError (non-retryable): If get_item_from_index_activity does not accept GetItemFromIndexParams
        ApplicationError (non-retryable): If no execution pattern is specified
    """
    # Validate activity
    if not check_is_activity(activity):
        raise ApplicationError(
            "`activity` must be an activity, please decorate it with @workflows.activity",
            non_retryable=True,
        )

    # Use the original unwrapped function for type resolution.
    # On Python 3.14+ (PEP 649), functools.wraps breaks annotation propagation
    # because setting __annotate__ clears __annotations__ at the C level.
    _activity_for_hints = getattr(activity, "__original_func__", activity)
    user_params_dict, activity_return_type, has_kwargs = get_function_signature_type_hints(
        _activity_for_hints, is_method=False
    )

    if not user_params_dict and not has_kwargs:
        raise ApplicationError(
            f"Activity '{activity.__name__}' takes no input parameters, "
            f"so items provided by the executor would be silently ignored.",
            non_retryable=True,
        )

    is_single_param = len(user_params_dict) == 1 and not has_kwargs

    result: WorkflowResults

    # List Executor
    if items is not None:
        _validate_items(
            items,
            user_params_dict,
            is_single_param,
            activity.__name__,
            activity_func=_activity_for_hints,
            has_kwargs=has_kwargs,
        )

        result = await workflow.execute_workflow(
            ParallelExecutionWorkflow,
            WorkflowParams(
                params=ListExecutorParams(
                    activity_name=activity.__name__,
                    items=items,
                    max_concurrent_scheduled_tasks=max_concurrent_scheduled_tasks,
                    extra_params=extra_params,
                )
            ),
        )

    # Chain Executor
    elif get_item_from_prev_item_activity is not None:
        if not check_is_activity(get_item_from_prev_item_activity):
            raise ApplicationError(
                "`get_item_from_prev_item_activity` must be an activity, please decorate it with @workflows.activity",
                non_retryable=True,
            )

        # Validate the chain provider's types:
        # 1. Return type must match the activity's input type
        # 2. Input type must accept its own return type (since the previous return
        #    value is fed back as the next input)
        _chain_for_hints = getattr(
            get_item_from_prev_item_activity, "__original_func__", get_item_from_prev_item_activity
        )
        chain_params_dict, chain_return_type, _ = get_function_signature_type_hints(_chain_for_hints, is_method=False)
        chain_item_type = extract_origin_type(chain_return_type)  # strip Optional/None

        # Chain provider must accept at least one parameter (the previous item)
        if not chain_params_dict:
            raise ApplicationError(
                "`get_item_from_prev_item_activity` must accept at least one parameter "
                "(the previous item), but it takes none",
                non_retryable=True,
            )

        # Validate provider input accepts its own return type
        chain_input_type = extract_origin_type(next(iter(chain_params_dict.values())))
        chain_item_cls = _resolve_class(chain_item_type)
        chain_input_cls = _resolve_class(chain_input_type)
        if (
            chain_item_cls is not None
            and chain_input_cls is not None
            and not issubclass(chain_item_cls, chain_input_cls)
        ):
            raise ApplicationError(
                f"`get_item_from_prev_item_activity` returns {_type_name(chain_item_type)}, "
                f"but its own input expects {_type_name(chain_input_type)}. "
                f"The return value is fed back as input on the next iteration",
                non_retryable=True,
            )

        if is_single_param:
            activity_param_type = next(iter(user_params_dict.values()))
            activity_param_cls = _resolve_class(activity_param_type)
            if (
                chain_item_cls is not None
                and activity_param_cls is not None
                and not issubclass(chain_item_cls, activity_param_cls)
            ):
                raise ApplicationError(
                    f"`get_item_from_prev_item_activity` returns {_type_name(chain_item_type)}, "
                    f"but activity '{activity.__name__}' expects {_type_name(activity_param_type)}",
                    non_retryable=True,
                )
        elif user_params_dict or has_kwargs:
            # Multi-param/kwargs: chain provider must return a dict
            if chain_item_cls is not None and not issubclass(chain_item_cls, dict):
                raise ApplicationError(
                    f"`get_item_from_prev_item_activity` returns {_type_name(chain_item_type)}, "
                    f"but activity '{activity.__name__}' expects a dict",
                    non_retryable=True,
                )

        result = await workflow.execute_workflow(
            ParallelExecutionWorkflow,
            WorkflowParams(
                params=ChainExecutorParams(
                    activity_name=activity.__name__,
                    get_item_from_prev_item_activity_name=get_item_from_prev_item_activity.__name__,
                )
            ),
        )

    # Offset Pagination Executor
    elif get_item_from_index_activity is not None and n_items is not None:
        if not check_is_activity(get_item_from_index_activity):
            raise ApplicationError(
                "`get_item_from_index_activity` must be an activity, please decorate it with @workflows.activity",
                non_retryable=True,
            )

        _fetcher_for_hints = getattr(get_item_from_index_activity, "__original_func__", get_item_from_index_activity)
        fetcher_params_dict, fetcher_return_type, _ = get_function_signature_type_hints(
            _fetcher_for_hints, is_method=False
        )
        fetcher_param_type = next(iter(fetcher_params_dict.values())) if fetcher_params_dict else None
        fetcher_param_cls = _resolve_class(fetcher_param_type) if fetcher_param_type is not None else None
        if fetcher_param_cls is None or not issubclass(fetcher_param_cls, GetItemFromIndexParams):
            raise ApplicationError(
                f"`get_item_from_index_activity` must take a single parameter of type "
                f"{GetItemFromIndexParams.__name__}, got {fetcher_param_type}",
                non_retryable=True,
            )

        # Validate that the offset fetcher's return type matches the activity's input type
        fetcher_item_type = extract_origin_type(fetcher_return_type)  # strip Optional/None
        fetcher_item_cls = _resolve_class(fetcher_item_type)

        if is_single_param:
            activity_param_type = next(iter(user_params_dict.values()))
            activity_param_cls = _resolve_class(activity_param_type)
            if (
                fetcher_item_cls is not None
                and activity_param_cls is not None
                and not issubclass(fetcher_item_cls, activity_param_cls)
            ):
                raise ApplicationError(
                    f"`get_item_from_index_activity` returns {_type_name(fetcher_item_type)}, "
                    f"but activity '{activity.__name__}' expects {_type_name(activity_param_type)}",
                    non_retryable=True,
                )
        elif user_params_dict or has_kwargs:
            # Multi-param/kwargs: offset fetcher must return a dict
            if fetcher_item_cls is not None and not issubclass(fetcher_item_cls, dict):
                raise ApplicationError(
                    f"`get_item_from_index_activity` returns {_type_name(fetcher_item_type)}, "
                    f"but activity '{activity.__name__}' expects a dict",
                    non_retryable=True,
                )

        logger.info("Starting offset pagination executor", n_items=n_items)

        default_params = OffsetPaginationExecutorParams(
            activity_name=activity.__name__,
            get_item_from_index_activity_name=get_item_from_index_activity.__name__,
            n_items=n_items,
            max_concurrent_scheduled_tasks=max_concurrent_scheduled_tasks,
            batch_size=max_concurrent_executions_per_worker,
            extra_params=extra_params,
        )
        dict_default_params = default_params.model_dump()

        results = await run_in_batches(
            fct=lambda params: workflow.execute_workflow(ParallelExecutionWorkflow, params),
            get_params_for_batch=lambda idx, batch_size: WorkflowParams(
                # construct without validation to avoid temporal timeout
                params=OffsetPaginationExecutorParams.model_construct(
                    **{
                        **dict_default_params,
                        "n_items": idx + batch_size,
                        "prev_idx": idx - 1,
                    }
                )
            ),
            n_items=n_items,
        )

        # construct without validation to avoid temporal timeout
        result = WorkflowResults.model_construct(values=[item for batch in results for item in batch.values])

    else:
        raise ApplicationError(
            "Must specify one execution pattern: 'items' (list), "
            "'get_item_from_prev_item_activity' (chain), or 'get_item_from_index_activity' (offset pagination)",
            non_retryable=True,
        )

    # Return results
    if activity_return_type is NoneType:
        return None
    else:
        return_adapter = TypeAdapter(activity_return_type)
        return cast(List[U], [return_adapter.validate_python(value) for value in result.values])
