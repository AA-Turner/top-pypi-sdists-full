"""
Type annotations for scheduler service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_scheduler.client import EventBridgeSchedulerClient

    session = get_session()
    async with session.create_client("scheduler") as client:
        client: EventBridgeSchedulerClient
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

from .paginator import ListScheduleGroupsPaginator, ListSchedulesPaginator
from .type_defs import (
    CreateScheduleGroupInputTypeDef,
    CreateScheduleGroupOutputTypeDef,
    CreateScheduleInputTypeDef,
    CreateScheduleOutputTypeDef,
    DeleteScheduleGroupInputTypeDef,
    DeleteScheduleInputTypeDef,
    GetScheduleGroupInputTypeDef,
    GetScheduleGroupOutputTypeDef,
    GetScheduleInputTypeDef,
    GetScheduleOutputTypeDef,
    ListScheduleGroupsInputTypeDef,
    ListScheduleGroupsOutputTypeDef,
    ListSchedulesInputTypeDef,
    ListSchedulesOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateScheduleInputTypeDef,
    UpdateScheduleOutputTypeDef,
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

__all__ = ("EventBridgeSchedulerClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class EventBridgeSchedulerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EventBridgeSchedulerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#generate_presigned_url)
        """

    async def create_schedule(
        self, **kwargs: Unpack[CreateScheduleInputTypeDef]
    ) -> CreateScheduleOutputTypeDef:
        """
        Creates the specified schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/create_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#create_schedule)
        """

    async def create_schedule_group(
        self, **kwargs: Unpack[CreateScheduleGroupInputTypeDef]
    ) -> CreateScheduleGroupOutputTypeDef:
        """
        Creates the specified schedule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/create_schedule_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#create_schedule_group)
        """

    async def delete_schedule(self, **kwargs: Unpack[DeleteScheduleInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/delete_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#delete_schedule)
        """

    async def delete_schedule_group(
        self, **kwargs: Unpack[DeleteScheduleGroupInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified schedule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/delete_schedule_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#delete_schedule_group)
        """

    async def get_schedule(
        self, **kwargs: Unpack[GetScheduleInputTypeDef]
    ) -> GetScheduleOutputTypeDef:
        """
        Retrieves the specified schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/get_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#get_schedule)
        """

    async def get_schedule_group(
        self, **kwargs: Unpack[GetScheduleGroupInputTypeDef]
    ) -> GetScheduleGroupOutputTypeDef:
        """
        Retrieves the specified schedule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/get_schedule_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#get_schedule_group)
        """

    async def list_schedule_groups(
        self, **kwargs: Unpack[ListScheduleGroupsInputTypeDef]
    ) -> ListScheduleGroupsOutputTypeDef:
        """
        Returns a paginated list of your schedule groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/list_schedule_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#list_schedule_groups)
        """

    async def list_schedules(
        self, **kwargs: Unpack[ListSchedulesInputTypeDef]
    ) -> ListSchedulesOutputTypeDef:
        """
        Returns a paginated list of your EventBridge Scheduler schedules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/list_schedules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#list_schedules)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with the Scheduler resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#list_tags_for_resource)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified EventBridge
        Scheduler resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified EventBridge Scheduler schedule
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#untag_resource)
        """

    async def update_schedule(
        self, **kwargs: Unpack[UpdateScheduleInputTypeDef]
    ) -> UpdateScheduleOutputTypeDef:
        """
        Updates the specified schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/update_schedule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#update_schedule)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_schedule_groups"]
    ) -> ListScheduleGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_schedules"]
    ) -> ListSchedulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/client/)
        """
