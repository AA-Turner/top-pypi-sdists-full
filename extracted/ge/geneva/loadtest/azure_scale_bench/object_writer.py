# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Object-storage read/write seam for the image upload + download jobs.

A tiny ``ObjectWriter`` / ``ObjectReader`` abstraction so the upload and download
jobs are testable with local filesystem implementations and run against Azure Blob
in production. The writer does conditional create (``overwrite=False`` → raise
``ObjectExistsError`` on conflict), unconditional overwrite, and HEAD; the upload
job decides what to do on conflict. The reader does a single GET, returning
``None`` when the object is absent.

A **sync** ``azure-storage-blob`` client is used deliberately. The production
upload/download UDFs are per-row scalar UDFs run by the Geneva applier (per-worker
concurrency comes from ``intra_applier_concurrency``), and a sync client is not
event-loop-bound, so it can be cached per worker process and reused across the
fragment's per-row calls without the asyncio loop-lifecycle pitfalls of caching
``aio`` clients across UDF invocations. Credentials are resolved on the WORKER from
env (``AZURE_STORAGE_ACCOUNT_KEY_<ACCOUNT>`` or ``AZURE_STORAGE_ACCOUNT_KEY``) or
``DefaultAzureCredential`` — never passed through the UDF manifest.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, NamedTuple, Protocol


def _resolve_account_key(account_name: str) -> str | None:
    """Account key from a per-account env, then a shared env (worker-side)."""
    per_account = os.environ.get(f"AZURE_STORAGE_ACCOUNT_KEY_{account_name.upper()}")
    return per_account or os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")


def _build_container_client(account_name: str, container: str) -> Any:
    """Build a sync ``ContainerClient`` (account key, else DefaultAzureCredential)."""
    from azure.storage.blob import BlobServiceClient

    account_url = f"https://{account_name}.blob.core.windows.net"
    key = _resolve_account_key(account_name)
    if key:
        service = BlobServiceClient(account_url, credential=key)
    else:
        from azure.identity import DefaultAzureCredential

        service = BlobServiceClient(account_url, credential=DefaultAzureCredential())
    return service.get_container_client(container)


class ObjectExistsError(Exception):
    """Raised by ``put(..., overwrite=False)`` when the object already exists."""


class ObjectStat(NamedTuple):
    """Size, etag, and (if available) content MD5 of an existing object."""

    size_bytes: int
    etag: str
    content_md5: str | None = None


class ObjectWriter(Protocol):
    """Minimal HEAD/PUT surface the upload job needs."""

    def head(self, key: str) -> ObjectStat | None:
        """Return the object's size/etag/md5, or ``None`` if it does not exist."""
        ...

    def put(
        self,
        key: str,
        data: bytes,
        *,
        content_type: str,
        content_md5: str | None = None,
        overwrite: bool = True,
    ) -> str:
        """Upload ``data`` at ``key`` and return the etag.

        With ``overwrite=False`` this is a conditional create: it raises
        ``ObjectExistsError`` if the object already exists (so the common fresh-seed
        path is a single PUT and no HEAD). ``content_md5`` (hex) is stored for a
        later integrity check.
        """
        ...


def content_type_for(image_format: str) -> str:
    """The blob content-type for a rendered image format."""
    return "image/jpeg" if image_format.lower() in ("jpg", "jpeg") else "image/png"


def md5_hex(data: bytes) -> str:
    """Hex MD5 of ``data`` (used as the local etag + the content-integrity check)."""
    return hashlib.md5(data, usedforsecurity=False).hexdigest()


class LocalFileWriter:
    """Filesystem-backed ``ObjectWriter`` for tests / local dry-runs.

    Writes to ``<base_dir>/<container>/<key>``; the etag + content_md5 are the MD5.
    """

    def __init__(self, base_dir: str | Path, container: str) -> None:
        self._root = Path(base_dir) / container

    def _path(self, key: str) -> Path:
        return self._root / key

    def head(self, key: str) -> ObjectStat | None:
        path = self._path(key)
        if not path.is_file():
            return None
        digest = md5_hex(path.read_bytes())
        return ObjectStat(path.stat().st_size, digest, digest)

    def put(
        self,
        key: str,
        data: bytes,
        *,
        content_type: str,
        content_md5: str | None = None,
        overwrite: bool = True,
    ) -> str:
        path = self._path(key)
        if not overwrite and path.is_file():
            raise ObjectExistsError(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return md5_hex(data)


class AzureBlobWriter:
    """Azure Blob ``ObjectWriter`` (sync ``azure-storage-blob``, one per account)."""

    def __init__(self, account_name: str, container: str) -> None:
        self._account = account_name
        self._container = container
        self._client = _build_container_client(account_name, container)

    def head(self, key: str) -> ObjectStat | None:
        from azure.core.exceptions import ResourceNotFoundError

        try:
            props = self._client.get_blob_client(key).get_blob_properties()
        except ResourceNotFoundError:
            return None
        raw_md5 = getattr(props.content_settings, "content_md5", None)
        return ObjectStat(
            int(props.size),
            (props.etag or "").strip('"'),
            bytes(raw_md5).hex() if raw_md5 else None,
        )

    def put(
        self,
        key: str,
        data: bytes,
        *,
        content_type: str,
        content_md5: str | None = None,
        overwrite: bool = True,
    ) -> str:
        from azure.core.exceptions import ResourceExistsError
        from azure.storage.blob import ContentSettings

        settings = ContentSettings(
            content_type=content_type,
            content_md5=bytearray.fromhex(content_md5) if content_md5 else None,
        )
        try:
            result = self._client.get_blob_client(key).upload_blob(
                data, overwrite=overwrite, content_settings=settings
            )
        except ResourceExistsError as exc:
            raise ObjectExistsError(key) from exc
        etag = result.get("etag", "") if isinstance(result, dict) else ""
        return (etag or "").strip('"')


class ObjectReader(Protocol):
    """Minimal GET surface the download job needs."""

    def get(self, key: str) -> bytes | None:
        """Return the object's bytes, or ``None`` if it does not exist."""
        ...


class LocalFileReader:
    """Filesystem-backed ``ObjectReader`` for tests / local dry-runs.

    Reads from ``<base_dir>/<container>/<key>`` (mirrors ``LocalFileWriter``).
    """

    def __init__(self, base_dir: str | Path, container: str) -> None:
        self._root = Path(base_dir) / container

    def get(self, key: str) -> bytes | None:
        path = self._root / key
        if not path.is_file():
            return None
        return path.read_bytes()


class AzureBlobReader:
    """Azure Blob ``ObjectReader`` (sync ``azure-storage-blob``, one per account)."""

    def __init__(self, account_name: str, container: str) -> None:
        self._account = account_name
        self._container = container
        self._client = _build_container_client(account_name, container)

    def get(self, key: str) -> bytes | None:
        from azure.core.exceptions import ResourceNotFoundError

        try:
            stream = self._client.get_blob_client(key).download_blob()
            return stream.readall()
        except ResourceNotFoundError:
            return None
