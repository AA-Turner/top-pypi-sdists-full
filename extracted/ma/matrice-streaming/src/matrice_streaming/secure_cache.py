"""Shared helpers for safe on-disk caching of downloaded video files.

The gateway caches downloaded videos under the shared temp root with a
predictable ``video_<md5>`` name. On a multi-user host a fixed, world-readable
cache dir lets a local attacker pre-create the directory (winning ownership) or
pre-seed a cache file the gateway would then decode instead of the real stream.

These helpers pin the cache to a per-user directory (``0700``), reject a
directory/file that is a symlink or owned by another uid, and let callers write
via an atomic ``mkstemp`` + ``os.replace`` so an existing/symlinked path can
never be silently trusted or clobbered.
"""

import os
import stat
import tempfile
from pathlib import Path

__all__ = ["secure_cache_dir", "is_safe_cached_file"]


def _current_uid() -> int:
    # The GPU streaming stack is Linux-only; getuid is always present there.
    # Fall back to 0 on platforms without it (best-effort, no multi-user model).
    getuid = getattr(os, "getuid", None)
    return getuid() if getuid is not None else 0


def secure_cache_dir(name: str) -> Path:
    """Return a per-user cache dir under the temp root, created mode 0700.

    The directory name is suffixed with the current uid so distinct users never
    share a cache path. Raises RuntimeError if an existing path at that location
    is a symlink, not a directory, or owned by another user (hijack attempt).
    """
    uid = _current_uid()
    base = Path(tempfile.gettempdir()) / f"{name}-{uid}"
    base.mkdir(mode=0o700, exist_ok=True)
    st = os.lstat(base)
    if stat.S_ISLNK(st.st_mode) or not stat.S_ISDIR(st.st_mode) or st.st_uid != uid:
        raise RuntimeError(f"Refusing to use insecure cache dir {base}: unexpected owner or type")
    # Re-assert perms in case the dir pre-existed with a looser mode.
    os.chmod(base, 0o700)
    return base


def is_safe_cached_file(path: os.PathLike) -> bool:
    """True if ``path`` is a regular file owned by the current uid.

    Rejects symlinks and files owned by other users so a pre-seeded cache entry
    is never trusted for reuse.
    """
    try:
        st = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and st.st_uid == _current_uid()
