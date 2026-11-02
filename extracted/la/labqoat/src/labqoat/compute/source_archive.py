"""Deterministic captured bytes for a declared image context."""

import gzip
import hashlib
import tarfile
from pathlib import Path


class SourceArchive:
    """Write selected regular files with reproducible metadata and no live Python objects."""

    @classmethod
    def write(cls, root: Path, entries: tuple[Path, ...], destination: Path) -> None:
        """Normalize archive order, gzip timestamp, permissions and ownership."""
        with (
            destination.open("wb") as output,
            gzip.GzipFile(filename="", mode="wb", fileobj=output, mtime=0) as compressed,
            tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive,
        ):
            for path in entries:
                cls._add(archive, path, path.relative_to(root).as_posix())

    @staticmethod
    def digest(root: Path, entries: tuple[Path, ...]) -> str:
        """Name the archive ``write`` would make from these files without compressing it: names, modes, contents."""
        digest = hashlib.sha256(b"labqoat-source-archive-1\n")
        for path in entries:
            executable = b"755" if path.stat().st_mode & 0o111 else b"644"
            digest.update(path.relative_to(root).as_posix().encode() + b"\0" + executable + b"\0")
            digest.update(hashlib.sha256(path.read_bytes()).digest())
        return "tree:" + digest.hexdigest()

    @staticmethod
    def _add(archive: tarfile.TarFile, path: Path, name: str) -> None:
        """Snapshot each file once and retain its executable bit independently of machine ownership."""
        with path.open("rb") as source:
            info = tarfile.TarInfo(name)
            info.size = path.stat().st_size
            info.mode = 0o755 if path.stat().st_mode & 0o111 else 0o644
            archive.addfile(info, source)
