"""Atomic replacement of owned local project state and generated artifacts."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory


class AtomicProjectFile:
    """Retain the previous complete file if writing or replacement is interrupted."""

    @staticmethod
    def write(target: Path, data: bytes) -> None:
        """Flush one owned sibling before replacing its destination and clean up on every failure."""
        target.parent.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(prefix=".labqoat-write-", dir=target.parent) as directory:
            path = Path(directory) / "content"
            with path.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            path.replace(target)
