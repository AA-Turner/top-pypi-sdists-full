"""The ``probe`` command-line adapter over :mod:`probe.sdk`.

The implementation (`probe.cli.main`) and the API client load on first use, not
on `import probe.cli`: a module beside them (`mcp_bridge`, `team_note_file`) costs
only itself (plan M1: the daemon imports those, and must not pay for the whole
CLI). `probe.cli.main` stays this module's `main` function, as before.
"""

from __future__ import annotations

import importlib
import sys
import types


def main(argv: list[str] | None = None) -> int:
    # Preserve the original public monkeypatch seam while keeping implementation
    # code in its own submodule. Do not retain a caller's temporary factory for
    # later commands invoked directly through the Typer app. Unpatched, `Client`
    # is not in this module's namespace yet and is not imported here: the SDK
    # client loads every wire model (~0.5 s), so a command imports it when it
    # builds one (`main._client_class`).
    implementation = _implementation()
    previous = implementation.Client
    implementation.Client = globals().get("Client")
    try:
        return implementation.main(argv)
    finally:
        implementation.Client = previous


def _implementation():
    return importlib.import_module(f"{__name__}.main")


def _client():
    from ..sdk.client import Client

    return Client


def __getattr__(name: str):
    if name == "Client":
        value = _client()
    elif name == "app":
        value = _implementation().app
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    globals()[name] = value
    return value


class _Package(types.ModuleType):
    """Importing the submodule `probe.cli.main` binds it as this package's `main`
    attribute; `probe.cli.main` must stay the function (`probe._entry` calls it),
    as it was when the submodule was imported first."""

    def __setattr__(self, name: str, value) -> None:
        if name == "main" and isinstance(value, types.ModuleType):
            return
        super().__setattr__(name, value)


sys.modules[__name__].__class__ = _Package

__all__ = ["Client", "app", "main"]
