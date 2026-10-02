# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["ExperimentAssignmentResponse", "UnionMember0", "UnionMember1"]


class UnionMember0(BaseModel):
    experiment_id: str

    in_experiment: Literal[True]

    success: Literal[True]

    variant_id: str

    experiment_key: Optional[str] = None

    experiment_name: Optional[str] = None

    is_control: Optional[bool] = None

    redirect: Optional[str] = None
    """
    Redirect destination for redirect (split-URL) variants — a same-domain relative
    path or an absolute https:// URL. Present only when the assigned variant is a
    redirect; absent for on-page (DOM-modification) variants. Read it straight off
    the payload and issue the redirect server-side.
    """

    type: Optional[str] = None

    variant_name: Optional[str] = None


class UnionMember1(BaseModel):
    in_experiment: Literal[False]

    success: Literal[True]


ExperimentAssignmentResponse: TypeAlias = Union[UnionMember0, UnionMember1]
