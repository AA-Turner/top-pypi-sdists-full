# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .restore_request_param import RestoreRequestParam

__all__ = ["EvaluationUpdateParams", "Evaluation", "EvaluationPartialEvaluationUpdateRequest"]


class EvaluationUpdateParams(TypedDict, total=False):
    evaluation: Required[Evaluation]


class EvaluationPartialEvaluationUpdateRequest(TypedDict, total=False):
    description: str

    name: str

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""


Evaluation: TypeAlias = Union[EvaluationPartialEvaluationUpdateRequest, RestoreRequestParam]
