# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FileUpdateParams"]


class FileUpdateParams(TypedDict, total=False):
    tags: Dict[str, object]

    x_project_id: Annotated[str, PropertyInfo(alias="x-project-id")]
