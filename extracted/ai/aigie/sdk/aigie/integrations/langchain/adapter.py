"""LangChain FrameworkAdapter (L3).

Tracing-only: plain LangChain exposes no mutable mid-run state.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, ClassVar

from aigie.integrations._base import FrameworkAdapter, register_adapter
from aigie.integrations.langchain._runtime import clear_runtime, set_runtime
from aigie.integrations.langchain.error_conversion import to_kytte_error
from aigie.integrations.langchain.event_classifier import LangChainEventClassifier
from aigie.integrations.langchain.lifecycle import LangChainLifecycle
from aigie.tracing.error_enricher import KytteErrorEnricher
from aigie.tracing.errors import KytteError

if TYPE_CHECKING:
    from aigie.rewind.coordinator import RewindCoordinator
    from aigie.tracing.emitter import TraceEmitter

logger = logging.getLogger(__name__)


@register_adapter(framework="langchain")
class LangChainAdapter(FrameworkAdapter):
    """FrameworkAdapter for LangChain (LCEL / chains / agents)."""

    _classifier: ClassVar[LangChainEventClassifier] = LangChainEventClassifier()

    def __init__(self) -> None:
        super().__init__()
        self._emitter: TraceEmitter | None = None
        self._lifecycle: LangChainLifecycle | None = None

    def extract_error(self, span: dict) -> KytteError | None:
        return to_kytte_error(span)

    def _install_tracing(
        self, emitter: TraceEmitter, *, coordinator: RewindCoordinator | None = None
    ) -> None:
        self._emitter = emitter
        emitter.register_span_complete_hook(KytteErrorEnricher(self.extract_error))
        # callback is constructed no-arg by langchain_core — pass emitter via the holder.
        set_runtime(emitter=emitter, config=None)
        self._lifecycle = LangChainLifecycle(emitter=emitter, adapter=self)
        self._lifecycle.install()

    def _uninstall_tracing(self) -> None:
        if self._lifecycle is not None:
            self._lifecycle.uninstall()
        self._lifecycle = None
        self._emitter = None
        clear_runtime()

    def event_classifier(self) -> LangChainEventClassifier:
        return self._classifier


__all__ = ["LangChainAdapter"]
