"""Portable directory synchronization over versioned project files and verified assets."""

from __future__ import annotations
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.memory_writes import MemoryWrites

if TYPE_CHECKING:
    from labqoat.assets_client import AssetsClient
    from labqoat.management_client import ManagementClient


class MemoryFileTransfer:
    """Share authored project trees while rejecting paths that escape the destination."""

    def __init__(self, client: ManagementClient, assets: AssetsClient, project: str) -> None:
        """Use explicit clients for metadata and content transfer; the project name scopes retry keys."""
        self.client = client
        self.assets = assets
        self.project = project

    def heads(self, path: str = "") -> dict[str, JsonDocument]:
        """Consume all bounded path pages and detect repeated cursors."""
        result: dict[str, JsonDocument] = {}
        after: str | None = None
        seen: set[str] = set()
        while True:
            page = self.client.get("/api/v1/memory/files", {"path": path, "after": after, "limit": 500})
            for raw in JsonDocument.expect_list(page["items"]):
                item = JsonDocument.expect_dict(raw)
                result[str(item["path"])] = item
            cursor = page.get("next_cursor")
            if cursor is None:
                return result
            if not isinstance(cursor, str) or cursor in seen:
                raise ValueError("Invalid project file pagination cursor.")
            seen.add(cursor)
            after = cursor

    def push(self, source: Path, remote: str | None = None) -> JsonDocument:
        """Skip unchanged content and publish each changed file under its checked head."""
        prefix = remote or self.default_path(source)
        self.validate_path(prefix)
        files = self.local_files(source)
        heads = self.heads(prefix)
        items: list[JsonValue] = []
        for path in files:
            name = f"{prefix}/{path.relative_to(source).as_posix()}" if source.is_dir() else prefix
            items.append(self.push_one(path, name, heads.get(name)))
        return JsonDocument({"items": items})

    def push_one(self, path: Path, name: str, previous: JsonDocument | None) -> JsonDocument:
        """Reuse asset bytes and a deterministic request identity for one changed file."""
        digest, size = self.assets.hash_file(path)
        if previous is not None and previous["sha256"] == digest and previous["byte_size"] == size:
            return JsonDocument({**previous, "skipped": True})
        asset = self.assets.upload_file(path, key="memory-asset:" + digest)
        payload = JsonDocument(
            {"path": name, "asset_id": asset.id, "expected_version": 0 if previous is None else previous["version"]}
        )
        target = "/api/v1/memory/files"
        payload["idempotency_key"] = MemoryWrites.key(target, {"project": self.project}, payload)
        return MemoryWrites.send(self.client, target, {}, payload)

    def pull(self, path: str, directory: Path) -> JsonDocument:
        """Download the shared tree with verified content and safe relative paths."""
        heads = self.heads(path)
        directory.mkdir(parents=True, exist_ok=True)
        items: list[JsonValue] = []
        for name, file in heads.items():
            destination = self.destination(directory, name)
            self.assets.download_to(str(file["asset_id"]), destination)
            items.append({"path": name, "version": file["version"], "asset_id": file["asset_id"]})
        return JsonDocument({"items": items})

    @staticmethod
    def default_path(source: Path) -> str:
        """Preserve ordinary relative paths without exposing a local absolute path."""
        return source.name if source.is_absolute() or ".." in source.parts else source.as_posix()

    @staticmethod
    def validate_path(name: str) -> None:
        """Reject absolute paths, traversal, platform separators and control bytes."""
        invalid_parts = any(part in ("", ".", "..") for part in name.split("/"))
        invalid_chars = any(ord(char) < 32 or ord(char) == 127 or char in "\\:" for char in name)
        if invalid_parts or invalid_chars or len(name.encode("utf-8")) > 1024:
            raise ValueError("Project files require a portable relative path.")

    @staticmethod
    def local_files(source: Path) -> list[Path]:
        """Enumerate a requested tree without following links or uploading hidden local configuration."""
        if source.is_symlink():
            raise ValueError("Project file sources cannot be symbolic links.")
        if source.is_file():
            return [source]
        if not source.is_dir():
            raise ValueError("Project file source does not exist.")
        paths = sorted(source.rglob("*"))
        if any(path.is_symlink() for path in paths):
            raise ValueError("Project file directories cannot contain symbolic links.")
        return [
            path
            for path in paths
            if path.is_file() and not any(part.startswith(".") for part in path.relative_to(source).parts)
        ]

    @staticmethod
    def destination(directory: Path, name: str) -> Path:
        """Refuse symlinks throughout the destination tree before replacing bytes."""
        MemoryFileTransfer.validate_path(name)
        if directory.is_symlink():
            raise ValueError("Project file destinations cannot contain symbolic links.")
        current = directory
        for part in PurePosixPath(name).parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("Project file destinations cannot contain symbolic links.")
        current.parent.mkdir(parents=True, exist_ok=True)
        return current
