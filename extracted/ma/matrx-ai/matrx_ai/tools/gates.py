"""Tool gating registry.

`tool_def.gating` is a jsonb array of `{gate: <name>, args: {...}}` entries.
Each `gate` name must resolve to a function registered here, or the
startup gate-registry pass (`aidream/startup/tools_check.py`) crashes loudly
per rule R15 of `common-docs/systems/agents/agent-tools/DECISIONS.md`.

Two flavours of gate exist, both registered the same way:

1. **Server-side advisory gates**. Functions that the server's tool dispatcher
   could call to filter tools BEFORE handing them to the model. Today none
   need to actually evaluate at dispatch time — surface defaults and
   binding-existence already do the heavy lifting — so these are registered
   as constant-true stubs that simply prove the name resolves.

2. **Client-side advisory gates**. Tools whose gating is enforced INSIDE the
   client (the Chrome extension's optional-permissions check, for example).
   The server stores the gate's name + args as metadata; the client reads
   it and decides what to expose to its user. The server-side function here
   exists ONLY so the startup registry check passes — it does not evaluate
   the permission. It returns True unconditionally; the client is the
   authority.

If a real server-side enforcement is later needed for any gate, swap the
stub for the real implementation. The shape (`(args, ctx) -> bool`) is
deliberately minimal so callers can stay simple.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

GateFn = Callable[[Mapping[str, Any], Any], bool]


# Public registry. `aidream/startup/tools_check.py` reads either the
# `is_registered` predicate or this dict directly to validate every
# `tool_def.gating` entry at boot.
GATES: dict[str, GateFn] = {}


def register(name: str) -> Callable[[GateFn], GateFn]:
    """Decorator: register a gate function under `name`."""
    def _wrap(fn: GateFn) -> GateFn:
        if name in GATES:
            raise ValueError(f"gate {name!r} already registered")
        GATES[name] = fn
        return fn
    return _wrap


def is_registered(name: str) -> bool:
    """Return True iff `name` resolves to a registered gate function."""
    return name in GATES


def get(name: str) -> GateFn | None:
    """Return the registered gate function or None."""
    return GATES.get(name)


def all_names() -> list[str]:
    """Return all registered gate names (sorted)."""
    return sorted(GATES)


# ---------------------------------------------------------------------------
# Built-in gates
# ---------------------------------------------------------------------------


@register("has_optional_permission")
def _has_optional_permission(args: Mapping[str, Any], ctx: Any) -> bool:
    """Client-side advisory gate. Stored on `tool_def.gating` as
    `{"gate": "has_optional_permission", "args": {"permission": "<chrome-permission>"}}`.

    The actual permission check runs INSIDE the Chrome extension before the
    tool is offered to the user. The server has no Chrome runtime, so this
    stub simply confirms the name resolves at startup. Returns True
    unconditionally — the client is the authority.
    """
    return True


@register("is_admin")
def _is_admin(args: Mapping[str, Any], ctx: Any) -> bool:
    """Server-side gate. True iff the request context belongs to an admin.

    The actual admin-only enforcement for tool discovery happens in
    `matrx_ai.tools.implementations.browser_discovery` and the discovery
    handlers that emit tool catalogs — they consult `ctx.is_admin` directly.
    This function exists so any `tool_def.gating` row referencing `is_admin`
    resolves cleanly at startup.
    """
    if ctx is None:
        return False
    return bool(getattr(ctx, "is_admin", False))


@register("requires_client_executor")
def _requires_client_executor(args: Mapping[str, Any], ctx: Any) -> bool:
    """Server-side gate, ENFORCED at merge time (`merge_request_tools`
    pre-flight), not here. Stored on `tool_def.gating` as
    `{"gate": "requires_client_executor", "args": {"executor": "chrome-extension"}}`.

    Meaning: this tool is only useful when the named client executor (or a
    dot-descendant, e.g. ``chrome-extension.pilot``) is live on the request —
    typically a server-side discovery/loader tool whose entire payload is
    client-delegated (``load_chrome_tools``). When the executor isn't in the
    request's active client-kind set, the merge funnel drops the tool before
    the model ever sees it. This stub exists so the gate name resolves at
    startup; the real check lives in
    ``matrx_ai.tools.merge.required_client_executor_unmet``.
    """
    return True


__all__ = [
    "GateFn",
    "register",
    "is_registered",
    "get",
    "all_names",
    "GATES",
]
