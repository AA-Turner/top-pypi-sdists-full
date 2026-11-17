"""
Type annotations for sagemaker-inference-router-runtime service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_inference_router_runtime/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemaker_inference_router_runtime.client import SageMakerInferenceRouterRuntimeClient

    session = Session()
    client: SageMakerInferenceRouterRuntimeClient = session.client("sagemaker-inference-router-runtime")
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
    InvokeInferenceRouterAsyncInputTypeDef,
    InvokeInferenceRouterAsyncOutputTypeDef,
    InvokeInferenceRouterInputTypeDef,
    InvokeInferenceRouterOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SageMakerInferenceRouterRuntimeClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalDependencyException: type[BotocoreClientError]
    InternalFailure: type[BotocoreClientError]
    ModelError: type[BotocoreClientError]
    ModelNotReadyException: type[BotocoreClientError]
    RequestTimeoutException: type[BotocoreClientError]
    ServiceUnavailableException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class SageMakerInferenceRouterRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-inference-router-runtime.html#SageMakerInferenceRouterRuntime.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_inference_router_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakerInferenceRouterRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-inference-router-runtime.html#SageMakerInferenceRouterRuntime.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_inference_router_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-inference-router-runtime/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_inference_router_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-inference-router-runtime/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_inference_router_runtime/client/#generate_presigned_url)
        """

    def invoke_inference_router(
        self, **kwargs: Unpack[InvokeInferenceRouterInputTypeDef]
    ) -> InvokeInferenceRouterOutputTypeDef:
        """
        Sends a real-time inference request to an inference router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-inference-router-runtime/client/invoke_inference_router.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_inference_router_runtime/client/#invoke_inference_router)
        """

    def invoke_inference_router_async(
        self, **kwargs: Unpack[InvokeInferenceRouterAsyncInputTypeDef]
    ) -> InvokeInferenceRouterAsyncOutputTypeDef:
        """
        Submits an asynchronous inference request to an inference router.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-inference-router-runtime/client/invoke_inference_router_async.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_inference_router_runtime/client/#invoke_inference_router_async)
        """
