"""
Main interface for kinesisanalyticsv2 service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisanalyticsv2/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kinesisanalyticsv2 import (
        Client,
        KinesisAnalyticsV2Client,
        ListApplicationOperationsPaginator,
        ListApplicationSnapshotsPaginator,
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
    )

    session = get_session()
    async with session.create_client("kinesisanalyticsv2") as client:
        client: KinesisAnalyticsV2Client
        ...


    list_application_operations_paginator: ListApplicationOperationsPaginator = client.get_paginator("list_application_operations")
    list_application_snapshots_paginator: ListApplicationSnapshotsPaginator = client.get_paginator("list_application_snapshots")
    list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
    list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
    ```
"""

from .client import KinesisAnalyticsV2Client
from .paginator import (
    ListApplicationOperationsPaginator,
    ListApplicationSnapshotsPaginator,
    ListApplicationsPaginator,
    ListApplicationVersionsPaginator,
)

Client = KinesisAnalyticsV2Client


__all__ = (
    "Client",
    "KinesisAnalyticsV2Client",
    "ListApplicationOperationsPaginator",
    "ListApplicationSnapshotsPaginator",
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
)
