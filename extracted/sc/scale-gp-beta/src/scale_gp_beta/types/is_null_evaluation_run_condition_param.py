# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["IsNullEvaluationRunConditionParam"]


class IsNullEvaluationRunConditionParam(TypedDict, total=False):
    operands: Required[Iterable[object]]

    op: Literal["is_null"]
