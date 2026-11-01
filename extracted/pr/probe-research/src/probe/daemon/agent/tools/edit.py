"""the edit tool: replace the one place `old` appears in a checked-out draft."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from probe.daemon.store.events import scrub


# ---------------------------------------------------------------------------
# edit: an exact find-and-replace in a checked-out draft.
# ---------------------------------------------------------------------------

#: Lines of context around an edit in its answer.
EDIT_CONTEXT_LINES = 3


def _within(path: Path, root: Path) -> bool:
    """Is `path` strictly inside `root`? Without case on a file system that
    ignores it (macOS, Windows: `realpath` keeps the spelling it was given),
    exactly elsewhere -- on Linux a folder spelled with other case is another
    folder."""
    if sys.platform == "darwin" or os.name == "nt":
        inner, outer = str(path).casefold(), str(root).casefold().rstrip(os.sep)
        return inner.startswith(outer + os.sep)
    return path != root and path.is_relative_to(root)


def _draft_roots() -> list[Path]:
    """The folders `edit` may change files in: the note and summary checkouts
    (`folders.note_dirs`, without the team note, whose every change the
    researcher sees first)."""
    from probe.daemon.session.session import note_dirs

    return [Path(os.path.realpath(str(d))) for d in note_dirs()[:2]]


async def edit_file(deps: Deps, path: str, old: str, new: str) -> str:
    """Replace the one place `old` appears in a checked-out draft with `new`.
    Refused: a path outside the note and summary draft folders (or a link
    out of them), Probe's bookkeeping beside a draft (`.base`, `.meta.json`,
    `.lock`, `.owner`), an `old` that is empty, missing or not unique. Answers
    with the changed lines and `EDIT_CONTEXT_LINES` around them. The file's
    mode is kept (drafts are 0600)."""
    from probe.daemon import shell as sh
    from probe.foundation.durable.durable import write_text_atomic

    stop = write_refusal(deps)
    if stop is not None:
        return stop
    raw = (path or "").strip()
    if not raw or "\0" in raw:
        return "not edited: give the draft's path"
    full = Path(os.path.expanduser(raw))
    full = full if full.is_absolute() else deps.cwd / full
    real = Path(os.path.realpath(str(full)))
    roots = _draft_roots()
    if not any(_within(real, root) for root in roots):
        return ("not edited: `edit` changes only a checked-out summary or note draft (the path a `probe "
                f"summary checkout` or `probe notes checkout` printed, under {', '.join(map(str, roots))})")
    if sh.is_bookkeeping(real.name) or sh.is_bookkeeping(full.name):
        return "not edited: that file is Probe's own record of the checkout, never edited"
    if not real.is_file():
        return f"not edited: {raw} does not exist; check the summary out first"
    if not old:
        return "not edited: `old` is empty; copy the exact text to replace from the draft"
    text = await asyncio.to_thread(real.read_text, encoding="utf-8")
    count = text.count(old)
    if count == 0:
        return (f"not edited: `old` is not in {raw}. `read` the part you mean to change (offset/limit) and "
                "copy it exactly, spaces and line breaks included")
    if count > 1:
        return (f"not edited: `old` appears {count} times in {raw}; include more of the text around it so it "
                "matches once")
    at = text.index(old)
    changed = text[:at] + new + text[at + len(old):]
    mode = real.stat().st_mode & 0o777
    await asyncio.to_thread(write_text_atomic, real, changed, mode=mode)
    first = text.count("\n", 0, at)
    last = first + new.rstrip("\n").count("\n")
    lines = changed.split("\n")
    if lines and lines[-1] == "" and changed.endswith("\n"):
        lines.pop()  # the file's final newline ends a line; it starts none
    lo, hi = max(0, first - EDIT_CONTEXT_LINES), min(len(lines), last + EDIT_CONTEXT_LINES + 1)
    shown = "\n".join(f"{n + 1:>6}\t{lines[n]}" for n in range(lo, hi))
    answer = scrub(f"edited {raw} (lines {first + 1}-{last + 1}):\n{shown}")
    deps.store.log_lookup(bite=deps.bite_id, tool="edit", query=str(real), result=answer[:2000])
    return answer
from probe.daemon.agent.tools.refusals import write_refusal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps  # noqa: E402 -- pieces need each other; the front door loads this one first
