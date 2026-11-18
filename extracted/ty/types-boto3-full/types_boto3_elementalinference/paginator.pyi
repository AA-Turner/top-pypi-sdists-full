"""
Type annotations for elementalinference service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_elementalinference.client import ElementalInferenceClient
    from types_boto3_elementalinference.paginator import (
        ListDictionariesPaginator,
        ListFeedsPaginator,
        ListFunctionsPaginator,
        ListQuestionSetVersionsPaginator,
        ListQuestionSetsPaginator,
        ListScheduleActionsPaginator,
        SearchFixturesPaginator,
    )

    session = Session()
    client: ElementalInferenceClient = session.client("elementalinference")

    list_dictionaries_paginator: ListDictionariesPaginator = client.get_paginator("list_dictionaries")
    list_feeds_paginator: ListFeedsPaginator = client.get_paginator("list_feeds")
    list_functions_paginator: ListFunctionsPaginator = client.get_paginator("list_functions")
    list_question_set_versions_paginator: ListQuestionSetVersionsPaginator = client.get_paginator("list_question_set_versions")
    list_question_sets_paginator: ListQuestionSetsPaginator = client.get_paginator("list_question_sets")
    list_schedule_actions_paginator: ListScheduleActionsPaginator = client.get_paginator("list_schedule_actions")
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
    ListFunctionsRequestPaginateTypeDef,
    ListFunctionsResponseTypeDef,
    ListQuestionSetsRequestPaginateTypeDef,
    ListQuestionSetsResponseTypeDef,
    ListQuestionSetVersionsRequestPaginateTypeDef,
    ListQuestionSetVersionsResponseTypeDef,
    ListScheduleActionsRequestPaginateTypeDef,
    ListScheduleActionsResponseTypeDef,
    SearchFixturesRequestPaginateTypeDef,
    SearchFixturesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDictionariesPaginator",
    "ListFeedsPaginator",
    "ListFunctionsPaginator",
    "ListQuestionSetVersionsPaginator",
    "ListQuestionSetsPaginator",
    "ListScheduleActionsPaginator",
    "SearchFixturesPaginator",
)

if TYPE_CHECKING:
    _ListDictionariesPaginatorBase = Paginator[ListDictionariesResponseTypeDef]
else:
    _ListDictionariesPaginatorBase = Paginator  # type: ignore[assignment]

class ListDictionariesPaginator(_ListDictionariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListDictionaries.html#ElementalInference.Paginator.ListDictionaries)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listdictionariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDictionariesRequestPaginateTypeDef]
    ) -> PageIterator[ListDictionariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListDictionaries.html#ElementalInference.Paginator.ListDictionaries.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listdictionariespaginator)
        """

if TYPE_CHECKING:
    _ListFeedsPaginatorBase = Paginator[ListFeedsResponseTypeDef]
else:
    _ListFeedsPaginatorBase = Paginator  # type: ignore[assignment]

class ListFeedsPaginator(_ListFeedsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFeeds.html#ElementalInference.Paginator.ListFeeds)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listfeedspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFeedsRequestPaginateTypeDef]
    ) -> PageIterator[ListFeedsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFeeds.html#ElementalInference.Paginator.ListFeeds.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listfeedspaginator)
        """

if TYPE_CHECKING:
    _ListFunctionsPaginatorBase = Paginator[ListFunctionsResponseTypeDef]
else:
    _ListFunctionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListFunctionsPaginator(_ListFunctionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFunctions.html#ElementalInference.Paginator.ListFunctions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listfunctionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFunctionsRequestPaginateTypeDef]
    ) -> PageIterator[ListFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListFunctions.html#ElementalInference.Paginator.ListFunctions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listfunctionspaginator)
        """

if TYPE_CHECKING:
    _ListQuestionSetVersionsPaginatorBase = Paginator[ListQuestionSetVersionsResponseTypeDef]
else:
    _ListQuestionSetVersionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListQuestionSetVersionsPaginator(_ListQuestionSetVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListQuestionSetVersions.html#ElementalInference.Paginator.ListQuestionSetVersions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listquestionsetversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQuestionSetVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListQuestionSetVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListQuestionSetVersions.html#ElementalInference.Paginator.ListQuestionSetVersions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listquestionsetversionspaginator)
        """

if TYPE_CHECKING:
    _ListQuestionSetsPaginatorBase = Paginator[ListQuestionSetsResponseTypeDef]
else:
    _ListQuestionSetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListQuestionSetsPaginator(_ListQuestionSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListQuestionSets.html#ElementalInference.Paginator.ListQuestionSets)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listquestionsetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQuestionSetsRequestPaginateTypeDef]
    ) -> PageIterator[ListQuestionSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListQuestionSets.html#ElementalInference.Paginator.ListQuestionSets.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listquestionsetspaginator)
        """

if TYPE_CHECKING:
    _ListScheduleActionsPaginatorBase = Paginator[ListScheduleActionsResponseTypeDef]
else:
    _ListScheduleActionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListScheduleActionsPaginator(_ListScheduleActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListScheduleActions.html#ElementalInference.Paginator.ListScheduleActions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listscheduleactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScheduleActionsRequestPaginateTypeDef]
    ) -> PageIterator[ListScheduleActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/ListScheduleActions.html#ElementalInference.Paginator.ListScheduleActions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#listscheduleactionspaginator)
        """

if TYPE_CHECKING:
    _SearchFixturesPaginatorBase = Paginator[SearchFixturesResponseTypeDef]
else:
    _SearchFixturesPaginatorBase = Paginator  # type: ignore[assignment]

class SearchFixturesPaginator(_SearchFixturesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/SearchFixtures.html#ElementalInference.Paginator.SearchFixtures)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#searchfixturespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchFixturesRequestPaginateTypeDef]
    ) -> PageIterator[SearchFixturesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elementalinference/paginator/SearchFixtures.html#ElementalInference.Paginator.SearchFixtures.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elementalinference/paginators/#searchfixturespaginator)
        """
