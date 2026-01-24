"""
Main interface for partnercentral-account service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_account/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_partnercentral_account import (
        Client,
        ListConnectionInvitationsPaginator,
        ListConnectionsPaginator,
        ListPartnersPaginator,
        PartnerCentralAccountAPIClient,
    )

    session = get_session()
    async with session.create_client("partnercentral-account") as client:
        client: PartnerCentralAccountAPIClient
        ...


    list_connection_invitations_paginator: ListConnectionInvitationsPaginator = client.get_paginator("list_connection_invitations")
    list_connections_paginator: ListConnectionsPaginator = client.get_paginator("list_connections")
    list_partners_paginator: ListPartnersPaginator = client.get_paginator("list_partners")
    ```
"""

from .client import PartnerCentralAccountAPIClient
from .paginator import (
    ListConnectionInvitationsPaginator,
    ListConnectionsPaginator,
    ListPartnersPaginator,
)

Client = PartnerCentralAccountAPIClient

__all__ = (
    "Client",
    "ListConnectionInvitationsPaginator",
    "ListConnectionsPaginator",
    "ListPartnersPaginator",
    "PartnerCentralAccountAPIClient",
)
