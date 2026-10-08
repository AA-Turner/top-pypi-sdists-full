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
    """One file the platform holds for a deployment or a configuration.

    Attributes:
        relative_path: Where the file sits, relative to the workspace root.
        size_bytes: Its size in bytes.
        sha3_256: SHA3-256 of the file's content.
        linkname: What it points at, when the entry is a symlink.
    """

    relative_path: str
    size_bytes: int
    sha3_256: str
    linkname: str | None

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
