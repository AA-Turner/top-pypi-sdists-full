"""WHO is calling, declared once at the standalone files service's front door (files.matrxserver.com).

Every write this service makes runs on the privileged pool: Postgres sees no ``auth.uid()``, so the only
provenance its row triggers can read is ``app.actor_tier`` / ``app.actor_system``. Until 2026-11-01 nothing
here declared them — and the session-context provider forwarded only the test stamp — so a person's write
that reached a tier-stamped table was refused by ``platform._stamp_actor_tier`` ("declares actor_tier=system,
but names no actor_system"). Found live: deleting a file attached to a chat (its ``platform.associations``
rows) answered 500 (aidream FOUND_DEFECTS AD282).

The class fix, the same shape as the aidream host's (``aidream/services/provenance/request_actor.py``):
``AuthMiddleware(request_scope=request_actor_scope)`` declares the caller for every admitted request, and the
ORM provider (:func:`standalone_session_gucs`) forwards that declaration with the test stamp.

* a person (Supabase JWT, guest fingerprint, file-session cookie) is ``user`` — a person's write names no
  system; the trigger ignores the system for the user tier;
* an ``mx_`` API key is ``system``, named ``api_key:<name|id>`` (the machine lane names itself);
* an anonymous caller declares nothing.

A handler that knows better nests its own ``matrx_orm.declared_actor(...)`` inside and wins (innermost first).
"""

from __future__ import annotations

from contextlib import AbstractAsyncContextManager
from typing import Any

from matrx_connect.context.app_context import AppContext
from matrx_orm import declared_actor, declared_actor_gucs

from matrx_files.standalone.test_stamp import test_run_gucs

_PERSON_AUTH_TYPES = frozenset({"token", "fingerprint", "cookie"})


def request_actor(ctx: AppContext) -> tuple[str, str] | None:
    """``(tier, system)`` an admitted request's writes are attributed to, or None."""
    user_id = (ctx.user_id or "").strip()
    if not user_id:
        return None
    if ctx.auth_type == "api_key":
        meta = ctx.metadata or {}
        return ("system", f"api_key:{meta.get('api_key_name') or meta.get('api_key_id') or user_id}")
    if ctx.auth_type in _PERSON_AUTH_TYPES:
        return ("user", user_id)
    return None


def request_actor_scope(ctx: AppContext) -> AbstractAsyncContextManager[Any] | None:
    """``AuthMiddleware(request_scope=...)`` hook: declare the request's actor."""
    actor = request_actor(ctx)
    return None if actor is None else declared_actor(*actor)


def standalone_session_gucs() -> dict[str, str]:
    """THE standalone service's ORM session-context provider: the declared actor, plus the test stamp."""
    return {**declared_actor_gucs(), **test_run_gucs()}


__all__ = ["request_actor", "request_actor_scope", "standalone_session_gucs"]
