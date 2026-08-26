"""Framework adapter for the Pipecat integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from aigie.integrations._base import FrameworkAdapter, register_adapter
from aigie.integrations.pipecat.config import PipecatConfig
from aigie.integrations.pipecat.error_conversion import to_kytte_error
from aigie.integrations.pipecat.event_classifier import PipecatEventClassifier
from aigie.integrations.pipecat.lifecycle import PipecatLifecycle, _get_singleton
from aigie.tracing.error_enricher import KytteErrorEnricher
from aigie.tracing.errors import KytteError

if TYPE_CHECKING:
    from aigie.rewind.coordinator import RewindCoordinator
    from aigie.tracing.emitter import TraceEmitter


@register_adapter(framework="pipecat")
class PipecatAdapter(FrameworkAdapter):
    """FrameworkAdapter for Pipecat voice pipelines."""

    _classifier: ClassVar[PipecatEventClassifier] = PipecatEventClassifier()

    def __init__(self) -> None:
        super().__init__()
        self._emitter: TraceEmitter | None = None
        self._lifecycle: PipecatLifecycle | None = None

    def extract_error(self, span: dict) -> KytteError | None:
        return to_kytte_error(span)

    def _install_tracing(
        self, emitter: TraceEmitter, *, coordinator: RewindCoordinator | None = None
    ) -> None:
        self._emitter = emitter
        emitter.register_span_complete_hook(KytteErrorEnricher(self.extract_error))
        self._lifecycle = _get_singleton()
        self._lifecycle.configure(emitter, PipecatConfig.from_env())
        self._lifecycle.install()

    def _uninstall_tracing(self) -> None:
        if self._lifecycle is not None:
            self._lifecycle.uninstall()
        self._lifecycle = None
        self._emitter = None

    def event_classifier(self) -> PipecatEventClassifier:
        return self._classifier


__all__ = ["PipecatAdapter"]
