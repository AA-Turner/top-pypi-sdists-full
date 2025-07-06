"""
Main interface for opensearch service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_opensearch import (
        Client,
        ListApplicationsPaginator,
        OpenSearchServiceClient,
    )

    session = get_session()
    async with session.create_client("opensearch") as client:
        client: OpenSearchServiceClient
        ...


    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```
"""

from .client import OpenSearchServiceClient
from .paginator import ListApplicationsPaginator

Client = OpenSearchServiceClient

__all__ = ("Client", "ListApplicationsPaginator", "OpenSearchServiceClient")
