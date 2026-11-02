"""Immutable asset reads and publication through explicitly injected invocation capabilities."""

import mimetypes
from collections.abc import Mapping
from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from pathlib import Path

from labqoat.references import AssetRef
from labqoat.storage.asset_publisher import AssetPublisher
from labqoat.storage.file_access import FileAccess
from labqoat.storage.unavailable_asset_publisher import UnavailableAssetPublisher
from labqoat.storage.unavailable_file_access import UnavailableFileAccess


@dataclass(frozen=True)
class RunAssets:
    """Combine verified leased reads with durable publication without introducing a second storage path."""

    files: FileAccess = field(default_factory=UnavailableFileAccess)
    publisher: AssetPublisher = field(default_factory=UnavailableAssetPublisher)

    def local_file(self, reference: AssetRef | Mapping[str, object]) -> AbstractContextManager[Path]:
        """Lease authorized immutable bytes for the caller's consumption scope."""
        return self.files.local_file(reference)

    def publish(
        self, source: str | Path, *, media_type: str | None = None, name: str | None = None, step: int | None = None
    ) -> AssetRef:
        """Retain verified bytes under the current Run; an omitted media type follows the file name."""
        guessed = mimetypes.guess_type(name or str(source))[0] or "application/octet-stream"
        return self.publisher.publish(source, media_type=media_type or guessed, name=name, step=step)

    def require_publishable(self, source: str | Path) -> int:
        """Reject a file the publisher cannot retain before spending work on it, and return its size."""
        return self.publisher.require_publishable(source)
