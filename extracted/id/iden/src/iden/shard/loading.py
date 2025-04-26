r"""Contain code to load a shard from its Uniform Resource Identifier
(URI)."""

from __future__ import annotations

__all__ = ["load_from_uri"]

from typing import TYPE_CHECKING

from iden.constants import LOADER
from iden.io import load_json
from iden.shard.loader import setup_shard_loader
from iden.utils.path import sanitize_path

if TYPE_CHECKING:
    from iden.shard import BaseShard


def load_from_uri(uri: str) -> BaseShard:
    r"""Load a shard from its Uniform Resource Identifier (URI).

    Args:
        uri: The URI of the shard.

    Returns:
        The shard associated to the URI.

    Raises:
        FileNotFoundError: if the URI file does not exist.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_json_shard, load_from_uri
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     uri = Path(tmpdir).joinpath("my_uri").as_uri()
    ...     _ = create_json_shard([1, 2, 3], uri=uri)
    ...     shard = load_from_uri(uri)
    ...     shard
    ...
    JsonShard(uri=file:///.../my_uri)

    ```
    """
    path = sanitize_path(uri)
    if not path.is_file():
        msg = f"uri file does not exist: {path}"
        raise FileNotFoundError(msg)
    config = load_json(path)
    loader = setup_shard_loader(config[LOADER])
    return loader.load(uri)
