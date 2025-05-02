"""
Type annotations for scheduler service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_scheduler.client import EventBridgeSchedulerClient
    from types_aiobotocore_scheduler.paginator import (
        ListScheduleGroupsPaginator,
        ListSchedulesPaginator,
    )

    session = get_session()
    with session.create_client("scheduler") as client:
        client: EventBridgeSchedulerClient

        list_schedule_groups_paginator: ListScheduleGroupsPaginator = client.get_paginator("list_schedule_groups")
        list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListScheduleGroupsInputPaginateTypeDef,
    ListScheduleGroupsOutputTypeDef,
    ListSchedulesInputPaginateTypeDef,
    ListSchedulesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListScheduleGroupsPaginator", "ListSchedulesPaginator")


if TYPE_CHECKING:
    _ListScheduleGroupsPaginatorBase = AioPaginator[ListScheduleGroupsOutputTypeDef]
else:
    _ListScheduleGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListScheduleGroupsPaginator(_ListScheduleGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListScheduleGroups.html#EventBridgeScheduler.Paginator.ListScheduleGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/#listschedulegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScheduleGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListScheduleGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListScheduleGroups.html#EventBridgeScheduler.Paginator.ListScheduleGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/#listschedulegroupspaginator)
        """


if TYPE_CHECKING:
    _ListSchedulesPaginatorBase = AioPaginator[ListSchedulesOutputTypeDef]
else:
    _ListSchedulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSchedulesPaginator(_ListSchedulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListSchedules.html#EventBridgeScheduler.Paginator.ListSchedules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/#listschedulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchedulesInputPaginateTypeDef]
    ) -> AioPageIterator[ListSchedulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListSchedules.html#EventBridgeScheduler.Paginator.ListSchedules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_scheduler/paginators/#listschedulespaginator)
        """
