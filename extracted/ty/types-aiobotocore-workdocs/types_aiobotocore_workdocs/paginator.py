"""
Type annotations for workdocs service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_workdocs.client import WorkDocsClient
    from types_aiobotocore_workdocs.paginator import (
        DescribeActivitiesPaginator,
        DescribeCommentsPaginator,
        DescribeDocumentVersionsPaginator,
        DescribeFolderContentsPaginator,
        DescribeGroupsPaginator,
        DescribeNotificationSubscriptionsPaginator,
        DescribeResourcePermissionsPaginator,
        DescribeRootFoldersPaginator,
        DescribeUsersPaginator,
        SearchResourcesPaginator,
    )

    session = get_session()
    with session.create_client("workdocs") as client:
        client: WorkDocsClient

        describe_activities_paginator: DescribeActivitiesPaginator = client.get_paginator("describe_activities")
        describe_comments_paginator: DescribeCommentsPaginator = client.get_paginator("describe_comments")
        describe_document_versions_paginator: DescribeDocumentVersionsPaginator = client.get_paginator("describe_document_versions")
        describe_folder_contents_paginator: DescribeFolderContentsPaginator = client.get_paginator("describe_folder_contents")
        describe_groups_paginator: DescribeGroupsPaginator = client.get_paginator("describe_groups")
        describe_notification_subscriptions_paginator: DescribeNotificationSubscriptionsPaginator = client.get_paginator("describe_notification_subscriptions")
        describe_resource_permissions_paginator: DescribeResourcePermissionsPaginator = client.get_paginator("describe_resource_permissions")
        describe_root_folders_paginator: DescribeRootFoldersPaginator = client.get_paginator("describe_root_folders")
        describe_users_paginator: DescribeUsersPaginator = client.get_paginator("describe_users")
        search_resources_paginator: SearchResourcesPaginator = client.get_paginator("search_resources")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeActivitiesRequestPaginateTypeDef,
    DescribeActivitiesResponseTypeDef,
    DescribeCommentsRequestPaginateTypeDef,
    DescribeCommentsResponseTypeDef,
    DescribeDocumentVersionsRequestPaginateTypeDef,
    DescribeDocumentVersionsResponseTypeDef,
    DescribeFolderContentsRequestPaginateTypeDef,
    DescribeFolderContentsResponseTypeDef,
    DescribeGroupsRequestPaginateTypeDef,
    DescribeGroupsResponseTypeDef,
    DescribeNotificationSubscriptionsRequestPaginateTypeDef,
    DescribeNotificationSubscriptionsResponseTypeDef,
    DescribeResourcePermissionsRequestPaginateTypeDef,
    DescribeResourcePermissionsResponseTypeDef,
    DescribeRootFoldersRequestPaginateTypeDef,
    DescribeRootFoldersResponseTypeDef,
    DescribeUsersRequestPaginateTypeDef,
    DescribeUsersResponseTypeDef,
    SearchResourcesRequestPaginateTypeDef,
    SearchResourcesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeActivitiesPaginator",
    "DescribeCommentsPaginator",
    "DescribeDocumentVersionsPaginator",
    "DescribeFolderContentsPaginator",
    "DescribeGroupsPaginator",
    "DescribeNotificationSubscriptionsPaginator",
    "DescribeResourcePermissionsPaginator",
    "DescribeRootFoldersPaginator",
    "DescribeUsersPaginator",
    "SearchResourcesPaginator",
)


if TYPE_CHECKING:
    _DescribeActivitiesPaginatorBase = AioPaginator[DescribeActivitiesResponseTypeDef]
else:
    _DescribeActivitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeActivitiesPaginator(_DescribeActivitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeActivities.html#WorkDocs.Paginator.DescribeActivities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeactivitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeActivitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeActivitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeActivities.html#WorkDocs.Paginator.DescribeActivities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeactivitiespaginator)
        """


if TYPE_CHECKING:
    _DescribeCommentsPaginatorBase = AioPaginator[DescribeCommentsResponseTypeDef]
else:
    _DescribeCommentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeCommentsPaginator(_DescribeCommentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeComments.html#WorkDocs.Paginator.DescribeComments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describecommentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCommentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeCommentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeComments.html#WorkDocs.Paginator.DescribeComments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describecommentspaginator)
        """


if TYPE_CHECKING:
    _DescribeDocumentVersionsPaginatorBase = AioPaginator[DescribeDocumentVersionsResponseTypeDef]
else:
    _DescribeDocumentVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDocumentVersionsPaginator(_DescribeDocumentVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeDocumentVersions.html#WorkDocs.Paginator.DescribeDocumentVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describedocumentversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDocumentVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDocumentVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeDocumentVersions.html#WorkDocs.Paginator.DescribeDocumentVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describedocumentversionspaginator)
        """


if TYPE_CHECKING:
    _DescribeFolderContentsPaginatorBase = AioPaginator[DescribeFolderContentsResponseTypeDef]
else:
    _DescribeFolderContentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeFolderContentsPaginator(_DescribeFolderContentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeFolderContents.html#WorkDocs.Paginator.DescribeFolderContents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describefoldercontentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFolderContentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeFolderContentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeFolderContents.html#WorkDocs.Paginator.DescribeFolderContents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describefoldercontentspaginator)
        """


if TYPE_CHECKING:
    _DescribeGroupsPaginatorBase = AioPaginator[DescribeGroupsResponseTypeDef]
else:
    _DescribeGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeGroupsPaginator(_DescribeGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeGroups.html#WorkDocs.Paginator.DescribeGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeGroups.html#WorkDocs.Paginator.DescribeGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describegroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeNotificationSubscriptionsPaginatorBase = AioPaginator[
        DescribeNotificationSubscriptionsResponseTypeDef
    ]
else:
    _DescribeNotificationSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeNotificationSubscriptionsPaginator(_DescribeNotificationSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeNotificationSubscriptions.html#WorkDocs.Paginator.DescribeNotificationSubscriptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describenotificationsubscriptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNotificationSubscriptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeNotificationSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeNotificationSubscriptions.html#WorkDocs.Paginator.DescribeNotificationSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describenotificationsubscriptionspaginator)
        """


if TYPE_CHECKING:
    _DescribeResourcePermissionsPaginatorBase = AioPaginator[
        DescribeResourcePermissionsResponseTypeDef
    ]
else:
    _DescribeResourcePermissionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeResourcePermissionsPaginator(_DescribeResourcePermissionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeResourcePermissions.html#WorkDocs.Paginator.DescribeResourcePermissions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeresourcepermissionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeResourcePermissionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeResourcePermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeResourcePermissions.html#WorkDocs.Paginator.DescribeResourcePermissions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeresourcepermissionspaginator)
        """


if TYPE_CHECKING:
    _DescribeRootFoldersPaginatorBase = AioPaginator[DescribeRootFoldersResponseTypeDef]
else:
    _DescribeRootFoldersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRootFoldersPaginator(_DescribeRootFoldersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeRootFolders.html#WorkDocs.Paginator.DescribeRootFolders)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describerootfolderspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRootFoldersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRootFoldersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeRootFolders.html#WorkDocs.Paginator.DescribeRootFolders.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describerootfolderspaginator)
        """


if TYPE_CHECKING:
    _DescribeUsersPaginatorBase = AioPaginator[DescribeUsersResponseTypeDef]
else:
    _DescribeUsersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeUsersPaginator(_DescribeUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeUsers.html#WorkDocs.Paginator.DescribeUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeuserspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/DescribeUsers.html#WorkDocs.Paginator.DescribeUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#describeuserspaginator)
        """


if TYPE_CHECKING:
    _SearchResourcesPaginatorBase = AioPaginator[SearchResourcesResponseTypeDef]
else:
    _SearchResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchResourcesPaginator(_SearchResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/SearchResources.html#WorkDocs.Paginator.SearchResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#searchresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs/paginator/SearchResources.html#WorkDocs.Paginator.SearchResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/paginators/#searchresourcespaginator)
        """
