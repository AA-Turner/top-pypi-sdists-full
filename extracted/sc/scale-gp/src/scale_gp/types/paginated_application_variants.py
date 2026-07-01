# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .application_variant_v0_response import ApplicationVariantV0Response
from .offline_application_variant_response import OfflineApplicationVariantResponse

__all__ = ["PaginatedApplicationVariants", "Item"]

Item: TypeAlias = Annotated[
    Union[ApplicationVariantV0Response, "ApplicationVariantAgentsServiceResponse", OfflineApplicationVariantResponse],
    PropertyInfo(discriminator="version"),
]


class PaginatedApplicationVariants(BaseModel):
    current_page: int
    """The current page number."""

    items: List[Item]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""


from .application_variant_agents_service_response import ApplicationVariantAgentsServiceResponse
