"""
Type annotations for codestar-notifications service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codestar_notifications.client import CodeStarNotificationsClient

    session = get_session()
    async with session.create_client("codestar-notifications") as client:
        client: CodeStarNotificationsClient
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

from .paginator import ListEventTypesPaginator, ListNotificationRulesPaginator, ListTargetsPaginator
from .type_defs import (
    CreateNotificationRuleRequestTypeDef,
    CreateNotificationRuleResultTypeDef,
    DeleteNotificationRuleRequestTypeDef,
    DeleteNotificationRuleResultTypeDef,
    DeleteTargetRequestTypeDef,
    DescribeNotificationRuleRequestTypeDef,
    DescribeNotificationRuleResultTypeDef,
    ListEventTypesRequestTypeDef,
    ListEventTypesResultTypeDef,
    ListNotificationRulesRequestTypeDef,
    ListNotificationRulesResultTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResultTypeDef,
    ListTargetsRequestTypeDef,
    ListTargetsResultTypeDef,
    SubscribeRequestTypeDef,
    SubscribeResultTypeDef,
    TagResourceRequestTypeDef,
    TagResourceResultTypeDef,
    UnsubscribeRequestTypeDef,
    UnsubscribeResultTypeDef,
    UntagResourceRequestTypeDef,
    UpdateNotificationRuleRequestTypeDef,
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


__all__ = ("CodeStarNotificationsClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConfigurationException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CodeStarNotificationsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeStarNotificationsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#generate_presigned_url)
        """

    async def create_notification_rule(
        self, **kwargs: Unpack[CreateNotificationRuleRequestTypeDef]
    ) -> CreateNotificationRuleResultTypeDef:
        """
        Creates a notification rule for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/create_notification_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#create_notification_rule)
        """

    async def delete_notification_rule(
        self, **kwargs: Unpack[DeleteNotificationRuleRequestTypeDef]
    ) -> DeleteNotificationRuleResultTypeDef:
        """
        Deletes a notification rule for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/delete_notification_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#delete_notification_rule)
        """

    async def delete_target(self, **kwargs: Unpack[DeleteTargetRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a specified target for notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/delete_target.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#delete_target)
        """

    async def describe_notification_rule(
        self, **kwargs: Unpack[DescribeNotificationRuleRequestTypeDef]
    ) -> DescribeNotificationRuleResultTypeDef:
        """
        Returns information about a specified notification rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/describe_notification_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#describe_notification_rule)
        """

    async def list_event_types(
        self, **kwargs: Unpack[ListEventTypesRequestTypeDef]
    ) -> ListEventTypesResultTypeDef:
        """
        Returns information about the event types available for configuring
        notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/list_event_types.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#list_event_types)
        """

    async def list_notification_rules(
        self, **kwargs: Unpack[ListNotificationRulesRequestTypeDef]
    ) -> ListNotificationRulesResultTypeDef:
        """
        Returns a list of the notification rules for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/list_notification_rules.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#list_notification_rules)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResultTypeDef:
        """
        Returns a list of the tags associated with a notification rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#list_tags_for_resource)
        """

    async def list_targets(
        self, **kwargs: Unpack[ListTargetsRequestTypeDef]
    ) -> ListTargetsResultTypeDef:
        """
        Returns a list of the notification rule targets for an Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/list_targets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#list_targets)
        """

    async def subscribe(self, **kwargs: Unpack[SubscribeRequestTypeDef]) -> SubscribeResultTypeDef:
        """
        Creates an association between a notification rule and an Chatbot topic or
        Chatbot client so that the associated target can receive notifications when the
        events described in the rule are triggered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/subscribe.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#subscribe)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> TagResourceResultTypeDef:
        """
        Associates a set of provided tags with a notification rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#tag_resource)
        """

    async def unsubscribe(
        self, **kwargs: Unpack[UnsubscribeRequestTypeDef]
    ) -> UnsubscribeResultTypeDef:
        """
        Removes an association between a notification rule and an Chatbot topic so that
        subscribers to that topic stop receiving notifications when the events
        described in the rule are triggered.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/unsubscribe.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#unsubscribe)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the association between one or more provided tags and a notification
        rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#untag_resource)
        """

    async def update_notification_rule(
        self, **kwargs: Unpack[UpdateNotificationRuleRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a notification rule for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/update_notification_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#update_notification_rule)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_event_types"]
    ) -> ListEventTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_notification_rules"]
    ) -> ListNotificationRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_targets"]
    ) -> ListTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar-notifications.html#CodeStarNotifications.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_notifications/client/)
        """
