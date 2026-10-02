# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["BatchCreateResponse", "Result", "ResultUnionMember0", "ResultUnionMember1"]


class ResultUnionMember0(BaseModel):
    index: int

    success: Literal[True]


class ResultUnionMember1(BaseModel):
    code: Literal["invalid_event", "queue_failed"]

    index: int

    message: str

    success: Literal[False]


Result: TypeAlias = Union[ResultUnionMember0, ResultUnionMember1]


class BatchCreateResponse(BaseModel):
    accepted: int

    failed: int

    results: List[Result]

    success: bool
