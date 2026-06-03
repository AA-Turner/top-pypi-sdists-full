"""
Type annotations for sagemakerjobruntime service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_sagemakerjobruntime.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import CompletionStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BlobTypeDef",
    "CompleteRolloutRequestTypeDef",
    "ResponseMetadataTypeDef",
    "SampleRequestTypeDef",
    "SampleResponseTypeDef",
    "SampleWithResponseStreamRequestTypeDef",
    "SampleWithResponseStreamResponseTypeDef",
    "UpdateRewardRequestTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class CompleteRolloutRequestTypeDef(TypedDict):
    JobArn: str
    TrajectoryId: str
    Status: NotRequired[CompletionStatusType]
    ClientToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class UpdateRewardRequestTypeDef(TypedDict):
    JobArn: str
    TrajectoryId: str
    Rewards: Sequence[float]
    ClientToken: NotRequired[str]

class SampleRequestTypeDef(TypedDict):
    JobArn: str
    TrajectoryId: str
    Body: BlobTypeDef

class SampleWithResponseStreamRequestTypeDef(TypedDict):
    JobArn: str
    TrajectoryId: str
    Body: BlobTypeDef

class SampleResponseTypeDef(TypedDict):
    ContentType: str
    Body: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef

class SampleWithResponseStreamResponseTypeDef(TypedDict):
    ContentType: str
    Body: StreamingBody
    ResponseMetadata: ResponseMetadataTypeDef
