# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["CreateKnowledgeBaseResponse"]


class CreateKnowledgeBaseResponse(BaseModel):
    knowledge_base_id: str
    """The unique ID of the created knowledge base"""
