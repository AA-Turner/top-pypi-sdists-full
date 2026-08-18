"""Public Session API contract and ergonomic client."""

from importlib import import_module
from typing import Any

from . import models, procedures
from .client import SessionClient, SessionEventSequenceError, SessionNotAttachedError
from .transport import SessionTransport

__all__ = [
    *models.__all__,
    *procedures.__all__,
    "SessionClient",
    "SessionEventSequenceError",
    "SessionNotAttachedError",
    "SessionTransport",
]  # pyright: ignore[reportUnsupportedDunderAll]

_MODEL_EXPORTS = frozenset(models.__all__)
_PROCEDURE_EXPORTS = frozenset(procedures.__all__)


def __getattr__(name: str) -> Any:
    if name in _MODEL_EXPORTS:
        value = getattr(import_module("mistralai.vibe.sdk.session.models"), name)
    elif name in _PROCEDURE_EXPORTS:
        value = getattr(import_module("mistralai.vibe.sdk.session.procedures"), name)
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    globals()[name] = value
    return value
