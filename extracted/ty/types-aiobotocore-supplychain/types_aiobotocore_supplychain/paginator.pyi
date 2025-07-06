"""
Type annotations for supplychain service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_supplychain.client import SupplyChainClient
    from types_aiobotocore_supplychain.paginator import (
        ListDataIntegrationEventsPaginator,
        ListDataIntegrationFlowExecutionsPaginator,
        ListDataIntegrationFlowsPaginator,
        ListDataLakeDatasetsPaginator,
        ListDataLakeNamespacesPaginator,
        ListInstancesPaginator,
    )

    session = get_session()
    with session.create_client("supplychain") as client:
        client: SupplyChainClient

        list_data_integration_events_paginator: ListDataIntegrationEventsPaginator = client.get_paginator("list_data_integration_events")
        list_data_integration_flow_executions_paginator: ListDataIntegrationFlowExecutionsPaginator = client.get_paginator("list_data_integration_flow_executions")
        list_data_integration_flows_paginator: ListDataIntegrationFlowsPaginator = client.get_paginator("list_data_integration_flows")
        list_data_lake_datasets_paginator: ListDataLakeDatasetsPaginator = client.get_paginator("list_data_lake_datasets")
        list_data_lake_namespaces_paginator: ListDataLakeNamespacesPaginator = client.get_paginator("list_data_lake_namespaces")
        list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDataIntegrationEventsRequestPaginateTypeDef,
    ListDataIntegrationEventsResponseTypeDef,
    ListDataIntegrationFlowExecutionsRequestPaginateTypeDef,
    ListDataIntegrationFlowExecutionsResponseTypeDef,
    ListDataIntegrationFlowsRequestPaginateTypeDef,
    ListDataIntegrationFlowsResponseTypeDef,
    ListDataLakeDatasetsRequestPaginateTypeDef,
    ListDataLakeDatasetsResponseTypeDef,
    ListDataLakeNamespacesRequestPaginateTypeDef,
    ListDataLakeNamespacesResponseTypeDef,
    ListInstancesRequestPaginateTypeDef,
    ListInstancesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDataIntegrationEventsPaginator",
    "ListDataIntegrationFlowExecutionsPaginator",
    "ListDataIntegrationFlowsPaginator",
    "ListDataLakeDatasetsPaginator",
    "ListDataLakeNamespacesPaginator",
    "ListInstancesPaginator",
)

if TYPE_CHECKING:
    _ListDataIntegrationEventsPaginatorBase = AioPaginator[ListDataIntegrationEventsResponseTypeDef]
else:
    _ListDataIntegrationEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataIntegrationEventsPaginator(_ListDataIntegrationEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationEvents.html#SupplyChain.Paginator.ListDataIntegrationEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataIntegrationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationEvents.html#SupplyChain.Paginator.ListDataIntegrationEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationeventspaginator)
        """

if TYPE_CHECKING:
    _ListDataIntegrationFlowExecutionsPaginatorBase = AioPaginator[
        ListDataIntegrationFlowExecutionsResponseTypeDef
    ]
else:
    _ListDataIntegrationFlowExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataIntegrationFlowExecutionsPaginator(_ListDataIntegrationFlowExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlowExecutions.html#SupplyChain.Paginator.ListDataIntegrationFlowExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationflowexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationFlowExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataIntegrationFlowExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlowExecutions.html#SupplyChain.Paginator.ListDataIntegrationFlowExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationflowexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListDataIntegrationFlowsPaginatorBase = AioPaginator[ListDataIntegrationFlowsResponseTypeDef]
else:
    _ListDataIntegrationFlowsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataIntegrationFlowsPaginator(_ListDataIntegrationFlowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationFlowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataIntegrationFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationflowspaginator)
        """

if TYPE_CHECKING:
    _ListDataLakeDatasetsPaginatorBase = AioPaginator[ListDataLakeDatasetsResponseTypeDef]
else:
    _ListDataLakeDatasetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataLakeDatasetsPaginator(_ListDataLakeDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdatalakedatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataLakeDatasetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataLakeDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdatalakedatasetspaginator)
        """

if TYPE_CHECKING:
    _ListDataLakeNamespacesPaginatorBase = AioPaginator[ListDataLakeNamespacesResponseTypeDef]
else:
    _ListDataLakeNamespacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataLakeNamespacesPaginator(_ListDataLakeNamespacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeNamespaces.html#SupplyChain.Paginator.ListDataLakeNamespaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdatalakenamespacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataLakeNamespacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataLakeNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeNamespaces.html#SupplyChain.Paginator.ListDataLakeNamespaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdatalakenamespacespaginator)
        """

if TYPE_CHECKING:
    _ListInstancesPaginatorBase = AioPaginator[ListInstancesResponseTypeDef]
else:
    _ListInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInstancesPaginator(_ListInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listinstancespaginator)
        """
