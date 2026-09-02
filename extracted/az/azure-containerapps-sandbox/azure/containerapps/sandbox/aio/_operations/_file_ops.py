"""Async file operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.rest import HttpRequest, HttpResponse
from azure.core.tracing.decorator_async import distributed_trace_async

from azure.containerapps.sandbox._helpers import _raise_if_error
from azure.containerapps.sandbox._models import DirListing, FileInfo

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


class AsyncFileOperationsMixin:
    """Async file operations for sandboxes (list, read, write, stat, delete, mkdir).

    Requires the host class to expose a ``_sbx_path`` property that returns the
    URL path for the sandbox (e.g. ``/subscriptions/.../sandboxes/{id}``).
    """

    @distributed_trace_async
    async def list_files(self, path: str = "/", *,
                         container_name: str | None = None,
                         **kwargs: Any) -> DirListing:
        """List directory contents in a sandbox."""
        params: dict = {"path": path, "api-version": self._api_version}
        if container_name:
            params["containerName"] = container_name
        result = await self._dp_get(f"{self._sbx_path}/files/list", params=params)
        return DirListing._from_dict(result)

    @distributed_trace_async
    async def stat_file(self, path: str, *,
                        container_name: str | None = None,
                        **kwargs: Any) -> FileInfo:
        """Get file/directory metadata."""
        params: dict = {"path": path, "api-version": self._api_version}
        if container_name:
            params["containerName"] = container_name
        result = await self._dp_get(f"{self._sbx_path}/files/stat", params=params)
        return FileInfo._from_dict(result)

    @distributed_trace_async
    async def read_file(self, path: str, *,
                        container_name: str | None = None,
                        **kwargs: Any) -> bytes:
        """Read a file from a sandbox (returns bytes)."""
        params: dict = {"path": path, "api-version": self._api_version}
        if container_name:
            params["containerName"] = container_name
        request = HttpRequest("GET", f"{self._endpoint}{self._sbx_path}/files", params=params)
        pipeline_response = await self._pipeline.run(request, stream=True)
        response = pipeline_response.http_response
        if response.status_code >= 400:
            await response.read()
            _raise_if_error(response)
        await response.read()
        return response.content

    @distributed_trace_async
    async def write_file(self, path: str, content: str | bytes, *,
                         create_dirs: bool = True,
                         mode: str | None = None,
                         container_name: str | None = None,
                         **kwargs: Any) -> None:
        """Write a file to a sandbox."""
        data = content.encode("utf-8") if isinstance(content, str) else content
        params: dict = {"path": path, "createDirs": str(create_dirs).lower(), "api-version": self._api_version}
        if mode:
            params["mode"] = mode
        if container_name:
            params["containerName"] = container_name
        request = HttpRequest(
            "PUT", f"{self._endpoint}{self._sbx_path}/files", content=data,
            headers={"Content-Type": "application/octet-stream"}, params=params,
        )
        await self._send_request(request)

    @distributed_trace_async
    async def delete_file(self, path: str, *,
                          recursive: bool = False,
                          container_name: str | None = None,
                          **kwargs: Any) -> None:
        """Delete a file or directory from a sandbox."""
        params: dict = {"path": path, "recursive": str(recursive).lower(), "api-version": self._api_version}
        if container_name:
            params["containerName"] = container_name
        request = HttpRequest("DELETE", f"{self._endpoint}{self._sbx_path}/files", params=params)
        pipeline_response = await self._pipeline.run(request)
        response = pipeline_response.http_response
        if response.status_code not in (200, 204):
            _raise_if_error(response)

    @distributed_trace_async
    async def mkdir(self, path: str, *,
                    container_name: str | None = None,
                    **kwargs: Any) -> None:
        """Create a directory in a sandbox."""
        params: dict = {"api-version": self._api_version}
        if container_name:
            params["containerName"] = container_name
        request = HttpRequest(
            "POST", f"{self._endpoint}{self._sbx_path}/files/mkdir", json={"path": path}, params=params,
        )
        await self._send_request(request)
