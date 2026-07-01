from __future__ import annotations

from dreadnode.datasets.local import LocalDataset
from dreadnode.storage.storage import Storage


def _default_storage() -> Storage:
    from dreadnode import DEFAULT_INSTANCE

    if DEFAULT_INSTANCE._storage is not None:
        return DEFAULT_INSTANCE.storage
    return Storage()


class Dataset(LocalDataset):
    """Published dataset loader backed by local storage manifests."""

    def __init__(
        self,
        name: str,
        storage: Storage | None = None,
        version: str | None = None,
    ) -> None:
        super().__init__(name, storage or _default_storage(), version=version)


def load_dataset(
    name: str,
    *,
    storage: Storage | None = None,
    version: str | None = None,
) -> Dataset:
    """Load a published dataset manifest from local storage."""
    return Dataset(name, storage=storage, version=version)
