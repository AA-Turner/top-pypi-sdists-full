"""THE ON-SCREEN WRITE GUARD — a record the person has open is changed only through its page.

W-60 (production, 2026-10-01 11:02–11:04Z, conversation ceba31ec…): the page
agent proposed a note change through ``apply_surface_write`` (target
``note_content``, apply policy "ask"), the person declined it on the approval
card, and 104 seconds later — in the SAME turn — the agent wrote the same change
into the same note through the server ``note`` tool (action ``patch``). The note
changed with no approval. The person's confirmation was only as strong as the
weakest write path to the record on their screen.

Ruling (destructive-and-expensive-actions + "a screen never lies"): a write to
the record the person has on screen goes through the surface's approval,
whatever tool the model chooses. The server is where every write path meets, so
it is enforced HERE, in the tool executor, for every server-side surface writer:

* WHICH records — a surface write target that is LIVE this turn (the page
  registered a handler; ``resolve_live_write_targets``) and declares
  ``updates_value`` naming a surface value that carries a record reference
  (``resource_ref`` / a bare ``*_file_id``-style id). Notes:
  ``note_content.updates_value = "current_note"`` and ``current_note`` is
  ``{__kind: resource_ref, resource_type: "note", resource_id}``. Any surface
  that declares the same pair is guarded with no code here
  (``aidream.services.conversation_context.surface_context``).
* WHICH tools — every server tool/action the write census classifies as a
  surface write (``SURFACE_WRITE_TOOLS`` ∪ ``STRUCTURED_WRITE_TOOLS``; the census
  guard proves that list complete). Reads, creates and removals are untouched.
* WHICH calls — a call whose arguments (at any depth) name a guarded record id.
  Ids are UUIDs, so one flat set serves every resource family without collision
  (the same reasoning as ``config.read_only_resources``).

A guarded write is refused with a tool result naming the reason and the right
door (``apply_surface_write``). After the person DECLINES an
``apply_surface_write`` in the turn, the refusal says so instead: nothing may
write that record another way in the same turn.

Client-delegated tools are not guarded here — ``apply_surface_write`` itself is
one, and it is the door.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from matrx_ai.tools.surface_write import STRUCTURED_WRITE_TOOLS, SURFACE_WRITE_TOOLS

#: AppContext.metadata key: ``{record_id: {"resource_type", "surface", "targets"}}``.
ON_SCREEN_RECORDS_KEY = "on_screen_write_records"
#: AppContext.metadata key: True once the person declined an
#: ``apply_surface_write`` in the current turn.
ON_SCREEN_DECLINED_KEY = "on_screen_write_declined"

SURFACE_WRITE_DOOR = "apply_surface_write"
PERSON_DECLINED_STATUS = "declined_by_person"
ON_SCREEN_ERROR_TYPE = "record_on_screen"
DECLINED_ERROR_TYPE = "person_declined_this_change"

_DISPATCH_FIELDS = ("action", "command", "op", "operation")
_WRITER_KEYS: frozenset[str] = frozenset(SURFACE_WRITE_TOOLS) | frozenset(STRUCTURED_WRITE_TOOLS)


def arm_on_screen_write_guard(
    metadata: dict[str, Any] | None,
    records: Mapping[str, Mapping[str, Any]] | None,
    *,
    declined: bool | None = None,
) -> None:
    """Replace this turn's guarded records on the shared ``AppContext.metadata``.

    Rebuilt from the surface scope on every turn (launch, continue, resume), so a
    plain replace is correct and an empty set clears the key — a record the
    person closed is never guarded by a stale entry. ``declined`` is set only
    when the caller knows it (the resume path reads the turn's ledger).
    """
    if metadata is None:
        return
    clean = {str(k).lower(): dict(v) for k, v in (records or {}).items() if k}
    if clean:
        metadata[ON_SCREEN_RECORDS_KEY] = clean
    else:
        metadata.pop(ON_SCREEN_RECORDS_KEY, None)
    if declined is not None:
        if declined:
            metadata[ON_SCREEN_DECLINED_KEY] = True
        else:
            metadata.pop(ON_SCREEN_DECLINED_KEY, None)


def output_is_person_decline(output: Any) -> bool:
    """True when a stored/returned tool output is the person's "keep as is"."""
    if isinstance(output, Mapping):
        return output.get("status") == PERSON_DECLINED_STATUS or output.get("declined") is True
    if isinstance(output, str) and PERSON_DECLINED_STATUS in output:
        import json

        try:
            parsed = json.loads(output)
        except ValueError:
            return False
        return isinstance(parsed, Mapping) and output_is_person_decline(parsed)
    return False


def writer_key(tool_name: str, arguments: Mapping[str, Any] | None) -> str | None:
    """The census key (``tool`` or ``tool:action``) when this call is a surface write."""
    args = arguments or {}
    for field in _DISPATCH_FIELDS:
        value = args.get(field)
        if isinstance(value, str) and value:
            key = f"{tool_name}:{value.strip()}"
            return key if key in _WRITER_KEYS else None
    return tool_name if tool_name in _WRITER_KEYS else None


def _strings(value: Any, depth: int = 0) -> Iterable[str]:
    if depth > 6:
        return
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for item in value.values():
            yield from _strings(item, depth + 1)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item, depth + 1)


def guarded_write_refusal(
    tool_name: str,
    arguments: Mapping[str, Any] | None,
    metadata: Mapping[str, Any] | None,
) -> tuple[str, str] | None:
    """``(error_type, message)`` when this server call writes an on-screen record, else None."""
    records = (metadata or {}).get(ON_SCREEN_RECORDS_KEY)
    if not records:
        return None
    key = writer_key(tool_name, arguments)
    if key is None:
        return None
    hit: str | None = None
    for text in _strings(dict(arguments or {})):
        candidate = text.strip().lower()
        if candidate in records:
            hit = candidate
            break
    if hit is None:
        return None
    record = records[hit]
    kind = str(record.get("resource_type") or "record")
    targets = [str(t) for t in record.get("targets") or () if t]
    door = (
        f"{SURFACE_WRITE_DOOR} (target {', '.join(targets)})" if targets else SURFACE_WRITE_DOOR
    )
    if (metadata or {}).get(ON_SCREEN_DECLINED_KEY):
        return (
            DECLINED_ERROR_TYPE,
            f"Refused: the person declined a change to this {kind} ({hit}) in this turn. "
            f"Nothing was changed. Do not write it with {key} or any other tool. "
            "Tell the person it was left as it was, or ask what they want instead.",
        )
    # Keep a SMALL edit small (2026-10-01): redirected from a server patch, the
    # model used to resend the whole note as the surface value. A text target
    # that is [patchable] takes the anchored edit the frontend seam resolves
    # (``surface-write-patch.ts``), so the redirect names that shape.
    return (
        ON_SCREEN_ERROR_TYPE,
        f"Refused: this {kind} ({hit}) is open on the person's screen, so {key} cannot change it "
        f"directly. Nothing was changed. Propose the change with {door} so they can confirm it. "
        "For a small edit send the edit, not the whole text: value "
        '{"command": "str_replace", "old_str": "<exact text now there, unique>", '
        '"new_str": "<replacement>"}.',
    )
