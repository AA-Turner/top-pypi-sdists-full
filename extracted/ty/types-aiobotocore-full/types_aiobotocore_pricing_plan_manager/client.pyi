"""
Type annotations for pricing-plan-manager service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_pricing_plan_manager.client import PricingPlanManagerClient

    session = get_session()
    async with session.create_client("pricing-plan-manager") as client:
        client: PricingPlanManagerClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListSubscriptionsPaginator
from .type_defs import (
    ApprovePaidSubscriptionInputTypeDef,
    ApprovePaidSubscriptionOutputTypeDef,
    AssociateResourcesToSubscriptionInputTypeDef,
    AssociateResourcesToSubscriptionOutputTypeDef,
    CancelSubscriptionChangeInputTypeDef,
    CancelSubscriptionChangeOutputTypeDef,
    CancelSubscriptionInputTypeDef,
    CancelSubscriptionOutputTypeDef,
    CreateSubscriptionInputTypeDef,
    CreateSubscriptionOutputTypeDef,
    DisassociateResourcesFromSubscriptionInputTypeDef,
    DisassociateResourcesFromSubscriptionOutputTypeDef,
    GetSubscriptionInputTypeDef,
    GetSubscriptionOutputTypeDef,
    ListSubscriptionsInputTypeDef,
    ListSubscriptionsOutputTypeDef,
    UpdateSubscriptionInputTypeDef,
    UpdateSubscriptionOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("PricingPlanManagerClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class PricingPlanManagerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager.html#PricingPlanManager.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PricingPlanManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager.html#PricingPlanManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#generate_presigned_url)
        """

    async def approve_paid_subscription(
        self, **kwargs: Unpack[ApprovePaidSubscriptionInputTypeDef]
    ) -> ApprovePaidSubscriptionOutputTypeDef:
        """
        Approves a subscription that is in <code>PENDING_APPROVAL</code> status,
        activating it and starting billing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/approve_paid_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#approve_paid_subscription)
        """

    async def associate_resources_to_subscription(
        self, **kwargs: Unpack[AssociateResourcesToSubscriptionInputTypeDef]
    ) -> AssociateResourcesToSubscriptionOutputTypeDef:
        """
        Adds one or more resources to an existing subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/associate_resources_to_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#associate_resources_to_subscription)
        """

    async def cancel_subscription(
        self, **kwargs: Unpack[CancelSubscriptionInputTypeDef]
    ) -> CancelSubscriptionOutputTypeDef:
        """
        Cancels a flat-rate pricing subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/cancel_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#cancel_subscription)
        """

    async def cancel_subscription_change(
        self, **kwargs: Unpack[CancelSubscriptionChangeInputTypeDef]
    ) -> CancelSubscriptionChangeOutputTypeDef:
        """
        Cancels a pending scheduled change on a subscription, such as a pending
        downgrade or cancellation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/cancel_subscription_change.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#cancel_subscription_change)
        """

    async def create_subscription(
        self, **kwargs: Unpack[CreateSubscriptionInputTypeDef]
    ) -> CreateSubscriptionOutputTypeDef:
        """
        Creates a flat-rate pricing subscription for the specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/create_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#create_subscription)
        """

    async def disassociate_resources_from_subscription(
        self, **kwargs: Unpack[DisassociateResourcesFromSubscriptionInputTypeDef]
    ) -> DisassociateResourcesFromSubscriptionOutputTypeDef:
        """
        Removes one or more resources from an existing subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/disassociate_resources_from_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#disassociate_resources_from_subscription)
        """

    async def get_subscription(
        self, **kwargs: Unpack[GetSubscriptionInputTypeDef]
    ) -> GetSubscriptionOutputTypeDef:
        """
        Returns the details of a flat-rate pricing subscription, including its current
        status, associated resources, and any pending scheduled changes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/get_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#get_subscription)
        """

    async def list_subscriptions(
        self, **kwargs: Unpack[ListSubscriptionsInputTypeDef]
    ) -> ListSubscriptionsOutputTypeDef:
        """
        Returns a summary of all flat-rate pricing subscriptions in the calling account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/list_subscriptions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#list_subscriptions)
        """

    async def update_subscription(
        self, **kwargs: Unpack[UpdateSubscriptionInputTypeDef]
    ) -> UpdateSubscriptionOutputTypeDef:
        """
        Changes the plan tier of an existing subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/update_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#update_subscription)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_subscriptions"]
    ) -> ListSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager.html#PricingPlanManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pricing-plan-manager.html#PricingPlanManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pricing_plan_manager/client/)
        """
