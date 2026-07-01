# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["KnowledgeBaseUpdateResponse"]


class KnowledgeBaseUpdateResponse(BaseModel):
    knowledge_base_name: Optional[str] = None
    """The name of the knowledge base"""

    metadata: Optional[Dict[str, object]] = None
    """Metadata associated with the knowledge base"""
