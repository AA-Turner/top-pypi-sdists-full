# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["EvaluationGroupUpdateParams"]


class EvaluationGroupUpdateParams(TypedDict, total=False):
    description: str
    """Optional description"""

    metadata: Dict[str, object]
    """Optional metadata key-value pairs"""

    name: str
    """Name of the evaluation group"""

    row_identifiers: Dict[str, str]
    """Optional mapping of evaluation_id to column name for cross-dataset joins"""

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""
