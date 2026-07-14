# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["LtEvaluationRunConditionParam"]


class LtEvaluationRunConditionParam(TypedDict, total=False):
    left: Required[object]

    right: Required[object]

    op: Literal["lt"]
