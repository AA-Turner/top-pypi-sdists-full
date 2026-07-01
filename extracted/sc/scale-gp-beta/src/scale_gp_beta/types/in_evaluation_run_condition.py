# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias, TypeAliasType

from .._utils import PropertyInfo
from .._compat import PYDANTIC_V1
from .._models import BaseModel

__all__ = [
    "InEvaluationRunCondition",
    "Left",
    "LeftConstEvaluationRunCondition",
    "LeftVarEvaluationRunCondition",
    "Operand",
    "OperandConstEvaluationRunCondition",
    "OperandVarEvaluationRunCondition",
]


class LeftConstEvaluationRunCondition(BaseModel):
    op: Optional[Literal["const"]] = None

    value: Union[str, float, bool, None] = None


class LeftVarEvaluationRunCondition(BaseModel):
    path: str

    op: Optional[Literal["var"]] = None


if TYPE_CHECKING or not PYDANTIC_V1:
    Left = TypeAliasType(
        "Left",
        Annotated[
            Union[
                LeftConstEvaluationRunCondition,
                LeftVarEvaluationRunCondition,
                "EqEvaluationRunCondition",
                "NeEvaluationRunCondition",
                "LtEvaluationRunCondition",
                "LteEvaluationRunCondition",
                "GtEvaluationRunCondition",
                "GteEvaluationRunCondition",
                "AndEvaluationRunCondition",
                "OrEvaluationRunCondition",
                "InEvaluationRunCondition",
                "NotInEvaluationRunCondition",
                "NotEvaluationRunCondition",
                "IsNullEvaluationRunCondition",
                "IsNotNullEvaluationRunCondition",
            ],
            PropertyInfo(discriminator="op"),
        ],
    )
else:
    Left: TypeAlias = Annotated[
        Union[
            LeftConstEvaluationRunCondition,
            LeftVarEvaluationRunCondition,
            "EqEvaluationRunCondition",
            "NeEvaluationRunCondition",
            "LtEvaluationRunCondition",
            "LteEvaluationRunCondition",
            "GtEvaluationRunCondition",
            "GteEvaluationRunCondition",
            "AndEvaluationRunCondition",
            "OrEvaluationRunCondition",
            "InEvaluationRunCondition",
            "NotInEvaluationRunCondition",
            "NotEvaluationRunCondition",
            "IsNullEvaluationRunCondition",
            "IsNotNullEvaluationRunCondition",
        ],
        PropertyInfo(discriminator="op"),
    ]


class OperandConstEvaluationRunCondition(BaseModel):
    op: Optional[Literal["const"]] = None

    value: Union[str, float, bool, None] = None


class OperandVarEvaluationRunCondition(BaseModel):
    path: str

    op: Optional[Literal["var"]] = None


if TYPE_CHECKING or not PYDANTIC_V1:
    Operand = TypeAliasType(
        "Operand",
        Annotated[
            Union[
                OperandConstEvaluationRunCondition,
                OperandVarEvaluationRunCondition,
                "EqEvaluationRunCondition",
                "NeEvaluationRunCondition",
                "LtEvaluationRunCondition",
                "LteEvaluationRunCondition",
                "GtEvaluationRunCondition",
                "GteEvaluationRunCondition",
                "AndEvaluationRunCondition",
                "OrEvaluationRunCondition",
                "InEvaluationRunCondition",
                "NotInEvaluationRunCondition",
                "NotEvaluationRunCondition",
                "IsNullEvaluationRunCondition",
                "IsNotNullEvaluationRunCondition",
            ],
            PropertyInfo(discriminator="op"),
        ],
    )
else:
    Operand: TypeAlias = Annotated[
        Union[
            OperandConstEvaluationRunCondition,
            OperandVarEvaluationRunCondition,
            "EqEvaluationRunCondition",
            "NeEvaluationRunCondition",
            "LtEvaluationRunCondition",
            "LteEvaluationRunCondition",
            "GtEvaluationRunCondition",
            "GteEvaluationRunCondition",
            "AndEvaluationRunCondition",
            "OrEvaluationRunCondition",
            "InEvaluationRunCondition",
            "NotInEvaluationRunCondition",
            "NotEvaluationRunCondition",
            "IsNullEvaluationRunCondition",
            "IsNotNullEvaluationRunCondition",
        ],
        PropertyInfo(discriminator="op"),
    ]


class InEvaluationRunCondition(BaseModel):
    left: Left

    operands: List[Operand]

    op: Optional[Literal["in"]] = None


from .eq_evaluation_run_condition import EqEvaluationRunCondition
from .gt_evaluation_run_condition import GtEvaluationRunCondition
from .lt_evaluation_run_condition import LtEvaluationRunCondition
from .ne_evaluation_run_condition import NeEvaluationRunCondition
from .or_evaluation_run_condition import OrEvaluationRunCondition
from .and_evaluation_run_condition import AndEvaluationRunCondition
from .gte_evaluation_run_condition import GteEvaluationRunCondition
from .lte_evaluation_run_condition import LteEvaluationRunCondition
from .not_evaluation_run_condition import NotEvaluationRunCondition
from .not_in_evaluation_run_condition import NotInEvaluationRunCondition
from .is_null_evaluation_run_condition import IsNullEvaluationRunCondition
from .is_not_null_evaluation_run_condition import IsNotNullEvaluationRunCondition
