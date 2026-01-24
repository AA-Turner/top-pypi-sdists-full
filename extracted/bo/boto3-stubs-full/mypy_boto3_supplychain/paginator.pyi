"""
Type annotations for supplychain service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_supplychain.client import SupplyChainClient
    from mypy_boto3_supplychain.paginator import (
        ListDataIntegrationEventsPaginator,
        ListDataIntegrationFlowExecutionsPaginator,
        ListDataIntegrationFlowsPaginator,
        ListDataLakeDatasetsPaginator,
        ListDataLakeNamespacesPaginator,
        ListInstancesPaginator,
    )

    session = Session()
    client: SupplyChainClient = session.client("supplychain")

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

from botocore.paginate import PageIterator, Paginator

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
    _ListDataIntegrationEventsPaginatorBase = Paginator[ListDataIntegrationEventsResponseTypeDef]
else:
    _ListDataIntegrationEventsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataIntegrationEventsPaginator(_ListDataIntegrationEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationEvents.html#SupplyChain.Paginator.ListDataIntegrationEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationEventsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataIntegrationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationEvents.html#SupplyChain.Paginator.ListDataIntegrationEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationeventspaginator)
        """

if TYPE_CHECKING:
    _ListDataIntegrationFlowExecutionsPaginatorBase = Paginator[
        ListDataIntegrationFlowExecutionsResponseTypeDef
    ]
else:
    _ListDataIntegrationFlowExecutionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataIntegrationFlowExecutionsPaginator(_ListDataIntegrationFlowExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlowExecutions.html#SupplyChain.Paginator.ListDataIntegrationFlowExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationflowexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationFlowExecutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataIntegrationFlowExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlowExecutions.html#SupplyChain.Paginator.ListDataIntegrationFlowExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationflowexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListDataIntegrationFlowsPaginatorBase = Paginator[ListDataIntegrationFlowsResponseTypeDef]
else:
    _ListDataIntegrationFlowsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataIntegrationFlowsPaginator(_ListDataIntegrationFlowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationFlowsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataIntegrationFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationflowspaginator)
        """

if TYPE_CHECKING:
    _ListDataLakeDatasetsPaginatorBase = Paginator[ListDataLakeDatasetsResponseTypeDef]
else:
    _ListDataLakeDatasetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataLakeDatasetsPaginator(_ListDataLakeDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdatalakedatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataLakeDatasetsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataLakeDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdatalakedatasetspaginator)
        """

if TYPE_CHECKING:
    _ListDataLakeNamespacesPaginatorBase = Paginator[ListDataLakeNamespacesResponseTypeDef]
else:
    _ListDataLakeNamespacesPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataLakeNamespacesPaginator(_ListDataLakeNamespacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeNamespaces.html#SupplyChain.Paginator.ListDataLakeNamespaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdatalakenamespacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataLakeNamespacesRequestPaginateTypeDef]
    ) -> PageIterator[ListDataLakeNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeNamespaces.html#SupplyChain.Paginator.ListDataLakeNamespaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdatalakenamespacespaginator)
        """

if TYPE_CHECKING:
    _ListInstancesPaginatorBase = Paginator[ListInstancesResponseTypeDef]
else:
    _ListInstancesPaginatorBase = Paginator  # type: ignore[assignment]

class ListInstancesPaginator(_ListInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstancesRequestPaginateTypeDef]
    ) -> PageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listinstancespaginator)
        """
