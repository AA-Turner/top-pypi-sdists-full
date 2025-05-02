"""
Type annotations for ecr service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ecr.client import ECRClient
    from types_aiobotocore_ecr.waiter import (
        ImageScanCompleteWaiter,
        LifecyclePolicyPreviewCompleteWaiter,
    )

    session = get_session()
    async with session.create_client("ecr") as client:
        client: ECRClient

        image_scan_complete_waiter: ImageScanCompleteWaiter = client.get_waiter("image_scan_complete")
        lifecycle_policy_preview_complete_waiter: LifecyclePolicyPreviewCompleteWaiter = client.get_waiter("lifecycle_policy_preview_complete")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeImageScanFindingsRequestWaitTypeDef,
    GetLifecyclePolicyPreviewRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ImageScanCompleteWaiter", "LifecyclePolicyPreviewCompleteWaiter")


class ImageScanCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/waiter/ImageScanComplete.html#ECR.Waiter.ImageScanComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/waiters/#imagescancompletewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImageScanFindingsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/waiter/ImageScanComplete.html#ECR.Waiter.ImageScanComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/waiters/#imagescancompletewaiter)
        """


class LifecyclePolicyPreviewCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/waiter/LifecyclePolicyPreviewComplete.html#ECR.Waiter.LifecyclePolicyPreviewComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/waiters/#lifecyclepolicypreviewcompletewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLifecyclePolicyPreviewRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/waiter/LifecyclePolicyPreviewComplete.html#ECR.Waiter.LifecyclePolicyPreviewComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr/waiters/#lifecyclepolicypreviewcompletewaiter)
        """
