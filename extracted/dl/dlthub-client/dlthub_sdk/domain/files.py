"""One entry in an uploaded deployment's or configuration's files manifest."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

# Current package
from dlthub_sdk._glue.context import _Ctx

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.dataplane_api.models import ManifestFilesResponse


@dataclass(frozen=True)
class FileEntry:
    """One file the platform holds for a deployment or a configuration."""

    relative_path: str
    """Path of the file inside the package, with `/` separators: relative to the
    workspace root for a deployment, and to the `.dlt` settings folder for a
    configuration.
    """
    size_bytes: int
    """Size of the file in bytes; 0 for a symlink."""
    sha3_256: str
    """Base64 SHA3-256 of the file contents, or of the `linkname` string for a symlink.
    """
    linkname: str | None
    """Symlink target; set for symlink entries only."""

    @staticmethod
    def _all_from_payload(
        _ctx: _Ctx[Any], payload: ManifestFilesResponse
    ) -> tuple[FileEntry, ...]:
        return tuple(
            FileEntry(
                relative_path=item.relative_path,
                size_bytes=item.size_bytes,
                sha3_256=item.sha3_256,
                linkname=item.linkname if isinstance(item.linkname, str) else None,
            )
            for item in payload.files
        )
