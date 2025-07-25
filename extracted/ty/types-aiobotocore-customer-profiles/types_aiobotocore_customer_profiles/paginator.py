"""
Type annotations for customer-profiles service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_customer_profiles.client import CustomerProfilesClient
    from types_aiobotocore_customer_profiles.paginator import (
        GetSimilarProfilesPaginator,
        ListDomainLayoutsPaginator,
        ListEventStreamsPaginator,
        ListEventTriggersPaginator,
        ListObjectTypeAttributesPaginator,
        ListRuleBasedMatchesPaginator,
        ListSegmentDefinitionsPaginator,
        ListUploadJobsPaginator,
    )

    session = get_session()
    with session.create_client("customer-profiles") as client:
        client: CustomerProfilesClient

        get_similar_profiles_paginator: GetSimilarProfilesPaginator = client.get_paginator("get_similar_profiles")
        list_domain_layouts_paginator: ListDomainLayoutsPaginator = client.get_paginator("list_domain_layouts")
        list_event_streams_paginator: ListEventStreamsPaginator = client.get_paginator("list_event_streams")
        list_event_triggers_paginator: ListEventTriggersPaginator = client.get_paginator("list_event_triggers")
        list_object_type_attributes_paginator: ListObjectTypeAttributesPaginator = client.get_paginator("list_object_type_attributes")
        list_rule_based_matches_paginator: ListRuleBasedMatchesPaginator = client.get_paginator("list_rule_based_matches")
        list_segment_definitions_paginator: ListSegmentDefinitionsPaginator = client.get_paginator("list_segment_definitions")
        list_upload_jobs_paginator: ListUploadJobsPaginator = client.get_paginator("list_upload_jobs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetSimilarProfilesRequestPaginateTypeDef,
    GetSimilarProfilesResponseTypeDef,
    ListDomainLayoutsRequestPaginateTypeDef,
    ListDomainLayoutsResponseTypeDef,
    ListEventStreamsRequestPaginateTypeDef,
    ListEventStreamsResponseTypeDef,
    ListEventTriggersRequestPaginateTypeDef,
    ListEventTriggersResponseTypeDef,
    ListObjectTypeAttributesRequestPaginateTypeDef,
    ListObjectTypeAttributesResponseTypeDef,
    ListRuleBasedMatchesRequestPaginateTypeDef,
    ListRuleBasedMatchesResponseTypeDef,
    ListSegmentDefinitionsRequestPaginateTypeDef,
    ListSegmentDefinitionsResponseTypeDef,
    ListUploadJobsRequestPaginateTypeDef,
    ListUploadJobsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetSimilarProfilesPaginator",
    "ListDomainLayoutsPaginator",
    "ListEventStreamsPaginator",
    "ListEventTriggersPaginator",
    "ListObjectTypeAttributesPaginator",
    "ListRuleBasedMatchesPaginator",
    "ListSegmentDefinitionsPaginator",
    "ListUploadJobsPaginator",
)


if TYPE_CHECKING:
    _GetSimilarProfilesPaginatorBase = AioPaginator[GetSimilarProfilesResponseTypeDef]
else:
    _GetSimilarProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetSimilarProfilesPaginator(_GetSimilarProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/GetSimilarProfiles.html#CustomerProfiles.Paginator.GetSimilarProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#getsimilarprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetSimilarProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetSimilarProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/GetSimilarProfiles.html#CustomerProfiles.Paginator.GetSimilarProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#getsimilarprofilespaginator)
        """


if TYPE_CHECKING:
    _ListDomainLayoutsPaginatorBase = AioPaginator[ListDomainLayoutsResponseTypeDef]
else:
    _ListDomainLayoutsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDomainLayoutsPaginator(_ListDomainLayoutsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListDomainLayouts.html#CustomerProfiles.Paginator.ListDomainLayouts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listdomainlayoutspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainLayoutsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainLayoutsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListDomainLayouts.html#CustomerProfiles.Paginator.ListDomainLayouts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listdomainlayoutspaginator)
        """


if TYPE_CHECKING:
    _ListEventStreamsPaginatorBase = AioPaginator[ListEventStreamsResponseTypeDef]
else:
    _ListEventStreamsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventStreamsPaginator(_ListEventStreamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListEventStreams.html#CustomerProfiles.Paginator.ListEventStreams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listeventstreamspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventStreamsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListEventStreams.html#CustomerProfiles.Paginator.ListEventStreams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listeventstreamspaginator)
        """


if TYPE_CHECKING:
    _ListEventTriggersPaginatorBase = AioPaginator[ListEventTriggersResponseTypeDef]
else:
    _ListEventTriggersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventTriggersPaginator(_ListEventTriggersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListEventTriggers.html#CustomerProfiles.Paginator.ListEventTriggers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listeventtriggerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventTriggersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventTriggersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListEventTriggers.html#CustomerProfiles.Paginator.ListEventTriggers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listeventtriggerspaginator)
        """


if TYPE_CHECKING:
    _ListObjectTypeAttributesPaginatorBase = AioPaginator[ListObjectTypeAttributesResponseTypeDef]
else:
    _ListObjectTypeAttributesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListObjectTypeAttributesPaginator(_ListObjectTypeAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListObjectTypeAttributes.html#CustomerProfiles.Paginator.ListObjectTypeAttributes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listobjecttypeattributespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListObjectTypeAttributesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListObjectTypeAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListObjectTypeAttributes.html#CustomerProfiles.Paginator.ListObjectTypeAttributes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listobjecttypeattributespaginator)
        """


if TYPE_CHECKING:
    _ListRuleBasedMatchesPaginatorBase = AioPaginator[ListRuleBasedMatchesResponseTypeDef]
else:
    _ListRuleBasedMatchesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRuleBasedMatchesPaginator(_ListRuleBasedMatchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListRuleBasedMatches.html#CustomerProfiles.Paginator.ListRuleBasedMatches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listrulebasedmatchespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuleBasedMatchesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRuleBasedMatchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListRuleBasedMatches.html#CustomerProfiles.Paginator.ListRuleBasedMatches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listrulebasedmatchespaginator)
        """


if TYPE_CHECKING:
    _ListSegmentDefinitionsPaginatorBase = AioPaginator[ListSegmentDefinitionsResponseTypeDef]
else:
    _ListSegmentDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSegmentDefinitionsPaginator(_ListSegmentDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListSegmentDefinitions.html#CustomerProfiles.Paginator.ListSegmentDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listsegmentdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSegmentDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSegmentDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListSegmentDefinitions.html#CustomerProfiles.Paginator.ListSegmentDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listsegmentdefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListUploadJobsPaginatorBase = AioPaginator[ListUploadJobsResponseTypeDef]
else:
    _ListUploadJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUploadJobsPaginator(_ListUploadJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListUploadJobs.html#CustomerProfiles.Paginator.ListUploadJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listuploadjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUploadJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUploadJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/customer-profiles/paginator/ListUploadJobs.html#CustomerProfiles.Paginator.ListUploadJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/paginators/#listuploadjobspaginator)
        """
