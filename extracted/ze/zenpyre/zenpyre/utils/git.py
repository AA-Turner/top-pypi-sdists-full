r"""Contain git utility functions."""

from __future__ import annotations

__all__ = ["get_current_commit_hash"]

import logging
import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)


def get_current_commit_hash(short: bool = False, cwd: Path | str | None = None) -> str | None:
    r"""Return the current git commit hash.

    Runs ``git rev-parse HEAD`` (or ``git rev-parse --short HEAD`` if
    ``short`` is ``True``) and returns its output.

    Args:
        short: If ``True``, return the abbreviated commit hash (e.g.
            ``"a1b2c3d"``) instead of the full 40-character SHA-1
            hash.
        cwd: The working directory to run the ``git`` command from.
            If ``None`` (the default), the current process's working
            directory is used. Pass this to query the commit hash of
            a repository other than the one containing the current
            working directory.

    Returns:
        The current commit hash as a string, or ``None`` if it could
        not be determined -- e.g. ``cwd`` is not inside a git
        repository, the repository has no commits yet, or the
        ``git`` executable is not available on the system.

    Example:
        ```pycon
        >>> from zenpyre.utils.git import get_current_commit_hash
        >>> commit_hash = get_current_commit_hash()  # doctest: +SKIP
        >>> short_commit_hash = get_current_commit_hash(short=True)  # doctest: +SKIP

        ```
    """
    cmd = ["git", "rev-parse", "--short", "HEAD"] if short else ["git", "rev-parse", "HEAD"]
    try:
        # The command is a fixed, hardcoded argument list (no user-controlled
        # input), so this is not vulnerable to shell/argument injection.
        return subprocess.check_output(  # noqa: S603
            cmd, cwd=cwd, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, OSError):
        logger.warning("Could not determine the current git commit hash.")
        return None
