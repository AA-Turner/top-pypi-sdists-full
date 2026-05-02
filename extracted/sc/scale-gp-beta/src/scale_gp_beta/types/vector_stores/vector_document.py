# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ..._models import BaseModel
from ..text_content import TextContent

__all__ = ["VectorDocument"]


class VectorDocument(BaseModel):
    """A document returned from direct lookups (get/list operations)."""

    id: str
    """Document ID"""

    content: Optional[TextContent] = None
    """Text content for documents."""

    metadata: Optional[Dict[str, object]] = None
    """Key-value metadata"""

    vector: Optional[List[float]] = None
    """Embedding vector (if requested)"""
