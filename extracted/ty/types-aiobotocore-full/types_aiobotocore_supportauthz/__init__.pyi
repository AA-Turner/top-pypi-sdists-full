"""
Main interface for supportauthz service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_supportauthz import (
        Client,
        ListActionsPaginator,
        ListSupportPermitRequestsPaginator,
        ListSupportPermitsPaginator,
        SupportAuthZClient,
    )

    session = get_session()
    async with session.create_client("supportauthz") as client:
        client: SupportAuthZClient
        ...


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
