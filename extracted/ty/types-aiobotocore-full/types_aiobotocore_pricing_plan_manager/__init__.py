"""
Main interface for pricing-plan-manager service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pricing_plan_manager import (
        Client,
        ListSubscriptionsPaginator,
        PricingPlanManagerClient,
    )

    session = get_session()
    async with session.create_client("pricing-plan-manager") as client:
        client: PricingPlanManagerClient
        ...


    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from .client import PricingPlanManagerClient
from .paginator import ListSubscriptionsPaginator

Client = PricingPlanManagerClient


__all__ = ("Client", "ListSubscriptionsPaginator", "PricingPlanManagerClient")
