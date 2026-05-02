# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr
from .value_constraint_param import ValueConstraintParam

__all__ = ["ApplicationAgentGraphInputParam"]


class ApplicationAgentGraphInputParam(TypedDict, total=False):
    name: Required[str]

    type: Required[
        Literal[
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
    ]

    default: str

    description: str

    examples: SequenceNotStr[str]

    required: bool

    title: str

    value_constraint: ValueConstraintParam
