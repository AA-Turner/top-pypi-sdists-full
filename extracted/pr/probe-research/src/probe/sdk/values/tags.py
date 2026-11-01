"""Client-side mirror of the server's canonical tag form (CONTRACT.md "tags").

Lowercase-kebab: NFC, control chars (Cc) become separators, invisible format
chars (Cf: zero-width, BOM) vanish, casefold, inner whitespace -> '-', dedupe
keeping first occurrence. Only the canonical form, never the caps (the server
owns those 422s), so "Baseline" equals "baseline" in the ``tags=`` filter
guard, write verification and the CLI ``tag`` verb.

MIRROR of ``_canonical`` in ``app/core/tags.py``: change both together
(tests/test_tags.py pins the shared vectors).
"""

from __future__ import annotations

import unicodedata
from typing import Iterable


def canonical_tags(tags: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for raw in tags:
        cleaned: list[str] = []
        for ch in unicodedata.normalize("NFC", str(raw)):
            cat = unicodedata.category(ch)
            if cat == "Cc":
                cleaned.append(" ")
            elif cat != "Cf":
                cleaned.append(ch)
        tag = "-".join("".join(cleaned).casefold().split())
        if not tag or tag in seen:
            continue
        seen.add(tag)
        out.append(tag)
    return out
