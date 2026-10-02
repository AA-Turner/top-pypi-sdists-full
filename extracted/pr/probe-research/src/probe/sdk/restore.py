"""Rebuild a snapshotted working tree, or say exactly what is missing.

The inverse of ``capture_manifest`` + the per-file (or ``code-bytes``) upload.
Each manifest entry names one of two sources, and this resolves both:

    source="git"   -> `git cat-file blob <blob>` from the recorded remote
    source="blob"  -> the run's per-file capture row (kind=code), or a member of
                      the code-bytes archive for runs stored that way

Every restored file is verified against the ``sha256`` the manifest recorded, and
the rebuilt tree is verified against ``tree_sha256``. A hash mismatch makes the
file UNAVAILABLE; it is never written and then hoped about. That rule is
inherited from ``probe.sandbox-state/1``, where bytes are served from a shared
archive only when the per-file hash agrees -- degrade to "unavailable", never to
a wrong answer.
"""

from __future__ import annotations

import gzip
import hashlib
import os
import subprocess
import tarfile
import tempfile
from collections.abc import Callable
from typing import Any

from .errors import RosError
from .snapshot import _NONINTERACTIVE_ENV, _file_sha256, is_inside_tree, tree_digest, wire_name

#: A depth-1 fetch of one commit. Bounded for the same reason every other remote
#: call here is: an audit of many runs must not wedge on one unreachable host.
FETCH_TIMEOUT = 120.0


class RestoreError(RosError):
    """The snapshot cannot be rebuilt from what was recorded."""


def _fetch_base(remote: str, commit: str, workdir: str) -> bool:
    """Materialise ``commit`` in a throwaway repo. False if it cannot be had.

    A depth-1 fetch of the commit brings its whole tree, so every ``source="git"``
    blob becomes readable from one network call rather than one per file.
    """
    subprocess.run(
        ["git", "init", "-q", "."], cwd=workdir, capture_output=True, text=True
    )
    try:
        proc = subprocess.run(
            ["git", "fetch", "--depth", "1", "--quiet", remote, commit],
            cwd=workdir,
            capture_output=True,
            text=True,
            env=_NONINTERACTIVE_ENV(),
            timeout=FETCH_TIMEOUT,
        )
    except (subprocess.TimeoutExpired, OSError):
        return False
    return proc.returncode == 0


def _write(dest_root: str, entry: dict, data: bytes | None, link: str | None) -> None:
    """Write one restored entry under ``dest_root`` -- and only under it.

    The manifest is server data. A symlink entry ``a -> /anywhere`` followed by a
    file entry ``a/victim.txt`` would otherwise make ``makedirs`` follow the link
    and ``unlink`` + ``open`` land OUTSIDE the destination (found by review).
    So no parent component of the target may be a symlink, and the parent's
    real path must sit inside the destination's real path, checked right before
    the write. A symlink AT the target is unlinked, never followed.
    """
    root = os.path.realpath(dest_root)
    target = os.path.join(dest_root, entry["path"])
    parent = os.path.dirname(target) or dest_root
    rel = os.path.relpath(parent, dest_root)
    probe = dest_root
    for component in () if rel == "." else rel.split(os.sep):
        probe = os.path.join(probe, component)
        if os.path.islink(probe):
            raise RestoreError(f"refusing to write {entry['path']!r} through a symlinked directory")
    os.makedirs(parent, exist_ok=True)
    real_parent = os.path.realpath(parent)
    if real_parent != root and not real_parent.startswith(root + os.sep):
        raise RestoreError(f"refusing to write {entry['path']!r} outside the destination")
    if os.path.lexists(target):
        if os.path.isdir(target) and not os.path.islink(target):
            raise RestoreError(f"refusing to replace directory {entry['path']!r} with a file")
        os.unlink(target)
    if link is not None:
        os.symlink(link, target)
        return
    with open(target, "wb") as fh:
        fh.write(data or b"")
    # A restored tree whose entrypoint lost +x does not run.
    if entry.get("mode") == "100755":
        os.chmod(target, 0o755)


def restore_snapshot(
    manifest: dict[str, Any],
    dest: str,
    *,
    archive_path: str | None = None,
    blob_fetch: Callable[[list[dict[str, Any]]], dict[str, bytes | None]] | None = None,
    verify_only: bool = False,
) -> dict[str, Any]:
    """Rebuild the tree described by ``manifest`` into ``dest``.

    ``archive_path`` is the downloaded ``code-bytes`` tarball, or None when the
    snapshot had nothing pending (or when the caller could not fetch it -- in
    which case those files are reported unavailable rather than silently absent).

    ``blob_fetch`` is the per-file source (0193, the default): given the ``source="blob"``
    entries, it returns a mapping ``{path: bytes}`` for the ones it could fetch
    (a missing key, or ``None``, means "no captured bytes for this file"; a
    mapping with a ``reasons`` attribute names WHY per path). It is consulted
    before the archive, so a run whose files were captured as artifact rows
    restores without any tarball, and a run that holds both takes each file
    from whichever has it; every byte is still verified against the manifest's
    sha256 here, exactly like the archive path. ``capture_blob_fetch`` is the
    SDK's implementation over a run's capture rows.

    ``verify_only`` resolves and hashes everything without writing, which is how
    a fleet gets swept for "which of these can actually be rebuilt?".

    Returns ``{"files": [...], "n_restored", "n_unavailable", "tree_sha256",
    "tree_matches"}``. Each file carries ``path``, ``source``, ``status``
    (``restored`` | ``verified`` | ``unavailable``) and, when unavailable, a
    ``reason``.
    """
    entries = manifest.get("entries") or []
    if not entries:
        raise RestoreError("manifest carries no entries; nothing to restore")
    for entry in entries:
        if not isinstance(entry, dict) or not all(
            isinstance(entry.get(k), str) for k in ("path", "mode", "sha256")
        ):
            # Checked BEFORE any file is written: a KeyError halfway through a
            # restore would leave a half-built tree with no report.
            raise RestoreError(f"manifest entry is malformed: {entry!r}"[:300])

    # source="blob" members, keyed by path.
    archived: dict[str, tarfile.TarInfo] = {}
    tar: tarfile.TarFile | None = None
    gz = None
    if archive_path and os.path.isfile(archive_path):
        gz = gzip.open(archive_path, "rb")
        tar = tarfile.open(fileobj=gz, mode="r")
        archived = {m.name: m for m in tar.getmembers()}

    fetched: Any = None
    if blob_fetch is not None:
        wanted = [e for e in entries if e.get("source") == "blob" and e.get("mode") != "120000"]
        try:
            fetched = blob_fetch(wanted)
        except RosError as exc:
            # The store said no for the whole batch (retention lock, storage
            # down). Every captured file reads as unavailable with that reason
            # instead of the restore dying with a traceback.
            fetched = _Unavailable(f"download refused: {exc}", [e["path"] for e in wanted])
    tmp_repo: str | None = None
    have_git = False
    needs_git = any(e.get("source") == "git" for e in entries)
    remote = manifest.get("remote")
    base = manifest.get("base_commit")
    if needs_git and remote and base:
        tmp_repo = tempfile.mkdtemp(prefix="probe-restore-")
        have_git = _fetch_base(str(remote), str(base), tmp_repo)

    results: list[dict[str, Any]] = []
    if not verify_only:
        os.makedirs(dest, exist_ok=True)

    try:
        for entry in sorted(entries, key=lambda e: str(e.get("path"))):
            path, source = entry.get("path"), entry.get("source")
            if not isinstance(path, str) or not is_inside_tree(path):
                # A manifest is data from the server; a path that would land
                # outside `dest` is refused before any branch touches disk.
                results.append(
                    {
                        "path": str(path),
                        "source": source,
                        "status": "unavailable",
                        "reason": "path is not a relative path inside the tree",
                    }
                )
                continue
            data: bytes | None = None
            link: str | None = None
            reason: str | None = None

            if entry.get("mode") == "120000":
                link = entry.get("symlink_target")
                if link is None and source == "blob" and path in archived:
                    link = archived[path].linkname
                if link is None:
                    reason = "symlink target not recorded"
            elif source == "git":
                if not have_git:
                    reason = (
                        f"cannot fetch {str(base)[:12] if base else 'base'} from "
                        f"{remote or 'no recorded remote'}"
                    )
                else:
                    proc = subprocess.run(
                        ["git", "cat-file", "blob", entry.get("blob", "")],
                        cwd=tmp_repo,
                        capture_output=True,
                    )
                    if proc.returncode == 0:
                        data = proc.stdout
                    else:
                        reason = f"blob {entry.get('blob', '')[:12]} not in the fetched commit"
            elif source == "reference":
                # Deliberately off-platform: too large to copy per run, so the
                # record identifies it rather than storing it. Not a failure and
                # not a restore -- reported as its own outcome so a reader knows
                # the file exists somewhere specific and is not here.
                results.append(
                    {
                        "path": path,
                        "source": source,
                        "status": "referenced",
                        "uri": entry.get("uri"),
                        "host": entry.get("host"),
                        "sha256": entry.get("sha256"),
                    }
                )
                continue
            elif source == "withheld":
                # Left out at capture because its content held a credential
                # (snapshot._ContentGate): never uploaded, so nothing to fetch.
                # Its own outcome, like a reference: not a failure of restore.
                results.append(
                    {
                        "path": path,
                        "source": source,
                        "status": "withheld",
                        "reason": entry.get("reason") or "secret",
                    }
                )
                continue
            elif source == "blob":
                if fetched is not None and fetched.get(path) is not None:
                    data = fetched[path]
                elif tar is None or path not in archived:
                    # Read AFTER the get above: a lazy fetch records its reasons
                    # as it loads. Never truth-test the mapping -- an empty one
                    # is still an answer. The rows were asked first, so their
                    # reason beats "not in the archive either".
                    reasons = getattr(fetched, "reasons", None) if fetched is not None else None
                    fetch_reason = reasons.get(path) if reasons is not None else None
                    if fetched is None:
                        reason = (
                            "code-bytes archive unavailable"
                            if tar is None
                            else "not present in the code-bytes archive"
                        )
                    elif tar is None:
                        reason = fetch_reason or "no captured bytes for this file"
                    else:
                        reason = fetch_reason or "not present in the code-bytes archive"
                else:
                    # Bounded by the recorded size: a hostile archive can declare
                    # a member far larger than the manifest says, and the sha
                    # check only runs after the read. A short or long member is a
                    # mismatch, reported exactly like wrong bytes.
                    expected = int(entry.get("size") or 0)
                    member = archived[path]
                    if member.size != expected:
                        reason = (
                            f"sha256 mismatch (archive member size {member.size} != recorded "
                            f"{expected})"
                        )
                    else:
                        stream = tar.extractfile(member)
                        data = stream.read(expected + 1) if stream is not None else b""
            else:
                reason = f"unknown source {source!r}"

            if reason is None and link is None:
                got = hashlib.sha256(data or b"").hexdigest()
                if got != entry.get("sha256"):
                    # Never write a file whose bytes disagree with the record.
                    reason = f"sha256 mismatch (recorded {str(entry.get('sha256'))[:12]})"

            if reason is not None:
                results.append(
                    {"path": path, "source": source, "status": "unavailable", "reason": reason}
                )
                continue

            if not verify_only:
                try:
                    _write(dest, entry, data, link)
                except (RestoreError, OSError) as exc:
                    results.append(
                        {"path": path, "source": source, "status": "unavailable", "reason": str(exc)}
                    )
                    continue
            results.append(
                {
                    "path": path,
                    "source": source,
                    "status": "verified" if verify_only else "restored",
                }
            )
    finally:
        if tar is not None:
            tar.close()
        if gz is not None:
            gz.close()
        if tmp_repo:
            subprocess.run(["rm", "-rf", tmp_repo], capture_output=True)

    unavailable = [r for r in results if r["status"] == "unavailable"]
    referenced = [r for r in results if r["status"] == "referenced"]
    withheld = [r for r in results if r["status"] == "withheld"]
    # Recompute the tree identity over what we actually produced. It can only
    # match when every file resolved, which is precisely the claim being made.
    tree = tree_digest(entries)

    return {
        "files": results,
        "n_restored": len(results) - len(unavailable) - len(referenced) - len(withheld),
        "n_unavailable": len(unavailable),
        # Held a credential at capture and was never uploaded.
        "n_withheld": len(withheld),
        "withheld": [r["path"] for r in withheld],
        # Off-platform by design, so NOT counted as a failure -- but the tree on
        # disk is still incomplete, so `tree_matches` stays False. A reader has to
        # be able to tell "rebuilt" from "rebuilt except the 40GB checkpoint".
        "n_referenced": len(referenced),
        "referenced": [
            {"path": r["path"], "uri": r.get("uri"), "host": r.get("host")}
            for r in referenced
        ],
        "tree_sha256": tree,
        "tree_matches": (
            tree == manifest.get("tree_sha256")
            and not unavailable
            and not referenced
            and not withheld
        ),
    }


def verify_restored_tree(manifest: dict[str, Any], root: str) -> list[str]:
    """Paths under ``root`` whose bytes disagree with the manifest, or are absent.

    Used after a restore to prove the tree on disk is the tree that was recorded,
    rather than trusting that the writes went where they were told.
    """
    bad: list[str] = []
    for entry in manifest.get("entries") or []:
        target = os.path.join(root, entry["path"])
        if entry.get("mode") == "120000":
            if not os.path.islink(target) or os.readlink(target) != entry.get(
                "symlink_target"
            ):
                bad.append(entry["path"])
            continue
        if not os.path.isfile(target):
            bad.append(entry["path"])
            continue
        if _file_sha256(target)[0] != entry.get("sha256"):
            bad.append(entry["path"])
    return bad


# --- per-file capture rows (0193) --------------------------------------------

#: One `download/batch` call per this many ids (the server's cap).
CAPTURE_DOWNLOAD_BATCH = 1000
#: Files fetched per lazy batch, and how many of them at once. A batch is held
#: in memory only until the restore loop walks past it, so a 4,600-file tree
#: costs one batch of bytes at a time, not the whole tree.
CAPTURE_FETCH_BATCH = 256
CAPTURE_GET_WORKERS = 16


def capture_rows(client: Any, run_id: str) -> list[dict[str, Any]]:
    """The run's COMPLETE per-file capture rows: ``kind='code'`` artifacts
    carrying ``meta.capture == 'code-snapshot'`` whose bytes landed. A pending
    or failed row holds nothing restorable and is left out on purpose. Empty
    for a run captured as an archive."""
    rows = client.list_run_artifacts(run_id, kind="code") or []
    return [
        r
        for r in rows
        if (r.get("meta") or {}).get("capture") == "code-snapshot"
        and r.get("status") == "complete"
    ]


class _Unavailable(dict):
    """A fetch that could not even ask: every path it was asked for carries the
    batch's reason. A real dict of reasons, not a "same answer for any key"
    subclass -- an empty dict subclass is falsy and `or {}` swaps it out."""

    def __init__(self, reason: str, paths: list[str]) -> None:
        super().__init__()
        self.reasons: dict[str, str] = {p: reason for p in paths}


class _LazyBlobs(dict):
    """``{path: bytes}`` that fetches on demand in batches of
    ``CAPTURE_FETCH_BATCH`` (each batch ``CAPTURE_GET_WORKERS`` wide) and keeps
    only the batch being restored. The restore loop walks entries in manifest
    order, so the batch containing the requested path is loaded and the one
    before it is dropped. ``reasons`` names why a path has no bytes."""

    def __init__(self, order: list[str], load) -> None:
        super().__init__()
        self._order = order
        self._index = {p: i for i, p in enumerate(order)}
        self._load = load
        self._loaded: set[str] = set()
        self.reasons: dict[str, str] = {}

    def _ensure(self, path: str) -> None:
        if path in self._loaded or path not in self._index:
            return
        i = self._index[path]
        batch = self._order[i : i + CAPTURE_FETCH_BATCH]
        self.clear()
        loaded = self._load(batch)
        self.update(loaded)
        # Everything the loader returned counts as loaded -- a twin path served
        # by a row in this batch must not be presigned and fetched again later.
        self._loaded.update(loaded)
        for p in batch:
            self.setdefault(p, None)
            self._loaded.add(p)

    def get(self, path, default=None):  # noqa: D102 -- dict protocol
        self._ensure(path)
        return super().get(path, default)

    def __getitem__(self, path):
        self._ensure(path)
        return super().__getitem__(path)


def capture_blob_fetch(client: Any, rows: list[dict[str, Any]], *, warn=None):
    """A ``restore_snapshot`` blob_fetch over a run's capture rows.

    Each manifest entry is matched to its row by ``(name, sha256)`` -- the
    identity the server keys on, with the name NFC-normalised the way the server
    stores it -- never by env_ref: a run can hold several snapshots and the same
    bytes under the same path serve all of them. Downloads are presigned in
    chunks of ``CAPTURE_DOWNLOAD_BATCH`` and fetched lazily, ``CAPTURE_FETCH_BATCH``
    files at a time; a file with no row, a ``refused``/``unknown`` verdict, or a
    failed GET is absent from the result WITH its reason, and restore reports it
    by path. ``warn`` (optional) receives one line per problem."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    by_identity: dict[tuple[str, str], str] = {}
    for row in rows:
        by_identity.setdefault((row.get("name"), row.get("content_hash")), row["id"])

    def _say(message: str) -> None:
        if warn is not None:
            warn(message)

    def fetch(entries: list[dict[str, Any]]):
        wanted: dict[str, list[str]] = {}  # artifact id -> every manifest path it serves
        blobs = _LazyBlobs([e["path"] for e in entries], lambda batch: _load(batch))
        for entry in entries:
            name = wire_name(entry.get("path") or "")
            aid = by_identity.get((name, entry.get("sha256")))
            if aid is None:
                blobs.reasons[entry["path"]] = "no captured bytes for this file"
            else:
                # An NFC and an NFD spelling of one file with the same bytes share
                # one row; both paths are restored from it.
                wanted.setdefault(aid, []).append(entry["path"])
        path_to_aid = {p: a for a, paths in wanted.items() for p in paths}

        def _load(batch: list[str]) -> dict[str, bytes | None]:
            out: dict[str, bytes | None] = {}
            ids = list(dict.fromkeys(path_to_aid[p] for p in batch if p in path_to_aid))
            urls: dict[str, str] = {}
            for start in range(0, len(ids), CAPTURE_DOWNLOAD_BATCH):
                chunk = ids[start : start + CAPTURE_DOWNLOAD_BATCH]
                try:
                    presigned = client.presign_download_batch(chunk)
                except RosError as exc:
                    for aid in chunk:
                        for p in wanted[aid]:
                            blobs.reasons[p] = f"download refused: {exc}"
                    _say(f"warning: could not presign {len(chunk)} downloads: {exc}")
                    continue
                for aid, item in (presigned.get("items") or {}).items():
                    url = (item or {}).get("download_url")
                    if url and aid in wanted:
                        urls[aid] = url
                for aid, reason in (presigned.get("refused") or {}).items():
                    if aid in wanted:
                        for p in wanted[aid]:
                            blobs.reasons[p] = f"download refused: {reason}"
                for aid in presigned.get("unknown") or []:
                    if aid in wanted:
                        for p in wanted[aid]:
                            blobs.reasons[p] = "no live artifact row for this file"
            with ThreadPoolExecutor(max_workers=CAPTURE_GET_WORKERS) as pool:
                futures = {pool.submit(client.transport.get_url, url): aid for aid, url in urls.items()}
                for fut in as_completed(futures):
                    aid = futures[fut]
                    try:
                        data = fut.result()
                        for p in wanted[aid]:
                            out[p] = data
                    except Exception as exc:  # noqa: BLE001 -- reported per file by restore
                        for p in wanted[aid]:
                            blobs.reasons[p] = "download failed"
                            out[p] = None
                        _say(f"warning: could not download {', '.join(wanted[aid])}: {exc}")
            return out

        return blobs

    return fetch
