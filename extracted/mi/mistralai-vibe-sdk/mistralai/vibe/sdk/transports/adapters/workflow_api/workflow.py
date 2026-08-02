"""Workflow wrappers — run any ModuleTask as a durable Temporal workflow.

TaskWorkflowMixin:
  Generic mixin providing workflow integration for any ModuleTask.
  Activities are computed at class definition time via __init_subclass__.
  Signal handlers, callback context setup, and task lifecycle are provided.
  Users write their own @workflow.entrypoint — full control over type
  narrowing and custom logic.

handle_callback_request:
  Shared callback resolution logic for all workflow wrappers. Implements
  4-way dispatch: composable impl → child workflow, leaf impl → activity,
  schema → bubble upstream, unknown → fail. Workflow classes delegate their
  on_callback_request signal handler to this function.

Two-lane architecture:
  Control lane (durable): Temporal history records activity inputs/outputs.
  Observability lane (ephemeral): NATS JetStream carries task() CM events.
  During Temporal replay, task() CM calls are no-ops (should_publish_event() -> False).

See agent_workflow.py for the reference DurableAgentWorkflow implementation.
"""

import typing
from collections.abc import Callable
from importlib import import_module
from typing import Any, cast, get_args

import temporalio.workflow  # type: ignore[reportMissingImports]
from mistralai.workflows import workflow  # type: ignore[reportMissingImports]
from pydantic import BaseModel

with workflow.unsafe.imports_passed_through():
    import structlog
    from structlog.contextvars import bound_contextvars

    from mistralai.vibe.sdk.agent.execution.loop import DownstreamWriter, StateModule
    from mistralai.vibe.sdk.agent.tasks.runtime import (
        ModuleTask,
        TaskConfigBase,
        default_registry,
        extract_impl_configs,
    )
    from mistralai.vibe.sdk.execution_record.patching.types import Op
    from mistralai.vibe.sdk.execution_record.state import FailedOutput, PendingOutput, TaskState
    from mistralai.vibe.sdk.observability import observability_context
    from mistralai.vibe.sdk.transports.adapters.workflow_api.callback import (
        ChildRoute,
        WorkflowCallbackBridge,
        WorkflowCallbackContext,
    )
    from mistralai.vibe.sdk.transports.adapters.workflow_api.executor import (
        WorkflowEffectExecutor,
        _CallbackImplInput,
        make_effect_activities,
        resolve_callback_impl,
    )
    from mistralai.vibe.sdk.transports.adapters.workflow_api.types import WorkflowTaskInput
    from mistralai.vibe.sdk.transports.events import (
        CallbackCallEvent,
        CallbackCallPayload,
        CallbackResultEvent,
        CallbackResultPayload,
        DownstreamMessage,
    )

logger = structlog.get_logger()


def _make_callback_impl_execution_id(parent_exec_id: str | None, request_id: str) -> str:
    """Build a callback implementation execution id scoped to the parent execution."""
    parent_scope = parent_exec_id or "root"
    return f"callback-impl-{parent_scope}-{request_id}"


# ---------------------------------------------------------------------------
# No-op DownstreamWriter — shared across all workflow wrappers
# ---------------------------------------------------------------------------


class WorkflowDownstreamWriter(DownstreamWriter):
    """No-op DownstreamWriter for use inside workflow wrappers.

    send_patches is a no-op because observability is provided by NATS
    events emitted inside activity handlers via WorkflowStateSink.
    """

    def send_patches(self, task_id: str, patches: list[Op]) -> None:
        pass

    def send(self, message: DownstreamMessage) -> None:
        pass


# ---------------------------------------------------------------------------
# Module class resolution
# ---------------------------------------------------------------------------


def _resolve_module_class(task_cls: type[ModuleTask[Any]]) -> type[StateModule]:
    """Get the concrete StateModule class from create_module's return annotation."""
    hints = typing.get_type_hints(task_cls.create_module)
    module_cls = hints.get("return")
    if module_cls is None or not isinstance(module_cls, type):
        msg = (
            f"{task_cls.__name__}.create_module must have a concrete return "
            f"type annotation (e.g. -> AgentModule)"
        )
        raise TypeError(msg)
    return cast(type[StateModule], module_cls)


def _extract_task_cls(cls: type) -> type[ModuleTask[Any]] | None:
    """Extract the TaskT type parameter from a TaskWorkflowMixin subclass.

    Inspects ``__orig_bases__`` (set by Python when a class inherits from
    a parametrized Generic) to find ``TaskWorkflowMixin[TaskT, ConfigT]``
    and returns TaskT if it's a concrete class.
    """
    for base in getattr(cls, "__orig_bases__", ()):
        origin = getattr(base, "__origin__", None)
        if origin is TaskWorkflowMixin:
            args = get_args(base)
            if args and isinstance(args[0], type):
                return args[0]
    return None


# ---------------------------------------------------------------------------
# TaskWorkflowMixin — generic base for durable workflow wrappers
# ---------------------------------------------------------------------------


class TaskWorkflowMixin[TaskT: ModuleTask[Any], ConfigT: BaseModel]:
    """Mixin providing workflow integration for any ModuleTask.

    Type parameters:
      TaskT:    the ModuleTask subclass (e.g. AgentTask)
      ConfigT:  the config type (e.g. AgentTaskConfig)

    Class-level (set by __init_subclass__ from TaskT):
      _task_cls:      extracted from the type parameter at class definition time
      _activity_map:  {effect_type: @activity fn}, computed once at import time

    Instance-level (set by __init__):
      _task_ctx:      WorkflowCallbackContext — mutable signal state

    Subclasses must:
      1. Parametrize both type args: TaskWorkflowMixin[AgentTask, AgentTaskConfig]
      2. Apply @workflow.define on the class
      3. Write their own @workflow.entrypoint method
    """

    _task_cls: type[ModuleTask[ConfigT]]
    _activity_map: dict[type, Callable[..., Any]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        task_cls = _extract_task_cls(cls)
        if task_cls is None:
            msg = (
                f"{cls.__name__} must parametrize TaskWorkflowMixin with a "
                f"concrete ModuleTask class. "
                f"Example: class MyWorkflow(TaskWorkflowMixin[AgentTask, AgentTaskConfig])"
            )
            raise TypeError(msg)
        cls._task_cls = task_cls
        module_cls = _resolve_module_class(task_cls)
        prefix = module_cls.__name__.removesuffix("Module").lower()
        # Compute activities at class definition time (= import time).
        # Temporal requires activities to exist before the worker starts.
        cls._activity_map = make_effect_activities(module_cls.effect_handlers, prefix)

    def __init__(self) -> None:
        self._task_ctx = WorkflowCallbackContext()

    # --- Signal handlers ---

    @workflow.signal("on_callback_result")
    async def _on_callback_result(self, payload: dict[str, Any]) -> None:
        """Receive callback result — keyed by SDK-owned correlation ID."""
        result = CallbackResultEvent.model_validate(payload)
        self._task_ctx.pending_callback_results[result.payload.id] = result

    @workflow.signal("on_callback_request")
    async def _on_callback_request(self, payload: dict[str, Any]) -> None:
        """Receive callback request — delegates to shared handler."""
        await handle_callback_request(self._task_ctx, payload)

    # --- Lifecycle helpers (private for now — may become extension points) ---

    def _prepare_execution(self, input: WorkflowTaskInput[ConfigT]) -> ModuleTask[ConfigT]:
        """Populate _task_ctx from workflow input. Returns the reconstructed task."""
        import contextlib

        self._task_ctx.self_exec_id = ""
        with contextlib.suppress(Exception):
            self._task_ctx.self_exec_id = temporalio.workflow.info().workflow_id
        self._task_ctx.parent_exec_id = input.parent_exec_id
        self._task_ctx.observability_context = input.observability_context

        task = self._task_cls.from_config(input.task_config)
        self._task_ctx.callback_schemas = task.unresolved_callbacks
        self._task_ctx.impl_configs = extract_impl_configs(input.task_config)  # type: ignore[arg-type]
        return task

    def _create_executor(self) -> WorkflowEffectExecutor:
        """Build executor from class activity_map + instance callback_ctx."""
        return WorkflowEffectExecutor(
            activity_map=self._activity_map,
            callback_ctx=self._task_ctx,
        )

    async def run_task(self, input: WorkflowTaskInput[ConfigT]) -> TaskState:
        """Full workflow lifecycle: reconstruct, execute, error wrap, emit.

        Calls _prepare_execution() then runs the reconstructed task.
        """
        task = self._prepare_execution(input)
        executor = self._create_executor()

        with (
            # Rehydrate caller context so reducers build serialized LLM metadata correctly.
            observability_context(**input.observability_context),
            bound_contextvars(task_id=input.task_id),
        ):
            logger.info("workflow.start", task_class=type(task).__name__)
            state = TaskState.model_validate(input.initial_state_dict)
            downstream = WorkflowDownstreamWriter()

            try:
                final = await task.execute(
                    state,
                    downstream,
                    effect_executor=executor,
                )
            except Exception as exc:
                logger.exception("workflow.execute_failed")
                final = state.model_copy(
                    update={"output": FailedOutput(error=f"{type(exc).__name__}: {exc}")}
                )
            logger.info("workflow.end", output_type=type(final.output).__name__)
            return final


# ---------------------------------------------------------------------------
# Shared callback resolution — used by all workflow wrappers
# ---------------------------------------------------------------------------


def _resolve_callback_workflow(impl_config: TaskConfigBase) -> type | None:
    """Check if a callback impl config routes to a child workflow.

    Returns the workflow class if the config type has a workflow binding
    with child dispatch support, otherwise None (→ activity path).
    """
    config_type = impl_config.type
    if not config_type:
        return None
    import_module("mistralai.vibe.sdk.transports.adapters.workflow_api.agent_workflow")
    binding = default_registry.get_binding(config_type)
    if binding and binding.workflow_cls and binding.supports_child_dispatch:
        return binding.workflow_cls
    return None


async def _dispatch_callback_as_workflow(
    ctx: WorkflowCallbackContext,
    request: CallbackCallEvent,
    name: str,
    impl_config: TaskConfigBase,
    workflow_cls: type,
) -> CallbackResultEvent:
    """Dispatch a callback implementation as a child workflow.

    Registers a child route so the impl's own callbacks can bubble back
    to this workflow for resolution.
    """
    child_exec_id = _make_callback_impl_execution_id(ctx.self_exec_id, request.payload.id)
    child_input: WorkflowTaskInput[Any] = WorkflowTaskInput(
        task_config=impl_config,
        task_id=request.payload.id,
        initial_state_dict=TaskState(
            id=request.payload.id,
            input=request.payload.input,
            output=PendingOutput(),
        ).model_dump(),
        parent_exec_id=ctx.self_exec_id,
        observability_context=ctx.observability_context,
    )

    # Register child route so the impl's own callbacks can bubble here
    ctx.child_routes[child_exec_id] = ChildRoute(
        child_exec_id=child_exec_id,
        path_segment=request.payload.id,
    )

    logger.info(
        "workflow.callback_impl_workflow.start",
        child_exec_id=child_exec_id,
        name=name,
    )
    result_raw = await workflow.execute_workflow(
        workflow=workflow_cls,
        params=child_input,
        execution_id=child_exec_id,
    )
    logger.info(
        "workflow.callback_impl_workflow.done",
        child_exec_id=child_exec_id,
        name=name,
    )
    result_state = (
        result_raw if isinstance(result_raw, TaskState) else TaskState.model_validate(result_raw)
    )
    return CallbackResultEvent(
        payload=CallbackResultPayload(id=request.payload.id, name=name, state=result_state, path=[])
    )


async def handle_callback_request(ctx: WorkflowCallbackContext, payload: dict[str, Any]) -> None:
    """Resolve a callback request from a child workflow.

    Shared logic for all workflow wrappers. Signal handlers delegate here.

    Resolution order:
    1. Name in impl_configs with workflow binding → child workflow
    2. Name in impl_configs without workflow binding → activity
    3. Name in callback_schemas → bubble upstream via signal
    4. Unknown → send FailedOutput back to child
    """
    source_exec_id: str = payload.pop("_source_exec_id")
    request = CallbackCallEvent.model_validate(payload)
    route = ctx.child_routes.get(source_exec_id)
    if route is None:
        logger.warning(
            "workflow.callback_request.unknown_child",
            source_exec_id=source_exec_id,
        )
        handle = temporalio.workflow.get_external_workflow_handle(source_exec_id)
        fail_event = CallbackResultEvent(
            payload=CallbackResultPayload(
                id=request.payload.id,
                name=request.payload.name,
                state=TaskState(
                    id=request.payload.id,
                    input=request.payload.input,
                    output=FailedOutput(error=f"Unknown child route: {source_exec_id}"),
                ),
                path=[],
            )
        )
        await handle.signal("on_callback_result", {"payload": fail_event.model_dump()})
        return

    name = request.payload.name
    logger.info(
        "workflow.callback_request",
        name=name,
        source_exec_id=source_exec_id,
        has_impl=name in ctx.impl_configs,
        has_schema=name in ctx.callback_schemas,
    )

    if name in ctx.impl_configs:
        impl_config = ctx.impl_configs[name]
        workflow_cls = _resolve_callback_workflow(impl_config)
        if workflow_cls is not None:
            logger.info(
                "workflow.callback_request.child_workflow",
                name=name,
                workflow_cls=workflow_cls.__name__,
            )
            result_event = await _dispatch_callback_as_workflow(
                ctx, request, name, impl_config, workflow_cls
            )
        else:
            result = await resolve_callback_impl(
                _CallbackImplInput(
                    request_id=request.payload.id,
                    request_input=request.payload.input,
                    impl_config=impl_config,
                )
            )
            result_state = TaskState.model_validate(result.state)
            result_event = CallbackResultEvent(
                payload=CallbackResultPayload(
                    id=request.payload.id, name=name, state=result_state, path=[]
                )
            )
    elif name in ctx.callback_schemas:
        bubble_bridge = WorkflowCallbackBridge(
            parent_exec_id=ctx.parent_exec_id,
            self_exec_id=ctx.self_exec_id,
            pending_results=ctx.pending_callback_results,
        )
        bubbled = CallbackCallEvent(
            payload=CallbackCallPayload(
                id=request.payload.id,
                name=request.payload.name,
                input=request.payload.input,
                path=[route.path_segment, *request.payload.path],
            )
        )
        await bubble_bridge.send_request(bubbled)
        upstream_result = await bubble_bridge.receive_result(request.payload.id)
        result_event = upstream_result
    else:
        result_event = CallbackResultEvent(
            payload=CallbackResultPayload(
                id=request.payload.id,
                name=name,
                state=TaskState(
                    id=request.payload.id,
                    input=request.payload.input,
                    output=FailedOutput(error=f"Unhandled callback: {name}"),
                ),
                path=[],
            )
        )

    handle = temporalio.workflow.get_external_workflow_handle(source_exec_id)
    await handle.signal("on_callback_result", {"payload": result_event.model_dump()})
