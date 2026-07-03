"""LangGraph FrameworkAdapter.

Registers as framework="langgraph". Owns the SDK's LangGraph tracing
surface: framework patching (`_install_tracing`) so LangGraph workflows
emit events to the platform via a `TraceEmitter`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aigie.auto_instrument._callback_utils import _safe_add_callback, normalize_callbacks
from aigie.integrations._base import FrameworkAdapter, register_adapter
from aigie.integrations.langgraph.config import LangGraphConfig
from aigie.integrations.langgraph.error_conversion import to_kytte_error
from aigie.integrations.langgraph.event_classifier import LangGraphEventClassifier
from aigie.integrations.langgraph.lifecycle import LangGraphLifecycle, _is_aigie_callback
from aigie.tracing.error_enricher import KytteErrorEnricher
from aigie.tracing.errors import KytteError

if TYPE_CHECKING:
    from aigie.rewind.coordinator import RewindCoordinator
    from aigie.tracing.emitter import TraceEmitter


@register_adapter(framework="langgraph")
class LangGraphAdapter(FrameworkAdapter):
    """FrameworkAdapter for LangGraph state-machine agents.

    Operates on the LangGraph state dict passed as ``ctx.framework_handle``.
    All methods degrade gracefully when the state shape is unexpected.
    """

    # ------------------------------------------------------------------
    # Generic FrameworkAdapter interface
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()
        self._emitter: TraceEmitter | None = None
        self._lifecycle: LangGraphLifecycle | None = None

    def extract_error(self, span: dict) -> KytteError | None:
        """Map a LangGraph failure dict to the canonical :class:`KytteError`.

        Delegates to :func:`to_kytte_error`; the adapter is the registered
        entry point so :class:`FrameworkAdapter`'s abstract contract is
        satisfied, but the actual mapping rules live in the conversion
        helper module.
        """
        return to_kytte_error(span)

    def _install_tracing(
        self, emitter: TraceEmitter, *, coordinator: RewindCoordinator | None = None
    ) -> None:
        """Install LangGraph tracing through the native callback substrate.

        Registers ``KytteErrorEnricher`` as the canonical post-emit hook
        that produces ``metadata.error``, then installs
        ``LangGraphLifecycle`` which monkey-patches ``StateGraph.compile``
        so every compiled workflow runs through ``LangGraphNativeCallback``.
        When supplied, ``coordinator`` enables LangGraph rewind capture.
        """

        self._emitter = emitter
        emitter.register_span_complete_hook(KytteErrorEnricher(self.extract_error))
        self._lifecycle = LangGraphLifecycle(
            emitter=emitter,
            adapter=self,
            config=LangGraphConfig.from_env(),
            coordinator=coordinator,
        )
        self._lifecycle.install()

    def _uninstall_tracing(self) -> None:
        """Drop the stored emitter. Monkey-patches applied by
        ``LangGraphLifecycle.install()`` are idempotent and not reversible
        here — production code never uninstalls.
        """
        self._lifecycle = None
        self._emitter = None

    # ------------------------------------------------------------------
    # Per-invocation callback registration (FrameworkAdapter overrides)
    # ------------------------------------------------------------------

    def register_callback(self, callback: Any, framework_config: Any) -> None:
        """Inject ``callback`` into LangGraph's per-invocation callbacks list.

        LangGraph/LangChain dispatch events only to callbacks present in
        ``config["callbacks"]``; without this registration, the framework
        runs but our callback receives zero events. ``_safe_add_callback``
        handles the three shapes ``config["callbacks"]`` can take (list,
        AsyncCallbackManager, CallbackManager).
        """
        if framework_config is None:
            return
        _safe_add_callback(framework_config, callback)

    def is_aigie_callback_already_registered(self, framework_config: Any) -> bool:
        """True if a LangGraphNativeCallback is already wired into
        ``framework_config["callbacks"]``."""
        return any(_is_aigie_callback(cb) for cb in normalize_callbacks(framework_config))

    _classifier: Any = None

    def event_classifier(self) -> Any:
        """Return the singleton LangGraphEventClassifier for this adapter.
        Used by LangGraphNativeCallback to dispatch raw events into kinds.
        """
        if self._classifier is None:
            self._classifier = LangGraphEventClassifier()
        return self._classifier
