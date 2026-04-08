"""Lazy DVC workspace via FUSE — files appear present but content downloads on first read.

The FUSE filesystem is implemented as a Rust binary (plato-fuse) for performance.
The binary must be on PATH (installed to /usr/local/bin/plato-fuse in the base image).

On commit, ``smart_commit()`` builds a new .dir manifest without
re-downloading untouched files — only modified/new files are uploaded.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shutil
from pathlib import Path

from plato.worlds.dvc_models import (
    DVCManifest,
    LazyDVCMount,
    S3Config,
    _env_flag_enabled,
)

logger = logging.getLogger(__name__)

PLATO_FUSE_S3_BUCKET = "plato-public-static"
PLATO_FUSE_S3_KEY = "plato-fuse"
PLATO_FUSE_INSTALL_PATH = "/usr/local/bin/plato-fuse"


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
    override = os.environ.get("PLATO_FUSE_BINARY")
    if override:
        override_path = Path(override)
        if override_path.is_file():
            logger.debug("Using PLATO_FUSE_BINARY override: %s", override_path)
            return str(override_path)
        raise RuntimeError(f"PLATO_FUSE_BINARY does not exist: {override}")

    binary = shutil.which("plato-fuse")
    if binary:
        logger.debug("Using plato-fuse from PATH: %s", binary)
        return binary

    logger.debug(
        "plato-fuse not found on PATH, downloading from s3://%s/%s",
        PLATO_FUSE_S3_BUCKET,
        PLATO_FUSE_S3_KEY,
    )

    proc = await asyncio.create_subprocess_exec(
        "aws",
        "s3",
        "cp",
        f"s3://{PLATO_FUSE_S3_BUCKET}/{PLATO_FUSE_S3_KEY}",
        PLATO_FUSE_INSTALL_PATH,
        "--no-sign-request",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"Failed to download plato-fuse from S3: {stderr.decode().strip()}")

    os.chmod(PLATO_FUSE_INSTALL_PATH, 0o755)
    logger.debug("Installed plato-fuse to %s", PLATO_FUSE_INSTALL_PATH)
    return PLATO_FUSE_INSTALL_PATH


async def mount_lazy(
    mountpoint: Path,
    manifest: DVCManifest,
    s3_config: S3Config,
    cache_dir: Path,
) -> LazyDVCMount:
    """Mount a lazy FUSE filesystem at *mountpoint*.

    The FUSE loop runs in a child process so the parent's asyncio
    loop is never blocked by filesystem operations on the mount.
    """
    # Write config for the worker process
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

    (cache_dir / "overlay").mkdir(parents=True, exist_ok=True)
    (cache_dir / "cache").mkdir(parents=True, exist_ok=True)

    # Start worker subprocess
    rust_binary = await _ensure_plato_fuse()
    logger.debug("Using Rust FUSE binary: %s", rust_binary)
    proc = await asyncio.create_subprocess_exec(
        rust_binary,
        str(config_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    worker_log_tasks: tuple[asyncio.Task[None], ...] | None = None
    if _env_flag_enabled("PLATO_FUSE_DEBUG"):
        worker_log_tasks = (
            asyncio.create_task(_forward_worker_logs(proc.stdout, label="stdout")),
            asyncio.create_task(_forward_worker_logs(proc.stderr, label="stderr")),
        )

    # Wait for the mount to appear (up to ~10 s)
    for _ in range(100):
        if proc.returncode is not None:
            _, stderr = await proc.communicate()
            err = stderr.decode().strip() if stderr else "unknown"
            raise RuntimeError(f"FUSE subprocess exited early (rc={proc.returncode}): {err}")
        if os.path.ismount(str(mountpoint)):
            break
        await asyncio.sleep(0.1)
    else:
        try:
            proc.kill()
            _, stderr = await asyncio.wait_for(proc.communicate(), timeout=5)
            err = stderr.decode().strip() if stderr else "unknown"
        except Exception:
            err = "unknown"
        raise RuntimeError(f"FUSE mount at {mountpoint} did not appear: {err}")

    logger.debug("Lazy DVC mounted at %s (%d files)", mountpoint, len(manifest.entries_list))
    return LazyDVCMount(
        mountpoint=mountpoint,
        cache_dir=cache_dir,
        manifest=manifest,
        worker_proc=proc,
        worker_log_tasks=worker_log_tasks,
    )


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
        except asyncio.TimeoutError:
            mount.worker_proc.kill()
            await mount.worker_proc.wait()
    if mount.worker_log_tasks:
        await asyncio.gather(*mount.worker_log_tasks, return_exceptions=True)

    logger.debug("Lazy DVC unmounted from %s", mount.mountpoint)
