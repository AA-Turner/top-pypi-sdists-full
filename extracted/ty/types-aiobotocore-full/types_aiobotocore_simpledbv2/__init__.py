"""
Main interface for simpledbv2 service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_simpledbv2/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_simpledbv2 import (
        Client,
        ExportSucceededWaiter,
        ListExportsPaginator,
        SimpleDBv2Client,
    )

    session = get_session()
    async with session.create_client("simpledbv2") as client:
        client: SimpleDBv2Client
        ...


    export_succeeded_waiter: ExportSucceededWaiter = client.get_waiter("export_succeeded")

    list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    ```
"""

from .client import SimpleDBv2Client
from .paginator import ListExportsPaginator
from .waiter import ExportSucceededWaiter

Client = SimpleDBv2Client


__all__ = ("Client", "ExportSucceededWaiter", "ListExportsPaginator", "SimpleDBv2Client")
