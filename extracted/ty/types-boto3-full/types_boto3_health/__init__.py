"""
Main interface for health service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_health/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_health import (
        Client,
        DescribeAffectedAccountsForOrganizationPaginator,
        DescribeAffectedEntitiesForOrganizationPaginator,
        DescribeAffectedEntitiesPaginator,
        DescribeEventAggregatesPaginator,
        DescribeEventTypesPaginator,
        DescribeEventsForOrganizationPaginator,
        DescribeEventsPaginator,
        DescribeServiceLifecyclePaginator,
        DescribeTagsForOrganizationPaginator,
        DescribeTagsPaginator,
        HealthClient,
    )

    session = Session()
    client: HealthClient = session.client("health")

    describe_affected_accounts_for_organization_paginator: DescribeAffectedAccountsForOrganizationPaginator = client.get_paginator("describe_affected_accounts_for_organization")
    describe_affected_entities_for_organization_paginator: DescribeAffectedEntitiesForOrganizationPaginator = client.get_paginator("describe_affected_entities_for_organization")
    describe_affected_entities_paginator: DescribeAffectedEntitiesPaginator = client.get_paginator("describe_affected_entities")
    describe_event_aggregates_paginator: DescribeEventAggregatesPaginator = client.get_paginator("describe_event_aggregates")
    describe_event_types_paginator: DescribeEventTypesPaginator = client.get_paginator("describe_event_types")
    describe_events_for_organization_paginator: DescribeEventsForOrganizationPaginator = client.get_paginator("describe_events_for_organization")
    describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    describe_service_lifecycle_paginator: DescribeServiceLifecyclePaginator = client.get_paginator("describe_service_lifecycle")
    describe_tags_for_organization_paginator: DescribeTagsForOrganizationPaginator = client.get_paginator("describe_tags_for_organization")
    describe_tags_paginator: DescribeTagsPaginator = client.get_paginator("describe_tags")
    ```
"""

from .client import HealthClient
from .paginator import (
    DescribeAffectedAccountsForOrganizationPaginator,
    DescribeAffectedEntitiesForOrganizationPaginator,
    DescribeAffectedEntitiesPaginator,
    DescribeEventAggregatesPaginator,
    DescribeEventsForOrganizationPaginator,
    DescribeEventsPaginator,
    DescribeEventTypesPaginator,
    DescribeServiceLifecyclePaginator,
    DescribeTagsForOrganizationPaginator,
    DescribeTagsPaginator,
)

Client = HealthClient


__all__ = (
    "Client",
    "DescribeAffectedAccountsForOrganizationPaginator",
    "DescribeAffectedEntitiesForOrganizationPaginator",
    "DescribeAffectedEntitiesPaginator",
    "DescribeEventAggregatesPaginator",
    "DescribeEventTypesPaginator",
    "DescribeEventsForOrganizationPaginator",
    "DescribeEventsPaginator",
    "DescribeServiceLifecyclePaginator",
    "DescribeTagsForOrganizationPaginator",
    "DescribeTagsPaginator",
    "HealthClient",
)
