r"""Contain path utility functions."""

from __future__ import annotations

__all__ = ["sanitize_path"]

from pathlib import Path
from urllib.parse import unquote, urlparse


def sanitize_path(path: Path | str) -> Path:
    r"""Sanitize the given path.

    Args:
        path: Specifies the path to sanitize.

    Returns:
        The sanitized path.

    Example usage:

    ```pycon
    >>> from pathlib import Path
    >>> from iden.utils.path import sanitize_path
    >>> sanitize_path("something")
    PosixPath('.../something')
    >>> sanitize_path("")
    PosixPath('...')
    >>> sanitize_path(Path("something"))
    PosixPath('.../something')
    >>> sanitize_path(Path("something/./../"))
    PosixPath('...')

    ```
    """
    if isinstance(path, str):
        # Use urlparse to parse file URI: https://stackoverflow.com/a/15048213
        path = Path(unquote(urlparse(path).path))
    return path.expanduser().resolve()
