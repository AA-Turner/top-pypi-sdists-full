"""
Type annotations for bedrock-runtime service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_runtime.client import BedrockRuntimeClient

    session = get_session()
    async with session.create_client("bedrock-runtime") as client:
        client: BedrockRuntimeClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListAsyncInvokesPaginator
from .type_defs import (
    ApplyGuardrailRequestTypeDef,
    ApplyGuardrailResponseTypeDef,
    ConverseRequestTypeDef,
    ConverseResponseTypeDef,
    ConverseStreamRequestTypeDef,
    ConverseStreamResponseTypeDef,
    GetAsyncInvokeRequestTypeDef,
    GetAsyncInvokeResponseTypeDef,
    InvokeModelRequestTypeDef,
    InvokeModelResponseTypeDef,
    InvokeModelWithBidirectionalStreamRequestTypeDef,
    InvokeModelWithBidirectionalStreamResponseTypeDef,
    InvokeModelWithResponseStreamRequestTypeDef,
    InvokeModelWithResponseStreamResponseTypeDef,
    ListAsyncInvokesRequestTypeDef,
    ListAsyncInvokesResponseTypeDef,
    StartAsyncInvokeRequestTypeDef,
    StartAsyncInvokeResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("BedrockRuntimeClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ModelErrorException: Type[BotocoreClientError]
    ModelNotReadyException: Type[BotocoreClientError]
    ModelStreamErrorException: Type[BotocoreClientError]
    ModelTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BedrockRuntimeClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BedrockRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#generate_presigned_url)
        """

    async def apply_guardrail(
        self, **kwargs: Unpack[ApplyGuardrailRequestTypeDef]
    ) -> ApplyGuardrailResponseTypeDef:
        """
        The action to apply a guardrail.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/apply_guardrail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#apply_guardrail)
        """

    async def converse(self, **kwargs: Unpack[ConverseRequestTypeDef]) -> ConverseResponseTypeDef:
        """
        Sends messages to the specified Amazon Bedrock model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#converse)
        """

    async def converse_stream(
        self, **kwargs: Unpack[ConverseStreamRequestTypeDef]
    ) -> ConverseStreamResponseTypeDef:
        """
        Sends messages to the specified Amazon Bedrock model and returns the response
        in a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#converse_stream)
        """

    async def get_async_invoke(
        self, **kwargs: Unpack[GetAsyncInvokeRequestTypeDef]
    ) -> GetAsyncInvokeResponseTypeDef:
        """
        Retrieve information about an asynchronous invocation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/get_async_invoke.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#get_async_invoke)
        """

    async def invoke_model(
        self, **kwargs: Unpack[InvokeModelRequestTypeDef]
    ) -> InvokeModelResponseTypeDef:
        """
        Invokes the specified Amazon Bedrock model to run inference using the prompt
        and inference parameters provided in the request body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/invoke_model.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#invoke_model)
        """

    async def invoke_model_with_bidirectional_stream(
        self, **kwargs: Unpack[InvokeModelWithBidirectionalStreamRequestTypeDef]
    ) -> InvokeModelWithBidirectionalStreamResponseTypeDef:
        """
        Invoke the specified Amazon Bedrock model to run inference using the
        bidirectional stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/invoke_model_with_bidirectional_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#invoke_model_with_bidirectional_stream)
        """

    async def invoke_model_with_response_stream(
        self, **kwargs: Unpack[InvokeModelWithResponseStreamRequestTypeDef]
    ) -> InvokeModelWithResponseStreamResponseTypeDef:
        """
        Invoke the specified Amazon Bedrock model to run inference using the prompt and
        inference parameters provided in the request body.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/invoke_model_with_response_stream.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#invoke_model_with_response_stream)
        """

    async def list_async_invokes(
        self, **kwargs: Unpack[ListAsyncInvokesRequestTypeDef]
    ) -> ListAsyncInvokesResponseTypeDef:
        """
        Lists asynchronous invocations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/list_async_invokes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#list_async_invokes)
        """

    async def start_async_invoke(
        self, **kwargs: Unpack[StartAsyncInvokeRequestTypeDef]
    ) -> StartAsyncInvokeResponseTypeDef:
        """
        Starts an asynchronous invocation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/start_async_invoke.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#start_async_invoke)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_async_invokes"]
    ) -> ListAsyncInvokesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html#BedrockRuntime.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_runtime/client/)
        """
