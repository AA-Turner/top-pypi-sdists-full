# LIFTED from legacy hugpy (read-only reference):
#   model_key_forms   <- py/foundation/hugpy_platform/src/hugpy_platform/model_keys.py:8-22 (verbatim)
#   canonical_key     <- py/inference/hugpy_engine/src/hugpy_engine/fit/types.py:53-60 (verbatim)
#   _canon_forms, serveable_match <- py/fleet/hugpy_fleet/src/hugpy_fleet/central/workers.py:3724,3762
# DROPPED: the blocked-sibling guard in serveable_match (no blocklist here).
"""Model-key identity: alias forms and the one membership predicate routing uses."""
from __future__ import annotations

import re
from typing import Any


def model_key_forms(model_key: Any) -> set[str]:
    """Return the raw key, case variants, and its ``/`` and ``~`` tails."""
    if not model_key:
        return set()
    raw = str(model_key).strip()
    forms = {raw, raw.lower()}
    # A native-wrapper unit id is ``key::variation``: the id names the model
    # ``key`` served through one of its files, so the head's forms are the
    # model's. A bare-key request therefore matches any advertised variation;
    # the exact id still matches first in serveable_match.
    if "::" in raw:
        head = raw.split("::", 1)[0].strip()
        if head:
            forms |= model_key_forms(head)
    tail = raw.split("/")[-1]
    forms.add(tail)
    forms.add(tail.lower())
    if "~" in raw:
        base = raw.split("~", 1)[1]
        if base:
            forms.add(base)
            forms.add(base.lower())
    return forms


# Case is not a name token (the routing alias union already folds it); the
# separator before the suffix may be ``-`` or ``_`` (``Qwen3.8_4B_Distilled_GGUF``
# is a live key) — nothing else is folded.
_FORMAT_SUFFIX_RE = re.compile(r"[-_]gguf$", re.IGNORECASE)


def canonical_key(model_key: Any) -> str:
    """``model_key`` with ONLY the trailing format suffix (``-GGUF``) removed.
    Every other token is identity and is kept verbatim."""
    s = str(model_key or "").strip()
    return _FORMAT_SUFFIX_RE.sub("", s, count=1)


def _canon_forms(forms) -> set:
    """The alias forms of a key reduced to their canonical identity (lower-cased,
    ``-GGUF`` stripped) — the set two keys must intersect on to be ONE model."""
    return {canonical_key(f).lower() for f in (forms or ()) if f}


def _owner(key: Any) -> "str | None":
    """The owner qualifier of ``owner~name`` / ``owner/name`` (lowercased), else None."""
    k = str(key or "").strip()
    for sep in ("~", "/"):
        if sep in k:
            o = k.split(sep, 1)[0].strip().lower()
            return o or None
    return None


def serveable_match(model_key: str, wanted: set, serveable) -> bool:
    """True iff one of ``serveable``'s advertised keys names ``model_key``."""
    want_c = _canon_forms(wanted)
    owner = _owner(model_key)
    for m in serveable:
        if m == model_key:
            return True
        # An OWNER-QUALIFIED request (``owner~name`` / ``owner/name``) is identity:
        # the wrapper qualifies a name only when two different models collide on
        # it, so a box advertising the bare name (or another owner's) holds a
        # DIFFERENT model — never credited (2026-10-05: stabilityai~sd-turbo was
        # routed to ae's bare comfy sd-turbo every other call).
        if owner is not None:
            mo = _owner(m)
            if mo is None or mo != owner:
                continue
        # Alias match = the "~"/"/"-tail union (k67) OR the ``-GGUF`` format
        # equivalence (operator rule 2026-09-29). Both are IDENTITY: nothing
        # here ever matches a key carrying an extra name token (``-Distill``,
        # a quant marker…), so a worker holding ``X-Distill-GGUF`` is never
        # credited with ``X-GGUF`` — not as resident, allocated, or on-disk.
        if (wanted & model_key_forms(m)) or (want_c & _canon_forms(model_key_forms(m))):
            return True
    return False
