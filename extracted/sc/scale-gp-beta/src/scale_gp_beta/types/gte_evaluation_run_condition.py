# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias, TypeAliasType

from .._utils import PropertyInfo
from .._compat import PYDANTIC_V1
from .._models import BaseModel

__all__ = [
    "GteEvaluationRunCondition",
    "Left",
    "LeftConstEvaluationRunCondition",
    "LeftVarEvaluationRunCondition",
    "Right",
    "RightConstEvaluationRunCondition",
    "RightVarEvaluationRunCondition",
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


class RightConstEvaluationRunCondition(BaseModel):
    op: Optional[Literal["const"]] = None

    value: Union[str, float, bool, None] = None


class RightVarEvaluationRunCondition(BaseModel):
    path: str

    op: Optional[Literal["var"]] = None


if TYPE_CHECKING or not PYDANTIC_V1:
    Right = TypeAliasType(
        "Right",
        Annotated[
            Union[
                RightConstEvaluationRunCondition,
                RightVarEvaluationRunCondition,
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
    Right: TypeAlias = Annotated[
        Union[
            RightConstEvaluationRunCondition,
            RightVarEvaluationRunCondition,
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


class GteEvaluationRunCondition(BaseModel):
    left: Left

    right: Right

    op: Optional[Literal["gte"]] = None


from .eq_evaluation_run_condition import EqEvaluationRunCondition
from .gt_evaluation_run_condition import GtEvaluationRunCondition
from .in_evaluation_run_condition import InEvaluationRunCondition
from .lt_evaluation_run_condition import LtEvaluationRunCondition
from .ne_evaluation_run_condition import NeEvaluationRunCondition
from .or_evaluation_run_condition import OrEvaluationRunCondition
from .and_evaluation_run_condition import AndEvaluationRunCondition
from .lte_evaluation_run_condition import LteEvaluationRunCondition
from .not_evaluation_run_condition import NotEvaluationRunCondition
from .not_in_evaluation_run_condition import NotInEvaluationRunCondition
from .is_null_evaluation_run_condition import IsNullEvaluationRunCondition
from .is_not_null_evaluation_run_condition import IsNotNullEvaluationRunCondition
