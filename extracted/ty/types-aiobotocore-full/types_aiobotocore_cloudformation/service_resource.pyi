"""
Type annotations for cloudformation service ServiceResource.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudformation.service_resource import CloudFormationServiceResource
    import types_aiobotocore_cloudformation.service_resource as cloudformation_resources

    session = get_session()
    async with session.resource("cloudformation") as resource:
        resource: CloudFormationServiceResource

        my_event: cloudformation_resources.Event = resource.Event(...)
        my_stack: cloudformation_resources.Stack = resource.Stack(...)
        my_stack_resource: cloudformation_resources.StackResource = resource.StackResource(...)
        my_stack_resource_summary: cloudformation_resources.StackResourceSummary = resource.StackResourceSummary(...)
```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import NoReturn

from aioboto3.resources.base import AIOBoto3ServiceResource
from aioboto3.resources.collection import AIOResourceCollection

from .client import CloudFormationClient
from .literals import (
    CapabilityType,
    DeletionModeType,
    DetailedStatusType,
    HookFailureModeType,
    HookStatusType,
    ResourceStatusType,
    StackStatusType,
)
from .type_defs import (
    CancelUpdateStackInputStackCancelUpdateTypeDef,
    CreateStackInputServiceResourceCreateStackTypeDef,
    DeleteStackInputStackDeleteTypeDef,
    ModuleInfoTypeDef,
    OutputTypeDef,
    ParameterTypeDef,
    RollbackConfigurationOutputTypeDef,
    StackDriftInformationTypeDef,
    StackResourceDriftInformationSummaryTypeDef,
    StackResourceDriftInformationTypeDef,
    TagTypeDef,
    UpdateStackInputStackUpdateTypeDef,
    UpdateStackOutputTypeDef,
)

try:
    from boto3.resources.base import ResourceMeta
except ImportError:
    from builtins import object as ResourceMeta  # type: ignore[assignment]
if sys.version_info >= (3, 9):
    from builtins import list as List
    from collections.abc import AsyncIterator, Awaitable, Sequence
else:
    from typing import AsyncIterator, Awaitable, List, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = (
    "CloudFormationServiceResource",
    "Event",
    "ServiceResourceStacksCollection",
    "Stack",
    "StackEventsCollection",
    "StackResource",
    "StackResourceSummariesCollection",
    "StackResourceSummary",
)

class ServiceResourceStacksCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/stacks.html#CloudFormation.ServiceResource.stacks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#serviceresourcestackscollection)
    """
    def all(self) -> ServiceResourceStacksCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/stacks.html#CloudFormation.ServiceResource.all)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#serviceresourcestackscollection)
        """

    def filter(  # type: ignore[override]
        self, *, StackName: str = ..., NextToken: str = ...
    ) -> ServiceResourceStacksCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/stacks.html#filter)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#serviceresourcestackscollection)
        """

    def limit(self, count: int) -> ServiceResourceStacksCollection:
        """
        Return at most this many Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/stacks.html#limit)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#serviceresourcestackscollection)
        """

    def page_size(self, count: int) -> ServiceResourceStacksCollection:
        """
        Fetch at most this many Stacks per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/stacks.html#page_size)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#serviceresourcestackscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Stack]]:
        """
        A generator which yields pages of Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/stacks.html#pages)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#serviceresourcestackscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/stacks.html#__iter__)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#serviceresourcestackscollection)
        """

    def __aiter__(self) -> AsyncIterator[Stack]:
        """
        A generator which yields Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/stacks.html#__iter__)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#serviceresourcestackscollection)
        """

class StackEventsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/events.html#CloudFormation.Stack.events)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackevents)
    """
    def all(self) -> StackEventsCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/events.html#CloudFormation.Stack.all)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackevents)
        """

    def filter(  # type: ignore[override]
        self, *, StackName: str = ..., NextToken: str = ...
    ) -> StackEventsCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/events.html#filter)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackevents)
        """

    def limit(self, count: int) -> StackEventsCollection:
        """
        Return at most this many Events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/events.html#limit)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackevents)
        """

    def page_size(self, count: int) -> StackEventsCollection:
        """
        Fetch at most this many Events per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/events.html#page_size)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackevents)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Event]]:
        """
        A generator which yields pages of Events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/events.html#pages)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackevents)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/events.html#__iter__)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackevents)
        """

    def __aiter__(self) -> AsyncIterator[Event]:
        """
        A generator which yields Events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/events.html#__iter__)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackevents)
        """

class StackResourceSummariesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/resource_summaries.html#CloudFormation.Stack.resource_summaries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource_summaries)
    """
    def all(self) -> StackResourceSummariesCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/resource_summaries.html#CloudFormation.Stack.all)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource_summaries)
        """

    def filter(  # type: ignore[override]
        self, *, NextToken: str = ...
    ) -> StackResourceSummariesCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/resource_summaries.html#filter)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource_summaries)
        """

    def limit(self, count: int) -> StackResourceSummariesCollection:
        """
        Return at most this many StackResourceSummarys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/resource_summaries.html#limit)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource_summaries)
        """

    def page_size(self, count: int) -> StackResourceSummariesCollection:
        """
        Fetch at most this many StackResourceSummarys per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/resource_summaries.html#page_size)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource_summaries)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[StackResourceSummary]]:
        """
        A generator which yields pages of StackResourceSummarys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/resource_summaries.html#pages)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource_summaries)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields StackResourceSummarys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/resource_summaries.html#__iter__)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource_summaries)
        """

    def __aiter__(self) -> AsyncIterator[StackResourceSummary]:
        """
        A generator which yields StackResourceSummarys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/resource_summaries.html#__iter__)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource_summaries)
        """

class Event(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/event/index.html#CloudFormation.Event)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#event)
    """

    id: str
    stack_id: Awaitable[str]
    event_id: Awaitable[str]
    stack_name: Awaitable[str]
    logical_resource_id: Awaitable[str]
    physical_resource_id: Awaitable[str]
    resource_type: Awaitable[str]
    timestamp: Awaitable[datetime]
    resource_status: Awaitable[ResourceStatusType]
    resource_status_reason: Awaitable[str]
    resource_properties: Awaitable[str]
    client_request_token: Awaitable[str]
    hook_type: Awaitable[str]
    hook_status: Awaitable[HookStatusType]
    hook_status_reason: Awaitable[str]
    hook_invocation_point: Awaitable[Literal["PRE_PROVISION"]]
    hook_failure_mode: Awaitable[HookFailureModeType]
    detailed_status: Awaitable[DetailedStatusType]
    meta: CloudFormationResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/event/get_available_subresources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#eventget_available_subresources-method)
        """

_Event = Event

class Stack(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/index.html#CloudFormation.Stack)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stack)
    """

    name: str
    events: StackEventsCollection
    resource_summaries: StackResourceSummariesCollection
    stack_id: Awaitable[str]
    stack_name: Awaitable[str]
    change_set_id: Awaitable[str]
    description: Awaitable[str]
    parameters: Awaitable[List[ParameterTypeDef]]
    creation_time: Awaitable[datetime]
    deletion_time: Awaitable[datetime]
    last_updated_time: Awaitable[datetime]
    rollback_configuration: Awaitable[RollbackConfigurationOutputTypeDef]
    stack_status: Awaitable[StackStatusType]
    stack_status_reason: Awaitable[str]
    disable_rollback: Awaitable[bool]
    notification_arns: Awaitable[List[str]]
    timeout_in_minutes: Awaitable[int]
    capabilities: Awaitable[List[CapabilityType]]
    outputs: Awaitable[List[OutputTypeDef]]
    role_arn: Awaitable[str]
    tags: Awaitable[List[TagTypeDef]]
    enable_termination_protection: Awaitable[bool]
    parent_id: Awaitable[str]
    root_id: Awaitable[str]
    drift_information: Awaitable[StackDriftInformationTypeDef]
    retain_except_on_create: Awaitable[bool]
    deletion_mode: Awaitable[DeletionModeType]
    detailed_status: Awaitable[DetailedStatusType]
    meta: CloudFormationResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/get_available_subresources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackget_available_subresources-method)
        """

    async def cancel_update(
        self, **kwargs: Unpack[CancelUpdateStackInputStackCancelUpdateTypeDef]
    ) -> None:
        """
        Cancels an update on the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/cancel_update.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackcancel_update-method)
        """

    async def delete(self, **kwargs: Unpack[DeleteStackInputStackDeleteTypeDef]) -> None:
        """
        Deletes a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/delete.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackdelete-method)
        """

    async def update(
        self, **kwargs: Unpack[UpdateStackInputStackUpdateTypeDef]
    ) -> UpdateStackOutputTypeDef:
        """
        Updates a stack as specified in the template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/update.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackupdate-method)
        """

    async def Resource(self, logical_id: str) -> _StackResource:
        """
        Creates a StackResource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/Resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/load.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stack/reload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackreload-method)
        """

_Stack = Stack

class StackResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stackresource/index.html#CloudFormation.StackResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresource)
    """

    stack_name: str
    logical_id: str
    stack_id: Awaitable[str]
    logical_resource_id: Awaitable[str]
    physical_resource_id: Awaitable[str]
    resource_type: Awaitable[str]
    last_updated_timestamp: Awaitable[datetime]
    resource_status: Awaitable[ResourceStatusType]
    resource_status_reason: Awaitable[str]
    description: Awaitable[str]
    metadata: Awaitable[str]
    drift_information: Awaitable[StackResourceDriftInformationTypeDef]
    module_info: Awaitable[ModuleInfoTypeDef]
    meta: CloudFormationResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this StackResource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stackresource/get_available_subresources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresourceget_available_subresources-method)
        """

    async def Stack(self) -> _Stack:
        """
        Creates a Stack resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stackresource/Stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresourcestack-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stackresource/load.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresourceload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stackresource/reload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresourcereload-method)
        """

_StackResource = StackResource

class StackResourceSummary(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stackresourcesummary/index.html#CloudFormation.StackResourceSummary)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresourcesummary)
    """

    stack_name: str
    logical_id: str
    logical_resource_id: Awaitable[str]
    physical_resource_id: Awaitable[str]
    resource_type: Awaitable[str]
    last_updated_timestamp: Awaitable[datetime]
    resource_status: Awaitable[ResourceStatusType]
    resource_status_reason: Awaitable[str]
    drift_information: Awaitable[StackResourceDriftInformationSummaryTypeDef]
    module_info: Awaitable[ModuleInfoTypeDef]
    meta: CloudFormationResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this StackResourceSummary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stackresourcesummary/get_available_subresources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresourcesummaryget_available_subresources-method)
        """

    async def Resource(self) -> _StackResource:
        """
        Creates a StackResource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/stackresourcesummary/Resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#stackresourcesummaryresource-method)
        """

_StackResourceSummary = StackResourceSummary

class CloudFormationResourceMeta(ResourceMeta):
    client: CloudFormationClient  # type: ignore[override]

class CloudFormationServiceResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/index.html)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/)
    """

    meta: CloudFormationResourceMeta  # type: ignore[override]
    stacks: ServiceResourceStacksCollection

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/get_available_subresources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#cloudformationserviceresourceget_available_subresources-method)
        """

    async def create_stack(
        self, **kwargs: Unpack[CreateStackInputServiceResourceCreateStackTypeDef]
    ) -> _Stack:
        """
        Creates a stack as specified in the template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/create_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#cloudformationserviceresourcecreate_stack-method)
        """

    async def Event(self, id: str) -> _Event:
        """
        Creates a Event resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/Event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#cloudformationserviceresourceevent-method)
        """

    async def Stack(self, name: str) -> _Stack:
        """
        Creates a Stack resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/Stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#cloudformationserviceresourcestack-method)
        """

    async def StackResource(self, stack_name: str, logical_id: str) -> _StackResource:
        """
        Creates a StackResource resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/StackResource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#cloudformationserviceresourcestackresource-method)
        """

    async def StackResourceSummary(self, stack_name: str, logical_id: str) -> _StackResourceSummary:
        """
        Creates a StackResourceSummary resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/service-resource/StackResourceSummary.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/service_resource/#cloudformationserviceresourcestackresourcesummary-method)
        """
