"""write the pending files into a verified, reproducible tar.gz, re-checking each file against its manifest entry."""

from __future__ import annotations
import contextlib
import hashlib
import os
import stat
from typing import Any, Literal
from probe.sdk.capture.code.code import SnapshotError, SnapshotTooLarge, is_inside_tree
from probe.sdk.capture.code.sources.directory import DEFAULT_MAX_UPLOAD_BYTES


def _file_sha256(path: str) -> tuple[str, int]:
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n


class _ChangedUnderStream(SnapshotError):
    """A file's bytes changed between its verification read and the read that
    streamed it into the tar; the wrong member is already written. Carries the
    path so the builder can rebuild once with that file reported as changed."""

    def __init__(self, path: str) -> None:
        super().__init__(
            f"{path!r} changed while it was being archived; the archive is discarded"
        )
        self.path = path


def pending_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """The files git cannot supply -- edited, untracked, unpushed, or no remote.

    These are exactly the files that make a run unreproducible on any other
    machine: the manifest records a sha256 for them, and a sha256 verifies a file
    you already have rather than producing one you do not.

    ``source="reference"`` is deliberately excluded: those are the deliberately
    off-platform ones (a base checkpoint on a shared volume), identified and
    verifiable but not copied.
    """
    return [e for e in (manifest.get("entries") or []) if e.get("source") == "blob"]


def build_pending_archive(
    cwd: str,
    manifest: dict[str, Any],
    dest: str,
    *,
    max_bytes: int = DEFAULT_MAX_UPLOAD_BYTES,
) -> dict[str, Any]:
    """Tar+gzip exactly the pending files into ``dest``. Returns a summary.

    DETERMINISTIC: mtime, uid/gid, owner names and member order are all
    normalised, and gzip's own mtime header is zeroed. Two identical trees
    therefore produce byte-identical archives, which is what lets the upload's
    content-addressed ``have`` check short-circuit -- a 200-run sweep over
    unchanged code uploads once and skips the other 199.

    Modes and symlinks survive: the manifest already distinguishes ``100755``
    from ``100644`` and records ``symlink_target`` for ``120000`` entries, and a
    restored tree that lost the executable bit does not run.

    Raises :class:`SnapshotTooLarge` rather than dropping files to fit.

    A tree that DRIFTED since the manifest was taken (a log the training job is
    still appending to, a results file rewritten, a temp file gone) is not an
    error and not a reason to store nothing: every regular file is hashed as it
    streams into the tar and compared to the manifest's ``sha256``/``size``,
    every symlink's target to ``symlink_target``, and the ones that still match
    are archived. The ones that do not are left out and NAMED -- ``missing`` and
    ``changed`` in the summary, ``n_files`` = what was actually written -- so the
    caller records them as unstored and a reader sees exactly which files this
    run is missing. What used to happen here was the silent version: a missing
    file was skipped and ``n_files`` still claimed it (an archive recorded as
    7,689 files held 316).

    Two things DO raise :class:`SnapshotError`: a manifest entry with no
    ``sha256``/``size`` (a malformed record, never archived unverified) and a
    file that shrank while its bytes were streaming (the tar member is already
    short, so the archive cannot be continued). Both leave nothing on disk.
    """
    pending = pending_entries(manifest)
    total = sum(int(e.get("size") or 0) for e in pending)
    if total > max_bytes:
        raise SnapshotTooLarge(
            f"pending code bytes are {total / 1e6:.1f} MB, over the "
            f"{max_bytes / 1e6:.0f} MB cap; raise --max-upload-mb, or lower "
            "--reference-over-mb so the large files are recorded where they "
            "live instead of copied"
        )


    # gzip mtime=0 AND filename="" so the container header is deterministic too,
    # not just the tar. Without the explicit filename, GzipFile copies the output
    # file's own name into the header -- so writing the same tree to two paths
    # produced two different hashes and the upload's content-addressed dedup
    # never fired. A test pins this.
    # A file whose bytes change between its verification read and the streamed
    # read has already put a wrong member in the tar. A sqlite file or an mmap'd
    # progress array rewritten in place at constant size can do that on every
    # snapshot, so the archive is rebuilt ONCE with that file reported as
    # changed; a second such file in the rebuild is genuinely a tree that will
    # not hold still, and raises.
    exclude: set[str] = set()
    for _attempt in (1, 2):
        try:
            missing, changed, written, written_bytes = _build_archive_once(
                cwd, pending, dest, exclude
            )
            break
        except _ChangedUnderStream as exc:
            if _attempt == 2:
                raise SnapshotError(f"{exc}; re-run the snapshot") from exc
            exclude.add(exc.path)

    sha, size = _file_sha256(dest)
    return {
        "path": dest,
        "sha256": sha,
        "size_bytes": size,
        "n_files": written,
        "uncompressed_bytes": written_bytes,
        "missing": missing,
        "changed": changed,
        "drift_message": (
            _partial_archive_message(missing, changed) if (missing or changed) else None
        ),
    }


_Verdict = Literal["written", "missing", "changed"]


def _build_archive_once(
    cwd: str, pending: list[dict[str, Any]], dest: str, exclude: set[str]
) -> tuple[list[str], list[str], int, int]:
    """One pass over ``pending`` into a fresh ``dest``. Paths in ``exclude`` are
    reported changed without being read. Any exception unlinks ``dest``."""
    import gzip
    import tarfile

    missing: list[str] = []
    changed: list[str] = []
    written = 0
    written_bytes = 0
    try:
        # Level 6, not the default 9: measured on a 7,902-file / 152 MB tree,
        # level 9 was ~60% of this function's wall time (14.1 s vs 5.6 s) for
        # 0.3% smaller output. Any fixed level keeps the archive deterministic.
        with open(dest, "wb") as raw, gzip.GzipFile(
            filename="", fileobj=raw, mode="wb", mtime=0, compresslevel=6
        ) as gz:
            with tarfile.open(fileobj=gz, mode="w") as archive:
                for entry in sorted(pending, key=lambda e: str(e.get("path"))):
                    path = entry.get("path")
                    verdict = "changed" if path in exclude else _archive_entry(archive, cwd, entry)
                    if verdict == "missing":
                        missing.append(path)
                    elif verdict == "changed":
                        changed.append(path)
                    else:
                        written += 1
                        written_bytes += int(entry.get("size") or 0)
    except BaseException:
        # Whatever interrupted the write, never leave a partial archive behind.
        with contextlib.suppress(OSError):
            os.unlink(dest)
        raise
    return missing, changed, written, written_bytes

#: How many drifted paths ride on the artifact meta / return dict. The COUNT is
#: never capped (``pending_upload`` is exact); the list is, because a tree that
#: drifted by thousands of files does not need thousands of names on one row.
DRIFTED_META_LIMIT = 50
_HASH_CHUNK = 1 << 20


def _archive_entry(archive: Any, cwd: str, entry: dict[str, Any]) -> _Verdict:
    """Verify ONE manifest entry against the working tree and stream it into
    ``archive`` if it still matches. Returns ``"written"``, ``"missing"`` or
    ``"changed"``. Raises SnapshotError for a malformed entry, a path that would
    leave the tree, a file that shrank or changed while its bytes were entering
    the tar, or an archive write failure -- every one leaves nothing on disk.

    Source-side surprises are verdicts, never exceptions: the file is opened
    with ``O_NOFOLLOW | O_NONBLOCK`` so a symlink or FIFO swapped in between the
    ``lstat`` and the ``open`` is refused on the descriptor instead of followed
    or blocked on; ``fstat`` re-checks "regular file of the recorded size"; the
    file is hashed BEFORE it is streamed (bounded to the recorded size, so a
    log that grew keeps its recorded prefix and archives as recorded), and
    hashed again as it streams. A mismatch on that second hash means the bytes
    changed inside the window between the two reads and a wrong member is
    already in the tar: that aborts the archive rather than uploading unverified
    bytes under a verified name.
    """
    import tarfile

    path = entry.get("path")
    if not isinstance(path, str) or not is_inside_tree(path):
        raise SnapshotError(f"manifest entry path {path!r} is not a relative path inside the tree")
    full = os.path.join(cwd, path)
    mode = entry.get("mode")

    if mode == "120000":
        recorded = entry.get("symlink_target")
        if not isinstance(recorded, str):
            raise SnapshotError(f"manifest entry {path!r} is a symlink with no recorded target")
        try:
            target = os.readlink(full)
        except FileNotFoundError:
            return "missing"
        except OSError:
            return "changed"  # not a symlink any more, or unreadable
        if target != recorded:
            return "changed"
        info = tarfile.TarInfo(path)
        info.type = tarfile.SYMTYPE
        info.linkname = recorded
        _normalise_member(info)
        _write_member(archive, info, None, path)
        return "written"

    verdict, fh = open_verified_file(cwd, entry)
    if verdict != "ok" or fh is None:
        return verdict  # "missing" | "changed"
    expected_size = int(entry["size"])
    expected_sha = entry["sha256"]
    with fh:
        info = tarfile.TarInfo(path)
        info.size = expected_size
        info.mode = 0o755 if mode == "100755" else 0o644
        _normalise_member(info)
        reader = _HashingReader(fh)
        _write_member(archive, info, reader, path, expected_size)
    if reader.hexdigest() != expected_sha:
        raise _ChangedUnderStream(path)
    return "written"


def open_verified_file(cwd: str, entry: dict[str, Any]) -> tuple[str, Any]:
    """Open ONE manifest entry's regular file only if it still matches its
    record, and hand back the descriptor positioned at byte 0.

    Returns ``("ok", fh)`` -- the caller owns and closes ``fh`` -- or
    ``("missing", None)`` / ``("changed", None)``. The file is opened with
    ``O_NOFOLLOW | O_NONBLOCK`` so a symlink or FIFO swapped in since the
    manifest is refused on the descriptor instead of followed or blocked on;
    ``fstat`` re-checks "regular file of the recorded size"; the bytes are hashed
    (bounded to the recorded size) BEFORE anything reads them again, so a
    consumer that streams the same descriptor sends exactly the bytes that were
    verified. Shared by the archive and the per-file capture paths: whatever
    leaves the machine has been checked against the record the same way.
    Raises SnapshotError for a malformed entry or a path that leaves the tree.
    """
    path = entry.get("path")
    if not isinstance(path, str) or not is_inside_tree(path):
        raise SnapshotError(f"manifest entry path {path!r} is not a relative path inside the tree")
    full = os.path.join(cwd, path)
    expected_sha = entry.get("sha256")
    size = entry.get("size")
    if not isinstance(expected_sha, str) or not expected_sha or isinstance(size, bool):
        raise SnapshotError(f"manifest entry {path!r} has no sha256/size; the record is malformed")
    try:
        expected_size = int(size)
    except (TypeError, ValueError):
        raise SnapshotError(f"manifest entry {path!r} has no sha256/size; the record is malformed") from None
    if expected_size < 0:
        raise SnapshotError(f"manifest entry {path!r} has a negative size; the record is malformed")

    try:
        st = os.lstat(full)
    except FileNotFoundError:
        return "missing", None
    except OSError:
        return "changed", None
    if not stat.S_ISREG(st.st_mode) or st.st_size != expected_size:
        return "changed", None
    # Every flag guarded: Windows has neither O_NONBLOCK nor O_NOFOLLOW, and an
    # AttributeError here would escape the fail-open handler.
    flags = (
        os.O_RDONLY
        | getattr(os, "O_NONBLOCK", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_BINARY", 0)
    )
    try:
        fd = os.open(full, flags)
    except FileNotFoundError:
        return "missing", None
    except OSError:
        return "changed", None  # ELOOP (a symlink now), ENXIO, EACCES, ...
    fh = os.fdopen(fd, "rb")
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size != expected_size:
            fh.close()
            return "changed", None
        _clear_nonblock(fd)
        pre = _HashingReader(fh)
        remaining = expected_size
        while remaining:
            chunk = pre.read(min(_HASH_CHUNK, remaining))
            if not chunk:
                break
            remaining -= len(chunk)
        if pre.bytes_read != expected_size or pre.hexdigest() != expected_sha:
            fh.close()
            return "changed", None
        fh.seek(0)
    except OSError:
        fh.close()
        return "changed", None
    return "ok", fh


def _clear_nonblock(fd: int) -> None:
    """Drop O_NONBLOCK after the descriptor proved to be a regular file (it was
    only there so a swapped-in FIFO could not block the open). No-op where the
    flag or fcntl does not exist (Windows)."""
    nonblock = getattr(os, "O_NONBLOCK", 0)
    if not nonblock:
        return
    try:
        import fcntl
    except ImportError:
        return
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) & ~nonblock)


def _write_member(archive: Any, info: Any, reader: Any, path: str, expected_size: int = 0) -> None:
    """One place for every archive write, so a write-side failure (ENOSPC, EIO,
    a file that shrank under the stream) is ALWAYS an abort with a precise
    message -- never mistaken for source drift and carried on from."""
    try:
        if reader is None:
            archive.addfile(info)
        else:
            archive.addfile(info, reader)
    except OSError as exc:
        if reader is not None and reader.bytes_read < expected_size:
            raise SnapshotError(
                f"{path!r} shrank while it was being archived; the archive is discarded, "
                "re-run the snapshot"
            ) from exc
        raise SnapshotError(f"writing {path!r} to the archive failed: {exc}") from exc


def _normalise_member(info: Any) -> None:  # tarfile.TarInfo; tarfile is imported lazily
    """Zero every field that would make two identical trees hash differently."""
    info.mtime = 0
    info.uid = info.gid = 0
    info.uname = info.gname = ""


class _HashingReader:
    """Hashes exactly the bytes pulled through it and counts them. Used twice per
    file: once to verify the file BEFORE it is streamed (bounded to the recorded
    size), once on the bytes ``tarfile`` actually pulls into the archive."""

    def __init__(self, fh) -> None:
        self._fh = fh
        self._h = hashlib.sha256()
        self.bytes_read = 0

    def read(self, n: int = -1) -> bytes:
        chunk = self._fh.read(n)
        self._h.update(chunk)
        self.bytes_read += len(chunk)
        return chunk

    def hexdigest(self) -> str:
        return self._h.hexdigest()


_PARTIAL_LIST_LIMIT = 5


def _partial_archive_message(missing: list[str], changed: list[str]) -> str:
    def _show(paths: list[str]) -> str:
        head = ", ".join(paths[:_PARTIAL_LIST_LIMIT])
        extra = len(paths) - _PARTIAL_LIST_LIMIT
        return head + (f", +{extra} more" if extra > 0 else "")

    parts = []
    if missing:
        parts.append(f"{len(missing)} missing from the working tree ({_show(missing)})")
    if changed:
        parts.append(f"{len(changed)} changed since the manifest was taken ({_show(changed)})")
    return (
        "left out of the archive because the tree no longer matched its manifest: "
        + "; ".join(parts)
        + ". Re-run the snapshot to capture them."
    )
