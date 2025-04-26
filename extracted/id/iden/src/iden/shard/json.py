r"""Contain JSON-based shard implementations."""

from __future__ import annotations

__all__ = ["JsonShard", "create_json_shard"]

import logging
from typing import TYPE_CHECKING, Any

from objectory import OBJECT_TARGET

from iden.constants import KWARGS, LOADER
from iden.io import JsonLoader, JsonSaver
from iden.shard.file import FileShard
from iden.utils.path import sanitize_path

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class JsonShard(FileShard[Any]):
    r"""Implement a JSON shard.

    The data are stored in a JSON file.

    Args:
        uri: The shard's URI.
        path: Specifies the path to the JSON file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import JsonShard
    >>> from iden.io import save_json
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     file = Path(tmpdir).joinpath("data.json")
    ...     save_json([1, 2, 3], file)
    ...     shard = JsonShard(uri="file:///data/1234456789", path=file)
    ...     shard.get_data()
    ...
    [1, 2, 3]

    ```
    """

    def __init__(self, uri: str, path: Path | str) -> None:
        super().__init__(uri, path, loader=JsonLoader())

    @classmethod
    def generate_uri_config(cls, path: Path) -> dict:
        r"""Generate the minimal config that is used to load the shard
        from its URI.

        The config must be compatible with the JSON format.

        Args:
            path: The path to the json file.

        Returns:
            The minimal config to load the shard from its URI.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import JsonShard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     file = Path(tmpdir).joinpath("data.json")
        ...     JsonShard.generate_uri_config(file)
        ...
        {'kwargs': {'path': '.../data.json'},
         'loader': {'_target_': 'iden.shard.loader.JsonShardLoader'}}

        ```
        """
        return {
            KWARGS: {"path": sanitize_path(path).as_posix()},
            LOADER: {OBJECT_TARGET: "iden.shard.loader.JsonShardLoader"},
        }


def create_json_shard(data: Any, uri: str, path: Path | None = None) -> JsonShard:
    r"""Create a ``JsonShard`` from data.

    Note:
        It is a utility function to create a ``JsonShard`` from its
            data and URI. It is possible to create a ``JsonShard``
            in other ways.

    Args:
        data: The data to save in the json file.
        uri: The shard's URI.
        path: The path to the JSON file. If ``None``, a path is
            automatically based on the URI.

    Returns:
        The ``JsonShard`` object.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_json_shard
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     shard = create_json_shard([1, 2, 3], uri=Path(tmpdir).joinpath("my_uri").as_uri())
    ...     shard.get_data()
    ...
    [1, 2, 3]

    ```
    """
    if path is None:
        path = sanitize_path(uri + ".json")
    logger.info(f"Saving URI file {uri}")
    JsonSaver().save(JsonShard.generate_uri_config(path), sanitize_path(uri))
    logger.info(f"Saving data in file {path}")
    JsonSaver().save(data, path)
    return JsonShard(uri, path)
