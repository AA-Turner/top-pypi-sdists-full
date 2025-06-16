"""
Main interface for security-ir service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_security_ir import (
        Client,
        ListCaseEditsPaginator,
        ListCasesPaginator,
        ListCommentsPaginator,
        ListMembershipsPaginator,
        SecurityIncidentResponseClient,
    )

    session = get_session()
    async with session.create_client("security-ir") as client:
        client: SecurityIncidentResponseClient
        ...


    list_case_edits_paginator: ListCaseEditsPaginator = client.get_paginator("list_case_edits")
    list_cases_paginator: ListCasesPaginator = client.get_paginator("list_cases")
    list_comments_paginator: ListCommentsPaginator = client.get_paginator("list_comments")
    list_memberships_paginator: ListMembershipsPaginator = client.get_paginator("list_memberships")
    ```
"""

from .client import SecurityIncidentResponseClient
from .paginator import (
    ListCaseEditsPaginator,
    ListCasesPaginator,
    ListCommentsPaginator,
    ListMembershipsPaginator,
)

Client = SecurityIncidentResponseClient


__all__ = (
    "Client",
    "ListCaseEditsPaginator",
    "ListCasesPaginator",
    "ListCommentsPaginator",
    "ListMembershipsPaginator",
    "SecurityIncidentResponseClient",
)
