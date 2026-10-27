"""
Main interface for ecr service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ecr import (
        Client,
        DescribeImageScanFindingsPaginator,
        DescribeImagesPaginator,
        DescribePullThroughCacheRulesPaginator,
        DescribeReplicationBackfillResultsPaginator,
        DescribeRepositoriesPaginator,
        DescribeRepositoryCreationTemplatesPaginator,
        ECRClient,
        GetLifecyclePolicyPreviewPaginator,
        ImageScanCompleteWaiter,
        LifecyclePolicyPreviewCompleteWaiter,
        ListImagesPaginator,
        ListReplicationBackfillsPaginator,
    )

    session = Session()
    client: ECRClient = session.client("ecr")

    image_scan_complete_waiter: ImageScanCompleteWaiter = client.get_waiter("image_scan_complete")
    lifecycle_policy_preview_complete_waiter: LifecyclePolicyPreviewCompleteWaiter = client.get_waiter("lifecycle_policy_preview_complete")

    describe_image_scan_findings_paginator: DescribeImageScanFindingsPaginator = client.get_paginator("describe_image_scan_findings")
    describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
    describe_pull_through_cache_rules_paginator: DescribePullThroughCacheRulesPaginator = client.get_paginator("describe_pull_through_cache_rules")
    describe_replication_backfill_results_paginator: DescribeReplicationBackfillResultsPaginator = client.get_paginator("describe_replication_backfill_results")
    describe_repositories_paginator: DescribeRepositoriesPaginator = client.get_paginator("describe_repositories")
    describe_repository_creation_templates_paginator: DescribeRepositoryCreationTemplatesPaginator = client.get_paginator("describe_repository_creation_templates")
    get_lifecycle_policy_preview_paginator: GetLifecyclePolicyPreviewPaginator = client.get_paginator("get_lifecycle_policy_preview")
    list_images_paginator: ListImagesPaginator = client.get_paginator("list_images")
    list_replication_backfills_paginator: ListReplicationBackfillsPaginator = client.get_paginator("list_replication_backfills")
    ```
"""

from .client import ECRClient
from .paginator import (
    DescribeImageScanFindingsPaginator,
    DescribeImagesPaginator,
    DescribePullThroughCacheRulesPaginator,
    DescribeReplicationBackfillResultsPaginator,
    DescribeRepositoriesPaginator,
    DescribeRepositoryCreationTemplatesPaginator,
    GetLifecyclePolicyPreviewPaginator,
    ListImagesPaginator,
    ListReplicationBackfillsPaginator,
)
from .waiter import ImageScanCompleteWaiter, LifecyclePolicyPreviewCompleteWaiter

Client = ECRClient

__all__ = (
    "Client",
    "DescribeImageScanFindingsPaginator",
    "DescribeImagesPaginator",
    "DescribePullThroughCacheRulesPaginator",
    "DescribeReplicationBackfillResultsPaginator",
    "DescribeRepositoriesPaginator",
    "DescribeRepositoryCreationTemplatesPaginator",
    "ECRClient",
    "GetLifecyclePolicyPreviewPaginator",
    "ImageScanCompleteWaiter",
    "LifecyclePolicyPreviewCompleteWaiter",
    "ListImagesPaginator",
    "ListReplicationBackfillsPaginator",
)
