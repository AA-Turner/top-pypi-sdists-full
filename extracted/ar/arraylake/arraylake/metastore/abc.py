from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from arraylake.types import Repo


class Metastore(ABC):  # pragma: no cover
    @abstractmethod
    async def ping(self) -> dict[str, Any]:
        """Verify that the metastore is accessible and responsive to the client."""
        ...

    @abstractmethod
    async def list_databases(self) -> Sequence[Repo]: ...

    @abstractmethod
    async def create_database(self, name: str):  # TODO: return type
        """Create a new metastore database.

        Parameters
        ----------
        name : str
            Name of repo

        Returns
        -------
        TODO
        """
        ...

    @abstractmethod
    async def delete_database(
        self,
        name: str,
        *,
        imsure: bool = False,
        imreallysure: bool = False,
        immediate: bool = False,
        retain_data: bool = False,
    ) -> None:
        """Delete an existing metastore database.

        Parameters
        ----------
        name : str
            Name of repo
        imsure, imreallysure : bool
            Confirm intent to delete.
        immediate : bool, default False
            Skip the soft-delete grace period and move straight to cleanup.
            With the default ``immediate=False`` the repo enters a recoverable
            "ghost" state for the grace period before the daily cleanup job
            takes it.
        retain_data : bool, default False
            Leave the bucket bytes alone when the cleanup runs; only the
            Arraylake metadata is removed.
        """
        ...
