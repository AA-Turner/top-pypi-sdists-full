"""
Type annotations for eventbridgev2 service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_eventbridgev2.client import EventBridgeV2Client

    session = get_session()
    async with session.create_client("eventbridgev2") as client:
        client: EventBridgeV2Client
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListEventBusesPaginator,
    ListEventSourcesPaginator,
    ListResourcePoliciesPaginator,
    ListSubscribersPaginator,
)
from .type_defs import (
    CreateEventBusRequestTypeDef,
    CreateEventBusResponseTypeDef,
    CreateEventSourceRequestTypeDef,
    CreateEventSourceResponseTypeDef,
    CreateSubscriberRequestTypeDef,
    CreateSubscriberResponseTypeDef,
    DeleteEventBusRequestTypeDef,
    DeleteEventSourceRequestTypeDef,
    DeleteResourcePolicyRequestTypeDef,
    DeleteResourcePolicyResponseTypeDef,
    DeleteSubscriberRequestTypeDef,
    DescribeEventBusRequestTypeDef,
    DescribeEventBusResponseTypeDef,
    DescribeEventSourceRequestTypeDef,
    DescribeEventSourceResponseTypeDef,
    DescribeSubscriberRequestTypeDef,
    DescribeSubscriberResponseTypeDef,
    GetResourcePolicyRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    ListEventBusesRequestTypeDef,
    ListEventBusesResponseTypeDef,
    ListEventSourcesRequestTypeDef,
    ListEventSourcesResponseTypeDef,
    ListResourcePoliciesRequestTypeDef,
    ListResourcePoliciesResponseTypeDef,
    ListSubscribersRequestTypeDef,
    ListSubscribersResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutEventsRequestTypeDef,
    PutEventsResponseTypeDef,
    PutRawEventsRequestTypeDef,
    PutRawEventsResponseTypeDef,
    PutResourcePolicyRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    RevokeResourceRequestTypeDef,
    RevokeResourceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateEventBusRequestTypeDef,
    UpdateEventBusResponseTypeDef,
    UpdateEventSourceRequestTypeDef,
    UpdateEventSourceResponseTypeDef,
    UpdateSubscriberRequestTypeDef,
    UpdateSubscriberResponseTypeDef,
)
from .waiter import EventBusActiveWaiter, EventBusDeletedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("EventBridgeV2Client",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConcurrentModificationException: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    IdempotentParameterMismatchException: type[BotocoreClientError]
    InternalException: type[BotocoreClientError]
    InvalidInputException: type[BotocoreClientError]
    InvalidStateException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    PolicyLengthExceededException: type[BotocoreClientError]
    PublicPolicyException: type[BotocoreClientError]
    ResourceAlreadyExistsException: type[BotocoreClientError]
    ResourceInUseException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    SchemaRegistryUnavailableException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]


class EventBridgeV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2.html#EventBridgeV2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EventBridgeV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2.html#EventBridgeV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#generate_presigned_url)
        """

    async def create_event_bus(
        self, **kwargs: Unpack[CreateEventBusRequestTypeDef]
    ) -> CreateEventBusResponseTypeDef:
        """
        Creates an event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/create_event_bus.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#create_event_bus)
        """

    async def create_event_source(
        self, **kwargs: Unpack[CreateEventSourceRequestTypeDef]
    ) -> CreateEventSourceResponseTypeDef:
        """
        Creates an EventSource, which forwards events from an origin (an AWS service or
        another account) onto an event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/create_event_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#create_event_source)
        """

    async def create_subscriber(
        self, **kwargs: Unpack[CreateSubscriberRequestTypeDef]
    ) -> CreateSubscriberResponseTypeDef:
        """
        Creates a subscriber on an event bus, which delivers matching events to the
        configured target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/create_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#create_subscriber)
        """

    async def delete_event_bus(
        self, **kwargs: Unpack[DeleteEventBusRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/delete_event_bus.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#delete_event_bus)
        """

    async def delete_event_source(
        self, **kwargs: Unpack[DeleteEventSourceRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an EventSource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/delete_event_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#delete_event_source)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestTypeDef]
    ) -> DeleteResourcePolicyResponseTypeDef:
        """
        Deletes the named resource policy attached to an event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/delete_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#delete_resource_policy)
        """

    async def delete_subscriber(
        self, **kwargs: Unpack[DeleteSubscriberRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/delete_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#delete_subscriber)
        """

    async def describe_event_bus(
        self, **kwargs: Unpack[DescribeEventBusRequestTypeDef]
    ) -> DescribeEventBusResponseTypeDef:
        """
        Returns the full configuration and lifecycle state of an event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/describe_event_bus.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#describe_event_bus)
        """

    async def describe_event_source(
        self, **kwargs: Unpack[DescribeEventSourceRequestTypeDef]
    ) -> DescribeEventSourceResponseTypeDef:
        """
        Returns the full configuration and lifecycle state of an EventSource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/describe_event_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#describe_event_source)
        """

    async def describe_subscriber(
        self, **kwargs: Unpack[DescribeSubscriberRequestTypeDef]
    ) -> DescribeSubscriberResponseTypeDef:
        """
        Returns the full configuration and state of a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/describe_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#describe_subscriber)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Returns the named resource policy attached to an event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/get_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#get_resource_policy)
        """

    async def list_event_buses(
        self, **kwargs: Unpack[ListEventBusesRequestTypeDef]
    ) -> ListEventBusesResponseTypeDef:
        """
        Lists the event buses visible to the caller: buses the account owns and buses
        shared with it through AWS RAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/list_event_buses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#list_event_buses)
        """

    async def list_event_sources(
        self, **kwargs: Unpack[ListEventSourcesRequestTypeDef]
    ) -> ListEventSourcesResponseTypeDef:
        """
        Lists EventSources as summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/list_event_sources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#list_event_sources)
        """

    async def list_resource_policies(
        self, **kwargs: Unpack[ListResourcePoliciesRequestTypeDef]
    ) -> ListResourcePoliciesResponseTypeDef:
        """
        Lists the resource policies attached to an event bus as summaries (policy name
        and revision ID).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/list_resource_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#list_resource_policies)
        """

    async def list_subscribers(
        self, **kwargs: Unpack[ListSubscribersRequestTypeDef]
    ) -> ListSubscribersResponseTypeDef:
        """
        Lists subscribers as summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/list_subscribers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#list_subscribers)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags on an event bus, subscriber, or event source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#list_tags_for_resource)
        """

    async def put_events(
        self, **kwargs: Unpack[PutEventsRequestTypeDef]
    ) -> PutEventsResponseTypeDef:
        """
        Publishes events to an event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/put_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#put_events)
        """

    async def put_raw_events(
        self, **kwargs: Unpack[PutRawEventsRequestTypeDef]
    ) -> PutRawEventsResponseTypeDef:
        """
        Publishes pre-shaped events to an event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/put_raw_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#put_raw_events)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Attaches a named resource policy to an event bus — the only resource type that
        supports policies; other resource ARNs are rejected.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/put_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#put_resource_policy)
        """

    async def revoke_resource(
        self, **kwargs: Unpack[RevokeResourceRequestTypeDef]
    ) -> RevokeResourceResponseTypeDef:
        """
        Revokes a subscriber or an EventSource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/revoke_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#revoke_resource)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds or replaces tags on an event bus, subscriber, or event source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes tags from an event bus, subscriber, or event source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#untag_resource)
        """

    async def update_event_bus(
        self, **kwargs: Unpack[UpdateEventBusRequestTypeDef]
    ) -> UpdateEventBusResponseTypeDef:
        """
        Updates an event bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/update_event_bus.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#update_event_bus)
        """

    async def update_event_source(
        self, **kwargs: Unpack[UpdateEventSourceRequestTypeDef]
    ) -> UpdateEventSourceResponseTypeDef:
        """
        Updates an EventSource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/update_event_source.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#update_event_source)
        """

    async def update_subscriber(
        self, **kwargs: Unpack[UpdateSubscriberRequestTypeDef]
    ) -> UpdateSubscriberResponseTypeDef:
        """
        Updates a subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/update_subscriber.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#update_subscriber)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_event_buses"]
    ) -> ListEventBusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_event_sources"]
    ) -> ListEventSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_policies"]
    ) -> ListResourcePoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_subscribers"]
    ) -> ListSubscribersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["event_bus_active"]
    ) -> EventBusActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["event_bus_deleted"]
    ) -> EventBusDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2.html#EventBridgeV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eventbridgev2.html#EventBridgeV2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eventbridgev2/client/)
        """
