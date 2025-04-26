r"""Contain a data structure to manage a dictionary of shards."""

from __future__ import annotations

__all__ = ["ShardDict", "create_shard_dict"]

import logging
from typing import Any, TypeVar

from coola import objects_are_equal
from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping
from objectory import OBJECT_TARGET

from iden.constants import LOADER, SHARDS
from iden.io import JsonSaver, load_json
from iden.shard.base import BaseShard
from iden.shard.exceptions import ShardNotFoundError
from iden.shard.utils import get_dict_uris
from iden.utils.path import sanitize_path

T = TypeVar("T")

logger = logging.getLogger(__name__)


class ShardDict(BaseShard[T]):
    r"""Implement a data structure to manage a dictionary of shards.

    Args:
        uri: The shard's URI.
        shards: The dictionary of shards.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.dataset import VanillaDataset
    >>> from iden.shard import create_json_shard, ShardDict
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     shards = {
    ...         "train": create_json_shard(
    ...             [1, 2, 3], uri=Path(tmpdir).joinpath("shards/uri1").as_uri()
    ...         ),
    ...         "val": create_json_shard(
    ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shards/uri2").as_uri()
    ...         ),
    ...     }
    ...     sd = ShardDict(uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards)
    ...     sd
    ...
    ShardDict(
      (uri): file:///.../uri
      (shards):
        (train): JsonShard(uri=file:///.../shards/uri1)
        (val): JsonShard(uri=file:///.../shards/uri2)
    )

    ```
    """

    def __init__(self, uri: str, shards: dict[str, BaseShard[T]]) -> None:
        self._uri = uri
        self._shards = shards.copy()

    def __contains__(self, item: str) -> bool:
        return item in self._shards

    def __getitem__(self, item: str) -> BaseShard[T]:
        return self._shards[item]

    def __len__(self) -> int:
        return len(self._shards)

    def __repr__(self) -> str:
        shards = f"\n{repr_mapping(self._shards)}" if self._shards else ""
        args = repr_indent(repr_mapping({"uri": self._uri, "shards": shards}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        shards = f"\n{str_mapping(self._shards)}" if self._shards else ""
        args = str_indent(str_mapping({"uri": self._uri, "shards": shards}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def clear(self) -> None:
        for shard in self._shards.values():
            shard.clear()

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(
            self.get_uri(), other.get_uri(), equal_nan=equal_nan
        ) and objects_are_equal(self.get_data(), other.get_data(), equal_nan=equal_nan)

    def get_data(self, cache: bool = False) -> dict[str, BaseShard[T]]:  # noqa: ARG002
        return self._shards.copy()

    def get_uri(self) -> str:
        return self._uri

    def get_shard(self, shard_id: str) -> Any:
        r"""Get a shard.

        Args:
            shard_id: The shard ID.

        Returns:
            The shard.

        Raises:
            ShardNotFoundError: if the shard does not exist.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard, ShardDict
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = {
        ...         "train": create_json_shard(
        ...             [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
        ...         ),
        ...         "val": create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     }
        ...     sd = ShardDict(uri=Path(tmpdir).joinpath("main_uri").as_uri(), shards=shards)
        ...     sd.get_shard("train")
        ...
        JsonShard(uri=file:///.../uri1)

        ```
        """
        shard = self._shards.get(shard_id, None)
        if shard is None:
            msg = f"shard `{shard_id}` does not exist"
            raise ShardNotFoundError(msg)
        return shard

    def get_shard_ids(self) -> set[str]:
        r"""Get the shard IDs.

        Returns:
            The shard IDs.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard, ShardDict
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = {
        ...         "train": create_json_shard(
        ...             [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
        ...         ),
        ...         "val": create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     }
        ...     sd = ShardDict(uri=Path(tmpdir).joinpath("main_uri").as_uri(), shards=shards)
        ...     sorted(sd.get_shard_ids())
        ...
        ['train', 'val']

        ```
        """
        return set(self._shards.keys())

    def has_shard(self, shard_id: str) -> bool:
        r"""Indicate if the shard exists or not.

        Args:
            shard_id: The shard ID.

        Returns:
            ``True`` if the shard exists, otherwise ``False``

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import create_json_shard, ShardDict
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = {
        ...         "train": create_json_shard(
        ...             [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
        ...         ),
        ...         "val": create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     }
        ...     sd = ShardDict(uri=Path(tmpdir).joinpath("main_uri").as_uri(), shards=shards)
        ...     sd.has_shard("train")
        ...     sd.has_shard("test")
        ...
        True
        False

        ```
        """
        return shard_id in self

    def is_cached(self) -> bool:
        return any(shard.is_cached() for shard in self._shards.values())

    @classmethod
    def from_uri(cls, uri: str) -> ShardDict[T]:
        r"""Instantiate a shard from its URI.

        Args:
            uri: The URI.

        Returns:
            The instantiated shard.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import ShardDict, create_json_shard, create_shard_dict
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = {
        ...         "train": create_json_shard(
        ...             [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
        ...         ),
        ...         "val": create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     }
        ...     uri = Path(tmpdir).joinpath("uri").as_uri()
        ...     _ = create_shard_dict(shards, uri=uri)
        ...     shard = ShardDict.from_uri(uri)
        ...     shard
        ...
        ShardDict(
          (uri): file:///.../uri
          (shards):
            (train): JsonShard(uri=file:///.../shard/uri1)
            (val): JsonShard(uri=file:///.../shard/uri2)
        )

        ```
        """
        # local import to avoid cyclic dependencies
        from iden.shard import load_from_uri

        config = load_json(sanitize_path(uri))
        shards = {key: load_from_uri(shard) for key, shard in config[SHARDS].items()}
        return cls(uri=uri, shards=shards)

    @classmethod
    def generate_uri_config(cls, shards: dict[str, BaseShard[T]]) -> dict:
        r"""Generate the minimal config that is used to load the shard
        from its URI.

        The config must be compatible with the JSON format.

        Args:
            shards: The shards.

        Returns:
            The minimal config to load the shard from its URI.

        Example usage:

        ```pycon
        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.shard import ShardDict, create_json_shard
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = {
        ...         "train": create_json_shard(
        ...             [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
        ...         ),
        ...         "val": create_json_shard(
        ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...         ),
        ...     }
        ...     ShardDict.generate_uri_config(shards)
        ...
        {'shards': {'train': 'file:///.../shard/uri1', 'val': 'file:///.../shard/uri2'},
         'loader': {'_target_': 'iden.shard.loader.ShardDictLoader'}}

        ```
        """
        return {
            SHARDS: get_dict_uris(shards),
            LOADER: {OBJECT_TARGET: "iden.shard.loader.ShardDictLoader"},
        }


def create_shard_dict(shards: dict[str, BaseShard[T]], uri: str) -> ShardDict[T]:
    r"""Create a ``ShardDict`` a list of shards.

    Note:
        It is a utility function to create a ``ShardDict`` from its
            shards and URI. It is possible to create a ``ShardDict``
            in other ways.

    Args:
        shards: The shards.
        uri: The shard's URI.

    Returns:
        The ``ShardDict`` object.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.shard import ShardDict, create_json_shard, create_shard_dict
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     shards = {
    ...         "train": create_json_shard(
    ...             [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
    ...         ),
    ...         "val": create_json_shard(
    ...             [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
    ...         ),
    ...     }
    ...     shard = create_shard_dict(shards, uri=Path(tmpdir).joinpath("uri").as_uri())
    ...     shard
    ...
    ShardDict(
      (uri): file:///.../uri
      (shards):
        (train): JsonShard(uri=file:///.../shard/uri1)
        (val): JsonShard(uri=file:///.../shard/uri2)
    )

    ```
    """
    logger.info(f"Saving URI file {uri}")
    JsonSaver().save(ShardDict.generate_uri_config(shards), sanitize_path(uri))
    return ShardDict(uri, shards)
