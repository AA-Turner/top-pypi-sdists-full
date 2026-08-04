"""Framework adapter for the OpenAI Agents SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aigie.integrations._base import FrameworkAdapter, register_adapter
from aigie.integrations.openai_agents.config import OpenAIAgentsConfig
from aigie.integrations.openai_agents.error_conversion import to_kytte_error
from aigie.integrations.openai_agents.processor import OpenAIAgentsProcessor
from aigie.tracing.error_enricher import KytteErrorEnricher
from aigie.tracing.errors import KytteError

if TYPE_CHECKING:
    from aigie.rewind.coordinator import RewindCoordinator
    from aigie.tracing.emitter import TraceEmitter


@register_adapter(framework="openai_agents")
class OpenAIAgentsAdapter(FrameworkAdapter):
    def __init__(self) -> None:
        self._processor: OpenAIAgentsProcessor | None = None

    def extract_error(self, span: dict) -> KytteError | None:
        return to_kytte_error(span)

    @property
    def processor(self) -> OpenAIAgentsProcessor | None:
        return self._processor

    def _install_tracing(
        self, emitter: TraceEmitter, *, coordinator: RewindCoordinator | None = None
    ) -> None:
        del coordinator
        try:
            from agents.tracing import add_trace_processor
        except ImportError:
            return
        config = OpenAIAgentsConfig.from_env()
        if self._processor is not None:
            self._processor.configure(emitter, config)
        else:
            self._processor = OpenAIAgentsProcessor(emitter, config)
            add_trace_processor(self._processor)  # type: ignore[arg-type]
        emitter.register_span_complete_hook(KytteErrorEnricher(self.extract_error))

    def _uninstall_tracing(self) -> None:
        if self._processor is not None:
            self._processor.detach()


__all__ = ["OpenAIAgentsAdapter"]
