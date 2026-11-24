"""THE FILE RULE on the wire: an attached file rides in the person's message it was attached to.

Arman, 2026-11-09 (``common-docs/operations/real-tests/VISION.md`` "Rulings 2026-11-09 morning"):
"small files should always be direct but even large files... unless they're massive or if they're
files that are like a pdf where we have clean text for them". The host (AI Dream
``conversation_context/file_blocks.py``) decides, per turn, which attached files reach the model
whole — the file's text, or a small scanned PDF as the PDF itself — and stages them on
``UnifiedConfig.metadata[CONTEXT_FILE_BLOCKS_KEY]``. It also stamps, on the person turn each file
was first attached to, that file's key (``FILE_BLOCK_HOMES_KEY`` in the stored message metadata).

``place_attached_files`` (one send-boundary step, on the WIRE copy only — the stored history is
never changed, defect 50) puts each staged file in ITS OWN block at the start of its home turn,
opened by the same ``<attachment kind name id/>`` identity label every attachment carries (PB-05
F7/F14). Same file, same turn, same bytes on every send of every later turn, so the file is written
to the prompt cache once and read from it afterwards — never re-sent in the per-turn context block
(REVIEW-C92 #2: a 50k-char file in that block cost ~12.5k uncached tokens per turn, and a tool-loop
turn's kept block carried one more copy per turn).

Placement is total (``place_attached_files``): a host-written turn is a home, a home the history
window cut is replaced by the oldest turn still on the wire (stable while the window holds), and a
list with no user turn gets the file in its own turn at the start — so the value list's note
"Full text in the person's message" never points at nothing (REVIEW-C103 #1, #3, #5).

THE HOMED BLOCK (generic, 2026-11-12). A file is one kind of HOMED block: text delivered whole once,
on its home turn, and replayed byte-identical on every later send. Every placed block carries
``HOMED_BLOCK_MARK`` (files keep ``FILE_BLOCK_MARK`` too), and placement, the order before the
per-turn platform block (``typed_text_last``) and the typed-layout positions key on that mark,
never on ``file_id``. The second kind is a HELD COPY: a host-staged entry
``{"kind": "held_copy", "key", "text", "home", "hash"}`` (``home`` = the home turn's message id;
the host may stamp ``HELD_COPY_HOMES_KEY`` on the turn's metadata instead, as for files). The text
is stored by the host as first rendered and placed as given, after the turn's files, before the
platform block. This package knows nothing about what a held copy holds.

A HELD COPY IS NEVER ORPHANED (2026-11-12, amendment 9). A file whose home the window cut moves to
the oldest kept turn; a held copy does not — the oldest kept turn can be the authored template turn
every conversation of the agent shares. It is left off this send and REPORTED (``off_wire``:
``{"kind", "key", "why": "cut"}``), and so is a homed block the fit step stubbed (``why: "stubbed"``).
An entry may carry ``note`` = ``{"after", "text", "off_wire"}``: the sentence the host's per-turn
block holds about the copy (found after ``after``) and the sentence that replaces it on a send where
the copy is not on the wire (``rewrite_off_wire_notes``), so the per-turn text never claims a copy
the request does not carry. The send boundary stamps the report on the newest person turn's
metadata (``HOMED_OFF_WIRE_KEY``, persisted with the turn) so the host homes a fresh copy next turn.
"""

from __future__ import annotations

from copy import copy
from html import escape
from typing import Any

#: ``UnifiedConfig.metadata`` key (runtime only): this turn's attached files that reach the model
#: whole. Each entry: ``{"key", "file_id", "file_name", "text"}`` for a file's text, or
#: ``{"key", "file_id", "file_name", "mime_type", "native": True}`` for a small scanned PDF sent as
#: the PDF itself.
CONTEXT_FILE_BLOCKS_KEY = "context_file_blocks"
#: Stored person-turn metadata key: the context keys of the attached files whose blocks ride this
#: turn (the turn each was first attached to).
FILE_BLOCK_HOMES_KEY = "attached_file_blocks"
#: Metadata on a placed block, so every later step (and a reader of the stored request) can tell it
#: from the person's own words.
FILE_BLOCK_MARK = "attached_file_block"
#: Metadata on EVERY placed homed block (files and held copies): the entry's key. Delivered once on
#: its home turn, replayed byte-identical; everything that orders or replays homed blocks keys on it.
HOMED_BLOCK_MARK = "homed_block"
#: Entry ``kind`` of a held copy (an entry with no ``kind`` is a file).
HELD_COPY_KIND = "held_copy"
#: Stored person-turn metadata key: the keys of the held copies homed on this turn (the host's
#: alternative to an entry's ``home`` message id).
HELD_COPY_HOMES_KEY = "held_copy_blocks"
#: Stored person-turn metadata key: the homed blocks a send of this turn could not carry whole —
#: ``[{"kind": "held_copy" | "file", "key", "why": "cut" | "stubbed"}]`` (module header).
HOMED_OFF_WIRE_KEY = "homed_blocks_off_wire"


def attachment_label_name(name: Any, ident: Any) -> str | None:
    """The person-facing name for an attachment label, or None. A name that is only the file's id
    plus an extension (``<id>.png``) was made up by storage, not given by a person: never shown, and
    its extension never trusted (it said ``.png`` for a JPEG)."""
    if not isinstance(name, str) or not name.strip():
        return None
    name = name.strip()
    stem = name.rsplit(".", 1)[0] if "." in name else name
    if ident and stem.lower() == str(ident).strip().lower():
        return None
    return name


def label_name_for(metadata: Any, ident: Any) -> str | None:
    """The label name for a media part: its stored ``file_name`` (named at dispatch, saved with the
    part, so turn 1 and every replay read the same one), never a storage-made ``<id>.<ext>``."""
    return attachment_label_name(metadata.get("file_name") if isinstance(metadata, dict) else None, ident)


def file_block_label(entry: dict[str, Any], *, converted_to: str | None = "text") -> str:
    """The ``<attachment .../>`` identity label (the same shape as ``message_config._media_identity_label``)."""
    attrs: dict[str, str] = {"kind": "document"}
    ident = str(entry.get("file_id") or entry.get("key") or "")
    name = attachment_label_name(entry.get("file_name"), entry.get("file_id"))
    if name:
        attrs["name"] = name
    else:
        attrs["name_unavailable"] = "no file name was found for this attachment"
    attrs["id"] = ident
    if converted_to:
        attrs["converted_to"] = converted_to
    rendered = " ".join(f'{k}="{escape(v, quote=True)}"' for k, v in attrs.items())
    return f"<attachment {rendered}/>"


def is_held_copy(entry: Any) -> bool:
    return isinstance(entry, dict) and entry.get("kind") == HELD_COPY_KIND


def held_copy_label(entry: dict[str, Any]) -> str:
    """The ``<held_copy .../>`` identity label: the entry's key, and its label / as-of when given."""
    attrs = {"key": str(entry.get("key") or "")}
    for name in ("label", "as_of"):
        value = entry.get(name)
        if isinstance(value, str) and value.strip():
            attrs[name] = value.strip()
    rendered = " ".join(f'{k}="{escape(v, quote=True)}"' for k, v in attrs.items())
    return f"<held_copy {rendered}/>"


def _blocks_for(entry: dict[str, Any]) -> list[Any]:
    from matrx_ai.config.media_config import DocumentContent
    from matrx_ai.config.unified_content import TextContent

    key = str(entry.get("key") or "")
    if is_held_copy(entry):
        text = entry.get("text")
        if not isinstance(text, str):
            return []
        return [TextContent(text=f"{held_copy_label(entry)}\n{text}", metadata={HOMED_BLOCK_MARK: key})]
    meta = {FILE_BLOCK_MARK: key, HOMED_BLOCK_MARK: key}
    if entry.get("native"):
        doc_meta: dict[str, Any] = dict(meta)
        if isinstance(entry.get("file_name"), str) and entry["file_name"].strip():
            doc_meta["file_name"] = entry["file_name"].strip()
        return [
            DocumentContent(
                file_id=str(entry["file_id"]),
                mime_type=str(entry.get("mime_type") or "application/pdf"),
                metadata=doc_meta,
            )
        ]
    text = entry.get("text")
    if not isinstance(text, str):
        return []
    return [TextContent(text=f"{file_block_label(entry)}\n{text}", metadata=meta)]


def is_file_block(block: Any) -> bool:
    """True for a block this step placed (a file's text or a scanned PDF), never the person's own."""
    metadata = getattr(block, "metadata", None)
    return isinstance(metadata, dict) and bool(metadata.get(FILE_BLOCK_MARK))


def is_homed_block(block: Any) -> bool:
    """True for any block ``place_attached_files`` placed (a file or a held copy), never the
    person's own. Ordering and replay key on this, never on ``file_id``."""
    metadata = getattr(block, "metadata", None)
    return isinstance(metadata, dict) and bool(metadata.get(HOMED_BLOCK_MARK))


def is_file_home(message: Any) -> bool:
    """Whether ``message`` can carry a file's block: a user-role turn written by the person OR by the
    host (a ``run_mandate`` host turn, ``ai.agent.start``, an inbox wake: REVIEW-C103 #1 — a run with
    only host-written turns must still receive its file), that carries no tool result (nothing may
    precede a tool result in a user turn: Anthropic refuses it, REVIEW-C103 #5) and is not the
    platform's own per-send turn (``HOST_TURN_KEY`` / ``REPLAYED_TURN_KEY``: rebuilt every send)."""
    from matrx_ai.config.tools_config import ToolResultContent
    from matrx_ai.config.typed_text_last import HOST_TURN_KEY, REPLAYED_TURN_KEY

    role = getattr(message, "role", None)
    if str(getattr(role, "value", role) or "").lower() != "user":
        return False
    metadata = getattr(message, "metadata", None) or {}
    if isinstance(metadata, dict) and (metadata.get(HOST_TURN_KEY) or metadata.get(REPLAYED_TURN_KEY)):
        return False
    return not any(isinstance(c, ToolResultContent) for c in getattr(message, "content", None) or [])


def _is_authored(message: Any) -> bool:
    from matrx_ai.config.cache_marks import TEMPLATE_METADATA_KEY

    metadata = getattr(message, "metadata", None)
    return isinstance(metadata, dict) and bool(metadata.get(TEMPLATE_METADATA_KEY))


def few_shot_indexes(messages: Any) -> set[int]:
    """Indexes of the agent's authored few-shot EXAMPLE exchanges: an authored template user turn
    answered by an authored template assistant turn (never a prefill), and that answer. A file
    placed there reads to the model as part of the example (REVIEW-C110 minor 3), so neither is
    ever a file's home. The authored turn her own words fill is answered by a real reply, so it
    stays a home."""
    from matrx_ai.config.message_flags import flags_of

    listed = list(messages or [])
    out: set[int] = set()
    for index in range(len(listed) - 1):
        user, answer = listed[index], listed[index + 1]
        role = getattr(user, "role", None)
        answer_role = getattr(answer, "role", None)
        if (
            str(getattr(role, "value", role) or "").lower() == "user"
            and str(getattr(answer_role, "value", answer_role) or "").lower() == "assistant"
            and _is_authored(user)
            and _is_authored(answer)
            and not flags_of(answer).get("prefill")
        ):
            out.update((index, index + 1))
    return out


def newest_file_home(messages: Any) -> Any:
    """The turn a newly attached file is homed on (the host stamps its key there): the newest
    ``is_file_home`` message that is not a few-shot example, or ``None``."""
    listed = list(messages or [])
    examples = few_shot_indexes(listed)
    return next(
        (m for i, m in reversed(list(enumerate(listed))) if i not in examples and is_file_home(m)), None
    )


def place_attached_files(
    messages: list[Any], entries: list[dict[str, Any]] | None, *, off_wire: list[dict[str, Any]] | None = None
) -> list[Any] | None:
    """``messages`` with every staged file block at the start of its home turn, or ``None`` when
    nothing is staged. The input list and its messages are never mutated.

    Placement is TOTAL — a staged file always reaches the wire (the host already told the model,
    in the value list, where its text is):

    1. its home: the ``is_file_home`` turn whose stored metadata names its key (the turn it was
       first attached to; host-written turns count);
    Never an authored few-shot example turn (``few_shot_indexes``).

    2. a home the history window or compaction cut: the OLDEST ``is_file_home`` turn still on the
       wire — the same message on every send while the window holds, so the file stays inside the
       cached prefix instead of moving to each new person turn (REVIEW-C103 #3);
    3. no such turn at all: its own user turn at the start of the list, right after the agent's
       leading few-shot examples (never after a tool result).

    Held copies (``HELD_COPY_KIND``) follow the same three rules; their home is the turn whose
    ``id`` is the entry's ``home`` or whose metadata names the key (``HELD_COPY_HOMES_KEY``), with
    ONE difference: a held copy whose home is not on the wire is never moved (rules 2 and 3) — it is
    left off this send and appended to ``off_wire`` (module header). In a home turn files come
    first, then held copies, each kind in the order staged.
    """
    staged = [
        e for e in entries or []
        if isinstance(e, dict) and e.get("key") and (e.get("file_id") or is_held_copy(e))
    ]
    if not staged:
        return None
    by_key = {str(e["key"]): e for e in staged}
    home_ids = {str(e["home"]): str(e["key"]) for e in staged if is_held_copy(e) and e.get("home")}
    placed: set[str] = set()
    homes: dict[int, list[str]] = {}
    oldest: int | None = None
    examples = few_shot_indexes(messages)
    for index, message in enumerate(messages):
        if index in examples or not is_file_home(message):
            continue
        if oldest is None:
            oldest = index
        metadata = getattr(message, "metadata", None) or {}
        keys = (
            [*(metadata.get(FILE_BLOCK_HOMES_KEY) or []), *(metadata.get(HELD_COPY_HOMES_KEY) or [])]
            if isinstance(metadata, dict)
            else []
        )
        message_id = getattr(message, "id", None)
        if message_id and str(message_id) in home_ids:
            keys.append(home_ids[str(message_id)])
        for key in keys:
            if key in by_key and key not in placed:
                homes.setdefault(index, []).append(key)
                placed.add(key)
    orphans = [key for key in by_key if key not in placed]
    for key in [k for k in orphans if is_held_copy(by_key[k])]:
        orphans.remove(key)
        if off_wire is not None:
            off_wire.append({"kind": HELD_COPY_KIND, "key": key, "why": "cut"})
    out = list(messages)
    if orphans and oldest is not None:
        homes.setdefault(oldest, []).extend(orphans)
        orphans = []
    for index, keys in homes.items():
        keys = sorted(keys, key=lambda k: is_held_copy(by_key[k]))  # files first, stable within a kind
        blocks = [block for key in keys for block in _blocks_for(by_key[key])]
        if not blocks:
            continue
        twin = copy(out[index])
        twin.content = [*blocks, *list(getattr(out[index], "content", None) or [])]
        out[index] = twin
    if orphans:
        from matrx_ai.config.message_config import UnifiedMessage

        orphans = sorted(orphans, key=lambda k: is_held_copy(by_key[k]))
        blocks = [block for key in orphans for block in _blocks_for(by_key[key])]
        if blocks:
            own = UnifiedMessage(role="user", content=blocks)
            own.metadata = {FILE_BLOCK_MARK: "own_turn", HOMED_BLOCK_MARK: "own_turn"}
            # First turn after the agent's leading few-shot examples (none: the very start), so
            # the authored prefix stays shared and the file is never read as an example.
            at = 0
            while at in examples:
                at += 1
            out.insert(at, own)
    return out


def homed_block_kind(block: Any) -> str:
    """``"file"`` or ``"held_copy"`` for a placed homed block (the report's ``kind``)."""
    return "file" if is_file_block(block) else HELD_COPY_KIND


def rewrite_off_wire_notes(messages: list[Any], entries: list[dict[str, Any]] | None, off_wire: list[dict[str, Any]]) -> list[Any] | None:
    """``messages`` with the per-turn block's sentence about each off-wire copy replaced by its
    ``off_wire`` sentence (module header), or ``None`` when nothing changed. Only the NEWEST
    platform block (this send's) is rewritten, on a copied message and block — an earlier turn's
    replayed block and the stored history are never touched. Every ``off_wire`` record gets
    ``note_rewritten``: True, or False when the entry gave no sentence or it was not found."""
    from matrx_ai.config.typed_text_last import TURN_CONTEXT_MARK

    by_key = {str(e.get("key")): e for e in entries or [] if isinstance(e, dict) and e.get("key")}
    where: tuple[int, int] | None = None
    for i in range(len(messages) - 1, -1, -1):
        content = list(getattr(messages[i], "content", None) or [])
        for j in range(len(content) - 1, -1, -1):
            text = getattr(content[j], "text", None)
            if isinstance(text, str) and text.startswith(TURN_CONTEXT_MARK):
                where = (i, j)
                break
        if where is not None:
            break
    changed = False
    text = None
    if where is not None:
        text = messages[where[0]].content[where[1]].text
    for record in off_wire:
        note = (by_key.get(str(record.get("key"))) or {}).get("note")
        record["note_rewritten"] = False
        if text is None or not isinstance(note, dict):
            continue
        after, said, instead = note.get("after"), note.get("text"), note.get("off_wire")
        if not all(isinstance(v, str) and v for v in (after, said, instead)):
            continue
        start = text.find(after)
        at = text.find(said, start) if start >= 0 else -1
        if at < 0:
            continue
        text = text[:at] + instead + text[at + len(said):]
        record["note_rewritten"] = changed = True
    if not changed or where is None:
        return None
    out = list(messages)
    message = copy(out[where[0]])
    content = list(getattr(message, "content", None) or [])
    block = copy(content[where[1]])
    block.text = text
    content[where[1]] = block
    message.content = content
    out[where[0]] = message
    return out


__all__ = [
    "CONTEXT_FILE_BLOCKS_KEY",
    "FILE_BLOCK_HOMES_KEY",
    "FILE_BLOCK_MARK",
    "HELD_COPY_HOMES_KEY",
    "HELD_COPY_KIND",
    "HOMED_BLOCK_MARK",
    "HOMED_OFF_WIRE_KEY",
    "file_block_label",
    "held_copy_label",
    "homed_block_kind",
    "is_file_block",
    "is_file_home",
    "is_held_copy",
    "is_homed_block",
    "newest_file_home",
    "place_attached_files",
    "rewrite_off_wire_notes",
]
