# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict, TypeAliasType

from .._compat import PYDANTIC_V1

__all__ = [
    "NeEvaluationRunConditionParam",
    "Left",
    "LeftConstEvaluationRunCondition",
    "LeftVarEvaluationRunCondition",
    "Right",
    "RightConstEvaluationRunCondition",
    "RightVarEvaluationRunCondition",
]


class LeftConstEvaluationRunCondition(TypedDict, total=False):
    op: Literal["const"]

    value: Union[str, float, bool]


class LeftVarEvaluationRunCondition(TypedDict, total=False):
    path: Required[str]

    op: Literal["var"]


if TYPE_CHECKING or not PYDANTIC_V1:
    Left = TypeAliasType(
        "Left",
        Union[
            LeftConstEvaluationRunCondition,
            LeftVarEvaluationRunCondition,
            "EqEvaluationRunConditionParam",
            "NeEvaluationRunConditionParam",
            "LtEvaluationRunConditionParam",
            "LteEvaluationRunConditionParam",
            "GtEvaluationRunConditionParam",
            "GteEvaluationRunConditionParam",
            "AndEvaluationRunConditionParam",
            "OrEvaluationRunConditionParam",
            "InEvaluationRunConditionParam",
            "NotInEvaluationRunConditionParam",
            "NotEvaluationRunConditionParam",
            "IsNullEvaluationRunConditionParam",
            "IsNotNullEvaluationRunConditionParam",
        ],
    )
else:
    Left: TypeAlias = Union[
        LeftConstEvaluationRunCondition,
        LeftVarEvaluationRunCondition,
        "EqEvaluationRunConditionParam",
        "NeEvaluationRunConditionParam",
        "LtEvaluationRunConditionParam",
        "LteEvaluationRunConditionParam",
        "GtEvaluationRunConditionParam",
        "GteEvaluationRunConditionParam",
        "AndEvaluationRunConditionParam",
        "OrEvaluationRunConditionParam",
        "InEvaluationRunConditionParam",
        "NotInEvaluationRunConditionParam",
        "NotEvaluationRunConditionParam",
        "IsNullEvaluationRunConditionParam",
        "IsNotNullEvaluationRunConditionParam",
    ]


class RightConstEvaluationRunCondition(TypedDict, total=False):
    op: Literal["const"]

    value: Union[str, float, bool]


class RightVarEvaluationRunCondition(TypedDict, total=False):
    path: Required[str]

    op: Literal["var"]


if TYPE_CHECKING or not PYDANTIC_V1:
    Right = TypeAliasType(
        "Right",
        Union[
            RightConstEvaluationRunCondition,
            RightVarEvaluationRunCondition,
            "EqEvaluationRunConditionParam",
            "NeEvaluationRunConditionParam",
            "LtEvaluationRunConditionParam",
            "LteEvaluationRunConditionParam",
            "GtEvaluationRunConditionParam",
            "GteEvaluationRunConditionParam",
            "AndEvaluationRunConditionParam",
            "OrEvaluationRunConditionParam",
            "InEvaluationRunConditionParam",
            "NotInEvaluationRunConditionParam",
            "NotEvaluationRunConditionParam",
            "IsNullEvaluationRunConditionParam",
            "IsNotNullEvaluationRunConditionParam",
        ],
    )
else:
    Right: TypeAlias = Union[
        RightConstEvaluationRunCondition,
        RightVarEvaluationRunCondition,
        "EqEvaluationRunConditionParam",
        "NeEvaluationRunConditionParam",
        "LtEvaluationRunConditionParam",
        "LteEvaluationRunConditionParam",
        "GtEvaluationRunConditionParam",
        "GteEvaluationRunConditionParam",
        "AndEvaluationRunConditionParam",
        "OrEvaluationRunConditionParam",
        "InEvaluationRunConditionParam",
        "NotInEvaluationRunConditionParam",
        "NotEvaluationRunConditionParam",
        "IsNullEvaluationRunConditionParam",
        "IsNotNullEvaluationRunConditionParam",
    ]


class NeEvaluationRunConditionParam(TypedDict, total=False):
    left: Required[Left]

    right: Required[Right]

    op: Literal["ne"]


from .eq_evaluation_run_condition_param import EqEvaluationRunConditionParam
from .gt_evaluation_run_condition_param import GtEvaluationRunConditionParam
from .in_evaluation_run_condition_param import InEvaluationRunConditionParam
from .lt_evaluation_run_condition_param import LtEvaluationRunConditionParam
from .or_evaluation_run_condition_param import OrEvaluationRunConditionParam
from .and_evaluation_run_condition_param import AndEvaluationRunConditionParam
from .gte_evaluation_run_condition_param import GteEvaluationRunConditionParam
from .lte_evaluation_run_condition_param import LteEvaluationRunConditionParam
from .not_evaluation_run_condition_param import NotEvaluationRunConditionParam
from .not_in_evaluation_run_condition_param import NotInEvaluationRunConditionParam
from .is_null_evaluation_run_condition_param import IsNullEvaluationRunConditionParam
from .is_not_null_evaluation_run_condition_param import IsNotNullEvaluationRunConditionParam
