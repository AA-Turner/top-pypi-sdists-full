"""
The files of a folder a policy is read from: what `seq serve` looks for classes in and `seq deploy` uploads - every file
but version control, caches, a virtualenv or build output at the folder's root, a version's build context, a .env file,
and what a .seqignore leaves out - each left one said with why. Open, so the folder `seq serve` reads on your own GPU is
the one a deployment would hold; the deployment's own packing (sequence-cloud) reads it from here.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from seq import source




_ROOT_SKIP_DIRS = frozenset({".venv", "venv", "env", "build", "dist", "node_modules"})


_ROOT_SKIP_SUFFIXES = (".egg-info",)








SOURCE_CONTEXT_DIR = "build-context"


IGNORE_FILE = ".seqignore"


_WHY_SKIPPED = {".git": "version control", ".hg": "version control", ".svn": "version control"}




_ENV_WHY = "a .env file: secrets go through `seq secret`; a .seqignore line !.env uploads it"


def _why(name: str, is_dir: bool) -> str:
    """Why seq.source leaves a file or directory of this name out of every tree."""
    if name in _WHY_SKIPPED:
        return _WHY_SKIPPED[name]
    if is_dir:
        return "a cache"
    return "the Finder's folder notes" if name == ".DS_Store" else "compiled bytecode"



def _glob(pattern: str) -> str:
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append(r"(?:.*/)?")
            i += 3
        elif pattern.startswith("**", i):
            out.append(r".*")
            i += 2
        elif pattern[i] == "*":
            out.append(r"[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append(r"[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return "".join(out)


def ignore_rules(folder: Path) -> list[tuple[re.Pattern, bool, bool, str]]:
    """The folder's .seqignore, as (pattern, directories only, takes back, the line): gitignore's form - a path from the
    folder (`third_party/openpi/docs`, `/notes.txt`) or a name at any depth below it (`data`, `*.bin`); a trailing / for
    directories only; * and ? within a name, ** across directories; # comments; `!` takes back what a line before it -
    or a parent folder's .seqignore - left out, though nothing inside a folder left out whole, as in git."""
    path = Path(folder) / IGNORE_FILE
    if not path.is_file():
        return []
    rules = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line == "!":
            continue
        back = line.startswith("!")
        body = line[1:] if back else line
        dir_only = body.endswith("/")
        pattern = body.rstrip("/")
        anchored = pattern.startswith("/") or "/" in pattern
        regex = ("^" if anchored else r"^(?:.*/)?") + _glob(pattern.lstrip("/")) + "$"
        rules.append((re.compile(regex), dir_only, back, line))
    return rules


def _decided(rel: str, is_dir: bool, layers: list[tuple[str, list]], why: str | None = None) -> str | None:
    """Why `rel` - a path from the folder's top - is left out, or None when it is kept: `why` before any rule (a .env
    file's), then every .seqignore above it, the top's first (`layers`: (its folder, its rules)), the last line to match
    deciding - a line leaves out, a `!` line takes back."""
    for folder, rules in layers:
        if folder and not rel.startswith(folder + "/"):
            continue
        sub = rel[len(folder) + 1:] if folder else rel
        for regex, dir_only, back, line in rules:
            if (is_dir or not dir_only) and regex.match(sub):
                why = None if back else f"{folder + '/' if folder else ''}{IGNORE_FILE}: {line}"
    return why


def _is_env(name: str) -> bool:
    return name == ".env" or name.startswith(".env.")



def _folder_files(root: Path, official: set[str]) -> tuple[list[tuple[Path, str]], list[tuple[str, str]]]:
    """Every file of the folder the snapshot keeps, as (path, path in the folder), and what it leaves out, with why."""
    files: list[tuple[Path, str]] = []
    left: list[tuple[str, str]] = []
    layers_of: dict[str, list[tuple[str, list]]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        here = Path(dirpath).relative_to(root).as_posix()
        here = "" if here == "." else here
        own = ignore_rules(Path(dirpath))
        layers = (layers_of[here.rpartition("/")[0]] if here else []) + ([(here, own)] if own else [])
        layers_of[here] = layers
        keep = []
        for d in sorted(dirnames):
            rel = f"{here}/{d}" if here else d
            why = None
            if os.path.islink(os.path.join(dirpath, d)):
                why = "a symbolic link"
            elif rel in official:
                why = "installed from its official package, as published"
            elif source.skipped(d, True):
                why = _why(d, True)
            elif not here and (d in _ROOT_SKIP_DIRS or d.endswith(_ROOT_SKIP_SUFFIXES)):
                why = "a virtualenv or build output at the folder's root"
            elif not here and d == SOURCE_CONTEXT_DIR:
                why = "a version's build context, as its source download writes it - not its code"
            else:
                why = _decided(rel, True, layers)
            if why:
                left.append((rel + "/", why))
            else:
                keep.append(d)
        dirnames[:] = keep
        for name in sorted(filenames):
            rel = f"{here}/{name}" if here else name
            full = Path(dirpath) / name
            why = None
            if full.is_symlink():
                why = "a symbolic link"
            elif not full.is_file():
                why = "not a regular file"
            elif source.skipped(name, False):
                why = _why(name, False)
            elif name in _WHY_SKIPPED:
                why = _WHY_SKIPPED[name]
            else:
                why = _decided(rel, False, layers, _ENV_WHY if _is_env(name) else None)
            if why:
                left.append((rel, why))
            else:
                files.append((full, rel))
    return files, left
