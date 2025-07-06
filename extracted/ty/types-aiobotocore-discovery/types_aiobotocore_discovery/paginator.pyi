"""
Type annotations for discovery service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_discovery.client import ApplicationDiscoveryServiceClient
    from types_aiobotocore_discovery.paginator import (
        DescribeAgentsPaginator,
        DescribeContinuousExportsPaginator,
        DescribeExportConfigurationsPaginator,
        DescribeExportTasksPaginator,
        DescribeImportTasksPaginator,
        DescribeTagsPaginator,
        ListConfigurationsPaginator,
    )

    session = get_session()
    with session.create_client("discovery") as client:
        client: ApplicationDiscoveryServiceClient

        describe_agents_paginator: DescribeAgentsPaginator = client.get_paginator("describe_agents")
        describe_continuous_exports_paginator: DescribeContinuousExportsPaginator = client.get_paginator("describe_continuous_exports")
        describe_export_configurations_paginator: DescribeExportConfigurationsPaginator = client.get_paginator("describe_export_configurations")
        describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
        describe_import_tasks_paginator: DescribeImportTasksPaginator = client.get_paginator("describe_import_tasks")
        describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
        list_configurations_paginator: ListConfigurationsPaginator = client.get_paginator("list_configurations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAgentsRequestPaginateTypeDef,
    DescribeAgentsResponseTypeDef,
    DescribeContinuousExportsRequestPaginateTypeDef,
    DescribeContinuousExportsResponseTypeDef,
    DescribeExportConfigurationsRequestPaginateTypeDef,
    DescribeExportConfigurationsResponseTypeDef,
    DescribeExportTasksRequestPaginateTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeImportTasksRequestPaginateTypeDef,
    DescribeImportTasksResponseTypeDef,
    DescribeTagsRequestPaginateTypeDef,
    DescribeTagsResponseTypeDef,
    ListConfigurationsRequestPaginateTypeDef,
    ListConfigurationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAgentsPaginator",
    "DescribeContinuousExportsPaginator",
    "DescribeExportConfigurationsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeImportTasksPaginator",
    "DescribeTagsPaginator",
    "ListConfigurationsPaginator",
)

if TYPE_CHECKING:
    _DescribeAgentsPaginatorBase = AioPaginator[DescribeAgentsResponseTypeDef]
else:
    _DescribeAgentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeAgentsPaginator(_DescribeAgentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeAgents.html#ApplicationDiscoveryService.Paginator.DescribeAgents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeagentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAgentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeAgents.html#ApplicationDiscoveryService.Paginator.DescribeAgents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeagentspaginator)
        """

if TYPE_CHECKING:
    _DescribeContinuousExportsPaginatorBase = AioPaginator[DescribeContinuousExportsResponseTypeDef]
else:
    _DescribeContinuousExportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeContinuousExportsPaginator(_DescribeContinuousExportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeContinuousExports.html#ApplicationDiscoveryService.Paginator.DescribeContinuousExports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describecontinuousexportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeContinuousExportsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeContinuousExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeContinuousExports.html#ApplicationDiscoveryService.Paginator.DescribeContinuousExports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describecontinuousexportspaginator)
        """

if TYPE_CHECKING:
    _DescribeExportConfigurationsPaginatorBase = AioPaginator[
        DescribeExportConfigurationsResponseTypeDef
    ]
else:
    _DescribeExportConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeExportConfigurationsPaginator(_DescribeExportConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeExportConfigurations.html#ApplicationDiscoveryService.Paginator.DescribeExportConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeexportconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExportConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeExportConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeExportConfigurations.html#ApplicationDiscoveryService.Paginator.DescribeExportConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeexportconfigurationspaginator)
        """

if TYPE_CHECKING:
    _DescribeExportTasksPaginatorBase = AioPaginator[DescribeExportTasksResponseTypeDef]
else:
    _DescribeExportTasksPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeExportTasksPaginator(_DescribeExportTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeExportTasks.html#ApplicationDiscoveryService.Paginator.DescribeExportTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeexporttaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExportTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeExportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeExportTasks.html#ApplicationDiscoveryService.Paginator.DescribeExportTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeexporttaskspaginator)
        """

if TYPE_CHECKING:
    _DescribeImportTasksPaginatorBase = AioPaginator[DescribeImportTasksResponseTypeDef]
else:
    _DescribeImportTasksPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeImportTasksPaginator(_DescribeImportTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeImportTasks.html#ApplicationDiscoveryService.Paginator.DescribeImportTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeimporttaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImportTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeImportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeImportTasks.html#ApplicationDiscoveryService.Paginator.DescribeImportTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describeimporttaskspaginator)
        """

if TYPE_CHECKING:
    _DescribeTagsPaginatorBase = AioPaginator[DescribeTagsResponseTypeDef]
else:
    _DescribeTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeTagsPaginator(_DescribeTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeTags.html#ApplicationDiscoveryService.Paginator.DescribeTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describetagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/DescribeTags.html#ApplicationDiscoveryService.Paginator.DescribeTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#describetagspaginator)
        """

if TYPE_CHECKING:
    _ListConfigurationsPaginatorBase = AioPaginator[ListConfigurationsResponseTypeDef]
else:
    _ListConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConfigurationsPaginator(_ListConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/ListConfigurations.html#ApplicationDiscoveryService.Paginator.ListConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#listconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/discovery/paginator/ListConfigurations.html#ApplicationDiscoveryService.Paginator.ListConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_discovery/paginators/#listconfigurationspaginator)
        """
