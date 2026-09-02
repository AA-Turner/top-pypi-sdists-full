"""Guest registry - resolve a stable auth.users UUID for fingerprint visitors.

LAZY FACADE (PEP 562). The real module body lives in ``_guest_registry_impl.py`` and
constructs classes/singletons from HOST-INJECTED ORM bases at module scope,
which requires ``matrx_ai.configure()``. Importing THIS module is therefore
always safe in an unconfigured environment — the impl is imported (and the
managers built, memoized by normal module caching) on FIRST ATTRIBUTE ACCESS,
so config errors surface at call time, never import time. Every public name of
the impl is re-exported unchanged; ``from matrx_ai.db.guest_registry import ...``
keeps working exactly as before in a configured host.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # static analysis only — never imported at runtime
    from ._guest_registry_impl import *  # noqa: F403


def __getattr__(name: str) -> Any:
    from . import _guest_registry_impl as _impl

    try:
        value = getattr(_impl, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
    globals()[name] = value  # cache: __getattr__ fires once per name
    return value


def __dir__() -> list[str]:
    from . import _guest_registry_impl as _impl

    return sorted(n for n in dir(_impl) if not n.startswith("_"))
