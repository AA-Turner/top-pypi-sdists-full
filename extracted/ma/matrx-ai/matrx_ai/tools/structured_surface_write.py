"""The read-before / attach-after pair every STRUCTURED writer uses for its receipt.

:func:`matrx_ai.tools.surface_write.attach_structured_write` renders a before and
an after value as stable JSON. Every structured writer (a plan node, a map
topic, a CMS row, a settings object, a dataset row) needs the same two extra
steps around it, and each one written by hand drifts:

* **read the prior value BEFORE the write** — and never let that read fail the
  write: :func:`read_prior` logs and answers ``None``, which skips the receipt;
* **scope both sides to what changed** — :func:`changed_fields` keeps the keys
  whose value moved (plus the keys the caller asked to set, so a no-op write
  still shows "no change" instead of vanishing) and drops bookkeeping columns
  (``updated_at`` …) that change on every write and would bury the real diff.

:func:`structured_surface_write` is both steps' tail: scope, then attach — on a
successful result only (``attach_surface_write`` enforces that).
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable, Iterable, Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from matrx_ai.tools.models import ToolResult

logger = logging.getLogger(__name__)

#: Bookkeeping columns that move on every write and say nothing about the change.
VOLATILE_FIELDS: frozenset[str] = frozenset(
    {"updated_at", "updated_by", "modified_at", "last_modified", "__kind"}
)


async def read_prior(thunk: Callable[[], Awaitable[Any]], *, what: str) -> Any | None:
    """The prior value for a receipt, or ``None`` when it could not be read.

    A failed prior read NEVER fails the write: the write path reports its own
    errors (a missing row, a denied id). The receipt is skipped and the skip is
    logged by name so a card that shows no diff is explainable."""
    try:
        return await thunk()
    except Exception as exc:  # noqa: BLE001 — a receipt is never worth a failed write
        logger.warning("[surface_write] prior read for %s failed; no receipt: %s", what, exc)
        return None


def changed_fields(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    *,
    keys: Iterable[str] = (),
    ignore: Iterable[str] = VOLATILE_FIELDS,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """``before`` / ``after`` cut down to the keys that moved, plus ``keys``.

    A key present on only one side stays on only that side, so an added field
    reads as an addition and a removed one as a removal."""
    skip = set(ignore)
    shown = {k for k in set(before) | set(after) if k not in skip and before.get(k) != after.get(k)}
    shown |= {k for k in keys if k in before or k in after}
    return (
        {k: before[k] for k in sorted(shown) if k in before},
        {k: after[k] for k in sorted(shown) if k in after},
    )


def structured_surface_write(
    result: ToolResult,
    *,
    before: Any,
    after: Any,
    target_type: str,
    target_id: str | None = None,
    target_label: str = "",
    keys: Iterable[str] = (),
    ignore: Iterable[str] = VOLATILE_FIELDS,
    scope: bool = True,
    edits: int | None = None,
) -> ToolResult:
    """Attach the structured receipt for a successful write.

    ``before is None`` means the prior read failed (:func:`read_prior`) — no
    receipt, never a failed write; pass ``{}`` for "did not exist yet". With
    ``scope`` (the default) two mappings are cut to what changed
    (:func:`changed_fields`); pass ``scope=False`` for a value already scoped
    by the caller (one node, one settings object)."""
    from matrx_ai.tools.surface_write import attach_structured_write

    if not result.success:
        return result
    if before is None or after is None:
        logger.warning(
            "[surface_write] %s %s: %s value unavailable; no receipt",
            target_type,
            target_id,
            "prior" if before is None else "new",
        )
        return result
    if scope and isinstance(before, Mapping) and isinstance(after, Mapping):
        before, after = changed_fields(before, after, keys=keys, ignore=ignore)
    return attach_structured_write(
        result,
        before=before,
        after=after,
        target_type=target_type,
        target_id=target_id,
        target_label=target_label,
        edits=edits,
    )


__all__ = [
    "VOLATILE_FIELDS",
    "changed_fields",
    "read_prior",
    "structured_surface_write",
]
