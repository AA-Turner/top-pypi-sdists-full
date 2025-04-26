r"""Contain pickle-based shard implementations."""

from __future__ import annotations

__all__ = ["PickleShard", "create_pickle_shard"]

import logging
from typing import TYPE_CHECKING, Any

from objectory import OBJECT_TARGET

from iden.constants import KWARGS, LOADER
from iden.io import JsonSaver, PickleLoader, PickleSaver
from iden.shard.file import FileShard
from iden.utils.path import sanitize_path

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class PickleShard(FileShard[Any]):
    r"""Implement a pickle shard.

    The data are stored in a pickle file.

    Args:
        uri: The shard's URI.
        path: Specifies the path to the pickle file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import PickleShard
    >>> from iden.io import save_pickle
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     file = Path(tmpdir).joinpath("data.pkl")
    ...     save_pickle([1, 2, 3], file)
    ...     shard = PickleShard(uri="file:///data/1234456789", path=file)
    ...     shard.get_data()
    ...
    [1, 2, 3]

    ```
    """

    def __init__(self, uri: str, path: Path | str) -> None:
        super().__init__(uri, path, loader=PickleLoader())

    @classmethod
    def generate_uri_config(cls, path: Path) -> dict:
        r"""Generate the minimal config that is used to load the shard
        from its URI.

        The config must be compatible with the JSON format.

        Args:
            path: The path to the pickle file.

        Returns:
            The minimal config to load the shard from its URI.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import PickleShard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     file = Path(tmpdir).joinpath("data.pkl")
        ...     PickleShard.generate_uri_config(file)
        ...
        {'kwargs': {'path': '.../data.pkl'},
         'loader': {'_target_': 'iden.shard.loader.PickleShardLoader'}}

        ```
        """
        return {
            KWARGS: {"path": sanitize_path(path).as_posix()},
            LOADER: {OBJECT_TARGET: "iden.shard.loader.PickleShardLoader"},
        }


def create_pickle_shard(data: Any, uri: str, path: Path | None = None) -> PickleShard:
    r"""Create a ``PickleShard`` from data.

    Note:
        It is a utility function to create a ``PickleShard`` from its
            data and URI. It is possible to create a ``PickleShard``
            in other ways.

    Args:
        data: The data to save in the pickle file.
        uri: The shard's URI.
        path: The path to the pickle file. If ``None``, a path is
            automatically based on the URI.

    Returns:
        The ``PickleShard`` object.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_pickle_shard
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     shard = create_pickle_shard([1, 2, 3], uri=Path(tmpdir).joinpath("my_uri").as_uri())
    ...     shard.get_data()
    ...
    [1, 2, 3]

    ```
    """
    if path is None:
        path = sanitize_path(uri + ".pkl")
    logger.info(f"Saving URI file {uri}")
    JsonSaver().save(PickleShard.generate_uri_config(path), sanitize_path(uri))
    logger.info(f"Saving data in file {path}")
    PickleSaver().save(data, path)
    return PickleShard(uri, path)
