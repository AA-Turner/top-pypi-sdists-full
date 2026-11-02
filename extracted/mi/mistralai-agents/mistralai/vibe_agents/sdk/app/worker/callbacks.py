"""Workflow signal and lifecycle adapter for Harness capability callbacks."""

from uuid import UUID

import structlog
from pydantic import JsonValue, TypeAdapter

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.harness.runtime.capabilities import (
    ApprovalCallbackInvocation,
    CapabilityCallbackRequest,
    CapabilityCallbackResult,
    ProvidedToolInvocation,
)
from mistralai.vibe.harness.runtime.hosts.workflows import (
    WorkflowCallbackTerminalReason,
    WorkflowCapabilityCallbackEventPort,
    WorkflowCapabilityCallbackSignalPort,
)
from mistralai.vibe.harness.runtime.session.callbacks import (
    build_capability_callback_result,
    public_callback_id,
)
from mistralai.vibe_agents import session_workflow as wire
from mistralai.vibe_agents.sdk.app.worker import lifecycle
from mistralai.vibe_agents.sdk.transport import annotation_keys

logger = structlog.get_logger(__name__)
_JSON_VALUE_ADAPTER: TypeAdapter[JsonValue] = TypeAdapter(JsonValue)


class WorkflowCallbackStore(
    WorkflowCapabilityCallbackEventPort,
    WorkflowCapabilityCallbackSignalPort,
):
    """Retain callback requests and results in one Workflow object instance."""

    def __init__(self) -> None:
        self._requests: dict[str, CapabilityCallbackRequest] = {}
        self._runtime_ids: dict[str, str] = {}
        self._published: set[str] = set()
        self._results: dict[str, CapabilityCallbackResult] = {}
        self._terminal_reasons: dict[str, WorkflowCallbackTerminalReason] = {}
        self._published_closures: set[str] = set()

    def get_callback_request(
        self,
        callback_id: str,
    ) -> CapabilityCallbackRequest | None:
        return self._requests.get(callback_id)

    def list_callback_requests(self) -> tuple[CapabilityCallbackRequest, ...]:
        return tuple(self._requests.values())

    def get_callback_terminal_reason(
        self,
        callback_id: str,
    ) -> WorkflowCallbackTerminalReason | None:
        return self._terminal_reasons.get(callback_id)

    async def open_callback_request(
        self,
        request: CapabilityCallbackRequest,
    ) -> CapabilityCallbackRequest:
        opened = self._requests.setdefault(request.callback_id, request)
        public_id = public_callback_id(request.callback_id)
        self._runtime_ids[public_id] = request.callback_id
        if request.callback_id not in self._published and request.callback_id not in self._terminal_reasons:
            invocation = request.invocation
            await lifecycle.emit_history_entry(
                wire.TaskCallHistoryEntry(
                    generation_status=wire.GenerationStatus.COMPLETE,
                    annotations={
                        annotation_keys.HARNESS_TURN_ID_ANNOTATION: request.invocation.turn_id,
                    },
                    payload=wire.CallbackTaskCallHistoryEntryPayload(
                        id=UUID(public_id),
                        name=_callback_name(request),
                        input=_callback_input(request),
                        tool_call_id=(
                            invocation.tool_call_id if isinstance(invocation, ApprovalCallbackInvocation) else None
                        ),
                        tool_id=(invocation.tool_id if isinstance(invocation, ApprovalCallbackInvocation) else None),
                    ),
                ),
                task_id=public_id,
            )
            self._published.add(request.callback_id)
        return opened

    async def publish_callback_ended(
        self,
        callback_id: str,
        *,
        reason: WorkflowCallbackTerminalReason,
    ) -> None:
        if callback_id in self._published_closures:
            return
        # Reject replies immediately, even while closure publication is retried.
        self._terminal_reasons.setdefault(callback_id, reason)
        if callback_id in self._results:
            return
        request = self._requests.get(callback_id)
        if request is None:
            return
        public_id = public_callback_id(callback_id)
        await lifecycle.emit_history_entry(
            wire.TaskResultHistoryEntry(
                generation_status=wire.GenerationStatus.COMPLETE,
                annotations={
                    annotation_keys.HARNESS_TURN_ID_ANNOTATION: request.invocation.turn_id,
                },
                payload=wire.TaskResultHistoryEntryPayload(
                    id=public_id,
                    name="callback_result",
                    state=wire.TaskStatePayload(
                        id=public_id,
                        output=wire.TaskOutputPayload(
                            status="failed",
                            error="Callback closed without a result",
                        ),
                    ),
                ),
            ),
            task_id=public_id,
        )
        self._published_closures.add(callback_id)

    @property
    def waiting_action_ids(self) -> frozenset[str]:
        """The Runtime Actions whose open callback still waits for the user or the app to answer."""

        return frozenset(
            _waited_action_id(request)
            for callback_id, request in self._requests.items()
            if callback_id not in self._results and callback_id not in self._terminal_reasons
        )

    def has_callback_result(self, callback_id: str) -> bool:
        return callback_id in self._results

    def receive_callback_result(
        self,
        request: CapabilityCallbackRequest,
    ) -> CapabilityCallbackResult | None:
        return self._results.get(request.callback_id)

    def submit_result(self, command: wire.CallbackResultCommand) -> bool:
        """Accept the first valid result for a known open callback.

        Refusing an invalid result leaves the callback open for another answer.
        """

        runtime_id = self._runtime_ids.get(str(command.callback_id))
        if runtime_id is None or runtime_id in self._terminal_reasons:
            return False
        request = self._requests[runtime_id]
        try:
            callback_result = _build_callback_result(request, command)
        except ValueError as error:
            # A signal has no reply, so the refusal is logged with the Harness's reason.
            logger.warning(
                "Refused a callback result; the callback stays open",
                callback_id=str(command.callback_id),
                reason=str(error),
            )
            return False

        self._results.setdefault(runtime_id, callback_result)
        return True

    def retire_callbacks(self, callback_ids: frozenset[str]) -> None:
        """Forget Host memory after consuming work commits; published history is unchanged."""
        for callback_id in callback_ids:
            self._requests.pop(callback_id, None)
            self._results.pop(callback_id, None)
            self._runtime_ids.pop(public_callback_id(callback_id), None)
        for callback_id in callback_ids:
            self._terminal_reasons.pop(callback_id, None)
        self._published.difference_update(callback_ids)
        self._published_closures.difference_update(callback_ids)


def _waited_action_id(request: CapabilityCallbackRequest) -> str:
    # An approval callback is named after its Approval Action; a capability invocation names its Action.
    if isinstance(request.invocation, ApprovalCallbackInvocation):
        return request.callback_id
    return request.invocation.action_id


def _build_callback_result(
    request: CapabilityCallbackRequest,
    command: wire.CallbackResultCommand,
) -> CapabilityCallbackResult:
    output = command.result.payload.result.output
    error: harness_session.ProtocolError | None = None
    if output.status == "failed" or output.error is not None:
        error = harness_session.ProtocolError(
            code="callback_failed",
            message=output.error or "Callback failed",
        )
    result = harness_session.CallbackResult(
        callback_id=request.callback_id,
        # A completed answer without a value carries {}; with content it means no value.
        output=None if output.content is not None and output.value == {} else output.value,
        error=error,
        content=output.content,
        is_error=output.is_error,
        meta=output.meta,
    )
    return build_capability_callback_result(request, result)


def _callback_name(request: CapabilityCallbackRequest) -> str:
    invocation = request.invocation
    if isinstance(invocation, ApprovalCallbackInvocation):
        return invocation.name
    if isinstance(invocation, ProvidedToolInvocation):
        return invocation.tool.name
    return invocation.binding_id


def _callback_input(request: CapabilityCallbackRequest) -> JsonValue:
    invocation = request.invocation
    if isinstance(invocation, ApprovalCallbackInvocation):
        return _JSON_VALUE_ADAPTER.validate_python(invocation.input)
    if isinstance(invocation, ProvidedToolInvocation):
        return _JSON_VALUE_ADAPTER.validate_python(invocation.arguments)
    return _JSON_VALUE_ADAPTER.validate_python(
        invocation.model_dump(mode="json", by_alias=True, exclude={"injected_session_inputs"})
    )


__all__ = ["WorkflowCallbackStore", "public_callback_id"]
