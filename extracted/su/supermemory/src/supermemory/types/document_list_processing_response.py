# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DocumentListProcessingResponse", "Document", "Pagination"]


class Document(BaseModel):
    id: str
    """Unique identifier of the document."""

    connection_id: Optional[str] = FieldInfo(alias="connectionId", default=None)
    """Optional ID of connection the document was created from.

    This is useful for identifying the source of the document.
    """

    created_at: str = FieldInfo(alias="createdAt")
    """Creation timestamp"""

    custom_id: Optional[str] = FieldInfo(alias="customId", default=None)
    """Optional custom ID of the document.

    This could be an ID from your database that will uniquely identify this
    document.
    """

    metadata: Union[str, float, bool, Dict[str, object], List[object], None] = None
    """Optional metadata for the document.

    This is used to store additional information about the document. You can use
    this to store any additional information you need about the document. Metadata
    can be filtered through. Keys must be strings and are case sensitive. Values can
    be strings, numbers, or booleans. You cannot nest objects.
    """

    status: Literal["unknown", "queued", "extracting", "chunking", "embedding", "indexing", "done", "failed"]
    """Status of the document"""

    summary: Optional[str] = None
    """Summary of the document content"""

    title: Optional[str] = None
    """Title of the document"""

    type: Literal[
        "text",
        "pdf",
        "tweet",
        "google_doc",
        "google_slide",
        "google_sheet",
        "image",
        "video",
        "audio",
        "notion_doc",
        "webpage",
        "onedrive",
        "github_markdown",
        "granola",
    ]
    """Type of the document"""

    updated_at: str = FieldInfo(alias="updatedAt")
    """Last update timestamp"""

    container_tags: Optional[List[str]] = FieldInfo(alias="containerTags", default=None)
    """Optional tags this document should be containerized by.

    This can be an ID for your user, a project ID, or any other identifier you wish
    to use to group documents.
    """

    error_code: Optional[str] = FieldInfo(alias="errorCode", default=None)
    """Stable error code when processing failed, if available"""

    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    """Human-readable processing error, if available"""

    stuck: Optional[bool] = None
    """True when the document is not done/failed and has not been updated for 4 hours"""


class Pagination(BaseModel):
    """Present when `view=all`"""

    current_page: float = FieldInfo(alias="currentPage")

    total_items: float = FieldInfo(alias="totalItems")

    total_pages: float = FieldInfo(alias="totalPages")

    limit: Optional[float] = None


class DocumentListProcessingResponse(BaseModel):
    """List of documents currently being processed"""

    documents: List[Document]

    total_count: float = FieldInfo(alias="totalCount")
    """Total number of processing documents"""

    pagination: Optional[Pagination] = None
    """Present when `view=all`"""
