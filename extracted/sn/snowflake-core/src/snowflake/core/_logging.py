import errno
import io
import logging
import os
import pathlib
import stat
import tempfile

from typing import Optional, Union


tempdir = pathlib.Path(tempfile.gettempdir())


def simple_file_logging(
    path: Union[str, pathlib.Path, None] = None,
    *,
    level: int = logging.DEBUG,
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> None:
    """Set up snowflake.core logging to a file.

    If ``path`` is not given, the tempfile module is used to determine
    the appropriate temporary location and a file named ``snowflake_core.log``
    is created.

    The log file is opened with mode ``0o600`` (owner read/write only).
    If the path already exists it must be a regular file owned by the
    current user; otherwise ``PermissionError`` is raised. Existing
    owner-writable modes are tightened to ``0o600``. Symlinks are not
    followed.

    Parameters
    __________
    path : str or pathlib.Path, optional
        Destination log file. Defaults to ``<tempdir>/snowflake_core.log``.
    level : int, optional
        Logging level enabled for the file. Default is ``logging.DEBUG``.
    format : str, optional
        Log record format string for the file handler.
    """
    if path is None:
        path = tempdir / "snowflake_core.log"
    logger = logging.getLogger("snowflake.core")
    fh = _SecureFileHandler(path)
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter(format))
    # Increase log level in case the log level of
    #  the top-level logger is lower than necessary
    if not logger.isEnabledFor(level):
        logger.setLevel(level)
    logger.addHandler(fh)


class _SecureFileHandler(logging.FileHandler):
    """FileHandler that creates or opens the log file with mode ``0o600``."""

    def _open(self) -> io.TextIOWrapper:
        return _open_private_log_file(
            self.baseFilename,
            encoding=self.encoding,
            errors=self.errors,
        )


def _open_private_log_file(
    path: Union[str, os.PathLike[str]],
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
) -> io.TextIOWrapper:
    """Open ``path`` for append with mode ``0o600``, without following symlinks."""
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(os.fspath(path), flags, 0o600)
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise PermissionError(f"Refusing to log to symlink {path}") from exc
        raise
    try:
        _ensure_private_log_fd(fd)
        return os.fdopen(fd, "a", encoding=encoding, errors=errors)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def _ensure_private_log_fd(fd: int) -> None:
    """Reject non-regular files and files owned by another user, then set mode ``0o600``.

    Parameters
    __________
    fd : int
        File descriptor of an already-opened log file.
    """
    file_stat = os.fstat(fd)
    if not stat.S_ISREG(file_stat.st_mode):
        raise PermissionError("snowflake.core log path must be a regular file")
    if hasattr(os, "getuid") and file_stat.st_uid != os.getuid():
        raise PermissionError("snowflake.core log file is not owned by the current user")
    if hasattr(os, "fchmod"):
        os.fchmod(fd, 0o600)
