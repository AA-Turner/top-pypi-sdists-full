"""
Type annotations for signer-data service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signer_data/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_signer_data.type_defs import TimestampTypeDef

    data: TimestampTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "GetRevocationStatusRequestTypeDef",
    "GetRevocationStatusResponseTypeDef",
    "ResponseMetadataTypeDef",
    "TimestampTypeDef",
)

TimestampTypeDef = Union[datetime, str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class GetRevocationStatusRequestTypeDef(TypedDict):
    signatureTimestamp: TimestampTypeDef
    platformId: str
    profileVersionArn: str
    jobArn: str
    certificateHashes: Sequence[str]


class GetRevocationStatusResponseTypeDef(TypedDict):
    revokedEntities: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
