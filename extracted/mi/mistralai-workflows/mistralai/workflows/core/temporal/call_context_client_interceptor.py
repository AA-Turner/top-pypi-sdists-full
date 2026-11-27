"""Client side of the call context: send it to the worker as a Temporal header.

The worker exposes it to the code the call runs through `get_call_context()`. A header keeps it out
of the input payload, so the input can stay fully encrypted, and outbound calls never inherit it.
"""

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

from temporalio.client import (
    Interceptor,
    OutboundInterceptor,
    SignalWorkflowInput,
    StartWorkflowInput,
    StartWorkflowUpdateInput,
    WorkflowHandle,
    WorkflowUpdateHandle,
)

from mistralai.workflows.constants import CALL_CONTEXT_HEADER
from mistralai.workflows.protocol.v1.workflow import call_context_to_payload

_outgoing_call_context: ContextVar[Mapping[str, Any] | None] = ContextVar("outgoing_call_context", default=None)


@contextmanager
def sending_call_context(call_context: Mapping[str, Any] | None) -> Iterator[None]:
    """Attach `call_context` to the Temporal start, signal or update made inside this block."""
    token = _outgoing_call_context.set(call_context)
    try:
        yield
    finally:
        _outgoing_call_context.reset(token)


class _CallContextOutboundInterceptor(OutboundInterceptor):
    def _attach(self, input: StartWorkflowInput | SignalWorkflowInput | StartWorkflowUpdateInput) -> None:
        call_context = _outgoing_call_context.get()
        if call_context:
            input.headers = {**(input.headers or {}), CALL_CONTEXT_HEADER: call_context_to_payload(call_context)}

    async def start_workflow(self, input: StartWorkflowInput) -> WorkflowHandle[Any, Any]:
        self._attach(input)
        return await super().start_workflow(input)

    async def signal_workflow(self, input: SignalWorkflowInput) -> None:
        self._attach(input)
        await super().signal_workflow(input)

    async def start_workflow_update(self, input: StartWorkflowUpdateInput) -> WorkflowUpdateHandle[Any]:
        self._attach(input)
        return await super().start_workflow_update(input)


class CallContextClientInterceptor(Interceptor):
    def intercept_client(self, next: OutboundInterceptor) -> OutboundInterceptor:
        return _CallContextOutboundInterceptor(next)
