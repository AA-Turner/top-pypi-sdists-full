"""Singleton manager instances for conversation exchange (cx_) tables.

LAZY FACADE (PEP 562). The real module body lives in ``_cx_managers_impl.py`` and
constructs classes/singletons from HOST-INJECTED ORM bases at module scope,
which requires ``matrx_ai.configure()``. Importing THIS module is therefore
always safe in an unconfigured environment — the impl is imported (and the
managers built, memoized by normal module caching) on FIRST ATTRIBUTE ACCESS,
so config errors surface at call time, never import time. Every public name of
the impl is re-exported unchanged; ``from matrx_ai.db.cx_managers import ...``
keeps working exactly as before in a configured host.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # static analysis only — never imported at runtime
    from ._cx_managers_impl import *  # noqa: F403


_REQUIRED_BASES: tuple[str, ...] = (
    "AgentMemoryBase",
    "ObservationalMemoryBase",
    "ObservationalMemoryEventBase",
    "RequestBase",
    "RequestSnapshotBase",
    "ToolCallBase",
    "ToolTraceBase",
    "UserRequestBase",
    "MessageBase",
    "MediaBase",
    "ConversationBase",
    "PendingInjectionBase",
)
_REQUIRED_MODELS: tuple[str, ...] = (
    "Message",
    "ToolCall",
    "ToolTrace",
    "Media",
    "UserRequest",
    "Request",
    "RequestSnapshot",
    "AgentMemory",
    "ObservationalMemory",
    "ObservationalMemoryEvent",
    "Conversation",
    "PendingInjection",
)


def is_available() -> bool:
    """Return whether the host registered every artifact needed to build ``cxm``."""
    from ._registry import has_requirements

    return has_requirements(models=_REQUIRED_MODELS, bases=_REQUIRED_BASES)


def server_maintenance_available() -> bool:
    """Return whether this process owns a complete server-side cx backend."""
    from matrx_ai.client_host import get_conversation_store

    return get_conversation_store() is None and is_available()


def __getattr__(name: str) -> Any:
    # Import machinery probes module dunders such as ``__path__`` while
    # resolving ``from ... import ...``. They are facade metadata, never cxm
    # exports; delegating them would eagerly import the ORM-backed impl.
    if name.startswith("__"):
        raise AttributeError(name)

    from . import _cx_managers_impl as _impl

    try:
        value = getattr(_impl, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
    globals()[name] = value  # cache: __getattr__ fires once per name
    return value


def __dir__() -> list[str]:
    from . import _cx_managers_impl as _impl

    return sorted(n for n in dir(_impl) if not n.startswith("_"))
