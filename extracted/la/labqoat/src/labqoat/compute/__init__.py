"""Decorator-authored compute declarations and automatic publication.

Each public name loads on first use, so worker processes that import compute internals do not load the
authoring API until authored code asks for it.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from labqoat.compute.app import App
    from labqoat.compute.automatic_recovery import AutomaticRecovery
    from labqoat.compute.batching import Batching
    from labqoat.compute.concurrency import Concurrency
    from labqoat.compute.enter_decorator import EnterDecorator
    from labqoat.compute.function import Function
    from labqoat.compute.image import Image
    from labqoat.compute.method_decorator import MethodDecorator
    from labqoat.compute.sandboxes import Sandboxes
    from labqoat.compute.scaling import Scaling
    from labqoat.compute.secret import Secret
    from labqoat.compute.volume import Volume
    from labqoat.compute.web_servers import web_server
    from labqoat.compute.workers import Workers

    enter = EnterDecorator
    method = MethodDecorator

_EXPORTS = {
    "App": ("labqoat.compute.app", "App"),
    "AutomaticRecovery": ("labqoat.compute.automatic_recovery", "AutomaticRecovery"),
    "Batching": ("labqoat.compute.batching", "Batching"),
    "Concurrency": ("labqoat.compute.concurrency", "Concurrency"),
    "Function": ("labqoat.compute.function", "Function"),
    "Image": ("labqoat.compute.image", "Image"),
    "Scaling": ("labqoat.compute.scaling", "Scaling"),
    "Sandboxes": ("labqoat.compute.sandboxes", "Sandboxes"),
    "Secret": ("labqoat.compute.secret", "Secret"),
    "Volume": ("labqoat.compute.volume", "Volume"),
    "Workers": ("labqoat.compute.workers", "Workers"),
    "web_server": ("labqoat.compute.web_servers", "web_server"),
    "enter": ("labqoat.compute.enter_decorator", "EnterDecorator"),
    "method": ("labqoat.compute.method_decorator", "MethodDecorator"),
}

__all__ = [
    "App",
    "AutomaticRecovery",
    "Batching",
    "Concurrency",
    "Function",
    "Image",
    "Scaling",
    "Sandboxes",
    "Secret",
    "Volume",
    "Workers",
    "web_server",
    "enter",
    "method",
]


def __getattr__(name: str) -> object:
    """Load a public name the first time it is read."""
    if name not in _EXPORTS:
        raise AttributeError(f"module 'labqoat.compute' has no attribute {name!r}")
    module, attribute = _EXPORTS[name]
    value = getattr(import_module(module), attribute)
    globals()[name] = value
    return value
