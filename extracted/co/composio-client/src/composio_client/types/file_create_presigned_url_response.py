# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.file_create_presigned_url_response."""

from __future__ import annotations

from typing import Literal

from pydantic import ConfigDict, Field
from .._base_model import BaseModel


class Metadata(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    storage_backend: Literal['s3', 'azure_blob_storage']
    "Storage backend used for the file.\n\nIf this is azure, use `x-ms-blob-type` header to set the blob type to\n`BlockBlob` while uploading the file"


class FileCreatePresignedURLResponse(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    id: str
    "ID of the request file. Example: \"req_file_9mZn4qR8sXwT\" "
    key: str
    "Object storage upload location.\n\nExample:\n\"projects/pr_1a2b3c4d5e6f/requests/slack/SLACK_UPLOAD_FILE/document_9mZn4q.docx\""
    metadata: Metadata
    new_presigned_url: str = Field(alias="newPresignedUrl")
    "[DEPRECATED] Use new_presigned_url instead.\n\nPresigned URL for upload. Example:\n\"https://storage.composio.dev/projects/pr_1a2b3c4d5e6f/requests/slack/document_9mZn4q.docx?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600...\""
    type: Literal['new']
    "[DEPRECATED] Indicates this is a new file that needs to be uploaded"


__all__ = [
    "FileCreatePresignedURLResponse",
    "Metadata",
]
