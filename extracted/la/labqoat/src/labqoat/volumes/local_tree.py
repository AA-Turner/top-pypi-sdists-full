"""Every path under a mount, named the way a volume names it."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from labqoat.volumes.local_item import LocalItem


class LocalTree:
    """Walk a directory without following links, keeping files, directories and symbolic links."""

    @staticmethod
    def scan(root: Path) -> dict[str, LocalItem]:
        """Map each relative POSIX path below ``root`` to what it is; unnameable paths are reported and skipped."""
        found: dict[str, LocalItem] = {}
        pending = [root]
        while pending:
            directory = pending.pop()
            with os.scandir(directory) as listing:
                for child in listing:
                    LocalTree._visit(root, Path(child.path), found, pending)
        return found

    @staticmethod
    def _visit(root: Path, path: Path, found: dict[str, LocalItem], pending: list[Path]) -> None:
        """Record one path and descend into real directories only."""
        relative = path.relative_to(root).as_posix()
        if not LocalTree.nameable(relative):
            print(f"Volume skips {relative!r}: its name is not UTF-8 text.", file=sys.stderr, flush=True)
            return
        item = LocalItem.read(path)
        if item is None:
            return
        found[relative] = item
        if item.kind == "directory":
            pending.append(path)

    @staticmethod
    def nameable(relative: str) -> bool:
        """Whether a path can be named in a volume: it must encode as UTF-8."""
        try:
            relative.encode("utf-8")
        except UnicodeEncodeError:
            return False
        return True
