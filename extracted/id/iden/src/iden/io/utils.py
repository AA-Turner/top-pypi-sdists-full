r"""Contain I/O utility functions."""

from __future__ import annotations

__all__ = ["generate_unique_tmp_path"]

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def generate_unique_tmp_path(path: Path) -> Path:
    r"""Return a unique temporary path given a path.

    This function updates the name to add a UUID.

    Args:
        path: The input path.

    Returns:
        The unique name.

    Example:
        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.io.utils import generate_unique_tmp_path
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     path = generate_unique_tmp_path(Path(tmpdir).joinpath("data.pt"))
        ...     path
        ...
        PosixPath('/.../data-....pt')

        ```
    """
    h = uuid.uuid4().hex
    extension = "".join(path.suffixes)[1:]
    if extension:
        extension = "." + extension
        stem = path.name[: -len(extension)]
    else:
        stem = path.name
    return path.with_name(f"{stem}-{h}{extension}")
