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
    async def delete_database(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete an existing metastore database.

        Parameters
        ----------
        name : str
            Name of repo
        imsure, imreallsure : bool
            Confirm permanent deletion.
        """
        ...
