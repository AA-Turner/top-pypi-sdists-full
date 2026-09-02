"""Local advisory profile lock (S2 §5.1 rule 2, §12.1).

Second-worker prevention is a FENCE, not a race resolved in the worker's favour.
A worker that cannot take the advisory lock on its profile directory refuses to
launch Chromium and returns ``profile_locked_locally`` — loudly. This is the
single-host advisory layer; the authoritative fence is the control plane's
activation key, and Chromium's own ``SingletonLock`` inside the user-data dir is a
third independent guard (proven in the WS-0 P1 harness).

``fcntl.flock`` is used because it is released automatically when the holding
process dies (a crashed worker never strands its own profile), which a lockfile
containing a PID cannot guarantee.
"""

from __future__ import annotations

import errno
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import fcntl

    _HAVE_FCNTL = True
except ImportError:  # pragma: no cover - non-POSIX
    _HAVE_FCNTL = False


class ProfileLockError(RuntimeError):
    """The advisory lock on the profile directory is already held."""


class ProfileLock:
    """A ``flock``-based advisory exclusive lock on ``<user_data_dir>.worker.lock``.

    The lock file sits BESIDE the user-data dir (not inside it) so it never becomes
    part of a profile checkpoint archive.
    """

    def __init__(self, user_data_dir: str) -> None:
        self._udd = Path(user_data_dir)
        self._lock_path = Path(f"{str(self._udd).rstrip(os.sep)}.worker.lock")
        self._fd: int | None = None

    @property
    def lock_path(self) -> str:
        return str(self._lock_path)

    @property
    def held(self) -> bool:
        return self._fd is not None

    def acquire(self) -> bool:
        """Take the lock. Returns True on success; raises ``ProfileLockError`` if
        another process holds it. Never blocks."""
        if self._fd is not None:
            return True
        self._lock_path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(str(self._lock_path), os.O_RDWR | os.O_CREAT, 0o600)
        if not _HAVE_FCNTL:  # pragma: no cover - non-POSIX fallback
            self._fd = fd
            return True
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            os.close(fd)
            if exc.errno in (errno.EACCES, errno.EAGAIN):
                logger.warning("profile lock already held: %s", self._lock_path)
                raise ProfileLockError(str(self._lock_path)) from exc
            raise
        os.write(fd, str(os.getpid()).encode("ascii"))
        self._fd = fd
        return True

    def clear_stale_chromium_singletons(self) -> list[str]:
        """Remove Chromium crash markers only while this worker owns the profile.

        Chromium leaves ``Singleton*`` files/symlinks behind when a Fargate task
        is killed.  They are not browser data, but a later task treats them as
        proof that the profile is still open on the previous host.  Our flock is
        the stronger cross-process fence: once it is held, no live Matrx worker
        may own this profile, so those three Chromium-owned artifacts are stale.

        A real directory at one of these names is unexpected and is refused
        rather than recursively removed.  This method never touches cookies,
        history, local storage, extensions, or any other profile content.
        """
        if not self.held:
            raise ProfileLockError("profile lock must be held before singleton cleanup")

        removed: list[str] = []
        for name in ("SingletonLock", "SingletonCookie", "SingletonSocket"):
            artifact = self._udd / name
            try:
                artifact.lstat()
            except FileNotFoundError:
                continue
            if artifact.is_dir() and not artifact.is_symlink():
                raise ProfileLockError(
                    f"refusing to remove Chromium singleton directory: {artifact}"
                )
            try:
                artifact.unlink()
            except FileNotFoundError:
                continue
            removed.append(name)
            logger.warning("removed stale Chromium singleton after profile lock: %s", artifact)
        return removed

    def release(self) -> None:
        if self._fd is None:
            return
        fd, self._fd = self._fd, None
        try:
            if _HAVE_FCNTL:
                fcntl.flock(fd, fcntl.LOCK_UN)
        except OSError:
            logger.debug("error unlocking %s", self._lock_path)
        finally:
            try:
                os.close(fd)
            except OSError:
                pass
