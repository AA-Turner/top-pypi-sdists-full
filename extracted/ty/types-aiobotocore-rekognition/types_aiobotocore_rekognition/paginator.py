"""
Type annotations for rekognition service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rekognition.client import RekognitionClient
    from types_aiobotocore_rekognition.paginator import (
        DescribeProjectVersionsPaginator,
        DescribeProjectsPaginator,
        ListCollectionsPaginator,
        ListDatasetEntriesPaginator,
        ListDatasetLabelsPaginator,
        ListFacesPaginator,
        ListProjectPoliciesPaginator,
        ListStreamProcessorsPaginator,
        ListUsersPaginator,
    )

    session = get_session()
    with session.create_client("rekognition") as client:
        client: RekognitionClient

        describe_project_versions_paginator: DescribeProjectVersionsPaginator = client.get_paginator("describe_project_versions")
        describe_projects_paginator: DescribeProjectsPaginator = client.get_paginator("describe_projects")
        list_collections_paginator: ListCollectionsPaginator = client.get_paginator("list_collections")
        list_dataset_entries_paginator: ListDatasetEntriesPaginator = client.get_paginator("list_dataset_entries")
        list_dataset_labels_paginator: ListDatasetLabelsPaginator = client.get_paginator("list_dataset_labels")
        list_faces_paginator: ListFacesPaginator = client.get_paginator("list_faces")
        list_project_policies_paginator: ListProjectPoliciesPaginator = client.get_paginator("list_project_policies")
        list_stream_processors_paginator: ListStreamProcessorsPaginator = client.get_paginator("list_stream_processors")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeProjectsRequestPaginateTypeDef,
    DescribeProjectsResponseTypeDef,
    DescribeProjectVersionsRequestPaginateTypeDef,
    DescribeProjectVersionsResponseTypeDef,
    ListCollectionsRequestPaginateTypeDef,
    ListCollectionsResponseTypeDef,
    ListDatasetEntriesRequestPaginateTypeDef,
    ListDatasetEntriesResponseTypeDef,
    ListDatasetLabelsRequestPaginateTypeDef,
    ListDatasetLabelsResponseTypeDef,
    ListFacesRequestPaginateTypeDef,
    ListFacesResponseTypeDef,
    ListProjectPoliciesRequestPaginateTypeDef,
    ListProjectPoliciesResponseTypeDef,
    ListStreamProcessorsRequestPaginateTypeDef,
    ListStreamProcessorsResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeProjectVersionsPaginator",
    "DescribeProjectsPaginator",
    "ListCollectionsPaginator",
    "ListDatasetEntriesPaginator",
    "ListDatasetLabelsPaginator",
    "ListFacesPaginator",
    "ListProjectPoliciesPaginator",
    "ListStreamProcessorsPaginator",
    "ListUsersPaginator",
)


if TYPE_CHECKING:
    _DescribeProjectVersionsPaginatorBase = AioPaginator[DescribeProjectVersionsResponseTypeDef]
else:
    _DescribeProjectVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeProjectVersionsPaginator(_DescribeProjectVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjectVersions.html#Rekognition.Paginator.DescribeProjectVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeProjectVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeProjectVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjectVersions.html#Rekognition.Paginator.DescribeProjectVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectversionspaginator)
        """


if TYPE_CHECKING:
    _DescribeProjectsPaginatorBase = AioPaginator[DescribeProjectsResponseTypeDef]
else:
    _DescribeProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeProjectsPaginator(_DescribeProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjects.html#Rekognition.Paginator.DescribeProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeProjectsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/DescribeProjects.html#Rekognition.Paginator.DescribeProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#describeprojectspaginator)
        """


if TYPE_CHECKING:
    _ListCollectionsPaginatorBase = AioPaginator[ListCollectionsResponseTypeDef]
else:
    _ListCollectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCollectionsPaginator(_ListCollectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListCollections.html#Rekognition.Paginator.ListCollections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listcollectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollectionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListCollections.html#Rekognition.Paginator.ListCollections.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listcollectionspaginator)
        """


if TYPE_CHECKING:
    _ListDatasetEntriesPaginatorBase = AioPaginator[ListDatasetEntriesResponseTypeDef]
else:
    _ListDatasetEntriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDatasetEntriesPaginator(_ListDatasetEntriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetEntries.html#Rekognition.Paginator.ListDatasetEntries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetentriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetEntriesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetEntriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetEntries.html#Rekognition.Paginator.ListDatasetEntries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetentriespaginator)
        """


if TYPE_CHECKING:
    _ListDatasetLabelsPaginatorBase = AioPaginator[ListDatasetLabelsResponseTypeDef]
else:
    _ListDatasetLabelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDatasetLabelsPaginator(_ListDatasetLabelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetLabels.html#Rekognition.Paginator.ListDatasetLabels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetlabelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetLabelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetLabelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListDatasetLabels.html#Rekognition.Paginator.ListDatasetLabels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listdatasetlabelspaginator)
        """


if TYPE_CHECKING:
    _ListFacesPaginatorBase = AioPaginator[ListFacesResponseTypeDef]
else:
    _ListFacesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFacesPaginator(_ListFacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListFaces.html#Rekognition.Paginator.ListFaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listfacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListFaces.html#Rekognition.Paginator.ListFaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listfacespaginator)
        """


if TYPE_CHECKING:
    _ListProjectPoliciesPaginatorBase = AioPaginator[ListProjectPoliciesResponseTypeDef]
else:
    _ListProjectPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProjectPoliciesPaginator(_ListProjectPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListProjectPolicies.html#Rekognition.Paginator.ListProjectPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listprojectpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProjectPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListProjectPolicies.html#Rekognition.Paginator.ListProjectPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listprojectpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListStreamProcessorsPaginatorBase = AioPaginator[ListStreamProcessorsResponseTypeDef]
else:
    _ListStreamProcessorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStreamProcessorsPaginator(_ListStreamProcessorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListStreamProcessors.html#Rekognition.Paginator.ListStreamProcessors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#liststreamprocessorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamProcessorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStreamProcessorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListStreamProcessors.html#Rekognition.Paginator.ListStreamProcessors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#liststreamprocessorspaginator)
        """


if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListUsers.html#Rekognition.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listuserspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/paginator/ListUsers.html#Rekognition.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/paginators/#listuserspaginator)
        """
