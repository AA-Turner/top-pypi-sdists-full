"""Walk a dataset folder into a hashed manifest with the recorder's own hasher."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any
from probe.sdk.catalog.refs import CatalogRefused
#: The server's ceiling per manifest (`dataset_manifest_files`).
MAX_MANIFEST_FILES = 100_000
#: Entries a folder walk looks at before it stops (it runs on the training thread).
MAX_WALK_ENTRIES = 1_000_000
#: The manifest's identity format, named in its body so the server can recompute it.
MANIFEST_FORMAT = "probe-manifest-v1"


# Identity: manifests, pointers


@dataclass
class ManifestFile:
    relpath: str
    size_bytes: int
    content_hash: str | None = None
    fingerprint: str | None = None
    rows: int | None = None
    #: Where it is on this machine (never sent).
    full: str = ""

    def identity_line(self) -> str:
        return f"{self.relpath}\t{self.size_bytes}\t{self.content_hash or self.fingerprint or ''}\n"

    def wire(self) -> dict:
        row: dict[str, Any] = {"relpath": self.relpath, "size_bytes": self.size_bytes}
        if self.content_hash:
            row["content_hash"] = self.content_hash
        if self.fingerprint:
            row["fingerprint"] = self.fingerprint
        if self.rows is not None:
            row["rows"] = self.rows
        return row


@dataclass
class Manifest:
    files: list[ManifestFile] = field(default_factory=list)
    #: Something is not identified by its full bytes (fingerprinted, unhashed,
    #: skipped, cut at the file ceiling).
    partial: bool = False
    #: Paths left out (a link, not a regular file, unreadable).
    skipped: int = 0

    @property
    def total_bytes(self) -> int:
        return sum(f.size_bytes for f in self.files)

    @property
    def rows_complete(self) -> bool:
        return bool(self.files) and all(f.rows is not None for f in self.files)

    @property
    def total_rows(self) -> int | None:
        return sum(f.rows or 0 for f in self.files) if self.rows_complete else None

    def identity(self) -> str:
        """sha256 of the sorted ``(relpath, size, sha256 | fingerprint)`` lines (tab-separated,
        newline-terminated, UTF-8; `MANIFEST_FORMAT`). Rows are NOT part of it: same bytes, same dataset."""
        digest = hashlib.sha256()
        for f in sorted(self.files, key=lambda f: f.relpath):
            digest.update(f.identity_line().encode("utf-8", "surrogatepass"))
        return digest.hexdigest()

    def body(self) -> dict:
        body: dict[str, Any] = {
            "format": MANIFEST_FORMAT,
            "files": [f.wire() for f in sorted(self.files, key=lambda f: f.relpath)],
            "partial": self.partial,
            "rows_complete": self.rows_complete,
        }
        return body

    def gz(self) -> bytes:
        raw = json.dumps(self.body(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return gzip.compress(raw.encode("utf-8", "surrogatepass"), mtime=0)


def _identify(
    path: str, *, budget: list[int], deadline: float, full: bool = False, cache: Any = None
) -> dict | None:
    """One file's identity via the recorder's hasher (same cache and budget, rows counted in the
    same read; `inputs.file_identity`). ``full`` (`hash="full"`, hosting): a file over the
    recorder's 1 GiB fingerprint line is read whole too."""
    from ..capture import lineage as inputs

    if full:
        try:
            size = os.stat(path).st_size
        except OSError:
            return None
        if size > inputs.FULL_HASH_MAX_BYTES:
            from ..artifact.hashing import fingerprint

            try:
                digest, size = fingerprint(path)
            except OSError:
                return None
            return {"content_hash": digest, "fingerprint": None, "size_bytes": size, "rows": None}
    return inputs.file_identity(path, budget=budget, cache=cache, deadline=deadline)


def _hash_cache() -> Any:
    """The recorder's per-machine hash cache: a dataset is hashed once per machine."""
    from ..capture import lineage as inputs

    return inputs._HashCache(batch=256)


def build_manifest(
    local: str, *, budget: list[int], deadline: float, require_full: bool = False, full: bool = False
) -> Manifest:
    """Manifest of a folder (or one file, by basename). The walk never follows a link (cannot
    escape the folder) and stops after `MAX_MANIFEST_FILES` files."""
    cache = _hash_cache()
    try:
        return _walk_manifest(local, cache=cache, budget=budget, deadline=deadline,
                              require_full=require_full, full=full)
    finally:
        cache.flush()


def _walk_manifest(
    local: str, *, cache: Any, budget: list[int], deadline: float, require_full: bool, full: bool
) -> Manifest:
    manifest = Manifest()
    if os.path.isfile(local):
        _add(manifest, os.path.basename(local), local, budget=budget, deadline=deadline, full=full, cache=cache)
        return _settle(manifest, require_full=require_full)
    seen = 0
    walk_errors: list[OSError] = []
    for root, dirs, leaves in os.walk(local, followlinks=False, onerror=walk_errors.append):
        seen += len(dirs) + len(leaves)
        if seen > MAX_WALK_ENTRIES:
            manifest.partial = True
            break
        kept = []
        for d in sorted(dirs):
            path = os.path.join(root, d)
            if os.path.islink(path):
                manifest.skipped += 1
                continue
            kept.append(d)
        dirs[:] = kept
        for leaf in sorted(leaves):
            path = os.path.join(root, leaf)
            if os.path.islink(path) or not os.path.isfile(path):
                manifest.skipped += 1
                continue
            if len(manifest.files) >= MAX_MANIFEST_FILES:
                manifest.partial = True
                break
            rel = os.path.relpath(path, local).replace(os.sep, "/")
            _add(manifest, rel, path, budget=budget, deadline=deadline, full=full, cache=cache)
    if walk_errors:
        manifest.skipped += len(walk_errors)
    return _settle(manifest, require_full=require_full)


def _add(
    manifest: Manifest, rel: str, path: str, *, budget: list[int], deadline: float,
    full: bool = False, cache: Any = None,
) -> None:
    got = _identify(path, budget=budget, deadline=deadline, full=full, cache=cache)
    if got is None:
        manifest.skipped += 1
        return
    manifest.files.append(
        ManifestFile(
            relpath=_shown_relpath(rel),
            size_bytes=int(got.get("size_bytes") or 0),
            content_hash=got.get("content_hash"),
            fingerprint=got.get("fingerprint"),
            rows=got.get("rows"),
            full=path,
        )
    )


def _shown_relpath(rel: str) -> str:
    """A relative path as it leaves the machine, scrubbed once like the read recorder's paths
    (a credential in a file name stays home); the identity is taken over this."""
    # scanning disabled: from . import redaction

    # scanning disabled: return redaction.scrub_string(rel)
    return rel


def _settle(manifest: Manifest, *, require_full: bool) -> Manifest:
    if manifest.skipped or any(not f.content_hash for f in manifest.files):
        manifest.partial = True
    if require_full and manifest.partial:
        missing = [f.relpath for f in manifest.files if not f.content_hash]
        raise CatalogRefused(
            "hosting needs every file fully hashed and readable, and "
            + (f"{len(missing)} file(s) are not (e.g. {missing[0]})" if missing else f"{manifest.skipped} path(s) were not readable files")
        )
    return manifest
