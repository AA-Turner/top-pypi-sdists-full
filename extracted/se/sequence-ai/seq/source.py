"""
The source a deployment runs, said as one hash, and a template's large upstream sources.

In one sentence: `files_sha256` is one sha256 over a set of files - each file's path, size and sha256 on a line of its
own, the lines in path order - which `seq deploy` prints for what it uploads and the platform keeps beside the version;
`tree_sha256` is the same over a directory → a template whose image installs an upstream too large to upload with a
deploy (LIBERO, robosuite) names it in third_party/SOURCES.json, by its official package's sha256 and the tree_sha256 of
what that package unpacks to → `seq init` downloads the package into third_party/<name>/ and checks both → `seq deploy`
leaves that directory out of the upload while it is as published (the image installs the same package, by its
sha256), refuses while it was changed (the image would not run the change), and goes on when it was never downloaded
(`seq init --no-source`).

WHY one line per file and not a hash of the archive: anyone can recompute it from their own folder, with no tar
settings to match. WHY a changed large upstream is refused rather than run as published: the user would be shown one
source and run another.

The format, for every reader that recomputes it (publish.py, the gateway): a regular file's path relative to the
directory, '/'-separated; a tab; its size in bytes; a tab; its sha256 in lowercase hex; a newline. The lines sorted by
their paths' UTF-8 bytes, the sha256 of all of them together. Left out wherever they are: the directories in SKIP_DIRS,
the files in SKIP_FILES or ending in SKIP_SUFFIXES, and symbolic links.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SKIP_DIRS = frozenset({".git", ".hg", ".svn", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
                       ".ipynb_checkpoints"})
SKIP_FILES = frozenset({".DS_Store"})
SKIP_SUFFIXES = (".pyc", ".pyo")
SOURCES = "third_party/SOURCES.json"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def files_sha256(entries: Iterable[tuple[str, int, str]]) -> str:
    """The hash of a set of files, each (path, size, sha256 hex)."""
    lines = sorted((path.encode(), f"{path}\t{size}\t{sha}\n") for path, size, sha in entries)
    return hashlib.sha256("".join(line for _, line in lines).encode()).hexdigest()


def skipped(name: str, is_dir: bool) -> bool:
    """Whether a file or directory of this name is never part of a tree."""
    return name in SKIP_DIRS if is_dir else (name in SKIP_FILES or name.endswith(SKIP_SUFFIXES))


def tree_files(root: Path) -> list[tuple[str, Path]]:
    """(path relative to `root`, path) of every file a tree holds, in path order."""
    out: list[tuple[str, Path]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if not skipped(d, True) and not os.path.islink(os.path.join(dirpath, d)))
        for name in sorted(filenames):
            full = Path(dirpath) / name
            if skipped(name, False) or full.is_symlink() or not full.is_file():
                continue
            out.append((full.relative_to(root).as_posix(), full))
    return out


def tree_sha256(root: Path) -> str:
    """The hash of the directory `root`, as SOURCES.json names a large upstream's."""
    return files_sha256((rel, p.stat().st_size, file_sha256(p)) for rel, p in tree_files(Path(root)))


@dataclass(frozen=True)
class Source:
    """A large upstream a template's image installs from its official package, as third_party/SOURCES.json names it."""
    name: str
    package_sha256: str
    size: int
    tree_sha256: str
    commit: str | None = None
    repo: str | None = None


def read_sources(folder: Path) -> list[Source]:
    """The large upstreams the template in `folder` names; none when it names none."""
    path = Path(folder) / SOURCES
    if not path.is_file():
        return []
    try:
        listed = json.loads(path.read_text())
        return [Source(name=str(name), package_sha256=str(s["package_sha256"]), size=int(s["size"]),
                       tree_sha256=str(s["tree_sha256"]), commit=s.get("commit"), repo=s.get("repo"))
                for name, s in sorted(listed.items())]
    except (ValueError, KeyError, TypeError, AttributeError):
        from seq.errors import PolicyDefinitionError

        raise PolicyDefinitionError(f"{path} is not what a template version writes there; take it from `seq init` "
                                    "again") from None


@dataclass(frozen=True)
class SourceState:
    """How the folder holds one large upstream: "as published", "changed" or "not downloaded"."""
    source: Source
    state: str
    local_sha256: str | None = None

    @property
    def path(self) -> str:
        return f"third_party/{self.source.name}"


def check_sources(folder: Path) -> list[SourceState]:
    """How the folder holds each large upstream its template names."""
    out = []
    for s in read_sources(folder):
        where = Path(folder) / "third_party" / s.name
        if not where.exists():
            out.append(SourceState(s, "not downloaded"))
            continue
        local = tree_sha256(where)
        out.append(SourceState(s, "as published" if local == s.tree_sha256 else "changed", local))
    return out


def changed_refusal(states: list[SourceState], folder: Path | None = None) -> str | None:
    """Why `seq deploy` stops when a large upstream was changed, and what to do; None when none was. `folder`: the
    deployed folder, its upstreams then named as the person who ran the command holds them (discover.shown)."""
    changed = [s for s in states if s.state == "changed"]
    if not changed:
        return None
    from seq import discover

    named = [discover.shown(folder, s.path) if folder is not None else s.path for s in changed]
    paths = ", ".join(named)
    return (f"{paths} differs from what this template version installs (its tree sha256 is "
            f"{changed[0].local_sha256[:12]}, the official package's {changed[0].source.tree_sha256[:12]}). The image "
            "installs a large upstream only from its official package, so a change to it cannot run yet - and it is "
            f"never run in its place. Undo the change, or delete {named[0]} to deploy as published (`seq init` "
            "downloads it again to read).")


def _mismatch():
    from sequence_ai.errors import InternalError

    class SourceMismatch(InternalError):
        """A large upstream's package is not what the template's SOURCES.json names."""
    return SourceMismatch


SourceMismatch = _mismatch()


def fetch_sources(folder: Path, *, template: str, version: str, get,
                  only: str | None = None) -> list[tuple[Source, int]]:
    """Download each large upstream the template in `folder` names (or the one named `only`) into third_party/<name>/,
    checked against its package_sha256 and tree_sha256: [(source, bytes downloaded)]. `get(upstream)` streams the
    official package (an httpx response). A package that is not what SOURCES.json says is never left in the folder:
    SourceMismatch."""
    done = []
    for s in read_sources(folder):
        target = Path(folder) / "third_party" / s.name
        if target.exists() or (only is not None and s.name != only):
            continue
        with tempfile.TemporaryDirectory(dir=Path(folder) / "third_party") as tmp:
            pkg = Path(tmp) / f"{s.name}.tar.gz"
            h, n = hashlib.sha256(), 0
            with get(s.name) as resp, open(pkg, "wb") as out:
                for chunk in resp.iter_bytes(1 << 20):
                    h.update(chunk)
                    n += len(chunk)
                    out.write(chunk)
            if (h.hexdigest(), n) != (s.package_sha256, s.size):
                raise SourceMismatch(f"{template} {version}: the package of {s.name} is {n} bytes, sha256 "
                                    f"{h.hexdigest()[:12]} - SOURCES.json says {s.size}, {s.package_sha256[:12]}")
            with tarfile.open(pkg, mode="r:gz") as tf:
                for member in tf.getmembers():
                    if not (member.name == s.name or member.name.startswith(s.name + "/")) or member.issym() \
                            or member.islnk():
                        raise SourceMismatch(f"{template} {version}: the package of {s.name} holds {member.name!r}, "
                                            f"which is not under {s.name}/")
                tf.extractall(tmp, filter="data")
            unpacked = Path(tmp) / s.name
            if tree_sha256(unpacked) != s.tree_sha256:
                raise SourceMismatch(f"{template} {version}: {s.name} unpacks to a tree other than SOURCES.json names")
            shutil.move(str(unpacked), str(target))
        done.append((s, n))
    return done
