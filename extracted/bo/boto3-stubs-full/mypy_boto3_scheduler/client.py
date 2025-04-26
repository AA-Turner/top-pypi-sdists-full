"""
Type annotations for scheduler service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_scheduler.client import EventBridgeSchedulerClient

    session = Session()
    client: EventBridgeSchedulerClient = session.client("scheduler")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
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
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("EventBridgeSchedulerClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class EventBridgeSchedulerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EventBridgeSchedulerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler.html#EventBridgeScheduler.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#generate_presigned_url)
        """

    def create_schedule(
        self, **kwargs: Unpack[CreateScheduleInputTypeDef]
    ) -> CreateScheduleOutputTypeDef:
        """
        Creates the specified schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/create_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#create_schedule)
        """

    def create_schedule_group(
        self, **kwargs: Unpack[CreateScheduleGroupInputTypeDef]
    ) -> CreateScheduleGroupOutputTypeDef:
        """
        Creates the specified schedule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/create_schedule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#create_schedule_group)
        """

    def delete_schedule(self, **kwargs: Unpack[DeleteScheduleInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/delete_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#delete_schedule)
        """

    def delete_schedule_group(
        self, **kwargs: Unpack[DeleteScheduleGroupInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified schedule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/delete_schedule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#delete_schedule_group)
        """

    def get_schedule(self, **kwargs: Unpack[GetScheduleInputTypeDef]) -> GetScheduleOutputTypeDef:
        """
        Retrieves the specified schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/get_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#get_schedule)
        """

    def get_schedule_group(
        self, **kwargs: Unpack[GetScheduleGroupInputTypeDef]
    ) -> GetScheduleGroupOutputTypeDef:
        """
        Retrieves the specified schedule group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/get_schedule_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#get_schedule_group)
        """

    def list_schedule_groups(
        self, **kwargs: Unpack[ListScheduleGroupsInputTypeDef]
    ) -> ListScheduleGroupsOutputTypeDef:
        """
        Returns a paginated list of your schedule groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/list_schedule_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#list_schedule_groups)
        """

    def list_schedules(
        self, **kwargs: Unpack[ListSchedulesInputTypeDef]
    ) -> ListSchedulesOutputTypeDef:
        """
        Returns a paginated list of your EventBridge Scheduler schedules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/list_schedules.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#list_schedules)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with the Scheduler resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified EventBridge
        Scheduler resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified EventBridge Scheduler schedule
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#untag_resource)
        """

    def update_schedule(
        self, **kwargs: Unpack[UpdateScheduleInputTypeDef]
    ) -> UpdateScheduleOutputTypeDef:
        """
        Updates the specified schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/update_schedule.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#update_schedule)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_schedule_groups"]
    ) -> ListScheduleGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_schedules"]
    ) -> ListSchedulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/client/#get_paginator)
        """
