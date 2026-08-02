"""Workflow callback infrastructure — signal-based CallbackBridge + routing.

WorkflowCallbackBridge:
  CallbackBridge implementation for the durable workflow path.
  Two-branch send_request: signals parent workflow if parent_exec_id is set,
  emits NATS callback_request event if top-level (external consumer).
  receive_result uses workflow.wait_condition on a shared pending_results dict.

ChildRoute:
  Maps a child workflow's transport identity (child_exec_id) to its semantic
  path identity (path_segment = logical child id for CallbackCallEvent.path).
  Registered at child dispatch time. Never conflated (DL-49).

WorkflowCallbackContext:
  Shared mutable context between the workflow class and TaskWorkflowMixin.
  The workflow class creates it, and the signal handlers read from it
  during execution.
"""

from dataclasses import dataclass, field

import temporalio.workflow  # type: ignore[reportMissingImports]
from mistralai.workflows import task as workflow_task  # type: ignore[reportMissingImports]
from mistralai.workflows import workflow  # type: ignore[reportMissingImports]
from pydantic import JsonValue

from mistralai.vibe.sdk.agent.execution.loop import CallbackBridge
from mistralai.vibe.sdk.agent.tasks.core import TaskCallback
from mistralai.vibe.sdk.agent.tasks.runtime import TaskConfigBase
from mistralai.vibe.sdk.transports.events import CallbackCallEvent, CallbackResultEvent


@dataclass(frozen=True)
class ChildRoute:
    """Maps transport identity to semantic path identity for a child workflow.

    child_exec_id: transport address for signal_external_workflow.
    path_segment: logical child id (TaskState.id) for CallbackCallEvent.path.
    """

    child_exec_id: str
    path_segment: str


@dataclass
class WorkflowCallbackContext:
    """Shared mutable context for callback handling in workflow execution.

    Created by the workflow class. Signal handlers read from this during
    execution. The mixin's prepare_execution() sets callback_schemas and
    impl_configs from the reconstructed task's properties.
    """

    pending_callback_results: dict[str, CallbackResultEvent] = field(default_factory=dict)
    child_routes: dict[str, ChildRoute] = field(default_factory=dict)
    parent_exec_id: str | None = None
    self_exec_id: str | None = None
    observability_context: dict[str, JsonValue] = field(default_factory=dict)
    callback_schemas: dict[str, TaskCallback] = field(default_factory=dict)
    impl_configs: dict[str, TaskConfigBase] = field(default_factory=dict)


class WorkflowCallbackBridge(CallbackBridge):
    """CallbackBridge for the durable workflow path.

    send_request branches on parent_exec_id:
    - If set: signal parent workflow with on_callback_request.
    - If None: emit a callback_request task() CM event (NATS) so the
      external consumer (WorkflowAPIChannel) can detect and resolve it.

    receive_result uses workflow.wait_condition on the shared
    pending_callback_results dict, keyed by call_id. Multiple concurrent
    callbacks each wait on their own call_id.

    Relies on the callback ID uniqueness invariant (see CallbackBridge
    in execution.py): call_id is the SDK-owned correlation key (uuid4).
    Each workflow instance has its own pending_results dict, so there
    is no cross-workflow collision.
    """

    def __init__(
        self,
        parent_exec_id: str | None,
        self_exec_id: str | None,
        pending_results: dict[str, CallbackResultEvent],
    ) -> None:
        self._parent_exec_id = parent_exec_id
        self._self_exec_id = self_exec_id
        self._pending_results = pending_results

    async def send_request(self, event: CallbackCallEvent) -> None:
        if self._parent_exec_id:
            data = event.model_dump()
            data["_source_exec_id"] = self._self_exec_id
            handle = temporalio.workflow.get_external_workflow_handle(self._parent_exec_id)
            # Wrap in {"payload": ...} to match signal handler parameter name —
            # Mistral Workflows SDK validates signal args as Pydantic model fields.
            await handle.signal("on_callback_request", {"payload": data})
        else:
            async with workflow_task(
                "callback_request",
                state=event.model_dump(),
                id=f"callback-{event.payload.id}",
            ):
                pass

    async def receive_result(self, call_id: str) -> CallbackResultEvent:
        await workflow.wait_condition(lambda: call_id in self._pending_results)
        return self._pending_results.pop(call_id)
