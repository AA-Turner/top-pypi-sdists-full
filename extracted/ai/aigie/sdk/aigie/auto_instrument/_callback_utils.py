"""Shared helpers for LangChain-callback-based framework integrations.

LangGraph and LangChain both inject `AigieCallbackHandler`-derived
handlers into `config["callbacks"]`. The shape of that config field
varies — sometimes a list, sometimes None, sometimes a
`langchain_core.callbacks.CallbackManager` instance. This helper
normalizes the addition.

Frameworks that don't use LangChain-style callbacks (Strands, Claude
Agent SDK, OpenAI Agents, etc.) have their own protocol-specific
injection mechanisms and do not import from this module.
"""

from __future__ import annotations

from typing import Any


def normalize_callbacks(config: dict | None) -> list[Any]:
    """Return ``config["callbacks"]`` flattened to a list of handlers.

    Accepts the three shapes LangChain uses: missing/None, a plain list, or
    a CallbackManager-like object exposing ``handlers`` + ``inheritable_handlers``.
    """
    if not config:
        return []
    callbacks = config.get("callbacks")
    if callbacks is None:
        return []
    if isinstance(callbacks, list):
        return callbacks
    return list(getattr(callbacks, "handlers", [])) + list(
        getattr(callbacks, "inheritable_handlers", [])
    )


def _safe_add_callback(config: dict, handler: Any) -> None:
    """Safely add a callback handler to config, regardless of callback type.

    Handles plain lists, AsyncCallbackManager, CallbackManager, and any
    other callback container. After this call, `config["callbacks"]` is
    guaranteed to be a list that contains `handler`.
    """
    existing = config.get("callbacks")
    if existing is None:
        config["callbacks"] = [handler]
    elif isinstance(existing, list):
        existing.append(handler)
    else:
        handlers = list(getattr(existing, "handlers", []))
        handlers += list(getattr(existing, "inheritable_handlers", []))
        config["callbacks"] = handlers + [handler]
