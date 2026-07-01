"""Entry points for the Dreadnode SDK app package."""

from __future__ import annotations

import typing as t

__all__ = ["DEFAULT_INSTANCE", "Dreadnode"]


def __getattr__(name: str) -> t.Any:
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    from dreadnode.app.main import DEFAULT_INSTANCE, Dreadnode

    exports = {
        "DEFAULT_INSTANCE": DEFAULT_INSTANCE,
        "Dreadnode": Dreadnode,
    }
    value = exports[name]
    globals()[name] = value
    return value
