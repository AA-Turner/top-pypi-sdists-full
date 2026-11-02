from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from matrx_connect.context.data_types import DataPayload
from matrx_connect.context.events import (
    CitationPayload,
    ContextAnalysisPayload,
    ContextStatePayload,
    ContextTrimmedPayload,
    InfoPayload,
    RecordReservedPayload,
    RecordUpdatePayload,
    InjectionConsumedPayload,
    ProviderRetryPayload,
    ReasoningState,
    ResourceAction,
    StructuredOutputPayload,
    ToolEventPayload,
    WarningPayload,
)
from matrx_connect.context.operations import CompletionPayload, InitPayload
from matrx_connect.context.phases import Phase


@runtime_checkable
class Emitter(Protocol):
    async def send_chunk(self, text: str) -> None: ...

    def reset_turn_text(self) -> None: ...

    def get_turn_text(self) -> str: ...

    async def send_reasoning_chunk(self, text: str) -> None: ...

    async def send_reasoning_state(self, state: ReasoningState) -> None: ...

    async def send_phase(self, phase: Phase) -> None: ...

    async def send_warning(self, payload: WarningPayload) -> None: ...

    async def send_info(self, payload: InfoPayload) -> None: ...

    async def send_data(self, payload: DataPayload | dict[str, Any] | Any) -> None: ...

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

    async def send_injection_consumed(self, payload: InjectionConsumedPayload) -> None: ...

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
