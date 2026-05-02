# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["CreateKnowledgeBaseUploadsFromFilesResponse"]


class CreateKnowledgeBaseUploadsFromFilesResponse(BaseModel):
    upload_ids: List[str]
    """List of upload IDs that have been kicked off by the upload API"""
