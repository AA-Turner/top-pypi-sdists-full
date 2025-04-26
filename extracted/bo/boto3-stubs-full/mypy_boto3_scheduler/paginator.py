"""
Type annotations for scheduler service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_scheduler.client import EventBridgeSchedulerClient
    from mypy_boto3_scheduler.paginator import (
        ListScheduleGroupsPaginator,
        ListSchedulesPaginator,
    )

    session = Session()
    client: EventBridgeSchedulerClient = session.client("scheduler")

    list_schedule_groups_paginator: ListScheduleGroupsPaginator = client.get_paginator("list_schedule_groups")
    list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListScheduleGroupsPaginatorBase = Paginator[ListScheduleGroupsOutputTypeDef]
else:
    _ListScheduleGroupsPaginatorBase = Paginator  # type: ignore[assignment]


class ListScheduleGroupsPaginator(_ListScheduleGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListScheduleGroups.html#EventBridgeScheduler.Paginator.ListScheduleGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/#listschedulegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScheduleGroupsInputPaginateTypeDef]
    ) -> PageIterator[ListScheduleGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListScheduleGroups.html#EventBridgeScheduler.Paginator.ListScheduleGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/#listschedulegroupspaginator)
        """


if TYPE_CHECKING:
    _ListSchedulesPaginatorBase = Paginator[ListSchedulesOutputTypeDef]
else:
    _ListSchedulesPaginatorBase = Paginator  # type: ignore[assignment]


class ListSchedulesPaginator(_ListSchedulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListSchedules.html#EventBridgeScheduler.Paginator.ListSchedules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/#listschedulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchedulesInputPaginateTypeDef]
    ) -> PageIterator[ListSchedulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/scheduler/paginator/ListSchedules.html#EventBridgeScheduler.Paginator.ListSchedules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/paginators/#listschedulespaginator)
        """
