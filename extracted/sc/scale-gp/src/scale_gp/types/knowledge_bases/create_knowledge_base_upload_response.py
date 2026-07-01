# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["CreateKnowledgeBaseUploadResponse"]


class CreateKnowledgeBaseUploadResponse(BaseModel):
    upload_id: str
    """ID of the created knowledge base upload job."""
