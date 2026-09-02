"""AiModelDTO — LAZY FACADE (PEP 562).

The real module body lives in ``_ai_model_dto_impl.py`` and resolves the
HOST-INJECTED ``AiModel`` model at module scope (``get_model("AiModel")``),
which requires ``matrx_ai.configure()``. Importing THIS module is always safe
in an unconfigured environment — the impl is imported (and ``AiModel`` resolved)
on FIRST ATTRIBUTE ACCESS, so config errors surface at call time, never import
time. Every public name of the impl is re-exported unchanged.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # static analysis only — never imported at runtime
    from ._ai_model_dto_impl import *  # noqa: F403


def __getattr__(name: str) -> Any:
    from . import _ai_model_dto_impl as _impl

    try:
        value = getattr(_impl, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
    globals()[name] = value  # cache: __getattr__ fires once per name
    return value


def __dir__() -> list[str]:
    from . import _ai_model_dto_impl as _impl

    return sorted(n for n in dir(_impl) if not n.startswith("_"))
