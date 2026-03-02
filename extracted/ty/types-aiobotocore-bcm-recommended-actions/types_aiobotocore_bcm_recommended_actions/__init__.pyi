"""
Main interface for bcm-recommended-actions service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_recommended_actions/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bcm_recommended_actions import (
        BillingandCostManagementRecommendedActionsClient,
        Client,
        ListRecommendedActionsPaginator,
    )

    session = get_session()
    async with session.create_client("bcm-recommended-actions") as client:
        client: BillingandCostManagementRecommendedActionsClient
        ...


    list_recommended_actions_paginator: ListRecommendedActionsPaginator = client.get_paginator("list_recommended_actions")
    ```
"""

from .client import BillingandCostManagementRecommendedActionsClient
from .paginator import ListRecommendedActionsPaginator

Client = BillingandCostManagementRecommendedActionsClient

__all__ = (
    "BillingandCostManagementRecommendedActionsClient",
    "Client",
    "ListRecommendedActionsPaginator",
)
