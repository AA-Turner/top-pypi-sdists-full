# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

from ..._types import SequenceNotStr

__all__ = ["GenerationJobCreateParams"]


class GenerationJobCreateParams(TypedDict, total=False):
    advanced_config: Dict[str, SequenceNotStr[str]]
    """Advanced configuration for the evaluation dataset generation job."""

    custom_instructions: str
    """Custom instructions for test case generation"""

    group_by_artifact_id: bool
    """
    If this flag is true, for every generated test case, the chunks used to generate
    it will be guaranteed to be from the same document (artifact).
    """

    harms_list: SequenceNotStr[str]
    """List of harms to be used for the evaluation dataset generation.

    If not provided, generation will use the knowledge base id.
    """

    num_test_cases: int
    """Number of test cases to generate for the evaluation dataset"""
