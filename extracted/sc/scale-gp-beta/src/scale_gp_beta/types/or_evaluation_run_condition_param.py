# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict, TypeAliasType

from .._compat import PYDANTIC_V1

__all__ = [
    "OrEvaluationRunConditionParam",
    "Operand",
    "OperandConstEvaluationRunCondition",
    "OperandVarEvaluationRunCondition",
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


class OrEvaluationRunConditionParam(TypedDict, total=False):
    operands: Required[Iterable[Operand]]

    op: Literal["or"]


from .eq_evaluation_run_condition_param import EqEvaluationRunConditionParam
from .gt_evaluation_run_condition_param import GtEvaluationRunConditionParam
from .in_evaluation_run_condition_param import InEvaluationRunConditionParam
from .lt_evaluation_run_condition_param import LtEvaluationRunConditionParam
from .ne_evaluation_run_condition_param import NeEvaluationRunConditionParam
from .and_evaluation_run_condition_param import AndEvaluationRunConditionParam
from .gte_evaluation_run_condition_param import GteEvaluationRunConditionParam
from .lte_evaluation_run_condition_param import LteEvaluationRunConditionParam
from .not_evaluation_run_condition_param import NotEvaluationRunConditionParam
from .not_in_evaluation_run_condition_param import NotInEvaluationRunConditionParam
from .is_null_evaluation_run_condition_param import IsNullEvaluationRunConditionParam
from .is_not_null_evaluation_run_condition_param import IsNotNullEvaluationRunConditionParam
