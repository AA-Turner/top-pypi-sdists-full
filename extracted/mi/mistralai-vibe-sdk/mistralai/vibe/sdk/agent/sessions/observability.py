import time
from dataclasses import dataclass, field
from typing import Literal

import structlog
from pydantic import BaseModel

from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTaskConfig
from mistralai.vibe.sdk.agent.telemetry_events import (
    EVENT_CONTEXT_KEYS,
    NEW_SESSION_EVENT,
    TOOL_CALL_FINISHED_EVENT,
)
from mistralai.vibe.sdk.capabilities.adapters.local_function import ToolTaskConfig
from mistralai.vibe.sdk.capabilities.file_tool_telemetry import builtin_file_metrics
from mistralai.vibe.sdk.execution_record.state import (
    CompletedOutput,
    HistoryEntry,
    TaskCallEntry,
    TaskResultEntry,
    TaskState,
)
from mistralai.vibe.sdk.observability import attributes_from_context
from mistralai.vibe.sdk.observability.datalake import ERROR_EVENT, atrack, track
from mistralai.vibe.sdk.transports.events import CallbackResultEvent, UpstreamMessage

logger = structlog.get_logger()

RunMode = Literal["stream", "completion"]
ToolCallStatus = Literal["success", "failure", "skipped", "running"]
ToolCompletionSource = Literal["client_tool_callback", "builtin_tool", "custom_tool"]

TOOL_STATUS_TELEMETRY_MAP: dict[str, ToolCallStatus] = {
    "completed": "success",
    "failed": "failure",
    "canceled": "skipped",
    "running": "running",
}
_BUILTIN_TOOL_FN_PATH_PREFIXES = (
    # Preserve builtin classification for execution records serialized before 0.6.0.
    "mistralai.vibe.sdk.tools.builtins.",
    "mistralai.vibe.sdk.capabilities.builtins.",
)


class ToolCallFinishedProperties(BaseModel):
    tool_name: str | None
    status: str
    decision: None = None
    approval_type: None = None
    agent_profile_name: str
    message_id: str | None
    tool_duration_ms: int | None
    tool_completion_source: ToolCompletionSource


@dataclass
class ToolCallTelemetryState:
    """Mutable per-session bookkeeping used to emit each tool-call event once."""

    started_at: dict[str, float] = field(default_factory=dict)
    emitted_result_ids: set[str] = field(default_factory=set)

    def record_started(self, call_id: str) -> None:
        self.started_at[call_id] = time.monotonic()

    def record_existing_results(
        self, history: list[HistoryEntry], task_config: AgentTaskConfig
    ) -> None:
        tool_calls = _tool_calls_from_history(history, task_config)
        for entry in history:
            if not isinstance(entry, TaskResultEntry):
                continue
            if entry.generation_status != "complete" or not entry.payload.id:
                continue
            if entry.payload.id not in tool_calls:
                continue

            self.emitted_result_ids.add(entry.payload.id)

    def ensure_started(self, call_id: str) -> None:
        self.started_at.setdefault(call_id, time.monotonic())

    def duration_ms_for(self, call_id: str) -> int | None:
        started_at = self.started_at.pop(call_id, None)
        return None if started_at is None else int((time.monotonic() - started_at) * 1000)

    def record_emitted(self, call_id: str) -> None:
        self.emitted_result_ids.add(call_id)

    def was_emitted(self, call_id: str) -> bool:
        return call_id in self.emitted_result_ids


def emit_session_created() -> None:
    track(
        NEW_SESSION_EVENT,
        properties=attributes_from_context(*EVENT_CONTEXT_KEYS[NEW_SESSION_EVENT]),
    )


async def emit_callback_tool_call_finished(
    *,
    message: UpstreamMessage,
    tool_calls: ToolCallTelemetryState,
) -> None:
    if not isinstance(message, CallbackResultEvent):
        return

    try:
        payload = message.payload
        raw_status = payload.state.output.status
        tool_duration_ms = tool_calls.duration_ms_for(payload.id)
        context = attributes_from_context(*EVENT_CONTEXT_KEYS[TOOL_CALL_FINISHED_EVENT])
        properties = (
            ToolCallFinishedProperties(
                tool_name=payload.name or None,
                status=TOOL_STATUS_TELEMETRY_MAP.get(raw_status, f"unknown:{raw_status}"),
                agent_profile_name=str(context["agent_name"]),
                message_id=str(context["task_id"]) if "task_id" in context else None,
                tool_duration_ms=tool_duration_ms,
                tool_completion_source="client_tool_callback",
            ).model_dump(mode="json", exclude_none=True)
            | context
        )
    except Exception:
        logger.warning(
            ERROR_EVENT,
            telemetry_event=TOOL_CALL_FINISHED_EVENT,
            exc_info=True,
        )
        return

    await atrack(TOOL_CALL_FINISHED_EVENT, properties=properties)


async def emit_history_tool_calls_finished(
    *,
    task_state: TaskState,
    task_config: AgentTaskConfig,
    tool_calls: ToolCallTelemetryState,
) -> None:
    tool_calls_by_id = _tool_calls_from_history(task_state.history, task_config)
    for call_id in tool_calls_by_id:
        if not tool_calls.was_emitted(call_id):
            tool_calls.ensure_started(call_id)

    for entry in task_state.history:
        try:
            if not isinstance(entry, TaskResultEntry):
                continue
            if entry.generation_status != "complete":
                continue
            if not entry.payload.id or tool_calls.was_emitted(entry.payload.id):
                continue
            tool_call = tool_calls_by_id.get(entry.payload.id)
            if tool_call is None or entry.payload.state is None:
                continue

            raw_status = entry.payload.state.output.status
            if raw_status == "running":
                continue

            call, tool_task_config = tool_call
            tool_duration_ms = tool_calls.duration_ms_for(entry.payload.id)
            tool_completion_source: ToolCompletionSource = (
                "builtin_tool"
                if tool_task_config.fn_path.startswith(_BUILTIN_TOOL_FN_PATH_PREFIXES)
                else "custom_tool"
            )
            file_metrics = (
                builtin_file_metrics(
                    tool_name=entry.payload.name or call.payload.name or None,
                    output=entry.payload.state.output,
                )
                if tool_completion_source == "builtin_tool"
                and isinstance(entry.payload.state.output, CompletedOutput)
                else {}
            )
            context = attributes_from_context(*EVENT_CONTEXT_KEYS[TOOL_CALL_FINISHED_EVENT])
            properties = (
                ToolCallFinishedProperties(
                    tool_name=entry.payload.name or call.payload.name or None,
                    status=TOOL_STATUS_TELEMETRY_MAP.get(raw_status, f"unknown:{raw_status}"),
                    agent_profile_name=str(context["agent_name"]),
                    message_id=str(context["task_id"]) if "task_id" in context else None,
                    tool_duration_ms=tool_duration_ms,
                    tool_completion_source=tool_completion_source,
                ).model_dump(mode="json", exclude_none=True)
                | file_metrics
                | context
            )
        except Exception:
            logger.warning(
                ERROR_EVENT,
                telemetry_event=TOOL_CALL_FINISHED_EVENT,
                exc_info=True,
            )
            return

        await atrack(TOOL_CALL_FINISHED_EVENT, properties=properties)
        tool_calls.record_emitted(entry.payload.id)


def _tool_calls_from_history(
    history: list[HistoryEntry],
    task_config: AgentTaskConfig,
) -> dict[str, tuple[TaskCallEntry, ToolTaskConfig]]:
    tool_calls: dict[str, tuple[TaskCallEntry, ToolTaskConfig]] = {}
    for entry in history:
        if not isinstance(entry, TaskCallEntry):
            continue
        if entry.payload.type != "child_task" or not entry.payload.id:
            continue

        child_task_config = task_config.tasks.get(entry.payload.name)
        if not isinstance(child_task_config, ToolTaskConfig):
            continue

        tool_calls[entry.payload.id] = (entry, child_task_config)
    return tool_calls
