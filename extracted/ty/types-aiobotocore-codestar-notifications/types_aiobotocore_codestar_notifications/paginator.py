"""
Type annotations for codestar-notifications service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codestar_notifications.client import CodeStarNotificationsClient
    from types_aiobotocore_codestar_notifications.paginator import (
        ListEventTypesPaginator,
        ListNotificationRulesPaginator,
        ListTargetsPaginator,
    )

    session = get_session()
    with session.create_client("codestar-notifications") as client:
        client: CodeStarNotificationsClient

        list_event_types_paginator: ListEventTypesPaginator = client.get_paginator("list_event_types")
        list_notification_rules_paginator: ListNotificationRulesPaginator = client.get_paginator("list_notification_rules")
        list_targets_paginator: ListTargetsPaginator = client.get_paginator("list_targets")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListEventTypesRequestPaginateTypeDef,
    ListEventTypesResultTypeDef,
    ListNotificationRulesRequestPaginateTypeDef,
    ListNotificationRulesResultTypeDef,
    ListTargetsRequestPaginateTypeDef,
    ListTargetsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListEventTypesPaginator", "ListNotificationRulesPaginator", "ListTargetsPaginator")


if TYPE_CHECKING:
    _ListEventTypesPaginatorBase = AioPaginator[ListEventTypesResultTypeDef]
else:
    _ListEventTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventTypesPaginator(_ListEventTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListEventTypes.html#CodeStarNotifications.Paginator.ListEventTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listeventtypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventTypesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListEventTypes.html#CodeStarNotifications.Paginator.ListEventTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listeventtypespaginator)
        """


if TYPE_CHECKING:
    _ListNotificationRulesPaginatorBase = AioPaginator[ListNotificationRulesResultTypeDef]
else:
    _ListNotificationRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNotificationRulesPaginator(_ListNotificationRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListNotificationRules.html#CodeStarNotifications.Paginator.ListNotificationRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listnotificationrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationRulesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListNotificationRules.html#CodeStarNotifications.Paginator.ListNotificationRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listnotificationrulespaginator)
        """


if TYPE_CHECKING:
    _ListTargetsPaginatorBase = AioPaginator[ListTargetsResultTypeDef]
else:
    _ListTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTargetsPaginator(_ListTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListTargets.html#CodeStarNotifications.Paginator.ListTargets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listtargetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/paginator/ListTargets.html#CodeStarNotifications.Paginator.ListTargets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/paginators/#listtargetspaginator)
        """
