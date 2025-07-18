"""
Type annotations for keyspacesstreams service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspacesstreams/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_keyspacesstreams.client import KeyspacesStreamsClient
    from types_aiobotocore_keyspacesstreams.paginator import (
        GetStreamPaginator,
        ListStreamsPaginator,
    )

    session = get_session()
    with session.create_client("keyspacesstreams") as client:
        client: KeyspacesStreamsClient

        get_stream_paginator: GetStreamPaginator = client.get_paginator("get_stream")
        list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetStreamInputPaginateTypeDef,
    GetStreamOutputTypeDef,
    ListStreamsInputPaginateTypeDef,
    ListStreamsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetStreamPaginator", "ListStreamsPaginator")

if TYPE_CHECKING:
    _GetStreamPaginatorBase = AioPaginator[GetStreamOutputTypeDef]
else:
    _GetStreamPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetStreamPaginator(_GetStreamPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspacesstreams/paginator/GetStream.html#KeyspacesStreams.Paginator.GetStream)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspacesstreams/paginators/#getstreampaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetStreamInputPaginateTypeDef]
    ) -> AioPageIterator[GetStreamOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspacesstreams/paginator/GetStream.html#KeyspacesStreams.Paginator.GetStream.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspacesstreams/paginators/#getstreampaginator)
        """

if TYPE_CHECKING:
    _ListStreamsPaginatorBase = AioPaginator[ListStreamsOutputTypeDef]
else:
    _ListStreamsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStreamsPaginator(_ListStreamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspacesstreams/paginator/ListStreams.html#KeyspacesStreams.Paginator.ListStreams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspacesstreams/paginators/#liststreamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStreamsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/keyspacesstreams/paginator/ListStreams.html#KeyspacesStreams.Paginator.ListStreams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_keyspacesstreams/paginators/#liststreamspaginator)
        """
