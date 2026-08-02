"""Filesystem helpers shared by the install tools."""

from pathlib import Path


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
