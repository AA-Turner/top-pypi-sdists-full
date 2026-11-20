"""
Type annotations for route53 service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_route53.client import Route53Client
    from mypy_boto3_route53.waiter import (
        HealthCheckSourceCreatedWaiter,
        HealthCheckSourceDeletedWaiter,
        ResourceRecordSetsChangedWaiter,
    )

    session = Session()
    client: Route53Client = session.client("route53")

    health_check_source_created_waiter: HealthCheckSourceCreatedWaiter = client.get_waiter("health_check_source_created")
    health_check_source_deleted_waiter: HealthCheckSourceDeletedWaiter = client.get_waiter("health_check_source_deleted")
    resource_record_sets_changed_waiter: ResourceRecordSetsChangedWaiter = client.get_waiter("resource_record_sets_changed")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import (
    GetChangeRequestWaitTypeDef,
    GetHealthCheckSourceRequestWaitExtraTypeDef,
    GetHealthCheckSourceRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "HealthCheckSourceCreatedWaiter",
    "HealthCheckSourceDeletedWaiter",
    "ResourceRecordSetsChangedWaiter",
)


class HealthCheckSourceCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/waiter/HealthCheckSourceCreated.html#Route53.Waiter.HealthCheckSourceCreated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/#healthchecksourcecreatedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetHealthCheckSourceRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/waiter/HealthCheckSourceCreated.html#Route53.Waiter.HealthCheckSourceCreated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/#healthchecksourcecreatedwaiter)
        """


class HealthCheckSourceDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/waiter/HealthCheckSourceDeleted.html#Route53.Waiter.HealthCheckSourceDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/#healthchecksourcedeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetHealthCheckSourceRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/waiter/HealthCheckSourceDeleted.html#Route53.Waiter.HealthCheckSourceDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/#healthchecksourcedeletedwaiter)
        """


class ResourceRecordSetsChangedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/waiter/ResourceRecordSetsChanged.html#Route53.Waiter.ResourceRecordSetsChanged)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/#resourcerecordsetschangedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetChangeRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/waiter/ResourceRecordSetsChanged.html#Route53.Waiter.ResourceRecordSetsChanged.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53/waiters/#resourcerecordsetschangedwaiter)
        """
