"""The proof of a record change is the store's outbox row — never an event's payload.

LANE 11 ROUND 3 (2026-10-02). ``authenticated`` may INSERT ``workflow.trigger_event`` (any
column, payload included) for a trigger it edits, so a payload proves nothing about what
changed. ``custom.io_outbox`` is written only by the store's own trigger in the same
transaction as the write; ``authenticated`` holds no INSERT/UPDATE/SELECT on it (measured on
the clone, 2026-10-02). So a store-trigger fire:

1. reads the outbox row named by the event's ``change_id`` through the SERVER's reader
   (host-injected — this package never reads ``custom`` itself);
2. checks it is a ``records.changed`` row of the trigger's organization and table, with an
   operation and changed fields the trigger watches;
3. BUILDS the run's ``trigger`` input from that row alone (ids + the record's new version),
   ignoring everything else the payload says.

No matching row → the event is refused with a sentence and no run is created.

The reader is injected by the host with :func:`configure_store_change_reader`; it returns
the outbox row as a plain dict ``{id, event_key, organization_id, table_id, record_id,
operation, changed_field_ids, metadata, actor}`` or None. Unconfigured, every store change
is refused (fails closed).
"""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from typing import Any

StoreChangeReader = Callable[[str], Awaitable[dict[str, Any] | None]]

_reader: StoreChangeReader | None = None

#: The outbox event key a record change is written under.
RECORD_CHANGED_EVENT_KEY = "records.changed"

#: A store trigger's event verb → the outbox operations it accepts.
_EVENT_OPERATIONS: dict[str, frozenset[str]] = {
    "record.created": frozenset({"created"}),
    "record.updated": frozenset({"updated"}),
    "record.archived": frozenset({"deleted"}),
    "record.matches": frozenset({"created", "updated"}),
    # A form answer and a booking are a created record that came through that door
    # (``metadata.change.via`` on the outbox row, chairdoors4_b): the verb names the door.
    "form.answered": frozenset({"created"}),
    "booking.made": frozenset({"created"}),
}

#: The door words a change event carries as ``metadata.change.via`` (chairdoors4_b): the three
#: doors that mark themselves, then who wrote when none did.
CHANGE_VIA_WORDS: frozenset[str] = frozenset({"form", "booking", "import", "agent", "api", "person"})

#: A store trigger's event verb → the ``via`` the change must carry, when the verb names a door.
_EVENT_VIA: dict[str, frozenset[str]] = {
    "form.answered": frozenset({"form"}),
    "booking.made": frozenset({"booking"}),
}


def via_of(row: dict[str, Any]) -> str | None:
    """The door a change came through, from ``metadata.change.via`` on its outbox row (None on a
    row written before the store said)."""
    metadata = _json(row.get("metadata")) or {}
    change_meta = metadata.get("change") if isinstance(metadata, dict) else None
    via = change_meta.get("via") if isinstance(change_meta, dict) else None
    return str(via) if via else None


class StoreChangeRefused(Exception):
    """A store-trigger event that no real record change backs. Dead-letter, never retry."""


def configure_store_change_reader(reader: StoreChangeReader | None) -> None:
    """Host wiring: how the server reads one ``custom.io_outbox`` row by id."""
    global _reader
    _reader = reader


def _json(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return value
    return value


async def read_store_change(change_id: str) -> dict[str, Any] | None:
    if _reader is None:
        raise StoreChangeRefused(
            "this server cannot read the store's change feed (no reader configured), so it "
            "cannot prove a record changed — nothing was run."
        )
    if not change_id:
        return None
    return await _reader(str(change_id))


#: Said on a change whose outbox row carries no chain: the emitter wrote it outside any
#: workflow run, so it starts a chain of its own.
CHAIN_ABSENT = "no workflow chain on this change: depth 0"


def chain_of(row: dict[str, Any]) -> dict[str, Any]:
    """The loop chain a change carries, from ``actor.chain`` on its outbox row.

    Shape the emitter writes: ``{"root_run": "<uuid of the first run>", "depth": <int >= 0>}``.
    Absent → ``{"root_run": None, "depth": 0, "said": CHAIN_ABSENT}`` (said, never guessed).
    Present but malformed → refused: a loop guard that cannot read the depth must not run.
    """
    actor = _json(row.get("actor")) or {}
    chain = actor.get("chain") if isinstance(actor, dict) else None
    if chain is None:
        return {"root_run": None, "depth": 0, "said": CHAIN_ABSENT}
    chain = _json(chain)
    depth = chain.get("depth") if isinstance(chain, dict) else None
    root = chain.get("root_run") if isinstance(chain, dict) else None
    if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0 or not root:
        raise StoreChangeRefused(
            f"change {row.get('id')} carries a workflow chain this server cannot read "
            f"({chain!r}); expected {{root_run, depth}} — nothing was run."
        )
    return {"root_run": str(root), "depth": depth}


def change_from_outbox(row: dict[str, Any]) -> dict[str, Any]:
    """The run's ``trigger`` input, built from the outbox row alone.

    Reads: ``id`` (uuid), ``record_id`` (uuid), ``table_id`` (uuid), ``operation`` (text),
    ``changed_field_ids`` (jsonb array of field-id strings), ``metadata.change.version``
    (int — the record's version after the change) and ``actor.chain`` (:func:`chain_of`).
    """
    metadata = _json(row.get("metadata")) or {}
    change_meta = metadata.get("change") if isinstance(metadata, dict) else None
    version = change_meta.get("version") if isinstance(change_meta, dict) else None
    changed = _json(row.get("changed_field_ids")) or []
    return {
        "change_id": str(row["id"]),
        "record_id": str(row.get("record_id")) if row.get("record_id") else None,
        "table_id": str(row.get("table_id")) if row.get("table_id") else None,
        "operation": row.get("operation"),
        "changed_field_ids": [str(f) for f in changed if f],
        "new_version": int(version) if isinstance(version, int) else None,
        "chain": chain_of(row),
        "via": via_of(row),
    }


def refusal_for(trigger: Any, row: dict[str, Any] | None, change_id: str) -> str | None:
    """Why this outbox row does not back a fire of this trigger, or None when it does."""
    if row is None:
        return (
            f"no record change {change_id or '(none named)'} exists in the store's change feed, "
            "so this event is not a real change — nothing was run."
        )
    spec = getattr(trigger, "event_source", None) or {}
    if row.get("event_key") != RECORD_CHANGED_EVENT_KEY:
        return f"change {change_id} is not a record change — nothing was run."
    if str(row.get("organization_id") or "") != str(getattr(trigger, "organization_id", "") or ""):
        return f"change {change_id} belongs to another organization — nothing was run."
    if str(row.get("table_id") or "") != str(spec.get("table_id") or ""):
        return f"change {change_id} is in another table than this trigger watches — nothing was run."
    operation = row.get("operation")
    allowed = _EVENT_OPERATIONS.get(str(spec.get("event") or ""), frozenset())
    if operation not in allowed:
        return f"change {change_id} ({operation}) is not the kind of change this trigger watches."
    operations = [str(o) for o in spec.get("operations") or []]
    if operations and operation not in operations:
        return f"change {change_id} ({operation}) is not one of this trigger's operations."
    # THE DOOR THE CHANGE CAME THROUGH (chairdoors4_b): the verb's own door first (form.answered
    # takes only `form`, booking.made only `booking`), then any `via` list the spec names.
    via = via_of(row)
    wanted = set(_EVENT_VIA.get(str(spec.get("event") or ""), frozenset()))
    wanted |= {str(v) for v in spec.get("via") or []}
    if wanted and via not in wanted:
        return (f"change {change_id} came through {via or 'an unmarked door'}, not "
                f"{' or '.join(sorted(wanted))} — not the kind of change this trigger watches.")
    watched = {str(f) for f in spec.get("field_ids") or []}
    changed = {str(f) for f in (_json(row.get("changed_field_ids")) or [])}
    if watched and operation == "updated" and not (watched & changed):
        return f"change {change_id} touched none of the fields this trigger watches."
    return None


async def verified_store_change(trigger: Any, change_id: str) -> dict[str, Any]:
    """The run input for a real change backing this trigger. Raises StoreChangeRefused."""
    row = await read_store_change(change_id)
    refusal = refusal_for(trigger, row, change_id)
    if refusal is not None:
        raise StoreChangeRefused(refusal)
    assert row is not None
    return change_from_outbox(row)


__all__ = [
    "CHAIN_ABSENT",
    "CHANGE_VIA_WORDS",
    "chain_of",
    "via_of",
    "RECORD_CHANGED_EVENT_KEY",
    "StoreChangeReader",
    "StoreChangeRefused",
    "change_from_outbox",
    "configure_store_change_reader",
    "read_store_change",
    "refusal_for",
    "verified_store_change",
]
