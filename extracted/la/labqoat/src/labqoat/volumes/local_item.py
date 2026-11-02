"""What a local path is, as one lstat and readlink see it."""

from __future__ import annotations

import os
import stat
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LocalItem:
    """A file, directory or symbolic link with the facts a commit compares; other kinds are not kept."""

    kind: str
    mode: int
    mtime_ns: int
    size: int
    target: str = ""

    @classmethod
    def read(cls, path: Path) -> LocalItem | None:
        """Describe ``path`` without following a link; sockets, pipes, devices and vanished paths are nothing."""
        try:
            status = path.lstat()
        except FileNotFoundError:
            return None
        mode = stat.S_IMODE(status.st_mode)
        if stat.S_ISLNK(status.st_mode):
            return cls("symlink", mode, status.st_mtime_ns, 0, os.readlink(path))
        if stat.S_ISDIR(status.st_mode):
            return cls("directory", mode, status.st_mtime_ns, 0)
        if stat.S_ISREG(status.st_mode):
            return cls("file", mode, status.st_mtime_ns, status.st_size)
        return None

    @property
    def signature(self) -> tuple[int, int]:
        """Size and modification time: a file whose signature is unchanged is not read again."""
        return self.size, self.mtime_ns
