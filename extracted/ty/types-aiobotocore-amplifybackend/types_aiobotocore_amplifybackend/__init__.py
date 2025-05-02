"""
Main interface for amplifybackend service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_amplifybackend import (
        AmplifyBackendClient,
        Client,
        ListBackendJobsPaginator,
    )

    session = get_session()
    async with session.create_client("amplifybackend") as client:
        client: AmplifyBackendClient
        ...


    list_backend_jobs_paginator: ListBackendJobsPaginator = client.get_paginator("list_backend_jobs")
    ```
"""

from .client import AmplifyBackendClient
from .paginator import ListBackendJobsPaginator

Client = AmplifyBackendClient


__all__ = ("AmplifyBackendClient", "Client", "ListBackendJobsPaginator")
