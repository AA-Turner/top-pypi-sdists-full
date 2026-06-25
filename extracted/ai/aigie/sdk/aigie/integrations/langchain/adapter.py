"""LangChain FrameworkAdapter (L3).

Tracing-only (empty ``capabilities()``, mirrors ``claude_agent_sdk``): plain
LangChain exposes no mutable mid-run state for workflow-domain interventions.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, ClassVar

from aigie.autonomous.adapters import (
    ActionType,
    ApplyResult,
    ApplyStatus,
    FrameworkAdapter,
    SpanContext,
    register_adapter,
)
from aigie.integrations.langchain._runtime import clear_runtime, set_runtime
from aigie.integrations.langchain.error_conversion import to_kytte_error
from aigie.integrations.langchain.event_classifier import LangChainEventClassifier
from aigie.integrations.langchain.lifecycle import LangChainLifecycle
from aigie.tracing.error_enricher import KytteErrorEnricher
from aigie.tracing.errors import KytteError

if TYPE_CHECKING:
    from aigie.autonomous.interventions.base import WorkflowIntervention
    from aigie.autonomous.runtime import AutonomousRuntime
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

    def _install_autonomous(self, runtime: AutonomousRuntime) -> None:
        return  # no autonomous surface — see capabilities()

    def _install_tracing(self, emitter: TraceEmitter) -> None:
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

    _CAPABILITIES: ClassVar[frozenset[ActionType]] = frozenset()

    @classmethod
    def capabilities(cls) -> frozenset[ActionType]:
        return cls._CAPABILITIES

    def apply(self, intervention: WorkflowIntervention, ctx: SpanContext) -> ApplyResult:
        return ApplyResult(
            status=ApplyStatus.SKIPPED,
            reason=f"unsupported_action:{intervention.action_type.name}",
            observed={},
        )


__all__ = ["LangChainAdapter"]
