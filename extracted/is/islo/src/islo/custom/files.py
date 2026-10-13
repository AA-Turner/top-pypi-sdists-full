"""File upload/download helpers with safe archive extraction."""

from __future__ import annotations

import asyncio
import io
import math
import os
import tarfile
import typing
from pathlib import Path, PurePosixPath

import httpx

if typing.TYPE_CHECKING:
    from ..base_client import AsyncBaseIslo


# Used by Harbor integrations to avoid wrapping this helper in another retry loop.
ASYNC_UPLOAD_FILE_RETRY_ATTEMPTS = 6


def _safe_tar_extract(tar: tarfile.TarFile, dest: Path) -> None:
    """Extract a tar archive with path traversal protection."""
    dest = dest.resolve()
    for member in tar.getmembers():
        member_path = (dest / member.name).resolve()
        if not str(member_path).startswith(str(dest)):
            raise ValueError(f"Tar member {member.name!r} would escape target directory")
        if member.issym() or member.islnk():
            link_target = (dest / member.linkname).resolve()
            if not str(link_target).startswith(str(dest)):
                raise ValueError(f"Tar symlink {member.name!r} points outside target directory")
    tar.extractall(dest, filter="data")


def download_file_to_path(
    client: httpx.Client,
    base_url: str,
    sandbox_name: str,
    remote_path: str,
    local_path: str | Path,
    *,
    token: str | None = None,
    timeout: float = 60.0,
) -> Path:
    """Download a single file from a sandbox to a local path."""
    local = Path(local_path)
    local.parent.mkdir(parents=True, exist_ok=True)

    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with client.stream(
        "GET",
        f"{base_url}/sandboxes/{sandbox_name}/files",
        params={"path": remote_path},
        headers=headers,
        timeout=timeout,
    ) as response:
        response.raise_for_status()
        with open(local, "wb") as f:
            for chunk in response.iter_bytes(chunk_size=65536):
                f.write(chunk)

    return local


def download_dir_to_path(
    client: httpx.Client,
    base_url: str,
    sandbox_name: str,
    remote_path: str,
    local_dir: str | Path,
    *,
    token: str | None = None,
    timeout: float = 120.0,
) -> Path:
    """Download a directory as tar.gz and extract it safely to a local directory."""
    local = Path(local_dir)
    local.mkdir(parents=True, exist_ok=True)

    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    buf = io.BytesIO()
    with client.stream(
        "GET",
        f"{base_url}/sandboxes/{sandbox_name}/files-archive",
        params={"path": remote_path},
        headers=headers,
        timeout=timeout,
    ) as response:
        response.raise_for_status()
        for chunk in response.iter_bytes(chunk_size=65536):
            buf.write(chunk)

    buf.seek(0)
    with tarfile.open(fileobj=buf, mode="r:gz") as tar:
        _safe_tar_extract(tar, local)

    return local


def upload_file_from_path(
    client: httpx.Client,
    base_url: str,
    sandbox_name: str,
    local_path: str | Path,
    remote_path: str,
    *,
    token: str | None = None,
    timeout: float = 60.0,
) -> None:
    """Upload a local file to a sandbox."""
    local = Path(local_path)
    if not local.is_file():
        raise FileNotFoundError(f"Local file not found: {local}")

    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with open(local, "rb") as f:
        response = client.post(
            f"{base_url}/sandboxes/{sandbox_name}/files",
            params={"path": remote_path},
            headers=headers,
            files={"file": (local.name, f)},
            timeout=timeout,
        )
    response.raise_for_status()


def upload_dir_from_path(
    client: httpx.Client,
    base_url: str,
    sandbox_name: str,
    local_dir: str | Path,
    remote_path: str,
    *,
    token: str | None = None,
    timeout: float = 120.0,
    exclude: typing.Sequence[str] = (),
) -> None:
    """Upload a local directory as tar.gz archive to a sandbox."""
    local = Path(local_dir)
    if not local.is_dir():
        raise NotADirectoryError(f"Local directory not found: {local}")

    exclude_set = set(exclude)

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for root, dirs, files in os.walk(local):
            dirs[:] = [d for d in dirs if d not in exclude_set]
            for file in files:
                filepath = Path(root) / file
                arcname = str(PurePosixPath(filepath.relative_to(local)))
                if arcname not in exclude_set:
                    tar.add(filepath, arcname=arcname)

    buf.seek(0)

    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = client.post(
        f"{base_url}/sandboxes/{sandbox_name}/files-archive",
        params={"path": remote_path},
        headers=headers,
        files={"file": ("archive.tar.gz", buf, "application/gzip")},
        timeout=timeout,
    )
    response.raise_for_status()


# ---------------------------------------------------------------------------
# Async helpers — use the SDK client directly (no raw httpx needed)
# ---------------------------------------------------------------------------


async def _async_get_client_internals(
    client: AsyncBaseIslo,
) -> tuple[str, dict[str, str]]:
    """Extract base_url and auth headers from an async Fern-generated client.

    Uses ``async_get_headers()`` so the async token provider (API key exchange)
    is properly awaited.
    """
    wrapper = client._client_wrapper
    headers = await wrapper.async_get_headers()
    return wrapper.get_environment().compute, headers


async def async_upload_file(
    client: AsyncBaseIslo,
    sandbox_name: str,
    local_path: str | Path,
    remote_path: str,
    *,
    timeout: float = 60.0,
) -> None:
    """Upload a local file to a sandbox (async)."""
    local = Path(local_path)
    if not local.is_file():
        raise FileNotFoundError(f"Local file not found: {local}")

    base_url, headers = await _async_get_client_internals(client)
    async with httpx.AsyncClient() as http:
        for attempt in range(ASYNC_UPLOAD_FILE_RETRY_ATTEMPTS):
            try:
                # Open afresh on each attempt so the multipart body starts at byte zero.
                with open(local, "rb") as f:
                    response = await http.post(
                        f"{base_url}/sandboxes/{sandbox_name}/files",
                        params={"path": remote_path},
                        headers=headers,
                        files={"file": (local.name, f)},
                        timeout=timeout,
                    )
            except httpx.TransportError:
                if attempt == ASYNC_UPLOAD_FILE_RETRY_ATTEMPTS - 1:
                    raise
                await asyncio.sleep(min(2**attempt, 30))
                continue

            if response.status_code != 429 or attempt == ASYNC_UPLOAD_FILE_RETRY_ATTEMPTS - 1:
                response.raise_for_status()
                return

            retry_after = response.headers.get("Retry-After")
            try:
                delay = float(retry_after) if retry_after is not None else 0
            except ValueError:
                delay = 0
            if not math.isfinite(delay) or delay <= 0:
                delay = min(2**attempt, 30)
            await asyncio.sleep(delay)


async def async_download_file(
    client: AsyncBaseIslo,
    sandbox_name: str,
    remote_path: str,
    local_path: str | Path,
    *,
    timeout: float = 60.0,
) -> Path:
    """Download a single file from a sandbox to a local path (async)."""
    local = Path(local_path)
    local.parent.mkdir(parents=True, exist_ok=True)

    base_url, headers = await _async_get_client_internals(client)
    async with httpx.AsyncClient() as http:
        async with http.stream(
            "GET",
            f"{base_url}/sandboxes/{sandbox_name}/files",
            params={"path": remote_path},
            headers=headers,
            timeout=timeout,
        ) as response:
            response.raise_for_status()
            with open(local, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=65536):
                    f.write(chunk)
    return local


async def async_upload_dir(
    client: AsyncBaseIslo,
    sandbox_name: str,
    local_dir: str | Path,
    remote_path: str,
    *,
    timeout: float = 120.0,
    exclude: typing.Sequence[str] = (),
) -> None:
    """Upload a local directory as tar.gz archive to a sandbox (async)."""
    local = Path(local_dir)
    if not local.is_dir():
        raise NotADirectoryError(f"Local directory not found: {local}")

    exclude_set = set(exclude)

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for root, dirs, files in os.walk(local):
            dirs[:] = [d for d in dirs if d not in exclude_set]
            for file in files:
                filepath = Path(root) / file
                arcname = str(PurePosixPath(filepath.relative_to(local)))
                if arcname not in exclude_set:
                    tar.add(filepath, arcname=arcname)

    buf.seek(0)

    base_url, headers = await _async_get_client_internals(client)
    async with httpx.AsyncClient() as http:
        response = await http.post(
            f"{base_url}/sandboxes/{sandbox_name}/files-archive",
            params={"path": remote_path},
            headers=headers,
            files={"file": ("archive.tar.gz", buf, "application/gzip")},
            timeout=timeout,
        )
    response.raise_for_status()


async def async_download_dir(
    client: AsyncBaseIslo,
    sandbox_name: str,
    remote_path: str,
    local_dir: str | Path,
    *,
    timeout: float = 120.0,
) -> Path:
    """Download a directory as tar.gz and extract it safely (async)."""
    local = Path(local_dir)
    local.mkdir(parents=True, exist_ok=True)

    base_url, headers = await _async_get_client_internals(client)
    buf = io.BytesIO()
    async with httpx.AsyncClient() as http:
        async with http.stream(
            "GET",
            f"{base_url}/sandboxes/{sandbox_name}/files-archive",
            params={"path": remote_path},
            headers=headers,
            timeout=timeout,
        ) as response:
            response.raise_for_status()
            async for chunk in response.aiter_bytes(chunk_size=65536):
                buf.write(chunk)

    buf.seek(0)
    with tarfile.open(fileobj=buf, mode="r:gz") as tar:
        _safe_tar_extract(tar, local)
    return local
