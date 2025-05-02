"""
Type annotations for workspaces service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_workspaces.client import WorkSpacesClient
    from types_aiobotocore_workspaces.paginator import (
        DescribeAccountModificationsPaginator,
        DescribeIpGroupsPaginator,
        DescribeWorkspaceBundlesPaginator,
        DescribeWorkspaceDirectoriesPaginator,
        DescribeWorkspaceImagesPaginator,
        DescribeWorkspacesConnectionStatusPaginator,
        DescribeWorkspacesPaginator,
        ListAccountLinksPaginator,
        ListAvailableManagementCidrRangesPaginator,
    )

    session = get_session()
    with session.create_client("workspaces") as client:
        client: WorkSpacesClient

        describe_account_modifications_paginator: DescribeAccountModificationsPaginator = client.get_paginator("describe_account_modifications")
        describe_ip_groups_paginator: DescribeIpGroupsPaginator = client.get_paginator("describe_ip_groups")
        describe_workspace_bundles_paginator: DescribeWorkspaceBundlesPaginator = client.get_paginator("describe_workspace_bundles")
        describe_workspace_directories_paginator: DescribeWorkspaceDirectoriesPaginator = client.get_paginator("describe_workspace_directories")
        describe_workspace_images_paginator: DescribeWorkspaceImagesPaginator = client.get_paginator("describe_workspace_images")
        describe_workspaces_connection_status_paginator: DescribeWorkspacesConnectionStatusPaginator = client.get_paginator("describe_workspaces_connection_status")
        describe_workspaces_paginator: DescribeWorkspacesPaginator = client.get_paginator("describe_workspaces")
        list_account_links_paginator: ListAccountLinksPaginator = client.get_paginator("list_account_links")
        list_available_management_cidr_ranges_paginator: ListAvailableManagementCidrRangesPaginator = client.get_paginator("list_available_management_cidr_ranges")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAccountModificationsRequestPaginateTypeDef,
    DescribeAccountModificationsResultTypeDef,
    DescribeIpGroupsRequestPaginateTypeDef,
    DescribeIpGroupsResultTypeDef,
    DescribeWorkspaceBundlesRequestPaginateTypeDef,
    DescribeWorkspaceBundlesResultTypeDef,
    DescribeWorkspaceDirectoriesRequestPaginateTypeDef,
    DescribeWorkspaceDirectoriesResultTypeDef,
    DescribeWorkspaceImagesRequestPaginateTypeDef,
    DescribeWorkspaceImagesResultTypeDef,
    DescribeWorkspacesConnectionStatusRequestPaginateTypeDef,
    DescribeWorkspacesConnectionStatusResultTypeDef,
    DescribeWorkspacesRequestPaginateTypeDef,
    DescribeWorkspacesResultTypeDef,
    ListAccountLinksRequestPaginateTypeDef,
    ListAccountLinksResultTypeDef,
    ListAvailableManagementCidrRangesRequestPaginateTypeDef,
    ListAvailableManagementCidrRangesResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAccountModificationsPaginator",
    "DescribeIpGroupsPaginator",
    "DescribeWorkspaceBundlesPaginator",
    "DescribeWorkspaceDirectoriesPaginator",
    "DescribeWorkspaceImagesPaginator",
    "DescribeWorkspacesConnectionStatusPaginator",
    "DescribeWorkspacesPaginator",
    "ListAccountLinksPaginator",
    "ListAvailableManagementCidrRangesPaginator",
)


if TYPE_CHECKING:
    _DescribeAccountModificationsPaginatorBase = AioPaginator[
        DescribeAccountModificationsResultTypeDef
    ]
else:
    _DescribeAccountModificationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAccountModificationsPaginator(_DescribeAccountModificationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeAccountModifications.html#WorkSpaces.Paginator.DescribeAccountModifications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeaccountmodificationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAccountModificationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAccountModificationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeAccountModifications.html#WorkSpaces.Paginator.DescribeAccountModifications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeaccountmodificationspaginator)
        """


if TYPE_CHECKING:
    _DescribeIpGroupsPaginatorBase = AioPaginator[DescribeIpGroupsResultTypeDef]
else:
    _DescribeIpGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeIpGroupsPaginator(_DescribeIpGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeIpGroups.html#WorkSpaces.Paginator.DescribeIpGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeipgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeIpGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeIpGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeIpGroups.html#WorkSpaces.Paginator.DescribeIpGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeipgroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeWorkspaceBundlesPaginatorBase = AioPaginator[DescribeWorkspaceBundlesResultTypeDef]
else:
    _DescribeWorkspaceBundlesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeWorkspaceBundlesPaginator(_DescribeWorkspaceBundlesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceBundles.html#WorkSpaces.Paginator.DescribeWorkspaceBundles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspacebundlespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeWorkspaceBundlesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeWorkspaceBundlesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceBundles.html#WorkSpaces.Paginator.DescribeWorkspaceBundles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspacebundlespaginator)
        """


if TYPE_CHECKING:
    _DescribeWorkspaceDirectoriesPaginatorBase = AioPaginator[
        DescribeWorkspaceDirectoriesResultTypeDef
    ]
else:
    _DescribeWorkspaceDirectoriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeWorkspaceDirectoriesPaginator(_DescribeWorkspaceDirectoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceDirectories.html#WorkSpaces.Paginator.DescribeWorkspaceDirectories)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspacedirectoriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeWorkspaceDirectoriesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeWorkspaceDirectoriesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceDirectories.html#WorkSpaces.Paginator.DescribeWorkspaceDirectories.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspacedirectoriespaginator)
        """


if TYPE_CHECKING:
    _DescribeWorkspaceImagesPaginatorBase = AioPaginator[DescribeWorkspaceImagesResultTypeDef]
else:
    _DescribeWorkspaceImagesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeWorkspaceImagesPaginator(_DescribeWorkspaceImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceImages.html#WorkSpaces.Paginator.DescribeWorkspaceImages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspaceimagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeWorkspaceImagesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeWorkspaceImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaceImages.html#WorkSpaces.Paginator.DescribeWorkspaceImages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspaceimagespaginator)
        """


if TYPE_CHECKING:
    _DescribeWorkspacesConnectionStatusPaginatorBase = AioPaginator[
        DescribeWorkspacesConnectionStatusResultTypeDef
    ]
else:
    _DescribeWorkspacesConnectionStatusPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeWorkspacesConnectionStatusPaginator(_DescribeWorkspacesConnectionStatusPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspacesConnectionStatus.html#WorkSpaces.Paginator.DescribeWorkspacesConnectionStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspacesconnectionstatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeWorkspacesConnectionStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeWorkspacesConnectionStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspacesConnectionStatus.html#WorkSpaces.Paginator.DescribeWorkspacesConnectionStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspacesconnectionstatuspaginator)
        """


if TYPE_CHECKING:
    _DescribeWorkspacesPaginatorBase = AioPaginator[DescribeWorkspacesResultTypeDef]
else:
    _DescribeWorkspacesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeWorkspacesPaginator(_DescribeWorkspacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaces.html#WorkSpaces.Paginator.DescribeWorkspaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeWorkspacesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeWorkspacesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/DescribeWorkspaces.html#WorkSpaces.Paginator.DescribeWorkspaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#describeworkspacespaginator)
        """


if TYPE_CHECKING:
    _ListAccountLinksPaginatorBase = AioPaginator[ListAccountLinksResultTypeDef]
else:
    _ListAccountLinksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAccountLinksPaginator(_ListAccountLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/ListAccountLinks.html#WorkSpaces.Paginator.ListAccountLinks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#listaccountlinkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountLinksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccountLinksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/ListAccountLinks.html#WorkSpaces.Paginator.ListAccountLinks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#listaccountlinkspaginator)
        """


if TYPE_CHECKING:
    _ListAvailableManagementCidrRangesPaginatorBase = AioPaginator[
        ListAvailableManagementCidrRangesResultTypeDef
    ]
else:
    _ListAvailableManagementCidrRangesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAvailableManagementCidrRangesPaginator(_ListAvailableManagementCidrRangesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/ListAvailableManagementCidrRanges.html#WorkSpaces.Paginator.ListAvailableManagementCidrRanges)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#listavailablemanagementcidrrangespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAvailableManagementCidrRangesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAvailableManagementCidrRangesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces/paginator/ListAvailableManagementCidrRanges.html#WorkSpaces.Paginator.ListAvailableManagementCidrRanges.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces/paginators/#listavailablemanagementcidrrangespaginator)
        """
