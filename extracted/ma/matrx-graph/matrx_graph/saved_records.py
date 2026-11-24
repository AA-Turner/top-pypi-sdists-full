"""What a step saved: the record ids every save inside one invocation wrote (G4, 2026-11-01).

A save step notes the rows it wrote with :func:`note_saved_records` (table, ids). The scheduler opens a
tally for each invocation (a ContextVar, the same shape as the spend tally in ``spend_gate``), and when
a For each item settles its ``item_settled`` event carries that tally, so a screen shows each item's
rows as they land instead of waiting for the whole list.

A tally opened INSIDE another one (a called workflow running inline in an item, or any nested
invocation) hands its ids to the outer tally when it closes, so an item's event names everything its
whole branch saved, however deep the save sat. Outside a workflow invocation there is no tally and a
note costs nothing.
"""

from __future__ import annotations

from collections.abc import Iterable
from contextvars import ContextVar, Token

#: table → ids, in the order they were written (duplicates kept once).
SavedRecords = dict[str, list[str]]

_TALLY: ContextVar[SavedRecords | None] = ContextVar("matrx_graph_saved_records", default=None)


def open_saved_records() -> tuple[SavedRecords, Token[SavedRecords | None]]:
    """Start the tally of one invocation. Close it with :func:`close_saved_records`."""
    tally: SavedRecords = {}
    return tally, _TALLY.set(tally)


def close_saved_records(tally: SavedRecords, token: Token[SavedRecords | None]) -> None:
    """End one invocation's tally; an outer tally (the item this invocation runs inside) receives its ids."""
    _TALLY.reset(token)
    outer = _TALLY.get()
    if outer is not None and outer is not tally:
        for table, ids in tally.items():
            _merge(outer, table, ids)


def note_saved_records(table: str, ids: Iterable[str | None]) -> None:
    """A save wrote these rows of ``table``. Empty ids (an element left unwritten) are not counted."""
    tally = _TALLY.get()
    if tally is None or not table:
        return
    _merge(tally, str(table), ids)


def current_saved_records() -> SavedRecords:
    """A copy of the tally the current invocation holds (empty outside one)."""
    tally = _TALLY.get()
    return {table: list(ids) for table, ids in (tally or {}).items()}


def _merge(tally: SavedRecords, table: str, ids: Iterable[str | None]) -> None:
    kept = tally.setdefault(table, [])
    seen = set(kept)
    for value in ids:
        if value is None or value == "":
            continue
        text = str(value)
        if text not in seen:
            seen.add(text)
            kept.append(text)
    if not kept:
        tally.pop(table, None)


__all__ = [
    "SavedRecords",
    "close_saved_records",
    "current_saved_records",
    "note_saved_records",
    "open_saved_records",
]
