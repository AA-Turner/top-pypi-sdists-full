"""
Type annotations for securitylake service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_securitylake.client import SecurityLakeClient
    from types_aiobotocore_securitylake.paginator import (
        GetDataLakeSourcesPaginator,
        ListDataLakeExceptionsPaginator,
        ListLogSourcesPaginator,
        ListSubscribersPaginator,
    )

    session = get_session()
    with session.create_client("securitylake") as client:
        client: SecurityLakeClient

        get_data_lake_sources_paginator: GetDataLakeSourcesPaginator = client.get_paginator("get_data_lake_sources")
        list_data_lake_exceptions_paginator: ListDataLakeExceptionsPaginator = client.get_paginator("list_data_lake_exceptions")
        list_log_sources_paginator: ListLogSourcesPaginator = client.get_paginator("list_log_sources")
        list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetDataLakeSourcesRequestPaginateTypeDef,
    GetDataLakeSourcesResponseTypeDef,
    ListDataLakeExceptionsRequestPaginateTypeDef,
    ListDataLakeExceptionsResponseTypeDef,
    ListLogSourcesRequestPaginateTypeDef,
    ListLogSourcesResponseTypeDef,
    ListSubscribersRequestPaginateTypeDef,
    ListSubscribersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetDataLakeSourcesPaginator",
    "ListDataLakeExceptionsPaginator",
    "ListLogSourcesPaginator",
    "ListSubscribersPaginator",
)

if TYPE_CHECKING:
    _GetDataLakeSourcesPaginatorBase = AioPaginator[GetDataLakeSourcesResponseTypeDef]
else:
    _GetDataLakeSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetDataLakeSourcesPaginator(_GetDataLakeSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/GetDataLakeSources.html#SecurityLake.Paginator.GetDataLakeSources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#getdatalakesourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDataLakeSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDataLakeSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/GetDataLakeSources.html#SecurityLake.Paginator.GetDataLakeSources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#getdatalakesourcespaginator)
        """

if TYPE_CHECKING:
    _ListDataLakeExceptionsPaginatorBase = AioPaginator[ListDataLakeExceptionsResponseTypeDef]
else:
    _ListDataLakeExceptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataLakeExceptionsPaginator(_ListDataLakeExceptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListDataLakeExceptions.html#SecurityLake.Paginator.ListDataLakeExceptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listdatalakeexceptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataLakeExceptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataLakeExceptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListDataLakeExceptions.html#SecurityLake.Paginator.ListDataLakeExceptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listdatalakeexceptionspaginator)
        """

if TYPE_CHECKING:
    _ListLogSourcesPaginatorBase = AioPaginator[ListLogSourcesResponseTypeDef]
else:
    _ListLogSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLogSourcesPaginator(_ListLogSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListLogSources.html#SecurityLake.Paginator.ListLogSources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listlogsourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLogSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLogSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListLogSources.html#SecurityLake.Paginator.ListLogSources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listlogsourcespaginator)
        """

if TYPE_CHECKING:
    _ListSubscribersPaginatorBase = AioPaginator[ListSubscribersResponseTypeDef]
else:
    _ListSubscribersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSubscribersPaginator(_ListSubscribersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListSubscribers.html#SecurityLake.Paginator.ListSubscribers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listsubscriberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscribersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSubscribersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake/paginator/ListSubscribers.html#SecurityLake.Paginator.ListSubscribers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listsubscriberspaginator)
        """
