"""L3 framework adapter for the Claude Agent SDK integration.

Registers as framework ``"claude_agent_sdk"``. Mirrors
``LangGraphAdapter`` in shape. ``_install_tracing`` wires the
``KytteErrorEnricher`` post-emit hook and installs monkey-patches via
``ClaudeAgentSDKLifecycle``.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, ClassVar

from aigie.integrations._base import FrameworkAdapter, register_adapter
from aigie.integrations.claude_agent_sdk.error_conversion import to_kytte_error
from aigie.integrations.claude_agent_sdk.event_classifier import (
    ClaudeAgentSDKEventClassifier,
)
from aigie.integrations.claude_agent_sdk.lifecycle import (
    ClaudeAgentSDKLifecycle,
    _get_singleton,
)
from aigie.integrations.claude_agent_sdk.rewind import ClaudeAgentSDKRewindCapability
from aigie.tracing.error_enricher import KytteErrorEnricher
from aigie.tracing.errors import KytteError

if TYPE_CHECKING:
    from aigie.rewind.coordinator import RewindCoordinator
    from aigie.tracing.emitter import TraceEmitter

logger = logging.getLogger(__name__)


@register_adapter(framework="claude_agent_sdk")
class ClaudeAgentSDKAdapter(FrameworkAdapter):
    """FrameworkAdapter for the Claude Agent SDK stream-based runtime."""

    _classifier: ClassVar[ClaudeAgentSDKEventClassifier] = ClaudeAgentSDKEventClassifier()

    def __init__(self) -> None:
        super().__init__()
        self._emitter: TraceEmitter | None = None
        self._lifecycle: ClaudeAgentSDKLifecycle | None = None

    def extract_error(self, span: dict) -> KytteError | None:
        return to_kytte_error(span)

    def _install_tracing(
        self, emitter: TraceEmitter, *, coordinator: RewindCoordinator | None = None
    ) -> None:
        self._emitter = emitter
        emitter.register_span_complete_hook(KytteErrorEnricher(self.extract_error))
        if coordinator is not None:
            coordinator.register(ClaudeAgentSDKRewindCapability())
        self._lifecycle = _get_singleton()
        self._lifecycle._emitter = emitter
        self._lifecycle._adapter = self
        self._lifecycle.install()

    def _uninstall_tracing(self) -> None:
        if self._lifecycle is not None:
            self._lifecycle.uninstall()
        self._lifecycle = None
        self._emitter = None

    def event_classifier(self) -> ClaudeAgentSDKEventClassifier:
        return self._classifier


__all__ = ["ClaudeAgentSDKAdapter"]
