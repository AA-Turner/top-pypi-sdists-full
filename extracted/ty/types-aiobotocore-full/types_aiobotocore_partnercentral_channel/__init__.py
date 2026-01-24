"""
Main interface for partnercentral-channel service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_channel/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_partnercentral_channel import (
        Client,
        ListChannelHandshakesPaginator,
        ListProgramManagementAccountsPaginator,
        ListRelationshipsPaginator,
        PartnerCentralChannelAPIClient,
    )

    session = get_session()
    async with session.create_client("partnercentral-channel") as client:
        client: PartnerCentralChannelAPIClient
        ...


    list_channel_handshakes_paginator: ListChannelHandshakesPaginator = client.get_paginator("list_channel_handshakes")
    list_program_management_accounts_paginator: ListProgramManagementAccountsPaginator = client.get_paginator("list_program_management_accounts")
    list_relationships_paginator: ListRelationshipsPaginator = client.get_paginator("list_relationships")
    ```
"""

from .client import PartnerCentralChannelAPIClient
from .paginator import (
    ListChannelHandshakesPaginator,
    ListProgramManagementAccountsPaginator,
    ListRelationshipsPaginator,
)

Client = PartnerCentralChannelAPIClient


__all__ = (
    "Client",
    "ListChannelHandshakesPaginator",
    "ListProgramManagementAccountsPaginator",
    "ListRelationshipsPaginator",
    "PartnerCentralChannelAPIClient",
)
