"""
Main interface for ram service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ram import (
        Client,
        GetResourcePoliciesPaginator,
        GetResourceShareAssociationsPaginator,
        GetResourceShareInvitationsPaginator,
        GetResourceSharesPaginator,
        ListPrincipalsPaginator,
        ListResourcesPaginator,
        RAMClient,
    )

    session = get_session()
    async with session.create_client("ram") as client:
        client: RAMClient
        ...


    get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
    get_resource_share_associations_paginator: GetResourceShareAssociationsPaginator = client.get_paginator("get_resource_share_associations")
    get_resource_share_invitations_paginator: GetResourceShareInvitationsPaginator = client.get_paginator("get_resource_share_invitations")
    get_resource_shares_paginator: GetResourceSharesPaginator = client.get_paginator("get_resource_shares")
    list_principals_paginator: ListPrincipalsPaginator = client.get_paginator("list_principals")
    list_resources_paginator: ListResourcesPaginator = client.get_paginator("list_resources")
    ```
"""

from .client import RAMClient
from .paginator import (
    GetResourcePoliciesPaginator,
    GetResourceShareAssociationsPaginator,
    GetResourceShareInvitationsPaginator,
    GetResourceSharesPaginator,
    ListPrincipalsPaginator,
    ListResourcesPaginator,
)

Client = RAMClient


__all__ = (
    "Client",
    "GetResourcePoliciesPaginator",
    "GetResourceShareAssociationsPaginator",
    "GetResourceShareInvitationsPaginator",
    "GetResourceSharesPaginator",
    "ListPrincipalsPaginator",
    "ListResourcesPaginator",
    "RAMClient",
)
