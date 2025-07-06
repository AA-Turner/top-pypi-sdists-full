"""
Main interface for kafkaconnect service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafkaconnect/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kafkaconnect import (
        Client,
        KafkaConnectClient,
        ListConnectorOperationsPaginator,
        ListConnectorsPaginator,
        ListCustomPluginsPaginator,
        ListWorkerConfigurationsPaginator,
    )

    session = get_session()
    async with session.create_client("kafkaconnect") as client:
        client: KafkaConnectClient
        ...


    list_connector_operations_paginator: ListConnectorOperationsPaginator = client.get_paginator("list_connector_operations")
    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    list_custom_plugins_paginator: ListCustomPluginsPaginator = client.get_paginator("list_custom_plugins")
    list_worker_configurations_paginator: ListWorkerConfigurationsPaginator = client.get_paginator("list_worker_configurations")
    ```
"""

from .client import KafkaConnectClient
from .paginator import (
    ListConnectorOperationsPaginator,
    ListConnectorsPaginator,
    ListCustomPluginsPaginator,
    ListWorkerConfigurationsPaginator,
)

Client = KafkaConnectClient

__all__ = (
    "Client",
    "KafkaConnectClient",
    "ListConnectorOperationsPaginator",
    "ListConnectorsPaginator",
    "ListCustomPluginsPaginator",
    "ListWorkerConfigurationsPaginator",
)
