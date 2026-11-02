"""Metadata-bound receipts for immutable, previously verified cache files."""

import json
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from labqoat.references import AssetRef
from labqoat.storage.verified_file import VerifiedFile


@dataclass(frozen=True, slots=True)
class CacheReceipt:
    """Avoid rehashing unchanged owned bytes while detecting replacement or mutation.

    A receipt is only as trustworthy as everything that can write beside it. Where other runs share the
    directory, pass ``trusted=False``: the bytes are hashed on every use and no receipt is read or written.
    """

    path: Path
    trusted: bool = True

    @property
    def receipt(self) -> Path:
        """Return the sidecar outside the dataset's logical namespace."""
        return self.path.with_suffix(".verified.json")

    def validate(self, reference: AssetRef) -> Path:
        """Rehash changed metadata and fail closed on altered asset contents."""
        if self.path.is_symlink() or not self.path.is_file():
            raise ValueError("Cached assets must be regular files")
        if not self.trusted:
            return VerifiedFile.validate(self.path, str(reference.blob_sha256), reference.byte_size)
        fingerprint = self._fingerprint(reference)
        if self._read() != fingerprint:
            VerifiedFile.validate(self.path, str(reference.blob_sha256), reference.byte_size)
            self.path.chmod(0o444)
            self.record(reference)
        self.receipt.touch()
        return self.path

    def record(self, reference: AssetRef) -> None:
        """Record metadata immediately after the caller publishes verified bytes."""
        self._write(self._fingerprint(reference))

    def _fingerprint(self, reference: AssetRef) -> list[str | int]:
        """Bind verification to identity, inode, size, and nanosecond change times."""
        stat = self.path.stat()
        return [
            str(reference.blob_sha256),
            reference.byte_size,
            stat.st_dev,
            stat.st_ino,
            stat.st_size,
            stat.st_mtime_ns,
            stat.st_ctime_ns,
        ]

    def _read(self) -> object:
        """Treat absent or invalid receipts as a request to verify the actual bytes."""
        if self.receipt.is_symlink():
            raise ValueError("Cache receipts cannot be symlinks")
        try:
            return json.loads(self.receipt.read_text(encoding="utf-8"))
        except (FileNotFoundError, ValueError):
            return None

    def _write(self, fingerprint: list[str | int]) -> None:
        """Publish receipts atomically even when several readers verify together."""
        pending = self.receipt.with_suffix(f".{uuid4()}.tmp")
        try:
            pending.write_text(json.dumps(fingerprint), encoding="utf-8")
            pending.replace(self.receipt)
        finally:
            pending.unlink(missing_ok=True)
