"""
Main interface for simpledbv2 service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_simpledbv2 import (
        Client,
        ExportSucceededWaiter,
        ListExportsPaginator,
        SimpleDBv2Client,
    )

    session = Session()
    client: SimpleDBv2Client = session.client("simpledbv2")

    export_succeeded_waiter: ExportSucceededWaiter = client.get_waiter("export_succeeded")

    list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    ```
"""

from .client import SimpleDBv2Client
from .paginator import ListExportsPaginator
from .waiter import ExportSucceededWaiter

Client = SimpleDBv2Client

__all__ = ("Client", "ExportSucceededWaiter", "ListExportsPaginator", "SimpleDBv2Client")
