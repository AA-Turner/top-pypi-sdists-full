"""
Type annotations for gameliftstreams service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_gameliftstreams.client import GameLiftStreamsClient
    from types_aiobotocore_gameliftstreams.paginator import (
        ListApplicationsPaginator,
        ListStreamGroupsPaginator,
        ListStreamSessionsByAccountPaginator,
        ListStreamSessionsPaginator,
    )

    session = get_session()
    with session.create_client("gameliftstreams") as client:
        client: GameLiftStreamsClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_stream_groups_paginator: ListStreamGroupsPaginator = client.get_paginator("list_stream_groups")
        list_stream_sessions_by_account_paginator: ListStreamSessionsByAccountPaginator = client.get_paginator("list_stream_sessions_by_account")
        list_stream_sessions_paginator: ListStreamSessionsPaginator = client.get_paginator("list_stream_sessions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApplicationsInputPaginateTypeDef,
    ListApplicationsOutputTypeDef,
    ListStreamGroupsInputPaginateTypeDef,
    ListStreamGroupsOutputTypeDef,
    ListStreamSessionsByAccountInputPaginateTypeDef,
    ListStreamSessionsByAccountOutputTypeDef,
    ListStreamSessionsInputPaginateTypeDef,
    ListStreamSessionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListApplicationsPaginator",
    "ListStreamGroupsPaginator",
    "ListStreamSessionsByAccountPaginator",
    "ListStreamSessionsPaginator",
)

if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsOutputTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/paginator/ListApplications.html#GameLiftStreams.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/paginators/#listapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/paginator/ListApplications.html#GameLiftStreams.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/paginators/#listapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListStreamGroupsPaginatorBase = AioPaginator[ListStreamGroupsOutputTypeDef]
else:
    _ListStreamGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStreamGroupsPaginator(_ListStreamGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/paginator/ListStreamGroups.html#GameLiftStreams.Paginator.ListStreamGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/paginators/#liststreamgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStreamGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/paginator/ListStreamGroups.html#GameLiftStreams.Paginator.ListStreamGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/paginators/#liststreamgroupspaginator)
        """

if TYPE_CHECKING:
    _ListStreamSessionsByAccountPaginatorBase = AioPaginator[
        ListStreamSessionsByAccountOutputTypeDef
    ]
else:
    _ListStreamSessionsByAccountPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStreamSessionsByAccountPaginator(_ListStreamSessionsByAccountPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/paginator/ListStreamSessionsByAccount.html#GameLiftStreams.Paginator.ListStreamSessionsByAccount)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/paginators/#liststreamsessionsbyaccountpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamSessionsByAccountInputPaginateTypeDef]
    ) -> AioPageIterator[ListStreamSessionsByAccountOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/paginator/ListStreamSessionsByAccount.html#GameLiftStreams.Paginator.ListStreamSessionsByAccount.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/paginators/#liststreamsessionsbyaccountpaginator)
        """

if TYPE_CHECKING:
    _ListStreamSessionsPaginatorBase = AioPaginator[ListStreamSessionsOutputTypeDef]
else:
    _ListStreamSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStreamSessionsPaginator(_ListStreamSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/paginator/ListStreamSessions.html#GameLiftStreams.Paginator.ListStreamSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/paginators/#liststreamsessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamSessionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStreamSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gameliftstreams/paginator/ListStreamSessions.html#GameLiftStreams.Paginator.ListStreamSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gameliftstreams/paginators/#liststreamsessionspaginator)
        """
