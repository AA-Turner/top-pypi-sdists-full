"""
Main interface for supportauthz service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supportauthz/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_supportauthz import (
        Client,
        ListActionsPaginator,
        ListSupportPermitRequestsPaginator,
        ListSupportPermitsPaginator,
        SupportAuthZClient,
    )

    session = Session()
    client: SupportAuthZClient = session.client("supportauthz")

    list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
    list_support_permit_requests_paginator: ListSupportPermitRequestsPaginator = client.get_paginator("list_support_permit_requests")
    list_support_permits_paginator: ListSupportPermitsPaginator = client.get_paginator("list_support_permits")
    ```
"""

from .client import SupportAuthZClient
from .paginator import (
    ListActionsPaginator,
    ListSupportPermitRequestsPaginator,
    ListSupportPermitsPaginator,
)

Client = SupportAuthZClient

__all__ = (
    "Client",
    "ListActionsPaginator",
    "ListSupportPermitRequestsPaginator",
    "ListSupportPermitsPaginator",
    "SupportAuthZClient",
)
