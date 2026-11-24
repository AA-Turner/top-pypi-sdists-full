"""The one-graph migration of notes and frames: ``metadata.annotations`` / ``metadata.groups`` -> information nodes.

One-graph CONTRACTS §2.5. Pure functions over a stored definition document (a dict with ``nodes``,
``edges``, ``metadata``; any other key is carried untouched), so the same code serves a draft, a
published version and a template, and the rehearsal can run on a copy of every live row.

* ``migrate_document`` — a sticky note (``type: "annotation"``) becomes ``type: "info"`` with
  ``data.spec_type = "info.note"``; a frame (``type: "group"``) becomes an ``info.frame`` and every
  member (step or note) is re-parented by ``parentId``; ``data.memberIds`` is dropped (it was a save-time
  projection of ``parentId``). Positions stay as stored: the stored document keeps ABSOLUTE positions
  (the canvas flattens on the way out and re-parents on the way in), and ``SetParentOp`` leaves them
  alone. Only a ``metadata`` key that CARRIED content is removed; an empty list stays, because an empty
  key was always part of the hash and a hash must not move.
* ``restore_document`` — the exact inverse (frames back to ``metadata.groups`` with ``memberIds``,
  notes back to ``metadata.annotations``), so the migration is reversible and round-trip identity is a test.
* ``normalized_legacy`` — what a legacy document means once the cases the canvas already ignores on load
  are applied (a member that no longer exists, a step claimed by a second frame, a frame left empty).
  The round trip is identity against this form. ``memberIds`` order carries no meaning (the canvas derives it
at save time from its node order, ``graph-canvas/src/groups.ts``), so both sides list it sorted.

A document the migration cannot carry faithfully raises ``MigrationRefused`` (an id used twice, a note that
is not a note, a frame inside a frame): the apply script reports and skips it, never guesses.
"""

from __future__ import annotations

import copy
from typing import Any, NamedTuple

from matrx_graph.information import FRAME_SPEC_TYPE, INFO_NODE_TYPE, LEGACY_PRESENTATION_KEYS

NOTE_SPEC_TYPE = "info.note"
ANNOTATION_TYPE = "annotation"
GROUP_TYPE = "group"


class MigrationRefused(ValueError):
    """A document the migration will not touch, with the reason."""


class Migrated(NamedTuple):
    document: dict[str, Any]
    changed: bool
    notes: int
    frames: int
    #: frames with no live member: the canvas drops these on load, so they are not carried.
    empty_frames_dropped: int
    #: members named by a second frame (the first frame wins, as the canvas loads them).
    claims_ignored: int


def has_legacy_content(document: dict[str, Any]) -> bool:
    meta = document.get("metadata") or {}
    return any(isinstance(meta.get(k), list) and len(meta[k]) > 0 for k in LEGACY_PRESENTATION_KEYS)


def _list(meta: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = meta.get(key)
    return [e for e in value if isinstance(e, dict)] if isinstance(value, list) else []


def migrate_document(document: dict[str, Any]) -> Migrated:
    """A copy of ``document`` with its notes and frames as information nodes (``changed`` False and the
    document returned as it came when it carries none)."""
    if not has_legacy_content(document):
        return Migrated(document, False, 0, 0, 0, 0)
    doc = copy.deepcopy(document)
    meta = doc.setdefault("metadata", {})
    nodes: list[dict[str, Any]] = list(doc.get("nodes") or [])
    annotations = _list(meta, "annotations")
    groups = _list(meta, "groups")

    seen: set[str] = set()
    for entry in (*nodes, *annotations, *groups):
        eid = entry.get("id")
        if not isinstance(eid, str) or not eid:
            raise MigrationRefused("an entry has no id")
        if eid in seen:
            raise MigrationRefused(f"id '{eid}' is used twice across nodes, notes and frames")
        seen.add(eid)

    notes: list[dict[str, Any]] = []
    for a in annotations:
        if a.get("type") != ANNOTATION_TYPE:
            raise MigrationRefused(f"note '{a['id']}' has type {a.get('type')!r}, not 'annotation'")
        if "parentId" in a:
            raise MigrationRefused(f"note '{a['id']}' already has a parentId")
        a["type"] = INFO_NODE_TYPE
        a["data"] = {**(a.get("data") or {}), "spec_type": NOTE_SPEC_TYPE}
        notes.append(a)

    carriers = {n["id"]: n for n in (*nodes, *notes)}
    frames: list[dict[str, Any]] = []
    dropped = ignored = 0
    for g in groups:
        if g.get("type") != GROUP_TYPE:
            raise MigrationRefused(f"frame '{g['id']}' has type {g.get('type')!r}, not 'group'")
        data = dict(g.get("data") or {})
        member_ids = data.pop("memberIds", None) or []
        live: list[str] = []
        for mid in member_ids:
            if mid not in carriers:
                continue  # a member deleted elsewhere: the canvas skips it on load
            if "parentId" in carriers[mid]:
                ignored += 1  # claimed by an earlier frame: first wins
                continue
            live.append(mid)
        if not live:
            dropped += 1
            continue
        for mid in live:
            carriers[mid]["parentId"] = g["id"]
        g["type"] = INFO_NODE_TYPE
        g["data"] = {**data, "spec_type": FRAME_SPEC_TYPE}
        frames.append(g)

    doc["nodes"] = [*frames, *nodes, *notes]
    for key in LEGACY_PRESENTATION_KEYS:
        if isinstance(meta.get(key), list) and meta[key]:
            del meta[key]
    return Migrated(doc, True, len(notes), len(frames), dropped, ignored)


def _is_spec(node: dict[str, Any], spec_type: str) -> bool:
    return node.get("type") == INFO_NODE_TYPE and (node.get("data") or {}).get("spec_type") == spec_type


def restore_document(document: dict[str, Any]) -> dict[str, Any]:
    """The inverse of ``migrate_document``: notes and frames back into ``metadata``. A document with
    neither comes back as it came."""
    nodes: list[dict[str, Any]] = list(document.get("nodes") or [])
    frame_ids = {n["id"] for n in nodes if _is_spec(n, FRAME_SPEC_TYPE)}
    note_ids = {n["id"] for n in nodes if _is_spec(n, NOTE_SPEC_TYPE)}
    if not frame_ids and not note_ids:
        return document
    doc = copy.deepcopy(document)
    nodes = list(doc["nodes"])
    for n in nodes:
        if n["id"] in frame_ids and n.get("parentId") is not None:
            raise MigrationRefused(f"frame '{n['id']}' sits inside a frame; the old shape cannot hold that")
    members: dict[str, list[str]] = {fid: [] for fid in frame_ids}
    steps: list[dict[str, Any]] = []
    annotations: list[dict[str, Any]] = []
    groups: list[dict[str, Any]] = []
    for n in nodes:
        parent = n.get("parentId")
        if n["id"] in frame_ids:
            continue
        if parent in frame_ids:
            members[parent].append(n["id"])
            del n["parentId"]
        if n["id"] in note_ids:
            data = dict(n.get("data") or {})
            data.pop("spec_type", None)
            n["type"] = ANNOTATION_TYPE
            n["data"] = data
            annotations.append(n)
        else:
            steps.append(n)
    for n in nodes:
        if n["id"] in frame_ids:
            data = dict(n.get("data") or {})
            data.pop("spec_type", None)
            data["memberIds"] = sorted(members[n["id"]])
            n["type"] = GROUP_TYPE
            n["data"] = data
            groups.append(n)
    doc["nodes"] = steps
    meta = doc.setdefault("metadata", {})
    if annotations:
        meta["annotations"] = [*_list(meta, "annotations"), *annotations]
    if groups:
        meta["groups"] = [*_list(meta, "groups"), *groups]
    return doc


def normalized_legacy(document: dict[str, Any]) -> dict[str, Any]:
    """``document`` as the canvas reads it on load: a ``memberIds`` entry naming nothing is skipped, a
    step named by two frames stays with the first, a frame left with no member is dropped. Written
    independently of ``migrate_document`` so the round-trip test compares two readings of the data."""
    doc = copy.deepcopy(document)
    meta = doc.get("metadata") or {}
    groups = _list(meta, "groups")
    if not groups:
        return doc
    ids = {n.get("id") for n in doc.get("nodes") or []} | {a.get("id") for a in _list(meta, "annotations")}
    claimed: set[str] = set()
    kept: list[dict[str, Any]] = []
    for g in groups:
        data = g.get("data") or {}
        live = [m for m in data.get("memberIds") or [] if m in ids and m not in claimed]
        claimed.update(live)
        if live:
            g["data"] = {**data, "memberIds": sorted(live)}
            kept.append(g)
    if kept:
        meta["groups"] = kept
    else:
        del meta["groups"]
    return doc


def census_of(document: dict[str, Any]) -> tuple[int, int]:
    """(notes, frames) still carried in ``metadata`` — the census the apply drives to zero."""
    meta = document.get("metadata") or {}
    return len(_list(meta, "annotations")), len(_list(meta, "groups"))
