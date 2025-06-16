"""
Main interface for braket service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_braket import (
        BraketClient,
        Client,
        SearchDevicesPaginator,
        SearchJobsPaginator,
        SearchQuantumTasksPaginator,
    )

    session = get_session()
    async with session.create_client("braket") as client:
        client: BraketClient
        ...


    search_devices_paginator: SearchDevicesPaginator = client.get_paginator("search_devices")
    search_jobs_paginator: SearchJobsPaginator = client.get_paginator("search_jobs")
    search_quantum_tasks_paginator: SearchQuantumTasksPaginator = client.get_paginator("search_quantum_tasks")
    ```
"""

from .client import BraketClient
from .paginator import SearchDevicesPaginator, SearchJobsPaginator, SearchQuantumTasksPaginator

Client = BraketClient

__all__ = (
    "BraketClient",
    "Client",
    "SearchDevicesPaginator",
    "SearchJobsPaginator",
    "SearchQuantumTasksPaginator",
)
