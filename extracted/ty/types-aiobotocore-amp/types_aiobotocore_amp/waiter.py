"""
Type annotations for amp service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_amp.client import PrometheusServiceClient
    from types_aiobotocore_amp.waiter import (
        ScraperActiveWaiter,
        ScraperDeletedWaiter,
        WorkspaceActiveWaiter,
        WorkspaceDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("amp") as client:
        client: PrometheusServiceClient

        scraper_active_waiter: ScraperActiveWaiter = client.get_waiter("scraper_active")
        scraper_deleted_waiter: ScraperDeletedWaiter = client.get_waiter("scraper_deleted")
        workspace_active_waiter: WorkspaceActiveWaiter = client.get_waiter("workspace_active")
        workspace_deleted_waiter: WorkspaceDeletedWaiter = client.get_waiter("workspace_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeScraperRequestWaitExtraTypeDef,
    DescribeScraperRequestWaitTypeDef,
    DescribeWorkspaceRequestWaitExtraTypeDef,
    DescribeWorkspaceRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ScraperActiveWaiter",
    "ScraperDeletedWaiter",
    "WorkspaceActiveWaiter",
    "WorkspaceDeletedWaiter",
)


class ScraperActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/waiter/ScraperActive.html#PrometheusService.Waiter.ScraperActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#scraperactivewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScraperRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/waiter/ScraperActive.html#PrometheusService.Waiter.ScraperActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#scraperactivewaiter)
        """


class ScraperDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/waiter/ScraperDeleted.html#PrometheusService.Waiter.ScraperDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#scraperdeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScraperRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/waiter/ScraperDeleted.html#PrometheusService.Waiter.ScraperDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#scraperdeletedwaiter)
        """


class WorkspaceActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/waiter/WorkspaceActive.html#PrometheusService.Waiter.WorkspaceActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#workspaceactivewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeWorkspaceRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/waiter/WorkspaceActive.html#PrometheusService.Waiter.WorkspaceActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#workspaceactivewaiter)
        """


class WorkspaceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/waiter/WorkspaceDeleted.html#PrometheusService.Waiter.WorkspaceDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#workspacedeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeWorkspaceRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp/waiter/WorkspaceDeleted.html#PrometheusService.Waiter.WorkspaceDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/waiters/#workspacedeletedwaiter)
        """
