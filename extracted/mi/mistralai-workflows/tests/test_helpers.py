from typing import Any

from mistralai.extra.workflows.encoding.storage.blob_storage import BlobNotFoundError, BlobStorage


class InMemoryBlobStorage(BlobStorage):
    """Simple in-memory blob storage for testing."""

    def __init__(self) -> None:
        self.blobs: dict[str, bytes] = {}

    async def upload_blob(self, key: str, content: bytes) -> str:
        self.blobs[key] = content
        return key

    async def get_blob(self, key: str) -> bytes:
        if key not in self.blobs:
            raise BlobNotFoundError(f"Blob not found: {key}")
        return self.blobs[key]

    async def get_blob_properties(self, key: str) -> dict[str, Any] | None:
        if key not in self.blobs:
            return None
        return {"size": len(self.blobs[key])}

    async def delete_blob(self, key: str) -> None:
        self.blobs.pop(key, None)

    async def blob_exists(self, key: str) -> bool:
        return key in self.blobs
