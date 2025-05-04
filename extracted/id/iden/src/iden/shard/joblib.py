r"""Contain joblib-based shard implementations."""

from __future__ import annotations

__all__ = ["JoblibShard", "create_joblib_shard"]

import logging
from typing import TYPE_CHECKING, Any

from coola.utils.path import sanitize_path
from objectory import OBJECT_TARGET

from iden.constants import KWARGS, LOADER
from iden.io import JoblibLoader, JoblibSaver, JsonSaver
from iden.shard.file import FileShard

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class JoblibShard(FileShard[Any]):
    r"""Implement a joblib shard.

    The data are stored in a joblib file.

    Args:
        uri: The shard's URI.
        path: The path to the joblib file.

    Raises:
        RuntimeError: if ``joblib`` is not installed.

    Example usage:

    ```pycon

    >>> import tempfile

    >>> from pathlib import Path
    >>> from iden.shard import JoblibShard
    >>> from iden.io import save_pickle
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     file = Path(tmpdir).joinpath("data.joblib")
    ...     save_pickle([1, 2, 3], file)
    ...     shard = JoblibShard(uri="file:///data/1234456789", path=file)
    ...     shard.get_data()
    ...
    [1, 2, 3]

    ```
    """

    def __init__(self, uri: str, path: Path | str) -> None:
        super().__init__(uri, path, loader=JoblibLoader())

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
        >>> from iden.shard import JoblibShard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     file = Path(tmpdir).joinpath("data.joblib")
        ...     JoblibShard.generate_uri_config(file)
        ...
        {'kwargs': {'path': '.../data.joblib'},
         'loader': {'_target_': 'iden.shard.loader.JoblibShardLoader'}}

        ```
        """
        return {
            KWARGS: {"path": sanitize_path(path).as_posix()},
            LOADER: {OBJECT_TARGET: "iden.shard.loader.JoblibShardLoader"},
        }


def create_joblib_shard(data: Any, uri: str, path: Path | None = None) -> JoblibShard:
    r"""Create a ``JoblibShard`` from data.

    Note:
        It is a utility function to create a ``JoblibShard`` from its
            data and URI. It is possible to create a ``JoblibShard``
            in other ways.

    Args:
        data: The data to save in the joblib file.
        uri: The shard's URI.
        path: The path to the joblib file. If ``None``, a path is
            automatically based on the URI.

    Returns:
        The ``JoblibShard`` object.

    Raises:
        RuntimeError: if ``joblib`` is not installed.

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
        path = sanitize_path(uri + ".joblib")
    logger.info(f"Saving URI file {uri}")
    JsonSaver().save(JoblibShard.generate_uri_config(path), sanitize_path(uri))
    logger.info(f"Saving data in file {path}")
    JoblibSaver().save(data, path)
    return JoblibShard(uri, path)
