"""
Main interface for iot1click-projects service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot1click_projects import (
        Client,
        IoT1ClickProjectsClient,
        ListPlacementsPaginator,
        ListProjectsPaginator,
    )

    session = get_session()
    async with session.create_client("iot1click-projects") as client:
        client: IoT1ClickProjectsClient
        ...


    list_placements_paginator: ListPlacementsPaginator = client.get_paginator("list_placements")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import IoT1ClickProjectsClient
from .paginator import ListPlacementsPaginator, ListProjectsPaginator

Client = IoT1ClickProjectsClient


__all__ = ("Client", "IoT1ClickProjectsClient", "ListPlacementsPaginator", "ListProjectsPaginator")
