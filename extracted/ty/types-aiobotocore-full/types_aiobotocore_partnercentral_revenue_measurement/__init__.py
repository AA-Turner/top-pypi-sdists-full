"""
Main interface for partnercentral-revenue-measurement service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_revenue_measurement/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_partnercentral_revenue_measurement import (
        Client,
        ListMarketplaceRevenueShareAllocationsPaginator,
        ListMarketplaceRevenueSharesPaginator,
        ListRevenueAttributionAllocationsPaginator,
        ListRevenueAttributionsPaginator,
        PartnerCentralRevenueMeasurementAPIClient,
    )

    session = get_session()
    async with session.create_client("partnercentral-revenue-measurement") as client:
        client: PartnerCentralRevenueMeasurementAPIClient
        ...


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
