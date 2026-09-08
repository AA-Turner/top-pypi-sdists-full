"""
Main interface for marketplace-catalog service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_marketplace_catalog import (
        Client,
        DescribeAssessmentPaginator,
        ListAssessmentsPaginator,
        ListChangeSetsPaginator,
        ListEntitiesPaginator,
        MarketplaceCatalogClient,
    )

    session = get_session()
    async with session.create_client("marketplace-catalog") as client:
        client: MarketplaceCatalogClient
        ...


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
