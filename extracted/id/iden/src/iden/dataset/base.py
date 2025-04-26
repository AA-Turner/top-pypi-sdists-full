r"""Contain the base class to implement a dataset object."""

from __future__ import annotations

__all__ = ["BaseDataset"]

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:

    from iden.shard import BaseShard

logger = logging.getLogger(__name__)

T = TypeVar("T")


class BaseDataset(Generic[T], ABC):
    r"""Define the base class to implement a dataset.

    Note this dataset class is very different from the PyTorch dataset
    class because it has a different goal. One of the goals is to help
    to organize and manage shards.

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

    @abstractmethod
    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        r"""Indicate if two datasets are equal or not.

        Args:
            other: The object to compare with.
            equal_nan: If ``True``, then two ``NaN``s will be
                considered equal.

        Returns:
            ``True`` if the two datasets are equal, otherwise ``False``.

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
        ...     dataset1 = VanillaDataset(
        ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
        ...     )
        ...     dataset2 = VanillaDataset(
        ...         uri=Path(tmpdir).joinpath("uri2").as_uri(), shards=shards, assets=assets
        ...     )
        ...     dataset1.equal(dataset2)
        ...
        False

        ```
        """

    @abstractmethod
    def get_asset(self, asset_id: str) -> Any:
        r"""Get a data asset from this sharded dataset.

        This method is useful to access some data variables/parameters
        that are not available before to load/preprocess the data.

        Args:
            asset_id: The asset ID used to find the asset.

        Returns:
            The asset.

        Raises:
            AssetNotFoundError: if the asset does not exist.

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
        ...                 {"mean": 42}, uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     dataset = VanillaDataset(
        ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
        ...     )
        ...     dataset.get_asset("stats").get_data()
        ...
        {'mean': 42}

        ```
        """

    @abstractmethod
    def has_asset(self, asset_id: str) -> bool:
        r"""Indicate if the asset exists or not.

        Args:
            asset_id: The asset ID used to find the asset.

        Returns:
            ``True`` if the asset exists, otherwise ``False``.

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
        ...                 {"mean": 42}, uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     dataset = VanillaDataset(
        ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
        ...     )
        ...     dataset.has_asset("stats")
        ...     dataset.has_asset("missing")
        ...
        True
        False

        ```
        """

    @abstractmethod
    def get_shards(self, split: str) -> tuple[BaseShard[T], ...]:
        r"""Get the shards for a given split.

        Returns:
            The shards for a given split. The shards are
                sorted by ascending order of URI.

        Raises:
            SplitNotFoundError: if the split does not exist.

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
        ...                 {"mean": 42}, uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     dataset = VanillaDataset(
        ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
        ...     )
        ...     dataset.get_shards("train")
        ...     dataset.get_shards("val")
        ...
        (JsonShard(uri=file:///.../uri1), JsonShard(uri=file:///.../uri2))
        ()

        ```
        """

    @abstractmethod
    def get_num_shards(self, split: str) -> int:
        r"""Get the number of shards for a given split.

        Returns:
            The number of shards in the dataset for a given split.

        Raises:
            SplitNotFoundError: if the split does not exist.

        Returns:
            The dataset splits.

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
        ...                 {"mean": 42}, uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     dataset = VanillaDataset(
        ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
        ...     )
        ...     dataset.get_num_shards("train")
        ...     dataset.get_num_shards("val")
        ...
        2
        0

        ```
        """

    @abstractmethod
    def get_splits(self) -> set[str]:
        r"""Get the available dataset splits.

        Returns:
            The dataset splits.

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
        ...                 {"mean": 42}, uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     dataset = VanillaDataset(
        ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
        ...     )
        ...     sorted(dataset.get_splits())
        ...
        ['train', 'val']

        ```
        """

    @abstractmethod
    def has_split(self, split: str) -> bool:
        r"""Indicate if a dataset split exists or not.

        Returns:
            ``True`` of the split exists, otherwise ``False``

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
        ...                 {"mean": 42}, uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     dataset = VanillaDataset(
        ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
        ...     )
        ...     dataset.has_split("train")
        ...     dataset.has_split("missing")
        ...
        True
        False

        ```
        """

    @abstractmethod
    def get_uri(self) -> str:
        r"""Get the Uniform Resource Identifier (URI) of the dataset.

        Returns:
            The dataset's URI.

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
        ...                 {"mean": 42}, uri=Path(tmpdir).joinpath("uri_stats").as_uri()
        ...             )
        ...         },
        ...         uri=Path(tmpdir).joinpath("uri_assets").as_uri(),
        ...     )
        ...     dataset = VanillaDataset(
        ...         uri=Path(tmpdir).joinpath("uri").as_uri(), shards=shards, assets=assets
        ...     )
        ...     dataset.get_uri()
        ...
        file:///.../uri

        ```
        """
