"""Conflict-key de-duplication for batched ``bulk_upsert`` writes.

Postgres refuses an ``INSERT ... ON CONFLICT DO UPDATE`` whose VALUES list
targets one conflict key twice — ``CardinalityViolationError``: *ON CONFLICT DO
UPDATE command cannot affect row a second time*. Every observation-derived
batch in this package is at risk of that, because the row key is DERIVED
(a URL normalizes to one page, an alias resolves to one canonical page), so a
list of legitimately distinct observations can collapse onto one key.

De-duplicating is the CORRECT behaviour, not a workaround: the second row would
overwrite the first inside the same statement anyway. Do it here, once, so no
caller has to remember — and log loudly when it fires, because a collapse is a
real fact about the data.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any

logger = logging.getLogger(__name__)


def dedupe_upsert_rows(
    rows: Sequence[dict[str, Any]],
    *,
    on_conflict: Sequence[str],
    context: str,
) -> list[dict[str, Any]]:
    """Return ``rows`` with at most one row per ``on_conflict`` key.

    The LAST occurrence wins — identical to what the statement itself would do
    if Postgres allowed the duplicate. ``context`` names the call site in the
    warning emitted whenever rows actually collapse.
    """

    if not rows:
        return []
    by_key: dict[tuple[Any, ...], dict[str, Any]] = {}
    for row in rows:
        by_key[tuple(row.get(field) for field in on_conflict)] = row
    deduped = list(by_key.values())
    collapsed = len(rows) - len(deduped)
    if collapsed:
        logger.warning(
            "%s: %d of %d upsert rows collapsed onto an existing (%s) key — "
            "kept the last occurrence of each",
            context,
            collapsed,
            len(rows),
            ", ".join(on_conflict),
        )
    return deduped


__all__ = ["dedupe_upsert_rows"]
