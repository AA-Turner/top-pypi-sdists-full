"""Publish immutable logical symlink views over already acquired cache files."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from labqoat.references import ResourceId, Sha256
from labqoat.storage.cache_lock import CacheLock
from labqoat.storage.verified_file import VerifiedFile


@dataclass(frozen=True, slots=True)
class DatasetView:
    """Own atomic, reusable views without copying or downloading asset contents."""

    root: Path
    cache_root: Path

    def publish(self, revision: ResourceId, digest: Sha256, files: Mapping[str, Path]) -> Path:
        """Publish once and validate an existing winner before reusing its links."""
        destination = self.root / "views" / str(revision)
        self._validate_destination(destination)
        lock = CacheLock(self.root / "view-locks" / str(revision))
        try:
            lock.acquire()
            if not destination.exists():
                self._build(destination, digest, files)
            self._validate(destination, digest, files)
            return destination
        finally:
            lock.close()

    def _validate_destination(self, destination: Path) -> None:
        """Reject redirected view directories before touching their contents."""
        if destination.is_symlink() or destination.parent.is_symlink():
            raise ValueError("Dataset view directory cannot be a symlink")
        if not destination.resolve().is_relative_to(self.root.resolve()):
            raise ValueError("Dataset view directory escapes its owned root")
        destination.parent.mkdir(parents=True, exist_ok=True)

    def _build(self, destination: Path, digest: Sha256, files: Mapping[str, Path]) -> None:
        """Build privately and publish through one same-filesystem directory rename."""
        with TemporaryDirectory(prefix=f".{destination.name}-", dir=destination.parent) as temporary:
            directory = Path(temporary)
            for logical, source in files.items():
                self._link(directory, logical, source)
            for path in directory.rglob("*"):
                if path.is_dir():
                    path.chmod(0o555)
            marker = destination.with_suffix(".manifest")
            if marker.is_symlink():
                raise ValueError("Dataset view marker cannot be a symlink")
            directory.replace(destination)
            destination.chmod(0o555)
            marker.write_text(str(digest), encoding="utf-8")

    def _link(self, directory: Path, logical: str, source: Path) -> None:
        """Preserve names while limiting every link to an exact verified cache target."""
        if source.is_symlink() or not source.resolve().is_relative_to(self.cache_root.resolve()):
            raise ValueError("Dataset view source escapes its cache")
        target = directory / VerifiedFile.relative(logical)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source.resolve())

    @staticmethod
    def _validate(destination: Path, digest: Sha256, files: Mapping[str, Path]) -> None:
        """A marker never substitutes for checking exact membership and link targets."""
        marker = destination.with_suffix(".manifest")
        if marker.is_symlink() or not marker.is_file() or marker.read_text(encoding="utf-8") != str(digest):
            raise ValueError("Dataset view is not a matching managed view")
        entries = {
            path.relative_to(destination).as_posix(): path
            for path in destination.rglob("*")
            if path.is_symlink() or not path.is_dir()
        }
        if entries.keys() != files.keys():
            raise ValueError("Dataset view membership does not match its manifest")
        for logical, target in entries.items():
            if not target.is_symlink() or target.resolve() != files[logical].resolve():
                raise ValueError("Dataset view link does not match its pinned asset")
