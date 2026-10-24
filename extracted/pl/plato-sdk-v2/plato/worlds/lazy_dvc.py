"""Lazy DVC workspace via FUSE — files appear present but content downloads on first read.

The FUSE filesystem is implemented as a Rust binary (plato-fuse) for performance.
The binary must be on PATH (installed to /usr/local/bin/plato-fuse in the base image).

On commit, ``smart_commit()`` builds a new .dir manifest without
re-downloading untouched files — only modified/new files are uploaded.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import signal
import time
from collections.abc import Callable
from pathlib import Path

from plato.utils.fuse_binary import (
    PLATO_FUSE_INSTALL_PATH,
    PLATO_FUSE_S3_BUCKET,
    PLATO_FUSE_S3_KEY,
    ensure_plato_fuse,
)
from plato.worlds.dvc_models import (
    DVCManifest,
    LazyDVCMount,
    S3Config,
    _env_flag_enabled,
)

__all__ = [
    "PLATO_FUSE_INSTALL_PATH",
    "PLATO_FUSE_S3_BUCKET",
    "PLATO_FUSE_S3_KEY",
    "mount_lazy",
    "unmount_lazy",
]

logger = logging.getLogger(__name__)


async def _forward_worker_logs(
    stream: asyncio.StreamReader | None,
    *,
    label: str,
    level: int = logging.INFO,
) -> None:
    if stream is None:
        return
    while True:
        line = await stream.readline()
        if not line:
            break
        logger.log(level, "plato_fuse[%s] %s", label, line.decode(errors="replace").rstrip())


async def _ensure_plato_fuse() -> str:
    """Return path to plato-fuse binary, downloading from S3 if not found."""
    binary, _source = await ensure_plato_fuse()
    return binary


async def mount_lazy(
    mountpoint: Path,
    manifest: DVCManifest,
    s3_config: S3Config,
    cache_dir: Path,
    *,
    phase_reporter: Callable[[str, float], None] | None = None,
) -> LazyDVCMount:
    """Mount a lazy FUSE filesystem at *mountpoint*.

    The FUSE loop runs in a child process so the parent's asyncio
    loop is never blocked by filesystem operations on the mount.
    """
    # Write config for the worker process
    started_at = time.monotonic()
    config_path = cache_dir / "config.json"
    for transient_path in (
        cache_dir / "live-meta.json",
        cache_dir / "live-dir-renames.json",
    ):
        transient_path.unlink(missing_ok=True)
    config_path.write_text(
        json.dumps(
            {
                "manifest": manifest.to_dict(),
                "s3_config": s3_config.to_dict(),
                "mountpoint": str(mountpoint),
                "cache_dir": str(cache_dir),
            }
        )
    )
    if phase_reporter is not None:
        phase_reporter("fuse_write_config", time.monotonic() - started_at)

    started_at = time.monotonic()
    (cache_dir / "overlay").mkdir(parents=True, exist_ok=True)
    (cache_dir / "cache").mkdir(parents=True, exist_ok=True)
    if phase_reporter is not None:
        phase_reporter("fuse_prepare_cache_dirs", time.monotonic() - started_at)

    # Start worker subprocess
    started_at = time.monotonic()
    rust_binary = await _ensure_plato_fuse()
    if phase_reporter is not None:
        phase_reporter("fuse_resolve_binary", time.monotonic() - started_at)

    started_at = time.monotonic()
    debug = _env_flag_enabled("PLATO_FUSE_DEBUG")
    # Its own session and its own log file: the mount keeps serving if this world process exits and a newer one
    # adopts it (handover.py). A pipe to this process would break, or fill up unread, once nobody reads it.
    log_path = cache_dir / "plato-fuse.log"
    log_file = None if debug else log_path.open("ab")
    try:
        proc = await asyncio.create_subprocess_exec(
            rust_binary,
            str(config_path),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE if debug else log_file,
            stderr=asyncio.subprocess.PIPE if debug else log_file,
            start_new_session=True,
        )
    finally:
        if log_file is not None:
            log_file.close()
    if phase_reporter is not None:
        phase_reporter("fuse_spawn_worker", time.monotonic() - started_at)
    worker_log_tasks: tuple[asyncio.Task[None], ...] | None = None
    if debug:
        worker_log_tasks = (
            asyncio.create_task(_forward_worker_logs(proc.stdout, label="stdout")),
            asyncio.create_task(_forward_worker_logs(proc.stderr, label="stderr")),
        )

    # Wait for the mount to appear (up to ~10 s)
    started_at = time.monotonic()
    for _ in range(100):
        if proc.returncode is not None:
            err = await _worker_error(proc, log_path, debug=debug)
            raise RuntimeError(f"FUSE subprocess exited early (rc={proc.returncode}): {err}")
        if os.path.ismount(str(mountpoint)):
            break
        await asyncio.sleep(0.1)
    else:
        try:
            proc.kill()
            await asyncio.wait_for(proc.wait(), timeout=5)
            err = await _worker_error(proc, log_path, debug=debug)
        except Exception:
            err = "unknown"
        raise RuntimeError(f"FUSE mount at {mountpoint} did not appear: {err}")
    if phase_reporter is not None:
        phase_reporter("fuse_wait_for_mount", time.monotonic() - started_at)

    logger.debug("Lazy DVC mounted at %s (%d files)", mountpoint, len(manifest.entries_list))
    return LazyDVCMount(
        mountpoint=mountpoint,
        cache_dir=cache_dir,
        manifest=manifest,
        worker_proc=proc,
        worker_log_tasks=worker_log_tasks,
        s3_config=s3_config,
    )


class AdoptedWorker:
    """A plato-fuse worker another world process started, adopted with its mount (handover.py): what a
    ``LazyDVCMount`` needs of its process. Not this process's child, so its exit status isn't known: 0 once gone."""

    def __init__(self, pid: int) -> None:
        self.pid = pid

    @property
    def returncode(self) -> int | None:
        try:
            os.kill(self.pid, 0)
        except ProcessLookupError:
            return 0
        except PermissionError:
            pass
        return None

    async def wait(self) -> int:
        while self.returncode is None:
            await asyncio.sleep(0.1)
        return 0

    def kill(self) -> None:
        with contextlib.suppress(ProcessLookupError, PermissionError):
            os.kill(self.pid, signal.SIGKILL)


async def _worker_error(proc: asyncio.subprocess.Process, log_path: Path, *, debug: bool) -> str:
    """What a plato-fuse worker that failed to mount said: its piped stderr (debug), else its log."""
    if debug:
        _, stderr = await proc.communicate()
        return stderr.decode(errors="replace").strip() if stderr else "unknown"
    try:
        said = log_path.read_bytes().decode(errors="replace").strip()
    except OSError:
        said = ""
    return said or "unknown"


async def unmount_lazy(mount: LazyDVCMount) -> None:
    """Unmount a lazy FUSE filesystem and wait for the worker to write metadata."""
    proc = await asyncio.create_subprocess_exec(
        "fusermount3",
        "-u",
        str(mount.mountpoint),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.wait()

    if mount.worker_proc:
        try:
            await asyncio.wait_for(mount.worker_proc.wait(), timeout=10)
        except TimeoutError:
            mount.worker_proc.kill()
            await mount.worker_proc.wait()
    if mount.worker_log_tasks:
        await asyncio.gather(*mount.worker_log_tasks, return_exceptions=True)

    logger.debug("Lazy DVC unmounted from %s", mount.mountpoint)
