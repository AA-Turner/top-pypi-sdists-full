"""
Type annotations for sagemaker-gateway-runtime service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_gateway_runtime/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_sagemaker_gateway_runtime.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from typing import IO, Any, Union

from botocore.eventstream import EventStream
from botocore.response import StreamingBody

from .literals import StreamErrorCodeType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "BlobTypeDef",
    "InternalStreamFailureTypeDef",
    "InvokeGlobalInferenceGatewayInputTypeDef",
    "InvokeGlobalInferenceGatewayOutputTypeDef",
    "InvokeGlobalInferenceGatewayWithResponseStreamInputTypeDef",
    "InvokeGlobalInferenceGatewayWithResponseStreamOutputTypeDef",
    "ModelStreamErrorTypeDef",
    "PayloadPartTypeDef",
    "ResponseMetadataTypeDef",
    "ResponseStreamTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class InternalStreamFailureTypeDef(TypedDict):
    Message: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ModelStreamErrorTypeDef(TypedDict):
    Message: str
    ErrorCode: NotRequired[StreamErrorCodeType]


class PayloadPartTypeDef(TypedDict):
    Bytes: NotRequired[bytes]


class InvokeGlobalInferenceGatewayInputTypeDef(TypedDict):
    GatewayId: str
    ContentType: str
    Body: BlobTypeDef
    Accept: NotRequired[str]
    CustomerIdentityToken: NotRequired[str]


class InvokeGlobalInferenceGatewayWithResponseStreamInputTypeDef(TypedDict):
    GatewayId: str
    ContentType: str
    Body: BlobTypeDef
    Accept: NotRequired[str]
    CustomerIdentityToken: NotRequired[str]


class InvokeGlobalInferenceGatewayOutputTypeDef(TypedDict):
    Body: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef


class ResponseStreamTypeDef(TypedDict):
    PayloadPart: NotRequired[PayloadPartTypeDef]
    ModelStreamError: NotRequired[ModelStreamErrorTypeDef]
    InternalStreamFailure: NotRequired[InternalStreamFailureTypeDef]


class InvokeGlobalInferenceGatewayWithResponseStreamOutputTypeDef(TypedDict):
    Body: EventStream[ResponseStreamTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
