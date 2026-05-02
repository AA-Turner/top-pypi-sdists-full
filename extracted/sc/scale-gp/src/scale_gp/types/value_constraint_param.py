# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["ValueConstraintParam"]


class ValueConstraintParam(TypedDict, total=False):
    potential_values: Required[SequenceNotStr[str]]

    selection_constraint_type: Required[Literal["single", "multi"]]

    value_type: Required[
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

    max_items: int

    min_items: int
