"""
Type annotations for partnercentral-revenue-measurement service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_partnercentral_revenue_measurement.client import PartnerCentralRevenueMeasurementAPIClient
    from types_boto3_partnercentral_revenue_measurement.paginator import (
        ListMarketplaceRevenueShareAllocationsPaginator,
        ListMarketplaceRevenueSharesPaginator,
        ListRevenueAttributionAllocationsPaginator,
        ListRevenueAttributionsPaginator,
    )

    session = Session()
    client: PartnerCentralRevenueMeasurementAPIClient = session.client("partnercentral-revenue-measurement")

    list_marketplace_revenue_share_allocations_paginator: ListMarketplaceRevenueShareAllocationsPaginator = client.get_paginator("list_marketplace_revenue_share_allocations")
    list_marketplace_revenue_shares_paginator: ListMarketplaceRevenueSharesPaginator = client.get_paginator("list_marketplace_revenue_shares")
    list_revenue_attribution_allocations_paginator: ListRevenueAttributionAllocationsPaginator = client.get_paginator("list_revenue_attribution_allocations")
    list_revenue_attributions_paginator: ListRevenueAttributionsPaginator = client.get_paginator("list_revenue_attributions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListMarketplaceRevenueShareAllocationsPaginatorBase = Paginator[
        ListMarketplaceRevenueShareAllocationsOutputTypeDef
    ]
else:
    _ListMarketplaceRevenueShareAllocationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListMarketplaceRevenueShareAllocationsPaginator(
    _ListMarketplaceRevenueShareAllocationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListMarketplaceRevenueShareAllocations.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListMarketplaceRevenueShareAllocations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/paginators/#listmarketplacerevenueshareallocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMarketplaceRevenueShareAllocationsInputPaginateTypeDef]
    ) -> PageIterator[ListMarketplaceRevenueShareAllocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListMarketplaceRevenueShareAllocations.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListMarketplaceRevenueShareAllocations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/paginators/#listmarketplacerevenueshareallocationspaginator)
        """


if TYPE_CHECKING:
    _ListMarketplaceRevenueSharesPaginatorBase = Paginator[
        ListMarketplaceRevenueSharesOutputTypeDef
    ]
else:
    _ListMarketplaceRevenueSharesPaginatorBase = Paginator  # type: ignore[assignment]


class ListMarketplaceRevenueSharesPaginator(_ListMarketplaceRevenueSharesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListMarketplaceRevenueShares.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListMarketplaceRevenueShares)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/paginators/#listmarketplacerevenuesharespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMarketplaceRevenueSharesInputPaginateTypeDef]
    ) -> PageIterator[ListMarketplaceRevenueSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListMarketplaceRevenueShares.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListMarketplaceRevenueShares.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/paginators/#listmarketplacerevenuesharespaginator)
        """


if TYPE_CHECKING:
    _ListRevenueAttributionAllocationsPaginatorBase = Paginator[
        ListRevenueAttributionAllocationsOutputTypeDef
    ]
else:
    _ListRevenueAttributionAllocationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListRevenueAttributionAllocationsPaginator(_ListRevenueAttributionAllocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListRevenueAttributionAllocations.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListRevenueAttributionAllocations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/paginators/#listrevenueattributionallocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRevenueAttributionAllocationsInputPaginateTypeDef]
    ) -> PageIterator[ListRevenueAttributionAllocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListRevenueAttributionAllocations.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListRevenueAttributionAllocations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/paginators/#listrevenueattributionallocationspaginator)
        """


if TYPE_CHECKING:
    _ListRevenueAttributionsPaginatorBase = Paginator[ListRevenueAttributionsOutputTypeDef]
else:
    _ListRevenueAttributionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListRevenueAttributionsPaginator(_ListRevenueAttributionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListRevenueAttributions.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListRevenueAttributions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/paginators/#listrevenueattributionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRevenueAttributionsInputPaginateTypeDef]
    ) -> PageIterator[ListRevenueAttributionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-revenue-measurement/paginator/ListRevenueAttributions.html#PartnerCentralRevenueMeasurementAPI.Paginator.ListRevenueAttributions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_partnercentral_revenue_measurement/paginators/#listrevenueattributionspaginator)
        """
