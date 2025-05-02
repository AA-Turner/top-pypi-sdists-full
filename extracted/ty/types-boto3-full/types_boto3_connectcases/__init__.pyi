"""
Main interface for connectcases service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_connectcases/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_connectcases import (
        Client,
        ConnectCasesClient,
        ListCaseRulesPaginator,
        SearchCasesPaginator,
        SearchRelatedItemsPaginator,
    )

    session = Session()
    client: ConnectCasesClient = session.client("connectcases")

    list_case_rules_paginator: ListCaseRulesPaginator = client.get_paginator("list_case_rules")
    search_cases_paginator: SearchCasesPaginator = client.get_paginator("search_cases")
    search_related_items_paginator: SearchRelatedItemsPaginator = client.get_paginator("search_related_items")
    ```
"""

from .client import ConnectCasesClient
from .paginator import ListCaseRulesPaginator, SearchCasesPaginator, SearchRelatedItemsPaginator

Client = ConnectCasesClient

__all__ = (
    "Client",
    "ConnectCasesClient",
    "ListCaseRulesPaginator",
    "SearchCasesPaginator",
    "SearchRelatedItemsPaginator",
)
