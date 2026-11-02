"""A no-op Emitter — swallows every user-facing event.

Use when an agent must run as a SIDE QUEST whose token stream and events must
NOT reach the user's response stream — e.g. a structured-output ranking/scoring
agent invoked mid-request while the real content (synthesis) is streaming on the
parent emitter. Without this, the side-quest agent (with ``stream: true``) leaks
its JSON tokens into the user's content stream via ``send_chunk``.

The agent's structured result still comes back through ``AgentRunResult`` — only
the wire output is muted. Persistence is unaffected (it does not go through the
emitter).
"""

from __future__ import annotations

from typing import Any

from matrx_connect.context.data_types import DataPayload
from matrx_connect.context.events import (
    CitationPayload,
    ContextAnalysisPayload,
    ContextStatePayload,
    ContextTrimmedPayload,
    InfoPayload,
    InjectionConsumedPayload,
    ProviderRetryPayload,
    ReasoningState,
    RecordReservedPayload,
    RecordUpdatePayload,
    ResourceAction,
    StructuredOutputPayload,
    ToolEventPayload,
    WarningPayload,
)
from matrx_connect.context.operations import CompletionPayload, InitPayload
from matrx_connect.context.phases import Phase


class SilentEmitter:
    """Satisfies the ``Emitter`` protocol; every user-facing method is a no-op.

    The per-turn TEXT BUFFER is real, though: the executor's terminal error
    paths recover a mid-stream partial answer via ``get_turn_text()`` and
    persist it — a silenced (reference-mode) child that fails after streaming
    would otherwise lose its billed partial text. Muted on the wire, never
    blind."""

    #: Muted on the wire: a model call under it never stamps the request latency clock
    #: (``request_latency.reaches_wire``).
    reaches_wire = False

    def __init__(
        self,
        *,
        forward_to: Any | None = None,
        forward_data_types: frozenset[str] | None = None,
    ) -> None:
        self._turn_text_acc: list[str] = []
        # A muted child may still owe the person ONE kind of live event — a TTS
        # stage's ``audio_stream_chunk`` IS the product, not leakage. Only the
        # named ``send_data`` types reach ``forward_to``; text, phases, tool and
        # lifecycle events stay muted. (2026-10-01: muting the podcast audio
        # stage whole made the episode wait ~45 min for the end of the run.)
        self._forward_to = forward_to if forward_data_types else None
        self._forward_data_types = forward_data_types or frozenset()

    async def send_chunk(self, text: str) -> None:
        if isinstance(text, str) and text:
            self._turn_text_acc.append(text)

    def reset_turn_text(self) -> None:
        self._turn_text_acc = []

    def get_turn_text(self) -> str:
        return "".join(self._turn_text_acc)

    async def send_reasoning_chunk(self, text: str) -> None: ...

    async def send_reasoning_state(self, state: ReasoningState) -> None: ...

    async def send_phase(self, phase: Phase) -> None: ...

    async def send_warning(self, payload: WarningPayload) -> None: ...

    async def send_info(self, payload: InfoPayload) -> None: ...

    async def send_data(self, payload: DataPayload | dict[str, Any] | Any) -> None:
        if self._forward_to is None:
            return
        data_type = (
            payload.get("type") if isinstance(payload, dict) else getattr(payload, "type", None)
        )
        if data_type in self._forward_data_types:
            await self._forward_to.send_data(payload)

    async def send_init(self, payload: InitPayload) -> None: ...

    async def send_completion(self, payload: CompletionPayload) -> None: ...

    async def send_error(
        self,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None: ...

    async def send_tool_event(self, event_data: ToolEventPayload) -> None: ...

    async def send_record_reserved(self, payload: RecordReservedPayload) -> None: ...

    async def send_record_update(self, payload: RecordUpdatePayload) -> None: ...

    async def send_resource_changed(
        self,
        *,
        kind: str,
        action: ResourceAction,
        resource_id: str,
        sandbox_id: str | None = None,
        user_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None: ...

    async def send_structured_output(self, payload: StructuredOutputPayload) -> None: ...

    async def send_injection_consumed(
        self, payload: InjectionConsumedPayload
    ) -> None: ...

    async def send_provider_retry(self, payload: ProviderRetryPayload) -> None: ...

    async def send_citation(self, payload: CitationPayload) -> None: ...

    async def send_context_analysis(self, payload: ContextAnalysisPayload) -> None: ...

    async def send_context_state(self, payload: ContextStatePayload) -> None: ...

    async def send_context_trimmed(self, payload: ContextTrimmedPayload) -> None: ...

    async def send_end(self, reason: str = "complete") -> None: ...

    async def send_cancelled(self) -> None: ...

    async def fatal_error(
        self,
        error_type: str,
        message: str,
        user_message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None: ...
