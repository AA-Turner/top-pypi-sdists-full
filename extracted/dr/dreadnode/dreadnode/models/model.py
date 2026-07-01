"""Model loader for published OCI-backed models."""

from __future__ import annotations

from dreadnode.models.local import LocalModel
from dreadnode.storage.storage import Storage


def _default_storage() -> Storage:
    from dreadnode import DEFAULT_INSTANCE

    if DEFAULT_INSTANCE._storage is not None:
        return DEFAULT_INSTANCE.storage
    return Storage()


class Model(LocalModel):
    """Published model loader backed by local storage manifests."""

    def __init__(
        self,
        name: str,
        storage: Storage | None = None,
        version: str | None = None,
    ) -> None:
        super().__init__(name, storage or _default_storage(), version=version)


def load_model(
    name: str,
    *,
    storage: Storage | None = None,
    version: str | None = None,
) -> Model:
    """Load a published model manifest from local storage."""
    return Model(name, storage=storage, version=version)
