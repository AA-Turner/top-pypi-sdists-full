"""
Type annotations for ecr service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_ecr.client import ECRClient
    from types_boto3_ecr.waiter import (
        ImageScanCompleteWaiter,
        LifecyclePolicyPreviewCompleteWaiter,
    )

    session = Session()
    client: ECRClient = session.client("ecr")

    image_scan_complete_waiter: ImageScanCompleteWaiter = client.get_waiter("image_scan_complete")
    lifecycle_policy_preview_complete_waiter: LifecyclePolicyPreviewCompleteWaiter = client.get_waiter("lifecycle_policy_preview_complete")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeImageScanFindingsRequestWaitTypeDef,
    GetLifecyclePolicyPreviewRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ImageScanCompleteWaiter", "LifecyclePolicyPreviewCompleteWaiter")


class ImageScanCompleteWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/waiter/ImageScanComplete.html#ECR.Waiter.ImageScanComplete)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr/waiters/#imagescancompletewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImageScanFindingsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/waiter/ImageScanComplete.html#ECR.Waiter.ImageScanComplete.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr/waiters/#imagescancompletewaiter)
        """


class LifecyclePolicyPreviewCompleteWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/waiter/LifecyclePolicyPreviewComplete.html#ECR.Waiter.LifecyclePolicyPreviewComplete)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr/waiters/#lifecyclepolicypreviewcompletewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLifecyclePolicyPreviewRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr/waiter/LifecyclePolicyPreviewComplete.html#ECR.Waiter.LifecyclePolicyPreviewComplete.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ecr/waiters/#lifecyclepolicypreviewcompletewaiter)
        """
