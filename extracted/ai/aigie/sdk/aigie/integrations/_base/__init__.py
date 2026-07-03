"""Adapter registry — decorator-based framework registration.

Public API
----------
- :func:`register_adapter` — class decorator to register a :class:`FrameworkAdapter` subclass.
- :func:`get` — look up (and cache) an adapter instance by framework name.
- :func:`unregister` — remove a framework from the registry + instance cache.
- :func:`unregister_all` — clear everything (used during shutdown / tests).
- :func:`registered_frameworks` — return the set of registered framework names.

Re-exports from base
--------------------
:class:`FrameworkAdapter`, :class:`SpanContext`, :class:`ApplyResult`,
:class:`ApplyStatus`, :class:`ActionType`.

Adding a new framework
----------------------
See ``docs/adapter-matrix.md`` for the three-step contract.
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from aigie.integrations._base.base import (
    ActionType,
    ApplyResult,
    ApplyStatus,
    FrameworkAdapter,
    SpanContext,
)

if TYPE_CHECKING:
    pass

__all__ = [
    # registry
    "register_adapter",
    "get",
    "unregister",
    "unregister_all",
    "registered_frameworks",
    # re-exports from base
    "FrameworkAdapter",
    "SpanContext",
    "ApplyResult",
    "ApplyStatus",
    "ActionType",
]

# ---------------------------------------------------------------------------
# Internal registry state
# ---------------------------------------------------------------------------

_REGISTRY: dict[str, type[FrameworkAdapter]] = {}
_INSTANCES: dict[str, FrameworkAdapter] = {}
_LOCK = threading.Lock()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def register_adapter(framework: str):
    """Class decorator that registers a FrameworkAdapter subclass.

    Usage::

        @register_adapter(framework="my_framework")
        class MyAdapter(FrameworkAdapter):
            @classmethod
            def capabilities(cls) -> set[ActionType]:
                return {ActionType.NEXT_STEP_INJECT_MESSAGE}

            def inject_next_message(self, ctx, role, content):
                ...

    Rules
    -----
    - ``framework`` must be a non-empty string.
    - Re-registering the *same class* for the same name is idempotent (safe
      for repeated module imports).
    - Registering a *different class* for an already-registered name raises
      :exc:`ValueError`.
    - The class itself is returned unchanged so the decorator can be stacked.
    """
    if not isinstance(framework, str) or not framework.strip():
        raise ValueError(
            f"register_adapter: 'framework' must be a non-empty string, got {framework!r}"
        )

    def decorator(cls: type[FrameworkAdapter]) -> type[FrameworkAdapter]:
        if not (isinstance(cls, type) and issubclass(cls, FrameworkAdapter)):
            raise TypeError(
                f"register_adapter: decorated class must be a FrameworkAdapter subclass, "
                f"got {cls!r}"
            )
        with _LOCK:
            existing = _REGISTRY.get(framework)
            if existing is not None and existing is not cls:
                raise ValueError(
                    f"register_adapter: framework {framework!r} is already registered "
                    f"by {existing.__qualname__!r}.  Unregister it first or use the "
                    f"same class (idempotent re-import is allowed)."
                )
            _REGISTRY[framework] = cls
        return cls

    return decorator


def get(framework: str) -> FrameworkAdapter | None:
    """Return a cached adapter instance for *framework*, or ``None`` if not registered.

    The first call for a given framework instantiates the registered class
    (no constructor arguments); subsequent calls return the same instance.
    Thread-safe.
    """
    with _LOCK:
        cls = _REGISTRY.get(framework)
        if cls is None:
            return None
        if framework not in _INSTANCES:
            _INSTANCES[framework] = cls()
        return _INSTANCES[framework]


def unregister(framework: str) -> None:
    """Remove *framework* from the registry and instance cache.

    Silently does nothing if the framework was not registered.
    """
    with _LOCK:
        _REGISTRY.pop(framework, None)
        _INSTANCES.pop(framework, None)


def unregister_all() -> None:
    """Clear the registry and instance cache entirely.

    Used during shutdown ordering and in test teardown fixtures.
    """
    with _LOCK:
        _REGISTRY.clear()
        _INSTANCES.clear()


def registered_frameworks() -> set[str]:
    """Return the set of currently registered framework names."""
    with _LOCK:
        return set(_REGISTRY.keys())
