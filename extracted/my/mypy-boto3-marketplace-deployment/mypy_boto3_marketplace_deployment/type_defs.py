"""
Type annotations for marketplace-deployment service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_deployment/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_marketplace_deployment.type_defs import DeploymentParameterInputTypeDef

    data: DeploymentParameterInputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "DeploymentParameterInputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutDeploymentParameterRequestTypeDef",
    "PutDeploymentParameterResponseTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
)


class DeploymentParameterInputTypeDef(TypedDict):
    name: str
    secretString: str


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: NotRequired[Mapping[str, str]]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutDeploymentParameterResponseTypeDef(TypedDict):
    agreementId: str
    deploymentParameterId: str
    resourceArn: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutDeploymentParameterRequestTypeDef(TypedDict):
    agreementId: str
    catalog: str
    deploymentParameter: DeploymentParameterInputTypeDef
    productId: str
    clientToken: NotRequired[str]
    expirationDate: NotRequired[TimestampTypeDef]
    tags: NotRequired[Mapping[str, str]]
