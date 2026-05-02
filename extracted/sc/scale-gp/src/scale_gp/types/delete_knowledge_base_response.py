# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DeleteKnowledgeBaseResponse"]


class DeleteKnowledgeBaseResponse(BaseModel):
    deleted: bool
    """Whether or not the knowledge base was successfully deleted"""

    knowledge_base_id: str
    """The ID of the knowledge base that was deleted"""
