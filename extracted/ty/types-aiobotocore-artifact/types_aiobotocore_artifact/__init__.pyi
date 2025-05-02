"""
Main interface for artifact service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_artifact/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_artifact import (
        ArtifactClient,
        Client,
        ListCustomerAgreementsPaginator,
        ListReportsPaginator,
    )

    session = get_session()
    async with session.create_client("artifact") as client:
        client: ArtifactClient
        ...


    list_customer_agreements_paginator: ListCustomerAgreementsPaginator = client.get_paginator("list_customer_agreements")
    list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    ```
"""

from .client import ArtifactClient
from .paginator import ListCustomerAgreementsPaginator, ListReportsPaginator

Client = ArtifactClient

__all__ = ("ArtifactClient", "Client", "ListCustomerAgreementsPaginator", "ListReportsPaginator")
