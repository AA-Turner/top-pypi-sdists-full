"""read a command's words: options vs names, GNU long-option abbreviations, canonical path spellings."""

from __future__ import annotations
import os
from typing import Sequence
from probe.daemon.shell.parse import _Word
from probe.daemon.shell.safe_lists import _HARNESS_NAMES, _MACOS_ALIASES


# --- small helpers ---------------------------------------------------------


def _inside(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip("/") + "/")


def _norm(path: str) -> str:
    path = os.path.normpath(path)
    return "/" + path.lstrip("/") if path.startswith("//") else path


def _canon(path: str) -> str:
    """One spelling for one place, for the private and credential checks: folded to
    one case (macOS's disks ignore it, and realpath keeps a name as written:
    ~/library is ~/Library there) and with macOS's second spellings taken off
    (`_MACOS_ALIASES`: /private/etc/ssh is /etc/ssh)."""
    out = path.casefold()
    for alias, real in _MACOS_ALIASES:
        if out == alias or out.startswith(alias + "/"):
            out = real + out[len(alias) :]
    return out or "/"


def _spellings(path: str) -> list[str]:
    """Every spelling of `path` (`_canon`'s) a folder above it may be named by: a walk
    of /System/Volumes or /private goes through it by its second spelling."""
    canon = _canon(path)
    forms = [canon, *(alias + canon[len(real) :] for alias, real in _MACOS_ALIASES
                      if real and (canon == real or canon.startswith(real + "/")))]
    return sorted({form for spelled in forms for form in (spelled, _MACOS_ALIASES[0][0] + spelled)})


def _long(arg: str, names: Sequence[str]) -> str | None:
    """The listed long option `arg` spells, counting GNU abbreviations (`--out=` is `--output=`)."""
    if not arg.startswith("--") or arg == "--":
        return None
    given = arg.split("=", 1)[0]
    for name in names:
        if name == given or (len(given) > 2 and name.startswith(given)):
            return name
    return None


def _short_letters(arg: str, value_letters: str) -> str:
    """The option letters of a cluster like `-rn`, up to the first one that takes a value."""
    if len(arg) < 2 or arg[0] != "-" or arg[1] == "-":
        return ""
    letters = []
    for ch in arg[1:]:
        letters.append(ch)
        if ch in value_letters:
            break
    return "".join(letters)


def _options(words: Sequence[_Word]) -> list[str]:
    """The arguments before a `--` (after it, everything is a name, never an option)."""
    out = []
    for w in words:
        if w.value == "--":
            break
        out.append(w.value)
    return out


def _dashdash_as_value(words: Sequence[_Word]) -> list[_Word] | None:
    """The same words, reading every `--` that comes right after an option as that
    option's VALUE (an empty one), so what follows it is read as options again.

    Whether `-e --` ends the options or hands `--` to `-e` depends on each
    option's arity, which the lists here do not know in full. So the caller
    checks both readings; None when no `--` is in that position."""
    out = list(words)
    changed = False
    for k in range(1, len(out)):
        prev = out[k - 1].value
        if out[k].value == "--" and prev.startswith("-") and prev not in ("-", "--"):
            out[k] = _Word("", "''", synthetic=True)
            changed = True
    return out if changed else None


def _positionals(words: Sequence[_Word], text_options: Sequence[str]) -> list[_Word]:
    """The arguments that are names, not options or a text option's separate value."""
    out: list[_Word] = []
    skip_next = False
    names_only = False
    for w in words:
        v = w.value
        if skip_next:
            skip_next = False
        elif w.synthetic:
            pass  # an option's value, not a name
        elif names_only or v == "-" or not v.startswith("-"):
            out.append(w)
        elif v == "--":
            names_only = True
        elif v in text_options:
            skip_next = True
    return out


def _hidden(comps: list[str], real: str) -> str | None:
    """The hidden folder in a path below a working folder, if any."""
    if comps and comps[-1] in _HARNESS_NAMES:
        return None
    for comp in comps[:-1]:
        if comp.startswith("."):
            return comp
    if comps and comps[-1].startswith(".") and os.path.isdir(real):
        return comps[-1]
    return None


def _clean_path(value: str | None) -> str:
    """The parent's PATH without empty or relative entries (a `.` there would run ./cat)."""
    entries: list[str] = []
    for entry in (value or "").split(os.pathsep):
        if entry and os.path.isabs(entry) and entry not in entries:
            entries.append(entry)
    return os.pathsep.join(entries) or os.defpath
