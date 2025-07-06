"""
Main interface for customer-profiles service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_customer_profiles/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_customer_profiles import (
        Client,
        CustomerProfilesClient,
        GetSimilarProfilesPaginator,
        ListEventStreamsPaginator,
        ListEventTriggersPaginator,
        ListObjectTypeAttributesPaginator,
        ListRuleBasedMatchesPaginator,
        ListSegmentDefinitionsPaginator,
    )

    session = get_session()
    async with session.create_client("customer-profiles") as client:
        client: CustomerProfilesClient
        ...


    get_similar_profiles_paginator: GetSimilarProfilesPaginator = client.get_paginator("get_similar_profiles")
    list_event_streams_paginator: ListEventStreamsPaginator = client.get_paginator("list_event_streams")
    list_event_triggers_paginator: ListEventTriggersPaginator = client.get_paginator("list_event_triggers")
    list_object_type_attributes_paginator: ListObjectTypeAttributesPaginator = client.get_paginator("list_object_type_attributes")
    list_rule_based_matches_paginator: ListRuleBasedMatchesPaginator = client.get_paginator("list_rule_based_matches")
    list_segment_definitions_paginator: ListSegmentDefinitionsPaginator = client.get_paginator("list_segment_definitions")
    ```
"""

from .client import CustomerProfilesClient
from .paginator import (
    GetSimilarProfilesPaginator,
    ListEventStreamsPaginator,
    ListEventTriggersPaginator,
    ListObjectTypeAttributesPaginator,
    ListRuleBasedMatchesPaginator,
    ListSegmentDefinitionsPaginator,
)

Client = CustomerProfilesClient

__all__ = (
    "Client",
    "CustomerProfilesClient",
    "GetSimilarProfilesPaginator",
    "ListEventStreamsPaginator",
    "ListEventTriggersPaginator",
    "ListObjectTypeAttributesPaginator",
    "ListRuleBasedMatchesPaginator",
    "ListSegmentDefinitionsPaginator",
)
