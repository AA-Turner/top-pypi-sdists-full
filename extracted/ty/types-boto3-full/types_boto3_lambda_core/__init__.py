"""
Main interface for lambda-core service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lambda_core/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_lambda_core import (
        Client,
        LambdaCoreClient,
        ListNetworkConnectorVersionsPaginator,
        ListNetworkConnectorsPaginator,
        ListRuntimeAliasesPaginator,
        ListRuntimeVersionsPaginator,
        ListRuntimesPaginator,
        RuntimeAliasActiveWaiter,
        RuntimeVersionActiveWaiter,
    )

    session = Session()
    client: LambdaCoreClient = session.client("lambda-core")

    runtime_alias_active_waiter: RuntimeAliasActiveWaiter = client.get_waiter("runtime_alias_active")
    runtime_version_active_waiter: RuntimeVersionActiveWaiter = client.get_waiter("runtime_version_active")

    list_network_connector_versions_paginator: ListNetworkConnectorVersionsPaginator = client.get_paginator("list_network_connector_versions")
    list_network_connectors_paginator: ListNetworkConnectorsPaginator = client.get_paginator("list_network_connectors")
    list_runtime_aliases_paginator: ListRuntimeAliasesPaginator = client.get_paginator("list_runtime_aliases")
    list_runtime_versions_paginator: ListRuntimeVersionsPaginator = client.get_paginator("list_runtime_versions")
    list_runtimes_paginator: ListRuntimesPaginator = client.get_paginator("list_runtimes")
    ```
"""

from .client import LambdaCoreClient
from .paginator import (
    ListNetworkConnectorsPaginator,
    ListNetworkConnectorVersionsPaginator,
    ListRuntimeAliasesPaginator,
    ListRuntimesPaginator,
    ListRuntimeVersionsPaginator,
)
from .waiter import RuntimeAliasActiveWaiter, RuntimeVersionActiveWaiter

Client = LambdaCoreClient


__all__ = (
    "Client",
    "LambdaCoreClient",
    "ListNetworkConnectorVersionsPaginator",
    "ListNetworkConnectorsPaginator",
    "ListRuntimeAliasesPaginator",
    "ListRuntimeVersionsPaginator",
    "ListRuntimesPaginator",
    "RuntimeAliasActiveWaiter",
    "RuntimeVersionActiveWaiter",
)
