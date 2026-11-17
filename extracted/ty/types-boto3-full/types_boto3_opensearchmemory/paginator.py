"""
Type annotations for opensearchmemory service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_opensearchmemory.client import OpenSearchMemoryClient
    from types_boto3_opensearchmemory.paginator import (
        ListEventsPaginator,
        ListMemoriesPaginator,
        ListSpacesPaginator,
        SearchEventsPaginator,
        SearchMemoriesPaginator,
    )

    session = Session()
    client: OpenSearchMemoryClient = session.client("opensearchmemory")

    list_events_paginator: ListEventsPaginator = client.get_paginator("list_events")
    list_memories_paginator: ListMemoriesPaginator = client.get_paginator("list_memories")
    list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    search_events_paginator: SearchEventsPaginator = client.get_paginator("search_events")
    search_memories_paginator: SearchMemoriesPaginator = client.get_paginator("search_memories")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEventsInputPaginateTypeDef,
    ListEventsOutputTypeDef,
    ListMemoriesInputPaginateTypeDef,
    ListMemoriesOutputTypeDef,
    ListSpacesRequestPaginateTypeDef,
    ListSpacesResponseTypeDef,
    SearchEventsInputPaginateTypeDef,
    SearchEventsOutputTypeDef,
    SearchMemoriesInputPaginateTypeDef,
    SearchMemoriesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListEventsPaginator",
    "ListMemoriesPaginator",
    "ListSpacesPaginator",
    "SearchEventsPaginator",
    "SearchMemoriesPaginator",
)


if TYPE_CHECKING:
    _ListEventsPaginatorBase = Paginator[ListEventsOutputTypeDef]
else:
    _ListEventsPaginatorBase = Paginator  # type: ignore[assignment]


class ListEventsPaginator(_ListEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/ListEvents.html#OpenSearchMemory.Paginator.ListEvents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#listeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventsInputPaginateTypeDef]
    ) -> PageIterator[ListEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/ListEvents.html#OpenSearchMemory.Paginator.ListEvents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#listeventspaginator)
        """


if TYPE_CHECKING:
    _ListMemoriesPaginatorBase = Paginator[ListMemoriesOutputTypeDef]
else:
    _ListMemoriesPaginatorBase = Paginator  # type: ignore[assignment]


class ListMemoriesPaginator(_ListMemoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/ListMemories.html#OpenSearchMemory.Paginator.ListMemories)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#listmemoriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMemoriesInputPaginateTypeDef]
    ) -> PageIterator[ListMemoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/ListMemories.html#OpenSearchMemory.Paginator.ListMemories.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#listmemoriespaginator)
        """


if TYPE_CHECKING:
    _ListSpacesPaginatorBase = Paginator[ListSpacesResponseTypeDef]
else:
    _ListSpacesPaginatorBase = Paginator  # type: ignore[assignment]


class ListSpacesPaginator(_ListSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/ListSpaces.html#OpenSearchMemory.Paginator.ListSpaces)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#listspacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpacesRequestPaginateTypeDef]
    ) -> PageIterator[ListSpacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/ListSpaces.html#OpenSearchMemory.Paginator.ListSpaces.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#listspacespaginator)
        """


if TYPE_CHECKING:
    _SearchEventsPaginatorBase = Paginator[SearchEventsOutputTypeDef]
else:
    _SearchEventsPaginatorBase = Paginator  # type: ignore[assignment]


class SearchEventsPaginator(_SearchEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/SearchEvents.html#OpenSearchMemory.Paginator.SearchEvents)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#searcheventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchEventsInputPaginateTypeDef]
    ) -> PageIterator[SearchEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/SearchEvents.html#OpenSearchMemory.Paginator.SearchEvents.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#searcheventspaginator)
        """


if TYPE_CHECKING:
    _SearchMemoriesPaginatorBase = Paginator[SearchMemoriesOutputTypeDef]
else:
    _SearchMemoriesPaginatorBase = Paginator  # type: ignore[assignment]


class SearchMemoriesPaginator(_SearchMemoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/SearchMemories.html#OpenSearchMemory.Paginator.SearchMemories)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#searchmemoriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchMemoriesInputPaginateTypeDef]
    ) -> PageIterator[SearchMemoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearchmemory/paginator/SearchMemories.html#OpenSearchMemory.Paginator.SearchMemories.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchmemory/paginators/#searchmemoriespaginator)
        """
