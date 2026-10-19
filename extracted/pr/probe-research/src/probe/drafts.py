"""An exact, find-and-replace change to a checked-out summary or note draft.

One rule, two doors: the daemon writer's `edit` tool (the classic tool set,
`daemon/tools.edit_file`) and `probe draft edit <path>` (everyone's CLI, and the
daemon's `bash`, which answers it in its own process). Only a file inside the
note and summary checkout folders (`daemon.folders.note_dirs`, the team note's
left out: the researcher sees each of its changes first), never Probe's own
bookkeeping beside a draft (`.base`, `.meta.json`, `.lock`, `.owner`), and the
old text must be found exactly once. On macOS and Windows a path is compared
without case (`within`), as the edit tool always did.

The change arrives on stdin, in a form a quoted heredoc carries as it is
(`EDIT_FORMAT`):

    probe draft edit <path> <<'EOF'
    <<<<<<< OLD
    the text as it is now, copied exactly
    ======= NEW
    what replaces it
    >>>>>>> END
    EOF

Lines in between are taken whole; the marker lines are not part of either text.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from probe._compat import StrEnum

OLD_MARK = "<<<<<<< OLD"
NEW_MARK = "======= NEW"
END_MARK = ">>>>>>> END"
EDIT_FORMAT = f"{OLD_MARK}\n<old text>\n{NEW_MARK}\n<new text>\n{END_MARK}"
#: Lines of context around an edit in its answer.
CONTEXT_LINES = 3


class Refusal(StrEnum):
    NO_PATH = "no_path"
    OUTSIDE = "outside"
    BOOKKEEPING = "bookkeeping"
    MISSING = "missing"
    EMPTY_OLD = "empty_old"
    NOT_FOUND = "not_found"
    MANY = "many"
    FORMAT = "format"


@dataclass
class Refused(Exception):
    kind: Refusal
    count: int = 0  # how many times `old` was found (MANY)
    detail: str = ""

    def __str__(self) -> str:  # pragma: no cover -- each door words its own refusals
        return f"{self.kind}: {self.detail}"


def within(path: Path, root: Path) -> bool:
    """Is `path` strictly inside `root`? Without case on a file system that
    ignores it (macOS, Windows: `realpath` keeps the spelling it was given),
    exactly elsewhere -- on Linux a folder spelled with other case is another
    folder."""
    if sys.platform == "darwin" or os.name == "nt":
        inner, outer = str(path).casefold(), str(root).casefold().rstrip(os.sep)
        return inner.startswith(outer + os.sep)
    return path != root and path.is_relative_to(root)


def draft_roots() -> list[Path]:
    """The folders a draft may be changed in: the note and summary checkouts."""
    from probe.daemon.folders import note_dirs

    return [Path(os.path.realpath(str(d))) for d in note_dirs()[:2]]


def resolve(raw: str, cwd: Path) -> Path:
    """The draft `raw` names (from `cwd`), resolved; Refused when it is not one."""
    from probe.daemon.shell import is_bookkeeping

    raw = (raw or "").strip()
    if not raw or "\0" in raw:
        raise Refused(Refusal.NO_PATH)
    full = Path(os.path.expanduser(raw))
    full = full if full.is_absolute() else cwd / full
    real = Path(os.path.realpath(str(full)))
    if not any(within(real, root) for root in draft_roots()):
        raise Refused(Refusal.OUTSIDE)
    if is_bookkeeping(real.name) or is_bookkeeping(full.name):
        raise Refused(Refusal.BOOKKEEPING)
    if not real.is_file():
        raise Refused(Refusal.MISSING)
    return real


def replace_once(real: Path, old: str, new: str, shown: str) -> str:
    """Replace the one place `old` appears in `real` with `new`; the answer
    names the changed lines (numbered) with CONTEXT_LINES around them. The
    file's mode is kept (drafts are 0600)."""
    from probe.sdk.durable import write_text_atomic

    if not old:
        raise Refused(Refusal.EMPTY_OLD)
    text = real.read_text(encoding="utf-8")
    count = text.count(old)
    if count == 0:
        raise Refused(Refusal.NOT_FOUND)
    if count > 1:
        raise Refused(Refusal.MANY, count=count)
    at = text.index(old)
    changed = text[:at] + new + text[at + len(old):]
    mode = real.stat().st_mode & 0o777
    write_text_atomic(real, changed, mode=mode)
    first = text.count("\n", 0, at)
    last = first + new.rstrip("\n").count("\n")
    lines = changed.split("\n")
    if lines and lines[-1] == "" and changed.endswith("\n"):
        lines.pop()  # the file's final newline ends a line; it starts none
    lo, hi = max(0, first - CONTEXT_LINES), min(len(lines), last + CONTEXT_LINES + 1)
    numbered = "\n".join(f"{n + 1:>6}\t{lines[n]}" for n in range(lo, hi))
    return f"edited {shown} (lines {first + 1}-{last + 1}):\n{numbered}"


def parse_change(stdin: str) -> tuple[str, str]:
    """`(old, new)` from the stdin form (`EDIT_FORMAT`); Refused(FORMAT) when it
    is not that form. A final newline after the END line is allowed."""
    lines = stdin.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if len(lines) < 3 or lines[0] != OLD_MARK or lines[-1] != END_MARK:
        raise Refused(Refusal.FORMAT, detail="the first line must read exactly "
                                             f"{OLD_MARK!r} and the last {END_MARK!r}")
    middle = lines[1:-1]
    marks = [k for k, line in enumerate(middle) if line == NEW_MARK]
    if len(marks) != 1:
        raise Refused(Refusal.FORMAT, detail=f"exactly one line must read {NEW_MARK!r} (found {len(marks)})")
    k = marks[0]
    return "\n".join(middle[:k]), "\n".join(middle[k + 1:])


#: What `probe draft edit` answers when it changes nothing (NEW wording,
#: tests/fixtures/daemon_prompts/tools/draft-edit.NEW.md).
EDIT_REFUSED: dict[Refusal, str] = {
    Refusal.NO_PATH: "not edited: give the draft's path: probe draft edit <path>",
    Refusal.OUTSIDE: ("not edited: `probe draft edit` changes only a draft `probe summary checkout` or `probe notes "
                      "checkout` printed (under {roots})"),
    Refusal.BOOKKEEPING: "not edited: that file is Probe's own record of the checkout, never edited",
    Refusal.MISSING: "not edited: {raw} does not exist; check the summary out first",
    Refusal.EMPTY_OLD: "not edited: the OLD part is empty; copy the text to replace from the draft",
    Refusal.NOT_FOUND: ("not edited: the OLD text is not in {raw}. Print that part (`sed -n '40,60p' {raw}`) and "
                        "copy it exactly, spaces and line breaks included"),
    Refusal.MANY: "not edited: the OLD text appears {count} times in {raw}; add text around it so it matches once",
    Refusal.FORMAT: "not edited: the change goes on stdin, as\n{format}\n({detail})",
}


def edit(raw: str, stdin: str | None, cwd: Path) -> tuple[int, str]:
    """`probe draft edit <raw>` with `stdin`: (exit code, what it prints)."""
    try:
        real = resolve(raw, cwd)
        old, new = parse_change(stdin or "")
        return 0, replace_once(real, old, new, raw.strip())
    except Refused as refused:
        text = EDIT_REFUSED[refused.kind].format(
            raw=(raw or "").strip(), count=refused.count, detail=refused.detail, format=EDIT_FORMAT,
            roots=", ".join(map(str, draft_roots())))
        return 1, text
