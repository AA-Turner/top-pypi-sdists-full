"""
Main interface for iotfleethub service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleethub/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotfleethub import (
        Client,
        IoTFleetHubClient,
        ListApplicationsPaginator,
    )

    session = get_session()
    async with session.create_client("iotfleethub") as client:
        client: IoTFleetHubClient
        ...


    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```
"""

from .client import IoTFleetHubClient
from .paginator import ListApplicationsPaginator

Client = IoTFleetHubClient

__all__ = ("Client", "IoTFleetHubClient", "ListApplicationsPaginator")
