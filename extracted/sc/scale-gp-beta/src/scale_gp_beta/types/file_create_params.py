# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._types import FileTypes
from .._utils import PropertyInfo

__all__ = ["FileCreateParams"]


class FileCreateParams(TypedDict, total=False):
    file: Required[FileTypes]

    x_project_id: Annotated[str, PropertyInfo(alias="x-project-id")]
