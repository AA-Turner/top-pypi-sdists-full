"""MODEL PRIORITY GROUPS — the operator's EXPLICIT, ORDERED fallback list.

WHAT THIS IS, AND WHAT IT IS NOT
-------------------------------
A *priority group* is a hand-written, ORDERED list of model keys. When a request
names ANY member of an enabled group, resolution walks that list IN THE
OPERATOR'S ORDER and routes the FIRST member that is actually usable right now.
Nothing is inferred, nothing is derived, nothing is guessed.

Contrast with ``managers/resolvers/groups.py`` (*model groups*, 2026-07-28),
which DERIVES membership by stripping packaging/quant suffixes off a repo name
("Qwen2.5-VL-7B-Instruct-GGUF" -> group "qwen2.5-vl-7b-instruct") and then picks
a member by a ranking pipeline (quality/speed/priority ticks, ladder walk, fit).
That feature is heuristic BOTH in who is in a group AND in which member wins.
It is off by default (settings ``model_groups.enabled``, default FALSE) and it
stays off unless an operator turns it on.

    THIS module is the EXPLICIT one, and it OUTRANKS the derived one. If a
    requested key belongs to an enabled priority group, the operator's ordering
    is the answer and the derivation pipeline is never consulted for that key.
    (Operator directive 2026-08-06: "not grouped by default" — an ordering the
    operator did not write is not an ordering they consented to.)

A BLOCK IS NEVER LAUNDERED
--------------------------
A blocked member is SKIPPED, never served. A group can only reorder which
candidate is tried; it can never make a blocked model reachable. When no member
of the group is usable, resolution returns "change nothing" and the originally
requested key fails exactly as it fails today — the group must not invent a new
error, and must not mask the old one.

PERSISTENCE
-----------
The F4 runtime settings store (``comms.settings.settings_store``), namespace
``model_priority_groups``, keyed by group id. That store is
``$PROJECTS_HOME/settings.json``: fcntl-locked read-modify-write, atomic
``os.replace``, thread-safe (an RLock), with a short read cache — the same
mechanism ``comms/blocklist.py`` uses for ``models.blocked``. No new storage
mechanism is introduced, and there is exactly ONE write path (this module), so
the operator gate on ``/llm/model-groups`` mutations is the only gate to get
right.

RECORD SHAPE
------------
    {"id": str,             # slug, the settings key
     "name": str,           # operator-facing label
     "members": [str, ...], # ORDERED model keys — the whole point
     "enabled": bool,
     "created_at": float, "updated_at": float, "by": str}

MATCHING is alias-tolerant, mirroring ``workers._match_keys``: a registry key
qualifies a base name with its owner via "~" ("Qwen~Qwen2.5-VL-7B-Instruct")
while the operator, the hub and the workers all routinely say the bare name
("Qwen2.5-VL-7B-Instruct"). Those spellings must intersect or a group written in
the obvious way would silently never fire. Suffixes are NEVER stripped here:
"Qwen2.5-VL-7B-Instruct" and "Qwen2.5-VL-7B-Instruct-GGUF" are two DIFFERENT
members that the operator listed in a deliberate order, and conflating them is
precisely the implicit behaviour this module exists to replace.
"""
from __future__ import annotations

import logging
import re
import time
from typing import Any, Dict, List, Optional, Tuple

from .settings import settings_store

logger = logging.getLogger(__name__)

# Settings namespace for the explicit group registry (group_id -> record).
NS = "model_priority_groups"

_SLUG_RE = re.compile(r"[^a-z0-9]+")


# ---------------------------------------------------------------------------
# Key matching
# ---------------------------------------------------------------------------
def key_forms(model_key: Any) -> set:
    """The spellings ``model_key`` may legitimately be named by.

    Deliberately the SAME rule as ``workers._match_keys``: raw, lowercased, the
    "/"-tail (hub_id -> repo name) and the "~"-tail (registry key -> bare base).
    Deliberately NOT ``resolvers.groups.base_name``: that one strips ``-GGUF``
    and quant tokens, which would merge the operator's two ordered members into
    one and destroy the ordering they asked for."""
    s = str(model_key or "").strip()
    if not s:
        return set()
    forms = {s, s.lower()}
    tail = s.split("/")[-1]
    forms.add(tail)
    forms.add(tail.lower())
    if "~" in s:
        base = s.split("~", 1)[1]
        if base:
            forms.add(base)
            forms.add(base.lower())
    return forms


def keys_match(a: Any, b: Any) -> bool:
    """True when ``a`` and ``b`` are two spellings of the same model."""
    fa, fb = key_forms(a), key_forms(b)
    return bool(fa and fb and (fa & fb))


def slugify(text: Any, fallback: str = "group") -> str:
    s = _SLUG_RE.sub("-", str(text or "").strip().lower()).strip("-")
    return s or fallback


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------
def _normalize(gid: str, raw: Any) -> Optional[dict]:
    """A stored value -> a well-formed record, or None when unusable.

    Tolerant on read (a hand-edited settings.json must not take the feature
    down) and strict on write (``validate``)."""
    if not isinstance(raw, dict):
        return None
    members: List[str] = []
    for m in (raw.get("members") or []):
        m = str(m or "").strip()
        # Order-preserving de-dup: a repeated member is a typo, not a second
        # chance — walking it twice would just print the same skip reason twice.
        if m and not any(keys_match(m, seen) for seen in members):
            members.append(m)
    return {
        "id": str(gid),
        "name": str(raw.get("name") or gid),
        "members": members,
        "enabled": bool(raw.get("enabled", True)),
        "created_at": raw.get("created_at"),
        "updated_at": raw.get("updated_at"),
        "by": raw.get("by") or "operator",
    }


# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------
def all_groups() -> List[dict]:
    """Every stored group, normalized, sorted by name then id. Never raises."""
    try:
        raw = settings_store.all(NS) or {}
    except Exception as exc:  # noqa: BLE001 — a read must never break a caller
        logger.warning("priority groups: read failed (%s) — no groups", exc)
        return []
    out = []
    for gid, rec in raw.items():
        norm = _normalize(str(gid), rec)
        if norm is not None:
            out.append(norm)
    out.sort(key=lambda g: (str(g.get("name") or "").lower(), g["id"]))
    return out


def get_group(group_id: Any) -> Optional[dict]:
    gid = str(group_id or "").strip()
    if not gid:
        return None
    try:
        return _normalize(gid, settings_store.get(NS, gid))
    except Exception as exc:  # noqa: BLE001
        logger.warning("priority groups: read failed for %s (%s)", gid, exc)
        return None


def enabled_groups() -> List[dict]:
    return [g for g in all_groups() if g.get("enabled")]


def group_for_key(model_key: Any, groups: Optional[List[dict]] = None
                  ) -> Optional[dict]:
    """The ENABLED group that lists ``model_key`` (alias-tolerant), or None.

    "At most one enabled group per key" is enforced on write (``validate``), so
    a first-match walk here is deterministic. If a hand-edited store ever breaks
    that invariant this returns the first by the stable sort order and logs it,
    rather than refusing to route."""
    groups = enabled_groups() if groups is None else [
        g for g in groups if g.get("enabled")]
    hits = [g for g in groups
            if any(keys_match(model_key, m) for m in (g.get("members") or []))]
    if len(hits) > 1:
        logger.warning(
            "priority groups: %s is claimed by %d enabled groups (%s) — using "
            "%s; fix the overlap, membership is meant to be exclusive",
            model_key, len(hits), [g["id"] for g in hits], hits[0]["id"])
    return hits[0] if hits else None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate(group_id: str, name: Any, members: Any, enabled: Any,
             groups: Optional[List[dict]] = None) -> Tuple[list, list]:
    """``(clean_members, errors)``. ``errors`` empty means the write is legal.

    THE ONE STRUCTURAL RULE: a model key may appear in AT MOST ONE ENABLED
    group. Two enabled groups claiming the same key would make resolution depend
    on iteration order, i.e. on nothing an operator can see. Conflicts are
    REPORTED with the offending key and the group that already holds it — never
    silently resolved by dropping a member (that would quietly rewrite the
    operator's list).

    A DISABLED group may overlap freely: it routes nothing, and staging a
    replacement group next to the live one is a legitimate thing to want."""
    errors: List[str] = []
    gid = str(group_id or "").strip()
    if not gid:
        errors.append("id is required")
    if not str(name or "").strip():
        errors.append("name is required")

    clean: List[str] = []
    if not isinstance(members, (list, tuple)):
        errors.append("members must be a list of model keys, in priority order")
        members = []
    for m in members:
        m = str(m or "").strip()
        if not m:
            continue
        if any(keys_match(m, seen) for seen in clean):
            errors.append(f"duplicate member {m!r} — a member may be listed once")
            continue
        clean.append(m)
    if not clean:
        errors.append("members must contain at least one model key")

    if bool(enabled):
        others = [g for g in (all_groups() if groups is None else groups)
                  if g.get("enabled") and g["id"] != gid]
        for m in clean:
            for og in others:
                if any(keys_match(m, om) for om in (og.get("members") or [])):
                    errors.append(
                        f"{m!r} is already a member of the enabled group "
                        f"{og['id']!r} ({og.get('name')}) — a model key may be "
                        f"in at most one enabled group")
    return clean, errors


# ---------------------------------------------------------------------------
# Writes
# ---------------------------------------------------------------------------
def put_group(group_id: Any, *, name: Any, members: Any, enabled: Any = True,
              by: Optional[str] = None) -> Tuple[Optional[dict], list]:
    """Create or REPLACE a group. ``(record, errors)``; record is None on error.

    Replace rather than merge: ``members`` is an ORDER, and a partial update of
    an order is not a thing that has a meaning. ``PATCH`` in the route layer
    reads the current record, applies the patch, and calls this — so there is
    still exactly one validated write path."""
    gid = slugify(group_id or name)
    clean, errors = validate(gid, name, members, enabled)
    if errors:
        return None, errors
    prior = get_group(gid) or {}
    now = time.time()
    rec = {
        "id": gid,
        "name": str(name).strip(),
        "members": clean,
        "enabled": bool(enabled),
        "created_at": prior.get("created_at") or now,
        "updated_at": now,
        "by": by or "operator",
    }
    settings_store.set(NS, gid, rec)
    logger.info("priority group %s: members=%s enabled=%s (by=%s)",
                gid, clean, rec["enabled"], rec["by"])
    return rec, []


def delete_group(group_id: Any) -> bool:
    gid = str(group_id or "").strip()
    if not gid:
        return False
    existed = settings_store.delete(NS, gid)
    if existed:
        logger.info("priority group deleted: %s", gid)
    return bool(existed)
