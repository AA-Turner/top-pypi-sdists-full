"""
Main interface for connectcases service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcases/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectcases import (
        Client,
        ConnectCasesClient,
        ListCaseRulesPaginator,
        SearchAllRelatedItemsPaginator,
        SearchCasesPaginator,
        SearchRelatedItemsPaginator,
    )

    session = get_session()
    async with session.create_client("connectcases") as client:
        client: ConnectCasesClient
        ...


    list_case_rules_paginator: ListCaseRulesPaginator = client.get_paginator("list_case_rules")
    search_all_related_items_paginator: SearchAllRelatedItemsPaginator = client.get_paginator("search_all_related_items")
    search_cases_paginator: SearchCasesPaginator = client.get_paginator("search_cases")
    search_related_items_paginator: SearchRelatedItemsPaginator = client.get_paginator("search_related_items")
    ```
"""

from .client import ConnectCasesClient
from .paginator import (
    ListCaseRulesPaginator,
    SearchAllRelatedItemsPaginator,
    SearchCasesPaginator,
    SearchRelatedItemsPaginator,
)

Client = ConnectCasesClient

__all__ = (
    "Client",
    "ConnectCasesClient",
    "ListCaseRulesPaginator",
    "SearchAllRelatedItemsPaginator",
    "SearchCasesPaginator",
    "SearchRelatedItemsPaginator",
)
