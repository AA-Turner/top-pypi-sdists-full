r"""Contain YAML-based shard implementations."""

from __future__ import annotations

__all__ = ["YamlShard", "create_yaml_shard"]

import logging
from typing import TYPE_CHECKING, Any

from objectory import OBJECT_TARGET

from iden.constants import KWARGS, LOADER
from iden.io import JsonSaver, YamlLoader, YamlSaver
from iden.shard.file import FileShard
from iden.utils.path import sanitize_path

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class YamlShard(FileShard[Any]):
    r"""Implement a YAML shard.

    The data are stored in a YAML file.

    Args:
        uri: The shard's URI.
        path: Specifies the path to the YAML file.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import YamlShard
    >>> from iden.io import save_yaml
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     file = Path(tmpdir).joinpath("data.yaml")
    ...     save_yaml([1, 2, 3], file)
    ...     shard = YamlShard(uri="file:///data/1234456789", path=file)
    ...     shard.get_data()
    ...
    [1, 2, 3]

    ```
    """

    def __init__(self, uri: str, path: Path | str) -> None:
        super().__init__(uri, path, loader=YamlLoader())

    @classmethod
    def generate_uri_config(cls, path: Path) -> dict:
        r"""Generate the minimal config that is used to load the shard
        from its URI.

        The config must be compatible with the YAML format.

        Args:
            path: The path to the yaml file.

        Returns:
            The minimal config to load the shard from its URI.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import YamlShard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     file = Path(tmpdir).joinpath("data.yaml")
        ...     YamlShard.generate_uri_config(file)
        ...
        {'kwargs': {'path': '.../data.yaml'},
         'loader': {'_target_': 'iden.shard.loader.YamlShardLoader'}}

        ```
        """
        return {
            KWARGS: {"path": sanitize_path(path).as_posix()},
            LOADER: {OBJECT_TARGET: "iden.shard.loader.YamlShardLoader"},
        }


def create_yaml_shard(data: Any, uri: str, path: Path | None = None) -> YamlShard:
    r"""Create a ``YamlShard`` from data.

    Note:
        It is a utility function to create a ``YamlShard`` from its
            data and URI. It is possible to create a ``YamlShard``
            in other ways.

    Args:
        data: The data to save in the yaml file.
        uri: The shard's URI.
        path: The path to the YAML file. If ``None``, a path is
            automatically based on the URI.

    Returns:
        The ``YamlShard`` object.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import create_yaml_shard
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     shard = create_yaml_shard([1, 2, 3], uri=Path(tmpdir).joinpath("my_uri").as_uri())
    ...     shard.get_data()
    ...
    [1, 2, 3]

    ```
    """
    if path is None:
        path = sanitize_path(uri + ".yaml")
    logger.info(f"Saving URI file {uri}")
    JsonSaver().save(YamlShard.generate_uri_config(path), sanitize_path(uri))
    logger.info(f"Saving data in file {path}")
    YamlSaver().save(data, path)
    return YamlShard(uri, path)
