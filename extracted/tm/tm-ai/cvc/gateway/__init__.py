"""
CVC Gateway — the redesigned single-folder gateway.

Public surface:

    from cvc.gateway import create_app       # new package factory
    from cvc.gateway import ws_chat_unified  # legacy compat (re-exported)
    from cvc.gateway import _get_event_bus   # legacy compat (re-exported)

The new package is at cvc/gateway/ (chat.py, sessions.py, runs.py, skills.py,
models.py, agent.py, context.py, health.py). The legacy 11,080-line
god-file is preserved as cvc.gateway_legacy and re-exported from this
package so existing imports (`from cvc import gateway as gw`,
`from cvc.gateway import _refresh_agent_budgets`) keep working.
"""

from __future__ import annotations

# CRITICAL: Put the vendored runtime on sys.path BEFORE importing
# anything from it. The tools and plugins packages are vendored under
# cvc/agent/_vendor/hermes/, but their internal imports use top-level
# package names (e.g. `import tools.registry`, `import plugins.browser`).
# Without this path injection, EVERY tool fails to load with
# `ModuleNotFoundError: No module named 'tools'`, leaving the agent
# toolless and forcing it to hallucinate answers. This was the root
# cause of "agent never completes the user's task, just gives a summary
# of what went wrong".
import sys
from pathlib import Path
_VENDORED_HERMES = Path(__file__).resolve().parents[2] / "agent" / "_vendor" / "hermes"
if str(_VENDORED_HERMES) not in sys.path:
    sys.path.insert(0, str(_VENDORED_HERMES))

# Re-export the legacy module so old imports keep working
from cvc import gateway_legacy as _legacy

# Import the new app submodule. This sets cvc.gateway.app to the
# *submodule* (cvc.gateway.app) by Python's package-attr rule, NOT the
# FastAPI object inside it. We need the FastAPI at the attribute path
# `cvc.gateway.app` for uvicorn's `cvc.gateway:app` import string to work
# (uvicorn does `getattr(package, 'app')` → must return a callable, not
# a module). So we import create_app, which causes the submodule to load,
# then re-bind the package's `app` attribute to the FastAPI instance.
from cvc.gateway.app import create_app  # noqa: F401
from cvc.gateway.app import app as _new_fastapi_app

# Re-export commonly-imported symbols from the legacy module
from cvc.gateway_legacy import (  # noqa: F401
    _hermes_api_server,
    _autopilot_on,
    _wire_subagent_runtime,
    _agent_cfg,
    _refresh_agent_budgets,
    _is_expensive_model,
    _resolve_budget,
    _budget_max_iterations,
    _budget_agent_timeout,
    _budget_tool_timeout,
    _soft_wrap_threshold,
    _pick_fallback_synthesis_provider,
    _build_fallback_llm,
    _diagnostic_giveup,
    _deterministic_synthesize,
    _build_nudge_message,
    _classify_stream_error,
    _format_overflow_message,
    _auto_compact_conversation,
    _configure_gateway_logging,
    _set_tool_confirm,
    _get_tool_confirm_result,
    _get_event_bus,
    _get_user_memory_context,
    _ensure,
    _get_db,
    _get_config,
    _get_engine,
    _pick_folder_macos,
    _pick_folder_windows,
    app as legacy_app,
)

__all__ = [
    "create_app",
    "ws_chat_unified",
    "_hermes_api_server",
    "_get_event_bus",
    "_refresh_agent_budgets",
    "legacy_app",
]


# ── PEP 562 module __getattr__ ─────────────────────────────────────────
#
# Some legacy dashboard code (notably cvc/dashboard/personas_api.py and
# cvc/adapters/telegram_handler.py) does ``from cvc import gateway as
# gw`` and then accesses ``gw._workspace_mgr`` (or other legacy module
# globals) at request time. The legacy module's _workspace_mgr is
# ``None`` until the lifespan runs, so a one-shot setattr at import
# time would snapshot a stale value. Instead we forward attribute
# access to the live legacy module: every ``gw._workspace_mgr`` lookup
# hits the current value, not a frozen copy.
#
# Python looks up class/module dict first, then __getattr__, so the
# new package's own canonical names (create_app, etc.) keep priority.
def __getattr__(name: str):
    # Never intercept dunders — those are framework-managed
    # (__path__, __spec__, __loader__, __getattr__ itself, …).
    if name.startswith("__") and name.endswith("__"):
        raise AttributeError(name)
    # Only forward to the legacy module if it actually has the name.
    # Otherwise raise AttributeError so hasattr() / dir() behave
    # correctly.
    if hasattr(_legacy, name):
        return getattr(_legacy, name)
    raise AttributeError(
        f"module 'cvc.gateway' has no attribute {name!r} "
        "(not on the new package, not on the legacy module)"
    )


# CRITICAL: After all the re-exports above, overwrite the package's `app`
# attribute to point at the FastAPI instance. Without this line, `app`
# resolves to the submodule `cvc.gateway.app` (a module object), and
# uvicorn's `cvc.gateway:app` import string fails with
# "TypeError: 'module' object is not callable".
#
# We do this AFTER the re-exports so legacy code that does
# `from cvc.gateway import app` (which Python would normally resolve to
# the submodule) gets the FastAPI. Tests confirm:
#   >>> cvc.gateway.app
#   <FastAPI object>          # ← what we want
#   >>> cvc.gateway.app.app    # also works — FastAPI.app attribute
#   <FastAPI object>
import sys as _sys
_sys.modules['cvc.gateway'].app = _new_fastapi_app  # type: ignore[attr-defined]
