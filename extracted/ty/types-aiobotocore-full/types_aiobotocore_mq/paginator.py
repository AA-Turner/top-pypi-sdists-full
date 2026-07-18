"""
Type annotations for mq service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mq.client import MQClient
    from types_aiobotocore_mq.paginator import (
        DescribeSharedResourcesPaginator,
        ListBrokersPaginator,
    )

    session = get_session()
    with session.create_client("mq") as client:
        client: MQClient

        describe_shared_resources_paginator: DescribeSharedResourcesPaginator = client.get_paginator("describe_shared_resources")
        list_brokers_paginator: ListBrokersPaginator = client.get_paginator("list_brokers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeSharedResourcesRequestPaginateTypeDef,
    DescribeSharedResourcesResponseTypeDef,
    ListBrokersRequestPaginateTypeDef,
    ListBrokersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeSharedResourcesPaginator", "ListBrokersPaginator")


if TYPE_CHECKING:
    _DescribeSharedResourcesPaginatorBase = AioPaginator[DescribeSharedResourcesResponseTypeDef]
else:
    _DescribeSharedResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSharedResourcesPaginator(_DescribeSharedResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/DescribeSharedResources.html#MQ.Paginator.DescribeSharedResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/#describesharedresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSharedResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSharedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/DescribeSharedResources.html#MQ.Paginator.DescribeSharedResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/#describesharedresourcespaginator)
        """


if TYPE_CHECKING:
    _ListBrokersPaginatorBase = AioPaginator[ListBrokersResponseTypeDef]
else:
    _ListBrokersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBrokersPaginator(_ListBrokersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/ListBrokers.html#MQ.Paginator.ListBrokers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/#listbrokerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBrokersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBrokersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/ListBrokers.html#MQ.Paginator.ListBrokers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/#listbrokerspaginator)
        """
