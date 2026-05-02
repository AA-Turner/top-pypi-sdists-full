# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["EvaluationGroupCreateParams"]


class EvaluationGroupCreateParams(TypedDict, total=False):
    evaluation_ids: Required[SequenceNotStr[str]]
    """List of evaluation IDs to include in the group"""

    name: Required[str]
    """Name of the evaluation group"""

    description: str
    """Optional description"""

    metadata: Dict[str, object]
    """Optional metadata key-value pairs"""

    row_identifiers: Dict[str, str]
    """Optional mapping of evaluation_id to column name for cross-dataset joins"""

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""
