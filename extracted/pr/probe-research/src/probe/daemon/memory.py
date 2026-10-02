"""The researcher's agent memory index, read-only (T3).

The daemon keeps no memory of its own. It reads the coding agent's: the
harness's own memory index (its MEMORY.md, as the adapter lists it), shown
scrubbed in a fresh start's prompt (`Worker.memory_block`: a bite's in bites
mode, a conversation's first message in conversation mode). The files the index
names stay on demand (the shell reads them).
"""

from __future__ import annotations

from pathlib import Path

from probe.daemon.store import scrub

#: The name of a harness's memory index file.
MAIN = "MEMORY.md"
#: The researcher's agent memory index shown in a request, at most this many characters.
AGENT_INDEX_CHARS = 6_000


def agent_memory_index(paths: list[Path], *, limit: int = AGENT_INDEX_CHARS) -> list[tuple[Path, str]]:
    """The researcher's own agent memory indexes (a harness's MEMORY.md, as its
    adapter lists it): `(path, scrubbed text)`, each at most `limit` characters.
    The files an index names stay on demand (the shell reads them)."""
    out: list[tuple[Path, str]] = []
    for path in paths:
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                text = handle.read(limit + 1)
        except OSError:
            continue
        text = scrub(text).strip()
        if not text:
            continue
        if len(text) > limit:
            text = text[:limit] + f"\n[... more: cat {path}]"
        out.append((path, text))
    return out
