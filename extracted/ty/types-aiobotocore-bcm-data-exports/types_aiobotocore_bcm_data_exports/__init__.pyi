"""
Main interface for bcm-data-exports service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_data_exports/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bcm_data_exports import (
        BillingandCostManagementDataExportsClient,
        Client,
        ListExecutionsPaginator,
        ListExportsPaginator,
        ListTablesPaginator,
    )

    session = get_session()
    async with session.create_client("bcm-data-exports") as client:
        client: BillingandCostManagementDataExportsClient
        ...


    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    list_tables_paginator: ListTablesPaginator = client.get_paginator("list_tables")
    ```
"""

from .client import BillingandCostManagementDataExportsClient
from .paginator import ListExecutionsPaginator, ListExportsPaginator, ListTablesPaginator

Client = BillingandCostManagementDataExportsClient

__all__ = (
    "BillingandCostManagementDataExportsClient",
    "Client",
    "ListExecutionsPaginator",
    "ListExportsPaginator",
    "ListTablesPaginator",
)
