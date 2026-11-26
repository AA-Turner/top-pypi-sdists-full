"""File operations for sandbox data-plane client."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from azure.core.tracing.decorator import distributed_trace

from azure.containerapps.sandbox._helpers import _ERROR_MAP
from azure.containerapps.sandbox._models import DirListing, FileInfo
from azure.containerapps.sandbox._response_helpers import _normalize_response

if TYPE_CHECKING:
    pass

logger = logging.getLogger("azure.containerapps.sandbox")


class FileOperationsMixin:
    """File operations for sandboxes (list, read, write, stat, delete, mkdir).

    Uses the host's private generated client and sandbox identifier.
    """

    @distributed_trace
    def list_files(self, path: str = "/", *,
                   container_name: str | None = None,
                   **kwargs: Any) -> DirListing:
        """List directory contents in a sandbox."""
        return self._generated.sandboxes.list_files(
            self._sandbox_id,
            path=path,
            container_name=container_name,
            **{"error_map": _ERROR_MAP, "cls": _normalize_response, **kwargs},
        )

    @distributed_trace
    def stat_file(self, path: str, *,
                  container_name: str | None = None,
                  **kwargs: Any) -> FileInfo:
        """Get file/directory metadata."""
        return self._generated.sandboxes.get_file_info(
            self._sandbox_id,
            path=path,
            container_name=container_name,
            **{"error_map": _ERROR_MAP, **kwargs},
        )

    @distributed_trace
    def read_file(self, path: str, *,
                  container_name: str | None = None,
                  **kwargs: Any) -> bytes:
        """Read a file from a sandbox (returns bytes)."""
        chunks = self._generated.sandboxes.read_file(
            self._sandbox_id, path=path, container_name=container_name, **{"error_map": _ERROR_MAP, **kwargs},
        )
        return b"".join(chunks)

    @distributed_trace
    def write_file(self, path: str, content: str | bytes, *,
                   create_dirs: bool = True,
                   mode: str | None = None,
                   container_name: str | None = None,
                   **kwargs: Any) -> None:
        """Write a file to a sandbox."""
        data = content.encode("utf-8") if isinstance(content, str) else content
        self._generated.sandboxes.write_file(
            self._sandbox_id, data, path=path, create_dirs=create_dirs,
            mode=int(mode, 8) if isinstance(mode, str) and mode else mode or None,
            container_name=container_name, **{"error_map": _ERROR_MAP, **kwargs},
        )

    @distributed_trace
    def delete_file(self, path: str, *,
                    recursive: bool = False,
                    container_name: str | None = None,
                    **kwargs: Any) -> None:
        """Delete a file or directory from a sandbox."""
        self._generated.sandboxes.delete_file(
            self._sandbox_id, path=path, recursive=recursive,
            container_name=container_name, **{"error_map": _ERROR_MAP, **kwargs},
        )

    @distributed_trace
    def mkdir(self, path: str, *,
              container_name: str | None = None,
              **kwargs: Any) -> None:
        """Create a directory in a sandbox."""
        self._generated.sandboxes.create_directory(
            self._sandbox_id, {"path": path}, container_name=container_name, **{"error_map": _ERROR_MAP, **kwargs},
        )
