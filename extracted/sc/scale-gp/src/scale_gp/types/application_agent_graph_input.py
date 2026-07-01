# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .value_constraint import ValueConstraint

__all__ = ["ApplicationAgentGraphInput"]


class ApplicationAgentGraphInput(BaseModel):
    name: str

    type: Literal[
        "ShortText",
        "SentenceText",
        "ParagraphText",
        "ArtifactId",
        "ArtifactIds",
        "KnowledgeBaseId",
        "KnowledgeBaseIds",
        "InputImageDir",
        "Message",
        "Messages",
        "integer",
        "number",
        "string",
        "boolean",
        "array",
        "object",
        "unknown",
    ]

    default: Optional[str] = None

    description: Optional[str] = None

    examples: Optional[List[str]] = None

    required: Optional[bool] = None

    title: Optional[str] = None

    value_constraint: Optional[ValueConstraint] = None
