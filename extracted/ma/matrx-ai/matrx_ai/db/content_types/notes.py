"""Notes content-type manager (host-injected NotesBase).

LAZY FACADE (PEP 562). The real module body lives in ``_notes_impl.py`` and
constructs classes/singletons from HOST-INJECTED ORM bases at module scope,
which requires ``matrx_ai.configure()``. Importing THIS module is therefore
always safe in an unconfigured environment — the impl is imported on FIRST
ATTRIBUTE ACCESS, so config errors surface at call time, never import time.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # static analysis only — never imported at runtime
    from ._notes_impl import *  # noqa: F403


def __getattr__(name: str) -> Any:
    from . import _notes_impl as _impl

    try:
        value = getattr(_impl, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
    globals()[name] = value  # cache: __getattr__ fires once per name
    return value


def __dir__() -> list[str]:
    from . import _notes_impl as _impl

    return sorted(n for n in dir(_impl) if not n.startswith("_"))
