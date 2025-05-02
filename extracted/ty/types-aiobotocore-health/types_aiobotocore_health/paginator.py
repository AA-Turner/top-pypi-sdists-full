"""
Type annotations for health service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_health.client import HealthClient
    from types_aiobotocore_health.paginator import (
        DescribeAffectedAccountsForOrganizationPaginator,
        DescribeAffectedEntitiesForOrganizationPaginator,
        DescribeAffectedEntitiesPaginator,
        DescribeEventAggregatesPaginator,
        DescribeEventTypesPaginator,
        DescribeEventsForOrganizationPaginator,
        DescribeEventsPaginator,
    )

    session = get_session()
    with session.create_client("health") as client:
        client: HealthClient

        describe_affected_accounts_for_organization_paginator: DescribeAffectedAccountsForOrganizationPaginator = client.get_paginator("describe_affected_accounts_for_organization")
        describe_affected_entities_for_organization_paginator: DescribeAffectedEntitiesForOrganizationPaginator = client.get_paginator("describe_affected_entities_for_organization")
        describe_affected_entities_paginator: DescribeAffectedEntitiesPaginator = client.get_paginator("describe_affected_entities")
        describe_event_aggregates_paginator: DescribeEventAggregatesPaginator = client.get_paginator("describe_event_aggregates")
        describe_event_types_paginator: DescribeEventTypesPaginator = client.get_paginator("describe_event_types")
        describe_events_for_organization_paginator: DescribeEventsForOrganizationPaginator = client.get_paginator("describe_events_for_organization")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAffectedAccountsForOrganizationRequestPaginateTypeDef,
    DescribeAffectedAccountsForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesForOrganizationRequestPaginateTypeDef,
    DescribeAffectedEntitiesForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesRequestPaginateTypeDef,
    DescribeAffectedEntitiesResponseTypeDef,
    DescribeEventAggregatesRequestPaginateTypeDef,
    DescribeEventAggregatesResponseTypeDef,
    DescribeEventsForOrganizationRequestPaginateTypeDef,
    DescribeEventsForOrganizationResponseTypeDef,
    DescribeEventsRequestPaginateTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventTypesRequestPaginateTypeDef,
    DescribeEventTypesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAffectedAccountsForOrganizationPaginator",
    "DescribeAffectedEntitiesForOrganizationPaginator",
    "DescribeAffectedEntitiesPaginator",
    "DescribeEventAggregatesPaginator",
    "DescribeEventTypesPaginator",
    "DescribeEventsForOrganizationPaginator",
    "DescribeEventsPaginator",
)


if TYPE_CHECKING:
    _DescribeAffectedAccountsForOrganizationPaginatorBase = AioPaginator[
        DescribeAffectedAccountsForOrganizationResponseTypeDef
    ]
else:
    _DescribeAffectedAccountsForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAffectedAccountsForOrganizationPaginator(
    _DescribeAffectedAccountsForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedAccountsForOrganization.html#Health.Paginator.DescribeAffectedAccountsForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedaccountsfororganizationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAffectedAccountsForOrganizationRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAffectedAccountsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedAccountsForOrganization.html#Health.Paginator.DescribeAffectedAccountsForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedaccountsfororganizationpaginator)
        """


if TYPE_CHECKING:
    _DescribeAffectedEntitiesForOrganizationPaginatorBase = AioPaginator[
        DescribeAffectedEntitiesForOrganizationResponseTypeDef
    ]
else:
    _DescribeAffectedEntitiesForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAffectedEntitiesForOrganizationPaginator(
    _DescribeAffectedEntitiesForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedEntitiesForOrganization.html#Health.Paginator.DescribeAffectedEntitiesForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedentitiesfororganizationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAffectedEntitiesForOrganizationRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAffectedEntitiesForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedEntitiesForOrganization.html#Health.Paginator.DescribeAffectedEntitiesForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedentitiesfororganizationpaginator)
        """


if TYPE_CHECKING:
    _DescribeAffectedEntitiesPaginatorBase = AioPaginator[DescribeAffectedEntitiesResponseTypeDef]
else:
    _DescribeAffectedEntitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAffectedEntitiesPaginator(_DescribeAffectedEntitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedEntities.html#Health.Paginator.DescribeAffectedEntities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedentitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAffectedEntitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAffectedEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeAffectedEntities.html#Health.Paginator.DescribeAffectedEntities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedentitiespaginator)
        """


if TYPE_CHECKING:
    _DescribeEventAggregatesPaginatorBase = AioPaginator[DescribeEventAggregatesResponseTypeDef]
else:
    _DescribeEventAggregatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventAggregatesPaginator(_DescribeEventAggregatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventAggregates.html#Health.Paginator.DescribeEventAggregates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventaggregatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventAggregatesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEventAggregatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventAggregates.html#Health.Paginator.DescribeEventAggregates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventaggregatespaginator)
        """


if TYPE_CHECKING:
    _DescribeEventTypesPaginatorBase = AioPaginator[DescribeEventTypesResponseTypeDef]
else:
    _DescribeEventTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventTypesPaginator(_DescribeEventTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventTypes.html#Health.Paginator.DescribeEventTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventtypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEventTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventTypes.html#Health.Paginator.DescribeEventTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventtypespaginator)
        """


if TYPE_CHECKING:
    _DescribeEventsForOrganizationPaginatorBase = AioPaginator[
        DescribeEventsForOrganizationResponseTypeDef
    ]
else:
    _DescribeEventsForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventsForOrganizationPaginator(_DescribeEventsForOrganizationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventsForOrganization.html#Health.Paginator.DescribeEventsForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventsfororganizationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsForOrganizationRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEventsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEventsForOrganization.html#Health.Paginator.DescribeEventsForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventsfororganizationpaginator)
        """


if TYPE_CHECKING:
    _DescribeEventsPaginatorBase = AioPaginator[DescribeEventsResponseTypeDef]
else:
    _DescribeEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEventsPaginator(_DescribeEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEvents.html#Health.Paginator.DescribeEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/paginator/DescribeEvents.html#Health.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventspaginator)
        """
