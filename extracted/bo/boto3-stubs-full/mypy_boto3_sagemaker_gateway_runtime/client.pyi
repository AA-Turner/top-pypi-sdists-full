"""
Type annotations for sagemaker-gateway-runtime service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_gateway_runtime/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemaker_gateway_runtime.client import SageMakerGatewayRuntimeClient

    session = Session()
    client: SageMakerGatewayRuntimeClient = session.client("sagemaker-gateway-runtime")
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
    InvokeGlobalInferenceGatewayInputTypeDef,
    InvokeGlobalInferenceGatewayOutputTypeDef,
    InvokeGlobalInferenceGatewayWithResponseStreamInputTypeDef,
    InvokeGlobalInferenceGatewayWithResponseStreamOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("SageMakerGatewayRuntimeClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    BadGatewayException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    GatewayTimeoutException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    InternalStreamFailure: type[BotocoreClientError]
    ModelStreamError: type[BotocoreClientError]
    PayloadTooLargeException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceUnavailableException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]

class SageMakerGatewayRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-gateway-runtime.html#SageMakerGatewayRuntime.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_gateway_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakerGatewayRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-gateway-runtime.html#SageMakerGatewayRuntime.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_gateway_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-gateway-runtime/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_gateway_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-gateway-runtime/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_gateway_runtime/client/#generate_presigned_url)
        """

    def invoke_global_inference_gateway(
        self, **kwargs: Unpack[InvokeGlobalInferenceGatewayInputTypeDef]
    ) -> InvokeGlobalInferenceGatewayOutputTypeDef:
        """
        Buffered (non-streaming) inference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-gateway-runtime/client/invoke_global_inference_gateway.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_gateway_runtime/client/#invoke_global_inference_gateway)
        """

    def invoke_global_inference_gateway_with_response_stream(
        self, **kwargs: Unpack[InvokeGlobalInferenceGatewayWithResponseStreamInputTypeDef]
    ) -> InvokeGlobalInferenceGatewayWithResponseStreamOutputTypeDef:
        """
        Streaming inference.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-gateway-runtime/client/invoke_global_inference_gateway_with_response_stream.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_gateway_runtime/client/#invoke_global_inference_gateway_with_response_stream)
        """
