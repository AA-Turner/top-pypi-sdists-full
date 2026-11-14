"""
Type annotations for imagebuilder service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_imagebuilder.client import ImagebuilderClient
    from mypy_boto3_imagebuilder.waiter import (
        ImageAvailableWaiter,
    )

    session = Session()
    client: ImagebuilderClient = session.client("imagebuilder")

    image_available_waiter: ImageAvailableWaiter = client.get_waiter("image_available")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetImageRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ImageAvailableWaiter",)


class ImageAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/waiter/ImageAvailable.html#Imagebuilder.Waiter.ImageAvailable)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/waiters/#imageavailablewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetImageRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/imagebuilder/waiter/ImageAvailable.html#Imagebuilder.Waiter.ImageAvailable.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_imagebuilder/waiters/#imageavailablewaiter)
        """
