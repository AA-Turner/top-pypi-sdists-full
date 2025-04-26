r"""Contain code to load a dataset from its Uniform Resource Identifier
(URI)."""

from __future__ import annotations

__all__ = ["load_from_uri"]

from typing import TYPE_CHECKING

from iden.constants import LOADER
from iden.dataset.loader.base import setup_dataset_loader
from iden.io import load_json
from iden.utils.path import sanitize_path

if TYPE_CHECKING:
    from iden.dataset import BaseDataset


def load_from_uri(uri: str) -> BaseDataset:
    r"""Load a dataset from its Uniform Resource Identifier (URI).

    Args:
        uri: The URI of the dataset.

    Returns:
        The dataset associated to the URI.

    Raises:
        FileNotFoundError: if the URI file does not exist.

    Example usage:

    ```pycon
    >>> import tempfile
    >>> from pathlib import Path
    >>> from iden.dataset import create_vanilla_dataset, load_from_uri
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
    ...     dataset = load_from_uri(uri)
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
    path = sanitize_path(uri)
    if not path.is_file():
        msg = f"uri file does not exist: {path}"
        raise FileNotFoundError(msg)
    config = load_json(path)
    loader = setup_dataset_loader(config[LOADER])
    return loader.load(uri)
