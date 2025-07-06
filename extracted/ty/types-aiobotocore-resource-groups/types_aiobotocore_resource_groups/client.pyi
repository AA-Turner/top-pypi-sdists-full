"""
Type annotations for resource-groups service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_resource_groups.client import ResourceGroupsClient

    session = get_session()
    async with session.create_client("resource-groups") as client:
        client: ResourceGroupsClient
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
    ListGroupingStatusesPaginator,
    ListGroupResourcesPaginator,
    ListGroupsPaginator,
    ListTagSyncTasksPaginator,
    SearchResourcesPaginator,
)
from .type_defs import (
    CancelTagSyncTaskInputTypeDef,
    CreateGroupInputTypeDef,
    CreateGroupOutputTypeDef,
    DeleteGroupInputTypeDef,
    DeleteGroupOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAccountSettingsOutputTypeDef,
    GetGroupConfigurationInputTypeDef,
    GetGroupConfigurationOutputTypeDef,
    GetGroupInputTypeDef,
    GetGroupOutputTypeDef,
    GetGroupQueryInputTypeDef,
    GetGroupQueryOutputTypeDef,
    GetTagsInputTypeDef,
    GetTagsOutputTypeDef,
    GetTagSyncTaskInputTypeDef,
    GetTagSyncTaskOutputTypeDef,
    GroupResourcesInputTypeDef,
    GroupResourcesOutputTypeDef,
    ListGroupingStatusesInputTypeDef,
    ListGroupingStatusesOutputTypeDef,
    ListGroupResourcesInputTypeDef,
    ListGroupResourcesOutputTypeDef,
    ListGroupsInputTypeDef,
    ListGroupsOutputTypeDef,
    ListTagSyncTasksInputTypeDef,
    ListTagSyncTasksOutputTypeDef,
    PutGroupConfigurationInputTypeDef,
    SearchResourcesInputTypeDef,
    SearchResourcesOutputTypeDef,
    StartTagSyncTaskInputTypeDef,
    StartTagSyncTaskOutputTypeDef,
    TagInputTypeDef,
    TagOutputTypeDef,
    UngroupResourcesInputTypeDef,
    UngroupResourcesOutputTypeDef,
    UntagInputTypeDef,
    UntagOutputTypeDef,
    UpdateAccountSettingsInputTypeDef,
    UpdateAccountSettingsOutputTypeDef,
    UpdateGroupInputTypeDef,
    UpdateGroupOutputTypeDef,
    UpdateGroupQueryInputTypeDef,
    UpdateGroupQueryOutputTypeDef,
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

__all__ = ("ResourceGroupsClient",)

class Exceptions(BaseClientExceptions):
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]

class ResourceGroupsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ResourceGroupsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#generate_presigned_url)
        """

    async def cancel_tag_sync_task(
        self, **kwargs: Unpack[CancelTagSyncTaskInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels the specified tag-sync task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/cancel_tag_sync_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#cancel_tag_sync_task)
        """

    async def create_group(
        self, **kwargs: Unpack[CreateGroupInputTypeDef]
    ) -> CreateGroupOutputTypeDef:
        """
        Creates a resource group with the specified name and description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/create_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#create_group)
        """

    async def delete_group(
        self, **kwargs: Unpack[DeleteGroupInputTypeDef]
    ) -> DeleteGroupOutputTypeDef:
        """
        Deletes the specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/delete_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#delete_group)
        """

    async def get_account_settings(self) -> GetAccountSettingsOutputTypeDef:
        """
        Retrieves the current status of optional features in Resource Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_account_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_account_settings)
        """

    async def get_group(self, **kwargs: Unpack[GetGroupInputTypeDef]) -> GetGroupOutputTypeDef:
        """
        Returns information about a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_group)
        """

    async def get_group_configuration(
        self, **kwargs: Unpack[GetGroupConfigurationInputTypeDef]
    ) -> GetGroupConfigurationOutputTypeDef:
        """
        Retrieves the service configuration associated with the specified resource
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_group_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_group_configuration)
        """

    async def get_group_query(
        self, **kwargs: Unpack[GetGroupQueryInputTypeDef]
    ) -> GetGroupQueryOutputTypeDef:
        """
        Retrieves the resource query associated with the specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_group_query.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_group_query)
        """

    async def get_tag_sync_task(
        self, **kwargs: Unpack[GetTagSyncTaskInputTypeDef]
    ) -> GetTagSyncTaskOutputTypeDef:
        """
        Returns information about a specified tag-sync task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_tag_sync_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_tag_sync_task)
        """

    async def get_tags(self, **kwargs: Unpack[GetTagsInputTypeDef]) -> GetTagsOutputTypeDef:
        """
        Returns a list of tags that are associated with a resource group, specified by
        an Amazon resource name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_tags)
        """

    async def group_resources(
        self, **kwargs: Unpack[GroupResourcesInputTypeDef]
    ) -> GroupResourcesOutputTypeDef:
        """
        Adds the specified resources to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/group_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#group_resources)
        """

    async def list_group_resources(
        self, **kwargs: Unpack[ListGroupResourcesInputTypeDef]
    ) -> ListGroupResourcesOutputTypeDef:
        """
        Returns a list of Amazon resource names (ARNs) of the resources that are
        members of a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/list_group_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#list_group_resources)
        """

    async def list_grouping_statuses(
        self, **kwargs: Unpack[ListGroupingStatusesInputTypeDef]
    ) -> ListGroupingStatusesOutputTypeDef:
        """
        Returns the status of the last grouping or ungrouping action for each resource
        in the specified application group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/list_grouping_statuses.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#list_grouping_statuses)
        """

    async def list_groups(
        self, **kwargs: Unpack[ListGroupsInputTypeDef]
    ) -> ListGroupsOutputTypeDef:
        """
        Returns a list of existing Resource Groups in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/list_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#list_groups)
        """

    async def list_tag_sync_tasks(
        self, **kwargs: Unpack[ListTagSyncTasksInputTypeDef]
    ) -> ListTagSyncTasksOutputTypeDef:
        """
        Returns a list of tag-sync tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/list_tag_sync_tasks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#list_tag_sync_tasks)
        """

    async def put_group_configuration(
        self, **kwargs: Unpack[PutGroupConfigurationInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches a service configuration to the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/put_group_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#put_group_configuration)
        """

    async def search_resources(
        self, **kwargs: Unpack[SearchResourcesInputTypeDef]
    ) -> SearchResourcesOutputTypeDef:
        """
        Returns a list of Amazon Web Services resource identifiers that matches the
        specified query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/search_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#search_resources)
        """

    async def start_tag_sync_task(
        self, **kwargs: Unpack[StartTagSyncTaskInputTypeDef]
    ) -> StartTagSyncTaskOutputTypeDef:
        """
        Creates a new tag-sync task to onboard and sync resources tagged with a
        specific tag key-value pair to an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/start_tag_sync_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#start_tag_sync_task)
        """

    async def tag(self, **kwargs: Unpack[TagInputTypeDef]) -> TagOutputTypeDef:
        """
        Adds tags to a resource group with the specified Amazon resource name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/tag.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#tag)
        """

    async def ungroup_resources(
        self, **kwargs: Unpack[UngroupResourcesInputTypeDef]
    ) -> UngroupResourcesOutputTypeDef:
        """
        Removes the specified resources from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/ungroup_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#ungroup_resources)
        """

    async def untag(self, **kwargs: Unpack[UntagInputTypeDef]) -> UntagOutputTypeDef:
        """
        Deletes tags from a specified resource group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/untag.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#untag)
        """

    async def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsInputTypeDef]
    ) -> UpdateAccountSettingsOutputTypeDef:
        """
        Turns on or turns off optional features in Resource Groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/update_account_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#update_account_settings)
        """

    async def update_group(
        self, **kwargs: Unpack[UpdateGroupInputTypeDef]
    ) -> UpdateGroupOutputTypeDef:
        """
        Updates the description for an existing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/update_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#update_group)
        """

    async def update_group_query(
        self, **kwargs: Unpack[UpdateGroupQueryInputTypeDef]
    ) -> UpdateGroupQueryOutputTypeDef:
        """
        Updates the resource query of a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/update_group_query.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#update_group_query)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_group_resources"]
    ) -> ListGroupResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_grouping_statuses"]
    ) -> ListGroupingStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_groups"]
    ) -> ListGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tag_sync_tasks"]
    ) -> ListTagSyncTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_resources"]
    ) -> SearchResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resource-groups.html#ResourceGroups.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resource_groups/client/)
        """
