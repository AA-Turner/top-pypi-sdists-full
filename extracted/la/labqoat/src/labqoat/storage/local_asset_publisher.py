"""Verified content-addressed storage for local workflow assets."""

import shutil
from collections.abc import Mapping
from contextlib import AbstractContextManager, nullcontext
from dataclasses import dataclass
from pathlib import Path
from uuid import NAMESPACE_URL, uuid4, uuid5

from labqoat.argument_codec import decode_result
from labqoat.references import AssetRef, ResourceId, Sha256
from labqoat.storage.verified_file import VerifiedFile


@dataclass(frozen=True, slots=True)
class LocalAssetPublisher:
    """Publish immutable files into an explicitly selected local directory."""

    root: Path

    def publish(
        self, source: str | Path, *, media_type: str, name: str | None = None, step: int | None = None
    ) -> AssetRef:
        """Copy verified bytes and preserve the same identity on replay."""
        source_path = Path(source)
        VerifiedFile.relative(source_path.name if name is None else name)
        if step is not None and step < 0:
            raise ValueError("Asset step cannot be negative")
        digest = VerifiedFile.digest(source_path)
        reference = AssetRef(
            id=ResourceId(uuid5(NAMESPACE_URL, f"labqoat-asset:{digest}")),
            blob_sha256=Sha256(digest),
            byte_size=source_path.stat().st_size,
            media_type=media_type,
        )
        target = self.path_for_digest(digest)
        self._copy(source_path, target, reference)
        return reference

    def require_publishable(self, source: str | Path, name: str | None = None) -> int:
        """Local storage has no size limit; report the size like every publisher."""
        del name
        return Path(source).stat().st_size

    def path_for_digest(self, digest: str) -> Path:
        """Return the content address after validating the digest."""
        Sha256.parse(digest)
        return self.root / "sha256" / digest[:2] / digest[2:4] / digest

    def path(self, reference: AssetRef) -> Path:
        """Return locally retained bytes only after verifying their identity."""
        target = self.path_for_digest(str(reference.blob_sha256))
        return VerifiedFile.validate(target, str(reference.blob_sha256), reference.byte_size)

    def local_file(self, reference: AssetRef | Mapping[str, object]) -> AbstractContextManager[Path]:
        """Expose retained local output bytes through the shared consumer interface."""
        asset = reference if isinstance(reference, AssetRef) else decode_result(reference, AssetRef)
        return nullcontext(self.path(asset))

    @staticmethod
    def _copy(source: Path, target: Path, reference: AssetRef) -> None:
        """Publish through a verified temporary file and reject corrupt caches."""
        digest = str(reference.blob_sha256)
        if target.exists():
            VerifiedFile.validate(target, digest, reference.byte_size)
            return
        target.parent.mkdir(parents=True, exist_ok=True)
        pending = target.with_suffix(f".{uuid4()}.tmp")
        try:
            shutil.copyfile(source, pending)
            VerifiedFile.validate(pending, digest, reference.byte_size)
            pending.replace(target)
        finally:
            pending.unlink(missing_ok=True)
