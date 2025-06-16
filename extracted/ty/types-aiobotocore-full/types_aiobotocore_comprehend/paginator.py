"""
Type annotations for comprehend service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_comprehend.client import ComprehendClient
    from types_aiobotocore_comprehend.paginator import (
        ListDocumentClassificationJobsPaginator,
        ListDocumentClassifiersPaginator,
        ListDominantLanguageDetectionJobsPaginator,
        ListEndpointsPaginator,
        ListEntitiesDetectionJobsPaginator,
        ListEntityRecognizersPaginator,
        ListKeyPhrasesDetectionJobsPaginator,
        ListPiiEntitiesDetectionJobsPaginator,
        ListSentimentDetectionJobsPaginator,
        ListTopicsDetectionJobsPaginator,
    )

    session = get_session()
    with session.create_client("comprehend") as client:
        client: ComprehendClient

        list_document_classification_jobs_paginator: ListDocumentClassificationJobsPaginator = client.get_paginator("list_document_classification_jobs")
        list_document_classifiers_paginator: ListDocumentClassifiersPaginator = client.get_paginator("list_document_classifiers")
        list_dominant_language_detection_jobs_paginator: ListDominantLanguageDetectionJobsPaginator = client.get_paginator("list_dominant_language_detection_jobs")
        list_endpoints_paginator: ListEndpointsPaginator = client.get_paginator("list_endpoints")
        list_entities_detection_jobs_paginator: ListEntitiesDetectionJobsPaginator = client.get_paginator("list_entities_detection_jobs")
        list_entity_recognizers_paginator: ListEntityRecognizersPaginator = client.get_paginator("list_entity_recognizers")
        list_key_phrases_detection_jobs_paginator: ListKeyPhrasesDetectionJobsPaginator = client.get_paginator("list_key_phrases_detection_jobs")
        list_pii_entities_detection_jobs_paginator: ListPiiEntitiesDetectionJobsPaginator = client.get_paginator("list_pii_entities_detection_jobs")
        list_sentiment_detection_jobs_paginator: ListSentimentDetectionJobsPaginator = client.get_paginator("list_sentiment_detection_jobs")
        list_topics_detection_jobs_paginator: ListTopicsDetectionJobsPaginator = client.get_paginator("list_topics_detection_jobs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDocumentClassificationJobsRequestPaginateTypeDef,
    ListDocumentClassificationJobsResponseTypeDef,
    ListDocumentClassifiersRequestPaginateTypeDef,
    ListDocumentClassifiersResponseTypeDef,
    ListDominantLanguageDetectionJobsRequestPaginateTypeDef,
    ListDominantLanguageDetectionJobsResponseTypeDef,
    ListEndpointsRequestPaginateTypeDef,
    ListEndpointsResponseTypeDef,
    ListEntitiesDetectionJobsRequestPaginateTypeDef,
    ListEntitiesDetectionJobsResponseTypeDef,
    ListEntityRecognizersRequestPaginateTypeDef,
    ListEntityRecognizersResponseTypeDef,
    ListKeyPhrasesDetectionJobsRequestPaginateTypeDef,
    ListKeyPhrasesDetectionJobsResponseTypeDef,
    ListPiiEntitiesDetectionJobsRequestPaginateTypeDef,
    ListPiiEntitiesDetectionJobsResponseTypeDef,
    ListSentimentDetectionJobsRequestPaginateTypeDef,
    ListSentimentDetectionJobsResponseTypeDef,
    ListTopicsDetectionJobsRequestPaginateTypeDef,
    ListTopicsDetectionJobsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDocumentClassificationJobsPaginator",
    "ListDocumentClassifiersPaginator",
    "ListDominantLanguageDetectionJobsPaginator",
    "ListEndpointsPaginator",
    "ListEntitiesDetectionJobsPaginator",
    "ListEntityRecognizersPaginator",
    "ListKeyPhrasesDetectionJobsPaginator",
    "ListPiiEntitiesDetectionJobsPaginator",
    "ListSentimentDetectionJobsPaginator",
    "ListTopicsDetectionJobsPaginator",
)


if TYPE_CHECKING:
    _ListDocumentClassificationJobsPaginatorBase = AioPaginator[
        ListDocumentClassificationJobsResponseTypeDef
    ]
else:
    _ListDocumentClassificationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDocumentClassificationJobsPaginator(_ListDocumentClassificationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDocumentClassificationJobs.html#Comprehend.Paginator.ListDocumentClassificationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listdocumentclassificationjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDocumentClassificationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDocumentClassificationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDocumentClassificationJobs.html#Comprehend.Paginator.ListDocumentClassificationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listdocumentclassificationjobspaginator)
        """


if TYPE_CHECKING:
    _ListDocumentClassifiersPaginatorBase = AioPaginator[ListDocumentClassifiersResponseTypeDef]
else:
    _ListDocumentClassifiersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDocumentClassifiersPaginator(_ListDocumentClassifiersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDocumentClassifiers.html#Comprehend.Paginator.ListDocumentClassifiers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listdocumentclassifierspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDocumentClassifiersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDocumentClassifiersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDocumentClassifiers.html#Comprehend.Paginator.ListDocumentClassifiers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listdocumentclassifierspaginator)
        """


if TYPE_CHECKING:
    _ListDominantLanguageDetectionJobsPaginatorBase = AioPaginator[
        ListDominantLanguageDetectionJobsResponseTypeDef
    ]
else:
    _ListDominantLanguageDetectionJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDominantLanguageDetectionJobsPaginator(_ListDominantLanguageDetectionJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDominantLanguageDetectionJobs.html#Comprehend.Paginator.ListDominantLanguageDetectionJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listdominantlanguagedetectionjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDominantLanguageDetectionJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDominantLanguageDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListDominantLanguageDetectionJobs.html#Comprehend.Paginator.ListDominantLanguageDetectionJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listdominantlanguagedetectionjobspaginator)
        """


if TYPE_CHECKING:
    _ListEndpointsPaginatorBase = AioPaginator[ListEndpointsResponseTypeDef]
else:
    _ListEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEndpointsPaginator(_ListEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEndpoints.html#Comprehend.Paginator.ListEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEndpoints.html#Comprehend.Paginator.ListEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listendpointspaginator)
        """


if TYPE_CHECKING:
    _ListEntitiesDetectionJobsPaginatorBase = AioPaginator[ListEntitiesDetectionJobsResponseTypeDef]
else:
    _ListEntitiesDetectionJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEntitiesDetectionJobsPaginator(_ListEntitiesDetectionJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEntitiesDetectionJobs.html#Comprehend.Paginator.ListEntitiesDetectionJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listentitiesdetectionjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEntitiesDetectionJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEntitiesDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEntitiesDetectionJobs.html#Comprehend.Paginator.ListEntitiesDetectionJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listentitiesdetectionjobspaginator)
        """


if TYPE_CHECKING:
    _ListEntityRecognizersPaginatorBase = AioPaginator[ListEntityRecognizersResponseTypeDef]
else:
    _ListEntityRecognizersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEntityRecognizersPaginator(_ListEntityRecognizersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEntityRecognizers.html#Comprehend.Paginator.ListEntityRecognizers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listentityrecognizerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEntityRecognizersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEntityRecognizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListEntityRecognizers.html#Comprehend.Paginator.ListEntityRecognizers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listentityrecognizerspaginator)
        """


if TYPE_CHECKING:
    _ListKeyPhrasesDetectionJobsPaginatorBase = AioPaginator[
        ListKeyPhrasesDetectionJobsResponseTypeDef
    ]
else:
    _ListKeyPhrasesDetectionJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListKeyPhrasesDetectionJobsPaginator(_ListKeyPhrasesDetectionJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListKeyPhrasesDetectionJobs.html#Comprehend.Paginator.ListKeyPhrasesDetectionJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listkeyphrasesdetectionjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKeyPhrasesDetectionJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKeyPhrasesDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListKeyPhrasesDetectionJobs.html#Comprehend.Paginator.ListKeyPhrasesDetectionJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listkeyphrasesdetectionjobspaginator)
        """


if TYPE_CHECKING:
    _ListPiiEntitiesDetectionJobsPaginatorBase = AioPaginator[
        ListPiiEntitiesDetectionJobsResponseTypeDef
    ]
else:
    _ListPiiEntitiesDetectionJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPiiEntitiesDetectionJobsPaginator(_ListPiiEntitiesDetectionJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListPiiEntitiesDetectionJobs.html#Comprehend.Paginator.ListPiiEntitiesDetectionJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listpiientitiesdetectionjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPiiEntitiesDetectionJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPiiEntitiesDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListPiiEntitiesDetectionJobs.html#Comprehend.Paginator.ListPiiEntitiesDetectionJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listpiientitiesdetectionjobspaginator)
        """


if TYPE_CHECKING:
    _ListSentimentDetectionJobsPaginatorBase = AioPaginator[
        ListSentimentDetectionJobsResponseTypeDef
    ]
else:
    _ListSentimentDetectionJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSentimentDetectionJobsPaginator(_ListSentimentDetectionJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListSentimentDetectionJobs.html#Comprehend.Paginator.ListSentimentDetectionJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listsentimentdetectionjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSentimentDetectionJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSentimentDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListSentimentDetectionJobs.html#Comprehend.Paginator.ListSentimentDetectionJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listsentimentdetectionjobspaginator)
        """


if TYPE_CHECKING:
    _ListTopicsDetectionJobsPaginatorBase = AioPaginator[ListTopicsDetectionJobsResponseTypeDef]
else:
    _ListTopicsDetectionJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTopicsDetectionJobsPaginator(_ListTopicsDetectionJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListTopicsDetectionJobs.html#Comprehend.Paginator.ListTopicsDetectionJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listtopicsdetectionjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTopicsDetectionJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTopicsDetectionJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend/paginator/ListTopicsDetectionJobs.html#Comprehend.Paginator.ListTopicsDetectionJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehend/paginators/#listtopicsdetectionjobspaginator)
        """
