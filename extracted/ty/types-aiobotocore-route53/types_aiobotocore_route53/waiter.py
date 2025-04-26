"""
Type annotations for route53 service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53.client import Route53Client
    from types_aiobotocore_route53.waiter import (
        ResourceRecordSetsChangedWaiter,
    )

    session = get_session()
    async with session.create_client("route53") as client:
        client: Route53Client

        resource_record_sets_changed_waiter: ResourceRecordSetsChangedWaiter = client.get_waiter("resource_record_sets_changed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetChangeRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ResourceRecordSetsChangedWaiter",)


class ResourceRecordSetsChangedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/waiter/ResourceRecordSetsChanged.html#Route53.Waiter.ResourceRecordSetsChanged)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/waiters/#resourcerecordsetschangedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetChangeRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/waiter/ResourceRecordSetsChanged.html#Route53.Waiter.ResourceRecordSetsChanged.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/waiters/#resourcerecordsetschangedwaiter)
        """
