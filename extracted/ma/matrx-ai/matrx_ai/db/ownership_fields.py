from __future__ import annotations

from typing import Any


def read_row_owner(row: Any) -> str | None:
    if isinstance(row, dict):
        owner = row.get("created_by") or row.get("user_id")
    else:
        owner = getattr(row, "created_by", None) or getattr(row, "user_id", None)
    return str(owner) if owner else None


def stamp_row_owner(
    row: dict[str, Any],
    owner_id: str,
    *,
    table_columns: frozenset[str] | None = None,
) -> None:
    if not owner_id:
        return
    if table_columns is None:
        # created_by is the canonical owner column platform-wide. The only
        # caller that may still need a legacy user_id is the schema-driven
        # path below, which asks the live table what columns it actually has.
        row.setdefault("created_by", owner_id)
        return
    if "created_by" in table_columns:
        row.setdefault("created_by", owner_id)
    if "user_id" in table_columns:
        row.setdefault("user_id", owner_id)


def stamp_org_id(row: dict[str, Any], organization_id: str | None) -> None:
    """Stamp the request's ``organization_id`` onto an outgoing cx_ INSERT.

    The 2026-06 schema reorg made ``organization_id`` NOT NULL on the org-scoped
    chat.* tables (conversation / user_request / message / tool_call / memory).
    This records the user's CHOSEN org (``ctx.organization_id``) so the row is
    attributed correctly. When the org is unknown (personal scope), we leave it
    unset and the DB backstop trigger ``chat._stamp_org_default`` defaults it to
    the creator's personal org — the same policy as
    ``resolve_effective_organization_id``. Idempotent: never overwrites an
    explicit value already in ``row``.
    """
    if organization_id:
        row.setdefault("organization_id", organization_id)
