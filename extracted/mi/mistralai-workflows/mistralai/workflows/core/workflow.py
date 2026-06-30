import inspect
import warnings
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import WRAPPER_ASSIGNMENTS, wraps
from random import Random
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Iterator, List, Literal, Type, TypeVar, overload
from uuid import UUID

import structlog
import temporalio.workflow
from pydantic import BaseModel
from temporalio.common import VersioningBehavior
from temporalio.workflow import ParentClosePolicy

if TYPE_CHECKING:
    from mistralai.workflows.core.execution import workflow_execution

from mistralai.workflows.core.config.config import RESERVED_QUERY_NAMES, RESERVED_UPDATE_NAMES, config
from mistralai.workflows.core.definition.validation._parameter_conversion import (
    convert_params_dict_to_user_args,
    convert_query_update_result_to_temporal_format,
    convert_result_to_temporal_format,
    resolve_handler_args,
)
from mistralai.workflows.core.definition.validation._schema_generator import (
    generate_pydantic_model_from_params,
    generate_pydantic_model_from_return_type,
)
from mistralai.workflows.core.definition.validation._validator import (
    get_function_signature_type_hints,
    raise_if_function_has_invalid_signature,
    validate_query_handler_signature,
    validate_signal_handler_signature,
    validate_update_handler_signature,
)
from mistralai.workflows.core.definition.workflow_definition import (
    _get_workflow_entrypoint_method,
    set_workflow_definition,
    set_workflow_entrypoint,
)
from mistralai.workflows.core.execution.workflow_execution import (  # noqa: F401 - used in static methods below
    execute_workflow,
)
from mistralai.workflows.core.sandbox import log_if_sandbox_restriction_error
from mistralai.workflows.core.tracing.utils import (
    set_otel_trace_id_in_current_workflow_execution,
)
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.models import (
    QueryDefinition,
    ScheduleDefinition,
    SignalDefinition,
    UpdateDefinition,
    WorkflowSpec,
)

Schedule = ScheduleDefinition

logger = structlog.get_logger(__name__)

ClassType = TypeVar("ClassType", bound=Type)
T = TypeVar("T")

# Exclude __annotations__ and __annotate__ from @wraps to prevent Temporal from
# seeing the original function's signature. The wrapper replaces the user's
# multi-arg signature (e.g. `run(self, name: str)`) with a single-dict signature
# (`run(self, params: dict)`), and Temporal must see the wrapper's annotations.
# Python 3.14 (PEP 649) adds __annotate__ to WRAPPER_ASSIGNMENTS; if copied,
# it causes __annotations__ to be lazily recomputed from the original function,
# defeating the __annotations__ exclusion.
_WRAPS_ASSIGNED = tuple(a for a in WRAPPER_ASSIGNMENTS if a not in ("__annotations__", "__annotate__"))

_registered_workflows: List[Type] = []


def get_all_registered_workflows() -> List[Type]:
    """Return all workflow classes registered via @workflow.define."""
    return _registered_workflows.copy()


@dataclass
class _HandlerMetadata:
    """Metadata stored on handler wrappers for runtime parameter conversion."""

    input_model: Type[BaseModel]
    user_params_dict: dict[str, Type]
    original_func: Callable
    has_kwargs: bool = False
    is_internal: bool = False


class workflow:
    @staticmethod
    def define(
        name: str,
        workflow_description: str | None = None,
        schedules: List[Schedule] | None = None,
        workflow_display_name: str | None = None,
        is_technical: bool = False,
        enforce_determinism: bool | None = None,
        execution_timeout: timedelta = timedelta(hours=1),
        on_behalf_of: bool = False,
    ) -> Callable[[ClassType], ClassType]:
        """Decorator to define a workflow class.

        This decorator registers a class as a Mistral workflow. The class must have exactly one method
        decorated with @workflow.entrypoint to serve as the workflow's main execution logic.

        Args:
            name: The workflow name used for identification and execution. Required.
            workflow_description: Optional description of what the workflow does.
            schedules: DEPRECATED. Optional list of schedule definitions for automated workflow execution.
                This parameter is deprecated and will be removed in the next major release. Use the API or
                AI Studio to create and manage schedules instead (POST /v1/workflows/{id}/schedules).

        Returns:
            A decorator function that transforms the class into a Mistral workflow.

        Raises:
            WorkflowsException: If name is not provided or if the class is not valid.

        Example:
            @workflow.define(name="my_workflow")
            class MyWorkflow:
                @workflow.entrypoint
                async def run(self, input: str) -> str:
                    return f"Processed: {input}"
        """

        def decorator(cls_type: ClassType) -> ClassType:
            if schedules is not None:
                warnings.warn(
                    "The 'schedules' parameter in @workflow.define is deprecated and will be removed "
                    "in the next major release. Please use the API or AI Studio to create and manage "
                    "schedules instead (POST /v1/workflows/{workflow_id}/schedules).",
                    DeprecationWarning,
                    stacklevel=2,
                )
            actual_name = name
            if config.worker.workflow_name_prefix:
                actual_name = f"{config.worker.workflow_name_prefix}{actual_name}"

            if not inspect.isclass(cls_type):
                raise WorkflowsException(
                    code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
                    message=f"@workflow.define only supports classes, got {type(cls_type)}",
                )

            original_run_method = _get_workflow_entrypoint_method(cls_type)

            if not original_run_method:
                raise WorkflowsException(
                    code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
                    message=(
                        f"Workflow class {cls_type} must have an entrypoint method. "
                        f"Use @workflow.entrypoint on one method in the class {cls_type}"
                    ),
                )

            user_method_name = original_run_method.__name__
            user_params_dict, return_type, _ = get_function_signature_type_hints(original_run_method, is_method=True)

            input_model = generate_pydantic_model_from_params(
                original_run_method.__name__, user_params_dict, func=original_run_method
            )
            output_model = generate_pydantic_model_from_return_type(original_run_method.__name__, return_type)

            @wraps(original_run_method, assigned=_WRAPS_ASSIGNED)
            async def run(self: Any, params: dict | None = None) -> Any:
                try:
                    set_otel_trace_id_in_current_workflow_execution()
                except Exception as e:
                    logger.warn("Failed to set otel trace id in current workflow execution", exc_info=e)

                actual_args = convert_params_dict_to_user_args(params, user_params_dict, input_model)

                try:
                    result = await original_run_method(self, *actual_args)
                except Exception as e:
                    log_if_sandbox_restriction_error(e, context="execution")
                    raise

                return convert_result_to_temporal_format(result, output_model)

            run.__qualname__ = f"{cls_type.__name__}.{user_method_name}"

            wrapped_run = temporalio.workflow.run(run)

            setattr(cls_type, user_method_name, wrapped_run)

            collected_signals: List[SignalDefinition] = []
            collected_queries: List[QueryDefinition] = []
            collected_updates: List[UpdateDefinition] = []

            for _, method_obj in inspect.getmembers(cls_type, predicate=inspect.isfunction):
                if hasattr(method_obj, "__wf_signal_def"):
                    collected_signals.append(getattr(method_obj, "__wf_signal_def"))
                elif hasattr(method_obj, "__wf_query_def"):
                    collected_queries.append(getattr(method_obj, "__wf_query_def"))
                elif hasattr(method_obj, "__wf_update_def"):
                    collected_updates.append(getattr(method_obj, "__wf_update_def"))

            # Sort for deterministic order to ensure consistent schema generation across runs
            collected_signals.sort(key=lambda s: s.name)
            collected_queries.sort(key=lambda q: q.name)
            collected_updates.sort(key=lambda u: u.name)

            if on_behalf_of and schedules:
                raise WorkflowsException(
                    code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
                    message=(
                        "on_behalf_of=True cannot be combined with schedules"
                        " because scheduled workflows lack user identity"
                    ),
                )

            actual_enforce_determinism = (
                enforce_determinism if enforce_determinism is not None else config.worker.default_enforce_determinism
            )

            if not actual_enforce_determinism:
                logger.warning(
                    "Workflow registered with determinism enforcement disabled. "
                    "This may lead to non-deterministic behavior and replay failures.",
                    workflow_name=actual_name,
                )

            # Collect plugin metadata from the class
            plugin_metadata = getattr(cls_type, "__plugin_metadata__", None) or None

            workflow_definition_obj = WorkflowSpec(
                name=actual_name,
                display_name=workflow_display_name,
                description=workflow_description,
                input_schema=input_model.model_json_schema(),
                output_schema=output_model.model_json_schema() if output_model is not None else None,
                is_technical=is_technical,
                on_behalf_of=on_behalf_of,
                signals=collected_signals,
                queries=collected_queries,
                updates=collected_updates,
                schedules=schedules or [],
                enforce_determinism=actual_enforce_determinism,
                execution_timeout=execution_timeout,
                plugin_metadata=plugin_metadata,
            )
            set_workflow_definition(cls_type, workflow_definition_obj)

            if not temporalio.workflow.unsafe.in_sandbox():
                _registered_workflows.append(cls_type)

            versioning_cfg = config.worker.versioning

            if versioning_cfg.enabled and versioning_cfg.deployment_name and versioning_cfg.build_id:
                logger.info(
                    "Workflow registered with PINNED versioning behavior",
                    workflow_name=actual_name,
                    deployment_name=versioning_cfg.deployment_name,
                    build_id=versioning_cfg.build_id,
                )
                return temporalio.workflow.defn(
                    sandboxed=actual_enforce_determinism,
                    name=actual_name,
                    versioning_behavior=VersioningBehavior.PINNED,
                )(cls_type)
            else:
                logger.info(
                    "Workflow registered WITHOUT versioning behavior",
                    workflow_name=actual_name,
                )
                return temporalio.workflow.defn(sandboxed=actual_enforce_determinism, name=actual_name)(cls_type)

        return decorator

    @staticmethod
    def entrypoint(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        """Decorator to mark the workflow entrypoint method.

        Marks a method as the main execution entry point for a workflow. Every workflow class
        must have exactly one method decorated with @workflow.entrypoint. This method will be
        called when the workflow is executed.

        The entrypoint method must be async and can accept parameters (as individual typed arguments)
        and return a value. All parameters and return types should be JSON-serializable or Pydantic models.

        Args:
            func: The async method to mark as the workflow entrypoint.

        Returns:
            The decorated method.

        Raises:
            WorkflowsException: If the method signature is invalid.

        Example:
            @workflow.entrypoint
            async def run(self, user_id: str, count: int) -> dict:
                # Workflow logic here
                return {"result": "success"}
        """
        raise_if_function_has_invalid_signature(func, is_method=True)

        set_workflow_entrypoint(func)
        return func

    @staticmethod
    def signal(
        name: str | None = None,
        description: str | None = None,
    ) -> Callable[[Callable], Callable]:
        """Decorator for workflow signal handlers.

        Signals allow external systems to send data into a running workflow asynchronously.
        Signal handlers do not return values - they update workflow state or trigger actions.
        Multiple signals can be sent to a workflow while it's executing.

        Args:
            name: The signal name. If not provided, uses the method name.
            description: Optional description of what the signal does.

        Returns:
            A decorator function for the signal handler method.

        Example:
            @workflow.signal(name="approve")
            async def handle_approval(self, approved_by: str) -> None:
                self.approved = True
                self.approver = approved_by
        """

        def decorator(func: Callable) -> Callable:
            validate_signal_handler_signature(func, is_method=True)

            actual_signal_name = name or func.__name__
            user_params_dict, _, has_kwargs = get_function_signature_type_hints(func, is_method=True)
            input_model = generate_pydantic_model_from_params(
                func.__name__, user_params_dict, func=func, allow_extra=has_kwargs
            )

            meta = _HandlerMetadata(
                input_model=input_model,
                user_params_dict=user_params_dict,
                original_func=func,
                has_kwargs=has_kwargs,
            )

            @wraps(func, assigned=_WRAPS_ASSIGNED)
            async def async_wrapper(self: Any, params: dict | None = None) -> None:
                handler_meta: _HandlerMetadata = getattr(async_wrapper, "__wf_handler_meta")
                actual_args, extra_kwargs = resolve_handler_args(
                    params, handler_meta.user_params_dict, handler_meta.input_model, handler_meta.has_kwargs
                )

                if inspect.iscoroutinefunction(handler_meta.original_func):
                    await handler_meta.original_func(self, *actual_args, **extra_kwargs)
                else:
                    handler_meta.original_func(self, *actual_args, **extra_kwargs)

            @wraps(func, assigned=_WRAPS_ASSIGNED)
            def sync_wrapper(self: Any, params: dict | None = None) -> None:
                handler_meta: _HandlerMetadata = getattr(sync_wrapper, "__wf_handler_meta")
                actual_args, extra_kwargs = resolve_handler_args(
                    params, handler_meta.user_params_dict, handler_meta.input_model, handler_meta.has_kwargs
                )
                handler_meta.original_func(self, *actual_args, **extra_kwargs)

            wrapper = async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

            signal_def = SignalDefinition(
                name=actual_signal_name,
                description=description,
                input_schema=input_model.model_json_schema(),
            )
            setattr(wrapper, "__wf_handler_meta", meta)
            setattr(wrapper, "__wf_signal_def", signal_def)

            return temporalio.workflow.signal(name=actual_signal_name)(wrapper)

        return decorator

    @staticmethod
    def query(
        name: str | None = None,
        description: str | None = None,
        _internal: bool = False,
    ) -> Callable[[Callable], Callable]:
        """Decorator for workflow query handlers.

        Queries allow external systems to read the current state of a running workflow synchronously.
        Query handlers must not modify workflow state - they are read-only operations.
        They return values immediately based on the current workflow state.

        Args:
            name: The query name. If not provided, uses the method name.
            description: Optional description of what the query returns.
            _internal: Internal flag for framework-reserved handlers.

        Returns:
            A decorator function for the query handler method.

        Example:
            @workflow.query(name="get_status")
            def get_current_status(self) -> str:
                return self.current_status
        """

        def decorator(func: Callable) -> Callable:
            validate_query_handler_signature(func, is_method=True)

            actual_query_name = name or func.__name__

            if not _internal and actual_query_name in RESERVED_QUERY_NAMES:
                raise ValueError(
                    f"Query name '{actual_query_name}' is reserved by the framework. "
                    f"Reserved query names: {', '.join(sorted(RESERVED_QUERY_NAMES))}"
                )

            user_params_dict, return_type, has_kwargs = get_function_signature_type_hints(func, is_method=True)
            input_model = generate_pydantic_model_from_params(
                func.__name__, user_params_dict, func=func, allow_extra=has_kwargs
            )
            output_model = generate_pydantic_model_from_return_type(func.__name__, return_type)

            meta = _HandlerMetadata(
                input_model=input_model,
                user_params_dict=user_params_dict,
                original_func=func,
                has_kwargs=has_kwargs,
                is_internal=_internal,
            )

            @wraps(func, assigned=_WRAPS_ASSIGNED)
            def wrapper(self: Any, params: dict | None = None) -> Any:
                handler_meta: _HandlerMetadata = getattr(wrapper, "__wf_handler_meta")
                actual_args, extra_kwargs = resolve_handler_args(
                    params, handler_meta.user_params_dict, handler_meta.input_model, handler_meta.has_kwargs
                )

                result = handler_meta.original_func(self, *actual_args, **extra_kwargs)
                return convert_query_update_result_to_temporal_format(result, output_model)

            query_def = QueryDefinition(
                name=actual_query_name,
                description=description,
                input_schema=input_model.model_json_schema(),
                output_schema=output_model.model_json_schema() if output_model else None,
            )
            setattr(wrapper, "__wf_handler_meta", meta)
            setattr(wrapper, "__wf_query_def", query_def)

            return temporalio.workflow.query(name=actual_query_name)(wrapper)

        return decorator

    @staticmethod
    def update(
        name: str | None = None,
        description: str | None = None,
        _internal: bool = False,
    ) -> Callable[[Callable], Callable]:
        """Decorator for workflow update handlers.

        Updates are similar to signals but they return a value and can be waited on.
        Unlike signals (fire-and-forget), updates provide synchronous feedback to the caller.
        They can modify workflow state and return the result of that modification.

        Args:
            name: The update name. If not provided, uses the method name.
            description: Optional description of what the update does.
            _internal: Internal flag for framework-reserved handlers.

        Returns:
            A decorator function for the update handler method.

        Example:
            @workflow.update(name="set_priority")
            async def update_priority(self, new_priority: int) -> dict:
                old = self.priority
                self.priority = new_priority
                return {"old": old, "new": new_priority}
        """

        def decorator(func: Callable) -> Callable:
            validate_update_handler_signature(func, is_method=True)

            actual_update_name = name or func.__name__

            if not _internal and actual_update_name in RESERVED_UPDATE_NAMES:
                raise ValueError(
                    f"Update name '{actual_update_name}' is reserved by the framework. "
                    f"Reserved update names: {', '.join(sorted(RESERVED_UPDATE_NAMES))}"
                )

            user_params_dict, return_type, has_kwargs = get_function_signature_type_hints(func, is_method=True)
            input_model = generate_pydantic_model_from_params(
                func.__name__, user_params_dict, func=func, allow_extra=has_kwargs
            )
            output_model = generate_pydantic_model_from_return_type(func.__name__, return_type)

            meta = _HandlerMetadata(
                input_model=input_model,
                user_params_dict=user_params_dict,
                original_func=func,
                has_kwargs=has_kwargs,
                is_internal=_internal,
            )

            @wraps(func, assigned=_WRAPS_ASSIGNED)
            async def async_wrapper(self: Any, params: dict | None = None) -> Any:
                handler_meta: _HandlerMetadata = getattr(async_wrapper, "__wf_handler_meta")
                actual_args, extra_kwargs = resolve_handler_args(
                    params, handler_meta.user_params_dict, handler_meta.input_model, handler_meta.has_kwargs
                )

                result = await handler_meta.original_func(self, *actual_args, **extra_kwargs)
                return convert_query_update_result_to_temporal_format(result, output_model)

            @wraps(func, assigned=_WRAPS_ASSIGNED)
            def sync_wrapper(self: Any, params: dict | None = None) -> Any:
                handler_meta: _HandlerMetadata = getattr(sync_wrapper, "__wf_handler_meta")
                actual_args, extra_kwargs = resolve_handler_args(
                    params, handler_meta.user_params_dict, handler_meta.input_model, handler_meta.has_kwargs
                )

                result = handler_meta.original_func(self, *actual_args, **extra_kwargs)
                return convert_query_update_result_to_temporal_format(result, output_model)

            wrapper = async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

            update_def = UpdateDefinition(
                name=actual_update_name,
                description=description,
                input_schema=input_model.model_json_schema(),
                output_schema=output_model.model_json_schema() if output_model else None,
            )
            setattr(wrapper, "__wf_handler_meta", meta)
            setattr(wrapper, "__wf_update_def", update_def)

            return temporalio.workflow.update(name=actual_update_name)(wrapper)

        return decorator

    @staticmethod
    @overload
    async def execute_workflow(
        workflow: Type,
        params: BaseModel,
        execution_timeout: timedelta | None = ...,
        execution_id: str | None = ...,
        wait: Literal[True] = ...,
        parent_close_policy: ParentClosePolicy | None = ...,
    ) -> Any: ...

    @staticmethod
    @overload
    async def execute_workflow(
        workflow: Type,
        params: BaseModel,
        execution_timeout: timedelta | None = ...,
        execution_id: str | None = ...,
        wait: Literal[False] = ...,
        parent_close_policy: ParentClosePolicy | None = ...,
    ) -> "workflow_execution.ChildWorkflowHandle": ...

    @staticmethod
    @overload
    async def execute_workflow(
        workflow: Type,
        params: BaseModel,
        execution_timeout: timedelta | None = ...,
        execution_id: str | None = ...,
        wait: bool = ...,
        parent_close_policy: ParentClosePolicy | None = ...,
    ) -> Any: ...

    @staticmethod
    async def execute_workflow(
        workflow: Type,
        params: BaseModel,
        execution_timeout: timedelta | None = None,
        execution_id: str | None = None,
        wait: bool = True,
        parent_close_policy: ParentClosePolicy | None = None,
    ) -> Any:
        """Execute a workflow. If called from within a workflow, it will execute as a child workflow.

        When called from within a workflow context, this starts a child workflow that inherits
        the parent's namespace and can be monitored as part of the parent's execution.
        When called outside a workflow context, it executes directly.

        Args:
            workflow: The workflow class to execute (must be decorated with @workflow.define).
            params: The parameters to pass to the workflow (must be a BaseModel).
            execution_timeout: The maximum time the workflow can run. Defaults to the workflow's
                declared execution_timeout from @workflow.define (itself 1 hour if unset).
            execution_id: Optional workflow ID. If None, a random ID will be generated.
            wait: If True (default), wait for the child to complete and return the result.
                  If False, return a ChildWorkflowHandle immediately (only inside a workflow).
            parent_close_policy: Policy for the child when the parent closes.
                                 Defaults to TERMINATE when wait=True, ABANDON when wait=False.

        Returns:
            The return value of the workflow's entrypoint method (wait=True),
            or a ChildWorkflowHandle (wait=False).

        Raises:
            WorkflowsException: If the workflow is not properly decorated or configured.

        Example:
            result = await workflow.execute_workflow(
                workflow=DataProcessingWorkflow,
                params=ProcessingParams(data_id="123"),
                execution_timeout=timedelta(minutes=30),
            )

            # Non-blocking:
            handle = await workflow.execute_workflow(
                workflow=BackgroundWorkflow,
                params=BackgroundParams(data_id="456"),
                wait=False,
            )
        """
        return await execute_workflow(
            workflow=workflow,
            params=params,
            execution_timeout=execution_timeout,
            execution_id=execution_id,
            wait=wait,
            parent_close_policy=parent_close_policy,
        )

    @staticmethod
    def now() -> datetime:
        """Return the current workflow time.

        This is a pass-through to `temporalio.workflow.now()` so SDK users can
        rely on `mistralai.workflows.workflow` without importing Temporal.
        """
        return temporalio.workflow.now()

    @staticmethod
    def uuid4() -> UUID:
        """Return a deterministic UUID for the current workflow execution.

        This is a pass-through to `temporalio.workflow.uuid4()` so SDK users can
        rely on `mistralai.workflows.workflow` without importing Temporal.
        """
        return temporalio.workflow.uuid4()

    @staticmethod
    def random() -> Random:
        """Return Temporal's deterministic random generator for the workflow.

        This is a pass-through to `temporalio.workflow.random()` so SDK users can
        rely on `mistralai.workflows.workflow` without importing Temporal.
        """
        return temporalio.workflow.random()

    @staticmethod
    async def wait_condition(
        predicate: Callable[[], bool],
        timeout: timedelta | float | None = None,
        timeout_summary: str | None = None,
    ) -> None:
        """Pauses workflow execution until the given predicate function returns true.

        The predicate is re-evaluated whenever a new event (signal, activity completion, etc.)
        occurs for the workflow. This is an efficient, non-blocking wait that doesn't consume
        resources while waiting. This is a pass-through to temporalio.workflow.wait_condition.

        Args:
            predicate: Non-async callback that accepts no parameters and returns a boolean.
                It will be called repeatedly until it returns True.
            timeout: Optional timeout in seconds (or timedelta) before raising asyncio.TimeoutError.
            timeout_summary: Optional simple string identifying the timer that may be visible
                in Temporal UI/CLI. Best treated as a timer ID.

        Raises:
            asyncio.TimeoutError: If the timeout is reached before predicate returns True.

        Example:
            # Wait for approval signal
            await workflow.wait_condition(
                lambda: self.is_approved,
                timeout=timedelta(hours=24),
                timeout_summary="approval_wait"
            )
        """
        logger.debug("mistralai.workflows.workflow.wait_condition called")

        await temporalio.workflow.wait_condition(predicate, timeout=timeout, timeout_summary=timeout_summary)

    @staticmethod
    def continue_as_new(params: BaseModel) -> None:
        """Continue workflow execution with fresh history.

        Stops the current workflow and starts a new execution with the same workflow ID
        but a new run ID and empty event history. Use this to prevent history from growing
        too large in long-running or iterative workflows.

        Args:
            params: Parameters for the new execution (must be BaseModel)

        Raises:
            WorkflowsException: If called outside workflow context

        Example:
            @workflow.define(name="paginated-processor")
            class PaginatedProcessor:
                @workflow.entrypoint
                async def run(self, params: ProcessorParams):
                    # Process current batch
                    await process_batch(params.page)

                    # Check if we should continue
                    if workflow.should_continue_as_new():
                        next_params = ProcessorParams(page=params.page + 1)
                        workflow.continue_as_new(next_params)

                    # Continue with next page
                    ...
        """
        if not temporalio.workflow.in_workflow():
            raise WorkflowsException(
                code=ErrorCode.WORKFLOW_DEFINITION_ERROR,
                message="continue_as_new can only be called from within a workflow",
            )

        temporalio.workflow.continue_as_new(params.model_dump())

    @staticmethod
    def should_continue_as_new() -> bool:
        """Check if Temporal suggests continuing as new due to history size.

        Returns True when the workflow's event history is approaching size limits.
        Use this to decide when to call continue_as_new() in long-running workflows.

        Returns:
            bool: True if continue-as-new is suggested, False otherwise

        Example:
            while has_more_work():
                await process_batch()

                if workflow.should_continue_as_new():
                    workflow.continue_as_new(get_next_state())
                    return  # Never reached, but good practice
        """
        if not temporalio.workflow.in_workflow():
            return False
        return temporalio.workflow.info().is_continue_as_new_suggested()

    class unsafe:
        # re-export imports_passed_through
        @staticmethod
        @contextmanager
        def imports_passed_through() -> Iterator[None]:
            with temporalio.workflow.unsafe.imports_passed_through():
                yield None

        # re-export sandbox_unrestricted
        @staticmethod
        @contextmanager
        def skip_determinism_enforcement() -> Iterator[None]:
            with temporalio.workflow.unsafe.sandbox_unrestricted():
                yield None
