"""
Type annotations for sagemakertrainingsessionruntime service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemakertrainingsessionruntime.client import SageMakerTrainingSessionRuntimeClient

    session = Session()
    client: SageMakerTrainingSessionRuntimeClient = session.client("sagemakertrainingsessionruntime")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    ExecuteSamplingOperationInputTypeDef,
    ExecuteSamplingOperationOutputTypeDef,
    ExecuteTrainingOperationInputTypeDef,
    ExecuteTrainingOperationOutputTypeDef,
    GetSamplingOperationResultInputTypeDef,
    GetSamplingOperationResultOutputTypeDef,
    GetTrainingOperationResultInputTypeDef,
    GetTrainingOperationResultOutputTypeDef,
    SampleTrainingSessionInputTypeDef,
    SampleTrainingSessionOutputTypeDef,
    SampleTrainingSessionWithResponseStreamInputTypeDef,
    SampleTrainingSessionWithResponseStreamOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SageMakerTrainingSessionRuntimeClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class SageMakerTrainingSessionRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime.html#SageMakerTrainingSessionRuntime.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakerTrainingSessionRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime.html#SageMakerTrainingSessionRuntime.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/#generate_presigned_url)
        """

    def execute_sampling_operation(
        self, **kwargs: Unpack[ExecuteSamplingOperationInputTypeDef]
    ) -> ExecuteSamplingOperationOutputTypeDef:
        """
        Submits an asynchronous sampling operation to generate text or compute
        log-probabilities from the model associated with the specified training
        session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime/client/execute_sampling_operation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/#execute_sampling_operation)
        """

    def execute_training_operation(
        self, **kwargs: Unpack[ExecuteTrainingOperationInputTypeDef]
    ) -> ExecuteTrainingOperationOutputTypeDef:
        """
        Submits an asynchronous training operation to the specified training session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime/client/execute_training_operation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/#execute_training_operation)
        """

    def get_sampling_operation_result(
        self, **kwargs: Unpack[GetSamplingOperationResultInputTypeDef]
    ) -> GetSamplingOperationResultOutputTypeDef:
        """
        Retrieves the current status and result of a previously submitted sampling
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime/client/get_sampling_operation_result.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/#get_sampling_operation_result)
        """

    def get_training_operation_result(
        self, **kwargs: Unpack[GetTrainingOperationResultInputTypeDef]
    ) -> GetTrainingOperationResultOutputTypeDef:
        """
        Retrieves the current status and result of a previously submitted training
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime/client/get_training_operation_result.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/#get_training_operation_result)
        """

    def sample_training_session(
        self, **kwargs: Unpack[SampleTrainingSessionInputTypeDef]
    ) -> SampleTrainingSessionOutputTypeDef:
        """
        Sends an inference request to the model associated with the specified training
        session and returns the response synchronously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime/client/sample_training_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/#sample_training_session)
        """

    def sample_training_session_with_response_stream(
        self, **kwargs: Unpack[SampleTrainingSessionWithResponseStreamInputTypeDef]
    ) -> SampleTrainingSessionWithResponseStreamOutputTypeDef:
        """
        Streams inference responses from the model associated with the specified
        training session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakertrainingsessionruntime/client/sample_training_session_with_response_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemakertrainingsessionruntime/client/#sample_training_session_with_response_stream)
        """
