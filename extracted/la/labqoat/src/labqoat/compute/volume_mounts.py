"""Freeze explicit mount declarations without exposing runtime-owned filesystem paths."""

import re
from collections.abc import Mapping
from pathlib import PurePosixPath
from typing import ClassVar

from labqoat.compute.volume import Volume
from labqoat.json_document import JsonValue


class VolumeMounts:
    """Keep persistent shared storage separate from code, credentials, and per-invocation scratch."""

    reserved: ClassVar[tuple[str, ...]] = (
        "/bin",
        "/dev",
        "/etc",
        "/lib",
        "/lib64",
        "/proc",
        "/run",
        "/sbin",
        "/sys",
        "/tmp",
        "/usr",
        "/workspace",
        "/labqoat-cache",
        "/opt/app",
        "/opt/labqoat-sdk",
        "/opt/runtime",
        "/opt/labqoat-runtime",
    )

    @classmethod
    def capture(cls, mounts: Mapping[str, Volume] | None) -> tuple[tuple[str, Volume], ...]:
        """Snapshot caller mappings and reject overlapping mounts before source publication."""
        entries = tuple(sorted((mounts or {}).items()))
        if len(entries) > 16:
            raise ValueError("At most 16 persistent volumes may be mounted")
        for path, _volume in entries:
            cls.validate_path(path)
            if any(other != path and other.startswith(path + "/") for other, _item in entries):
                raise ValueError("Volume mount paths cannot overlap")
        return entries

    @classmethod
    def validate_path(cls, path: str) -> None:
        """Allow normalized portable paths that cannot replace managed worker files."""
        if len(path) > 256 or re.fullmatch(r"/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+", path) is None:
            raise ValueError("Volume mounts require a portable absolute path of at most 256 characters")
        if ".." in path.split("/") or str(PurePosixPath(path)) != path:
            raise ValueError("Volume mount paths must be normalized")
        if any(path == root or path.startswith(root + "/") or root.startswith(path + "/") for root in cls.reserved):
            raise ValueError("Volume mounts cannot replace managed runtime paths")

    @staticmethod
    def to_dict(mounts: tuple[tuple[str, Volume], ...]) -> dict[str, JsonValue] | None:
        """Omit absent mounts so existing execution identities remain unchanged."""
        return {path: volume.to_dict() for path, volume in mounts} or None
