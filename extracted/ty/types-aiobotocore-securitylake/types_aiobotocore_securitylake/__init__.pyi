"""
Main interface for securitylake service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_securitylake import (
        Client,
        GetDataLakeSourcesPaginator,
        ListDataLakeExceptionsPaginator,
        ListLogSourcesPaginator,
        ListSubscribersPaginator,
        SecurityLakeClient,
    )

    session = get_session()
    async with session.create_client("securitylake") as client:
        client: SecurityLakeClient
        ...


    get_data_lake_sources_paginator: GetDataLakeSourcesPaginator = client.get_paginator("get_data_lake_sources")
    list_data_lake_exceptions_paginator: ListDataLakeExceptionsPaginator = client.get_paginator("list_data_lake_exceptions")
    list_log_sources_paginator: ListLogSourcesPaginator = client.get_paginator("list_log_sources")
    list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```
"""

from .client import SecurityLakeClient
from .paginator import (
    GetDataLakeSourcesPaginator,
    ListDataLakeExceptionsPaginator,
    ListLogSourcesPaginator,
    ListSubscribersPaginator,
)

Client = SecurityLakeClient

__all__ = (
    "Client",
    "GetDataLakeSourcesPaginator",
    "ListDataLakeExceptionsPaginator",
    "ListLogSourcesPaginator",
    "ListSubscribersPaginator",
    "SecurityLakeClient",
)
