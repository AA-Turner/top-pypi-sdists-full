"""
Type annotations for observabilityadmin service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_observabilityadmin.client import CloudWatchObservabilityAdminServiceClient
    from types_aiobotocore_observabilityadmin.paginator import (
        ListResourceTelemetryForOrganizationPaginator,
        ListResourceTelemetryPaginator,
    )

    session = get_session()
    with session.create_client("observabilityadmin") as client:
        client: CloudWatchObservabilityAdminServiceClient

        list_resource_telemetry_for_organization_paginator: ListResourceTelemetryForOrganizationPaginator = client.get_paginator("list_resource_telemetry_for_organization")
        list_resource_telemetry_paginator: ListResourceTelemetryPaginator = client.get_paginator("list_resource_telemetry")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListResourceTelemetryForOrganizationInputPaginateTypeDef,
    ListResourceTelemetryForOrganizationOutputTypeDef,
    ListResourceTelemetryInputPaginateTypeDef,
    ListResourceTelemetryOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListResourceTelemetryForOrganizationPaginator", "ListResourceTelemetryPaginator")


if TYPE_CHECKING:
    _ListResourceTelemetryForOrganizationPaginatorBase = AioPaginator[
        ListResourceTelemetryForOrganizationOutputTypeDef
    ]
else:
    _ListResourceTelemetryForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceTelemetryForOrganizationPaginator(
    _ListResourceTelemetryForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetryForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetryForOrganization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetryfororganizationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceTelemetryForOrganizationInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceTelemetryForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetryForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetryForOrganization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetryfororganizationpaginator)
        """


if TYPE_CHECKING:
    _ListResourceTelemetryPaginatorBase = AioPaginator[ListResourceTelemetryOutputTypeDef]
else:
    _ListResourceTelemetryPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceTelemetryPaginator(_ListResourceTelemetryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetry.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetry)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetrypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceTelemetryInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceTelemetryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetry.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetry.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetrypaginator)
        """
