"""Content fingerprinting for the upload flow.

Its own module: ``client`` (anchored uploads) and ``run`` (run-anchored) both need
it and cannot import each other (``client`` imports ``Run`` at file bottom; the
reverse import deadlocks depending on which is reached first). Also keeps ONE
definition of the wire contract's hash.
"""

from __future__ import annotations

import hashlib
import os
import socket
import stat
import time
from pathlib import Path

from ...foundation.safe_warn import safe_warn

#: Streaming read size, so a multi-GB artifact is never held in memory to hash.
_CHUNK_BYTES = 1024 * 1024


def fingerprint(path: str) -> tuple[str, int]:
    """``(sha256 hex, size_bytes)`` for a local file.

    Lowercase hex: the server 422s on anything else.
    """
    digest = hashlib.sha256()
    size = 0
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(_CHUNK_BYTES), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def local_file_uri(abspath: str) -> str:
    """RFC 8089 ``file://`` URI for an absolute local path.

    ``pathlib`` percent-encodes spaces, ``#``, ``%`` and non-ASCII so the pointer
    round-trips. The RAW path is kept in ``meta.local_path``; agents resolve that, not this URI.
    """
    return Path(abspath).as_uri()


def reference_fields(
    path: str,
    *,
    hash_content: bool = False,
    allow_missing: bool = False,
    size_bytes: int | None = None,
) -> dict:
    """Artifact fields for a local-PATH reference (bytes NOT uploaded).

    Returns ``uri`` (``file://`` pointer), ``meta`` (raw ``local_path`` and recording
    ``host``), and ``size_bytes``/``content_hash`` when known. Only ``os.stat`` runs by
    default (a 16 GB reference must not read 16 GB); ``hash_content`` opts into a full
    fingerprint (content dedup, later reference->managed adoption). Raises
    ``FileNotFoundError`` for a missing path unless ``allow_missing`` (it may live on a
    mount/host this machine cannot see). ``size_bytes`` is a size the caller already
    measured, so a folder is not walked again (Lightning sums a sharded checkpoint once per save).
    """
    local = os.path.abspath(path)
    exists = os.path.exists(local)
    if not exists and not allow_missing:
        raise FileNotFoundError(
            f"cannot reference '{local}': no such file. Pass allow_missing to record it "
            "anyway (e.g. it lives on a mount or host this machine does not see)."
        )
    fields: dict = {
        "uri": local_file_uri(local),
        "meta": {"local_path": local, "host": socket.gethostname()},
    }
    if exists:
        if os.path.isdir(local):
            fields["meta"]["is_directory"] = True
            if size_bytes is not None:
                fields["size_bytes"] = size_bytes
            else:
                # A sharded checkpoint (DeepSpeed, FSDP) is a FOLDER; its own entry size (4096) says nothing, so sum the contents.
                size, n_files, complete = folder_size(local)
                fields["size_bytes"] = size
                fields["meta"]["n_files"] = n_files
                if not complete:
                    fields["meta"]["size_partial"] = True
            if hash_content:
                # Said on the row and by warning: a requested fingerprint must not look taken.
                fields["meta"]["content_hash_skipped"] = "directory"
                safe_warn.warn(
                    f"probe: hash_content=True does not apply to a folder ({local}); it was "
                    "recorded by size, without a content hash.",
                    stacklevel=3,
                )
        elif hash_content:
            digest, size = fingerprint(path)
            fields["content_hash"] = digest
            fields["size_bytes"] = size
        else:
            fields["size_bytes"] = os.path.getsize(local)
    return fields


#: lstat-summing runs beside a training loop, maybe on a network filesystem. Past
#: either bound the size is a lower bound, flagged ``meta.size_partial``.
FOLDER_MAX_ENTRIES = 100_000
FOLDER_MAX_SECONDS = 2.0


def folder_size(root: str) -> tuple[int, int, bool]:
    """``(bytes, files, complete)`` under ``root``: regular files only, symlinks not
    followed, unreadable entries skipped; ``lstat`` only. Stops after
    :data:`FOLDER_MAX_ENTRIES` entries or :data:`FOLDER_MAX_SECONDS` with ``complete=False``."""
    total = count = seen = 0
    deadline = time.monotonic() + FOLDER_MAX_SECONDS
    for dirpath, dirnames, filenames in os.walk(root, onerror=lambda _e: None):
        seen += len(dirnames)
        if seen > FOLDER_MAX_ENTRIES or time.monotonic() > deadline:
            return total, count, False
        for filename in filenames:
            seen += 1
            if seen > FOLDER_MAX_ENTRIES or time.monotonic() > deadline:
                return total, count, False
            try:
                info = os.lstat(os.path.join(dirpath, filename))
            except OSError:
                continue
            if stat.S_ISREG(info.st_mode):
                total += info.st_size
                count += 1
    return total, count, True
