"""
Type annotations for budgets service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_budgets.client import BudgetsClient
    from types_aiobotocore_budgets.paginator import (
        DescribeBudgetActionHistoriesPaginator,
        DescribeBudgetActionsForAccountPaginator,
        DescribeBudgetActionsForBudgetPaginator,
        DescribeBudgetNotificationsForAccountPaginator,
        DescribeBudgetPerformanceHistoryPaginator,
        DescribeBudgetsPaginator,
        DescribeNotificationsForBudgetPaginator,
        DescribeSubscribersForNotificationPaginator,
    )

    session = get_session()
    with session.create_client("budgets") as client:
        client: BudgetsClient

        describe_budget_action_histories_paginator: DescribeBudgetActionHistoriesPaginator = client.get_paginator("describe_budget_action_histories")
        describe_budget_actions_for_account_paginator: DescribeBudgetActionsForAccountPaginator = client.get_paginator("describe_budget_actions_for_account")
        describe_budget_actions_for_budget_paginator: DescribeBudgetActionsForBudgetPaginator = client.get_paginator("describe_budget_actions_for_budget")
        describe_budget_notifications_for_account_paginator: DescribeBudgetNotificationsForAccountPaginator = client.get_paginator("describe_budget_notifications_for_account")
        describe_budget_performance_history_paginator: DescribeBudgetPerformanceHistoryPaginator = client.get_paginator("describe_budget_performance_history")
        describe_budgets_paginator: DescribeBudgetsPaginator = client.get_paginator("describe_budgets")
        describe_notifications_for_budget_paginator: DescribeNotificationsForBudgetPaginator = client.get_paginator("describe_notifications_for_budget")
        describe_subscribers_for_notification_paginator: DescribeSubscribersForNotificationPaginator = client.get_paginator("describe_subscribers_for_notification")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeBudgetActionHistoriesRequestPaginateTypeDef,
    DescribeBudgetActionHistoriesResponseTypeDef,
    DescribeBudgetActionsForAccountRequestPaginateTypeDef,
    DescribeBudgetActionsForAccountResponseTypeDef,
    DescribeBudgetActionsForBudgetRequestPaginateTypeDef,
    DescribeBudgetActionsForBudgetResponseTypeDef,
    DescribeBudgetNotificationsForAccountRequestPaginateTypeDef,
    DescribeBudgetNotificationsForAccountResponseTypeDef,
    DescribeBudgetPerformanceHistoryRequestPaginateTypeDef,
    DescribeBudgetPerformanceHistoryResponseTypeDef,
    DescribeBudgetsRequestPaginateTypeDef,
    DescribeBudgetsResponsePaginatorTypeDef,
    DescribeNotificationsForBudgetRequestPaginateTypeDef,
    DescribeNotificationsForBudgetResponseTypeDef,
    DescribeSubscribersForNotificationRequestPaginateTypeDef,
    DescribeSubscribersForNotificationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeBudgetActionHistoriesPaginator",
    "DescribeBudgetActionsForAccountPaginator",
    "DescribeBudgetActionsForBudgetPaginator",
    "DescribeBudgetNotificationsForAccountPaginator",
    "DescribeBudgetPerformanceHistoryPaginator",
    "DescribeBudgetsPaginator",
    "DescribeNotificationsForBudgetPaginator",
    "DescribeSubscribersForNotificationPaginator",
)


if TYPE_CHECKING:
    _DescribeBudgetActionHistoriesPaginatorBase = AioPaginator[
        DescribeBudgetActionHistoriesResponseTypeDef
    ]
else:
    _DescribeBudgetActionHistoriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBudgetActionHistoriesPaginator(_DescribeBudgetActionHistoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionHistories.html#Budgets.Paginator.DescribeBudgetActionHistories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionhistoriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBudgetActionHistoriesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBudgetActionHistoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionHistories.html#Budgets.Paginator.DescribeBudgetActionHistories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionhistoriespaginator)
        """


if TYPE_CHECKING:
    _DescribeBudgetActionsForAccountPaginatorBase = AioPaginator[
        DescribeBudgetActionsForAccountResponseTypeDef
    ]
else:
    _DescribeBudgetActionsForAccountPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBudgetActionsForAccountPaginator(_DescribeBudgetActionsForAccountPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionsForAccount.html#Budgets.Paginator.DescribeBudgetActionsForAccount)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionsforaccountpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBudgetActionsForAccountRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBudgetActionsForAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionsForAccount.html#Budgets.Paginator.DescribeBudgetActionsForAccount.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionsforaccountpaginator)
        """


if TYPE_CHECKING:
    _DescribeBudgetActionsForBudgetPaginatorBase = AioPaginator[
        DescribeBudgetActionsForBudgetResponseTypeDef
    ]
else:
    _DescribeBudgetActionsForBudgetPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBudgetActionsForBudgetPaginator(_DescribeBudgetActionsForBudgetPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionsForBudget.html#Budgets.Paginator.DescribeBudgetActionsForBudget)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionsforbudgetpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBudgetActionsForBudgetRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBudgetActionsForBudgetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetActionsForBudget.html#Budgets.Paginator.DescribeBudgetActionsForBudget.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetactionsforbudgetpaginator)
        """


if TYPE_CHECKING:
    _DescribeBudgetNotificationsForAccountPaginatorBase = AioPaginator[
        DescribeBudgetNotificationsForAccountResponseTypeDef
    ]
else:
    _DescribeBudgetNotificationsForAccountPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBudgetNotificationsForAccountPaginator(
    _DescribeBudgetNotificationsForAccountPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetNotificationsForAccount.html#Budgets.Paginator.DescribeBudgetNotificationsForAccount)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetnotificationsforaccountpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBudgetNotificationsForAccountRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBudgetNotificationsForAccountResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetNotificationsForAccount.html#Budgets.Paginator.DescribeBudgetNotificationsForAccount.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetnotificationsforaccountpaginator)
        """


if TYPE_CHECKING:
    _DescribeBudgetPerformanceHistoryPaginatorBase = AioPaginator[
        DescribeBudgetPerformanceHistoryResponseTypeDef
    ]
else:
    _DescribeBudgetPerformanceHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBudgetPerformanceHistoryPaginator(_DescribeBudgetPerformanceHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetPerformanceHistory.html#Budgets.Paginator.DescribeBudgetPerformanceHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetperformancehistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBudgetPerformanceHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBudgetPerformanceHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgetPerformanceHistory.html#Budgets.Paginator.DescribeBudgetPerformanceHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetperformancehistorypaginator)
        """


if TYPE_CHECKING:
    _DescribeBudgetsPaginatorBase = AioPaginator[DescribeBudgetsResponsePaginatorTypeDef]
else:
    _DescribeBudgetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBudgetsPaginator(_DescribeBudgetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgets.html#Budgets.Paginator.DescribeBudgets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBudgetsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBudgetsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeBudgets.html#Budgets.Paginator.DescribeBudgets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describebudgetspaginator)
        """


if TYPE_CHECKING:
    _DescribeNotificationsForBudgetPaginatorBase = AioPaginator[
        DescribeNotificationsForBudgetResponseTypeDef
    ]
else:
    _DescribeNotificationsForBudgetPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeNotificationsForBudgetPaginator(_DescribeNotificationsForBudgetPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeNotificationsForBudget.html#Budgets.Paginator.DescribeNotificationsForBudget)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describenotificationsforbudgetpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNotificationsForBudgetRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeNotificationsForBudgetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeNotificationsForBudget.html#Budgets.Paginator.DescribeNotificationsForBudget.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describenotificationsforbudgetpaginator)
        """


if TYPE_CHECKING:
    _DescribeSubscribersForNotificationPaginatorBase = AioPaginator[
        DescribeSubscribersForNotificationResponseTypeDef
    ]
else:
    _DescribeSubscribersForNotificationPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSubscribersForNotificationPaginator(_DescribeSubscribersForNotificationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeSubscribersForNotification.html#Budgets.Paginator.DescribeSubscribersForNotification)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describesubscribersfornotificationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSubscribersForNotificationRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSubscribersForNotificationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/paginator/DescribeSubscribersForNotification.html#Budgets.Paginator.DescribeSubscribersForNotification.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/paginators/#describesubscribersfornotificationpaginator)
        """
