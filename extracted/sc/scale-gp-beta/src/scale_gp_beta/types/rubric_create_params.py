# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr
from .rubrics.rubric_criteria_input_param import RubricCriteriaInputParam

__all__ = ["RubricCreateParams"]


class RubricCreateParams(TypedDict, total=False):
    title: Required[str]
    """The rubric title"""

    criteria: Iterable[RubricCriteriaInputParam]
    """Initial criteria to create with the rubric"""

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""
