"""
Main interface for cloudcontrol service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudcontrol import (
        Client,
        CloudControlApiClient,
        ListResourceRequestsPaginator,
        ListResourcesPaginator,
        ResourceRequestSuccessWaiter,
    )

    session = get_session()
    async with session.create_client("cloudcontrol") as client:
        client: CloudControlApiClient
        ...


    resource_request_success_waiter: ResourceRequestSuccessWaiter = client.get_waiter("resource_request_success")

    list_resource_requests_paginator: ListResourceRequestsPaginator = client.get_paginator("list_resource_requests")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```
"""

from .client import CloudControlApiClient
from .paginator import ListResourceRequestsPaginator, ListResourcesPaginator
from .waiter import ResourceRequestSuccessWaiter

Client = CloudControlApiClient

__all__ = (
    "Client",
    "CloudControlApiClient",
    "ListResourceRequestsPaginator",
    "ListResourcesPaginator",
    "ResourceRequestSuccessWaiter",
)
