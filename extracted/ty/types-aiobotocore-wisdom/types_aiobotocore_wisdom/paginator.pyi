"""
Type annotations for wisdom service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_wisdom.client import ConnectWisdomServiceClient
    from types_aiobotocore_wisdom.paginator import (
        ListAssistantAssociationsPaginator,
        ListAssistantsPaginator,
        ListContentsPaginator,
        ListImportJobsPaginator,
        ListKnowledgeBasesPaginator,
        ListQuickResponsesPaginator,
        QueryAssistantPaginator,
        SearchContentPaginator,
        SearchQuickResponsesPaginator,
        SearchSessionsPaginator,
    )

    session = get_session()
    with session.create_client("wisdom") as client:
        client: ConnectWisdomServiceClient

        list_assistant_associations_paginator: ListAssistantAssociationsPaginator = client.get_paginator("list_assistant_associations")
        list_assistants_paginator: ListAssistantsPaginator = client.get_paginator("list_assistants")
        list_contents_paginator: ListContentsPaginator = client.get_paginator("list_contents")
        list_import_jobs_paginator: ListImportJobsPaginator = client.get_paginator("list_import_jobs")
        list_knowledge_bases_paginator: ListKnowledgeBasesPaginator = client.get_paginator("list_knowledge_bases")
        list_quick_responses_paginator: ListQuickResponsesPaginator = client.get_paginator("list_quick_responses")
        query_assistant_paginator: QueryAssistantPaginator = client.get_paginator("query_assistant")
        search_content_paginator: SearchContentPaginator = client.get_paginator("search_content")
        search_quick_responses_paginator: SearchQuickResponsesPaginator = client.get_paginator("search_quick_responses")
        search_sessions_paginator: SearchSessionsPaginator = client.get_paginator("search_sessions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAssistantAssociationsRequestPaginateTypeDef,
    ListAssistantAssociationsResponseTypeDef,
    ListAssistantsRequestPaginateTypeDef,
    ListAssistantsResponseTypeDef,
    ListContentsRequestPaginateTypeDef,
    ListContentsResponseTypeDef,
    ListImportJobsRequestPaginateTypeDef,
    ListImportJobsResponseTypeDef,
    ListKnowledgeBasesRequestPaginateTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListQuickResponsesRequestPaginateTypeDef,
    ListQuickResponsesResponseTypeDef,
    QueryAssistantRequestPaginateTypeDef,
    QueryAssistantResponseTypeDef,
    SearchContentRequestPaginateTypeDef,
    SearchContentResponseTypeDef,
    SearchQuickResponsesRequestPaginateTypeDef,
    SearchQuickResponsesResponseTypeDef,
    SearchSessionsRequestPaginateTypeDef,
    SearchSessionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssistantAssociationsPaginator",
    "ListAssistantsPaginator",
    "ListContentsPaginator",
    "ListImportJobsPaginator",
    "ListKnowledgeBasesPaginator",
    "ListQuickResponsesPaginator",
    "QueryAssistantPaginator",
    "SearchContentPaginator",
    "SearchQuickResponsesPaginator",
    "SearchSessionsPaginator",
)

if TYPE_CHECKING:
    _ListAssistantAssociationsPaginatorBase = AioPaginator[ListAssistantAssociationsResponseTypeDef]
else:
    _ListAssistantAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssistantAssociationsPaginator(_ListAssistantAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListAssistantAssociations.html#ConnectWisdomService.Paginator.ListAssistantAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listassistantassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssistantAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssistantAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListAssistantAssociations.html#ConnectWisdomService.Paginator.ListAssistantAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listassistantassociationspaginator)
        """

if TYPE_CHECKING:
    _ListAssistantsPaginatorBase = AioPaginator[ListAssistantsResponseTypeDef]
else:
    _ListAssistantsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssistantsPaginator(_ListAssistantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListAssistants.html#ConnectWisdomService.Paginator.ListAssistants)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listassistantspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssistantsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssistantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListAssistants.html#ConnectWisdomService.Paginator.ListAssistants.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listassistantspaginator)
        """

if TYPE_CHECKING:
    _ListContentsPaginatorBase = AioPaginator[ListContentsResponseTypeDef]
else:
    _ListContentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContentsPaginator(_ListContentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListContents.html#ConnectWisdomService.Paginator.ListContents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listcontentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListContents.html#ConnectWisdomService.Paginator.ListContents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listcontentspaginator)
        """

if TYPE_CHECKING:
    _ListImportJobsPaginatorBase = AioPaginator[ListImportJobsResponseTypeDef]
else:
    _ListImportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImportJobsPaginator(_ListImportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListImportJobs.html#ConnectWisdomService.Paginator.ListImportJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listimportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListImportJobs.html#ConnectWisdomService.Paginator.ListImportJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listimportjobspaginator)
        """

if TYPE_CHECKING:
    _ListKnowledgeBasesPaginatorBase = AioPaginator[ListKnowledgeBasesResponseTypeDef]
else:
    _ListKnowledgeBasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListKnowledgeBasesPaginator(_ListKnowledgeBasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListKnowledgeBases.html#ConnectWisdomService.Paginator.ListKnowledgeBases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listknowledgebasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKnowledgeBasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKnowledgeBasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListKnowledgeBases.html#ConnectWisdomService.Paginator.ListKnowledgeBases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listknowledgebasespaginator)
        """

if TYPE_CHECKING:
    _ListQuickResponsesPaginatorBase = AioPaginator[ListQuickResponsesResponseTypeDef]
else:
    _ListQuickResponsesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListQuickResponsesPaginator(_ListQuickResponsesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListQuickResponses.html#ConnectWisdomService.Paginator.ListQuickResponses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listquickresponsespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQuickResponsesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQuickResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/ListQuickResponses.html#ConnectWisdomService.Paginator.ListQuickResponses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#listquickresponsespaginator)
        """

if TYPE_CHECKING:
    _QueryAssistantPaginatorBase = AioPaginator[QueryAssistantResponseTypeDef]
else:
    _QueryAssistantPaginatorBase = AioPaginator  # type: ignore[assignment]

class QueryAssistantPaginator(_QueryAssistantPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/QueryAssistant.html#ConnectWisdomService.Paginator.QueryAssistant)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#queryassistantpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[QueryAssistantRequestPaginateTypeDef]
    ) -> AioPageIterator[QueryAssistantResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/QueryAssistant.html#ConnectWisdomService.Paginator.QueryAssistant.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#queryassistantpaginator)
        """

if TYPE_CHECKING:
    _SearchContentPaginatorBase = AioPaginator[SearchContentResponseTypeDef]
else:
    _SearchContentPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchContentPaginator(_SearchContentPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchContent.html#ConnectWisdomService.Paginator.SearchContent)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#searchcontentpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchContentRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchContentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchContent.html#ConnectWisdomService.Paginator.SearchContent.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#searchcontentpaginator)
        """

if TYPE_CHECKING:
    _SearchQuickResponsesPaginatorBase = AioPaginator[SearchQuickResponsesResponseTypeDef]
else:
    _SearchQuickResponsesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchQuickResponsesPaginator(_SearchQuickResponsesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchQuickResponses.html#ConnectWisdomService.Paginator.SearchQuickResponses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#searchquickresponsespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchQuickResponsesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchQuickResponsesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchQuickResponses.html#ConnectWisdomService.Paginator.SearchQuickResponses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#searchquickresponsespaginator)
        """

if TYPE_CHECKING:
    _SearchSessionsPaginatorBase = AioPaginator[SearchSessionsResponseTypeDef]
else:
    _SearchSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchSessionsPaginator(_SearchSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchSessions.html#ConnectWisdomService.Paginator.SearchSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#searchsessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchSessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wisdom/paginator/SearchSessions.html#ConnectWisdomService.Paginator.SearchSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wisdom/paginators/#searchsessionspaginator)
        """
