"""Canonical access checks for ``seo.collection_run`` — the ONE kernel.

DEF-12 / WS-5: the standalone and aidream collection routes each compared the
caller against ``row.created_by`` OR the row's org against the caller's
*currently active* ``ctx.organization_id``. That locks a legitimate user out
of their own run the instant a different organization is active, and grants
ANY member of the matching org — not just admins — blanket read of every run
in it. The platform's canonical rule keys access on the USER, never the
active org:

- Reads:  ``iam.has_access_for(user_id, 'seo_collection_run', run_id, level)``
- Lists:  ``iam.is_discoverable(user_id, 'seo_collection_run', run_id, level)``

Both predicates resolve owner (unconditional, any org active), org
admin/owner, explicit ``iam.permissions`` grants, membership, and
reachability inside the ONE SECURITY DEFINER body — see
``common-docs/systems/platform/access/STATE.md``. Never hand-roll a
comparison against ``created_by``/``organization_id`` again; call these.

Host (aidream) and standalone (``matrx_seo.standalone.app``) both import this
module directly — neither implements its own version, and the host router
never reaches into ``standalone.app`` for it.
"""

from __future__ import annotations

import logging

from matrx_orm import call_function

from matrx_seo.db import PACKAGE_DB_NAME

logger = logging.getLogger(__name__)

COLLECTION_RUN_RESOURCE_TYPE = "seo_collection_run"


async def collection_run_readable(
    user_id: str | None, run_id: str, *, level: str = "viewer"
) -> bool:
    """True iff ``user_id`` may READ collection run ``run_id`` at ``level``.

    Fail-closed: a blank id or any DB error reads as no access.
    """
    if not user_id or not run_id:
        return False
    try:
        return bool(
            await call_function(
                PACKAGE_DB_NAME,
                "iam",
                "has_access_for",
                user_id,
                COLLECTION_RUN_RESOURCE_TYPE,
                str(run_id),
                level,
                mode="scalar",
            )
        )
    except Exception:  # noqa: BLE001 — fail closed, never raise into the route
        logger.warning(
            "seo collection_run access check failed for %s (level=%s)", run_id, level, exc_info=True
        )
        return False


async def collection_run_discoverable(
    user_id: str | None, run_id: str, *, level: str = "viewer"
) -> bool:
    """True iff run ``run_id`` should appear in a LIST/search for ``user_id``.

    Omits contextual (reachability-only) access by design — see
    ``common-docs/systems/platform/access/CONTEXTUAL_ACCESS.md``. Use this for any enumeration
    surface; never ``collection_run_readable`` for a list.
    """
    if not user_id or not run_id:
        return False
    try:
        return bool(
            await call_function(
                PACKAGE_DB_NAME,
                "iam",
                "is_discoverable",
                user_id,
                COLLECTION_RUN_RESOURCE_TYPE,
                str(run_id),
                level,
                mode="scalar",
            )
        )
    except Exception:  # noqa: BLE001 — fail closed
        logger.warning(
            "seo collection_run discoverability check failed for %s (level=%s)",
            run_id,
            level,
            exc_info=True,
        )
        return False


async def discoverable_collection_run_ids(user_id: str | None, *, level: str = "viewer") -> set[str]:
    """EVERY run id the person may enumerate — ``iam.discoverable_ids``, ONE statement.

    The set twin of :func:`collection_run_discoverable` (the enumerator can never be wider than
    the per-row reader). A list asks THIS once instead of asking the per-row predicate for every
    row: at ~0.4s a call that was 10s for a 25-row page. Fails loud — an empty answer would read
    as "no runs" — so a failure raises.
    """
    if not user_id:
        return set()
    from matrx_orm import TypedArg

    ids = await call_function(
        PACKAGE_DB_NAME,
        "iam",
        "discoverable_ids",
        str(user_id),
        COLLECTION_RUN_RESOURCE_TYPE,
        TypedArg(level, "public.permission_level"),
        mode="scalar",
    )
    return {str(i) for i in (ids or [])}


def _newest_runs(offset: int, size: int, organization_id: str | None):
    """Read newest runs; ``organization_id`` is an explicit optional filter."""
    from matrx_seo.db import models_seo as m

    query = m.CollectionRun.filter(deleted_at__isnull=True)
    if organization_id:
        query = query.filter(organization_id=organization_id)
    return query.order_by("-created_at").offset(offset).limit(size).all()


async def _pick_visible(discoverable: set[str], chunk: list, *, limit: int, size: int, organization_id):
    out: list = []
    offset = 0
    while True:
        out.extend(r for r in chunk if str(r.id) in discoverable)
        if len(out) >= limit or len(chunk) < size:
            return out[:limit]
        offset += size
        chunk = await _newest_runs(offset, size, organization_id)


async def list_discoverable_runs(
    user_id: str | None,
    *,
    organization_id: str | None = None,
    limit: int = 25,
    while_waiting=None,
) -> tuple[list, object]:
    """``(rows, extra)``: the newest ``limit`` runs the person may enumerate, across all her orgs.

    The discoverable set (the kernel's ~1.3s call) and the newest rows are read TOGETHER, then
    intersected — never the other way round (``id IN`` a 9,000-id list cost 1.4s on its own).
    ``while_waiting(visible_rows)`` receives only the discovered intersection, never the global
    candidate window. When the newest chunk holds fewer than ``limit`` discoverable rows and more
    exist, the next chunk is read.
    ``organization_id`` is an explicit optional filter only on the page.
    """
    import asyncio

    size = max(int(limit) * 4, 50)
    if not user_id:
        return [], None
    discoverable_task = asyncio.ensure_future(discoverable_collection_run_ids(user_id))
    try:
        chunk = await _newest_runs(0, size, organization_id)
        discoverable = await discoverable_task
    except BaseException:
        discoverable_task.cancel()
        raise
    if not discoverable:
        return [], None
    visible = await _pick_visible(
        discoverable, chunk, limit=int(limit), size=size, organization_id=organization_id
    )
    extra = await while_waiting(visible) if while_waiting is not None else None
    return visible, extra


__all__ = [
    "COLLECTION_RUN_RESOURCE_TYPE",
    "collection_run_discoverable",
    "discoverable_collection_run_ids",
    "list_discoverable_runs",
    "collection_run_readable",
]
