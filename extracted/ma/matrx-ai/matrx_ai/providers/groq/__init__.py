"""Groq adapters exposed without loading the Groq SDK until one is selected."""

from __future__ import annotations

import importlib
from typing import Any

#: Exported name -> the sibling module that defines it (under that same name).
#: A flat str -> str table on purpose: the mandate scanner resolves
#: ``_EXPORTS.get(name)`` to this closed set of our own submodules, so the lazy
#: import below is a static fact to it rather than an UNRESOLVED_IMPORT row.
_EXPORTS: dict[str, str] = {
    "GroqChat": ".groq_api",
    "GroqSTT": ".stt",
    "GroqTranslator": ".translator",
}

__all__ = list(_EXPORTS)


def __getattr__(name: str) -> Any:
    module_name = _EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(importlib.import_module(module_name, __name__), name)
    globals()[name] = value
    return value
