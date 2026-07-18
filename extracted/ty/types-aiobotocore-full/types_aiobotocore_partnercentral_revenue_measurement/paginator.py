"""
Type annotations for partnercentral-revenue-measurement service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_partnercentral_revenue_measurement.client import PartnerCentralRevenueMeasurementAPIClient
    from types_aiobotocore_partnercentral_revenue_measurement.paginator import (
        ListMarketplaceRevenueShareAllocationsPaginator,
        ListMarketplaceRevenueSharesPaginator,
        ListRevenueAttributionAllocationsPaginator,
        ListRevenueAttributionsPaginator,
    )

    session = get_session()
    with session.create_client("partnercentral-revenue-measurement") as client:
        client: PartnerCentralRevenueMeasurementAPIClient

        list_marketplace_revenue_share_allocations_paginator: ListMarketplaceRevenueShareAllocationsPaginator = client.get_paginator("list_marketplace_revenue_share_allocations")
        list_marketplace_revenue_shares_paginator: ListMarketplaceRevenueSharesPaginator = client.get_paginator("list_marketplace_revenue_shares")
        list_revenue_attribution_allocations_paginator: ListRevenueAttributionAllocationsPaginator = client.get_paginator("list_revenue_attribution_allocations")
        list_revenue_attributions_paginator: ListRevenueAttributionsPaginator = client.get_paginator("list_revenue_attributions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListMarketplaceRevenueShareAllocationsInputPaginateTypeDef,
    ListMarketplaceRevenueShareAllocationsOutputTypeDef,
    ListMarketplaceRevenueSharesInputPaginateTypeDef,
    ListMarketplaceRevenueSharesOutputTypeDef,
    ListRevenueAttributionAllocationsInputPaginateTypeDef,
    ListRevenueAttributionAllocationsOutputTypeDef,
    ListRevenueAttributionsInputPaginateTypeDef,
    ListRevenueAttributionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListMarketplaceRevenueShareAllocationsPaginator",
    "ListMarketplaceRevenueSharesPaginator",
    "ListRevenueAttributionAllocationsPaginator",
    "ListRevenueAttributionsPaginator",
)


if TYPE_CHECKING:
    _ListMarketplaceRevenueShareAllocationsPaginatorBase = AioPaginator[
        ListMarketplaceRevenueShareAllocationsOutputTypeDef
    ]
else:
    _ListMarketplaceRevenueShareAllocationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMarketplaceRevenueShareAllocationsPaginator(
    _ListMarketplaceRevenueShareAllocationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListMarketplaceRevenueShareAllocations.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListMarketplaceRevenueShareAllocations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/paginators/#listmarketplacerevenueshareallocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMarketplaceRevenueShareAllocationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMarketplaceRevenueShareAllocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListMarketplaceRevenueShareAllocations.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListMarketplaceRevenueShareAllocations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/paginators/#listmarketplacerevenueshareallocationspaginator)
        """


if TYPE_CHECKING:
    _ListMarketplaceRevenueSharesPaginatorBase = AioPaginator[
        ListMarketplaceRevenueSharesOutputTypeDef
    ]
else:
    _ListMarketplaceRevenueSharesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMarketplaceRevenueSharesPaginator(_ListMarketplaceRevenueSharesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListMarketplaceRevenueShares.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListMarketplaceRevenueShares)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/paginators/#listmarketplacerevenuesharespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMarketplaceRevenueSharesInputPaginateTypeDef]
    ) -> AioPageIterator[ListMarketplaceRevenueSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListMarketplaceRevenueShares.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListMarketplaceRevenueShares.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/paginators/#listmarketplacerevenuesharespaginator)
        """


if TYPE_CHECKING:
    _ListRevenueAttributionAllocationsPaginatorBase = AioPaginator[
        ListRevenueAttributionAllocationsOutputTypeDef
    ]
else:
    _ListRevenueAttributionAllocationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRevenueAttributionAllocationsPaginator(_ListRevenueAttributionAllocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListRevenueAttributionAllocations.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListRevenueAttributionAllocations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/paginators/#listrevenueattributionallocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRevenueAttributionAllocationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRevenueAttributionAllocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListRevenueAttributionAllocations.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListRevenueAttributionAllocations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/paginators/#listrevenueattributionallocationspaginator)
        """


if TYPE_CHECKING:
    _ListRevenueAttributionsPaginatorBase = AioPaginator[ListRevenueAttributionsOutputTypeDef]
else:
    _ListRevenueAttributionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRevenueAttributionsPaginator(_ListRevenueAttributionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListRevenueAttributions.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListRevenueAttributions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/paginators/#listrevenueattributionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRevenueAttributionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRevenueAttributionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListRevenueAttributions.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListRevenueAttributions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/paginators/#listrevenueattributionspaginator)
        """
