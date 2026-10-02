"""
Per-request Supabase client builder for the scheduler API routes.

The package's internal queries module (``matrx_scheduler.queries``) reads
``sch_*`` tables via matrx-orm Model calls with NO RLS applied (the same
unrestricted trust level the service-role Supabase client this module
used to inject had) to drive the scanner across all users. The HTTP
routes here MUST NOT use that trust level -- user-initiated CRUD has to
bind RLS to the caller's identity, which is why ``api.user_queries`` runs
every query inside ``matrx_orm.rls_session`` scoped to the JWT this
module extracts.

Two paths are supported for building the per-request client that carries
that JWT:

1. **Host-injected factory** (preferred). The host calls
   ``matrx_scheduler.configure(user_supabase_factory=...)`` at startup
   with a callable that takes a user JWT and returns a per-request
   Supabase client. aidream injects its existing
   ``aidream.services.scheduling.per_request_client.make_user_supabase_client``.

2. **Built-in env-based factory** (fallback). Reads
   ``SUPABASE_MATRIX_URL`` + ``SUPABASE_MATRIX_PUBLISHABLE_KEY`` from the
   environment and builds an AsyncClient whose ``apikey`` header is the
   publishable key (project identification only -- carries no
   privileges) and whose ``Authorization`` header is ``Bearer <user_jwt>``
   (RLS sees ``auth.uid()`` = caller). matrx-local can use this by just
   setting the two env vars and never touching ``user_supabase_factory``.

Either way: the service-role key is NEVER usable from these routes.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from fastapi import HTTPException, Request, status

from matrx_scheduler._ext import get_ext


@lru_cache(maxsize=1)
def _env_project_config() -> tuple[str, str]:
    """
    Read Supabase project URL + publishable key from environment.

    Cached -- env reads happen once per process. Raises a 503-friendly
    RuntimeError if the env isn't configured.
    """
    url = os.environ.get("SUPABASE_MATRIX_URL") or os.environ.get("SUPABASE_URL")
    publishable = os.environ.get("SUPABASE_MATRIX_PUBLISHABLE_KEY") or os.environ.get(
        "SUPABASE_PUBLISHABLE_KEY"
    )
    if not url:
        raise RuntimeError(
            "SUPABASE_MATRIX_URL (or SUPABASE_URL) is not set. "
            "Either inject a user_supabase_factory via "
            "matrx_scheduler.configure(...) or set the env var."
        )
    if not publishable:
        raise RuntimeError(
            "SUPABASE_MATRIX_PUBLISHABLE_KEY (or SUPABASE_PUBLISHABLE_KEY) "
            "is not set. Scheduler API routes require the new-format "
            "sb_publishable_... key. Either inject a user_supabase_factory "
            "or set the env var."
        )
    if not publishable.startswith("sb_publishable_"):
        raise RuntimeError(
            "Publishable key does not have the expected sb_publishable_ "
            f"prefix (got {publishable[:20]}...). Verify you're using the "
            "new-format key, not the legacy anon JWT."
        )
    return url, publishable


def default_user_supabase_factory(user_jwt: str) -> Any:
    """
    Fallback factory: build a per-request AsyncClient from env vars.

    Imported lazily so the supabase + httpx deps aren't required for
    package consumers that inject their own factory.
    """
    if not user_jwt:
        raise ValueError("user_jwt is required")

    import httpx  # noqa: PLC0415
    from supabase import AsyncClient  # noqa: PLC0415
    from supabase.lib.client_options import AsyncClientOptions  # noqa: PLC0415

    url, publishable_key = _env_project_config()
    http_client = httpx.AsyncClient(timeout=30.0)
    options = AsyncClientOptions(
        httpx_client=http_client,
        headers={"Authorization": f"Bearer {user_jwt}"},
    )
    return AsyncClient(url, publishable_key, options)


def extract_jwt(request: Request) -> str:
    """Pull the caller's bearer token out of the Authorization header."""
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing bearer token",
        )
    return auth.split(" ", 1)[1]


def make_user_client(user_jwt: str) -> Any:
    """
    Build a per-request user-scoped Supabase client.

    Uses the host-injected factory when available; falls back to the
    env-based default. Either path produces a client whose Authorization
    header is the user JWT -- RLS is the single line of authority.
    """
    factory = get_ext("user_supabase_factory", required=False)
    if factory is None:
        return default_user_supabase_factory(user_jwt)
    return factory(user_jwt)


def user_client_dep(request: Request) -> Any:
    """
    FastAPI dependency: returns a per-request user-scoped Supabase
    client. 401s if no bearer token is present.

    The returned client is no longer used to query ``sch_*`` tables
    directly (that now goes through ``api.user_queries``'s matrx-orm +
    ``rls_session`` seam) -- it's kept only as the vehicle for the
    caller's bearer token, which ``user_queries._claims_from_client``
    reads back out of ``sb.options.headers["Authorization"]``.

    Usage::

        @router.get("/tasks")
        async def list_tasks(
            sb = Depends(user_client_dep),
            ctx: AppContext = Depends(context_dep),
        ):
            return await user_queries.list_tasks(sb)
    """
    jwt = extract_jwt(request)
    return make_user_client(jwt)
