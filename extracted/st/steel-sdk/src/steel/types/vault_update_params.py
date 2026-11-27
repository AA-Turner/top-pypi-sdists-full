# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["VaultUpdateParams"]


class VaultUpdateParams(TypedDict, total=False):
    project_id: Annotated[str, PropertyInfo(alias="projectId")]

    description: Optional[str]

    name: str
    """
    1–63 lowercase letters, digits, hyphens, underscores or dots; must start with a
    letter or digit.
    """
