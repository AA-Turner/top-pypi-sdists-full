"""
Type annotations for elementalinference service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elementalinference.client import ElementalInferenceClient
    from mypy_boto3_elementalinference.paginator import (
        ListDictionariesPaginator,
        ListFeedsPaginator,
        SearchFixturesPaginator,
    )

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")

    list_dictionaries_paginator: ListDictionariesPaginator = client.get_paginator("list_dictionaries")
    list_feeds_paginator: ListFeedsPaginator = client.get_paginator("list_feeds")
    search_fixtures_paginator: SearchFixturesPaginator = client.get_paginator("search_fixtures")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListDictionariesRequestPaginateTypeDef,
    ListDictionariesResponseTypeDef,
    ListFeedsRequestPaginateTypeDef,
    ListFeedsResponseTypeDef,
    SearchFixturesRequestPaginateTypeDef,
    SearchFixturesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListDictionariesPaginator", "ListFeedsPaginator", "SearchFixturesPaginator")


if TYPE_CHECKING:
    _ListDictionariesPaginatorBase = Paginator[ListDictionariesResponseTypeDef]
else:
    _ListDictionariesPaginatorBase = Paginator  # type: ignore[assignment]


class ListDictionariesPaginator(_ListDictionariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListDictionaries.html#ElementalInference.Paginator.ListDictionaries)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/#listdictionariespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDictionariesRequestPaginateTypeDef]
    ) -> PageIterator[ListDictionariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListDictionaries.html#ElementalInference.Paginator.ListDictionaries.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/#listdictionariespaginator)
        """


if TYPE_CHECKING:
    _ListFeedsPaginatorBase = Paginator[ListFeedsResponseTypeDef]
else:
    _ListFeedsPaginatorBase = Paginator  # type: ignore[assignment]


class ListFeedsPaginator(_ListFeedsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFeeds.html#ElementalInference.Paginator.ListFeeds)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/#listfeedspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFeedsRequestPaginateTypeDef]
    ) -> PageIterator[ListFeedsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFeeds.html#ElementalInference.Paginator.ListFeeds.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/#listfeedspaginator)
        """


if TYPE_CHECKING:
    _SearchFixturesPaginatorBase = Paginator[SearchFixturesResponseTypeDef]
else:
    _SearchFixturesPaginatorBase = Paginator  # type: ignore[assignment]


class SearchFixturesPaginator(_SearchFixturesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/SearchFixtures.html#ElementalInference.Paginator.SearchFixtures)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/#searchfixturespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchFixturesRequestPaginateTypeDef]
    ) -> PageIterator[SearchFixturesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/SearchFixtures.html#ElementalInference.Paginator.SearchFixtures.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elementalinference/paginators/#searchfixturespaginator)
        """
