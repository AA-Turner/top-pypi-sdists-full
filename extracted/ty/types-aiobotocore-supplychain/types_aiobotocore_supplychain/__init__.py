"""
Main interface for supplychain service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_supplychain import (
        Client,
        ListDataIntegrationEventsPaginator,
        ListDataIntegrationFlowExecutionsPaginator,
        ListDataIntegrationFlowsPaginator,
        ListDataLakeDatasetsPaginator,
        ListDataLakeNamespacesPaginator,
        ListInstancesPaginator,
        SupplyChainClient,
    )

    session = get_session()
    async with session.create_client("supplychain") as client:
        client: SupplyChainClient
        ...


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
