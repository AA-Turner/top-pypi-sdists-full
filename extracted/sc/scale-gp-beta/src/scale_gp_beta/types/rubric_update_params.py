# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .restore_request_param import RestoreRequestParam

__all__ = ["RubricUpdateParams", "Rubric", "RubricPartialRubricRequestBase"]


class RubricUpdateParams(TypedDict, total=False):
    rubric: Required[Rubric]


class RubricPartialRubricRequestBase(TypedDict, total=False):
    tags: SequenceNotStr[str]
    """The tags associated with the entity"""

    title: str
    """The rubric title"""


Rubric: TypeAlias = Union[RubricPartialRubricRequestBase, RestoreRequestParam]
