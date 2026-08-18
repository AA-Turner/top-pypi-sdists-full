"""Agent pattern — LLM-driven task with tool calling and subtask orchestration.

AgentTask drives a conversation loop: call LLM → execute tool calls → repeat,
using ExecutionLoop for action processing and sub_task_reducer for child tasks.
"""

import json
from typing import Annotated, Any, ClassVar, Literal

import structlog
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SerializeAsAny,
    StringConstraints,
    TypeAdapter,
    ValidationError,
)

from mistralai.vibe.sdk.agent.execution.compaction import (
    COMPACTION_STREAM_NAME,
    _latest_user_message_index,
    has_compactable_history,
    make_compaction_entry,
    run_compaction,
)
from mistralai.vibe.sdk.agent.execution.completion_request_telemetry import (
    emit_completion_request_sent,
)
from mistralai.vibe.sdk.agent.execution.loop import (
    AppendHistoryScope,
    CallbackBridge,
    DownstreamWriter,
    EffectRegistry,
    ExecutionLoop,
    FixedHistoryScope,
    HistoryScope,
    LocalCallbackBridge,
    StateModule,
    StateSink,
)
from mistralai.vibe.sdk.agent.execution.resources import spawn_child_scope
from mistralai.vibe.sdk.agent.execution.sub_task import (
    CallbackResultReceived,
    CallCallback,
    FailSubTask,
    SpawnSubTask,
    SubTaskCallRequest,
    SubTaskCompleted,
    _update_result_entry,
    resolve_callback_request,
    sub_task_reducer,
)
from mistralai.vibe.sdk.agent.tasks.core import TaskCallback
from mistralai.vibe.sdk.agent.tasks.runtime import ModuleTask, TaskConfigBase, task_from_config
from mistralai.vibe.sdk.capabilities.mcp.call_tool import mcp_tool_configs_from_history
from mistralai.vibe.sdk.capabilities.mcp.config import McpConfigBase
from mistralai.vibe.sdk.capabilities.mcp.initialization import (
    MCP_INITIALIZATION_TYPE,
    McpInitError,
    McpInitializationContent,
    McpInitOk,
    discover_mcp_tools,
)
from mistralai.vibe.sdk.execution_record.patching.json_patch import apply_patches, reroute_patches
from mistralai.vibe.sdk.execution_record.patching.produce import diff
from mistralai.vibe.sdk.execution_record.state import (
    CompletedOutput,
    ContentBlock,
    FailedOutput,
    ImageContentBlock,
    MessageEntry,
    MessageEntryPayload,
    StateEntry,
    StateEntryPayload,
    TaskCallEntry,
    TaskResultEntry,
    TaskState,
    TextContentBlock,
    ThinkingContentBlock,
    content_blocks,
)
from mistralai.vibe.sdk.observability import (
    RequestMetadata,
    TelemetryCallType,
    observability_context,
)
from mistralai.vibe.sdk.providers.completion.bridge import (
    build_completion_request_from_state,
    stream_states,
)
from mistralai.vibe.sdk.providers.completion.config import (
    CompletionConfig,
    MistralCompletionConfig,
    completion_config_from_obj,
    completion_from_config,
)
from mistralai.vibe.sdk.providers.completion.errors import (
    CompletionContextTooLargeError,
    is_context_too_large_error,
)
from mistralai.vibe.sdk.providers.completion.tokens import (
    estimate_context_tokens,
    latest_compaction_sentinel_index,
)
from mistralai.vibe.sdk.providers.completion.types import (
    COMPLETION_USAGE_ANNOTATION,
)
from mistralai.vibe.sdk.providers.completion.usage import TokenUsage
from mistralai.vibe.sdk.transports.events import (
    CallbackCallEvent,
    CallbackCallPayload,
    TaskResultEvent,
    TaskStateUpdateEvent,
)

logger = structlog.get_logger()
_CONTENT_BLOCKS_ADAPTER = TypeAdapter(list[ContentBlock])
_CONTENT_BLOCK_MODEL_TYPES = (
    TextContentBlock,
    ThinkingContentBlock,
    ImageContentBlock,
)
_CONTENT_BLOCK_REQUIRED_FIELDS = {
    "text": "text",
    "thinking": "thinking",
    "image": "image_url",
}

__all__ = [
    "AgentAction",
    "AgentEffect",
    "AgentModule",
    "AgentTask",
    "AgentTaskConfig",
    "CallCompactionLLM",
    "CallLLM",
    "CompactionStatusUpdated",
    "ContextOverflowed",
    "Continue",
    "Initialize",
    "InitializeMcp",
    "LLMTurnComplete",
    "McpInitialized",
    "PrepareLLMTurn",
    "StartCompaction",
    "_handle_call_compaction_llm",
    "_handle_call_llm",
    "_handle_continue",
    "_handle_initialize_mcp",
    "_handle_spawn_subtask",
]


def _looks_like_content_blocks(value: object) -> bool:
    if not isinstance(value, list) or not value:
        return False

    for block in value:
        if isinstance(block, _CONTENT_BLOCK_MODEL_TYPES):
            continue
        if not isinstance(block, dict):
            return False
        block_type = block.get("type")
        if not isinstance(block_type, str):
            return False
        required_field = _CONTENT_BLOCK_REQUIRED_FIELDS.get(block_type)
        if required_field is None or required_field not in block:
            return False
    return True


# ---------------------------------------------------------------------------
# Serializable task config
# ---------------------------------------------------------------------------


class AgentTaskConfig(TaskConfigBase):
    """Config for reconstructing an AgentTask."""

    model_config = ConfigDict(extra="forbid")

    type: Literal["agent"] = "agent"
    completion: SerializeAsAny[CompletionConfig]
    name: str = ""
    description: str = ""
    input_schema: dict[str, Any] | None = None
    system_prompt: str | None = None
    max_iterations: int | None = None
    auto_compact_threshold: int = 0
    compaction_prompt: Annotated[str, StringConstraints(strip_whitespace=True)] | None = None
    tasks: dict[str, SerializeAsAny["TaskConfigBase"]] = {}
    callback_implems: dict[str, SerializeAsAny["TaskConfigBase"]] = {}
    direct_callbacks: list[TaskCallback] = []
    mcps: dict[str, SerializeAsAny["McpConfigBase"]] = {}


# ---------------------------------------------------------------------------
# AgentTask internal actions (reducer inputs) — Pydantic for activity return boundary
# ---------------------------------------------------------------------------


class Initialize(BaseModel):
    """Dispatched once at startup to kick off the first LLM call."""


class _LLMRequestTelemetry(BaseModel):
    metadata: dict[str, Any] | None = None
    post_compaction_metadata: dict[str, Any] | None = None

    def preserve_for_post_compaction(self) -> "_LLMRequestTelemetry":
        return self.model_copy(update={"post_compaction_metadata": self.metadata})


class McpInitialized(BaseModel):
    """Dispatched when one MCP initialization has produced a summary."""

    entry: StateEntry | None = None


class PrepareLLMTurn(BaseModel):
    """Internal action for the normalized pre-LLM-turn boundary."""

    telemetry: _LLMRequestTelemetry = Field(default_factory=_LLMRequestTelemetry)


class LLMTurnComplete(BaseModel):
    """Dispatched when the LLM finishes a turn.

    `response` carries the complete assistant MessageEntry values produced
    by the turn in streamed order. The reducer appends them authoritatively,
    since streaming goes through the sink and never touches the reducer's
    state.
    """

    response: Annotated[list[MessageEntry], Field(default_factory=list)]
    tool_calls: Annotated[list[TaskCallEntry], Field(default_factory=list)]
    usage: TokenUsage | None = None
    stream_scope: HistoryScope | None = None


class ContextOverflowed(BaseModel):
    """Dispatched when an LLM call hit the context limit before streaming."""

    can_retry: bool
    telemetry: _LLMRequestTelemetry = Field(default_factory=_LLMRequestTelemetry)


class StartCompaction(BaseModel):
    """Mark the beginning of a compaction. ``preserve_latest_user`` keeps the latest user message
    after the sentinel (threshold compaction) or folds it into the summary (overflow)."""

    preserve_latest_user: bool
    telemetry: _LLMRequestTelemetry = Field(default_factory=_LLMRequestTelemetry)


class CompactionStatusUpdated(BaseModel):
    """Dispatched with the finalized compaction entry."""

    entry: StateEntry
    retry_context_overflow: bool
    telemetry: _LLMRequestTelemetry = Field(default_factory=_LLMRequestTelemetry)
    error: str | None = None
    stream_scope: HistoryScope | None = None


# Full action union for the agent's StateModule
AgentAction = (
    Initialize
    | McpInitialized
    | PrepareLLMTurn
    | LLMTurnComplete
    | ContextOverflowed
    | StartCompaction
    | CompactionStatusUpdated
    | SubTaskCallRequest
    | SubTaskCompleted
    | CallbackResultReceived
)


# ---------------------------------------------------------------------------
# AgentTask internal effects — Pydantic for Temporal serialization
# ---------------------------------------------------------------------------


class CallLLM(BaseModel):
    """Effect: call the LLM with current state.

    Self-contained — carries all state needed for execution so the handler
    does not need to read from the execution loop.
    """

    state: TaskState  # parent state — handler builds completion request from this
    completion: SerializeAsAny[CompletionConfig]
    tools: dict[str, Any]  # llm-visible tool schemas (serializable)
    telemetry: _LLMRequestTelemetry = Field(default_factory=_LLMRequestTelemetry)
    retry_context_overflow: bool = True


class CallCompactionLLM(BaseModel):
    """Effect: summarize the conversation and finalize the running sentinel."""

    state: TaskState
    completion: SerializeAsAny[CompletionConfig]
    tools: dict[str, Any]
    threshold: int
    telemetry: _LLMRequestTelemetry = Field(default_factory=_LLMRequestTelemetry)
    preserve_latest_user: bool = True
    compaction_prompt: str | None = None

    # Stream namespace for the workflow activity (not serialized state). The workflow
    # streaming layer uses this both to keep the compaction stream id distinct from the
    # following LLM turn and to know it must drop the running sentinel from the stream
    # baseline.
    stream_name: ClassVar[str] = COMPACTION_STREAM_NAME


class Continue[ActionT: AgentAction](BaseModel):
    """Internal effect: defer an action to the next drain cycle.

    The handler returns ``[with_action]``, the execution loop drains it after
    the whole effect batch completes, so it is safe to emit alongside other
    effects that run in parallel.
    """

    with_action: ActionT


class InitializeMcp(BaseModel):
    """Effect: initialize one MCP server."""

    mcp_name: str
    mcp_config: SerializeAsAny[McpConfigBase]


AgentEffect = (
    CallLLM
    | CallCompactionLLM
    | InitializeMcp
    | SpawnSubTask
    | CallCallback
    | FailSubTask
    | Continue[AgentAction]
)


# ---------------------------------------------------------------------------
# Effect handler registry
# ---------------------------------------------------------------------------

_registry = EffectRegistry()


# ---------------------------------------------------------------------------
# AgentModule — StateModule subclass for agent lifecycle
# ---------------------------------------------------------------------------

# :TODO:agent [A3] Extract llm_turn_reducer as composable building blocks
# (like sub_task_reducer). Deferred — wait for second LLM-driving StateModule.


def _response_with_usage_annotation(
    response: MessageEntry,
    usage: TokenUsage | None,
    *,
    provider: str,
    model: str,
) -> MessageEntry:
    if usage is None:
        return response

    annotations = dict(response.annotations or {})
    annotations[COMPLETION_USAGE_ANNOTATION] = usage.annotation(provider=provider, model=model)
    return response.model_copy(update={"annotations": annotations})


def _llm_request_metadata(
    state: TaskState, call_type: TelemetryCallType = "main_call"
) -> dict[str, Any]:
    with observability_context(call_type=call_type, message_id=state.id):
        return RequestMetadata.build_from_context()


class AgentModule(StateModule):
    """StateModule for an LLM-driven agent.

    Combines the master reducer (routing to sub-reducers by action type)
    and effect handlers (LLM calls, subtask spawning, callbacks).
    """

    effect_handlers = _registry
    initial_action_type = Initialize

    def __init__(
        self,
        completion: CompletionConfig,
        tasks: dict[str, Any],
        max_iterations: int | None,
        system_prompt: str | None = None,
        callback_implems: dict[str, Any] | None = None,
        callback_schemas: dict[str, TaskCallback] | None = None,
        task_configs: dict[str, TaskConfigBase] | None = None,
        auto_compact_threshold: int = 0,
        compaction_prompt: str | None = None,
        mcp_configs: dict[str, McpConfigBase] | None = None,
    ) -> None:
        """Initialize the agent module.

        Args:
            completion: Serializable completion configuration used by LLM effects.
            tasks: Subtask implementations visible to the LLM. Used for
                spawning subtasks and presented as tool definitions.
            max_iterations: Maximum number of LLM calls before the loop is
                forcibly completed. None means unlimited.
            system_prompt: Optional system message. When provided and history
                is empty, the Initialize reducer injects it as the first
                history entry (along with the user input).
            callback_implems: Callback implementations NOT visible to the LLM.
                Resolve children's callback requests locally. Merged with
                tasks into the internal resolution table.
            callback_schemas: Callback schemas keyed by name. When a call
                targets a callback name (not in the resolution table), the
                request is emitted downstream for the parent to resolve.
                Also presented to the LLM as callable tools.
            task_configs: Serializable task configs keyed by name. Stored on
                SpawnSubTask effects so the activity handler can reconstruct
                tasks without a global registry. None on the local path
                (handler uses resolvable_tasks directly).
            mcp_configs: Serializable MCP server configs keyed by name.
        """
        self._completion = completion
        self._provider_name = completion.type
        self._model_name = completion.model
        self._system_prompt = system_prompt
        self._tasks = tasks
        self._callback_implems = callback_implems or {}
        self._max_iterations = max_iterations
        self._auto_compact_threshold = auto_compact_threshold
        self._compaction_prompt = compaction_prompt
        self._callback_schemas = callback_schemas or {}
        self._task_configs = task_configs or {}
        self._mcp_configs = mcp_configs if mcp_configs is not None else {}
        self._all_resolvable: dict[str, Any] = {**self._tasks, **self._callback_implems}
        self._exec_loop: ExecutionLoop | None = None  # set via bind_exec_loop()
        self._downstream: DownstreamWriter | None = None

        # Pre-compute serializable tool definitions for CallLLM effects.
        # Merges tasks + callback_schemas into a dict of {name: {description, input_schema}}.
        tools_serialized: dict[str, Any] = {}
        for name, task in self._tasks.items():
            tools_serialized[name] = {
                "description": getattr(task, "description", "") or "",
                "input_schema": getattr(task, "input_schema", None) or {},
            }
        for name, cb in self._callback_schemas.items():
            tools_serialized[name] = {
                "description": cb.card.description or "",
                "input_schema": cb.card.input_schema or {},
            }
        self._tools_serialized = tools_serialized

    def bind_exec_loop(
        self,
        loop: ExecutionLoop,
        downstream: "DownstreamWriter | None" = None,
    ) -> None:
        self._exec_loop = loop
        self._downstream = downstream

    def _inject_initial_messages(self, state: TaskState) -> tuple[TaskState, list[Any]]:
        """Inject system prompt and input-as-user-message into empty history.

        Returns (new_state, patches). No-op if history is non-empty.
        """
        initial_entries: list[MessageEntry] = []
        if self._system_prompt:
            initial_entries.append(
                MessageEntry(
                    payload=MessageEntryPayload(
                        role="system", content=content_blocks(self._system_prompt)
                    ),
                )
            )
        if state.input is not None:
            if isinstance(state.input, str):
                user_content = content_blocks(state.input)
            elif _looks_like_content_blocks(state.input):
                try:
                    user_content = _CONTENT_BLOCKS_ADAPTER.validate_python(state.input)
                except ValidationError:
                    user_content = content_blocks(json.dumps(state.input))
            else:
                user_content = content_blocks(json.dumps(state.input))
            initial_entries.append(
                MessageEntry(
                    payload=MessageEntryPayload(role="user", content=user_content),
                )
            )
        if not initial_entries:
            return (state, [])
        new_state = state.model_copy(update={"history": initial_entries})
        return (new_state, list(diff(state, new_state)))

    def _register_mcp_tools(self, state: TaskState) -> None:
        """Fold MCP tools discovered in history into the resolvable tables."""
        for mcp_tool_visible_name, mcp_config in mcp_tool_configs_from_history(
            state.history, self._mcp_configs
        ).items():
            if (
                mcp_tool_visible_name in self._tasks
                or mcp_tool_visible_name in self._callback_implems
                or mcp_tool_visible_name in self._callback_schemas
            ):
                logger.warning("mcp.tool.name_collision", visible_name=mcp_tool_visible_name)
                continue

            self._all_resolvable[mcp_tool_visible_name] = task_from_config(mcp_config)
            self._tools_serialized[mcp_tool_visible_name] = {
                "description": mcp_config.description or "",
                "input_schema": mcp_config.input_schema or {},
            }
            self._task_configs[mcp_tool_visible_name] = mcp_config

    def _make_call_llm(
        self,
        state: TaskState,
        *,
        telemetry: _LLMRequestTelemetry | None = None,
        retry_context_overflow: bool = True,
    ) -> CallLLM:
        """Create a fully-populated CallLLM effect."""
        if telemetry is None:
            telemetry = _LLMRequestTelemetry(metadata=_llm_request_metadata(state))
        return CallLLM(
            state=state,
            completion=self._completion,
            tools=self._tools_serialized,
            telemetry=telemetry,
            retry_context_overflow=retry_context_overflow,
        )

    def _should_auto_compact(self, state: TaskState) -> bool:
        """Whether the projected context has grown past the auto-compact threshold."""
        if self._auto_compact_threshold <= 0 or not has_compactable_history(state):
            return False

        latest_sentinel_index = latest_compaction_sentinel_index(state)
        if latest_sentinel_index >= 0 and not any(
            isinstance(entry, MessageEntry) and entry.payload.role == "assistant"
            for entry in state.history[latest_sentinel_index + 1 :]
        ):
            return False

        context_tokens = estimate_context_tokens(state, self._tools_serialized)
        return context_tokens >= self._auto_compact_threshold

    def _next_turn(
        self, state: TaskState, *, telemetry: _LLMRequestTelemetry
    ) -> tuple[TaskState, list[Any]]:
        """Decide the next step: stop on max iterations, compact, or call the LLM."""
        if self._max_iterations_reached(state):
            final = state.model_copy(update={"output": CompletedOutput(value={"response": ""})})
            return (final, [])
        if self._should_auto_compact(state):
            return self.reduce(
                state,
                StartCompaction(
                    preserve_latest_user=True,
                    telemetry=telemetry.preserve_for_post_compaction(),
                ),
            )
        return (state, [self._make_call_llm(state, telemetry=telemetry)])

    def _count_assistant_messages(self, state: TaskState) -> int:
        """Count assistant messages in history (for max_iterations check)."""
        return sum(
            1
            for e in state.history
            if isinstance(e, MessageEntry)
            and e.payload.role == "assistant"
            and e.payload.channel != "thinking"
        )

    def _max_iterations_reached(self, state: TaskState) -> bool:
        """Check if max iterations limit has been reached."""
        return (
            self._max_iterations is not None
            and self._count_assistant_messages(state) >= self._max_iterations
        )

    def reduce(self, state: TaskState, action: Any) -> tuple[TaskState, list[Any]]:
        """Master reducer. Routes to sub-reducers by action type.

        Max iterations check lives here (not in handle_effect) so it works
        identically on both local and workflow paths.

        Returns:
            ``(new_state, effects)``. Transport patches are computed by the
            execution loop, not by reducers.
        """
        match action:
            case Initialize():
                # Inject system prompt + user input if history is empty.
                if not state.history:
                    state, _ = self._inject_initial_messages(state)
                telemetry = _LLMRequestTelemetry(metadata=_llm_request_metadata(state))

                # Check for already initialized MCPs based on their name
                # and config hash (server_key)
                already_initialized: set[tuple[str, str]] = set()
                for entry in state.history:
                    if (
                        not isinstance(entry, StateEntry)
                        or entry.payload.type != MCP_INITIALIZATION_TYPE
                    ):
                        continue
                    content = entry.payload.content
                    if not isinstance(content, dict):
                        continue
                    detail = content.get("detail")
                    mcp_name = content.get("mcp_name")
                    server_key = content.get("mcp_server_key")
                    if (
                        isinstance(detail, dict)
                        and detail.get("status") == "ok"
                        and isinstance(mcp_name, str)
                        and isinstance(server_key, str)
                    ):
                        already_initialized.add((mcp_name, server_key))

                mcp_initializations = [
                    InitializeMcp(mcp_name=name, mcp_config=config)
                    for name, config in self._mcp_configs.items()
                    if (name, config.server_key) not in already_initialized
                ]
                if mcp_initializations:
                    return (
                        state,
                        [
                            *mcp_initializations,
                            Continue(with_action=PrepareLLMTurn(telemetry=telemetry)),
                        ],
                    )
                return self.reduce(state, PrepareLLMTurn(telemetry=telemetry))

            case McpInitialized(entry=entry):
                if entry:
                    state = state.model_copy(update={"history": [*state.history, entry]})
                return (state, [])

            case PrepareLLMTurn(telemetry=telemetry):
                # Derive mcp tools from cached entries, this is safe to replay
                # and will be solved by a proper resource layer.
                self._register_mcp_tools(state)
                return self._next_turn(state, telemetry=telemetry)

            case ContextOverflowed(can_retry=True, telemetry=telemetry):
                return self.reduce(
                    state,
                    StartCompaction(
                        preserve_latest_user=False,
                        telemetry=telemetry.preserve_for_post_compaction(),
                    ),
                )

            case ContextOverflowed(can_retry=False):
                final = state.model_copy(
                    update={
                        "output": FailedOutput(
                            error="LLM request still exceeds context limit after compaction"
                        )
                    }
                )
                return (final, [])

            case StartCompaction(
                preserve_latest_user=preserve_latest_user,
                telemetry=telemetry,
            ):
                history = state.history
                anchor = _latest_user_message_index(state) if preserve_latest_user else len(history)
                running = make_compaction_entry(
                    "running",
                    threshold=self._auto_compact_threshold,
                    old_context_tokens=estimate_context_tokens(state, self._tools_serialized),
                )
                running_state = state.model_copy(
                    update={"history": [*history[:anchor], running, *history[anchor:]]}
                )
                return (
                    running_state,
                    [
                        CallCompactionLLM(
                            state=running_state,
                            completion=self._completion,
                            tools=self._tools_serialized,
                            threshold=self._auto_compact_threshold,
                            telemetry=telemetry.model_copy(
                                update={
                                    "metadata": _llm_request_metadata(
                                        state, call_type="secondary_call"
                                    )
                                }
                            ),
                            preserve_latest_user=preserve_latest_user,
                            compaction_prompt=self._compaction_prompt,
                        )
                    ],
                )

            case CompactionStatusUpdated(
                entry=entry,
                error=error,
                retry_context_overflow=retry,
                telemetry=telemetry,
            ):
                idx = latest_compaction_sentinel_index(state)
                committed = state.model_copy(
                    update={"history": [*state.history[:idx], entry, *state.history[idx + 1 :]]}
                )

                if error is not None:
                    return (committed.model_copy(update={"output": FailedOutput(error=error)}), [])
                return (
                    committed,
                    [
                        self._make_call_llm(
                            committed,
                            telemetry=_LLMRequestTelemetry(
                                metadata=telemetry.post_compaction_metadata
                            ),
                            retry_context_overflow=retry,
                        )
                    ],
                )

            case LLMTurnComplete(
                response=response,
                tool_calls=tool_calls,
                usage=usage,
            ):
                all_effects: list[Any] = []
                if usage is not None and response:
                    response = list(response)
                    for index, entry in enumerate(response):
                        if entry.payload.channel != "thinking":
                            response[index] = _response_with_usage_annotation(
                                entry,
                                usage,
                                provider=self._provider_name,
                                model=self._model_name,
                            )
                            break
                    else:
                        response[0] = _response_with_usage_annotation(
                            response[0],
                            usage,
                            provider=self._provider_name,
                            model=self._model_name,
                        )

                visible_response = None
                for entry in response:
                    if entry.payload.channel != "thinking":
                        visible_response = entry
                        break

                if response:
                    current_state = state.model_copy(
                        update={"history": [*state.history, *response]}
                    )

                    if not tool_calls:
                        content = (
                            "".join(
                                block.text
                                for block in visible_response.payload.content
                                if isinstance(block, TextContentBlock)
                            )
                            if visible_response
                            else ""
                        )
                        final = current_state.model_copy(
                            update={"output": CompletedOutput(value={"response": content})}
                        )
                        return (final, all_effects)
                else:
                    current_state = state
                    if not tool_calls:
                        return (current_state, all_effects)

                for tc in tool_calls:
                    current_state, effects = sub_task_reducer(
                        current_state,
                        SubTaskCallRequest(call=tc),
                        self._all_resolvable,
                        callback_schemas=self._callback_schemas,
                    )
                    all_effects.extend(effects)

                # Set parent state and task_config on all SpawnSubTask effects.
                # Parent state is the final state (after all call/result entries
                # are appended) to ensure concurrent handlers reroute to
                # non-overlapping paths. task_config enables reconstruction on
                # the activity path.
                for i, effect in enumerate(all_effects):
                    if isinstance(effect, SpawnSubTask):
                        updates: dict[str, Any] = {"state": current_state}
                        task_name = effect.call.payload.name
                        if task_name in self._task_configs:
                            updates["task_config"] = self._task_configs[task_name]
                        all_effects[i] = effect.model_copy(update=updates)

                return (current_state, all_effects)

            case SubTaskCompleted(call_id=call_id, final_state=final_state):
                new_state = _update_result_entry(state, call_id, final_state) or state

                # Check if all pending tool calls are resolved
                all_resolved = not any(
                    isinstance(e, TaskResultEntry) and e.generation_status == "generating"
                    for e in new_state.history
                )
                continuation_effects: list[Any] = []
                if all_resolved:
                    new_state, continuation_effects = self.reduce(
                        new_state,
                        PrepareLLMTurn(
                            telemetry=_LLMRequestTelemetry(
                                metadata=_llm_request_metadata(
                                    new_state, call_type="secondary_call"
                                )
                            )
                        ),
                    )
                return (new_state, continuation_effects)

            case CallbackResultReceived():
                new_state, sub_effects = sub_task_reducer(
                    state, action, self._all_resolvable, callback_schemas=self._callback_schemas
                )
                # Check if all pending tool calls are resolved
                all_resolved = not any(
                    isinstance(e, TaskResultEntry) and e.generation_status == "generating"
                    for e in new_state.history
                )
                cb_effects: list[Any] = list(sub_effects)
                if all_resolved:
                    new_state, continuation_effects = self.reduce(
                        new_state,
                        PrepareLLMTurn(
                            telemetry=_LLMRequestTelemetry(
                                metadata=_llm_request_metadata(
                                    new_state, call_type="secondary_call"
                                )
                            )
                        ),
                    )
                    cb_effects.extend(continuation_effects)
                return (new_state, cb_effects)

            case SubTaskCallRequest():
                return sub_task_reducer(
                    state, action, self._all_resolvable, callback_schemas=self._callback_schemas
                )

            case _:
                return (state, [])

    def _get_callback_bridge(self) -> CallbackBridge | None:
        """Build a LocalCallbackBridge if downstream and loop are available."""
        if self._downstream is not None and self._exec_loop is not None:
            return LocalCallbackBridge(self._downstream, self._exec_loop)
        return None

    async def handle_effect(self, effect: Any, sink: StateSink) -> list[Any]:
        """Effect handler for ExecutionLoop path.

        Dispatches to standalone handler functions via the effect_handlers
        registry. Injects module-level context (resolvable_tasks,
        callback_bridge) as additional kwargs where needed.

        CallCallback is a signal effect (DL-50) and is NOT in the registry.
        It is handled as an explicit fallback using the CallbackBridge.
        """
        handler = self.effect_handlers.get(type(effect))
        if handler is None:
            # Fallback for effects not in the registry (e.g. CallCallback)
            if isinstance(effect, CallCallback):
                return await _handle_call_callback(
                    effect=effect,
                    callback_bridge=self._get_callback_bridge(),
                )
            return []

        if isinstance(effect, SpawnSubTask):
            spawn_result: list[Any] = await handler(
                effect,
                sink,
                resolvable_tasks=self._all_resolvable,
                callback_schemas=self._callback_schemas,
                callback_bridge=self._get_callback_bridge(),
            )
            return spawn_result

        handler_result: list[Any] = await handler(effect, sink)
        return handler_result


# ---------------------------------------------------------------------------
# AgentTask — the LLM-driven task (inherits from ModuleTask)
# ---------------------------------------------------------------------------


class AgentTask(ModuleTask[AgentTaskConfig]):
    """LLM-driven task backed by AgentModule.

    The most common task pattern. Given a serializable completion config
    and a set of task implementations (subtasks the agent can call), it
    drives a conversation loop:

        call LLM -> execute tool calls -> call LLM again -> ...

    until the task completes (LLM returns without tool calls and output is
    set to CompletedOutput) or max_iterations is reached.

    Inherits execute(), run(), and card metadata from ModuleTask.
    Implements create_module() and from_config().
    """

    def __init__(
        self,
        completion: CompletionConfig | dict[str, Any] | None = None,
        tasks: dict[str, Any] | None = None,
        direct_callbacks: list[TaskCallback] | None = None,
        callback_implems: dict[str, Any] | None = None,
        system_prompt: str | None = None,
        max_iterations: int | None = None,
        auto_compact_threshold: int = 0,
        compaction_prompt: str | None = None,
        name: str = "",
        description: str = "",
        input_schema: dict[str, Any] | None = None,
        output_schema: dict[str, Any] | None = None,
        task_configs: dict[str, TaskConfigBase] | None = None,
        mcp_configs: dict[str, McpConfigBase] | None = None,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
        )

        if completion is None:
            completion = MistralCompletionConfig()
        self.completion = completion_config_from_obj(completion)
        self.provider_name = self.completion.type
        self.tasks = tasks or {}
        self._direct_callbacks = direct_callbacks or []
        self._callback_implems = callback_implems or {}
        self._task_configs = task_configs or {}
        self._mcp_configs = mcp_configs or {}
        self.system_prompt = system_prompt
        self.max_iterations = max_iterations
        self.auto_compact_threshold = auto_compact_threshold
        self.compaction_prompt = compaction_prompt
        self.model_name = self.completion.model

        # Fail fast: callback_implems must not themselves require callbacks.
        # Nested callbacks are not supported — the resolver only consumes
        # TaskStateUpdateEvent, so any CallbackCallEvent from an impl would hang.
        for impl_name, impl_task in self._callback_implems.items():
            impl_cbs: list[Any] = getattr(impl_task, "callbacks", [])
            if impl_cbs:
                cb_names = [cb.card.name for cb in impl_cbs]
                msg = (
                    f"Callback implementation '{impl_name}' declares unresolved "
                    f"callbacks {cb_names}. Nested callbacks are not supported — "
                    f"the implementation would hang waiting for a resolver."
                )
                raise ValueError(msg)

        # Auto-compute self.callbacks:
        # (children's unresolved callbacks) + (direct_callbacks) - (callback_implems keys)
        children_unresolved: dict[str, TaskCallback] = {}
        for task in self.tasks.values():
            for cb in getattr(task, "callbacks", []):
                if cb.card.name not in self._callback_implems:
                    children_unresolved[cb.card.name] = cb
        all_cbs = {**children_unresolved}
        for cb in self._direct_callbacks:
            all_cbs[cb.card.name] = cb  # direct wins on name collision
        self.callbacks: list[TaskCallback] = list(all_cbs.values())

        # Callback resolution: names this task can resolve locally
        self._resolvable_names = frozenset(self.tasks.keys()) | frozenset(
            self._callback_implems.keys()
        )

    @classmethod
    def from_config(cls, config: Any, **kwargs: Any) -> "AgentTask":
        """Construct from config.

        Accepts an AgentTaskConfig (or dict). Reconstructs live task objects
        from TaskConfig and stores serializable completion config.

        Nested children are reconstructed via ``default_registry`` — the
        worker process must install matching extensions globally.
        """
        from mistralai.vibe.sdk.agent.tasks.runtime import task_from_config

        if not isinstance(config, AgentTaskConfig):
            config = AgentTaskConfig.model_validate(config)

        tasks = kwargs.get("tasks") or {
            name: task_from_config(cfg) for name, cfg in config.tasks.items()
        }
        cb_implems = {name: task_from_config(cfg) for name, cfg in config.callback_implems.items()}
        return cls(
            completion=config.completion,
            name=config.name,
            description=config.description,
            input_schema=config.input_schema,
            system_prompt=config.system_prompt,
            max_iterations=config.max_iterations,
            auto_compact_threshold=config.auto_compact_threshold,
            compaction_prompt=config.compaction_prompt,
            tasks=tasks,
            callback_implems=cb_implems,
            direct_callbacks=config.direct_callbacks,
            mcp_configs=config.mcps,
            task_configs=config.tasks,
        )

    def create_module(self) -> AgentModule:
        """Create a fully configured AgentModule."""
        callback_schemas = {cb.card.name: cb for cb in self.callbacks}
        return AgentModule(
            completion=self.completion,
            tasks=self.tasks,
            max_iterations=self.max_iterations,
            system_prompt=self.system_prompt,
            callback_implems=self._callback_implems,
            callback_schemas=callback_schemas,
            task_configs=self._task_configs,
            auto_compact_threshold=self.auto_compact_threshold,
            compaction_prompt=self.compaction_prompt,
            mcp_configs=self._mcp_configs,
        )


# ---------------------------------------------------------------------------
# Standalone effect handlers for ExecutionLoop
# ---------------------------------------------------------------------------


@_registry.handles(CallCompactionLLM)
async def _handle_call_compaction_llm(
    effect: CallCompactionLLM,
    sink: StateSink,
) -> list[CompactionStatusUpdated]:
    """Run the summary and stream the sentinel lifecycle so callers see it mid-turn."""
    sentinel_index = latest_compaction_sentinel_index(effect.state)
    scoped_sink = sink.scoped(FixedHistoryScope(index=sentinel_index))
    async with scoped_sink:
        await scoped_sink.update(effect.state)

        outcome = await run_compaction(
            completion_from_config(effect.completion),
            effect.state,
            tools=effect.tools,
            threshold=effect.threshold,
            compaction_prompt=effect.compaction_prompt,
            provider=effect.completion.type,
            model=effect.completion.model,
            request_metadata=effect.telemetry.metadata,
        )

        history = effect.state.history
        finalized_state = effect.state.model_copy(
            update={
                "history": [
                    *history[:sentinel_index],
                    outcome.entry,
                    *history[sentinel_index + 1 :],
                ]
            }
        )
        await scoped_sink.update(finalized_state)

    return [
        CompactionStatusUpdated(
            entry=outcome.entry,
            retry_context_overflow=effect.preserve_latest_user,
            telemetry=effect.telemetry,
            error=outcome.error,
            stream_scope=scoped_sink.scope,
        )
    ]


@_registry.handles(CallLLM)
async def _handle_call_llm(
    effect: CallLLM,
    sink: StateSink,
) -> list[LLMTurnComplete | ContextOverflowed]:
    """Call the LLM, stream state updates via sink, return LLMTurnComplete.

    Streams intermediate state updates (text deltas, assistant entry creation)
    through the StateSink so the consumer sees tokens as they arrive.
    The reducer never sees these streaming events. At the end, returns
    a single LLMTurnComplete action containing the complete assistant
    MessageEntries and extracted tool calls.

    Args:
        effect: CallLLM effect carrying state, completion config, tools.
        sink: StateSink for streaming state updates downstream.

    Returns:
        A list containing one LLMTurnComplete action.
    """
    completion = completion_from_config(effect.completion)
    request = build_completion_request_from_state(
        effect.state,
        effect.tools,
        metadata=effect.telemetry.metadata,
    )
    await emit_completion_request_sent(model=effect.completion.model, request=request)
    latest_usage: TokenUsage | None = None

    current_state = effect.state
    tool_calls: list[TaskCallEntry] = []
    streamed_state = False
    scoped_sink = sink.scoped(AppendHistoryScope(start_index=len(current_state.history)))
    try:
        async with scoped_sink:
            async for new_state, streamed_tool_calls, usage in stream_states(
                current_state,
                completion.complete(request),
            ):
                await scoped_sink.update(new_state)
                streamed_state = True
                current_state = new_state
                if streamed_tool_calls is not None:
                    tool_calls = streamed_tool_calls
                if usage is not None:
                    latest_usage = usage
    except CompletionContextTooLargeError:
        if streamed_state:
            raise
        return [
            ContextOverflowed(
                can_retry=effect.retry_context_overflow,
                telemetry=effect.telemetry,
            )
        ]
    except Exception as exc:
        if is_context_too_large_error(exc) and not streamed_state:
            return [
                ContextOverflowed(
                    can_retry=effect.retry_context_overflow,
                    telemetry=effect.telemetry,
                )
            ]
        raise

    # Extract the assistant messages produced by this turn in streamed order.
    response: list[MessageEntry] = []
    for entry in current_state.history[len(effect.state.history) :]:
        if not isinstance(entry, MessageEntry) or entry.payload.role != "assistant":
            continue
        response.append(entry)

    return [
        LLMTurnComplete(
            response=response,
            tool_calls=tool_calls,
            usage=latest_usage,
            stream_scope=scoped_sink.scope,
        )
    ]


@_registry.handles(Continue)
async def _handle_continue(effect: Continue[AgentAction], sink: StateSink) -> list[AgentAction]:
    """Return the deferred action so the loop drains it next iteration."""
    return [effect.with_action]


@_registry.handles(InitializeMcp)
async def _handle_initialize_mcp(
    effect: InitializeMcp,
    sink: StateSink,
) -> list[McpInitialized]:
    """Initialize one MCP server: open it, discover its tools, then tear it down."""
    try:
        tools = await discover_mcp_tools(effect.mcp_config)

        entry = StateEntry(
            payload=StateEntryPayload(
                type=MCP_INITIALIZATION_TYPE,
                content=McpInitializationContent(
                    mcp_name=effect.mcp_name,
                    mcp_type=effect.mcp_config.type,
                    mcp_server_key=effect.mcp_config.server_key,
                    detail=McpInitOk(status="ok", tools=tools),
                ).model_dump(),
            )
        )
    except Exception as error:
        logger.warning(
            "mcp.initialization.failed",
            mcp_name=effect.mcp_name,
            mcp_type=effect.mcp_config.type,
            error_type=type(error).__name__,
            exc_info=error,
        )
        entry = StateEntry(
            payload=StateEntryPayload(
                type=MCP_INITIALIZATION_TYPE,
                content=McpInitializationContent(
                    mcp_name=effect.mcp_name,
                    mcp_type=effect.mcp_config.type,
                    mcp_server_key=effect.mcp_config.server_key,
                    detail=McpInitError(
                        status="error",
                        error_type=type(error).__name__,
                        error="MCP initialization failed",
                    ),
                ).model_dump(),
            )
        )
    return [McpInitialized(entry=entry)]


@_registry.handles(FailSubTask)
async def _handle_fail_subtask(effect: FailSubTask, sink: StateSink) -> list[SubTaskCompleted]:
    return [SubTaskCompleted(call_id=effect.call_id, final_state=effect.final_state)]


@_registry.handles(SpawnSubTask)
async def _handle_spawn_subtask(
    effect: SpawnSubTask,
    sink: StateSink,
    resolvable_tasks: dict[str, Any] | None = None,
    callback_schemas: dict[str, TaskCallback] | None = None,
    callback_bridge: CallbackBridge | None = None,
) -> list[SubTaskCompleted]:
    """Run a child task, relay patches via sink, return SubTaskCompleted.

    Iterates the child channel, rerouting child patches into the parent scope
    and calling sink.update(parent_state) so the consumer sees child progress
    as part of the parent's state evolution.

    Also handles child callback requests (CallbackCallEvent) via the shared
    resolve_callback_request function. The callback_bridge is used for
    bubbling unresolved callbacks upstream.

    On the local path, the module injects resolvable_tasks, callback_schemas,
    and callback_bridge. On the workflow activity path, resolvable_tasks is
    None and the task is reconstructed from task_config.

    Args:
        effect: SpawnSubTask effect with parent state, call info, and child state.
        sink: StateSink for streaming rerouted parent state updates.
        resolvable_tasks: Tasks that can resolve child callbacks locally.
        callback_schemas: Callback schemas for bubbling upstream.
        callback_bridge: CallbackBridge for bubbling unresolved callbacks.

    Returns:
        A list containing one SubTaskCompleted action with the final child state.
    """
    if resolvable_tasks is None:
        if effect.task_config is None:
            msg = f"No resolvable_tasks and no task_config for {effect.call.payload.name}"
            raise ValueError(msg)
        from mistralai.vibe.sdk.agent.tasks.runtime import task_from_config

        task = task_from_config(effect.task_config)
    else:
        task = resolvable_tasks[effect.call.payload.name]

    async with spawn_child_scope(should_raise=False):
        channel = await task.run(effect.child_state)
        prefix = f"/history/{effect.result_index}/payload/state"
        scoped_sink = sink.scoped(FixedHistoryScope(index=effect.result_index))

        local_tasks = resolvable_tasks or {}
        local_schemas = callback_schemas or {}

        parent_state = effect.state
        child_state = effect.child_state
        async for message in channel:
            if isinstance(message, TaskStateUpdateEvent):
                child_state = apply_patches(child_state, message.payload.patches)
                rerouted = reroute_patches(message.payload.patches, prefix)
                parent_state = apply_patches(parent_state, rerouted)
                await scoped_sink.update(parent_state)

            elif isinstance(message, TaskResultEvent):
                child_state = message.payload.result
            elif isinstance(message, CallbackCallEvent):
                await resolve_callback_request(
                    request=message,
                    child_path_segment=effect.call.payload.id,
                    send_result_to_child=channel.send,
                    task_implementations=local_tasks,
                    callback_schemas=local_schemas,
                    bubble_upstream=callback_bridge,
                )

        return [
            SubTaskCompleted(
                call_id=effect.call.payload.id,
                final_state=child_state,
                stream_scope=scoped_sink.scope,
            )
        ]


async def _handle_call_callback(
    effect: CallCallback,
    callback_bridge: CallbackBridge | None = None,
) -> list[Any]:
    """Emit CallbackCallEvent via CallbackBridge, await result, return action.

    Sends a CallbackCallEvent through the CallbackBridge so the parent can
    resolve the callback. Then waits for a CallbackResultEvent via
    bridge.receive_result(). Returns a CallbackResultReceived action.

    On the local path, callback_bridge is a LocalCallbackBridge.
    On the workflow path, it is a WorkflowCallbackBridge (signal-based).

    Args:
        effect: CallCallback effect with call info.
        callback_bridge: Transport-abstracted bridge for callback exchange.

    Returns:
        A list containing one CallbackResultReceived action.
    """
    if callback_bridge is None:
        msg = "callback_bridge required for callback handling"
        raise RuntimeError(msg)

    call_event = CallbackCallEvent(
        payload=CallbackCallPayload(
            id=effect.call.payload.id,
            name=effect.call.payload.name,
            input=effect.call.payload.input,
            path=[],
        )
    )
    await callback_bridge.send_request(call_event)
    result = await callback_bridge.receive_result(effect.call.payload.id)

    return [
        CallbackResultReceived(
            call_id=effect.call.payload.id,
            result_state=result.payload.state,
        )
    ]
