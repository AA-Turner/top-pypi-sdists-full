"""
Main interface for partnercentral-revenue-measurement service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_revenue_measurement/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_partnercentral_revenue_measurement import (
        Client,
        ListMarketplaceRevenueShareAllocationsPaginator,
        ListMarketplaceRevenueSharesPaginator,
        ListRevenueAttributionAllocationsPaginator,
        ListRevenueAttributionsPaginator,
        PartnerCentralRevenueMeasurementAPIClient,
    )

    session = Session()
    client: PartnerCentralRevenueMeasurementAPIClient = session.client("partnercentral-revenue-measurement")

    list_marketplace_revenue_share_allocations_paginator: ListMarketplaceRevenueShareAllocationsPaginator = client.get_paginator("list_marketplace_revenue_share_allocations")
    list_marketplace_revenue_shares_paginator: ListMarketplaceRevenueSharesPaginator = client.get_paginator("list_marketplace_revenue_shares")
    list_revenue_attribution_allocations_paginator: ListRevenueAttributionAllocationsPaginator = client.get_paginator("list_revenue_attribution_allocations")
    list_revenue_attributions_paginator: ListRevenueAttributionsPaginator = client.get_paginator("list_revenue_attributions")
    ```
"""

from .client import PartnerCentralRevenueMeasurementAPIClient
from .paginator import (
    ListMarketplaceRevenueShareAllocationsPaginator,
    ListMarketplaceRevenueSharesPaginator,
    ListRevenueAttributionAllocationsPaginator,
    ListRevenueAttributionsPaginator,
)

Client = PartnerCentralRevenueMeasurementAPIClient


__all__ = (
    "Client",
    "ListMarketplaceRevenueShareAllocationsPaginator",
    "ListMarketplaceRevenueSharesPaginator",
    "ListRevenueAttributionAllocationsPaginator",
    "ListRevenueAttributionsPaginator",
    "PartnerCentralRevenueMeasurementAPIClient",
)
