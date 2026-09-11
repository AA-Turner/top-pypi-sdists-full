"""Groq adapters exposed without loading the Groq SDK until one is selected."""

from __future__ import annotations

import importlib
from typing import Any

_EXPORTS: dict[str, tuple[str, str]] = {
    "GroqChat": (".groq_api", "GroqChat"),
    "GroqSTT": (".stt", "GroqSTT"),
    "GroqTranslator": (".translator", "GroqTranslator"),
}

__all__ = list(_EXPORTS)


def __getattr__(name: str) -> Any:
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, symbol_name = target
    value = getattr(importlib.import_module(module_name, __name__), symbol_name)
    globals()[name] = value
    return value
