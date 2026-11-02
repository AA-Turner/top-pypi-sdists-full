"""The change feed's deletion leg: one bounded page that includes tombstones.

``DatabaseClient.list_changed_files_async`` answers the sandbox down-sync with
MODIFICATIONS ONLY — it filters ``deleted_at IS NULL`` and never selects the
column. That was survivable while a second downstream transport existed: a
soft-delete reached the replica over Supabase Realtime. On 2026-09-17 the
sandbox deleted that subscriber (a sandbox never talks to the platform database
— the bridge is the one hop and it is what carries the organization), which
left the poll as the ONE downstream and deletions with no way home: a file the
person deleted in the UI stayed on the sandbox's disk, and the shutdown
up-sync pushed it back to the cloud. The delete undid itself.

This module is that one query, written once, so the page a sandbox polls is the
whole truth about what changed since its cursor:

* rows with ``updated_at > since``, **tombstones included** — the
  ``platform._touch_row`` trigger stamps ``updated_at`` on a soft-delete, so a
  deletion rides the same cursor as a modification and no second ordering,
  cursor, or pagination scheme is needed;
* ``deleted_at`` is SELECTED, so the caller can mark the row rather than
  inferring a deletion from absence (absence is also what a page-limit looks
  like);
* the same tenant scope as every other bridge read — ``organization_id`` is
  REQUIRED and applied **in SQL**, because a scope applied after the limit is a
  short page that reads as the end of the feed.

It lives beside ``db.py`` instead of inside it deliberately: ``db.py`` and
``sync_engine.py`` were being edited by another lane in the same hour, and a
new read has no business colliding with that.

Consumer: ``aidream/services/sandboxes/cloud_files_changes.py`` (the
``GET /api/cloud-files/changes`` bridge route). Contract both halves meet on:
matrx-sandbox ``sandbox-image/sdk/matrx_agent/cloud_sync/FEATURE.md`` § The
``/changes`` contract.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .db import (
    CHANGE_FEED_STATEMENT_TIMEOUT_SECONDS,
    _SYNC_LIST_FIELDS,
    DatabaseClient,
    _vals,
)

#: Exactly what the modifications-only feed selected, plus the one column that
#: says a row is a tombstone. Nothing was removed: a consumer reading the old
#: page shape keeps working, it simply now also learns about deletions.
CHANGE_FEED_FIELDS: tuple[str, ...] = (*_SYNC_LIST_FIELDS, "deleted_at")


def _models():
    """Lazy model access — and the loud not-bound gate (mirrors ``db._models``)."""
    from matrx_files.db import ensure_bound

    ensure_bound()
    from matrx_files.db import models_files, models_iam

    return models_files, models_iam


async def list_changed_files_including_deletions_async(
    *,
    user_id: str,
    since_iso: str,
    limit: int = 1000,
    organization_id: str,
    include_system: bool = False,
) -> list[dict[str, Any]]:
    """One page of this owner's changes in ONE organization, tombstones included.

    Rows are ordered oldest → newest by ``updated_at`` and hard-limited, so the
    caller's cursor (the newest ``updated_at`` it emitted) can never skip work:
    anything truncated by the limit is still greater than that cursor.

    Args:
        user_id: the person the sandbox acts for (``files.files.created_by``).
        since_iso: exclusive cursor; only ``updated_at > since`` is returned.
        limit: hard bound on the page — small rows, bounded parse (the
            2026-06-12 ``event_loop_stall`` lesson).
        organization_id: REQUIRED. The tenant the bridge call was admitted for.
        include_system: keep ``generations/`` and ``system-files/`` (app
            artifacts) out of a user's replica unless a caller really wants them.

    Returns:
        Row dicts carrying ``CHANGE_FEED_FIELDS``; a row whose ``deleted_at`` is
        set is a tombstone — the file no longer exists for this person.
    """
    if not organization_id:
        raise ValueError(
            "organization_id is required: an absent organization is a refusal, "
            "never every tenant. Read it off the carried request context "
            "(context_organization_id) and pass it."
        )

    mf, _ = _models()
    from matrx_orm import Q

    from matrx_files.system_paths import SystemPathRegistry

    since = datetime.fromisoformat(since_iso.replace("Z", "+00:00"))
    # NOTE the absent ``deleted_at__isnull=True``: that filter IS the defect this
    # module exists to fix. Everything else matches the modifications-only feed.
    q = mf.Files.filter(
        created_by=user_id,
        organization_id=organization_id,
        updated_at__gt=since,
    )
    if not include_system:
        for root in SystemPathRegistry.roots():
            q = q.filter(~Q(file_path__startswith=f"{root}/"))
    rows = await (
        q.order_by("updated_at")
        .limit(limit)
        .timeout(CHANGE_FEED_STATEMENT_TIMEOUT_SECONDS)
        .replay_safe_empty()
        .values(*CHANGE_FEED_FIELDS)
    )
    return DatabaseClient._owner_from_db_many(_vals(rows))


__all__ = [
    "CHANGE_FEED_FIELDS",
    "list_changed_files_including_deletions_async",
]
