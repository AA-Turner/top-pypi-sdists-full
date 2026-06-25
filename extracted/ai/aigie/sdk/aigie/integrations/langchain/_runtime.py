"""Process-level holder for the LangChain integration's emitter + config.

``register_configure_hook`` constructs ``LangChainNativeCallback`` with no args,
so the emitter can't be passed in — the adapter stashes it here and the callback
reads it at construction. One Aigie client per process, so a singleton fits.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class _LangChainRuntime:
    emitter: Any = None
    config: Any = None


_runtime = _LangChainRuntime()


def set_runtime(*, emitter: Any, config: Any = None) -> None:
    _runtime.emitter = emitter
    _runtime.config = config


def get_runtime() -> _LangChainRuntime:
    return _runtime


def clear_runtime() -> None:
    _runtime.emitter = None
    _runtime.config = None
