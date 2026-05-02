# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, List, Union, Optional
from typing_extensions import Literal, TypeAlias, TypeAliasType

from .._compat import PYDANTIC_V1
from .._models import BaseModel
from .component import Component

__all__ = ["Container", "Child"]

if TYPE_CHECKING or not PYDANTIC_V1:
    Child = TypeAliasType("Child", Union["Container", Component])
else:
    Child: TypeAlias = Union["Container", Component]


class Container(BaseModel):
    children: List[Child]
    """The children to be displayed within the container"""

    direction: Optional[Literal["row", "column"]] = None
    """The axis that children are placed in the container.

    Based on CSS `flex-direction` (see:
    https://developer.mozilla.org/en-US/docs/Web/CSS/flex-direction)
    """
