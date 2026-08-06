"""Filesystem helpers shared by the install tools."""

import os
from pathlib import Path


def atomic_write_private_text(path: Path, content: str, *, encoding: str = "utf-8") -> None:
    """Write ``content`` to ``path`` atomically, readable by its owner only.

    Same atomic rename as :func:`atomic_write_text`, but the temporary file is
    created with ``0600`` from the start — so a file holding a secret is never
    world-readable, not even during the write. On Windows the mode is ignored
    and the default ACL applies (same model as ``~/.aws/credentials``).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding=encoding) as handle:
        handle.write(content)
    tmp.replace(path)


def atomic_write_text(path: Path, content: str, *, encoding: str = "utf-8", errors: str = "strict") -> None:
    """Write ``content`` to ``path`` atomically.

    Writes a sibling ``*.tmp`` file then renames it over the target, so a
    concurrent reader (e.g. Claude Code reading ``settings.json`` while a
    background refresh rewrites it) never observes a half-written file. Parent
    directories are created as needed.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding=encoding, errors=errors)
    tmp.replace(path)
