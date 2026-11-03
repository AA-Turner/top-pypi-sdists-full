"""Stage an immutable file copy within the outbox's disk budget, verify it is unchanged, delete unread copies."""

from __future__ import annotations
import os
import shutil
import time
from pathlib import Path
from typing import Any

from .... import errors
from .....foundation.durable.durable import file_lock, fsync_directory, try_clone
from probe.sdk.artifact.storage_handlers.multipart.queue import _live_op_ids
#: An orphaned staged copy (its op gone) is kept this long before gc.
_ORPHAN_GRACE_SECONDS = 3600


def staged_dir(journal: Any) -> Path:
    return Path(journal.dir) / "multipart" / "staged"


def _private(path: Path) -> Path:
    """``path`` and ``multipart/`` above it, owner-only (0700) whatever the umask."""
    Path(path.parent.parent).mkdir(parents=True, exist_ok=True)
    for level in (path.parent, path):
        try:
            level.mkdir(mode=0o700)
        except FileExistsError:
            pass
        try:
            os.chmod(level, 0o700)
        except OSError:
            pass
    return path


def _identity(st: os.stat_result) -> dict:
    # Not ctime: making the hardlink itself changes it.
    return {
        "dev": st.st_dev,
        "ino": st.st_ino,
        "size": st.st_size,
        "mtime_ns": st.st_mtime_ns,
    }


def _free_bytes(directory: Path) -> int:
    return shutil.disk_usage(directory).free


def _floor(journal: Any) -> int:
    """The outbox's own free-space floor (#2054), 0 when it has none."""
    try:
        return max(0, int(journal._free_floor()))
    except Exception:  # noqa: BLE001 -- no floor known: no floor
        return 0


def _pinned(journal: Any, directory: Path) -> tuple[int, int]:
    """(bytes, count) of the staged copies of uploads still queued."""
    live = _live_op_ids(journal)
    total = count = 0
    for op_id in live:
        try:
            total += (directory / f"{op_id}.src").stat().st_size
            count += 1
        except OSError:
            continue
    return total, count


class StageRefused(Exception):
    """Could not stage within the budget; the caller records a reference row and warns."""


def stage(journal: Any, src: str, op_id: str, *, allow_copy: bool = True) -> dict:
    """Make the immutable copy the upload reads. Returns the op's ``multipart`` staging
    fields; raises `StageRefused` with the reason.

    ``allow_copy=False`` refuses rather than copy: output capture stages at run close
    on the caller's thread, where a gigabyte cross-filesystem copy has no deadline (D18); it keeps a pointer."""
    directory = _private(staged_dir(journal))
    dest = directory / f"{op_id}.src"
    size = os.stat(src).st_size
    floor = _floor(journal)
    free = _free_bytes(directory)
    pinned, waiting = _pinned(journal, directory)
    if free - floor < pinned + size:
        mib = 1 << 20
        raise StageRefused(
            f"it could not be staged for a later upload: {free // mib} MiB free on the outbox's "
            f"disk, less its {floor // mib} MiB floor, does not cover its {size // mib} MiB"
            + (f" and the {pinned // mib} MiB of {waiting} upload(s) still waiting" if waiting else "")
        )
    mode = "hardlink"
    try:
        os.link(src, dest)
    except OSError:
        temporary = directory / f".{op_id}.tmp"
        temporary.unlink(missing_ok=True)
        try:
            if try_clone(src, str(temporary)):
                mode = "reflink"
            elif not allow_copy:
                raise StageRefused(
                    "it is on another filesystem than the outbox, and output capture does not "
                    "copy a big file at a run's close"
                )
            else:
                shutil.copyfile(src, temporary)
                mode = "copy"
            os.chmod(temporary, 0o600)
            os.replace(temporary, dest)
        finally:
            temporary.unlink(missing_ok=True)
    fsync_directory(directory)
    return {
        "staged_path": str(dest),
        "stage_mode": mode,
        "identity": _identity(os.stat(dest)),
        "staged_at": time.time(),
    }


def gc_staging(journal: Any, *, now: float | None = None) -> int:
    """Delete staged files nothing will read: a copy whose op is gone and a kill-cut
    partial (``.<op>.tmp``), once `_ORPHAN_GRACE_SECONDS` old. A LIVE op's copy is
    left (the op gives up after 7 days, `advance`). Ages by ctime (a hardlink's
    mtime is its source's). Returns how many went."""
    directory = staged_dir(journal)
    try:
        names = os.listdir(directory)
    except FileNotFoundError:
        return 0
    now = time.time() if now is None else now
    # Under the queue's append lock, as `outbox/held` moves an op between ops/ and held/: a move
    # between this scan's two listings would read as no op at all and lose the copy (R9).
    with file_lock(Path(journal.dir) / ".append.lock"):
        return _remove_unread(directory, names, _live_op_ids(journal), now)


def _remove_unread(directory: Path, names: list, live: set, now: float) -> int:
    removed = 0
    for name in names:
        partial = name.startswith(".") and name.endswith(".tmp")
        if not partial and name.split(".", 1)[0] in live:
            continue
        path = directory / name
        try:
            age = now - path.stat().st_ctime
        except FileNotFoundError:
            continue
        if age > _ORPHAN_GRACE_SECONDS:
            path.unlink(missing_ok=True)
            removed += 1
    return removed


def release_staged(state: dict) -> None:
    """Delete this upload's staged copy (never the caller's own file)."""
    if state.get("stage_mode") not in ("hardlink", "reflink", "copy"):
        return
    path = state.get("staged_path")
    if path:
        Path(path).unlink(missing_ok=True)


def _check_staged(state: dict) -> None:
    """The staged copy is unchanged, or nothing more is sent (permanent: the drain records a reference row)."""
    try:
        st = os.stat(state["staged_path"])
    except FileNotFoundError:
        raise errors.ValidationError(
            "the staged copy of this artifact is gone", status=422
        ) from None
    if _identity(st) != state["identity"]:
        raise errors.ValidationError(
            "the staged copy of this artifact changed while it was uploading (a hardlink "
            "shares the file the program rewrote in place); nothing more is sent",
            status=422,
        )
