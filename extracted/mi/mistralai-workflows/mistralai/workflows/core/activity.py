import datetime
import inspect
from contextvars import ContextVar
from functools import wraps
from typing import Any, Callable, Dict, List, TypeVar, cast

import structlog
import temporalio
import temporalio.activity
import temporalio.common
import temporalio.workflow
import tenacity
from pydantic import BaseModel

from mistralai.workflows.core._events.event_context import (
    BackgroundEventPublisher,
    EventContext,
    _background_event_publisher,
)
from mistralai.workflows.core.config.config import INTERNAL_ACTIVITY_PREFIX, config
from mistralai.workflows.core.definition.validation._validator import (
    get_function_signature_type_hints,
    raise_if_function_has_invalid_return_type,
    raise_if_function_has_invalid_signature,
    raise_if_function_has_invalid_usage,
)
from mistralai.workflows.core.dependencies.dependency_injector import DependencyInjector
from mistralai.workflows.core.execution.local_activity import is_local_activity_enabled
from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import (
    set_activity_as_sticky_to_worker,
)
from mistralai.workflows.core.rate_limiting.rate_limit import (
    RateLimit,
    get_rate_limit,
    local_wait_rate_limit,
    set_rate_limit,
)
from mistralai.workflows.core.utils.contextvars import reset_contextvar, unwrap_contextual_result
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

logger = structlog.get_logger(__name__)


_temporal_activities: List[Callable] = []
_activities_by_name: Dict[str, Callable] = {}

context_var_task_queue: ContextVar[str | None] = ContextVar("task_queue", default=None)
_context_var_is_inside_activity: ContextVar[bool] = ContextVar("is_inside_activity", default=False)

T = TypeVar("T", bound=Callable[..., Any] | type)


def activity(
    start_to_close_timeout: datetime.timedelta = datetime.timedelta(minutes=5),
    retry_policy_max_attempts: int | None = None,
    retry_policy_backoff_coefficient: float | None = None,
    name: str | None = None,
    sticky_to_worker: bool = False,
    rate_limit: RateLimit | None = None,
    heartbeat_timeout: datetime.timedelta | None = None,
    _skip_registering: bool = False,
    _allow_reserved_name: bool = False,
) -> Callable[[T], T]:
    """
    Decorator for defining activities with configuration options.

    This decorator transforms a regular Python function into an activity with
    various configuration options for timeouts, retries, and worker scoping.

    Args:
        start_to_close_timeout: Maximum time the activity is allowed to execute.
        retry_policy_max_attempts: Maximum number of retry attempts.
        retry_policy_backoff_coefficient: Backoff coefficient for retry delays.
        name: Optional name override for the activity. Defaults to function name.
        sticky_to_worker: Whether the activity should be sticky to a worker.
                          See `workflow_sdk.worker.sticky_worker_session` for more details.
        rate_limit: Set a rate limit for the activity across all workers.
                    See `workflow_sdk.worker.rate_limit.RateLimit` for more details.
        heartbeat_timeout: Maximum time between heartbeats before the activity is
                          considered failed. When set, activities should call
                          `heartbeat()` periodically to report
                          progress. This enables fast detection of stuck activities.
                          Note: Not supported for local activities.

    Internal only args:
        _skip_registering: Whether to skip automatic registration of this activity.
                           When set to `True`, the activity will not be returned by `get_all_temporal_activities()`.

    Returns:
        A decorator function that transforms the target function into an activity.
    """

    def decorator(target: T) -> T:
        # Only support module-level functions
        if not inspect.isfunction(target):
            raise WorkflowsException(
                code=ErrorCode.ACTIVITY_NOT_MODULE_LEVEL,
                message=f"@workflows.activity only supports module-level functions, got {type(target)}",
            )
        else:
            return cast(
                T,
                _decorate_activity(
                    target,
                    start_to_close_timeout,
                    retry_policy_max_attempts,
                    retry_policy_backoff_coefficient,
                    activity_name=name,
                    sticky_to_worker=sticky_to_worker,
                    rate_limit=rate_limit,
                    heartbeat_timeout=heartbeat_timeout,
                    _skip_registering=_skip_registering,
                    _allow_reserved_name=_allow_reserved_name,
                ),
            )

    return decorator


def _decorate_activity(
    func: Callable,
    start_to_close_timeout: datetime.timedelta,
    retry_policy_max_attempts: int | None,
    retry_policy_backoff_coefficient: float | None,
    activity_name: str | None,
    sticky_to_worker: bool,
    rate_limit: RateLimit | None,
    heartbeat_timeout: datetime.timedelta | None,
    _skip_registering: bool,
    _allow_reserved_name: bool,
) -> Callable:
    """
    See `activity` decorator for documentation.
    """

    if activity_name is not None:
        func.__name__ = activity_name

    name_to_check = activity_name or func.__name__
    if not _allow_reserved_name and name_to_check.startswith(INTERNAL_ACTIVITY_PREFIX):
        raise WorkflowsException(
            code=ErrorCode.ACTIVITY_RESERVED_NAME,
            message=f"Activity name '{name_to_check}' uses reserved prefix '{INTERNAL_ACTIVITY_PREFIX}'. "
            f"This prefix is reserved for internal framework activities.",
        )
    # Validate signature BEFORE dependency injection modifies it
    raise_if_function_has_invalid_signature(func, is_method=False, allow_kwargs=True)

    user_params_dict, _, has_kwargs = get_function_signature_type_hints(func, is_method=False)
    func.__has_kwargs__ = has_kwargs  # type: ignore[attr-defined]

    original_func = func

    activity_deps = DependencyInjector.collect_dependencies([original_func])

    dependency_injector = DependencyInjector.get_singleton_instance()
    func = dependency_injector.auto_resolve_dependencies(func)

    # For kwargs activities, create a packed version that accepts a single dict
    # This allows Temporal to serialize/deserialize kwargs properly
    if has_kwargs:
        unpacked_func = func  # The function with original signature

        @wraps(func)
        async def packed_func(__packed_params__: dict[str, Any]) -> Any:
            """Packed activity that unpacks params and calls the original function."""
            # Reconstruct BaseModel params from dicts (Temporal deserializes them as dicts)
            reconstructed_params = {}
            for param_name, param_value in __packed_params__.items():
                if param_name in user_params_dict:
                    param_type = user_params_dict[param_name]
                    if (
                        isinstance(param_value, dict)
                        and inspect.isclass(param_type)
                        and issubclass(param_type, BaseModel)
                    ):
                        param_value = param_type.model_validate(param_value)
                reconstructed_params[param_name] = param_value
            return await unpacked_func(**reconstructed_params)

        func = temporalio.activity.defn(packed_func)
    else:
        # Preserve original annotations so Temporal's data converter can
        # resolve type hints for deserialization (PEP 649 / Python 3.14+
        # breaks get_type_hints through functools.wraps chains)
        func.__annotations__ = original_func.__annotations__
        func = temporalio.activity.defn(func)

    if sticky_to_worker:
        set_activity_as_sticky_to_worker(func)

    if rate_limit is not None:
        set_rate_limit(func, rate_limit)
    elif get_rate_limit(func) is not None:
        raise ValueError(
            "Cannot use `@rate_limit` with `@activity`, please use the parameter `rate_limit` instead in `@activity`."  # noqa: E501
        )

    func.__wf_activity_params__ = {  # type: ignore[union-attr]
        "start_to_close_timeout_seconds": start_to_close_timeout.total_seconds(),
        "retry_policy_max_attempts": retry_policy_max_attempts,
        "retry_policy_backoff_coefficient": retry_policy_backoff_coefficient,
        "sticky_to_worker": sticky_to_worker,
        "heartbeat_timeout_seconds": heartbeat_timeout.total_seconds() if heartbeat_timeout is not None else None,
    }

    # When determinism enforcement is enabled, the temporal sandbox reimports the code in the sandbox
    # with the mistralai-workflows passed through. This re-imports causes the activity code
    # to be re-executed, once per workflow, and thus causes the activity to be registered multiple times.
    # To prevent this, we do not register activities when running in the temporal sandbox
    # only the activity registration out of the sandbox is kept.
    actual_skip_registering = _skip_registering or temporalio.workflow.unsafe.in_sandbox()

    if not actual_skip_registering:
        # Register activity for temporal worker
        _temporal_activities.append(func)

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        """This wrapper is used to execute an activity from a Workflow."""
        effective_max_attempts = (
            retry_policy_max_attempts
            if retry_policy_max_attempts is not None
            else config.worker.retry_policy_max_attempts
        )
        effective_backoff = (
            retry_policy_backoff_coefficient
            if retry_policy_backoff_coefficient is not None
            else config.worker.retry_policy_backoff_coefficient
        )

        is_inside_activity = _context_var_is_inside_activity.get(False)
        token = _context_var_is_inside_activity.set(True)
        publisher = None
        publisher_token = None

        try:
            raise_if_function_has_invalid_usage(original_func, args, kwargs, is_method=False)

            if not temporalio.activity.in_activity():
                # When running outside a Temporal activity (local execution), only set up
                # the event publisher if an EventContext has been initialized.
                # Without this guard, get_singleton() would log a warning for every
                # direct activity call where no event context exists (e.g. unit tests).
                if EventContext.has_context():
                    context = EventContext.get_singleton()
                    if context:
                        publisher = BackgroundEventPublisher(context)
                        publisher_token = BackgroundEventPublisher.set_current(publisher)

            if temporalio.workflow.in_workflow():
                # Determine task queue for activity scheduling
                if sticky_to_worker:
                    task_queue = context_var_task_queue.get()
                    if task_queue is None:
                        raise WorkflowsException(
                            code=ErrorCode.STICKY_WORKER_SESSION_MISSING,
                            message=f"Activity '{func.__name__}' is sticky to worker but no task queue is set. "
                            "Please call this activity inside `run_sticky_worker_session` context manager.",
                        )
                elif rate_limit is not None:
                    rate_limit_config = get_rate_limit(func)
                    if rate_limit_config is None:
                        raise ValueError(f"Activity '{func.__name__}' has rate limit but no rate limit config is set.")
                    task_queue = rate_limit_config.task_queue
                else:
                    task_queue = config.get_effective_task_queue()
                logger.debug(
                    "Executing activity inside workflow",
                    activity_name=func.__name__,
                    task_queue=task_queue,
                )
                # For kwargs activities, pack all params into a single dict
                if has_kwargs:
                    param_names = list(user_params_dict.keys())
                    packed_params = {**dict(zip(param_names, args)), **kwargs}
                    temporal_args: tuple = (packed_params,)
                elif kwargs:
                    # Typed-params-only activity called with keyword arguments:
                    # merge kwargs into positional args in parameter declaration order.
                    # We must preserve positions for optional params not provided in kwargs
                    # by filling in their default values.
                    sig = inspect.signature(original_func)
                    sig_params = [p for p in sig.parameters.values() if p.name in user_params_dict]
                    positional_from_kwargs: list = []
                    for param in sig_params[len(args) :]:
                        if param.name in kwargs:
                            positional_from_kwargs.append(kwargs[param.name])
                        elif param.default is not inspect.Parameter.empty:
                            positional_from_kwargs.append(param.default)
                        else:
                            break
                    temporal_args = args + tuple(positional_from_kwargs)
                else:
                    temporal_args = args

                if is_local_activity_enabled():
                    if rate_limit is not None:
                        logger.warning(
                            "Rate limiting is not supported for local activities",
                            activity_name=func.__name__,
                            rate_limit_config=rate_limit.model_dump()
                            if hasattr(rate_limit, "model_dump")
                            else str(rate_limit),
                        )
                    if heartbeat_timeout is not None:
                        logger.warning(
                            "Heartbeat timeout is not supported for local activities",
                            activity_name=func.__name__,
                            heartbeat_timeout=str(heartbeat_timeout),
                        )
                    result = await temporalio.workflow.execute_local_activity(
                        func,
                        args=temporal_args,
                        start_to_close_timeout=start_to_close_timeout,
                        retry_policy=temporalio.common.RetryPolicy(
                            maximum_attempts=effective_max_attempts,
                            backoff_coefficient=effective_backoff,
                        ),
                    )
                else:
                    result = await temporalio.workflow.execute_activity(
                        func,
                        args=temporal_args,
                        task_queue=task_queue,
                        start_to_close_timeout=start_to_close_timeout,
                        heartbeat_timeout=heartbeat_timeout,
                        retry_policy=temporalio.common.RetryPolicy(
                            maximum_attempts=effective_max_attempts,
                            backoff_coefficient=effective_backoff,
                        ),
                    )
            else:
                if rate_limit is not None:
                    rate_limit_config = get_rate_limit(func)
                    if rate_limit_config is None:
                        raise ValueError(f"Activity '{func.__name__}' has rate limit but no rate limit config is set.")
                    await local_wait_rate_limit(rate_limit_config)

                local_func = (
                    func
                    if temporalio.activity.in_activity() or is_inside_activity
                    else tenacity.retry(
                        retry=tenacity.retry_if_exception_type(Exception),
                        stop=tenacity.stop_after_attempt(effective_max_attempts),
                        wait=tenacity.wait_exponential(multiplier=effective_backoff),
                        reraise=True,
                    )(func)
                )

                # For kwargs activities, pack params into a single dict (same as workflow path)
                if has_kwargs:
                    param_names = list(user_params_dict.keys())
                    packed_params = {**dict(zip(param_names, args)), **kwargs}
                    local_args: tuple = (packed_params,)
                    local_kwargs: dict = {}
                else:
                    local_args = args
                    local_kwargs = kwargs

                logger.debug(
                    "Executing activity outside workflow",
                    activity_name=func.__name__,
                )
                dependency_injector = DependencyInjector.get_singleton_instance()
                async with dependency_injector.with_scoped_dependencies(activity_deps):
                    result = await local_func(*local_args, **local_kwargs)

            _, result = unwrap_contextual_result(result)
            raise_if_function_has_invalid_return_type(original_func, result, is_method=False)

            if publisher:
                await publisher.drain()

        except Exception:
            # Wait for pending events even on failure
            if publisher:
                await publisher.drain()
            raise
        finally:
            if publisher:
                await publisher.shutdown()
            if publisher_token is not None:
                reset_contextvar(_background_event_publisher, publisher_token)
            reset_contextvar(_context_var_is_inside_activity, token)

        return result

    if hasattr(func, "__temporal_activity_definition"):
        wrapper.__temporal_activity_definition = func.__temporal_activity_definition  # type: ignore[attr-defined]

    # Store original function for reliable type resolution on Python 3.14+
    # (PEP 649: setting __annotate__ clears __annotations__ at the C level,
    # breaking get_type_hints through functools.wraps chains)
    wrapper.__original_func__ = original_func  # type: ignore[attr-defined]

    # Copy __has_kwargs__ to wrapper so tool.py can access it
    if hasattr(original_func, "__has_kwargs__"):
        wrapper.__has_kwargs__ = original_func.__has_kwargs__  # type: ignore[attr-defined]

    if not actual_skip_registering:
        # Register activity for internal usage
        _activities_by_name[wrapper.__name__] = wrapper

    return cast(Callable, wrapper)


def activity_heartbeat(*details: Any) -> None:
    """Report activity heartbeat to indicate the activity is still alive.

    Long-running activities should call this periodically when a
    ``heartbeat_timeout`` is configured on the ``@activity`` decorator.

    Args:
        *details: Optional details to report with the heartbeat. These can be
            used to track progress (e.g. number of items processed).
    """
    temporalio.activity.heartbeat(*details)


def get_all_temporal_activities() -> List[Callable]:
    """
    Get a list of all registered Temporal activities.

    Returns:
        List[Callable]: A list of all activity functions registered with Temporal.
    """
    return _temporal_activities.copy()  # return a copy to avoid modifying the original list


def get_wrapped_activity(activity_name: str) -> Callable | None:
    """
    Get a wrapped activity function by name.

    Args:
        activity_name: The name of the activity to retrieve.

    Returns:
        Callable | None: The wrapped activity function if found, None otherwise.
    """
    return _activities_by_name.get(activity_name)


def check_is_activity(func: Callable) -> bool:
    """
    Check if a function is a registered Temporal activity.

    Args:
        func: The function to check.

    Returns:
        bool: True if the function is a registered Temporal activity, False otherwise.
    """
    return hasattr(func, "__temporal_activity_definition") and func.__name__ in _activities_by_name
