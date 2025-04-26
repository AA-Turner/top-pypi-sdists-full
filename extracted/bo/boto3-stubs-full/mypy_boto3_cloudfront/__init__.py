"""
Main interface for cloudfront service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudfront import (
        Client,
        CloudFrontClient,
        DistributionDeployedWaiter,
        InvalidationCompletedWaiter,
        ListCloudFrontOriginAccessIdentitiesPaginator,
        ListDistributionsPaginator,
        ListInvalidationsPaginator,
        ListKeyValueStoresPaginator,
        ListPublicKeysPaginator,
        ListStreamingDistributionsPaginator,
        StreamingDistributionDeployedWaiter,
    )

    session = Session()
    client: CloudFrontClient = session.client("cloudfront")

    distribution_deployed_waiter: DistributionDeployedWaiter = client.get_waiter("distribution_deployed")
    invalidation_completed_waiter: InvalidationCompletedWaiter = client.get_waiter("invalidation_completed")
    streaming_distribution_deployed_waiter: StreamingDistributionDeployedWaiter = client.get_waiter("streaming_distribution_deployed")

    list_cloud_front_origin_access_identities_paginator: ListCloudFrontOriginAccessIdentitiesPaginator = client.get_paginator("list_cloud_front_origin_access_identities")
    list_distributions_paginator: ListDistributionsPaginator = client.get_paginator("list_distributions")
    list_invalidations_paginator: ListInvalidationsPaginator = client.get_paginator("list_invalidations")
    list_key_value_stores_paginator: ListKeyValueStoresPaginator = client.get_paginator("list_key_value_stores")
    list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    list_streaming_distributions_paginator: ListStreamingDistributionsPaginator = client.get_paginator("list_streaming_distributions")
    ```
"""

from .client import CloudFrontClient
from .paginator import (
    ListCloudFrontOriginAccessIdentitiesPaginator,
    ListDistributionsPaginator,
    ListInvalidationsPaginator,
    ListKeyValueStoresPaginator,
    ListPublicKeysPaginator,
    ListStreamingDistributionsPaginator,
)
from .waiter import (
    DistributionDeployedWaiter,
    InvalidationCompletedWaiter,
    StreamingDistributionDeployedWaiter,
)

Client = CloudFrontClient


__all__ = (
    "Client",
    "CloudFrontClient",
    "DistributionDeployedWaiter",
    "InvalidationCompletedWaiter",
    "ListCloudFrontOriginAccessIdentitiesPaginator",
    "ListDistributionsPaginator",
    "ListInvalidationsPaginator",
    "ListKeyValueStoresPaginator",
    "ListPublicKeysPaginator",
    "ListStreamingDistributionsPaginator",
    "StreamingDistributionDeployedWaiter",
)
