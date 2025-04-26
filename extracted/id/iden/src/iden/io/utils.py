r"""Contain I/O utility functions."""

from __future__ import annotations

__all__ = ["generate_unique_tmp_path", "get_loader_mapping"]

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from iden.io import BaseLoader


def generate_unique_tmp_path(path: Path) -> Path:
    r"""Return a unique temporary path given a path.

    This function updates the name to add a UUID.

    Args:
        path: The input path.

    Returns:
        The unique name.

    Example usage:

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


def get_loader_mapping() -> dict[str, BaseLoader]:
    r"""Get a default mapping between the file extensions and loaders.

    Returns:
        The mapping between the file extensions and loaders.

    Example usage:

    ```pycon
    >>> from iden.io.utils import get_loader_mapping
    >>> get_loader_mapping()
    {'json': JsonLoader(), 'pkl': PickleLoader(), 'pickle': PickleLoader(), ...}

    ```
    """
    from iden import io  # Local import to avoid cyclic dependencies

    return (
        io.json.get_loader_mapping()
        | io.pickle.get_loader_mapping()
        | io.text.get_loader_mapping()
        | io.torch.get_loader_mapping()
        | io.yaml.get_loader_mapping()
    )
