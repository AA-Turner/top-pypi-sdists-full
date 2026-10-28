"""Local materialization of an immutable System tree."""

from __future__ import annotations

import os
import stat
import zipfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Protocol

from istari_digital_client._tree_core import (
    MaterializationConflictError,
    MaterializationError,
    digest,
    validate_tree_paths,
    write_file,
)

__all__ = [
    "MaterializationConflictError",
    "MaterializationError",
    "MaterializationResult",
    "PackageContentDeniedError",
    "materialize_system_tree",
]


class _SystemTreeClient(Protocol):
    def get_system_tree(self, snapshot_id: str) -> Any: ...

    def download_system_tree_archive(self, snapshot_id: str) -> bytearray: ...


@dataclass(frozen=True)
class MaterializationResult:
    """Where one snapshot was written and which tree paths it wrote."""

    destination: Path
    snapshot_id: str
    written_paths: tuple[str, ...]


class PackageContentDeniedError(MaterializationError):
    """The current user cannot download every package file in the System tree."""

    def __init__(self, entries: list[Any]) -> None:
        """Record the paths of the denied tree entries."""
        self.paths = tuple(sorted(entry.path for entry in entries))
        super().__init__(
            f"System tree package content is not accessible: {', '.join(self.paths)}"
        )


def materialize_system_tree(
    client: _SystemTreeClient,
    snapshot_id: str,
    destination: str | os.PathLike[str],
    *,
    overwrite: bool = False,
) -> MaterializationResult:
    """Download one verified System tree and write it under ``destination``."""
    root = Path(destination).absolute()
    if root.is_symlink() or (root.exists() and not root.is_dir()):
        raise MaterializationConflictError(
            {str(root)}, "destination is not a directory"
        )
    if not overwrite and root.exists() and any(root.iterdir()):
        raise MaterializationConflictError(
            (child.name for child in root.iterdir()), "destination is not empty"
        )
    tree = client.get_system_tree(snapshot_id)
    entries = {entry.path: entry for entry in tree.entries}
    denied = [
        entry
        for entry in entries.values()
        if entry.kind in {"package", "placement"}
        and "download" not in (entry.allowed_actions or ())
    ]
    if denied:
        raise PackageContentDeniedError(denied)
    validate_tree_paths(entries)
    content = _read_archive(
        bytes(client.download_system_tree_archive(snapshot_id)), entries
    )
    for path, value in content.items():
        write_file(root, path, value, replace=overwrite)
    return MaterializationResult(root, str(snapshot_id), tuple(sorted(content)))


def _read_archive(archive: bytes, entries: dict[str, Any]) -> dict[str, bytes]:
    content: dict[str, bytes] = {}
    try:
        with zipfile.ZipFile(BytesIO(archive)) as package:
            for member in package.infolist():
                entry = entries.get(member.filename)
                if entry is None or member.filename in content:
                    raise MaterializationConflictError(
                        {member.filename}, "archive path is not in the System tree"
                    )
                if not stat.S_ISREG(member.external_attr >> 16) or (
                    entry.size is not None and member.file_size != entry.size
                ):
                    raise MaterializationConflictError(
                        {member.filename},
                        "archive entry does not match the System tree",
                    )
                value = package.read(member)
                if digest(value, entry.checksum_salt) != entry.checksum:
                    raise MaterializationConflictError(
                        {member.filename},
                        "archive entry does not match the System tree",
                    )
                content[member.filename] = value
    except zipfile.BadZipFile as exc:
        raise MaterializationError(
            "System tree archive is not a valid ZIP file"
        ) from exc
    if missing := entries.keys() - content.keys():
        raise MaterializationConflictError(missing, "archive omits System tree paths")
    return content
