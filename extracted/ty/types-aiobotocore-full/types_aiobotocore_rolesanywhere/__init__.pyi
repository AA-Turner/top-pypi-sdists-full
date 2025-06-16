"""
Main interface for rolesanywhere service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rolesanywhere import (
        Client,
        IAMRolesAnywhereClient,
        ListCrlsPaginator,
        ListProfilesPaginator,
        ListSubjectsPaginator,
        ListTrustAnchorsPaginator,
    )

    session = get_session()
    async with session.create_client("rolesanywhere") as client:
        client: IAMRolesAnywhereClient
        ...


    list_crls_paginator: ListCrlsPaginator = client.get_paginator("list_crls")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    list_subjects_paginator: ListSubjectsPaginator = client.get_paginator("list_subjects")
    list_trust_anchors_paginator: ListTrustAnchorsPaginator = client.get_paginator("list_trust_anchors")
    ```
"""

from .client import IAMRolesAnywhereClient
from .paginator import (
    ListCrlsPaginator,
    ListProfilesPaginator,
    ListSubjectsPaginator,
    ListTrustAnchorsPaginator,
)

Client = IAMRolesAnywhereClient

__all__ = (
    "Client",
    "IAMRolesAnywhereClient",
    "ListCrlsPaginator",
    "ListProfilesPaginator",
    "ListSubjectsPaginator",
    "ListTrustAnchorsPaginator",
)
