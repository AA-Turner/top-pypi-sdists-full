# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict, TypeAliasType

from .._compat import PYDANTIC_V1
from .component_param import ComponentParam

__all__ = ["ContainerParam", "Child"]

if TYPE_CHECKING or not PYDANTIC_V1:
    Child = TypeAliasType("Child", Union["ContainerParam", ComponentParam])
else:
    Child: TypeAlias = Union["ContainerParam", ComponentParam]


class ContainerParam(TypedDict, total=False):
    children: Required[Iterable[Child]]
    """The children to be displayed within the container"""

    direction: Literal["row", "column"]
    """The axis that children are placed in the container.

    Based on CSS `flex-direction` (see:
    https://developer.mozilla.org/en-US/docs/Web/CSS/flex-direction)
    """
