"""
Type annotations for workspaces-instances service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_workspaces_instances.client import WorkspacesInstancesClient
    from types_aiobotocore_workspaces_instances.paginator import (
        ListInstanceTypesPaginator,
        ListRegionsPaginator,
        ListWorkspaceInstancesPaginator,
    )

    session = get_session()
    with session.create_client("workspaces-instances") as client:
        client: WorkspacesInstancesClient

        list_instance_types_paginator: ListInstanceTypesPaginator = client.get_paginator("list_instance_types")
        list_regions_paginator: ListRegionsPaginator = client.get_paginator("list_regions")
        list_workspace_instances_paginator: ListWorkspaceInstancesPaginator = client.get_paginator("list_workspace_instances")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListInstanceTypesRequestPaginateTypeDef,
    ListInstanceTypesResponseTypeDef,
    ListRegionsRequestPaginateTypeDef,
    ListRegionsResponseTypeDef,
    ListWorkspaceInstancesRequestPaginateTypeDef,
    ListWorkspaceInstancesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListInstanceTypesPaginator", "ListRegionsPaginator", "ListWorkspaceInstancesPaginator")


if TYPE_CHECKING:
    _ListInstanceTypesPaginatorBase = AioPaginator[ListInstanceTypesResponseTypeDef]
else:
    _ListInstanceTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInstanceTypesPaginator(_ListInstanceTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/paginator/ListInstanceTypes.html#WorkspacesInstances.Paginator.ListInstanceTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/paginators/#listinstancetypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstanceTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstanceTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/paginator/ListInstanceTypes.html#WorkspacesInstances.Paginator.ListInstanceTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/paginators/#listinstancetypespaginator)
        """


if TYPE_CHECKING:
    _ListRegionsPaginatorBase = AioPaginator[ListRegionsResponseTypeDef]
else:
    _ListRegionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRegionsPaginator(_ListRegionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/paginator/ListRegions.html#WorkspacesInstances.Paginator.ListRegions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/paginators/#listregionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRegionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/paginator/ListRegions.html#WorkspacesInstances.Paginator.ListRegions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/paginators/#listregionspaginator)
        """


if TYPE_CHECKING:
    _ListWorkspaceInstancesPaginatorBase = AioPaginator[ListWorkspaceInstancesResponseTypeDef]
else:
    _ListWorkspaceInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkspaceInstancesPaginator(_ListWorkspaceInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/paginator/ListWorkspaceInstances.html#WorkspacesInstances.Paginator.ListWorkspaceInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/paginators/#listworkspaceinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkspaceInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkspaceInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-instances/paginator/ListWorkspaceInstances.html#WorkspacesInstances.Paginator.ListWorkspaceInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_instances/paginators/#listworkspaceinstancespaginator)
        """
