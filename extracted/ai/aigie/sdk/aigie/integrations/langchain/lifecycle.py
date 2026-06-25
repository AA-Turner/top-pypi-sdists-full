"""LangChain lifecycle binding (L2).

LangChain has no compile-style entry point, so instead of patching ``invoke``
we register langchain_core's ``register_configure_hook`` (the LangSmith
mechanism): every run's ``_configure`` then attaches a fresh
``LangChainNativeCallback`` at the top-level run and inherits it into children.
"""

from __future__ import annotations

import logging
import os
from contextvars import ContextVar
from typing import Any

from aigie.tracing.callback_lifecycle import CallbackLifecycle

logger = logging.getLogger(__name__)

# Left None on purpose: enablement is driven by the env var, so langchain_core
# constructs a fresh handler per top-level run (== one trace per invocation).
_AIGIE_LC_VAR: ContextVar[Any | None] = ContextVar("aigie_langchain_handler", default=None)

_ENABLE_ENV_VAR = "AIGIE_LANGCHAIN_ENABLED"

_hook_registered = False


class LangChainLifecycle(CallbackLifecycle):
    framework_type = "langchain"

    def __init__(
        self,
        emitter: Any = None,
        adapter: Any = None,
        *,
        config: Any = None,
    ) -> None:
        CallbackLifecycle.__init__(self)
        self._emitter = emitter
        self._adapter = adapter
        self._config = config

    def _install_native_hook(self) -> bool:
        """Register the configure hook and enable it via the env var."""
        global _hook_registered
        try:
            from langchain_core.tracers.context import register_configure_hook

            from aigie.integrations.langchain.native_callback import LangChainNativeCallback
        except ImportError:
            return False

        if not _hook_registered:
            register_configure_hook(
                _AIGIE_LC_VAR,
                True,  # inheritable: child runs reuse the top-level handler
                LangChainNativeCallback,
                _ENABLE_ENV_VAR,
            )
            _hook_registered = True

        os.environ[_ENABLE_ENV_VAR] = "1"
        return True

    def _uninstall_native_hook(self) -> None:
        """Disable the hook. The registration itself can't be unregistered from
        langchain_core, but clearing the env var stops handler creation."""
        os.environ.pop(_ENABLE_ENV_VAR, None)


_singleton: LangChainLifecycle | None = None


def _get_singleton() -> LangChainLifecycle:
    global _singleton
    if _singleton is None:
        _singleton = LangChainLifecycle()
    return _singleton


def install_langchain_patches() -> None:
    """Module-level entry point matching the registry's ``patch_function`` shape."""
    _get_singleton().install()


def uninstall_langchain_patches() -> None:
    """Module-level uninstaller used by the test conftest."""
    _get_singleton().uninstall()


__all__ = [
    "LangChainLifecycle",
    "install_langchain_patches",
    "uninstall_langchain_patches",
]
