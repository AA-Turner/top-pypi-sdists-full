"""Filesystem resource — a named, mountable storage volume backed by Airstore."""

from __future__ import annotations

import posixpath
from typing import Any


def file(path: str, *, label: str | None = None) -> dict[str, Any]:
    """Return a stable, JSON-safe reference to an app filesystem path.

    The returned value is intended for table cells and collection rows. It is
    not a presigned URL; Capsule resolves the path when a user opens it.
    """
    normalized = _normalize_app_path(path)
    ref: dict[str, Any] = {"_type": "file", "path": normalized}
    if label:
        ref["label"] = label
    return ref


class FileSystem:
    """Declare a named filesystem that can be mounted into an app.

    Usage::

        fs = cpsl.FileSystem("my-data")

        @app.cls(
            image=cpsl.Image(...),
            filesystems={"/data": fs},
        )
        class MyApp:
            ...
    """

    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("FileSystem name must not be empty")
        self.name = name
        self._mount_path: str | None = None
        self._sources: list[dict[str, Any]] = []
        self._tools: list[dict[str, Any]] = []

    def link(self, path: str, *, label: str | None = None) -> dict[str, Any]:
        """Return a stable file reference under this filesystem's mount path."""
        if not self._mount_path:
            raise RuntimeError(
                f"FileSystem {self.name!r} is not mounted yet; "
                "use cpsl.file('/mount/path') or pass the FileSystem to App(filesystems=...) first"
            )
        rel = str(path).lstrip("/")
        return file(posixpath.join(self._mount_path, rel), label=label)

    def smart_source(
        self,
        integration: str,
        name: str,
        *,
        guidance: str = "",
        output_format: str = "folder",
        file_ext: str = "",
        filename_format: str = "",
        cache_ttl: int = 0,
    ) -> "FileSystem":
        """Expose a smart Airstore source view under ``/sources``.

        The Airstore source service infers the provider query from ``name`` and
        optional ``guidance``.
        """
        self._append_source(
            mode="smart",
            integration=integration,
            name=name,
            guidance=guidance,
            output_format=output_format,
            file_ext=file_ext,
            filename_format=filename_format,
            cache_ttl=cache_ttl,
        )
        return self

    def source_query(
        self,
        integration: str,
        name: str,
        *,
        filter: dict[str, Any] | str,
        output_format: str = "folder",
        file_ext: str = "",
        filename_format: str = "",
        cache_ttl: int = 0,
    ) -> "FileSystem":
        """Expose a manual Airstore source view under ``/sources``."""
        self._append_source(
            mode="query",
            integration=integration,
            name=name,
            filter=filter,
            output_format=output_format,
            file_ext=file_ext,
            filename_format=filename_format,
            cache_ttl=cache_ttl,
        )
        return self

    def mcp(
        self,
        name: str,
        *,
        command: str | None = None,
        args: list[str] | None = None,
        url: str | None = None,
        env: dict[str, str] | None = None,
        transport: str | None = None,
    ) -> "FileSystem":
        """Expose an MCP server under ``/tools`` for this filesystem."""
        if not command and not url:
            raise ValueError("mcp requires either command= or url=")
        self._append_tool(
            kind="mcp",
            name=name,
            command=command,
            args=args or [],
            url=url,
            env=env or {},
            transport=transport or ("stdio" if command else "http"),
        )
        return self

    def tool(self, name: str, **config: Any) -> "FileSystem":
        """Expose a workspace tool under ``/tools`` for this filesystem."""
        kind = config.pop("kind", "mcp")
        self._append_tool(kind=kind, name=name, **config)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "sources": list(self._sources),
            "tools": list(self._tools),
        }

    def _append_source(self, **source: Any) -> None:
        if not source.get("integration"):
            raise ValueError("source integration must not be empty")
        if not source.get("name"):
            raise ValueError("source name must not be empty")
        output_format = source.get("output_format")
        if output_format not in {"folder", "file"}:
            raise ValueError("output_format must be 'folder' or 'file'")
        self._sources.append(source)

    def _append_tool(self, **tool: Any) -> None:
        if not tool.get("name"):
            raise ValueError("tool name must not be empty")
        self._tools.append(tool)

    def _bind_mount_path(self, mount_path: str) -> None:
        self._mount_path = _normalize_app_path(mount_path)

    def __repr__(self) -> str:
        return f"FileSystem({self.name!r})"


def _normalize_app_path(path: str) -> str:
    if not path:
        raise ValueError("file path must not be empty")
    if not path.startswith("/"):
        raise ValueError("file path must start with '/'")
    normalized = posixpath.normpath(path)
    if normalized == ".":
        normalized = "/"
    return normalized
