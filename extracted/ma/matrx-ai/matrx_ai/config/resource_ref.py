"""
Resource reference normalization — the single primitive every list-of-resources
structured input uses to decide *how* an attached item should be resolved.

A client attaches a resource (a note, a task, …) in one of two intents:

  1. **reference** — "include this resource by ID and keep it live." The server
     fetches the current copy from the database every turn (honouring keep_fresh,
     editable tools, ownership checks). This is the default and the normal case.

  2. **snapshot** — "include exactly the content I'm handing you, do not go to
     the database." The server renders the supplied fields verbatim. Useful when
     the caller wants a frozen copy, has no DB record, or deliberately wants to
     avoid a fetch.

Historically each input type expected a bare list of UUID strings
(`note_ids: list[str]`). Real clients send richer shapes — most commonly a list
of *whole resource objects* `{"id": ..., "label": ..., "content": ...}` — which
blew up when fed straight into a `WHERE id = $1` query (the dict was bound as the
UUID). This primitive accepts every shape and reduces each entry to a single
canonical :class:`ResourceRef`, so no resolver ever has to guess again.

Accepted entry shapes (all three valid in the same list):

    "0dbd9901-…"                              -> reference, id="0dbd9901-…"
    {"id": "0dbd9901-…", "label": "…"}        -> reference, id="0dbd9901-…"
    {"mode": "snapshot", "content": "…", …}   -> snapshot, inline=<the dict>

Mode selection rules (in order):

    - explicit mode key  -> "snapshot"/"inline"/"value"/"embedded" => snapshot;
                            "reference"/"live"/"fetch" => reference
    - no mode + usable id                                          => reference
    - no mode + no id + inline content present                     => snapshot
    - otherwise                                                    => unresolvable
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

ReferenceMode = Literal["reference", "snapshot"]

# Keys a dict entry may use to declare its mode, checked in order.
_MODE_KEYS: tuple[str, ...] = ("mode", "attach_mode", "ref_mode")
_SNAPSHOT_VALUES: frozenset[str] = frozenset({"snapshot", "inline", "value", "embedded", "content"})
_REFERENCE_VALUES: frozenset[str] = frozenset({"reference", "live", "fetch", "ref", "id", "by_id"})

# Keys a dict entry may carry its identifier under, checked in order. The first
# is the canonical one; the rest tolerate per-resource naming the clients emit.
_ID_KEYS: tuple[str, ...] = ("id", "note_id", "task_id", "resource_id", "uuid")

# Fields whose presence signals real inline content worth snapshotting when no
# id is available. Generic across resource types.
_INLINE_CONTENT_KEYS: tuple[str, ...] = ("content", "text", "body", "description", "value")


@dataclass(slots=True)
class ResourceRef:
    """One normalized attachment reference.

    - ``id``     — the resolvable identifier, or ``None`` if the entry carried no
      usable id (snapshot-only or malformed).
    - ``mode``   — ``"reference"`` (fetch from DB) or ``"snapshot"`` (use inline).
    - ``inline`` — the original dict for snapshot rendering. Empty for bare-string
      entries.
    """

    id: str | None
    mode: ReferenceMode
    inline: dict[str, Any] = field(default_factory=dict)

    @property
    def has_inline_content(self) -> bool:
        return any(
            isinstance(self.inline.get(k), str) and self.inline.get(k) for k in _INLINE_CONTENT_KEYS
        )


def _extract_id(entry: dict[str, Any]) -> str | None:
    for key in _ID_KEYS:
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _explicit_mode(entry: dict[str, Any]) -> ReferenceMode | None:
    for key in _MODE_KEYS:
        raw = entry.get(key)
        if isinstance(raw, str):
            normalized = raw.strip().lower()
            if normalized in _SNAPSHOT_VALUES:
                return "snapshot"
            if normalized in _REFERENCE_VALUES:
                return "reference"
    return None


def normalize_resource_ref(entry: str | dict[str, Any] | None) -> ResourceRef | None:
    """Reduce a single list entry to a canonical :class:`ResourceRef`.

    Returns ``None`` for entries that carry neither a usable id nor inline
    content (nothing the resolver could ever turn into output).
    """
    if isinstance(entry, str):
        ident = entry.strip()
        return ResourceRef(id=ident, mode="reference") if ident else None

    if isinstance(entry, dict):
        ident = _extract_id(entry)
        explicit = _explicit_mode(entry)

        if explicit == "snapshot":
            mode: ReferenceMode = "snapshot"
        elif explicit == "reference":
            mode = "reference"
        elif ident:
            mode = "reference"
        else:
            # No id and no explicit mode — only resolvable if there's inline
            # content to snapshot.
            mode = "snapshot"

        ref = ResourceRef(id=ident, mode=mode, inline=dict(entry))

        # A snapshot with neither id nor inline content is unresolvable.
        if mode == "snapshot" and not ident and not ref.has_inline_content:
            return None
        # A reference with no id is unresolvable, but fall back to snapshot when
        # the dict happens to carry inline content.
        if mode == "reference" and not ident:
            if ref.has_inline_content:
                ref.mode = "snapshot"
                return ref
            return None
        return ref

    return None


def normalize_resource_refs(
    entries: list[str | dict[str, Any]] | None,
) -> list[ResourceRef]:
    """Normalize a raw client list into canonical refs, dropping unusable ones."""
    if not entries:
        return []
    refs: list[ResourceRef] = []
    for entry in entries:
        ref = normalize_resource_ref(entry)
        if ref is not None:
            refs.append(ref)
    return refs
