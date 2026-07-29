"""POSIX SHM cleanup helpers.

Generalizes the ``_clean_stale_shm`` pattern from py_streaming so any caller
(gateway shutdown, inference pipeline shutdown, manual ops) can unlink
``/dev/shm/{prefix}*`` files owned by the current uid, without trampling
files that belong to other users on shared hosts.

Consumer-safety rule: we never unlink a SHM file that another process still
has mapped — the producer/consumer convention in our codebase is that
*producers* own the lifecycle. ``safe_unlink_if_owner`` enforces that:
caller passes the path; we unlink only if the file is owned by us. If the
caller wants extra safety (skip when other processes still hold the inode
mapped), use ``cleanup_owned_shm`` with ``check_lsof=True`` — falls back to
"unlink anyway" silently if ``lsof`` isn't on PATH.
"""

from __future__ import annotations

import glob
import logging
import os
import shutil
import subprocess
from typing import Iterable, List

logger = logging.getLogger(__name__)

_SHM_DIR = "/dev/shm"  # nosec B108 - canonical POSIX shared-memory path; not a tmp dir

# Default patterns covering everything our gateway / inference services create.
DEFAULT_PREFIXES = (
    "cuda_ipc_",
    "shm_results_",
    "global_frame",
    "databus__",
    "gpu_camera_map",
    "sem.loky-",
)


def cleanup_owned_shm(
    prefixes: Iterable[str] = DEFAULT_PREFIXES,
    *,
    shm_dir: str = _SHM_DIR,
    check_lsof: bool = False,
) -> List[str]:
    """Unlink ``{shm_dir}/{prefix}*`` files owned by the current uid.

    Returns the list of files actually unlinked. Never raises; logs at debug
    level on per-file failures.
    """
    unlinked: List[str] = []
    if not os.path.isdir(shm_dir):
        return unlinked
    my_uid = os.getuid()
    lsof_path = shutil.which("lsof") if check_lsof else None
    for prefix in prefixes:
        # Match exact name (e.g. ``gpu_camera_map``) and any descendant
        # (``gpu_camera_map_*``) so callers don't have to pass both forms.
        for path in sorted(
            set(glob.glob(os.path.join(shm_dir, prefix + "*")) + glob.glob(os.path.join(shm_dir, prefix)))
        ):
            try:
                if not os.path.exists(path):
                    continue
                st = os.stat(path)
                if st.st_uid != my_uid:
                    continue
                if lsof_path and _has_other_holders(lsof_path, path):
                    logger.debug("skipping %s — other process holds it", path)
                    continue
                os.unlink(path)
                unlinked.append(path)
            except FileNotFoundError:
                continue
            except OSError:
                logger.debug("unlink failed for %s", path, exc_info=True)
    return unlinked


def safe_unlink_if_owner(path: str) -> bool:
    """Unlink ``path`` only if it's owned by the current uid. Returns True on success."""
    try:
        st = os.stat(path)
    except FileNotFoundError:
        return False
    except OSError:
        return False
    if st.st_uid != os.getuid():
        return False
    try:
        os.unlink(path)
        return True
    except FileNotFoundError:
        return False
    except OSError:
        logger.debug("unlink failed for %s", path, exc_info=True)
        return False


def _has_other_holders(lsof_path: str, file_path: str) -> bool:
    """Best-effort check: is any process other than us holding ``file_path``?"""
    try:
        result = subprocess.run(  # noqa: S603 - lsof_path is shutil.which result
            [lsof_path, "-Fp", "--", file_path],
            capture_output=True,
            text=True,
            timeout=2.0,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        return False
    if result.returncode != 0:
        return False
    my_pid = os.getpid()
    for line in result.stdout.splitlines():
        if line.startswith("p"):
            try:
                pid = int(line[1:])
            except ValueError:
                continue
            if pid != my_pid:
                return True
    return False
