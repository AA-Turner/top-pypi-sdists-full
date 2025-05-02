"""
Type annotations for cloudcontrol service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudcontrol.client import CloudControlApiClient
    from types_aiobotocore_cloudcontrol.paginator import (
        ListResourceRequestsPaginator,
        ListResourcesPaginator,
    )

    session = get_session()
    with session.create_client("cloudcontrol") as client:
        client: CloudControlApiClient

        list_resource_requests_paginator: ListResourceRequestsPaginator = client.get_paginator("list_resource_requests")
        list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListResourceRequestsInputPaginateTypeDef,
    ListResourceRequestsOutputTypeDef,
    ListResourcesInputPaginateTypeDef,
    ListResourcesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListResourceRequestsPaginator", "ListResourcesPaginator")


if TYPE_CHECKING:
    _ListResourceRequestsPaginatorBase = AioPaginator[ListResourceRequestsOutputTypeDef]
else:
    _ListResourceRequestsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceRequestsPaginator(_ListResourceRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResourceRequests.html#CloudControlApi.Paginator.ListResourceRequests)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/#listresourcerequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceRequestsInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResourceRequests.html#CloudControlApi.Paginator.ListResourceRequests.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/#listresourcerequestspaginator)
        """


if TYPE_CHECKING:
    _ListResourcesPaginatorBase = AioPaginator[ListResourcesOutputTypeDef]
else:
    _ListResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourcesPaginator(_ListResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResources.html#CloudControlApi.Paginator.ListResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/#listresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/paginator/ListResources.html#CloudControlApi.Paginator.ListResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/paginators/#listresourcespaginator)
        """
