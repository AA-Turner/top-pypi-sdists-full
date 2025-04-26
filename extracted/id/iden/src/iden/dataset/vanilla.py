r"""Contain the base class to implement a dataset object."""

from __future__ import annotations

__all__ = ["VanillaDataset", "create_vanilla_dataset", "check_shards"]

import logging
from typing import TYPE_CHECKING, Any, TypeVar

from coola import objects_are_equal
from coola.utils import repr_indent, repr_mapping, str_indent, str_mapping
from objectory import OBJECT_TARGET

from iden.constants import ASSETS, LOADER, SHARDS
from iden.dataset.base import BaseDataset
from iden.dataset.exceptions import AssetNotFoundError, SplitNotFoundError
from iden.io import JsonSaver, load_json
from iden.shard import ShardDict
from iden.utils.path import sanitize_path

if TYPE_CHECKING:
    from iden.shard import BaseShard, ShardTuple

logger = logging.getLogger(__name__)

T = TypeVar("T")


class VanillaDataset(BaseDataset[T]):
    r"""Implement a simple dataset.

    Args:
        uri: The URI associated to the dataset.
        shards: The dataset's shards. Each item in the mapping
            represent a dataset split, where the key is the dataset
            split and the value is the shards.
        assets: The dataset's assets.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.dataset import VanillaDataset
    >>> from iden.shard import create_json_shard, create_shard_dict, create_shard_tuple
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     shards = create_shard_dict(
    ...         shards={
    ...             "train": create_shard_tuple(
    ...                 [
    ...                     create_json_shard(
    ...                         [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
    ...                     ),
    ...                     create_json_shard(
    ...                         [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
    ...                     ),
    ...                 ],
    ...                 uri=Path(tmpdir).joinpath("uri_train").as_uri(),
    ...             ),
    ...             "val": create_shard_tuple(
    ...                 shards=[],
    ...                 uri=Path(tmpdir).joinpath("uri_val").as_uri(),
    ...             ),
    ...         },
    ...         uri=Path(tmpdir).joinpath("uri_shards").as_uri(),
    ...     )
    ...     assets = create_shard_dict(
    ...         shards={
    ...             "stats": create_json_shard(
    ...                 [1, 2, 3], uri=Path(tmpdir).joinpath("uri_stats").as_uri()
    ...             )
    ...         },
    ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
    ...     )
    ...     dataset = VanillaDataset(
    ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
    ...     )
    ...     dataset
    ...
    VanillaDataset(
      (uri): file:///.../uri
      (shards): ShardDict(
          (uri): file:///.../uri_shards
          (shards):
            (train): ShardTuple(
                (uri): file:///.../uri_train
                (shards):
                  (0): JsonShard(uri=file:///.../shard/uri1)
                  (1): JsonShard(uri=file:///.../shard/uri2)
              )
            (val): ShardTuple(
                (uri): file:///.../uri_val
                (shards):
              )
        )
      (assets): ShardDict(
          (uri): file:///.../uri_assets
          (shards):
            (stats): JsonShard(uri=file:///.../uri_stats)
        )
    )

    ```
    """

    def __init__(
        self, uri: str, shards: ShardDict[ShardTuple[BaseShard[T]]], assets: ShardDict
    ) -> None:
        self._uri = str(uri)
        check_shards(shards)
        self._shards = shards
        self._assets = assets

    def __repr__(self) -> str:
        args = repr_indent(
            repr_mapping(
                {
                    "uri": self._uri,
                    "shards": self._shards,
                    "assets": self._assets,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def __str__(self) -> str:
        args = str_indent(
            str_mapping(
                {
                    "uri": self._uri,
                    "shards": self._shards,
                    "assets": self._assets,
                }
            )
        )
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            objects_are_equal(self.get_uri(), other.get_uri(), equal_nan=equal_nan)
            and objects_are_equal(self._shards, other._shards, equal_nan=equal_nan)
            and objects_are_equal(self._assets, other._assets, equal_nan=equal_nan)
        )

    def get_asset(self, asset_id: str) -> BaseShard:
        if asset_id not in self._assets:
            msg = f"asset '{asset_id}' does not exist"
            raise AssetNotFoundError(msg)
        return self._assets.get_shard(asset_id)

    def has_asset(self, asset_id: str) -> bool:
        return self._assets.has_shard(asset_id)

    def get_shards(self, split: str) -> tuple[BaseShard[T], ...]:
        if split not in self._shards:
            msg = f"split '{split}' does not exist"
            raise SplitNotFoundError(msg)
        return self._shards[split].get_data()

    def get_num_shards(self, split: str) -> int:
        if split not in self._shards:
            msg = f"split '{split}' does not exist"
            raise SplitNotFoundError(msg)
        return len(self._shards.get_shard(split))

    def get_splits(self) -> set[str]:
        return self._shards.get_shard_ids()

    def has_split(self, split: str) -> bool:
        return split in self._shards

    def get_uri(self) -> str:
        return self._uri

    @classmethod
    def from_uri(cls, uri: str) -> VanillaDataset:
        r"""Instantiate a shard from its URI.

        Args:
            uri: The URI.

        Returns:
            The instantiated shard.

        Example usage:

        ```pycon

        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.dataset import create_vanilla_dataset
        >>> from iden.shard import create_json_shard, create_shard_dict, create_shard_tuple
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = create_shard_dict(
        ...         shards={
        ...             "train": create_shard_tuple(
        ...                 [
        ...                     create_json_shard(
        ...                         [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
        ...                     ),
        ...                     create_json_shard(
        ...                         [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...                     ),
        ...                 ],
        ...                 uri=Path(tmpdir).joinpath("uri_train").as_uri(),
        ...             ),
        ...             "val": create_shard_tuple(
        ...                 shards=[],
        ...                 uri=Path(tmpdir).joinpath("uri_val").as_uri(),
        ...             ),
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_shards").as_uri(),
        ...     )
        ...     assets = create_shard_dict(
        ...         shards={
        ...             "stats": create_json_shard(
        ...                 [1, 2, 3], uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     uri = Path(tmpdir).joinpath("uri").as_uri()
        ...     _ = create_vanilla_dataset(uri=uri, shards=shards, assets=assets)
        ...     dataset = VanillaDataset.from_uri(uri)
        ...     dataset
        ...
        VanillaDataset(
          (uri): file:///.../uri
          (shards): ShardDict(
              (uri): file:///.../uri_shards
              (shards):
                (train): ShardTuple(
                    (uri): file:///.../uri_train
                    (shards):
                      (0): JsonShard(uri=file:///.../shard/uri1)
                      (1): JsonShard(uri=file:///.../shard/uri2)
                  )
                (val): ShardTuple(
                    (uri): file:///.../uri_val
                    (shards):
                  )
            )
          (assets): ShardDict(
              (uri): file:///.../uri_assets
              (shards):
                (stats): JsonShard(uri=file:///.../uri_stats)
            )
        )

        ```
        """
        # local import to avoid cyclic dependencies
        from iden.shard import load_from_uri

        config = load_json(sanitize_path(uri))
        shards = load_from_uri(config[SHARDS])
        assets = load_from_uri(config[ASSETS])
        return cls(uri=uri, shards=shards, assets=assets)

    @classmethod
    def generate_uri_config(
        cls,
        shards: ShardDict[ShardTuple[BaseShard[T]]],
        assets: ShardDict,
    ) -> dict:
        r"""Generate the minimal config that is used to load the dataset
        from its URI.

        The config must be compatible with the JSON format.

        Args:
            shards: The shards in the dataset. Each item in the mapping
                represent a dataset split, where the key is the dataset
                split and the value is the shards.
            assets: The dataset's assets.

        Returns:
            The minimal config to load the shard from its URI.

        Example usage:

        ```pycon

        >>> import tempfile
        >>> from pathlib import Path
        >>> from iden.dataset import VanillaDataset
        >>> from iden.shard import create_json_shard, create_shard_dict, create_shard_tuple
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     shards = create_shard_dict(
        ...         shards={
        ...             "train": create_shard_tuple(
        ...                 [
        ...                     create_json_shard(
        ...                         [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
        ...                     ),
        ...                     create_json_shard(
        ...                         [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
        ...                     ),
        ...                 ],
        ...                 uri=Path(tmpdir).joinpath("uri_train").as_uri(),
        ...             ),
        ...             "val": create_shard_tuple(
        ...                 shards=[],
        ...                 uri=Path(tmpdir).joinpath("uri_val").as_uri(),
        ...             ),
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_shards").as_uri(),
        ...     )
        ...     assets = create_shard_dict(
        ...         shards={
        ...             "stats": create_json_shard(
        ...                 [1, 2, 3], uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     config = VanillaDataset.generate_uri_config(shards=shards, assets=assets)
        ...     config
        ...
        {'loader': {'_target_': 'iden.dataset.loader.VanillaDatasetLoader'},
         'shards': 'file:///.../uri_shards',
         'assets': 'file:///.../uri_assets'}

        ```
        """
        return {
            LOADER: {OBJECT_TARGET: "iden.dataset.loader.VanillaDatasetLoader"},
            SHARDS: shards.get_uri(),
            ASSETS: assets.get_uri(),
        }


def create_vanilla_dataset(
    shards: ShardDict[ShardTuple[BaseShard[T]]],
    assets: ShardDict,
    uri: str,
) -> VanillaDataset:
    r"""Create a ``VanillaDataset`` from its shards.

    Note:
        It is a utility function to create a ``VanillaDataset`` from
            its shards and URI. It is possible to create a
            ``VanillaDataset`` in other ways.

    Args:
        shards: The dataset's shards. Each item in the mapping
            represent a dataset split, where the key is the dataset
            split and the value is the shards.
        assets: The dataset's assets.
        uri: The URI associated to the dataset.

    Returns:
        The instantited ``VanillaDataset`` object.

    Example usage:

    ```pycon

    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.dataset import create_vanilla_dataset
    >>> from iden.shard import create_json_shard, create_shard_dict, create_shard_tuple
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     shards = create_shard_dict(
    ...         shards={
    ...             "train": create_shard_tuple(
    ...                 [
    ...                     create_json_shard(
    ...                         [1, 2, 3], uri=Path(tmpdir).joinpath("shard/uri1").as_uri()
    ...                     ),
    ...                     create_json_shard(
    ...                         [4, 5, 6, 7], uri=Path(tmpdir).joinpath("shard/uri2").as_uri()
    ...                     ),
    ...                 ],
    ...                 uri=Path(tmpdir).joinpath("uri_train").as_uri(),
    ...             ),
    ...             "val": create_shard_tuple(
    ...                 shards=[],
    ...                 uri=Path(tmpdir).joinpath("uri_val").as_uri(),
    ...             ),
    ...         },
    ...         uri=Path(tmpdir).joinpath("uri_shards").as_uri(),
    ...     )
    ...     assets = create_shard_dict(
    ...         shards={
    ...             "stats": create_json_shard(
    ...                 [1, 2, 3], uri=Path(tmpdir).joinpath("uri_stats").as_uri()
    ...             )
    ...         },
    ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
    ...     )
    ...     dataset = create_vanilla_dataset(
    ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
    ...     )
    ...     dataset
    ...
    VanillaDataset(
      (uri): file:///.../uri
      (shards): ShardDict(
          (uri): file:///.../uri_shards
          (shards):
            (train): ShardTuple(
                (uri): file:///.../uri_train
                (shards):
                  (0): JsonShard(uri=file:///.../shard/uri1)
                  (1): JsonShard(uri=file:///.../shard/uri2)
              )
            (val): ShardTuple(
                (uri): file:///.../uri_val
                (shards):
              )
        )
      (assets): ShardDict(
          (uri): file:///.../uri_assets
          (shards):
            (stats): JsonShard(uri=file:///.../uri_stats)
        )
    )

    ```
    """
    logger.info(f"Saving URI file {uri}")
    JsonSaver().save(
        VanillaDataset.generate_uri_config(shards=shards, assets=assets), sanitize_path(uri)
    )
    return VanillaDataset(uri=uri, shards=shards, assets=assets)


def check_shards(shards: BaseShard) -> None:
    r"""Check if the shards have a valid configuration.

    The shards must be sorted by ascending order of URIs.

    Args:
        shards: The shards to check.

    Raises:
        TypeError: if the type is incorrect.
        RuntimeError: if the shard configuration is incorrect.
    """
    if not isinstance(shards, ShardDict):
        msg = f"Incorrect shard type: {type(shards)}"
        raise TypeError(msg)
    for shard_id in shards.get_shard_ids():
        if not shards.get_shard(shard_id).is_sorted_by_uri():
            msg = f"split '{shard_id}' is not sorted by ascending order of URIs"
            raise RuntimeError(msg)
