"""Project Harness Session history and status onto Vibe Agents event documents."""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import ClassVar

from pydantic import TypeAdapter

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.runtime.hosts.workflows import session_events as workflow_events
from mistralai.vibe.harness.runtime.session.events import state as runtime_event_state
from mistralai.vibe_agents import session_workflow as session_wire
from mistralai.vibe_agents.sdk.transport import annotation_keys
from mistralai.vibe_agents.session_workflow.notice_projection import (
    notice_to_legacy_task_protocol_payload,
)

_JSON_OBJECT_ADAPTER: TypeAdapter[session_wire.JsonObject] = TypeAdapter(session_wire.JsonObject)
# Harness error messages can carry provider or exception text, which a failed Turn must not expose.
_TURN_FAILED_MESSAGE = "The turn failed."


@dataclass(frozen=True, slots=True)
class _WaitingStatus:
    reason: str = "waiting_for_input"
    termination: session_wire.FailedTurnTermination | None = None


class LegacyTaskSessionEventPublisher(workflow_events.WorkflowSessionEventPublisher):
    """Publish legacy history and status rows from canonical Harness events."""

    publisher_type: ClassVar[str] = "agents_sdk_legacy_task_protocol"
    workflow_task_type: ClassVar[str] = session_wire.SESSION_EVENT_TASK_TYPE

    def __init__(
        self,
        batches: list[runtime_event_state.SessionEventBatch] | None = None,
        *,
        lifecycle_emitter: workflow_events.WorkflowTaskLifecycleEmitter | None = None,
    ) -> None:
        self._product_lifecycle_emitter = lifecycle_emitter or workflow_events.emit_workflow_task_lifecycle
        super().__init__(lifecycle_emitter=self._emit_lifecycle_with_status_sidecar)
        self._batches = batches
        self._status_reasons: dict[str, _WaitingStatus] = {}

    async def publish(self, batch: runtime_event_state.SessionEventBatch) -> None:
        self.record_batch(batch)
        await super().publish(batch)

    def record_batch(self, batch: runtime_event_state.SessionEventBatch) -> None:
        if self._batches is not None:
            self._batches.append(batch.model_copy(deep=True))
        self._status_reasons.update(_status_reasons_for_batch(batch))

    def project_history_entry(
        self,
        entry: harness_session.HistoryEntry,
    ) -> workflow_events.WorkflowTaskProjection | None:
        if _is_command_user_message(entry) or _is_empty_assistant_message(entry):
            return None
        if isinstance(
            entry,
            harness_session.CapabilityContextMessageHistoryEntry | harness_session.InputContextMessageHistoryEntry,
        ):
            # The task protocol has no context message; a capability's notice is published
            # as an alert.
            return None
        return workflow_events.WorkflowTaskProjection(state=_history_entry_state(entry))

    def project_session_event(
        self,
        event: harness_session.SessionEvent,
        *,
        task_id: str,
    ) -> workflow_events.WorkflowTaskProjection | None:
        if not isinstance(event, harness_session.SessionUpdatedEvent):
            return None
        if event.session.status == "running":
            content: session_wire.JsonObject = {"status": "running"}
        elif event.session.status == "waiting":
            waiting = self._status_reasons.pop(task_id, _WaitingStatus())
            content = {"status": "waiting_for_input", "reason": waiting.reason}
            if waiting.termination is not None:
                content["termination"] = waiting.termination.model_dump(mode="json")
        else:
            return None
        entry = session_wire.StateHistoryEntry(
            id=task_id,
            generation_status=session_wire.GenerationStatus.COMPLETE,
            payload=session_wire.StateHistoryEntryPayload(
                type="workflow_status",
                content=content,
            ),
        )
        state = session_wire.WorkflowSessionHistoryEntryEvent(entry=entry).model_dump(
            mode="json",
            by_alias=True,
            exclude_none=True,
        )
        return workflow_events.WorkflowTaskProjection(state=_JSON_OBJECT_ADAPTER.validate_python(state))

    async def _emit_lifecycle_with_status_sidecar(
        self,
        *,
        task_id: str,
        task_type: str,
        initial_state: workflow_events.WorkflowJsonObject,
        in_progress_states: Iterable[workflow_events.WorkflowJsonObject],
        completed_state: workflow_events.WorkflowJsonObject | None,
        failed: bool,
        failure_message: str | None,
        include_started: bool = True,
    ) -> None:
        await self._product_lifecycle_emitter(
            task_id=task_id,
            task_type=task_type,
            initial_state=initial_state,
            in_progress_states=in_progress_states,
            completed_state=completed_state,
            failed=failed,
            failure_message=failure_message,
            include_started=include_started,
        )
        status = _status_sidecar(initial_state)
        if status is None:
            return
        await self._product_lifecycle_emitter(
            task_id=f"{task_id}:session-status",
            task_type=task_type,
            initial_state=status,
            in_progress_states=(),
            completed_state=status,
            failed=False,
            failure_message=None,
        )


def _status_reasons_for_batch(
    batch: runtime_event_state.SessionEventBatch,
) -> dict[str, _WaitingStatus]:
    reasons: dict[str, _WaitingStatus] = {}
    waiting = _WaitingStatus()
    for event_index, event in enumerate(batch.events):
        if isinstance(event, harness_session.TurnTerminatedEvent):
            waiting = _waiting_status_for_termination(event.turn.termination)
        elif isinstance(event, harness_session.SessionUpdatedEvent) and event.session.status == "waiting":
            reasons[f"{batch.batch_id}:{event_index}"] = waiting
            waiting = _WaitingStatus()
    return reasons


def _waiting_status_for_termination(termination: harness_session.Termination | None) -> _WaitingStatus:
    match termination:
        case harness_session.CancelledTermination():
            return _WaitingStatus(reason="turn_interrupted")
        case harness_session.FailedTermination(error=error):
            return _WaitingStatus(
                termination=session_wire.FailedTurnTermination(
                    error=session_wire.TurnFailureError(code=error.code or "turn_failed", message=_TURN_FAILED_MESSAGE)
                )
            )
        case harness_session.CompletedTermination(stop_reason=str() as stop_reason):
            return _WaitingStatus(reason=stop_reason)
        case _:
            return _WaitingStatus()


def _status_sidecar(
    state: workflow_events.WorkflowJsonObject,
) -> workflow_events.WorkflowJsonObject | None:
    if state.get("type") != "history_entry":
        return None
    entry = state.get("entry")
    if not isinstance(entry, dict):
        return None
    payload = entry.get("payload")
    if not isinstance(payload, dict) or payload.get("type") != "workflow_status":
        return None
    content = payload.get("content")
    if not isinstance(content, dict):
        return None
    status = content.get("status")
    if status == "running":
        event = session_wire.WorkflowSessionStatusChangedEvent(
            status=session_wire.WorkflowSessionStatus.RUNNING,
        )
    elif status == "waiting_for_input":
        reason = content.get("reason")
        event = session_wire.WorkflowSessionStatusChangedEvent(
            status=session_wire.WorkflowSessionStatus.WAITING,
            reason=reason if isinstance(reason, str) else "waiting_for_input",
        )
    else:
        return None
    return _JSON_OBJECT_ADAPTER.validate_python(event.model_dump(mode="json", by_alias=True, exclude_none=True))


def _is_command_user_message(entry: harness_session.HistoryEntry) -> bool:
    return isinstance(entry, harness_session.MessageHistoryEntry) and entry.role == "user"


def _is_empty_assistant_message(entry: harness_session.HistoryEntry) -> bool:
    if not isinstance(entry, harness_session.MessageHistoryEntry) or entry.role != "assistant":
        return False
    return not any(not isinstance(block, harness_session.TextContentBlock) or block.text for block in entry.content)


def _history_entry_state(entry: harness_session.HistoryEntry) -> session_wire.JsonObject:
    event = session_wire.WorkflowSessionHistoryEntryEvent(entry=_history_entry_to_legacy_task_protocol(entry))
    return _JSON_OBJECT_ADAPTER.validate_python(event.model_dump(mode="json", by_alias=True, exclude_none=True))


def _history_entry_to_legacy_task_protocol(
    entry: harness_session.HistoryEntry,
) -> session_wire.HistoryEntry:
    annotations = _history_annotations(entry)
    if isinstance(entry, harness_session.ReasoningHistoryEntry):
        reasoning_text = "\n\n".join(part for part in [*entry.summary, entry.text] if part)
        return session_wire.MessageHistoryEntry(
            id=entry.id,
            generation_status=entry.generation_status,
            annotations=annotations,
            payload=session_wire.MessageHistoryEntryPayload(
                role="assistant",
                content=[session_wire.MessageTextContentBlock(text=reasoning_text)],
                channel="thinking",
            ),
        )
    if isinstance(entry, harness_session.MessageHistoryEntry):
        return session_wire.MessageHistoryEntry(
            id=entry.id,
            generation_status=entry.generation_status,
            annotations=annotations,
            payload=session_wire.MessageHistoryEntryPayload(
                role=entry.role,
                content=[
                    _JSON_OBJECT_ADAPTER.validate_python(
                        block.model_dump(mode="json", by_alias=True, exclude_none=True)
                    )
                    for block in entry.content
                ],
            ),
        )
    if isinstance(entry, harness_session.ToolCallHistoryEntry):
        return session_wire.TaskCallHistoryEntry(
            generation_status=entry.generation_status,
            annotations=annotations,
            payload=session_wire.TaskCallHistoryEntryPayload(
                id=entry.tool_call_id,
                name=entry.name,
                input=entry.arguments,
            ),
        )
    if isinstance(entry, harness_session.ToolResultHistoryEntry):
        return session_wire.TaskResultHistoryEntry(
            generation_status=entry.generation_status,
            annotations=annotations,
            payload=session_wire.TaskResultHistoryEntryPayload(
                id=entry.tool_call_id,
                name=entry.name or "",
                state=session_wire.TaskStatePayload(
                    id=entry.tool_call_id,
                    output=session_wire.TaskOutputPayload(
                        status=_tool_result_status(entry),
                        value=entry.result,
                        error=entry.error.message if entry.error is not None else None,
                    ),
                ),
            ),
        )
    if isinstance(entry, harness_session.NoticeHistoryEntry):
        return session_wire.StateHistoryEntry(
            id=entry.id,
            generation_status=entry.generation_status,
            annotations=annotations,
            payload=notice_to_legacy_task_protocol_payload(
                notice_kind=entry.notice_kind,
                level=entry.level,
                message=entry.message,
                details=entry.details,
            ),
        )
    if isinstance(entry, harness_session.CheckpointHistoryEntry):
        content: session_wire.JsonObject = {"checkpointKind": entry.checkpoint_kind}
        if entry.message is not None:
            content["message"] = entry.message
        if entry.details is not None:
            content["details"] = entry.details
        return session_wire.StateHistoryEntry(
            id=entry.id,
            generation_status=entry.generation_status,
            annotations=annotations,
            payload=session_wire.StateHistoryEntryPayload(
                type="checkpoint",
                content=content,
            ),
        )
    raise TypeError(f"Unsupported Harness history entry: {type(entry).__name__}")


def _history_annotations(entry: harness_session.HistoryEntry) -> session_wire.JsonObject | None:
    annotations = dict(entry.annotations)
    if entry.turn_id is not None:
        annotations[annotation_keys.HARNESS_TURN_ID_ANNOTATION] = entry.turn_id
    if isinstance(entry, harness_session.ToolCallHistoryEntry):
        annotations[annotation_keys.HARNESS_TOOL_KIND_ANNOTATION] = entry.tool_kind
    return annotations or None


def _tool_result_status(entry: harness_session.ToolResultHistoryEntry) -> str:
    if entry.generation_status == "generating":
        return "running"
    if entry.error is not None:
        return "failed"
    return "completed"


__all__ = ["LegacyTaskSessionEventPublisher"]
