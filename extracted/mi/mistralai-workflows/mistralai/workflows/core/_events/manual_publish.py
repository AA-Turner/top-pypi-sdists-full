"""Workflow-side publishing of manually emitted event batches.

EventContext.publish_events_batch delegates here from workflow code: each batch is published by
a local activity whose completion is checkpointed in the run's history, so a worker restart
resumes after the last published batch instead of losing or duplicating its events.

This module is imported by event_context at module level, so it must not import, at module
level, anything that imports event_context back (event_activities, activity,
workflow_run_config); those imports are deferred to the functions that need them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import temporalio.workflow

from mistralai.workflows.core._events.event_encoder import _strip_unserializable_payloads
from mistralai.workflows.core._events.manual_publish_state import next_legacy_manual_publish_ordinal
from mistralai.workflows.protocol.v1.events import JSONPatchPayload, WorkflowEvent

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


@dataclass(frozen=True)
class BatchEvent:
    """One recorded workflow event paired with the encrypted paths of its JSON patch payload."""

    serialized: dict[str, Any]
    encrypted_paths: list[str]


def _json_patch_payload(event: WorkflowEvent) -> JSONPatchPayload | None:
    payload = getattr(event.attributes, "payload", None)
    return payload if isinstance(payload, JSONPatchPayload) else None


def _encrypted_paths_of(event: WorkflowEvent) -> list[str]:
    payload = _json_patch_payload(event)
    return sorted(payload._encrypted_paths) if payload else []


def _restore_encrypted_paths(event: WorkflowEvent, encrypted_paths: list[str]) -> None:
    payload = _json_patch_payload(event)
    if payload:
        payload._encrypted_paths = set(encrypted_paths)


async def _publish_workflow_events(events: list[WorkflowEvent]) -> None:
    # Deferred: event_context imports this module at module level and event_activities imports
    # event_context at module level, so a module-level import here would close a cycle.
    from mistralai.workflows.core._events.event_activities import _run_batch_emitter
    from mistralai.workflows.core._events.event_context import _permanent_publish_failure

    if not temporalio.workflow.patched("durable-manual-event-batches"):
        # A run-wide False is memoized, so each legacy invocation needs its own migration marker.
        ordinal = next_legacy_manual_publish_ordinal()
        if not temporalio.workflow.patched(f"durable-manual-event-batches-fallback:{ordinal}"):
            return
    events = [_strip_unserializable_payloads(event) for event in events]
    encrypted_paths = [_encrypted_paths_of(event) for event in events]
    try:
        serialized = [event.model_dump(mode="json") for event in events]
    except Exception as e:
        raise _permanent_publish_failure(events, e) from e
    batch = [
        BatchEvent(serialized=event, encrypted_paths=paths)
        for event, paths in zip(serialized, encrypted_paths, strict=True)
    ]
    await _execute_batch_emitter(batch, _run_batch_emitter)


async def _execute_batch_emitter(
    events: list[BatchEvent], run_batch_emitter: Callable[[list[BatchEvent]], Awaitable[bool]]
) -> None:
    if not await run_batch_emitter(events):
        midpoint = len(events) // 2
        await _execute_batch_emitter(events[:midpoint], run_batch_emitter)
        await _execute_batch_emitter(events[midpoint:], run_batch_emitter)
