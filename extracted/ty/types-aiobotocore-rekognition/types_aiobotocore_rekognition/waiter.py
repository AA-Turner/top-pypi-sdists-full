"""
Type annotations for rekognition service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rekognition.client import RekognitionClient
    from types_aiobotocore_rekognition.waiter import (
        ProjectVersionRunningWaiter,
        ProjectVersionTrainingCompletedWaiter,
    )

    session = get_session()
    async with session.create_client("rekognition") as client:
        client: RekognitionClient

        project_version_running_waiter: ProjectVersionRunningWaiter = client.get_waiter("project_version_running")
        project_version_training_completed_waiter: ProjectVersionTrainingCompletedWaiter = client.get_waiter("project_version_training_completed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeProjectVersionsRequestWaitExtraTypeDef,
    DescribeProjectVersionsRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ProjectVersionRunningWaiter", "ProjectVersionTrainingCompletedWaiter")


class ProjectVersionRunningWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/waiter/ProjectVersionRunning.html#Rekognition.Waiter.ProjectVersionRunning)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/#projectversionrunningwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeProjectVersionsRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/waiter/ProjectVersionRunning.html#Rekognition.Waiter.ProjectVersionRunning.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/#projectversionrunningwaiter)
        """


class ProjectVersionTrainingCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/waiter/ProjectVersionTrainingCompleted.html#Rekognition.Waiter.ProjectVersionTrainingCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/#projectversiontrainingcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeProjectVersionsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition/waiter/ProjectVersionTrainingCompleted.html#Rekognition.Waiter.ProjectVersionTrainingCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rekognition/waiters/#projectversiontrainingcompletedwaiter)
        """
