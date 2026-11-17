"""
Type annotations for sagemaker-inference-router-runtime service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemaker_inference_router_runtime/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_sagemaker_inference_router_runtime.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from typing import IO, Any, Union

from botocore.response import StreamingBody

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "BlobTypeDef",
    "InvokeInferenceRouterAsyncInputTypeDef",
    "InvokeInferenceRouterAsyncOutputTypeDef",
    "InvokeInferenceRouterInputTypeDef",
    "InvokeInferenceRouterOutputTypeDef",
    "ResponseMetadataTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class InvokeInferenceRouterAsyncInputTypeDef(TypedDict):
    InferenceRouterName: str
    RoutingTargetName: str
    InputLocation: str
    ContentType: NotRequired[str]
    Accept: NotRequired[str]
    CustomAttributes: NotRequired[str]
    InferenceId: NotRequired[str]
    S3OutputPathExtension: NotRequired[str]
    Filename: NotRequired[str]
    RequestTTLSeconds: NotRequired[int]
    InvocationTimeoutSeconds: NotRequired[int]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class InvokeInferenceRouterInputTypeDef(TypedDict):
    InferenceRouterName: str
    RoutingTargetName: str
    Body: BlobTypeDef
    ContentType: NotRequired[str]
    Accept: NotRequired[str]
    InferenceId: NotRequired[str]
    PrefixAwareId: NotRequired[str]
    CustomAttributes: NotRequired[str]


class InvokeInferenceRouterAsyncOutputTypeDef(TypedDict):
    InferenceId: str
    OutputLocation: str
    FailureLocation: str
    ResponseMetadata: ResponseMetadataTypeDef


class InvokeInferenceRouterOutputTypeDef(TypedDict):
    Body: StreamingBody
    ContentType: str
    InvokedRoutedResourceArn: str
    RoutingReason: str
    InvokedProductionVariant: str
    CustomAttributes: str
    ResponseMetadata: ResponseMetadataTypeDef
