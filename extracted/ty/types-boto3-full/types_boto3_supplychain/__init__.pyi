"""
Main interface for supplychain service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supplychain/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_supplychain import (
        Client,
        ListDataIntegrationEventsPaginator,
        ListDataIntegrationFlowExecutionsPaginator,
        ListDataIntegrationFlowsPaginator,
        ListDataLakeDatasetsPaginator,
        ListDataLakeNamespacesPaginator,
        ListInstancesPaginator,
        SupplyChainClient,
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

from .client import SupplyChainClient
from .paginator import (
    ListDataIntegrationEventsPaginator,
    ListDataIntegrationFlowExecutionsPaginator,
    ListDataIntegrationFlowsPaginator,
    ListDataLakeDatasetsPaginator,
    ListDataLakeNamespacesPaginator,
    ListInstancesPaginator,
)

Client = SupplyChainClient

__all__ = (
    "Client",
    "ListDataIntegrationEventsPaginator",
    "ListDataIntegrationFlowExecutionsPaginator",
    "ListDataIntegrationFlowsPaginator",
    "ListDataLakeDatasetsPaginator",
    "ListDataLakeNamespacesPaginator",
    "ListInstancesPaginator",
    "SupplyChainClient",
)
