"""Deployment bases whose robots run the server's exported contract (every units base but
π0.5's, and the catalog models their deployments serve).

A deployment on one of these bases has no runtime contract in this SDK: the session's
deployment block is the whole contract (cameras, widths, horizons, rate, action meaning,
history), checked against the resolved runtime. A base declares its parser and its contract
in its ``dreamscale.deploy_bases`` module (``ExportedBase``); the SDK's shared code (the
runtime contract, control rate and session) never names it.
"""

from __future__ import annotations

from typing import Any

from dreamscale.deploy_bases import ExportedBase


def _exported() -> dict[str, ExportedBase]:
    # The registry imports the CLI's base modules: loaded when first asked, not with the
    # policy runtime.
    from dreamscale import deploy_bases

    return deploy_bases.exported_bases()


def __getattr__(name: str) -> Any:
    if name == "EXPORTED_BASES":
        return _exported()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def exported_base(model: str | None) -> ExportedBase | None:
    """The base whose deployments ``model`` (an internal id) serves, if it exports its
    contract."""
    return _exported().get(model or "")
