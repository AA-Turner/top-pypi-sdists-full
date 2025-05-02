"""
Type annotations for mq service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mq.client import MQClient
    from types_aiobotocore_mq.paginator import (
        ListBrokersPaginator,
    )

    session = get_session()
    with session.create_client("mq") as client:
        client: MQClient

        list_brokers_paginator: ListBrokersPaginator = client.get_paginator("list_brokers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListBrokersRequestPaginateTypeDef, ListBrokersResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListBrokersPaginator",)

if TYPE_CHECKING:
    _ListBrokersPaginatorBase = AioPaginator[ListBrokersResponseTypeDef]
else:
    _ListBrokersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBrokersPaginator(_ListBrokersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/ListBrokers.html#MQ.Paginator.ListBrokers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/#listbrokerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBrokersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBrokersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mq/paginator/ListBrokers.html#MQ.Paginator.ListBrokers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mq/paginators/#listbrokerspaginator)
        """
