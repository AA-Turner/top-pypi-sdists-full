# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["NotInEvaluationRunConditionParam"]


class NotInEvaluationRunConditionParam(TypedDict, total=False):
    left: Required[object]

    operands: Required[Iterable[object]]

    op: Literal["not_in"]
