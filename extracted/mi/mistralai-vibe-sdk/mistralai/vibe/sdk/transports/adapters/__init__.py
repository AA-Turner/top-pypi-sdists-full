"""Concrete transport adapters (local, HTTP, workflow API...)."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "LocalChannel",
    "StreamableHttpBinding",
]

if TYPE_CHECKING:
    from mistralai.vibe.sdk.transports.adapters.local import LocalChannel
    from mistralai.vibe.sdk.transports.adapters.streamable_http import StreamableHttpBinding

_LAZY_EXPORTS = {
    "LocalChannel": "mistralai.vibe.sdk.transports.adapters.local",
    "StreamableHttpBinding": "mistralai.vibe.sdk.transports.adapters.streamable_http",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
