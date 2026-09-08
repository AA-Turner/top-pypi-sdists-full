"""
Type annotations for pricing-plan-manager service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pricing_plan_manager.client import PricingPlanManagerClient
    from types_aiobotocore_pricing_plan_manager.paginator import (
        ListSubscriptionsPaginator,
    )

    session = get_session()
    with session.create_client("pricing-plan-manager") as client:
        client: PricingPlanManagerClient

        list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListSubscriptionsInputPaginateTypeDef, ListSubscriptionsOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListSubscriptionsPaginator",)


if TYPE_CHECKING:
    _ListSubscriptionsPaginatorBase = AioPaginator[ListSubscriptionsOutputTypeDef]
else:
    _ListSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSubscriptionsPaginator(_ListSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/paginator/ListSubscriptions.html#PricingPlanManager.Paginator.ListSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/paginators/#listsubscriptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/paginator/ListSubscriptions.html#PricingPlanManager.Paginator.ListSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/paginators/#listsubscriptionspaginator)
        """
