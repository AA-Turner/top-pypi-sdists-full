"""recognize files no command may touch (a checkout's bookkeeping, the installed package's own files) and the note folders it may write."""

from __future__ import annotations
import os
import re
import sys
from pathlib import Path
from typing import Sequence
from probe.daemon.shell.held import _held_commands, _held_dirs, _held_resolve
from probe.daemon.shell.words import _inside, _norm


#: The files `probe` keeps beside a checked-out document (`note_sync.Paths`: the
#: base copy, its version and owner, the lock; `summary_cli`'s visuals version):
#: never the daemon's to write. A forged version would push stale text past the
#: server's concurrent-edit and erasure checks.
_BOOKKEEPING = (".base", ".meta.json", ".lock", ".owner")
#: Any case: macOS and Windows file systems ignore it, so `X.BASE` is `X.base`.
_BOOKKEEPING_NAMED = re.compile(r"""[^\s'"`;|&<>()=]*(?:\.base|\.meta\.json|\.lock|\.owner)(?=$|[\s'"`;|&<>()])""", re.I)


def _record_hashes() -> dict[str, str]:
    """Real path -> sha256 (RECORD's urlsafe base64) of every file the installed
    `probe-research` package lists in its RECORD; empty when it has none."""
    global _RECORD
    if _RECORD is None:
        found: dict[str, str] = {}
        try:
            from importlib import metadata

            dist = metadata.distribution("probe-research")
            for entry in dist.files or []:
                if entry.hash is not None and entry.hash.mode == "sha256":
                    found[os.path.realpath(str(dist.locate_file(entry)))] = entry.hash.value
        except Exception:  # noqa: BLE001 -- no package metadata: no file is the package's
            found = {}
        _RECORD = found
    return _RECORD


_RECORD: dict[str, str] | None = None


def packaged_file(real: str) -> bool:
    """Is `real` a file of the installed package, as its RECORD lists it: the
    path AND its content (sha256)? A second name another file was given there
    (a hard link to a key) does not hash alike."""
    import base64
    import hashlib

    want = _record_hashes().get(real)
    if want is None:
        return False
    try:
        with open(real, "rb") as handle:
            digest = hashlib.sha256(handle.read(4 * 1024 * 1024 + 1)).digest()
    except OSError:
        return False
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode() == want


#: Words of a command line, as the bookkeeping ban reads them (quotes already gone).
_TOKENS = re.compile(r"[^\s;|&<>()=]+")
#: What can stand for other characters in a name: globs, braces, expansions.
_STANDS_IN = "?*[{$`"


def _unquoted(text: str) -> str:
    """`text` without quotes and backslashes, as bash joins the pieces of a word
    (`x.md.ba''se`, `x.md.ba\\se`, `x.md."BASE"` are all `x.md.base`)."""
    return re.sub(r"[\"'\\]", "", text)


def _fold(path: str) -> str:
    """`path` without case where the file system ignores it (macOS, Windows):
    `~/.local/STATE/probe/notes` is the notes folder there."""
    return path.casefold() if sys.platform == "darwin" or os.name == "nt" else path


def _could_be_bookkeeping(name: str) -> bool:
    """Could this file name, as written, be a checkout's bookkeeping file? Its
    suffix in any case, or a glob, brace or expansion that could expand to one
    (`x.md.bas?`, `x.md.ba[s]e`, `x.md.b*`, `x.md.ba{s,}e`)."""
    import fnmatch

    folded = name.casefold()
    if folded.endswith(_BOOKKEEPING):
        return True
    if not any(c in folded for c in _STANDS_IN):
        return False
    if any(c in folded for c in "{$`"):
        return True  # expands to what the text does not show
    literal = re.split(r"[?*\[]", folded, maxsplit=1)[0]
    return any(fnmatch.fnmatchcase(literal + suffix[j:], folded)
               for suffix in _BOOKKEEPING for j in range(len(suffix) + 1)
               if (literal + suffix[j:]).endswith(suffix))


def is_bookkeeping(name: str) -> bool:
    """A checkout's base copy, version or lock (`_BOOKKEEPING`), in any case."""
    return name.casefold().endswith(_BOOKKEEPING)


def names_writable(command: str, *, cwd: Path, home: Path, folders: Sequence[Path]) -> str | None:
    """A word of `command` naming `folders` (the notes the daemon writes without a
    question) or a file in them, else None. Such a command is never asked: a yes
    to it could run text nobody was shown. Read broadly on purpose: every word
    (and the parts of `--opt=VALUE` / `A:B`), in every folder a `cd` may reach,
    and the folders' paths anywhere in the text."""
    home_s = _norm(os.path.abspath(str(home)))
    roots: list[str] = []
    for folder in folders:
        for path in (_norm(os.path.abspath(str(folder))), os.path.realpath(str(folder))):
            if path not in roots:
                roots.append(path)
    if not roots:
        return None
    for root in roots:
        forms = [root]
        if _inside(root, home_s) and root != home_s:
            rel = root[len(home_s) + 1 :]
            forms += [f"~/{rel}", f"$HOME/{rel}", f"${{HOME}}/{rel}"]
        if any(form in command for form in forms):
            return root
    commands = _held_commands(command)
    if commands is None:
        return None  # the caller refuses a command it cannot read (`held_scripts`)
    dirs = _held_dirs(commands, os.path.realpath(str(cwd)), home_s)
    for c in commands:
        for word in [*c.words, *c.stdin, *c.targets]:
            for piece in {word, *re.split(r"[=:]", word)}:
                if not piece:
                    continue
                for real in _held_resolve(piece, dirs, home_s):
                    if any(_inside(real, root) for root in roots):
                        return real
    return None
