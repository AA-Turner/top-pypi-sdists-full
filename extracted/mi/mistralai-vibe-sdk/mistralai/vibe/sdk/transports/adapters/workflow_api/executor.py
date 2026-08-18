"""WorkflowEffectExecutor and make_effect_activities for the workflow adapter.

Routes effects by category: activity effects to named Temporal activities,
composable subtasks to child workflows. make_effect_activities auto-wraps
standalone handler functions as @activity
decorated functions, producing per-effect named activities for Temporal UI
observability (e.g. agent_CallLLM, agent_SpawnSubTask).

Action serialization:
  Each generated activity wraps its return value in a dynamically-created
  Pydantic ResultModel (e.g. agent_CallLLM_Result) whose ``actions`` field
  carries the concrete action list type (e.g. list[LLMTurnComplete]).
  Because Temporal always deserializes a top-level BaseModel correctly,
  the actions are fully rehydrated on the workflow side — no manual
  tag-and-rehydrate step needed.

  Handler functions MUST have a concrete return type annotation
  (e.g. ``-> list[LLMTurnComplete]``) so the ResultModel field type is
  specific enough for Pydantic to validate.

Child-workflow routing:
  Uses ModuleTaskRegistry to decide whether a SpawnSubTask should dispatch
  as a child workflow. The routing rule:
  - Extract config type name from effect.task_config
  - Look up binding in the registry
  - If spec.workflow_cls is not None AND spec.supports_child_dispatch → child workflow
  - Otherwise → activity (local handler)
"""

from collections.abc import Callable, Iterable
from datetime import timedelta
from importlib import import_module
from typing import Any

import structlog
from mistralai.workflows import activity, workflow  # type: ignore[reportMissingImports]
from mistralai.workflows import task as workflow_task  # type: ignore[reportMissingImports]
from pydantic import BaseModel, SerializeAsAny, create_model
from structlog.contextvars import bound_contextvars
from temporalio import activity as temporal_activity  # type: ignore[reportMissingImports]

from mistralai.vibe.sdk.agent.execution.compaction import COMPACTION_STREAM_NAME
from mistralai.vibe.sdk.agent.execution.loop import EffectExecutor, EffectRegistry
from mistralai.vibe.sdk.agent.execution.resources import (
    ResourcesScope,
    bind_execution_scope,
)
from mistralai.vibe.sdk.agent.execution.sub_task import (
    CallbackResultReceived,
    CallCallback,
    SpawnSubTask,
    SubTaskCompleted,
)
from mistralai.vibe.sdk.agent.tasks.runtime import TaskConfigBase
from mistralai.vibe.sdk.execution_record.state import TaskState
from mistralai.vibe.sdk.observability import COMMON_CONTEXT_KEYS, attributes_from_context
from mistralai.vibe.sdk.providers.completion.tokens import latest_compaction_sentinel_index
from mistralai.vibe.sdk.transports.adapters.workflow_api.callback import (
    ChildRoute,
    WorkflowCallbackBridge,
    WorkflowCallbackContext,
)
from mistralai.vibe.sdk.transports.adapters.workflow_api.streaming import (
    LLM_STREAM_NAME,
    WorkflowStateSink,
)
from mistralai.vibe.sdk.transports.adapters.workflow_api.types import WorkflowTaskInput
from mistralai.vibe.sdk.transports.events import CallbackCallEvent, CallbackCallPayload

logger = structlog.get_logger()
NO_RETRY_MAX_ATTEMPTS = 1


def _extract_state(effect: Any) -> TaskState | None:
    """Extract the TaskState carried by an effect.

    All activity-bound effects carry a ``state: TaskState`` field.
    Returns None only if the field is missing (shouldn't happen in practice).
    """
    state = getattr(effect, "state", None)
    return state if isinstance(state, TaskState) else None


def _stream_initial_state(effect: Any, state: TaskState | None) -> TaskState | None:
    """Return the state baseline used by the workflow streaming sink."""
    if state is None or getattr(effect, "stream_name", None) != COMPACTION_STREAM_NAME:
        return state
    index = latest_compaction_sentinel_index(state)
    if index < 0:
        return state
    history = state.history
    return state.model_copy(update={"history": [*history[:index], *history[index + 1 :]]})


def make_effect_activities(
    handler_map: EffectRegistry,
    prefix: str,
) -> dict[type, Callable[..., Any]]:
    """Wrap each handler as a @activity. Returns {effect_type: activity_fn}.

    Each generated activity:
    1. Constructs a WorkflowStateSink from the effect's state
    2. Calls the standalone handler with (effect, sink)
    3. Wraps the result in a typed ResultModel for Temporal serialization

    Handler functions must have a concrete return type annotation
    (e.g. ``-> list[LLMTurnComplete]``). This type is embedded in the
    ResultModel so Temporal + Pydantic can deserialize actions correctly.

    Most users should not call this directly — instead, subclass
    ``TaskWorkflowMixin`` which calls this automatically at class
    definition time with the correct handler_map and prefix.

    __annotations__ must be set BEFORE applying @activity — the decorator
    introspects type annotations at decoration time for Pydantic deserialization.
    """
    activities: dict[type, Callable[..., Any]] = {}
    for effect_type, handler_fn in handler_map.items():
        activities[effect_type] = _make_activity(
            effect_type,
            handler_fn,
            prefix,
        )
    return activities


def _make_activity(
    effect_type: type,
    handler_fn: Callable[..., Any],
    prefix: str,
) -> Callable[..., Any]:
    """Create a single @activity wrapper for one effect handler.

    Uses a factory function to capture handler_fn in a proper closure,
    avoiding keyword-only default arg patterns that confuse the @activity
    decorator's signature introspection.

    The handler's return type annotation (e.g. list[LLMTurnComplete]) is
    used to create a typed ResultModel. This ensures Temporal deserializes
    the activity result into concrete Pydantic models, not raw dicts.

    Activities are configured with a heartbeat_timeout so Temporal can
    detect stuck activities. The wrapper calls heartbeat() periodically
    via a background task.
    """
    activity_name = f"{prefix}_{effect_type.__name__}"
    return_type = handler_fn.__annotations__.get("return", list)
    result_model = create_model(f"{activity_name}_Result", actions=(return_type, ...))

    async def wrapped(effect_data: Any) -> Any:
        import asyncio

        state = _extract_state(effect_data)
        task_id = state.id if state is not None else "unknown"
        with bound_contextvars(
            activity=activity_name,
            task_id=task_id,
        ):
            logger.debug("activity.start")
            stream_name = getattr(effect_data, "stream_name", LLM_STREAM_NAME)
            sink = WorkflowStateSink(
                task_id,
                initial_state=_stream_initial_state(effect_data, state),
                stream_name=stream_name,
                stream_sequence=WorkflowStateSink._derive_stream_sequence(stream_name, state),
            )

            # Periodic heartbeat so Temporal knows the activity is alive
            heartbeat_task = asyncio.create_task(_heartbeat_loop())
            scope = ResourcesScope()
            try:
                with bind_execution_scope(scope):
                    result: list[Any] = await handler_fn(effect_data, sink)
            except Exception:
                logger.exception("activity.failed")
                raise
            finally:
                heartbeat_task.cancel()
                try:
                    await scope.aclose()
                except Exception:
                    logger.exception("activity.scope_finalize_failed")
            logger.debug("activity.done", action_count=len(result))
            return result_model(actions=result)

    wrapped.__name__ = activity_name
    wrapped.__qualname__ = activity_name
    # Annotations must be set before @activity inspects them
    wrapped.__annotations__ = {"effect_data": effect_type, "return": result_model}
    return activity(
        start_to_close_timeout=timedelta(minutes=10),
        retry_policy_max_attempts=NO_RETRY_MAX_ATTEMPTS,
        heartbeat_timeout=timedelta(minutes=2),
    )(wrapped)


async def _heartbeat_loop(interval: float = 30.0) -> None:
    """Send periodic heartbeats to Temporal while an activity is running."""
    import asyncio
    import contextlib

    while True:
        await asyncio.sleep(interval)
        with contextlib.suppress(Exception):
            temporal_activity.heartbeat()


# ---------------------------------------------------------------------------
# Callback resolution activity — runs implementation tasks outside workflow thread
# ---------------------------------------------------------------------------


class _CallbackImplInput(BaseModel):
    """Input for the resolve_callback_impl activity."""

    request_id: str
    request_input: Any = None
    impl_config: SerializeAsAny[TaskConfigBase]


class _CallbackImplOutput(BaseModel):
    """Output from the resolve_callback_impl activity."""

    state: dict[str, Any]


@activity(
    start_to_close_timeout=timedelta(minutes=10),
    retry_policy_max_attempts=NO_RETRY_MAX_ATTEMPTS,
)
async def resolve_callback_impl(input: _CallbackImplInput) -> _CallbackImplOutput:
    """Run a callback implementation task as an activity.

    Reconstructs the task from config, runs it to completion, and returns
    the final state. This runs in an activity thread where I/O is permitted,
    unlike the workflow's deterministic thread where signal handlers execute.
    """
    from mistralai.vibe.sdk.agent.tasks.runtime import task_from_config
    from mistralai.vibe.sdk.execution_record.patching.json_patch import apply_patches
    from mistralai.vibe.sdk.execution_record.state import PendingOutput
    from mistralai.vibe.sdk.transports.events import TaskResultEvent, TaskStateUpdateEvent

    with bound_contextvars(activity="resolve_callback_impl", request_id=input.request_id):
        logger.info("callback_impl.start")
        task = task_from_config(input.impl_config)
        state = TaskState(
            id=input.request_id,
            input=input.request_input,
            output=PendingOutput(),
        )
        scope = ResourcesScope()
        try:
            with bind_execution_scope(scope):
                channel = await task.run(state)
                async for msg in channel:
                    if isinstance(msg, TaskStateUpdateEvent):
                        state = apply_patches(state, msg.payload.patches)
                    elif isinstance(msg, TaskResultEvent):
                        state = msg.payload.result
                    elif isinstance(msg, CallbackCallEvent):
                        logger.warning(
                            "callback_impl.nested_callback_dropped",
                            callback_name=msg.payload.name,
                            callback_id=msg.payload.id,
                        )
        finally:
            try:
                await scope.aclose()
            except Exception:
                logger.exception("callback_impl.scope_finalize_failed")
        logger.info("callback_impl.done")
        return _CallbackImplOutput(state=state.model_dump())


def _get_config_type_name(task_config: Any) -> str:
    """Extract the config type name from a task_config instance."""
    if isinstance(task_config, TaskConfigBase):
        return str(task_config.type)
    return ""


class WorkflowEffectExecutor(EffectExecutor):
    """Routes effects by category: activities, child workflows, or signals.

    Three-way dispatch (DL-50):
    1. SpawnSubTask → child workflow (registry routing) or activity
    2. CallCallback → inline signal-based handler (no activity boundary)
    3. activity_map lookup → named Temporal activity

    CallCallback is a signal effect and MUST NOT appear in the activity_map.
    Sending Temporal signals from inside an activity is forbidden.

    The optional ``registry`` parameter is for **test isolation only** —
    it scopes routing lookups within a single process. It does not
    propagate across the Temporal serialization boundary: child workflows
    and activities reconstruct tasks via ``default_registry``. The worker
    process must install matching extensions globally.
    """

    def __init__(
        self,
        activity_map: dict[type, Callable[..., Any]],
        registry: Any = None,
        callback_ctx: "WorkflowCallbackContext | None" = None,
    ) -> None:
        self._activity_map = activity_map
        self._registry = registry
        self._callback_ctx = callback_ctx

    def _get_registry(self) -> Any:
        if self._registry is not None:
            return self._registry
        from mistralai.vibe.sdk.agent.tasks.runtime import default_registry

        return default_registry

    def _resolve_child_workflow(self, task_config: Any) -> type | None:
        """Return the workflow class if child dispatch is supported, else None."""
        registry = self._get_registry()
        type_name = _get_config_type_name(task_config)
        if not type_name:
            return None
        import_module("mistralai.vibe.sdk.transports.adapters.workflow_api.agent_workflow")
        binding = registry.get_binding(type_name)
        if binding is None:
            return None
        if binding.workflow_cls is not None and binding.supports_child_dispatch:
            wf_cls: type = binding.workflow_cls
            return wf_cls
        return None

    async def execute(self, effect: Any) -> list[Any]:
        effect_type = type(effect)

        # 1. Composable subtask → child workflow via registry routing
        if isinstance(effect, SpawnSubTask):
            workflow_cls = self._resolve_child_workflow(effect.task_config)
            if workflow_cls is not None:
                logger.debug(
                    "executor.dispatch",
                    effect=effect_type.__name__,
                    route="child_workflow",
                    child_task=effect.call.payload.name,
                )
                return await self._dispatch_child_workflow(effect, workflow_cls)

        # 2. CallCallback → inline signal-based handler (DL-50)
        if isinstance(effect, CallCallback):
            logger.debug(
                "executor.dispatch",
                effect=effect_type.__name__,
                route="signal",
            )
            return await self._dispatch_callback(effect)

        # 3. Activity map lookup
        if effect_type in self._activity_map:
            logger.debug(
                "executor.dispatch",
                effect=effect_type.__name__,
                route="activity",
            )
            raw: Any = await self._activity_map[effect_type](effect)
            actions: Any | None = (
                getattr(raw, "actions", None) if isinstance(raw, BaseModel) else None
            )
            # Unwrap ResultModel from real activities; pass through raw lists
            # from test mocks that bypass Temporal serialization.
            if actions is not None and isinstance(actions, Iterable):
                return list(actions)
            return list(raw)
        msg = f"No handler for {effect_type}"
        raise NotImplementedError(msg)

    async def _dispatch_child_workflow(
        self, effect: SpawnSubTask, workflow_cls: type
    ) -> list[SubTaskCompleted]:
        """Dispatch a composable subtask as a child Temporal workflow.

        Emits parent_state_sync and child_mapping markers before starting the
        child so the client channel can project live child updates into the
        parent's pending result slot.
        """
        child_exec_id = effect.child_state.id
        prefix = f"/history/{effect.result_index}/payload/state"

        if effect.task_config is None:
            msg = "Cannot dispatch child workflow without task_config"
            raise ValueError(msg)
        config = effect.task_config
        # Pass parent_exec_id so the child can signal back for callbacks
        parent_exec_id = self._callback_ctx.self_exec_id if self._callback_ctx else None
        child_input: WorkflowTaskInput[Any] = WorkflowTaskInput(
            task_config=config,
            task_id=effect.child_state.id,
            initial_state_dict=effect.child_state.model_dump(),
            parent_exec_id=parent_exec_id,
            observability_context=attributes_from_context(*COMMON_CONTEXT_KEYS),
        )

        # Register child route for callback resolution (DL-49)
        if self._callback_ctx is not None:
            self._callback_ctx.child_routes[child_exec_id] = ChildRoute(
                child_exec_id=child_exec_id,
                path_segment=effect.child_state.id,
            )

        logger.info(
            "executor.child_workflow.start",
            child_exec_id=child_exec_id,
            child_task_id=effect.child_state.id,
            prefix=prefix,
        )

        async with workflow_task(
            "parent_state_sync",
            state=effect.state.model_dump(),
            id=f"sync-{child_exec_id}",
        ):
            pass

        async with workflow_task(
            "child_mapping",
            state={"child_exec_id": child_exec_id, "prefix": prefix},
            id=f"mapping-{child_exec_id}",
        ):
            pass

        try:
            result = await workflow.execute_workflow(
                workflow=workflow_cls,
                params=child_input,
                execution_id=child_exec_id,
            )
        except Exception:
            logger.exception(
                "executor.child_workflow.failed",
                child_exec_id=child_exec_id,
            )
            raise
        logger.info(
            "executor.child_workflow.done",
            child_exec_id=child_exec_id,
        )
        # run_task returns TaskState; Temporal may deliver
        # it as a dict after JSON round-trip.
        final_state = result if isinstance(result, TaskState) else TaskState.model_validate(result)
        return [SubTaskCompleted(call_id=effect.call.payload.id, final_state=final_state)]

    async def _dispatch_callback(self, effect: CallCallback) -> list[CallbackResultReceived]:
        """Handle CallCallback inline via signal-based WorkflowCallbackBridge.

        Runs in workflow code — no activity boundary. Constructs a
        WorkflowCallbackBridge, sends the callback request, waits for the
        result, and returns CallbackResultReceived.
        """
        if self._callback_ctx is None:
            msg = "CallCallback requires callback_ctx on WorkflowEffectExecutor"
            raise RuntimeError(msg)

        bridge = WorkflowCallbackBridge(
            parent_exec_id=self._callback_ctx.parent_exec_id,
            self_exec_id=self._callback_ctx.self_exec_id,
            pending_results=self._callback_ctx.pending_callback_results,
        )

        call_event = CallbackCallEvent(
            payload=CallbackCallPayload(
                id=effect.call.payload.id,
                name=effect.call.payload.name,
                input=effect.call.payload.input,
            )
        )
        await bridge.send_request(call_event)
        result = await bridge.receive_result(effect.call.payload.id)

        return [
            CallbackResultReceived(
                call_id=effect.call.payload.id,
                result_state=result.payload.state,
            )
        ]
