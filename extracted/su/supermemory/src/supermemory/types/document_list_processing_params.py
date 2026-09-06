# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DocumentListProcessingParams"]


class DocumentListProcessingParams(TypedDict, total=False):
    container_tags: Annotated[str, PropertyInfo(alias="containerTags")]
    """Comma-separated container tags to filter by"""

    limit: Union[str, float]
    """Number of items per page. Used with `view=all`."""

    page: Union[str, float]
    """Page number to fetch. Used with `view=all`."""

    view: Literal["active", "pending", "all"]
    """`active` returns in-flight documents updated in the last 4 hours.

    `pending` returns every document that is not done or failed, with no time
    cutoff. `all` also includes failed documents, paginated.
    """
