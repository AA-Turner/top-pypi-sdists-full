"""Verified asset leases on invocation scratch when shared storage cannot fit the payload."""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from labqoat.references import AssetRef
from labqoat.storage.asset_source import AssetSource
from labqoat.storage.verified_file import VerifiedFile


@dataclass(frozen=True, slots=True)
class TemporaryAssetFile:
    """Own one read-only verified payload and remove it when its consumer releases the lease."""

    root: Path

    @contextmanager
    def local_file(self, reference: AssetRef, source: AssetSource) -> Iterator[Path]:
        """Stream into private scratch, verify exact identity, and clean up every exit path."""
        self.root.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(prefix="asset-", dir=self.root) as directory:
            path = Path(directory) / "payload"
            source.download_to(reference, path)
            VerifiedFile.validate(path, str(reference.blob_sha256), reference.byte_size)
            path.chmod(0o444)
            yield path
