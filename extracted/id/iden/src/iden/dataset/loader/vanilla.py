r"""Contain shard loader implementations for
``VanillaDatasetLoader``."""

from __future__ import annotations

__all__ = ["VanillaDatasetLoader"]

from typing import TypeVar

from iden.dataset.loader.base import BaseDatasetLoader
from iden.dataset.vanilla import VanillaDataset

T = TypeVar("T")


class VanillaDatasetLoader(BaseDatasetLoader[T]):
    r"""Implement a ``VanillaDatasetLoader`` loader.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.dataset import create_vanilla_dataset
    >>> from iden.dataset.loader import VanillaDatasetLoader
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
    ...     loader = VanillaDatasetLoader()
    ...     dataset = loader.load(uri)
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

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def load(self, uri: str) -> VanillaDataset[T]:
        return VanillaDataset.from_uri(uri)
