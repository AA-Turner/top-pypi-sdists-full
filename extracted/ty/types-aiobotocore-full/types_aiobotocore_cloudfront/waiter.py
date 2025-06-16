"""
Type annotations for cloudfront service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudfront.client import CloudFrontClient
    from types_aiobotocore_cloudfront.waiter import (
        DistributionDeployedWaiter,
        InvalidationCompletedWaiter,
        InvalidationForDistributionTenantCompletedWaiter,
        StreamingDistributionDeployedWaiter,
    )

    session = get_session()
    async with session.create_client("cloudfront") as client:
        client: CloudFrontClient

        distribution_deployed_waiter: DistributionDeployedWaiter = client.get_waiter("distribution_deployed")
        invalidation_completed_waiter: InvalidationCompletedWaiter = client.get_waiter("invalidation_completed")
        invalidation_for_distribution_tenant_completed_waiter: InvalidationForDistributionTenantCompletedWaiter = client.get_waiter("invalidation_for_distribution_tenant_completed")
        streaming_distribution_deployed_waiter: StreamingDistributionDeployedWaiter = client.get_waiter("streaming_distribution_deployed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetDistributionRequestWaitTypeDef,
    GetInvalidationForDistributionTenantRequestWaitTypeDef,
    GetInvalidationRequestWaitTypeDef,
    GetStreamingDistributionRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DistributionDeployedWaiter",
    "InvalidationCompletedWaiter",
    "InvalidationForDistributionTenantCompletedWaiter",
    "StreamingDistributionDeployedWaiter",
)


class DistributionDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/DistributionDeployed.html#CloudFront.Waiter.DistributionDeployed)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#distributiondeployedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetDistributionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/DistributionDeployed.html#CloudFront.Waiter.DistributionDeployed.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#distributiondeployedwaiter)
        """


class InvalidationCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/InvalidationCompleted.html#CloudFront.Waiter.InvalidationCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#invalidationcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetInvalidationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/InvalidationCompleted.html#CloudFront.Waiter.InvalidationCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#invalidationcompletedwaiter)
        """


class InvalidationForDistributionTenantCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/InvalidationForDistributionTenantCompleted.html#CloudFront.Waiter.InvalidationForDistributionTenantCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#invalidationfordistributiontenantcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetInvalidationForDistributionTenantRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/InvalidationForDistributionTenantCompleted.html#CloudFront.Waiter.InvalidationForDistributionTenantCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#invalidationfordistributiontenantcompletedwaiter)
        """


class StreamingDistributionDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/StreamingDistributionDeployed.html#CloudFront.Waiter.StreamingDistributionDeployed)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#streamingdistributiondeployedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetStreamingDistributionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/waiter/StreamingDistributionDeployed.html#CloudFront.Waiter.StreamingDistributionDeployed.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront/waiters/#streamingdistributiondeployedwaiter)
        """
