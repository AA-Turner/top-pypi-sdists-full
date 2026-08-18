"""AsyncSession — default async session implementation."""

import asyncio
import time
from collections.abc import AsyncGenerator, Callable, Sequence
from contextlib import asynccontextmanager
from types import TracebackType
from typing import cast

import structlog
from pydantic import JsonValue

import mistralai.vibe.sdk.agent.sessions.observability as session_observability
from mistralai.vibe.sdk.agent.config import AgentConfig
from mistralai.vibe.sdk.agent.execution.resources import (
    ResourcesScope,
    bind_execution_scope,
    stop_execution_scope,
)
from mistralai.vibe.sdk.agent.sessions.helpers import IdFactory, default_id_factory
from mistralai.vibe.sdk.agent.sessions.observability import RunMode
from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTaskConfig
from mistralai.vibe.sdk.agent.tasks.helpers import AgentTaskFactory
from mistralai.vibe.sdk.capabilities.builtins.skill_tool import configured_skill_count
from mistralai.vibe.sdk.capabilities.registry import ClientToolRegistry
from mistralai.vibe.sdk.execution_record.patching.json_patch import apply_patches
from mistralai.vibe.sdk.execution_record.state import (
    ContentBlock,
    HistoryEntry,
    MessageEntry,
    MessageEntryPayload,
    PendingOutput,
    TaskResultEntry,
    TaskState,
    content_blocks,
)
from mistralai.vibe.sdk.observability import (
    SESSION_OBSERVABILITY_ATTRIBUTE_KEYS,
    SPAN_CONTEXT_KEYS,
    ObservabilityAttributes,
    attributes_from_context,
    observability_context,
    otel,
    upsert_in_context,
    validate_observability_attributes,
)
from mistralai.vibe.sdk.transports.channel import Channel
from mistralai.vibe.sdk.transports.events import (
    CallbackCallEvent,
    DownstreamMessage,
    TaskResultEvent,
    TaskStateUpdateEvent,
    UpstreamMessage,
)

logger = structlog.get_logger()


class AsyncSession:
    """Default async Session implementation backed by an agent task factory.

    Owns the conversation history for a single session. Each call to
    run() builds a TaskState from accumulated history, delegates to
    the underlying Task, and updates history from the result.

    Not safe for concurrent run() calls on the same session instance.
    """

    def __init__(
        self,
        *,
        task_config: AgentTaskConfig,
        agent_task_factory: AgentTaskFactory,
        history: Sequence[HistoryEntry] | None = None,
        id_factory: IdFactory | None = None,
        client_tool_registry: ClientToolRegistry | None = None,
        conversation_id: str | None = None,
        observability_attributes: ObservabilityAttributes | None = None,
    ) -> None:
        self._task_config = task_config.model_copy(deep=True)
        self._agent_task_factory = agent_task_factory
        self._task = self._agent_task_factory(self._task_config)
        self._history: list[HistoryEntry] = list(history) if history else []
        self._id_factory = id_factory or default_id_factory
        self._session_id = self._id_factory()
        self._conversation_id = conversation_id
        self._observability_attributes = validate_observability_attributes(observability_attributes)
        self._client_tool_registry = client_tool_registry or ClientToolRegistry()
        self._channel: Channel | None = None
        self._resources_scope = ResourcesScope()
        self._closed = False
        self._run_in_progress = False
        self._task_config_stale = False
        self._tool_calls = session_observability.ToolCallTelemetryState()
        with observability_context(**self._session_context_bindings()):
            session_observability.emit_session_created()

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def conversation_id(self) -> str | None:
        return self._conversation_id

    @property
    def history(self) -> list[HistoryEntry]:
        return list(self._history)

    def _build_state(self, prompt: str | list[ContentBlock]) -> TaskState:
        """Build TaskState for the next turn from current history + new prompt."""
        task_id = self._id_factory()

        if not self._history:
            return TaskState(id=task_id, input=prompt)

        history: list[HistoryEntry] = list(self._history)

        if self._task_config_stale:
            history = self._reconcile_history_with_task_config(history)

        # Skip the user-message append when resuming mid-turn after a tool result (empty prompt
        # from a continue-as-new resume): the LLM expects [tool_call, tool_result] directly,
        # not an empty user message injected before the next assistant turn. Reconcile can empty a
        # single-system-message history, so guard history[-1] to keep the original append behavior.
        has_pending_user_message = (
            bool(history)
            and isinstance(history[-1], MessageEntry)
            and history[-1].payload.role == "user"
            and not prompt
        )
        should_append_user_message = (
            prompt or not history or not isinstance(history[-1], TaskResultEntry)
        )
        if not has_pending_user_message and should_append_user_message:
            history.append(
                MessageEntry(
                    payload=MessageEntryPayload(role="user", content=content_blocks(prompt))
                )
            )
        return TaskState(id=task_id, input=prompt, history=history)

    def _reconcile_history_with_task_config(
        self, history: list[HistoryEntry]
    ) -> list[HistoryEntry]:
        """Return history with the leading system message matching current task config."""
        if not history:
            return history

        system_prompt = self._task_config.system_prompt or None
        has_system_message = (
            isinstance(history[0], MessageEntry) and history[0].payload.role == "system"
        )
        if has_system_message and system_prompt is None:
            return history[1:]
        if has_system_message and system_prompt is not None:
            return [
                MessageEntry(
                    payload=MessageEntryPayload(
                        role="system", content=content_blocks(system_prompt)
                    )
                ),
                *history[1:],
            ]
        if system_prompt is not None:
            return [
                MessageEntry(
                    payload=MessageEntryPayload(
                        role="system", content=content_blocks(system_prompt)
                    )
                ),
                *history,
            ]

        return history

    async def run(
        self,
        prompt: str | list[ContentBlock],
    ) -> AsyncGenerator[DownstreamMessage, None]:
        """Stream protocol task-progress events for a single turn."""
        self._check_closed()
        if self._run_in_progress:
            raise RuntimeError("Session run already in progress")

        self._run_in_progress = True
        try:
            prior_history = list(self._history)
            self._tool_calls.record_existing_results(prior_history, self._task_config)
            state = self._build_state(prompt)
            async with self._run_telemetry(mode="stream", current_state=lambda: state):
                async for message, next_state in self._run_task(state):
                    state = next_state
                    yield message
        finally:
            self._run_in_progress = False

    async def send_message(self, message: UpstreamMessage) -> None:
        """Send an upstream message to the active run."""
        self._check_closed()
        if self._channel is None:
            raise RuntimeError("No active session run")
        await self._channel.send(message)
        with observability_context(**self._session_context_bindings()):
            await session_observability.emit_callback_tool_call_finished(
                message=message,
                tool_calls=self._tool_calls,
            )

    async def run_to_completion(self, prompt: str | list[ContentBlock]) -> TaskState:
        """Run a single turn and return the final state."""
        self._check_closed()
        if self._run_in_progress:
            raise RuntimeError("Session run already in progress")

        self._run_in_progress = True
        try:
            prior_history = list(self._history)
            self._tool_calls.record_existing_results(prior_history, self._task_config)
            state = self._build_state(prompt)
            async with self._run_telemetry(mode="completion", current_state=lambda: state):
                async for message, next_state in self._run_task(state):
                    if isinstance(message, CallbackCallEvent):
                        raise RuntimeError(
                            "Task requested a callback; use run() and"
                            " send_message() to resolve callbacks"
                        )
                    state = next_state

            return state
        finally:
            self._run_in_progress = False

    def fork(self, *, conversation_id: str | None = None) -> "AsyncSession":
        """Create a new session branching from the current history."""
        self._check_closed()
        history = list(self._history)
        if self._task_config_stale:
            history = self._reconcile_history_with_task_config(history)

        return AsyncSession(
            task_config=self._task_config,
            agent_task_factory=self._agent_task_factory,
            history=history,
            id_factory=self._id_factory,
            client_tool_registry=self._client_tool_registry,
            conversation_id=conversation_id,
            observability_attributes=self._observability_attributes,
        )

    async def close(self) -> None:
        """Release resources held by the session."""
        if self._closed:
            return
        self._closed = True

        channel = self._channel
        self._channel = None
        if channel is not None:
            try:
                await channel.close()
            except Exception:
                logger.warning(
                    "session.async.close.channel_close_failed",
                    session_id=self.session_id,
                    exc_info=True,
                )

        try:
            await self._resources_scope.aclose()
        except Exception:
            logger.warning(
                "session.async.close.scope_finalize_failed",
                session_id=self.session_id,
                exc_info=True,
            )

    def set_config(self, config: AgentConfig) -> None:
        """Replace the SDK config used for future turns in this session."""
        self._check_closed()
        if self._run_in_progress:
            raise RuntimeError("Cannot update config while a run is in progress")

        task_config = config.to_task_config().model_copy(deep=True)
        task = self._agent_task_factory(task_config)
        client_tool_registry = config.client_tool_registry()

        self._task_config = task_config
        self._task = task
        self._client_tool_registry = client_tool_registry
        self._task_config_stale = True

    async def _run_task(
        self, state: TaskState
    ) -> AsyncGenerator[tuple[DownstreamMessage, TaskState], None]:
        """Run a task state through the underlying channel and track state updates."""
        await self._reset_resources_if_config_stale()

        with bind_execution_scope(self._resources_scope):
            channel = await self._task.run(state)

            # Preventing a race condition where the channel is already closed.
            if self._closed:
                await channel.close()
                return

            self._channel = channel

            try:
                async for message in channel:
                    if isinstance(message, TaskStateUpdateEvent):
                        state = apply_patches(state, message.payload.patches)
                        self._store_history(state)
                        await session_observability.emit_history_tool_calls_finished(
                            task_state=state,
                            task_config=self._task_config,
                            tool_calls=self._tool_calls,
                        )
                        with stop_execution_scope():
                            yield message, state
                        continue

                    if isinstance(message, TaskResultEvent):
                        state = message.payload.result
                        self._store_history(state)
                        await session_observability.emit_history_tool_calls_finished(
                            task_state=state,
                            task_config=self._task_config,
                            tool_calls=self._tool_calls,
                        )
                        with stop_execution_scope():
                            yield message, state
                        continue

                    if isinstance(message, CallbackCallEvent):
                        self._tool_calls.record_started(message.payload.id)
                        if self._client_tool_registry.can_handle(message):
                            with stop_execution_scope():
                                await self._client_tool_registry.handle_event(self, message)
                            continue

                        with stop_execution_scope():
                            yield message, state
                        continue

                    logger.warning(
                        "session.async.unknown_downstream_message",
                        message_type=type(message).__name__,
                        session_id=self.session_id,
                        task_id=state.id,
                    )
                    with stop_execution_scope():
                        yield cast(DownstreamMessage, message), state
            finally:
                self._channel = None
                await channel.close()

    async def _reset_resources_if_config_stale(self) -> None:
        """Finalize and replace the session scope after a config change."""
        if not self._task_config_stale:
            return

        old = self._resources_scope
        try:
            self._resources_scope = ResourcesScope()

            await old.aclose()
        except Exception:
            logger.warning(
                "session.async.resource_scope_reset_failed",
                session_id=self.session_id,
                exc_info=True,
            )

    @asynccontextmanager
    async def _run_telemetry(
        self,
        *,
        mode: RunMode,
        current_state: Callable[[], TaskState],
    ) -> AsyncGenerator[None, None]:
        state = current_state()
        started_at = time.monotonic()
        with (
            observability_context(
                **self._session_context_bindings(),
                task_id=state.id,
                run_mode=mode,
                status="running",
                history_length=len(state.history),
            ),
            otel.start_span(
                f"invoke_agent {self._task_config.name}",
                self._span_attributes_from_context(),
            ) as span,
        ):
            try:
                yield

                state = current_state()
                if mode == "completion" and isinstance(state.output, PendingOutput):
                    raise RuntimeError("Task produced no terminal task result")
                upsert_in_context(status=state.output.status)
            except asyncio.CancelledError:
                upsert_in_context(status="canceled")
                raise
            except Exception:
                upsert_in_context(status="failed")
                raise
            finally:
                state = current_state()
                upsert_in_context(history_length=len(state.history))
                span.set_attributes(otel.otel_attributes(self._span_attributes_from_context()))
                self._log_run_completed(
                    duration_ms=int((time.monotonic() - started_at) * 1000),
                )

    def _session_context_bindings(self) -> dict[str, JsonValue]:
        return {
            "entrypoint": "unknown",
            **self._observability_attributes,
            **attributes_from_context(*SESSION_OBSERVABILITY_ATTRIBUTE_KEYS),
            "nb_skills": configured_skill_count(self._task_config.tasks),
            "nb_mcp_servers": len(self._task_config.mcps),
            "session_id": self._session_id,
            "conversation_id": self._conversation_id,
            "agent_name": self._task_config.name,
            "model": self._task_config.completion.model,
            "provider": self._task_config.completion.type,
        }

    def _span_attributes_from_context(self) -> dict[str, object]:
        run_attributes = attributes_from_context(*SPAN_CONTEXT_KEYS)
        attributes: dict[str, object] = {
            **run_attributes,
            "gen_ai.operation.name": "invoke_agent",
        }
        if agent_name := run_attributes.get("agent_name"):
            attributes["gen_ai.agent.name"] = agent_name
        if model := run_attributes.get("model"):
            attributes["gen_ai.request.model"] = model
        if provider := run_attributes.get("provider"):
            attributes["gen_ai.provider.name"] = provider
        if conversation_id := run_attributes.get("conversation_id"):
            attributes["gen_ai.conversation.id"] = conversation_id
        return attributes

    def _log_run_completed(self, *, duration_ms: int) -> None:
        context = attributes_from_context(
            "agent_name",
            "run_mode",
            "model",
            "provider",
            "session_id",
            "conversation_id",
            "task_id",
            "status",
        )
        status = context.get("status")
        if status is None:
            return

        span = otel.current_span()
        if not span.is_recording() and status not in {"canceled", "failed"}:
            return

        log = logger.warning if status in {"canceled", "failed"} else logger.info
        log(
            "vibe_sdk.run.completed",
            **context,
            duration_ms=duration_ms,
        )

    def _store_history(self, state: TaskState) -> None:
        self._history = list(state.history)
        self._task_config_stale = False

    def _check_closed(self) -> None:
        if self._closed:
            raise RuntimeError("Session is closed")

    async def __aenter__(self) -> "AsyncSession":
        self._check_closed()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()
