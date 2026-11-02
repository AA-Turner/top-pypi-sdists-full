"""Bounded image context selection before immutable source publication."""

import os
from pathlib import Path, PurePosixPath
from typing import ClassVar

from labqoat.compute.context_ignore import ContextIgnore


class ContextFiles:
    """Filter image context inputs and reject links before creating a deterministic archive."""

    _excluded: ClassVar[frozenset[str]] = frozenset(
        {
            ".git",
            ".labqoat",
            ".storage",
            ".venv",
            ".mypy_cache",
            ".ruff_cache",
            ".pytest_cache",
            ".turbo",
            "__pycache__",
            "node_modules",
            "_build",
            "deps",
        }
    )

    @classmethod
    def _entries(cls, root: Path, ignore: ContextIgnore) -> list[Path]:
        """Walk eligible directories without following links or reading excluded local configuration."""
        entries = []
        for parent, directories, files in os.walk(root, followlinks=False):
            directories[:] = [name for name in directories if not cls._private(name)]
            for name in [*directories, *files]:
                path = Path(parent) / name
                if cls._private(name) or not ignore.includes(PurePosixPath(path.relative_to(root))):
                    continue
                if path.is_symlink():
                    raise ValueError(f"Compute context cannot contain links: {path.relative_to(root)}")
                if path.is_file() and name != ".dockerignore":
                    entries.append(path)
        return entries

    @classmethod
    def _private(cls, name: str) -> bool:
        """Keep untracked configuration, credentials and generated caches out of source archives."""
        return name in cls._excluded or name.startswith(".env") or name.endswith((".local", ".pyc"))

    @classmethod
    def private(cls, name: str) -> bool:
        """Apply the same unconditional private-file policy to every captured input."""
        return cls._private(name)

    @classmethod
    def directory(cls, root: Path, patterns: tuple[str, ...] = ()) -> dict[str, Path]:
        """Select an explicit directory with inline ignore rules and no link traversal."""
        if not root.is_dir() or any(path.is_symlink() for path in (root, *root.parents)):
            raise ValueError(f"Image directories must exist and cannot contain links: {root}")
        entries = cls._entries(root, ContextIgnore("\n".join(patterns)))
        return {path.relative_to(root).as_posix(): path for path in entries}
