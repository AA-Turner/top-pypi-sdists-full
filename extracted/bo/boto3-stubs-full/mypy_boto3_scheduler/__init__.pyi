"""
Main interface for scheduler service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_scheduler/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_scheduler import (
        Client,
        EventBridgeSchedulerClient,
        ListScheduleGroupsPaginator,
        ListSchedulesPaginator,
    )

    session = Session()
    client: EventBridgeSchedulerClient = session.client("scheduler")

    list_schedule_groups_paginator: ListScheduleGroupsPaginator = client.get_paginator("list_schedule_groups")
    list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```
"""

from .client import EventBridgeSchedulerClient
from .paginator import ListScheduleGroupsPaginator, ListSchedulesPaginator

Client = EventBridgeSchedulerClient

__all__ = (
    "Client",
    "EventBridgeSchedulerClient",
    "ListScheduleGroupsPaginator",
    "ListSchedulesPaginator",
)
