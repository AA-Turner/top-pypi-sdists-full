"""Vibe Agents lifecycle events emitted outside canonical Harness history."""

import time
from typing import Literal

import temporalio.workflow
from pydantic import JsonValue

import mistralai.workflows as workflows
from mistralai.vibe.harness.runtime.content import to_model_json_text
from mistralai.vibe.harness.runtime.hosts.workflows import session_events as workflow_events
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.transport import annotation_keys
from mistralai.vibe_agents.session_workflow import message_context, session_v1_wire

# Reporting a start with no initial command as idle adds lifecycle activity calls to the Workflow
# history. A Session already running when this shipped has none of them, so replaying it under the
# new code would diverge. The marker keeps those runs on the path their history records.
_IDLE_START_WAITING_STATUS_PATCH = "vibe_agents_sdk.idle_start_waiting_status.v1"


def _now_ms() -> int:
    if temporalio.workflow.in_workflow():
        return int(temporalio.workflow.now().timestamp() * 1000)
    return int(time.time() * 1000)


async def emit_session_started(params: wire.SessionWorkflowStartInput) -> None:
    """Publish stable product rows for a newly opened Harness Session."""

    starts_idle = _starts_idle(params)
    if params.session_protocol == "session_v1":
        # v1 has no state entry kind, so the initialized row is dropped. The idle status still has to
        # go out: an idle start runs no turn, so this is the only event telling a client the session
        # is up and waiting. Its readers are the vibe_agents projection and code-server; this SDK's
        # own remote transport reads the legacy rows below, never these.
        if starts_idle:
            await _emit_v1_waiting_status(str(params.session_id))
        return
    initialized = wire.StateHistoryEntry(
        payload=wire.SessionInitializedStatePayload(
            content=wire.SessionInitializedStateContent(
                application_id=params.application_id,
                application_name=params.application_name,
                agent_id=params.agent_id,
                agent_name=params.agent_name,
                source=_command_source(params.initial_command),
            )
        )
    )
    await emit_history_entry(
        initialized,
        task_id=f"{params.session_id}:initialized",
    )
    if starts_idle:
        await _emit_legacy_waiting_status(str(params.session_id))


async def emit_command_receipt(
    command: wire.SessionWorkflowCommand,
    *,
    session_id: str,
    session_v1: bool,
    turn_id: str | None = None,
) -> None:
    """Publish the product-owned acknowledgement for one accepted command."""

    if session_v1:
        await _emit_v1_command_receipt(command, session_id=session_id, turn_id=turn_id)
        return
    entry = build_history_entry_for_command(command, turn_id=turn_id)
    if entry is None:
        return
    await emit_history_entry(entry, task_id=_command_task_id(command))


async def _emit_v1_command_receipt(
    command: wire.SessionWorkflowCommand,
    *,
    session_id: str,
    turn_id: str | None,
) -> None:
    # The Harness publisher drops role="user" entries so this stays the one public user row.
    if not isinstance(command, wire.MessageCommand):
        return
    # command_id is optional and the API accepts an initial command without one. Key the row on the
    # turn instead of dropping it, or the session shows an answer to a message it never recorded.
    # turn_id falls back to workflow.uuid4(), so it survives replay as stable task ids require.
    entry_id = _command_task_id(command) or (f"{turn_id}:user" if turn_id is not None else None)
    if entry_id is None:
        return
    await emit_v1_message_receipt(
        entry_id,
        turn_id=turn_id or command.expected_turn_id or _message_turn_id(command),
        content=_v1_message_content(command),
        annotations=dict(message_context.annotations_for_context(command.context))
        if command.context is not None
        else {},
        session_id=session_id,
    )


async def emit_v1_message_receipt(
    entry_id: str,
    *,
    turn_id: str | None,
    content: list[session_v1_wire.ContentBlock],
    annotations: dict[str, JsonValue],
    session_id: str,
) -> None:
    """Publish the Session v1 row of one user message, from either message path."""

    now = _now_ms()
    entry = session_v1_wire.WorkflowMessageHistoryEntry(
        id=entry_id,
        turn_id=turn_id,
        generation_status="complete",
        created_at=now,
        updated_at=now,
        annotations=annotations,
        role="user",
        content=content,
    )
    state = session_v1_wire.WorkflowSessionV1TaskState(session_id=session_id, entry=entry).model_dump(
        mode="json",
        exclude_none=True,
    )
    await workflow_events.emit_workflow_task_lifecycle(
        task_id=entry_id,
        task_type=wire.SESSION_V1_EVENT_TASK_TYPE,
        initial_state=state,
        completed_state=state,
    )


async def _emit_v1_waiting_status(session_id: str) -> None:
    now = _now_ms()
    state = session_v1_wire.WorkflowSessionV1StatusTaskState(
        session_id=session_id,
        session_event=session_v1_wire.WorkflowSessionUpdatedEvent(
            session=session_v1_wire.Session(
                id=session_id,
                root_session_id=session_id,
                status="waiting",
                created_at=now,
                updated_at=now,
            )
        ),
    ).model_dump(mode="json", exclude_none=True)
    await workflow_events.emit_workflow_task_lifecycle(
        task_id=f"{session_id}:initial-status",
        task_type=wire.SESSION_V1_STATUS_EVENT_TASK_TYPE,
        initial_state=state,
        completed_state=state,
    )


async def emit_v1_turn_refused(session_id: str, *, turn_id: str, error: session_v1_wire.ProtocolError) -> None:
    """Publish a Turn that failed before it started, because the Session refused its message.

    Session v1 has no command outcome row, so this event is how a client that waits for the Turn
    learns that it will never run.
    """

    state = session_v1_wire.WorkflowSessionV1TurnTaskState(
        session_id=session_id,
        root_session_id=session_id,
        turn_event=session_v1_wire.WorkflowTurnTerminatedEvent(
            turn=session_v1_wire.TurnState(
                id=turn_id,
                status="terminated",
                completed_at=_now_ms(),
                termination=session_v1_wire.FailedTermination(error=error),
            )
        ),
    ).model_dump(mode="json", exclude_none=True)
    # Started-only, like the Runtime's own Turn events: the controller reads no completed Turn event.
    await workflow_events.emit_workflow_task_lifecycle(
        task_id=f"{turn_id}:refused",
        task_type=wire.SESSION_V1_TURN_EVENT_TASK_TYPE,
        initial_state=state,
    )


def _v1_message_content(command: wire.MessageCommand) -> list[session_v1_wire.ContentBlock]:
    blocks: list[session_v1_wire.ContentBlock] = []
    for part in command.message.parts:
        if isinstance(part, wire.MessagePartText):
            blocks.append(session_v1_wire.TextContentBlock(text=part.text))
        elif isinstance(part, wire.MessagePartImage):
            blocks.append(session_v1_wire.ImageContentBlock(uri=part.image_url))
        elif isinstance(part, wire.MessagePartResourceLink):
            blocks.append(
                session_v1_wire.ResourceLinkContentBlock(
                    uri=part.uri,
                    name=part.name,
                    media_type=part.mime_type,
                )
            )
        elif isinstance(part, wire.MessagePartForm):
            blocks.append(session_v1_wire.TextContentBlock(text=to_model_json_text(part.model_dump(mode="json"))))
    return blocks


async def emit_command_outcome(
    command_id: str,
    *,
    outcome: Literal["accepted", "rejected"],
    turn_id: str | None,
    reason: str | None,
    session_v1: bool,
    retryable: bool = False,
) -> None:
    """Publish an explicit compare-and-set result for a Turn command."""

    # A command outcome is a legacy state row with no v1 entry kind.
    if session_v1:
        return
    content: dict[str, JsonValue] = {
        "commandId": command_id,
        "outcome": outcome,
        "turnId": turn_id,
        "reason": reason,
    }
    if retryable:
        content["retryable"] = True
    await emit_history_entry(
        wire.StateHistoryEntry(
            generation_status=wire.GenerationStatus.COMPLETE,
            payload=wire.StateHistoryEntryPayload(
                type=annotation_keys.HARNESS_COMMAND_OUTCOME_STATE,
                content=content,
            ),
        ),
        task_id=command_id,
    )


async def emit_history_entry(
    entry: wire.HistoryEntry,
    *,
    task_id: str | None = None,
) -> None:
    state = wire.WorkflowSessionHistoryEntryEvent(entry=entry).model_dump(
        mode="json",
        by_alias=True,
        exclude_none=True,
    )
    await workflow_events.emit_workflow_task_lifecycle(
        task_id=task_id or str(workflows.workflow.uuid4()),
        task_type=wire.SESSION_EVENT_TASK_TYPE,
        initial_state=state,
        completed_state=state,
    )


async def _emit_legacy_waiting_status(session_id: str) -> None:
    """Project an idle empty Session onto the legacy Vibe Agents status contract."""

    task_id = f"{session_id}:initial-status"
    reason = "waiting_for_input"
    entry = wire.StateHistoryEntry(
        id=task_id,
        generation_status=wire.GenerationStatus.COMPLETE,
        payload=wire.StateHistoryEntryPayload(
            type="workflow_status",
            content={"status": "waiting_for_input", "reason": reason},
        ),
    )
    await emit_history_entry(entry, task_id=task_id)
    status = wire.WorkflowSessionStatusChangedEvent(
        status=wire.WorkflowSessionStatus.WAITING,
        reason=reason,
    ).model_dump(mode="json", by_alias=True, exclude_none=True)
    await workflow_events.emit_workflow_task_lifecycle(
        task_id=f"{task_id}:session-status",
        task_type=wire.SESSION_EVENT_TASK_TYPE,
        initial_state=status,
        completed_state=status,
    )


def _starts_idle(params: wire.SessionWorkflowStartInput) -> bool:
    """True when the Session opens with no message to run.

    Two shapes: neither ``initial_command`` nor ``initial_turn``, and the explicit
    ``resume``/``empty_session`` sentinel. Other non-message commands run no Turn either (the
    Workflow only admits a ``MessageCommand``) but stay out of this branch; widening it is a
    separate change.
    """

    if params.initial_turn is not None:
        return False
    command = params.initial_command
    if isinstance(command, wire.SystemCommand):
        return command.action == "resume" and command.reason == "empty_session"
    if command is not None:
        return False
    if not temporalio.workflow.in_workflow():
        return True
    return temporalio.workflow.patched(_IDLE_START_WAITING_STATUS_PATCH)


def message_content(command: wire.MessageCommand) -> list[wire.MessageContentBlock]:
    blocks: list[wire.MessageContentBlock] = []
    for part in command.message.parts:
        if isinstance(part, wire.MessagePartText):
            blocks.append(wire.MessageTextContentBlock(text=part.text))
        elif isinstance(part, wire.MessagePartImage):
            blocks.append(wire.MessageImageContentBlock(image_url=part.image_url))
        elif isinstance(part, wire.MessagePartResourceLink):
            blocks.append(
                wire.MessageResourceLinkContentBlock(
                    uri=part.uri,
                    name=part.name,
                    mime_type=part.mime_type,
                    annotations=part.annotations,
                )
            )
        elif isinstance(part, wire.MessagePartForm):
            blocks.append(wire.MessageTextContentBlock(text=to_model_json_text(part.model_dump(mode="json"))))
    return blocks


def message_text(command: wire.MessageCommand) -> str:
    return "\n".join(
        part.text for part in command.message.parts if isinstance(part, wire.MessagePartText) and part.text
    )


def build_history_entry_for_command(
    command: wire.SessionWorkflowCommand,
    *,
    turn_id: str | None,
) -> wire.HistoryEntry | None:
    if isinstance(command, wire.MessageCommand):
        return build_message_history_entry(command, turn_id=turn_id)
    if isinstance(command, wire.CallbackResultCommand):
        result = command.result.payload.result
        task_id = result.id or str(command.callback_id)
        return wire.TaskResultHistoryEntry(
            generation_status=wire.GenerationStatus.COMPLETE,
            payload=wire.TaskResultHistoryEntryPayload(
                id=task_id,
                name="callback_result",
                state=wire.TaskStatePayload(
                    id=task_id,
                    input=result.input,
                    output=wire.TaskOutputPayload.model_validate(result.output.model_dump(mode="json")),
                    history=[],
                ),
            ),
        )
    return None


def build_message_history_entry(command: wire.MessageCommand, *, turn_id: str | None) -> wire.MessageHistoryEntry:
    annotations = dict(message_context.annotations_for_context(command.context)) if command.context is not None else {}
    annotations[annotation_keys.HARNESS_TURN_ID_ANNOTATION] = (
        turn_id or command.expected_turn_id or _message_turn_id(command)
    )
    return wire.MessageHistoryEntry(
        id=str(command.command_id) if command.command_id is not None else None,
        generation_status=wire.GenerationStatus.COMPLETE,
        annotations=annotations,
        payload=wire.MessageHistoryEntryPayload(
            role="user",
            content=message_content(command),
            meta=wire.MessageMeta(source=command.source),
        ),
    )


def _command_source(command: wire.SessionWorkflowCommand | None) -> str | None:
    if isinstance(command, wire.MessageCommand | wire.IntegrationEventCommand):
        return command.source
    return None


def _command_task_id(command: wire.SessionWorkflowCommand) -> str | None:
    if isinstance(command, wire.CallbackResultCommand):
        return str(command.callback_id)
    return str(command.command_id) if command.command_id is not None else None


def _message_turn_id(command: wire.MessageCommand) -> str | None:
    return _command_task_id(command)


__all__ = [
    "build_history_entry_for_command",
    "build_message_history_entry",
    "emit_command_receipt",
    "emit_command_outcome",
    "emit_history_entry",
    "emit_session_started",
    "emit_v1_message_receipt",
    "emit_v1_turn_refused",
    "message_text",
]
