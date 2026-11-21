"""
Main interface for partnercentral-channel service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_partnercentral_channel/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_partnercentral_channel import (
        Client,
        ListChannelContractsPaginator,
        ListChannelHandshakesPaginator,
        ListProgramManagementAccountsPaginator,
        ListRelationshipsPaginator,
        PartnerCentralChannelAPIClient,
    )

    session = Session()
    client: PartnerCentralChannelAPIClient = session.client("partnercentral-channel")

    list_channel_contracts_paginator: ListChannelContractsPaginator = client.get_paginator("list_channel_contracts")
    list_channel_handshakes_paginator: ListChannelHandshakesPaginator = client.get_paginator("list_channel_handshakes")
    list_program_management_accounts_paginator: ListProgramManagementAccountsPaginator = client.get_paginator("list_program_management_accounts")
    list_relationships_paginator: ListRelationshipsPaginator = client.get_paginator("list_relationships")
    ```
"""

from .client import PartnerCentralChannelAPIClient
from .paginator import (
    ListChannelContractsPaginator,
    ListChannelHandshakesPaginator,
    ListProgramManagementAccountsPaginator,
    ListRelationshipsPaginator,
)

Client = PartnerCentralChannelAPIClient


__all__ = (
    "Client",
    "ListChannelContractsPaginator",
    "ListChannelHandshakesPaginator",
    "ListProgramManagementAccountsPaginator",
    "ListRelationshipsPaginator",
    "PartnerCentralChannelAPIClient",
)
