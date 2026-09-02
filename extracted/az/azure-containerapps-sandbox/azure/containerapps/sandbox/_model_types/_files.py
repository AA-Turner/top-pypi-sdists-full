"""File and directory listing models."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FileInfo:
    """Information about a file or directory."""
    name: str = ""
    path: str = ""
    size: int | None = None
    is_directory: bool = False
    modified_at: str | None = None
    mode: str | None = None

    @classmethod
    def _from_dict(cls, d: dict) -> FileInfo:
        return cls(
            name=d.get("name", ""),
            path=d.get("path", ""),
            size=d.get("size"),
            is_directory=d.get("isDirectory", False),
            modified_at=d.get("modifiedAt"),
            mode=d.get("mode"),
        )


@dataclass(frozen=True)
class DirListing:
    """Directory listing result."""
    path: str = ""
    entries: list[FileInfo] = field(default_factory=list)

    @classmethod
    def _from_dict(cls, d: dict) -> DirListing:
        return cls(
            path=d.get("path", ""),
            entries=[FileInfo._from_dict(e) for e in d.get("entries", [])],
        )
