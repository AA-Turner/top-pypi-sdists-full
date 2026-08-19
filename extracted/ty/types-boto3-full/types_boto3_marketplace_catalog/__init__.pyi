"""
Main interface for marketplace-catalog service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_catalog/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_marketplace_catalog import (
        Client,
        DescribeAssessmentPaginator,
        ListAssessmentsPaginator,
        ListChangeSetsPaginator,
        ListEntitiesPaginator,
        MarketplaceCatalogClient,
    )

    session = Session()
    client: MarketplaceCatalogClient = session.client("marketplace-catalog")

    describe_assessment_paginator: DescribeAssessmentPaginator = client.get_paginator("describe_assessment")
    list_assessments_paginator: ListAssessmentsPaginator = client.get_paginator("list_assessments")
    list_change_sets_paginator: ListChangeSetsPaginator = client.get_paginator("list_change_sets")
    list_entities_paginator: ListEntitiesPaginator = client.get_paginator("list_entities")
    ```
"""

from .client import MarketplaceCatalogClient
from .paginator import (
    DescribeAssessmentPaginator,
    ListAssessmentsPaginator,
    ListChangeSetsPaginator,
    ListEntitiesPaginator,
)

Client = MarketplaceCatalogClient

__all__ = (
    "Client",
    "DescribeAssessmentPaginator",
    "ListAssessmentsPaginator",
    "ListChangeSetsPaginator",
    "ListEntitiesPaginator",
    "MarketplaceCatalogClient",
)
