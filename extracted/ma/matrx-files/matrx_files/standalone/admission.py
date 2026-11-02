"""Organization admission for the standalone files service — A FILE READ IS DECIDED BY ACCESS.

Law: common-docs/policies/access-ladder.md §3/§4/§8 (Arman, 2026-09-23): a read
is decided by the person's access to the record, never refused because no organization was
picked. ``AuthMiddleware`` refuses an authenticated request that resolved no organization; that
is right for a WRITE (a new row needs its destination) and a RUN (cost lands somewhere), and
wrong for:

* the per-file reads (``GET /files/{id}``, ``/download``, ``/asset``, ``GET /assets/{id}``) —
  each handler calls ``FileService.read_record(file_id, user_id=…)``, which authorizes the row
  by ``files.has_access_for`` as the person. The row carries its OWN organization
  (``FileRecord.organization_id``), so nothing downstream needs the picker's. A route declares
  itself with ``Depends(file_read_decided_by_access)`` on the route (``router_files`` /
  ``router_assets``); this module composes the declarations from the route table the service
  actually mounts.
* ``POST /files/session`` — the file-session cookie is minted for the PERSON
  (``mint_session_cookie_value(user_id, …)``); it names no organization and writes no row.
  It is organization-free by construction: an exact route, never a prefix.

Seen live 2026-09-25 (GATES-TAIL, VERIFIER-21 #2): a fresh session with no organization picked
opened ``/files/f/<id>`` and this service answered 400 to both. A file shared with a person
personally carries an organization she is not a member of, so the FILE's organization header
was refused too ("denied") — the resource lane admits it and the handler decides by access.

Composition REFUSES TO BOOT when a declared route is not a read, or when a canary read is
missing (a lost marker import would otherwise re-gate every file read, silently).
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from matrx_connect import AuthenticatedResourceRoute, authenticated_resource_routes

from matrx_files.api.read_by_access import file_read_decided_by_access

READ_METHODS: frozenset[str] = frozenset({"GET", "HEAD"})

#: Identity-only routes: they act for the person and touch no organization's rows.
ORGANIZATION_FREE_ROUTES: tuple[str, ...] = ("/files/session",)

#: The reads that MUST come back from the route table, or the wiring is broken.
CANARY_READS: tuple[AuthenticatedResourceRoute, ...] = (
    AuthenticatedResourceRoute("GET", "/files/{file_id}"),
    AuthenticatedResourceRoute("GET", "/files/{file_id}/download"),
)


def compose_file_reads(app: FastAPI) -> tuple[AuthenticatedResourceRoute, ...]:
    declared = tuple(authenticated_resource_routes(app, file_read_decided_by_access))
    writes = sorted(f"{e.method} {e.path}" for e in declared if e.method not in READ_METHODS)
    if writes:
        raise RuntimeError(
            "[matrx-files] a route declared file_read_decided_by_access on a method that is "
            f"not a read: {writes}. Only GET/HEAD may be admitted without an organization."
        )
    missing = [f"{e.method} {e.path}" for e in CANARY_READS if e not in declared]
    if missing:
        raise RuntimeError(
            f"[matrx-files] file read declarations lost known entries: {missing}. Refusing to boot "
            "rather than re-gating every file read on the selected organization."
        )
    return declared


def admission_config(app: FastAPI, *, public_paths: tuple[str, ...]) -> dict[str, Any]:
    """The ``AuthMiddleware`` admission kwargs, composed from the mounted route table."""
    from matrx_connect.middleware import DEFAULT_ORG_EXEMPT_PATHS

    return {
        "organization_exempt_paths": DEFAULT_ORG_EXEMPT_PATHS + tuple(public_paths),
        "organization_exempt_routes": ORGANIZATION_FREE_ROUTES,
        "authenticated_resource_routes": compose_file_reads(app),
    }
