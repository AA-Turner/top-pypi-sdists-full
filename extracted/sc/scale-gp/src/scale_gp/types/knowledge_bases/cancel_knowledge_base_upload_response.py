# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["CancelKnowledgeBaseUploadResponse"]


class CancelKnowledgeBaseUploadResponse(BaseModel):
    canceled: bool
    """Whether cancellation was successful."""

    upload_id: str
    """ID of the knowledge base upload job that was cancelled."""
