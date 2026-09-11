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
    from dlthub_sdk._gen.dataplane_api.models import TFilesManifest


@dataclass(frozen=True)
class FileEntry:
    """One file the platform holds for a deployment or a configuration.

    Attributes:
        path: Where the file sits, relative to the workspace root.
        size: Its size in bytes.
        content_hash: SHA3-256 of the file's content.
        link_to: What it points at, when the entry is a symlink.
    """

    path: str
    size: int
    content_hash: str
    link_to: str | None

    @staticmethod
    def _all_from_payload(
        _ctx: _Ctx[Any], payload: TFilesManifest
    ) -> tuple[FileEntry, ...]:
        return tuple(
            FileEntry(
                path=item.relative_path,
                size=item.size_in_bytes,
                content_hash=item.sha3_256,
                link_to=item.linkname if isinstance(item.linkname, str) else None,
            )
            for item in payload.files
        )
