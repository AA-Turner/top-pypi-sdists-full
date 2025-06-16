"""
Type annotations for budgets service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_budgets.client import BudgetsClient

    session = get_session()
    async with session.create_client("budgets") as client:
        client: BudgetsClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeBudgetActionHistoriesPaginator,
    DescribeBudgetActionsForAccountPaginator,
    DescribeBudgetActionsForBudgetPaginator,
    DescribeBudgetNotificationsForAccountPaginator,
    DescribeBudgetPerformanceHistoryPaginator,
    DescribeBudgetsPaginator,
    DescribeNotificationsForBudgetPaginator,
    DescribeSubscribersForNotificationPaginator,
)
from .type_defs import (
    CreateBudgetActionRequestTypeDef,
    CreateBudgetActionResponseTypeDef,
    CreateBudgetRequestTypeDef,
    CreateNotificationRequestTypeDef,
    CreateSubscriberRequestTypeDef,
    DeleteBudgetActionRequestTypeDef,
    DeleteBudgetActionResponseTypeDef,
    DeleteBudgetRequestTypeDef,
    DeleteNotificationRequestTypeDef,
    DeleteSubscriberRequestTypeDef,
    DescribeBudgetActionHistoriesRequestTypeDef,
    DescribeBudgetActionHistoriesResponseTypeDef,
    DescribeBudgetActionRequestTypeDef,
    DescribeBudgetActionResponseTypeDef,
    DescribeBudgetActionsForAccountRequestTypeDef,
    DescribeBudgetActionsForAccountResponseTypeDef,
    DescribeBudgetActionsForBudgetRequestTypeDef,
    DescribeBudgetActionsForBudgetResponseTypeDef,
    DescribeBudgetNotificationsForAccountRequestTypeDef,
    DescribeBudgetNotificationsForAccountResponseTypeDef,
    DescribeBudgetPerformanceHistoryRequestTypeDef,
    DescribeBudgetPerformanceHistoryResponseTypeDef,
    DescribeBudgetRequestTypeDef,
    DescribeBudgetResponseTypeDef,
    DescribeBudgetsRequestTypeDef,
    DescribeBudgetsResponseTypeDef,
    DescribeNotificationsForBudgetRequestTypeDef,
    DescribeNotificationsForBudgetResponseTypeDef,
    DescribeSubscribersForNotificationRequestTypeDef,
    DescribeSubscribersForNotificationResponseTypeDef,
    ExecuteBudgetActionRequestTypeDef,
    ExecuteBudgetActionResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateBudgetActionRequestTypeDef,
    UpdateBudgetActionResponseTypeDef,
    UpdateBudgetRequestTypeDef,
    UpdateNotificationRequestTypeDef,
    UpdateSubscriberRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("BudgetsClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CreationLimitExceededException: Type[BotocoreClientError]
    DuplicateRecordException: Type[BotocoreClientError]
    ExpiredNextTokenException: Type[BotocoreClientError]
    InternalErrorException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceLockedException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]

class BudgetsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BudgetsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#generate_presigned_url)
        """

    async def create_budget(self, **kwargs: Unpack[CreateBudgetRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates a budget and, if included, notifications and subscribers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/create_budget.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#create_budget)
        """

    async def create_budget_action(
        self, **kwargs: Unpack[CreateBudgetActionRequestTypeDef]
    ) -> CreateBudgetActionResponseTypeDef:
        """
        Creates a budget action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/create_budget_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#create_budget_action)
        """

    async def create_notification(
        self, **kwargs: Unpack[CreateNotificationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/create_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#create_notification)
        """

    async def create_subscriber(
        self, **kwargs: Unpack[CreateSubscriberRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/create_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#create_subscriber)
        """

    async def delete_budget(self, **kwargs: Unpack[DeleteBudgetRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/delete_budget.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#delete_budget)
        """

    async def delete_budget_action(
        self, **kwargs: Unpack[DeleteBudgetActionRequestTypeDef]
    ) -> DeleteBudgetActionResponseTypeDef:
        """
        Deletes a budget action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/delete_budget_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#delete_budget_action)
        """

    async def delete_notification(
        self, **kwargs: Unpack[DeleteNotificationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/delete_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#delete_notification)
        """

    async def delete_subscriber(
        self, **kwargs: Unpack[DeleteSubscriberRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/delete_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#delete_subscriber)
        """

    async def describe_budget(
        self, **kwargs: Unpack[DescribeBudgetRequestTypeDef]
    ) -> DescribeBudgetResponseTypeDef:
        """
        Describes a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_budget)
        """

    async def describe_budget_action(
        self, **kwargs: Unpack[DescribeBudgetActionRequestTypeDef]
    ) -> DescribeBudgetActionResponseTypeDef:
        """
        Describes a budget action detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_budget_action)
        """

    async def describe_budget_action_histories(
        self, **kwargs: Unpack[DescribeBudgetActionHistoriesRequestTypeDef]
    ) -> DescribeBudgetActionHistoriesResponseTypeDef:
        """
        Describes a budget action history detail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_action_histories.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_budget_action_histories)
        """

    async def describe_budget_actions_for_account(
        self, **kwargs: Unpack[DescribeBudgetActionsForAccountRequestTypeDef]
    ) -> DescribeBudgetActionsForAccountResponseTypeDef:
        """
        Describes all of the budget actions for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_actions_for_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_budget_actions_for_account)
        """

    async def describe_budget_actions_for_budget(
        self, **kwargs: Unpack[DescribeBudgetActionsForBudgetRequestTypeDef]
    ) -> DescribeBudgetActionsForBudgetResponseTypeDef:
        """
        Describes all of the budget actions for a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_actions_for_budget.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_budget_actions_for_budget)
        """

    async def describe_budget_notifications_for_account(
        self, **kwargs: Unpack[DescribeBudgetNotificationsForAccountRequestTypeDef]
    ) -> DescribeBudgetNotificationsForAccountResponseTypeDef:
        """
        Lists the budget names and notifications that are associated with an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_notifications_for_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_budget_notifications_for_account)
        """

    async def describe_budget_performance_history(
        self, **kwargs: Unpack[DescribeBudgetPerformanceHistoryRequestTypeDef]
    ) -> DescribeBudgetPerformanceHistoryResponseTypeDef:
        """
        Describes the history for <code>DAILY</code>, <code>MONTHLY</code>, and
        <code>QUARTERLY</code> budgets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budget_performance_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_budget_performance_history)
        """

    async def describe_budgets(
        self, **kwargs: Unpack[DescribeBudgetsRequestTypeDef]
    ) -> DescribeBudgetsResponseTypeDef:
        """
        Lists the budgets that are associated with an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_budgets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_budgets)
        """

    async def describe_notifications_for_budget(
        self, **kwargs: Unpack[DescribeNotificationsForBudgetRequestTypeDef]
    ) -> DescribeNotificationsForBudgetResponseTypeDef:
        """
        Lists the notifications that are associated with a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_notifications_for_budget.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_notifications_for_budget)
        """

    async def describe_subscribers_for_notification(
        self, **kwargs: Unpack[DescribeSubscribersForNotificationRequestTypeDef]
    ) -> DescribeSubscribersForNotificationResponseTypeDef:
        """
        Lists the subscribers that are associated with a notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/describe_subscribers_for_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#describe_subscribers_for_notification)
        """

    async def execute_budget_action(
        self, **kwargs: Unpack[ExecuteBudgetActionRequestTypeDef]
    ) -> ExecuteBudgetActionResponseTypeDef:
        """
        Executes a budget action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/execute_budget_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#execute_budget_action)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags associated with a budget or budget action resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#list_tags_for_resource)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates tags for a budget or budget action resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes tags associated with a budget or budget action resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#untag_resource)
        """

    async def update_budget(self, **kwargs: Unpack[UpdateBudgetRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a budget.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/update_budget.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#update_budget)
        """

    async def update_budget_action(
        self, **kwargs: Unpack[UpdateBudgetActionRequestTypeDef]
    ) -> UpdateBudgetActionResponseTypeDef:
        """
        Updates a budget action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/update_budget_action.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#update_budget_action)
        """

    async def update_notification(
        self, **kwargs: Unpack[UpdateNotificationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a notification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/update_notification.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#update_notification)
        """

    async def update_subscriber(
        self, **kwargs: Unpack[UpdateSubscriberRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/update_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#update_subscriber)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_budget_action_histories"]
    ) -> DescribeBudgetActionHistoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_budget_actions_for_account"]
    ) -> DescribeBudgetActionsForAccountPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_budget_actions_for_budget"]
    ) -> DescribeBudgetActionsForBudgetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_budget_notifications_for_account"]
    ) -> DescribeBudgetNotificationsForAccountPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_budget_performance_history"]
    ) -> DescribeBudgetPerformanceHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_budgets"]
    ) -> DescribeBudgetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_notifications_for_budget"]
    ) -> DescribeNotificationsForBudgetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_subscribers_for_notification"]
    ) -> DescribeSubscribersForNotificationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/budgets.html#Budgets.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_budgets/client/)
        """
