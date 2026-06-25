"""LangChain-native callback handler (L3 framework binding).

Just the framework seams — the callback-driven trace boundary lives in
``LangChainCallbackBase`` (opted into via ``callback_driven = True``).
``register_configure_hook`` constructs this no-arg, so the emitter + config come
from the runtime holder the adapter's ``_install_tracing`` populated.
"""

from __future__ import annotations

from aigie.integrations.langchain._runtime import get_runtime
from aigie.integrations.langchain.event_classifier import LangChainEventClassifier
from aigie.tracing.lc_callback_base import LangChainCallbackBase

_DEFAULT_WORKFLOW_NAME = "LangChain Workflow"

# Stateless, shared across every per-run handler instance.
_CLASSIFIER = LangChainEventClassifier()


class LangChainNativeCallback(LangChainCallbackBase):
    """Callback-driven LangChainCallbackBase bound to LangChain."""

    framework_name = "langchain"
    callback_driven = True

    def __init__(self) -> None:
        rt = get_runtime()
        super().__init__(
            emitter=rt.emitter,
            workflow_name=_DEFAULT_WORKFLOW_NAME,
            classifier=_CLASSIFIER,
            config=rt.config,
        )
