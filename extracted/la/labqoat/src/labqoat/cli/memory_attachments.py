"""Upload node attachments through the existing content-addressed asset protocol."""

from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING
from labqoat.json_document import JsonValue

if TYPE_CHECKING:
    from labqoat.assets_client import AssetsClient


class MemoryAttachments:
    """Bind available asset identities and portable names to the authored revision."""

    @staticmethod
    def upload(client: AssetsClient, paths: tuple[str, ...]) -> list[JsonValue]:
        """Retain each local file as shared bytes before publishing the revision."""
        names = [Path(path).name for path in paths]
        if len(set(names)) != len(names):
            raise ValueError("Attachment names must be unique.")
        return [MemoryAttachments.one(client, Path(path)) for path in paths]

    @staticmethod
    def one(client: AssetsClient, path: Path) -> JsonValue:
        """Use a digest key so replaying a failed publication reuses the same asset."""
        digest, _size = client.hash_file(path)
        asset = client.upload_file(path, key="memory-asset:" + digest)
        return {"name": path.name, "asset_id": asset.id}
