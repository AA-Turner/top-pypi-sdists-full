"""Copies of an installed package that one owner keeps, to load from instead of
a folder someone else rewrites or deletes ("pins").

Two owners: the Probe service pins the tap it imports (`service.recorders`,
`<machine folder>/taps/`: a coding agent's plugin cache deletes old version
folders under a tap imported hours earlier), and the update pins the Probe pi
package after `pi update` (`cli.pi_pins`, `<state>/pi/pins/`: `pi update` runs
`git clean -fdx` on the clone a running pi session loaded its code from).

A pin is a folder named `<version>-<fingerprint>` holding one or more source
trees at their relative paths, marked done with PIN_DONE written last. It is
made in a staging folder beside it and renamed into place; a source that
changed while it was copied (an agent still installing it) is never marked
done. A pin made from the same files is reused, not made again. Writers of one
store take its lock (`LOCK_NAME`) to publish and to
prune, so one never removes a pin another just published (two pi sessions
starting at once each pin the package).
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import random
import re
import shutil
import time
from collections.abc import Collection, Mapping
from pathlib import Path

#: Written last into a pin: one without it was cut short, and is made again.
PIN_DONE = ".pinned"
#: Pins kept besides the one loading: the newest-used few, and none unused for
#: longer than PIN_KEEP_S.
PIN_KEEP = 3
PIN_KEEP_S = 7 * 86400
#: A staging folder (a copy cut short) left this long is removed.
STALE_STAGING_S = 3600
#: The store's lock file (a file: `prune` looks at folders only).
LOCK_NAME = ".pins.lock"

_VERSION = re.compile(r"^\d+(\.\d+)*$")
_SKIP = ("__pycache__", "*.pyc")


@contextlib.contextmanager
def _locked(store: Path):
    """The store's lock for this block (`oscompat.flock`: Windows too)."""
    from probe._shared import oscompat  # noqa: PLC0415

    store.mkdir(parents=True, exist_ok=True)
    with open(store / LOCK_NAME, "a", encoding="utf-8") as handle:
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX)
        try:
            yield
        finally:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)


def _files(rel: str, src: Path):
    """`(name, path)` of every regular file under `src`, `name` relative to the
    pin root; `src` itself when it is a file."""
    if src.is_file():
        yield rel, src
        return
    for path in sorted(src.rglob("*")):
        if "__pycache__" in path.parts or path.suffix == ".pyc" or not path.is_file():
            continue
        yield f"{rel}/{path.relative_to(src).as_posix()}", path


def fingerprint(sources: Mapping[str, Path], *, times: bool = True) -> str:
    """The files `sources` hold (relative name -> tree or file), with their sizes
    (and times): a pin made from these same files is reused. Without times:
    what a copy of them must hold (a copy's times need not match to the ns)."""
    digest = hashlib.sha256()
    for rel, src in sorted(sources.items()):
        for name, path in _files(rel, src):
            info = path.stat()
            when = f"\0{info.st_mtime_ns}" if times else ""
            digest.update(f"{name}\0{info.st_size}{when}\n".encode())
    return digest.hexdigest()[:16]


def pin_name(version: str | None, fp: str, default: str) -> str:
    return f"{version if _VERSION.match(version or '') else default}-{fp}"


def make(store: Path, version: str | None, sources: Mapping[str, Path], *, default: str = "pin",
         meta: dict | None = None, symlinks: bool = False) -> Path:
    """The pin of `sources` in `store`, made unless a complete one of the same
    files is there. Raises OSError when a source cannot be copied whole (the
    caller keeps loading from where it is). `symlinks`: keep links as links
    (a pi clone's node_modules/.bin, which point inside the tree); else, as the
    tap's pins always did, copy what they point to, so a pin never depends on
    the folder it was made from."""
    before = fingerprint(sources)
    name = pin_name(version, before, default)
    target = store / name
    if not (target / PIN_DONE).is_file():
        store.mkdir(parents=True, exist_ok=True)
        staging = store / f".{name}.{os.getpid()}.{random.randrange(1 << 30)}"
        try:
            for rel, src in sources.items():
                dest = staging / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                if src.is_file():
                    shutil.copy2(src, dest)
                else:
                    shutil.copytree(src, dest, symlinks=symlinks, ignore=shutil.ignore_patterns(*_SKIP))
            copied = {rel: staging / rel for rel in sources}
            if fingerprint(sources) != before or (
                fingerprint(sources, times=False) != fingerprint(copied, times=False)
            ):
                raise OSError(f"{', '.join(str(s) for s in sources.values())} changed while it was copied")
            (staging / PIN_DONE).write_text(json.dumps({**(meta or {}), "version": version}), encoding="utf-8")
            with _locked(store):
                if not (target / PIN_DONE).is_file():  # else another writer published it meanwhile: keep theirs
                    if target.exists():
                        shutil.rmtree(target)  # a pin cut short (no PIN_DONE)
                    os.replace(staging, target)
        finally:
            shutil.rmtree(staging, ignore_errors=True)
    with contextlib.suppress(OSError):
        os.utime(target)  # in use now: the prune counts from here
    return target


def complete(store: Path, name: str) -> bool:
    """Is `store/name` a whole pin?"""
    return bool(name) and "/" not in name and not name.startswith(".") and (store / name / PIN_DONE).is_file()


def prune(store: Path, keep: Collection[Path] = (), referenced: Collection[str] = (), *,
          keep_n: int = PIN_KEEP, keep_s: float = PIN_KEEP_S) -> list[Path]:
    """Remove the pins past `keep_n` (newest-used first) and any unused for
    `keep_s`, and staging leftovers; never one in `keep` or named in
    `referenced` (pins live processes still load from). Returns what it removed."""
    if not store.is_dir():
        return []
    with _locked(store):
        return _prune(store, keep, referenced, keep_n, keep_s)


def _prune(store: Path, keep: Collection[Path], referenced: Collection[str], keep_n: int, keep_s: float) -> list[Path]:
    try:
        entries = [p for p in store.iterdir() if p not in keep and p.is_dir() and not p.is_symlink()]
    except OSError:
        return []
    now = time.time()

    def used(path: Path) -> float:
        try:
            return path.stat().st_mtime
        except OSError:
            return 0.0

    copies = sorted((p for p in entries if not p.name.startswith(".")), key=used, reverse=True)
    stale = [p for p in entries if p.name.startswith(".") and now - used(p) > STALE_STAGING_S]
    doomed = copies[keep_n:] + [p for p in copies[:keep_n] if now - used(p) > keep_s] + stale
    removed = []
    for path in doomed:
        if path.name in referenced:
            continue
        shutil.rmtree(path, ignore_errors=True)
        removed.append(path)
    return removed
