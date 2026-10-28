"""Tree-materialization rules shared by the SDK checkout and the agent's job-tree preparation.

Server tree paths are portable: forward-slash separated, no empty, ``.`` or ``..``
segments, no Windows-invalid characters or device names, and unique after NFC
normalization and case folding, with no path that is also a directory of another.
"""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
import unicodedata
from collections.abc import Callable, Iterable
from pathlib import Path

_WINDOWS_DEVICE_NAME = re.compile(
    r"^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?$", re.IGNORECASE
)
_WINDOWS_INVALID_CHARACTERS = frozenset('<>:"|?*')
_MAX_SEGMENT_BYTES = 255


class MaterializationError(RuntimeError):
    """The requested tree cannot be materialized."""


class MaterializationConflictError(MaterializationError):
    """Tree, archive, or local paths conflict with the requested materialization."""

    def __init__(self, paths: Iterable[str], message: str) -> None:
        """Record the conflicting paths in a stable order."""
        self.paths = tuple(sorted(paths))
        super().__init__(f"{message}: {', '.join(self.paths)}")


def path_parts(path: str) -> tuple[str, ...]:
    """Split a portable tree path into segments, rejecting unsafe ones."""
    parts = tuple(path.split("/"))
    if "\\" in path or any(part in {"", ".", ".."} or _unsafe(part) for part in parts):
        raise MaterializationConflictError({path}, "System tree path is unsafe")
    return parts


def validate_tree_paths(paths: Iterable[str]) -> dict[str, tuple[str, ...]]:
    """Segments of every path, once no two paths collide as files or as file and directory."""
    parts: dict[str, tuple[str, ...]] = {}
    keys: dict[str, str] = {}
    for path in paths:
        parts[path] = path_parts(path)
        key = unicodedata.normalize("NFC", path).casefold()
        if key in keys:
            raise MaterializationConflictError(
                {keys[key], path}, "System tree paths collide"
            )
        keys[key] = path
    directories = {
        "/".join(segments[:index])
        for segments in (key.split("/") for key in keys)
        for index in range(1, len(segments))
    }
    if collisions := directories & keys.keys():
        raise MaterializationConflictError(
            (keys[key] for key in collisions), "System tree paths are also directories"
        )
    return parts


def digest(content: bytes, salt: str | None) -> str:
    """The server's salted SHA-384 hex digest of ``content``."""
    value = hashlib.sha384(content, usedforsecurity=False)
    if salt is not None:
        value.update(salt.encode("utf-8"))
    return value.hexdigest()


def write_file(
    root: Path,
    path: str,
    content: bytes | Callable[[], bytes],
    *,
    replace: bool,
) -> Path:
    """Write one regular 0644 file at a validated tree path under ``root``.

    Parents are created; a symlinked or non-directory parent, or a directory at
    the target, is a conflict. An existing file or symlink at the target is
    replaced when ``replace`` is set and a conflict otherwise. A callable
    ``content`` is read only once the target is known to be writable.
    """
    parts = path.split("/")
    for depth in range(len(parts)):
        parent = root.joinpath(*parts[:depth])
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            raise MaterializationConflictError(
                {path}, "local parent is not a directory"
            )
        parent.mkdir(parents=True, exist_ok=True)
    target = root.joinpath(*parts)
    if target.is_symlink() or target.is_file():
        if not replace:
            raise MaterializationConflictError({path}, "local path already exists")
    elif target.exists():
        raise MaterializationConflictError({path}, "local path is not a file")
    # Write beside the target and swap it in, so a failed write leaves the old file in place.
    fd, temporary = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.")
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(content() if callable(content) else content)
        os.chmod(temporary, 0o644)
        os.replace(temporary, target)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise
    return target


def _unsafe(segment: str) -> bool:
    return (
        len(segment.encode()) > _MAX_SEGMENT_BYTES
        or any(ord(c) < 32 or c in _WINDOWS_INVALID_CHARACTERS for c in segment)
        or segment.endswith((" ", "."))
        or _WINDOWS_DEVICE_NAME.fullmatch(segment) is not None
    )
