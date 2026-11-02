"""the inode signature and content hash a store verifies a file by, and when a saved signature may stand in."""

from __future__ import annotations
import hashlib
import os
from pathlib import Path
import stat
import time

#: A file written within this long is re-read whatever its signature says.
#: Timestamp resolution is 1-10ms on Linux and coarser through NFS/SMB, so a
#: write landing in the same tick as the stat is invisible to the cache.
SIGNATURE_SETTLE_SECONDS = 2.0


def _signature_tuple(value) -> tuple[int, int, int, int, int]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def signature_of(value) -> str | None:
    """The inode fingerprint of a stat result, or None when it cannot be trusted.

    WHAT THIS IS FOR. Re-reading a terabyte to learn that nothing changed is the
    single largest cost in a repeat import, and every backup tool solves it the
    same way: remember the inode facts, and only read again when one of them
    moved. `st_ctime_ns` is the load-bearing field -- userspace has no API to
    set it, so any write, rename or permission change bumps it, which is what
    makes this stronger than the size+mtime pair `hash_current` rightly refuses
    to accept on its own. `st_dev`/`st_ino` catch a replace-by-rename that
    restored every other field.

    WHEN IT RETURNS NONE. A whole-second `ctime_ns` means the filesystem is not
    recording sub-second resolution (exFAT, some NFS/SMB mounts, a translating
    NAS). There the timestamps cannot distinguish two writes in the same second,
    so there is no signature worth storing and the file is hashed every time --
    exactly today's behaviour, kept for the filesystems that need it.
    """
    if not value.st_ctime_ns or value.st_ctime_ns % 1_000_000_000 == 0:
        return None
    return ":".join(str(part) for part in _signature_tuple(value))


def hash_current(root: Path, relative: str) -> tuple[str, int]:
    """Hash one confined, stable open file. Same size/mtime is never enough."""
    digest, size, _ = hash_current_signed(root, relative)
    return digest, size


def hash_current_signed(root: Path, relative: str) -> tuple[str, int, str | None]:
    """`hash_current`, also returning the inode signature it verified against.

    Split out rather than changing `hash_current`'s shape: the signature is
    meaningful only NEXT to the digest it was taken with, and callers that just
    want bytes should not have to carry a third value to ignore it.
    """
    target = (root / relative).resolve(strict=True)
    if not target.is_relative_to(root.resolve()) or Path(relative).is_absolute():
        raise CoverageError(f"Source escapes the folder: {relative}")
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        before = os.fstat(handle.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise CoverageError(f"Source is not a regular file: {relative}")
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
        after = os.fstat(handle.fileno())
    current = (root / relative).stat()
    if (_signature_tuple(before) != _signature_tuple(after)
            or _signature_tuple(after) != _signature_tuple(current)):
        raise CoverageError(f"Source changed while it was being verified: {relative}")
    return digest.hexdigest(), after.st_size, signature_of(current)


def reusable_signature(root: Path, relative: str, saved: str | None) -> str | None:
    """The current signature when a saved one may stand in for re-reading the file.

    None means "read it". Three ways to get there, and all three are ordinary:
    nothing saved, the file moved in some way, or the signature is too young to
    trust -- a file whose mtime is inside the settle window may still be being
    written, and the write would land in the same timestamp we just recorded.
    """
    if not saved:
        return None
    try:
        current = (root / relative).stat()
    except OSError:
        return None
    if not stat.S_ISREG(current.st_mode):
        return None
    signature = signature_of(current)
    if signature is None or signature != saved:
        return None
    if current.st_mtime_ns > (time.time() - SIGNATURE_SETTLE_SECONDS) * 1_000_000_000:
        return None
    return signature
from probe.cli.imports.folder.coverage.coverage import CoverageError  # noqa: E402 -- pieces need each other; the front door loads this one first
