"""High-level Chronos datasets client.

Provides a clean interface for managing dataset files and versions.
Used by hillclimb and other automation that needs tabular data for
parametrized experiments.
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from plato.chronos.api.datasets import (
    create_dataset_file,
    create_dataset_file_version,
    delete_dataset_file,
    delete_dataset_version,
    list_dataset_files,
    update_dataset_file,
    update_dataset_version,
)
from plato.chronos.models import (
    DatasetColumn,
    DatasetFileCreateRequest,
    DatasetFileResponse,
    DatasetFileUpdateRequest,
    DatasetVersionCreateRequest,
    Folder,
)

logger = logging.getLogger(__name__)


class AsyncDatasets:
    """Async client for the Chronos datasets API.

    Usage::

        from plato.chronos.datasets import AsyncDatasets

        datasets = AsyncDatasets(base_url="https://chronos.plato.so", api_key="pk_...")

        # List all dataset files
        files = await datasets.list_files()

        # Get a dataset file by ID
        file = await datasets.get_file("file-public-id")

        # Create a dataset file with columns and rows
        file = await datasets.create_file(
            name="my-dataset",
            columns=[{"name": "url", "type": "str"}, {"name": "expected", "type": "str"}],
            rows=[{"url": "https://example.com", "expected": "Homepage"}],
        )

        # Create a new version with updated rows
        file = await datasets.create_version(
            file_id="file-public-id",
            columns=[{"name": "url", "type": "str"}],
            rows=[{"url": "https://example.com/new"}],
        )

        # Delete
        await datasets.delete_file("file-public-id")
        await datasets.delete_version("version-public-id")
    """

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        client: httpx.AsyncClient | None = None,
    ):
        if client is not None:
            self._client = client
            self._owns_client = False
        else:
            resolved_url = (base_url or os.environ.get("CHRONOS_URL", "https://chronos.plato.so")).rstrip("/")
            resolved_key = api_key or os.environ.get("PLATO_API_KEY", "")
            headers = {"X-API-Key": resolved_key} if resolved_key else {}
            self._client = httpx.AsyncClient(
                base_url=resolved_url,
                headers=headers,
                timeout=60.0,
            )
            self._owns_client = True

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> AsyncDatasets:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    # -----------------------------------------------------------------------
    # Dataset files
    # -----------------------------------------------------------------------

    async def list_files(self, *, folder: str | None = None) -> list[DatasetFileResponse]:
        """List all dataset files, optionally filtered by folder."""
        response = await list_dataset_files.asyncio(self._client, folder=folder)
        return list(response.files)

    async def get_file(self, file_id: str) -> DatasetFileResponse:
        """Get a dataset file by public ID (includes versions with rows)."""
        response = await list_dataset_files.asyncio(self._client)
        for f in response.files:
            if f.public_id == file_id:
                return f
        raise ValueError(f"Dataset file '{file_id}' not found")

    async def create_file(
        self,
        *,
        name: str,
        description: str | None = None,
        columns: list[dict[str, Any]] | None = None,
        rows: list[dict[str, Any]] | None = None,
        folder: str | None = None,
        notes: str | None = None,
    ) -> DatasetFileResponse:
        """Create a new dataset file with an initial version."""
        col_models = None
        if columns:
            col_models = [DatasetColumn(**c) for c in columns]
        return await create_dataset_file.asyncio(
            self._client,
            body=DatasetFileCreateRequest(
                name=name,
                description=description,
                columns=col_models,
                rows=rows,
                folder=Folder(folder) if folder else None,
                notes=notes,
            ),
        )

    async def update_file(
        self,
        file_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        folder: str | None = None,
    ) -> DatasetFileResponse:
        """Update dataset file metadata."""
        kwargs: dict[str, Any] = {}
        if name is not None:
            kwargs["name"] = name
        if description is not None:
            kwargs["description"] = description
        if folder is not None:
            kwargs["folder"] = folder
        return await update_dataset_file.asyncio(
            self._client,
            public_id=file_id,
            body=DatasetFileUpdateRequest(**kwargs),
        )

    async def delete_file(self, file_id: str) -> None:
        """Delete a dataset file and all its versions."""
        await delete_dataset_file.asyncio(self._client, public_id=file_id)

    # -----------------------------------------------------------------------
    # Dataset versions
    # -----------------------------------------------------------------------

    async def create_version(
        self,
        *,
        file_id: str,
        columns: list[dict[str, Any]] | None = None,
        rows: list[dict[str, Any]] | None = None,
        notes: str | None = None,
    ) -> DatasetFileResponse:
        """Create a new version of a dataset file."""
        col_models = None
        if columns:
            col_models = [DatasetColumn(**c) for c in columns]
        return await create_dataset_file_version.asyncio(
            self._client,
            public_id=file_id,
            body=DatasetVersionCreateRequest(
                columns=col_models,
                rows=rows,
                notes=notes,
            ),
        )

    async def update_version(
        self,
        version_id: str,
        *,
        columns: list[dict[str, Any]] | None = None,
        rows: list[dict[str, Any]] | None = None,
        notes: str | None = None,
    ) -> DatasetFileResponse:
        """Update a dataset version's mutable fields."""
        col_models = None
        if columns:
            col_models = [DatasetColumn(**c) for c in columns]
        return await update_dataset_version.asyncio(
            self._client,
            public_id=version_id,
            body=DatasetVersionCreateRequest(
                columns=col_models,
                rows=rows,
                notes=notes,
            ),
        )

    async def delete_version(self, version_id: str) -> None:
        """Delete a single dataset version."""
        await delete_dataset_version.asyncio(self._client, public_id=version_id)


class Datasets:
    """Synchronous client for the Chronos datasets API.

    Usage::

        from plato.chronos.datasets import Datasets

        datasets = Datasets(base_url="https://chronos.plato.so", api_key="pk_...")
        files = datasets.list_files()
        file = datasets.get_file("file-public-id")
    """

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        client: httpx.Client | None = None,
    ):
        if client is not None:
            self._client = client
            self._owns_client = False
        else:
            resolved_url = (base_url or os.environ.get("CHRONOS_URL", "https://chronos.plato.so")).rstrip("/")
            resolved_key = api_key or os.environ.get("PLATO_API_KEY", "")
            headers = {"X-API-Key": resolved_key} if resolved_key else {}
            self._client = httpx.Client(
                base_url=resolved_url,
                headers=headers,
                timeout=60.0,
            )
            self._owns_client = True

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> Datasets:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def list_files(self, *, folder: str | None = None) -> list[DatasetFileResponse]:
        response = list_dataset_files.sync(self._client, folder=folder)
        return list(response.files)

    def get_file(self, file_id: str) -> DatasetFileResponse:
        response = list_dataset_files.sync(self._client)
        for f in response.files:
            if f.public_id == file_id:
                return f
        raise ValueError(f"Dataset file '{file_id}' not found")

    def create_file(
        self,
        *,
        name: str,
        description: str | None = None,
        columns: list[dict[str, Any]] | None = None,
        rows: list[dict[str, Any]] | None = None,
        folder: str | None = None,
        notes: str | None = None,
    ) -> DatasetFileResponse:
        col_models = None
        if columns:
            col_models = [DatasetColumn(**c) for c in columns]
        return create_dataset_file.sync(
            self._client,
            body=DatasetFileCreateRequest(
                name=name,
                description=description,
                columns=col_models,
                rows=rows,
                folder=Folder(folder) if folder else None,
                notes=notes,
            ),
        )

    def create_version(
        self,
        *,
        file_id: str,
        columns: list[dict[str, Any]] | None = None,
        rows: list[dict[str, Any]] | None = None,
        notes: str | None = None,
    ) -> DatasetFileResponse:
        col_models = None
        if columns:
            col_models = [DatasetColumn(**c) for c in columns]
        return create_dataset_file_version.sync(
            self._client,
            public_id=file_id,
            body=DatasetVersionCreateRequest(
                columns=col_models,
                rows=rows,
                notes=notes,
            ),
        )

    def delete_file(self, file_id: str) -> None:
        delete_dataset_file.sync(self._client, public_id=file_id)

    def delete_version(self, version_id: str) -> None:
        delete_dataset_version.sync(self._client, public_id=version_id)
