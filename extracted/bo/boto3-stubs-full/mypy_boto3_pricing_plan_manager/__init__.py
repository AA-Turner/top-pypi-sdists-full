"""
Main interface for pricing-plan-manager service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pricing_plan_manager/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pricing_plan_manager import (
        Client,
        ListSubscriptionsPaginator,
        PricingPlanManagerClient,
    )

    session = Session()
    client: PricingPlanManagerClient = session.client("pricing-plan-manager")

    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from .client import PricingPlanManagerClient
from .paginator import ListSubscriptionsPaginator

Client = PricingPlanManagerClient


__all__ = ("Client", "ListSubscriptionsPaginator", "PricingPlanManagerClient")
