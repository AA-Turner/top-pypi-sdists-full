"""
Type annotations for marketplace-deployment service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_deployment/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_marketplace_deployment.type_defs import DataAsAServiceConfigurationDetailTypeDef

    data: DataAsAServiceConfigurationDetailTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import DeploymentConfigurationJobErrorCodeType, DeploymentConfigurationJobStatusType

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "DataAsAServiceConfigurationDetailTypeDef",
    "DeploymentConfigurationDetailTypeDef",
    "DeploymentConfigurationJobSummaryTypeDef",
    "DeploymentParameterInputTypeDef",
    "GetDeploymentConfigurationJobRequestTypeDef",
    "GetDeploymentConfigurationJobResponseTypeDef",
    "GetDeploymentConfigurationRequestTypeDef",
    "GetDeploymentConfigurationResponseTypeDef",
    "ListDeploymentConfigurationJobsRequestPaginateTypeDef",
    "ListDeploymentConfigurationJobsRequestTypeDef",
    "ListDeploymentConfigurationJobsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutDeploymentParameterRequestTypeDef",
    "PutDeploymentParameterResponseTypeDef",
    "ResponseMetadataTypeDef",
    "StartDeploymentConfigurationJobRequestTypeDef",
    "StartDeploymentConfigurationJobResponseTypeDef",
    "TagResourceRequestTypeDef",
    "TimestampTypeDef",
    "UntagResourceRequestTypeDef",
)

class DataAsAServiceConfigurationDetailTypeDef(TypedDict):
    fulfillmentUrl: str

class DeploymentParameterInputTypeDef(TypedDict):
    name: str
    secretString: str

class GetDeploymentConfigurationJobRequestTypeDef(TypedDict):
    catalog: str
    productId: str
    deliveryOptionType: Literal["data-as-a-service"]
    jobId: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class GetDeploymentConfigurationRequestTypeDef(TypedDict):
    catalog: str
    productId: str
    deliveryOptionType: Literal["data-as-a-service"]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListDeploymentConfigurationJobsRequestTypeDef(TypedDict):
    catalog: str
    productId: str
    deliveryOptionType: Literal["data-as-a-service"]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

TimestampTypeDef = Union[datetime, str]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: NotRequired[Mapping[str, str]]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class DeploymentConfigurationDetailTypeDef(TypedDict):
    dataAsAService: NotRequired[DataAsAServiceConfigurationDetailTypeDef]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutDeploymentParameterResponseTypeDef(TypedDict):
    resourceArn: str
    agreementId: str
    deploymentParameterId: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListDeploymentConfigurationJobsRequestPaginateTypeDef(TypedDict):
    catalog: str
    productId: str
    deliveryOptionType: Literal["data-as-a-service"]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class PutDeploymentParameterRequestTypeDef(TypedDict):
    catalog: str
    productId: str
    agreementId: str
    deploymentParameter: DeploymentParameterInputTypeDef
    tags: NotRequired[Mapping[str, str]]
    expirationDate: NotRequired[TimestampTypeDef]
    clientToken: NotRequired[str]

class DeploymentConfigurationJobSummaryTypeDef(TypedDict):
    jobId: str
    status: DeploymentConfigurationJobStatusType
    configuration: DeploymentConfigurationDetailTypeDef
    createdAt: datetime

class GetDeploymentConfigurationJobResponseTypeDef(TypedDict):
    jobId: str
    configuration: DeploymentConfigurationDetailTypeDef
    status: DeploymentConfigurationJobStatusType
    createdAt: datetime
    configurationArn: str
    endedAt: datetime
    errorCode: DeploymentConfigurationJobErrorCodeType
    message: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetDeploymentConfigurationResponseTypeDef(TypedDict):
    configuration: DeploymentConfigurationDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class StartDeploymentConfigurationJobRequestTypeDef(TypedDict):
    catalog: str
    productId: str
    deliveryOptionType: Literal["data-as-a-service"]
    configuration: DeploymentConfigurationDetailTypeDef
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class StartDeploymentConfigurationJobResponseTypeDef(TypedDict):
    jobId: str
    configuration: DeploymentConfigurationDetailTypeDef
    status: DeploymentConfigurationJobStatusType
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListDeploymentConfigurationJobsResponseTypeDef(TypedDict):
    jobs: list[DeploymentConfigurationJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
