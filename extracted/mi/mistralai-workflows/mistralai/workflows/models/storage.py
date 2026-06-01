from datetime import datetime

from pydantic import BaseModel, Field


class BlobRef(BaseModel):
    """A reference to a large object stored in blob storage.

    This model represents metadata about objects stored in external blob storage,
    allowing workflows to pass references to large payloads without exceeding
    Temporal's message size limits.
    """

    uri: str = Field(description="The unique URI of the blob in storage.")
    content_type: str = Field(default="application/octet-stream", description="MIME type of the stored object.")
    size_bytes: int = Field(description="Size of the object in bytes.")

    # Optional metadata for better tracking and management
    key: str | None = Field(default=None, description="The storage key/path used to store the blob.")
    created_at: datetime | None = Field(default=None, description="When the blob was created in storage.")
    expires_at: datetime | None = Field(default=None, description="When the blob expires and should be cleaned up.")
