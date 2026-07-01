# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict, TypeAliasType

from .._compat import PYDANTIC_V1

__all__ = [
    "NotInEvaluationRunConditionParam",
    "Left",
    "LeftConstEvaluationRunCondition",
    "LeftVarEvaluationRunCondition",
    "Operand",
    "OperandConstEvaluationRunCondition",
    "OperandVarEvaluationRunCondition",
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


class OperandConstEvaluationRunCondition(TypedDict, total=False):
    op: Literal["const"]

    value: Union[str, float, bool]


class OperandVarEvaluationRunCondition(TypedDict, total=False):
    path: Required[str]

    op: Literal["var"]


if TYPE_CHECKING or not PYDANTIC_V1:
    Operand = TypeAliasType(
        "Operand",
        Union[
            OperandConstEvaluationRunCondition,
            OperandVarEvaluationRunCondition,
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
    Operand: TypeAlias = Union[
        OperandConstEvaluationRunCondition,
        OperandVarEvaluationRunCondition,
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


class NotInEvaluationRunConditionParam(TypedDict, total=False):
    left: Required[Left]

    operands: Required[Iterable[Operand]]

    op: Literal["not_in"]


from .eq_evaluation_run_condition_param import EqEvaluationRunConditionParam
from .gt_evaluation_run_condition_param import GtEvaluationRunConditionParam
from .in_evaluation_run_condition_param import InEvaluationRunConditionParam
from .lt_evaluation_run_condition_param import LtEvaluationRunConditionParam
from .ne_evaluation_run_condition_param import NeEvaluationRunConditionParam
from .or_evaluation_run_condition_param import OrEvaluationRunConditionParam
from .and_evaluation_run_condition_param import AndEvaluationRunConditionParam
from .gte_evaluation_run_condition_param import GteEvaluationRunConditionParam
from .lte_evaluation_run_condition_param import LteEvaluationRunConditionParam
from .not_evaluation_run_condition_param import NotEvaluationRunConditionParam
from .is_null_evaluation_run_condition_param import IsNullEvaluationRunConditionParam
from .is_not_null_evaluation_run_condition_param import IsNotNullEvaluationRunConditionParam
