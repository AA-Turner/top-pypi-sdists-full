# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

__all__ = ["KnowledgeBaseUpdateParams"]


class KnowledgeBaseUpdateParams(TypedDict, total=False):
    knowledge_base_name: str
    """The name of the knowledge base"""

    metadata: Dict[str, object]
    """Metadata associated with the knowledge base"""
