"""
Type annotations for savingsplans service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_savingsplans.client import SavingsPlansClient

    session = get_session()
    async with session.create_client("savingsplans") as client:
        client: SavingsPlansClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CreateSavingsPlanRequestTypeDef,
    CreateSavingsPlanResponseTypeDef,
    DeleteQueuedSavingsPlanRequestTypeDef,
    DescribeSavingsPlanRatesRequestTypeDef,
    DescribeSavingsPlanRatesResponseTypeDef,
    DescribeSavingsPlansOfferingRatesRequestTypeDef,
    DescribeSavingsPlansOfferingRatesResponseTypeDef,
    DescribeSavingsPlansOfferingsRequestTypeDef,
    DescribeSavingsPlansOfferingsResponseTypeDef,
    DescribeSavingsPlansRequestTypeDef,
    DescribeSavingsPlansResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ReturnSavingsPlanRequestTypeDef,
    ReturnSavingsPlanResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("SavingsPlansClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SavingsPlansClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans.html#SavingsPlans.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SavingsPlansClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans.html#SavingsPlans.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#generate_presigned_url)
        """

    async def create_savings_plan(
        self, **kwargs: Unpack[CreateSavingsPlanRequestTypeDef]
    ) -> CreateSavingsPlanResponseTypeDef:
        """
        Creates a Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/create_savings_plan.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#create_savings_plan)
        """

    async def delete_queued_savings_plan(
        self, **kwargs: Unpack[DeleteQueuedSavingsPlanRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the queued purchase for the specified Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/delete_queued_savings_plan.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#delete_queued_savings_plan)
        """

    async def describe_savings_plan_rates(
        self, **kwargs: Unpack[DescribeSavingsPlanRatesRequestTypeDef]
    ) -> DescribeSavingsPlanRatesResponseTypeDef:
        """
        Describes the rates for the specified Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plan_rates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#describe_savings_plan_rates)
        """

    async def describe_savings_plans(
        self, **kwargs: Unpack[DescribeSavingsPlansRequestTypeDef]
    ) -> DescribeSavingsPlansResponseTypeDef:
        """
        Describes the specified Savings Plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plans.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#describe_savings_plans)
        """

    async def describe_savings_plans_offering_rates(
        self, **kwargs: Unpack[DescribeSavingsPlansOfferingRatesRequestTypeDef]
    ) -> DescribeSavingsPlansOfferingRatesResponseTypeDef:
        """
        Describes the offering rates for the specified Savings Plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plans_offering_rates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#describe_savings_plans_offering_rates)
        """

    async def describe_savings_plans_offerings(
        self, **kwargs: Unpack[DescribeSavingsPlansOfferingsRequestTypeDef]
    ) -> DescribeSavingsPlansOfferingsResponseTypeDef:
        """
        Describes the offerings for the specified Savings Plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plans_offerings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#describe_savings_plans_offerings)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#list_tags_for_resource)
        """

    async def return_savings_plan(
        self, **kwargs: Unpack[ReturnSavingsPlanRequestTypeDef]
    ) -> ReturnSavingsPlanResponseTypeDef:
        """
        Returns the specified Savings Plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/return_savings_plan.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#return_savings_plan)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/#untag_resource)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans.html#SavingsPlans.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans.html#SavingsPlans.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_savingsplans/client/)
        """
