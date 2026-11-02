from __future__ import annotations

from typing import TYPE_CHECKING

# Lazily re-export what the CLI and the worker import from here. This is an internal surface, not the
# SDK's: an author builds an Agent in Python, and loading a project from disk is the CLI's job.
# Importing this package must not pull in the loader (and through it agents + the koyeb sandbox, ~3s)
# just to run the CLI, so PEP 562 __getattr__ (below) defers the heavy import until the name is
# actually accessed, keeping `--help` and arg parsing near-instant.
__all__ = ["AgentApp", "AgentProjectError", "load_app"]

# TYPE_CHECKING-only: give type-checkers the real names WITHOUT the load-time import __getattr__ defers.
if TYPE_CHECKING:
    from mistralai.vibe_agents.sdk.app.errors import AgentProjectError
    from mistralai.vibe_agents.sdk.app.loader import AgentApp, load_app


def __getattr__(name: str) -> object:
    if name == "AgentProjectError":
        from mistralai.vibe_agents.sdk.app.errors import AgentProjectError  # noqa: PLC0415

        return AgentProjectError
    if name in {"AgentApp", "load_app"}:
        from mistralai.vibe_agents.sdk.app import loader  # noqa: PLC0415

        return getattr(loader, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
