"""
Main interface for codeguru-security service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_security/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeguru_security import (
        Client,
        CodeGuruSecurityClient,
        GetFindingsPaginator,
        ListFindingsMetricsPaginator,
        ListScansPaginator,
    )

    session = get_session()
    async with session.create_client("codeguru-security") as client:
        client: CodeGuruSecurityClient
        ...


    get_findings_paginator: GetFindingsPaginator = client.get_paginator("get_findings")
    list_findings_metrics_paginator: ListFindingsMetricsPaginator = client.get_paginator("list_findings_metrics")
    list_scans_paginator: ListScansPaginator = client.get_paginator("list_scans")
    ```
"""

from .client import CodeGuruSecurityClient
from .paginator import GetFindingsPaginator, ListFindingsMetricsPaginator, ListScansPaginator

Client = CodeGuruSecurityClient

__all__ = (
    "Client",
    "CodeGuruSecurityClient",
    "GetFindingsPaginator",
    "ListFindingsMetricsPaginator",
    "ListScansPaginator",
)
