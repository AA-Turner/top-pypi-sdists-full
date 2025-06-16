"""
Type annotations for sagemaker service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker.client import SageMakerClient
    from types_aiobotocore_sagemaker.waiter import (
        EndpointDeletedWaiter,
        EndpointInServiceWaiter,
        ImageCreatedWaiter,
        ImageDeletedWaiter,
        ImageUpdatedWaiter,
        ImageVersionCreatedWaiter,
        ImageVersionDeletedWaiter,
        NotebookInstanceDeletedWaiter,
        NotebookInstanceInServiceWaiter,
        NotebookInstanceStoppedWaiter,
        ProcessingJobCompletedOrStoppedWaiter,
        TrainingJobCompletedOrStoppedWaiter,
        TransformJobCompletedOrStoppedWaiter,
    )

    session = get_session()
    async with session.create_client("sagemaker") as client:
        client: SageMakerClient

        endpoint_deleted_waiter: EndpointDeletedWaiter = client.get_waiter("endpoint_deleted")
        endpoint_in_service_waiter: EndpointInServiceWaiter = client.get_waiter("endpoint_in_service")
        image_created_waiter: ImageCreatedWaiter = client.get_waiter("image_created")
        image_deleted_waiter: ImageDeletedWaiter = client.get_waiter("image_deleted")
        image_updated_waiter: ImageUpdatedWaiter = client.get_waiter("image_updated")
        image_version_created_waiter: ImageVersionCreatedWaiter = client.get_waiter("image_version_created")
        image_version_deleted_waiter: ImageVersionDeletedWaiter = client.get_waiter("image_version_deleted")
        notebook_instance_deleted_waiter: NotebookInstanceDeletedWaiter = client.get_waiter("notebook_instance_deleted")
        notebook_instance_in_service_waiter: NotebookInstanceInServiceWaiter = client.get_waiter("notebook_instance_in_service")
        notebook_instance_stopped_waiter: NotebookInstanceStoppedWaiter = client.get_waiter("notebook_instance_stopped")
        processing_job_completed_or_stopped_waiter: ProcessingJobCompletedOrStoppedWaiter = client.get_waiter("processing_job_completed_or_stopped")
        training_job_completed_or_stopped_waiter: TrainingJobCompletedOrStoppedWaiter = client.get_waiter("training_job_completed_or_stopped")
        transform_job_completed_or_stopped_waiter: TransformJobCompletedOrStoppedWaiter = client.get_waiter("transform_job_completed_or_stopped")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeEndpointInputWaitExtraTypeDef,
    DescribeEndpointInputWaitTypeDef,
    DescribeImageRequestWaitExtraExtraTypeDef,
    DescribeImageRequestWaitExtraTypeDef,
    DescribeImageRequestWaitTypeDef,
    DescribeImageVersionRequestWaitExtraTypeDef,
    DescribeImageVersionRequestWaitTypeDef,
    DescribeNotebookInstanceInputWaitExtraExtraTypeDef,
    DescribeNotebookInstanceInputWaitExtraTypeDef,
    DescribeNotebookInstanceInputWaitTypeDef,
    DescribeProcessingJobRequestWaitTypeDef,
    DescribeTrainingJobRequestWaitTypeDef,
    DescribeTransformJobRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "EndpointDeletedWaiter",
    "EndpointInServiceWaiter",
    "ImageCreatedWaiter",
    "ImageDeletedWaiter",
    "ImageUpdatedWaiter",
    "ImageVersionCreatedWaiter",
    "ImageVersionDeletedWaiter",
    "NotebookInstanceDeletedWaiter",
    "NotebookInstanceInServiceWaiter",
    "NotebookInstanceStoppedWaiter",
    "ProcessingJobCompletedOrStoppedWaiter",
    "TrainingJobCompletedOrStoppedWaiter",
    "TransformJobCompletedOrStoppedWaiter",
)

class EndpointDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/EndpointDeleted.html#SageMaker.Waiter.EndpointDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#endpointdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndpointInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/EndpointDeleted.html#SageMaker.Waiter.EndpointDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#endpointdeletedwaiter)
        """

class EndpointInServiceWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/EndpointInService.html#SageMaker.Waiter.EndpointInService)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#endpointinservicewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEndpointInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/EndpointInService.html#SageMaker.Waiter.EndpointInService.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#endpointinservicewaiter)
        """

class ImageCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageCreated.html#SageMaker.Waiter.ImageCreated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imagecreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImageRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageCreated.html#SageMaker.Waiter.ImageCreated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imagecreatedwaiter)
        """

class ImageDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageDeleted.html#SageMaker.Waiter.ImageDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imagedeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImageRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageDeleted.html#SageMaker.Waiter.ImageDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imagedeletedwaiter)
        """

class ImageUpdatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageUpdated.html#SageMaker.Waiter.ImageUpdated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imageupdatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImageRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageUpdated.html#SageMaker.Waiter.ImageUpdated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imageupdatedwaiter)
        """

class ImageVersionCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageVersionCreated.html#SageMaker.Waiter.ImageVersionCreated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imageversioncreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImageVersionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageVersionCreated.html#SageMaker.Waiter.ImageVersionCreated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imageversioncreatedwaiter)
        """

class ImageVersionDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageVersionDeleted.html#SageMaker.Waiter.ImageVersionDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imageversiondeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImageVersionRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ImageVersionDeleted.html#SageMaker.Waiter.ImageVersionDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#imageversiondeletedwaiter)
        """

class NotebookInstanceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceDeleted.html#SageMaker.Waiter.NotebookInstanceDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#notebookinstancedeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNotebookInstanceInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceDeleted.html#SageMaker.Waiter.NotebookInstanceDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#notebookinstancedeletedwaiter)
        """

class NotebookInstanceInServiceWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceInService.html#SageMaker.Waiter.NotebookInstanceInService)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#notebookinstanceinservicewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNotebookInstanceInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceInService.html#SageMaker.Waiter.NotebookInstanceInService.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#notebookinstanceinservicewaiter)
        """

class NotebookInstanceStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceStopped.html#SageMaker.Waiter.NotebookInstanceStopped)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#notebookinstancestoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeNotebookInstanceInputWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/NotebookInstanceStopped.html#SageMaker.Waiter.NotebookInstanceStopped.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#notebookinstancestoppedwaiter)
        """

class ProcessingJobCompletedOrStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ProcessingJobCompletedOrStopped.html#SageMaker.Waiter.ProcessingJobCompletedOrStopped)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#processingjobcompletedorstoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeProcessingJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/ProcessingJobCompletedOrStopped.html#SageMaker.Waiter.ProcessingJobCompletedOrStopped.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#processingjobcompletedorstoppedwaiter)
        """

class TrainingJobCompletedOrStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/TrainingJobCompletedOrStopped.html#SageMaker.Waiter.TrainingJobCompletedOrStopped)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#trainingjobcompletedorstoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTrainingJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/TrainingJobCompletedOrStopped.html#SageMaker.Waiter.TrainingJobCompletedOrStopped.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#trainingjobcompletedorstoppedwaiter)
        """

class TransformJobCompletedOrStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/TransformJobCompletedOrStopped.html#SageMaker.Waiter.TransformJobCompletedOrStopped)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#transformjobcompletedorstoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTransformJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/waiter/TransformJobCompletedOrStopped.html#SageMaker.Waiter.TransformJobCompletedOrStopped.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker/waiters/#transformjobcompletedorstoppedwaiter)
        """
