"""
Type annotations for greengrass service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_greengrass.client import GreengrassClient
    from types_aiobotocore_greengrass.paginator import (
        ListBulkDeploymentDetailedReportsPaginator,
        ListBulkDeploymentsPaginator,
        ListConnectorDefinitionVersionsPaginator,
        ListConnectorDefinitionsPaginator,
        ListCoreDefinitionVersionsPaginator,
        ListCoreDefinitionsPaginator,
        ListDeploymentsPaginator,
        ListDeviceDefinitionVersionsPaginator,
        ListDeviceDefinitionsPaginator,
        ListFunctionDefinitionVersionsPaginator,
        ListFunctionDefinitionsPaginator,
        ListGroupVersionsPaginator,
        ListGroupsPaginator,
        ListLoggerDefinitionVersionsPaginator,
        ListLoggerDefinitionsPaginator,
        ListResourceDefinitionVersionsPaginator,
        ListResourceDefinitionsPaginator,
        ListSubscriptionDefinitionVersionsPaginator,
        ListSubscriptionDefinitionsPaginator,
    )

    session = get_session()
    with session.create_client("greengrass") as client:
        client: GreengrassClient

        list_bulk_deployment_detailed_reports_paginator: ListBulkDeploymentDetailedReportsPaginator = client.get_paginator("list_bulk_deployment_detailed_reports")
        list_bulk_deployments_paginator: ListBulkDeploymentsPaginator = client.get_paginator("list_bulk_deployments")
        list_connector_definition_versions_paginator: ListConnectorDefinitionVersionsPaginator = client.get_paginator("list_connector_definition_versions")
        list_connector_definitions_paginator: ListConnectorDefinitionsPaginator = client.get_paginator("list_connector_definitions")
        list_core_definition_versions_paginator: ListCoreDefinitionVersionsPaginator = client.get_paginator("list_core_definition_versions")
        list_core_definitions_paginator: ListCoreDefinitionsPaginator = client.get_paginator("list_core_definitions")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_device_definition_versions_paginator: ListDeviceDefinitionVersionsPaginator = client.get_paginator("list_device_definition_versions")
        list_device_definitions_paginator: ListDeviceDefinitionsPaginator = client.get_paginator("list_device_definitions")
        list_function_definition_versions_paginator: ListFunctionDefinitionVersionsPaginator = client.get_paginator("list_function_definition_versions")
        list_function_definitions_paginator: ListFunctionDefinitionsPaginator = client.get_paginator("list_function_definitions")
        list_group_versions_paginator: ListGroupVersionsPaginator = client.get_paginator("list_group_versions")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_logger_definition_versions_paginator: ListLoggerDefinitionVersionsPaginator = client.get_paginator("list_logger_definition_versions")
        list_logger_definitions_paginator: ListLoggerDefinitionsPaginator = client.get_paginator("list_logger_definitions")
        list_resource_definition_versions_paginator: ListResourceDefinitionVersionsPaginator = client.get_paginator("list_resource_definition_versions")
        list_resource_definitions_paginator: ListResourceDefinitionsPaginator = client.get_paginator("list_resource_definitions")
        list_subscription_definition_versions_paginator: ListSubscriptionDefinitionVersionsPaginator = client.get_paginator("list_subscription_definition_versions")
        list_subscription_definitions_paginator: ListSubscriptionDefinitionsPaginator = client.get_paginator("list_subscription_definitions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListBulkDeploymentDetailedReportsRequestPaginateTypeDef,
    ListBulkDeploymentDetailedReportsResponseTypeDef,
    ListBulkDeploymentsRequestPaginateTypeDef,
    ListBulkDeploymentsResponseTypeDef,
    ListConnectorDefinitionsRequestPaginateTypeDef,
    ListConnectorDefinitionsResponseTypeDef,
    ListConnectorDefinitionVersionsRequestPaginateTypeDef,
    ListConnectorDefinitionVersionsResponseTypeDef,
    ListCoreDefinitionsRequestPaginateTypeDef,
    ListCoreDefinitionsResponseTypeDef,
    ListCoreDefinitionVersionsRequestPaginateTypeDef,
    ListCoreDefinitionVersionsResponseTypeDef,
    ListDeploymentsRequestPaginateTypeDef,
    ListDeploymentsResponseTypeDef,
    ListDeviceDefinitionsRequestPaginateTypeDef,
    ListDeviceDefinitionsResponseTypeDef,
    ListDeviceDefinitionVersionsRequestPaginateTypeDef,
    ListDeviceDefinitionVersionsResponseTypeDef,
    ListFunctionDefinitionsRequestPaginateTypeDef,
    ListFunctionDefinitionsResponseTypeDef,
    ListFunctionDefinitionVersionsRequestPaginateTypeDef,
    ListFunctionDefinitionVersionsResponseTypeDef,
    ListGroupsRequestPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListGroupVersionsRequestPaginateTypeDef,
    ListGroupVersionsResponseTypeDef,
    ListLoggerDefinitionsRequestPaginateTypeDef,
    ListLoggerDefinitionsResponseTypeDef,
    ListLoggerDefinitionVersionsRequestPaginateTypeDef,
    ListLoggerDefinitionVersionsResponseTypeDef,
    ListResourceDefinitionsRequestPaginateTypeDef,
    ListResourceDefinitionsResponseTypeDef,
    ListResourceDefinitionVersionsRequestPaginateTypeDef,
    ListResourceDefinitionVersionsResponseTypeDef,
    ListSubscriptionDefinitionsRequestPaginateTypeDef,
    ListSubscriptionDefinitionsResponseTypeDef,
    ListSubscriptionDefinitionVersionsRequestPaginateTypeDef,
    ListSubscriptionDefinitionVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListBulkDeploymentDetailedReportsPaginator",
    "ListBulkDeploymentsPaginator",
    "ListConnectorDefinitionVersionsPaginator",
    "ListConnectorDefinitionsPaginator",
    "ListCoreDefinitionVersionsPaginator",
    "ListCoreDefinitionsPaginator",
    "ListDeploymentsPaginator",
    "ListDeviceDefinitionVersionsPaginator",
    "ListDeviceDefinitionsPaginator",
    "ListFunctionDefinitionVersionsPaginator",
    "ListFunctionDefinitionsPaginator",
    "ListGroupVersionsPaginator",
    "ListGroupsPaginator",
    "ListLoggerDefinitionVersionsPaginator",
    "ListLoggerDefinitionsPaginator",
    "ListResourceDefinitionVersionsPaginator",
    "ListResourceDefinitionsPaginator",
    "ListSubscriptionDefinitionVersionsPaginator",
    "ListSubscriptionDefinitionsPaginator",
)


if TYPE_CHECKING:
    _ListBulkDeploymentDetailedReportsPaginatorBase = AioPaginator[
        ListBulkDeploymentDetailedReportsResponseTypeDef
    ]
else:
    _ListBulkDeploymentDetailedReportsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBulkDeploymentDetailedReportsPaginator(_ListBulkDeploymentDetailedReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListBulkDeploymentDetailedReports.html#Greengrass.Paginator.ListBulkDeploymentDetailedReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listbulkdeploymentdetailedreportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBulkDeploymentDetailedReportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBulkDeploymentDetailedReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListBulkDeploymentDetailedReports.html#Greengrass.Paginator.ListBulkDeploymentDetailedReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listbulkdeploymentdetailedreportspaginator)
        """


if TYPE_CHECKING:
    _ListBulkDeploymentsPaginatorBase = AioPaginator[ListBulkDeploymentsResponseTypeDef]
else:
    _ListBulkDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBulkDeploymentsPaginator(_ListBulkDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListBulkDeployments.html#Greengrass.Paginator.ListBulkDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listbulkdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBulkDeploymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBulkDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListBulkDeployments.html#Greengrass.Paginator.ListBulkDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listbulkdeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListConnectorDefinitionVersionsPaginatorBase = AioPaginator[
        ListConnectorDefinitionVersionsResponseTypeDef
    ]
else:
    _ListConnectorDefinitionVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConnectorDefinitionVersionsPaginator(_ListConnectorDefinitionVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListConnectorDefinitionVersions.html#Greengrass.Paginator.ListConnectorDefinitionVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listconnectordefinitionversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorDefinitionVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectorDefinitionVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListConnectorDefinitionVersions.html#Greengrass.Paginator.ListConnectorDefinitionVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listconnectordefinitionversionspaginator)
        """


if TYPE_CHECKING:
    _ListConnectorDefinitionsPaginatorBase = AioPaginator[ListConnectorDefinitionsResponseTypeDef]
else:
    _ListConnectorDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConnectorDefinitionsPaginator(_ListConnectorDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListConnectorDefinitions.html#Greengrass.Paginator.ListConnectorDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listconnectordefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectorDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListConnectorDefinitions.html#Greengrass.Paginator.ListConnectorDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listconnectordefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListCoreDefinitionVersionsPaginatorBase = AioPaginator[
        ListCoreDefinitionVersionsResponseTypeDef
    ]
else:
    _ListCoreDefinitionVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCoreDefinitionVersionsPaginator(_ListCoreDefinitionVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListCoreDefinitionVersions.html#Greengrass.Paginator.ListCoreDefinitionVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listcoredefinitionversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCoreDefinitionVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCoreDefinitionVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListCoreDefinitionVersions.html#Greengrass.Paginator.ListCoreDefinitionVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listcoredefinitionversionspaginator)
        """


if TYPE_CHECKING:
    _ListCoreDefinitionsPaginatorBase = AioPaginator[ListCoreDefinitionsResponseTypeDef]
else:
    _ListCoreDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCoreDefinitionsPaginator(_ListCoreDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListCoreDefinitions.html#Greengrass.Paginator.ListCoreDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listcoredefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCoreDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCoreDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListCoreDefinitions.html#Greengrass.Paginator.ListCoreDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listcoredefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentsPaginatorBase = AioPaginator[ListDeploymentsResponseTypeDef]
else:
    _ListDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentsPaginator(_ListDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListDeployments.html#Greengrass.Paginator.ListDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListDeployments.html#Greengrass.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listdeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListDeviceDefinitionVersionsPaginatorBase = AioPaginator[
        ListDeviceDefinitionVersionsResponseTypeDef
    ]
else:
    _ListDeviceDefinitionVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeviceDefinitionVersionsPaginator(_ListDeviceDefinitionVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListDeviceDefinitionVersions.html#Greengrass.Paginator.ListDeviceDefinitionVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listdevicedefinitionversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeviceDefinitionVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeviceDefinitionVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListDeviceDefinitionVersions.html#Greengrass.Paginator.ListDeviceDefinitionVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listdevicedefinitionversionspaginator)
        """


if TYPE_CHECKING:
    _ListDeviceDefinitionsPaginatorBase = AioPaginator[ListDeviceDefinitionsResponseTypeDef]
else:
    _ListDeviceDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeviceDefinitionsPaginator(_ListDeviceDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListDeviceDefinitions.html#Greengrass.Paginator.ListDeviceDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listdevicedefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeviceDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeviceDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListDeviceDefinitions.html#Greengrass.Paginator.ListDeviceDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listdevicedefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListFunctionDefinitionVersionsPaginatorBase = AioPaginator[
        ListFunctionDefinitionVersionsResponseTypeDef
    ]
else:
    _ListFunctionDefinitionVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFunctionDefinitionVersionsPaginator(_ListFunctionDefinitionVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListFunctionDefinitionVersions.html#Greengrass.Paginator.ListFunctionDefinitionVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listfunctiondefinitionversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFunctionDefinitionVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFunctionDefinitionVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListFunctionDefinitionVersions.html#Greengrass.Paginator.ListFunctionDefinitionVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listfunctiondefinitionversionspaginator)
        """


if TYPE_CHECKING:
    _ListFunctionDefinitionsPaginatorBase = AioPaginator[ListFunctionDefinitionsResponseTypeDef]
else:
    _ListFunctionDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFunctionDefinitionsPaginator(_ListFunctionDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListFunctionDefinitions.html#Greengrass.Paginator.ListFunctionDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listfunctiondefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFunctionDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFunctionDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListFunctionDefinitions.html#Greengrass.Paginator.ListFunctionDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listfunctiondefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListGroupVersionsPaginatorBase = AioPaginator[ListGroupVersionsResponseTypeDef]
else:
    _ListGroupVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGroupVersionsPaginator(_ListGroupVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListGroupVersions.html#Greengrass.Paginator.ListGroupVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listgroupversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListGroupVersions.html#Greengrass.Paginator.ListGroupVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listgroupversionspaginator)
        """


if TYPE_CHECKING:
    _ListGroupsPaginatorBase = AioPaginator[ListGroupsResponseTypeDef]
else:
    _ListGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGroupsPaginator(_ListGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListGroups.html#Greengrass.Paginator.ListGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListGroups.html#Greengrass.Paginator.ListGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listgroupspaginator)
        """


if TYPE_CHECKING:
    _ListLoggerDefinitionVersionsPaginatorBase = AioPaginator[
        ListLoggerDefinitionVersionsResponseTypeDef
    ]
else:
    _ListLoggerDefinitionVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLoggerDefinitionVersionsPaginator(_ListLoggerDefinitionVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListLoggerDefinitionVersions.html#Greengrass.Paginator.ListLoggerDefinitionVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listloggerdefinitionversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLoggerDefinitionVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLoggerDefinitionVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListLoggerDefinitionVersions.html#Greengrass.Paginator.ListLoggerDefinitionVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listloggerdefinitionversionspaginator)
        """


if TYPE_CHECKING:
    _ListLoggerDefinitionsPaginatorBase = AioPaginator[ListLoggerDefinitionsResponseTypeDef]
else:
    _ListLoggerDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLoggerDefinitionsPaginator(_ListLoggerDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListLoggerDefinitions.html#Greengrass.Paginator.ListLoggerDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listloggerdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLoggerDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLoggerDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListLoggerDefinitions.html#Greengrass.Paginator.ListLoggerDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listloggerdefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListResourceDefinitionVersionsPaginatorBase = AioPaginator[
        ListResourceDefinitionVersionsResponseTypeDef
    ]
else:
    _ListResourceDefinitionVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceDefinitionVersionsPaginator(_ListResourceDefinitionVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListResourceDefinitionVersions.html#Greengrass.Paginator.ListResourceDefinitionVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listresourcedefinitionversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceDefinitionVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceDefinitionVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListResourceDefinitionVersions.html#Greengrass.Paginator.ListResourceDefinitionVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listresourcedefinitionversionspaginator)
        """


if TYPE_CHECKING:
    _ListResourceDefinitionsPaginatorBase = AioPaginator[ListResourceDefinitionsResponseTypeDef]
else:
    _ListResourceDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceDefinitionsPaginator(_ListResourceDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListResourceDefinitions.html#Greengrass.Paginator.ListResourceDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listresourcedefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListResourceDefinitions.html#Greengrass.Paginator.ListResourceDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listresourcedefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListSubscriptionDefinitionVersionsPaginatorBase = AioPaginator[
        ListSubscriptionDefinitionVersionsResponseTypeDef
    ]
else:
    _ListSubscriptionDefinitionVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSubscriptionDefinitionVersionsPaginator(_ListSubscriptionDefinitionVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListSubscriptionDefinitionVersions.html#Greengrass.Paginator.ListSubscriptionDefinitionVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listsubscriptiondefinitionversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionDefinitionVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionDefinitionVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListSubscriptionDefinitionVersions.html#Greengrass.Paginator.ListSubscriptionDefinitionVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listsubscriptiondefinitionversionspaginator)
        """


if TYPE_CHECKING:
    _ListSubscriptionDefinitionsPaginatorBase = AioPaginator[
        ListSubscriptionDefinitionsResponseTypeDef
    ]
else:
    _ListSubscriptionDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSubscriptionDefinitionsPaginator(_ListSubscriptionDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListSubscriptionDefinitions.html#Greengrass.Paginator.ListSubscriptionDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listsubscriptiondefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass/paginator/ListSubscriptionDefinitions.html#Greengrass.Paginator.ListSubscriptionDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrass/paginators/#listsubscriptiondefinitionspaginator)
        """
