"""
Type annotations for ecs service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ecs.client import ECSClient
    from types_aiobotocore_ecs.paginator import (
        ListAccountSettingsPaginator,
        ListAttributesPaginator,
        ListClustersPaginator,
        ListContainerInstancesPaginator,
        ListServicesByNamespacePaginator,
        ListServicesPaginator,
        ListTaskDefinitionFamiliesPaginator,
        ListTaskDefinitionsPaginator,
        ListTasksPaginator,
    )

    session = get_session()
    with session.create_client("ecs") as client:
        client: ECSClient

        list_account_settings_paginator: ListAccountSettingsPaginator = client.get_paginator("list_account_settings")
        list_attributes_paginator: ListAttributesPaginator = client.get_paginator("list_attributes")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_container_instances_paginator: ListContainerInstancesPaginator = client.get_paginator("list_container_instances")
        list_services_by_namespace_paginator: ListServicesByNamespacePaginator = client.get_paginator("list_services_by_namespace")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
        list_task_definition_families_paginator: ListTaskDefinitionFamiliesPaginator = client.get_paginator("list_task_definition_families")
        list_task_definitions_paginator: ListTaskDefinitionsPaginator = client.get_paginator("list_task_definitions")
        list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAccountSettingsRequestPaginateTypeDef,
    ListAccountSettingsResponseTypeDef,
    ListAttributesRequestPaginateTypeDef,
    ListAttributesResponseTypeDef,
    ListClustersRequestPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListContainerInstancesRequestPaginateTypeDef,
    ListContainerInstancesResponseTypeDef,
    ListServicesByNamespaceRequestPaginateTypeDef,
    ListServicesByNamespaceResponseTypeDef,
    ListServicesRequestPaginateTypeDef,
    ListServicesResponseTypeDef,
    ListTaskDefinitionFamiliesRequestPaginateTypeDef,
    ListTaskDefinitionFamiliesResponseTypeDef,
    ListTaskDefinitionsRequestPaginateTypeDef,
    ListTaskDefinitionsResponseTypeDef,
    ListTasksRequestPaginateTypeDef,
    ListTasksResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAccountSettingsPaginator",
    "ListAttributesPaginator",
    "ListClustersPaginator",
    "ListContainerInstancesPaginator",
    "ListServicesByNamespacePaginator",
    "ListServicesPaginator",
    "ListTaskDefinitionFamiliesPaginator",
    "ListTaskDefinitionsPaginator",
    "ListTasksPaginator",
)


if TYPE_CHECKING:
    _ListAccountSettingsPaginatorBase = AioPaginator[ListAccountSettingsResponseTypeDef]
else:
    _ListAccountSettingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAccountSettingsPaginator(_ListAccountSettingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListAccountSettings.html#ECS.Paginator.ListAccountSettings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listaccountsettingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountSettingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccountSettingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListAccountSettings.html#ECS.Paginator.ListAccountSettings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listaccountsettingspaginator)
        """


if TYPE_CHECKING:
    _ListAttributesPaginatorBase = AioPaginator[ListAttributesResponseTypeDef]
else:
    _ListAttributesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAttributesPaginator(_ListAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListAttributes.html#ECS.Paginator.ListAttributes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listattributespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttributesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListAttributes.html#ECS.Paginator.ListAttributes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listattributespaginator)
        """


if TYPE_CHECKING:
    _ListClustersPaginatorBase = AioPaginator[ListClustersResponseTypeDef]
else:
    _ListClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListClusters.html#ECS.Paginator.ListClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListClusters.html#ECS.Paginator.ListClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listclusterspaginator)
        """


if TYPE_CHECKING:
    _ListContainerInstancesPaginatorBase = AioPaginator[ListContainerInstancesResponseTypeDef]
else:
    _ListContainerInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListContainerInstancesPaginator(_ListContainerInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListContainerInstances.html#ECS.Paginator.ListContainerInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listcontainerinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainerInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContainerInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListContainerInstances.html#ECS.Paginator.ListContainerInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listcontainerinstancespaginator)
        """


if TYPE_CHECKING:
    _ListServicesByNamespacePaginatorBase = AioPaginator[ListServicesByNamespaceResponseTypeDef]
else:
    _ListServicesByNamespacePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServicesByNamespacePaginator(_ListServicesByNamespacePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListServicesByNamespace.html#ECS.Paginator.ListServicesByNamespace)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listservicesbynamespacepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesByNamespaceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServicesByNamespaceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListServicesByNamespace.html#ECS.Paginator.ListServicesByNamespace.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listservicesbynamespacepaginator)
        """


if TYPE_CHECKING:
    _ListServicesPaginatorBase = AioPaginator[ListServicesResponseTypeDef]
else:
    _ListServicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListServices.html#ECS.Paginator.ListServices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listservicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListServices.html#ECS.Paginator.ListServices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listservicespaginator)
        """


if TYPE_CHECKING:
    _ListTaskDefinitionFamiliesPaginatorBase = AioPaginator[
        ListTaskDefinitionFamiliesResponseTypeDef
    ]
else:
    _ListTaskDefinitionFamiliesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTaskDefinitionFamiliesPaginator(_ListTaskDefinitionFamiliesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTaskDefinitionFamilies.html#ECS.Paginator.ListTaskDefinitionFamilies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listtaskdefinitionfamiliespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTaskDefinitionFamiliesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTaskDefinitionFamiliesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTaskDefinitionFamilies.html#ECS.Paginator.ListTaskDefinitionFamilies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listtaskdefinitionfamiliespaginator)
        """


if TYPE_CHECKING:
    _ListTaskDefinitionsPaginatorBase = AioPaginator[ListTaskDefinitionsResponseTypeDef]
else:
    _ListTaskDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTaskDefinitionsPaginator(_ListTaskDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTaskDefinitions.html#ECS.Paginator.ListTaskDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listtaskdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTaskDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTaskDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTaskDefinitions.html#ECS.Paginator.ListTaskDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listtaskdefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListTasksPaginatorBase = AioPaginator[ListTasksResponseTypeDef]
else:
    _ListTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTasksPaginator(_ListTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTasks.html#ECS.Paginator.ListTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs/paginator/ListTasks.html#ECS.Paginator.ListTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecs/paginators/#listtaskspaginator)
        """
