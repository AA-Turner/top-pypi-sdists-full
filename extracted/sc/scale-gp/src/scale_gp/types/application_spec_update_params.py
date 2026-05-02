# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["ApplicationSpecUpdateParams", "PartialApplicationSpecRequest", "RestoreRequest"]


class PartialApplicationSpecRequest(TypedDict, total=False):
    description: str
    """The description of the Application Spec"""

    name: str
    """The name of the Application Spec"""

    restore: Literal[False]
    """Set to true to restore the entity from the database."""

    run_online_evaluation: bool
    """Whether the application spec should run online evaluation, default is `false`"""

    theme_id: str


class RestoreRequest(TypedDict, total=False):
    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""


ApplicationSpecUpdateParams: TypeAlias = Union[PartialApplicationSpecRequest, RestoreRequest]
