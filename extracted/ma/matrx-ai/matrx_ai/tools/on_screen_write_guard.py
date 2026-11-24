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
  ``{envelope: resource_ref, resource_type: "note", resource_id}``. Any surface
  that declares the same pair is guarded with no code here
  (``aidream.services.conversation_context.surface_context``).
* WHICH tools — every server tool/action the write census classifies as a
  surface write (``SURFACE_WRITE_TOOLS`` ∪ ``STRUCTURED_WRITE_TOOLS``; the census
  guard proves that list complete). Reads, creates and removals are untouched.
* WHICH calls — a call whose arguments (at any depth) name a guarded record id.
  Ids are UUIDs, so one flat set serves every resource family without collision
  (the same reasoning as ``config.read_only_resources``).

A guarded write that is one exact anchored edit on a [patchable] target, while the
page offers ``apply_surface_write`` this turn, IS sent to the person as that approval
card: the executor delegates the same edit to ``apply_surface_write`` under the same
call id (``on_screen_surface_redirect``), so the right call never comes back as a
failed one (Q-05, 2026-11-10). Any other guarded write is refused with a tool result
naming the reason and the right door (``apply_surface_write``). After the person DECLINES an
``apply_surface_write`` in the turn, the refusal says so instead: nothing may
write that record another way in the same turn.

Client-delegated tools are not guarded here — ``apply_surface_write`` itself is
one, and it is the door.
"""

from __future__ import annotations

import json
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
    """The census key (``tool`` or ``tool:action``) when this call is a surface write.

    The census is keyed by the name a tool is declared under in code; a call arriving under a
    rename alias (the DB's old name during a rename window) maps to it first.
    """
    from matrx_ai.tools.declared import code_name_for

    tool_name = code_name_for(tool_name)
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


def _guarded_hit(
    tool_name: str,
    arguments: Mapping[str, Any] | None,
    metadata: Mapping[str, Any] | None,
) -> tuple[str, str, Mapping[str, Any]] | None:
    """``(writer_key, record_id, record)`` when this server call writes an on-screen record."""
    records = (metadata or {}).get(ON_SCREEN_RECORDS_KEY)
    if not records:
        return None
    key = writer_key(tool_name, arguments)
    if key is None:
        return None
    for text in _strings(dict(arguments or {})):
        candidate = text.strip().lower()
        if candidate in records:
            return key, candidate, records[candidate]
    return None


def on_screen_surface_redirect(
    tool_name: str,
    arguments: Mapping[str, Any] | None,
    metadata: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    """The ``apply_surface_write`` arguments that ARE this server write, when it can go to the card.

    Q-05 (2026-11-10, conversation 12c200b3): the model's ``note`` patch on the note open
    on screen was the right edit, yet it came back as a failed tool call and the model had
    to repeat it through ``apply_surface_write``. A right call must succeed the first time,
    so the executor sends this same edit to the person as the approval card in place of the
    server write (``ToolExecutor`` on-screen block). None — and the refusal stands — when the
    person declined a change this turn, or the call is not one exact anchored edit on a
    [patchable] target (a whole rewrite, a many-match edit, no patchable target).
    """
    if (metadata or {}).get(ON_SCREEN_DECLINED_KEY):
        return None
    hit = _guarded_hit(tool_name, arguments, metadata)
    if hit is None:
        return None
    if not _is_only_an_edit_of_its_subject(tool_name, arguments, hit[1]):
        return None
    ready, _note = _ready_surface_call(arguments, hit[2])
    return ready


#: The top-level argument that names the record a server writer changes (its SUBJECT), per tool.
#: A tool not listed here names it in a top-level ``id`` or ``*_id`` argument.
_SUBJECT_KEYS: dict[str, tuple[str, ...]] = {
    "note": ("note_id",),
    "data": ("id",),
    "document": ("document_id", "id"),
}


def _subject_keys(tool_name: str, args: Mapping[str, Any]) -> tuple[str, ...]:
    from matrx_ai.tools.declared import code_name_for

    declared = _SUBJECT_KEYS.get(code_name_for(tool_name))
    if declared is not None:
        return declared
    return tuple(k for k in args if k == "id" or k.endswith("_id"))


def _is_only_an_edit_of_its_subject(
    tool_name: str, arguments: Mapping[str, Any] | None, record_id: str
) -> bool:
    """True when the call is exactly "this find/replace on the on-screen record", nothing more.

    REVIEW-C105: the redirect turned ANY census writer carrying a find/replace pair and the
    on-screen id anywhere in its arguments into the card, silently dropping every other
    argument (a title, a regex or case flag, another field), and a call on ANOTHER record
    that merely mentioned the on-screen id became a card patching it. The card must be the
    call the model made, so the redirect happens only when (1) the on-screen id is the call's
    own top-level SUBJECT and (2) the find/replace pair is the only edit-bearing argument.
    Anything else keeps the refusal, which names the door and the shape.
    """
    args = arguments or {}
    subject = next(
        (
            k
            for k in _subject_keys(tool_name, args)
            if isinstance(args.get(k), str) and args[k].strip().lower() == record_id
        ),
        None,
    )
    if subject is None:
        return False
    pair = next(
        ((f, r) for f, r in _ANCHORED_EDIT_PAIRS if isinstance(args.get(f), str) and args.get(f)),
        None,
    )
    if pair is None:
        return False
    allowed = {*_DISPATCH_FIELDS, subject, *pair, "resource_type", *_MANY_MATCH_KEYS}
    # A key sent as null carries nothing (models often echo optional fields as null).
    return all(key in allowed or args[key] is None for key in args)


def guarded_write_refusal(
    tool_name: str,
    arguments: Mapping[str, Any] | None,
    metadata: Mapping[str, Any] | None,
) -> tuple[str, str] | None:
    """``(error_type, message)`` when this server call writes an on-screen record, else None."""
    found = _guarded_hit(tool_name, arguments, metadata)
    if found is None:
        return None
    key, hit, record = found
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
    #
    # Q-05 (2026-11-09, conversation 7f041c85): an agent told "if the patch
    # fails, say so and stop" read the old "Refused: ... cannot change it" as a
    # failed patch and stopped, so the person never got the approval card. The
    # refusal states FACTS only (review C74: a tool result never tells the model
    # to set aside its operator's instructions): this was not a failed edit, the
    # change can go to the person as an approval card, and — when the refused
    # call carried one anchored edit and the record has a [patchable] target —
    # the ready call for that same edit on that target.
    ready, note = _ready_surface_call(arguments, record)
    lead = (
        f"Not a failed edit: this {kind} ({hit}) is open on the person's screen, and edits to an open "
        f"{kind} are made through the page, where the person approves them on a card. "
    )
    if ready:
        body = (
            f"This same edit, as that approval card: {SURFACE_WRITE_DOOR} "
            f"{json.dumps(ready, ensure_ascii=False)}. "
            "It is the same patch (one exact str_replace), not an update or a rewrite. "
            f"Nothing was changed yet; {key} does not write a {kind} that is open on screen."
        )
    else:
        body = (
            f"The door is {door}. Nothing was changed yet; {key} does not write a {kind} that is open "
            "on screen. "
            + (
                note
                or "For a small edit the value is the edit, not the whole text: "
                '{"command": "str_replace", "old_str": "<exact text now there, unique>", '
                '"new_str": "<replacement>"}.'
            )
        )
    return ON_SCREEN_ERROR_TYPE, lead + body


#: Argument pairs a server writer uses for an anchored edit: (find, replace).
_ANCHORED_EDIT_PAIRS: tuple[tuple[str, str], ...] = (
    ("search_text", "replacement_text"),
    ("old_str", "new_str"),
    ("old_text", "new_text"),
    ("find", "replace"),
    ("search", "replace"),
)

#: Arguments asking for more than one match. The page's anchored edit replaces
#: EXACTLY one match (``surface-write-patch.ts``: "Must match exactly once"), so a
#: call carrying one of these is never handed back as a single str_replace.
_MANY_MATCH_KEYS: tuple[str, ...] = ("replace_all", "all_occurrences", "occurrence", "occurrences", "count")

#: Suggested-action line the executor attaches to a ``record_on_screen`` refusal (facts only).
ON_SCREEN_SUGGESTED_ACTION = (
    "apply_surface_write sends this change to the person as an approval card."
)


def _asks_many(args: Mapping[str, Any]) -> bool:
    for key in _MANY_MATCH_KEYS:
        value = args.get(key)
        if value is True:
            return True
        if key != "replace_all" and isinstance(value, (int, str)) and not isinstance(value, bool):
            if str(value).strip().lower() not in ("", "1", "first"):
                return True
    return False


def _ready_surface_call(
    arguments: Mapping[str, Any] | None, record: Mapping[str, Any]
) -> tuple[dict[str, Any] | None, str | None]:
    """``(ready_call, note)`` for the refused edit: the ``apply_surface_write`` arguments.

    The ready call names the record's [patchable] target — the one that takes an
    anchored edit — never simply its first target (a title target listed first
    would turn a body edit into a title write). No patchable target, no anchored
    pair, or a many-match edit: no ready call; ``note`` says why when it matters.
    """
    args = arguments or {}
    pair = next(
        (
            (args.get(f), args.get(r))
            for f, r in _ANCHORED_EDIT_PAIRS
            if isinstance(args.get(f), str) and args.get(f) and isinstance(args.get(r), str)
        ),
        None,
    )
    if pair is None:
        return None, None
    patchable = [str(t) for t in record.get("patchable_targets") or () if t]
    if not patchable:
        return None, None
    if _asks_many(args):
        return None, (
            f"The page's edit replaces exactly one match: for several places, one {SURFACE_WRITE_DOOR} "
            f'per place on target {patchable[0]}, value {{"command": "str_replace", "old_str": '
            '"<text unique to that place>", "new_str": "<replacement>"}.'
        )
    old, new = pair
    call = {
        "target": patchable[0],
        "value": {"command": "str_replace", "old_str": old, "new_str": new},
    }
    return call, None
