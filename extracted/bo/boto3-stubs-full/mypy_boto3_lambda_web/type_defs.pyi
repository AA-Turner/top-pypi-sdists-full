"""
Type annotations for lambda-web service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_lambda_web.type_defs import AccountQuotasTypeDef

    data: AccountQuotasTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ApplicationLogLevelType,
    AuthTypeType,
    AutoDeploymentModeType,
    EndpointStateType,
    EndpointTypeType,
    EndpointUpdateStatusType,
    FunctionStateType,
    RevisionStateType,
    SystemLogLevelType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "AccountQuotasTypeDef",
    "AccountUsageTypeDef",
    "BuildConfigTypeDef",
    "CodeConfigTypeDef",
    "CreateWebFunctionEndpointRequestTypeDef",
    "CreateWebFunctionEndpointResponseTypeDef",
    "CreateWebFunctionRequestTypeDef",
    "CreateWebFunctionResponseTypeDef",
    "CreateWebFunctionRevisionRequestTypeDef",
    "CreateWebFunctionRevisionResponseTypeDef",
    "DeleteResourcePolicyRequestTypeDef",
    "DeleteWebFunctionEndpointRequestTypeDef",
    "DeleteWebFunctionRequestTypeDef",
    "DeleteWebFunctionRevisionRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointConfigTypeDef",
    "FilterTypeDef",
    "FunctionEndpointSummaryTypeDef",
    "FunctionRevisionSummaryTypeDef",
    "FunctionSummaryTypeDef",
    "GetResourcePolicyRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetWebAccountSettingsResponseTypeDef",
    "GetWebFunctionEndpointRequestTypeDef",
    "GetWebFunctionEndpointRequestWaitExtraExtraTypeDef",
    "GetWebFunctionEndpointRequestWaitExtraTypeDef",
    "GetWebFunctionEndpointRequestWaitTypeDef",
    "GetWebFunctionEndpointResponseTypeDef",
    "GetWebFunctionRequestTypeDef",
    "GetWebFunctionRequestWaitExtraTypeDef",
    "GetWebFunctionRequestWaitTypeDef",
    "GetWebFunctionResponseTypeDef",
    "GetWebFunctionRevisionRequestTypeDef",
    "GetWebFunctionRevisionRequestWaitTypeDef",
    "GetWebFunctionRevisionResponseTypeDef",
    "ListTagsRequestTypeDef",
    "ListTagsResponseTypeDef",
    "ListWebFunctionEndpointsRequestPaginateTypeDef",
    "ListWebFunctionEndpointsRequestTypeDef",
    "ListWebFunctionEndpointsResponseTypeDef",
    "ListWebFunctionRevisionsRequestPaginateTypeDef",
    "ListWebFunctionRevisionsRequestTypeDef",
    "ListWebFunctionRevisionsResponseTypeDef",
    "ListWebFunctionsRequestPaginateTypeDef",
    "ListWebFunctionsRequestTypeDef",
    "ListWebFunctionsResponseTypeDef",
    "LoggingConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PutResourcePolicyRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "RegionalEndpointTypeDef",
    "ResponseMetadataTypeDef",
    "RevisionConfigTypeDef",
    "RevisionErrorTypeDef",
    "RevisionWeightTypeDef",
    "RuntimeConfigTypeDef",
    "S3ObjectTypeDef",
    "ScalingConfigTypeDef",
    "ServiceConfigOutputTypeDef",
    "ServiceConfigTypeDef",
    "ServiceConfigUnionTypeDef",
    "TagResourceRequestTypeDef",
    "TelemetryConfigTypeDef",
    "ThrottleConfigTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateWebFunctionEndpointRequestTypeDef",
    "UpdateWebFunctionEndpointResponseTypeDef",
    "WaiterConfigTypeDef",
)

class AccountQuotasTypeDef(TypedDict):
    maxTotalArmVCpus: int
    maxTotalRateLimit: int
    maxRevisionsPerFunction: int
    maxEndpointsPerFunction: int

class AccountUsageTypeDef(TypedDict):
    functionCount: int

class RuntimeConfigTypeDef(TypedDict):
    runtime: str

class S3ObjectTypeDef(TypedDict):
    bucket: str
    key: str
    versionId: NotRequired[str]

class RevisionWeightTypeDef(TypedDict):
    revisionId: str
    weight: int

class ScalingConfigTypeDef(TypedDict):
    maxEnvironments: NotRequired[int]

class ThrottleConfigTypeDef(TypedDict):
    rateLimit: NotRequired[int]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class FunctionRevisionSummaryTypeDef(TypedDict):
    revisionArn: str
    revisionId: str
    state: RevisionStateType
    stateReason: str
    createdAt: datetime
    description: NotRequired[str]

class RevisionErrorTypeDef(TypedDict):
    attribute: str
    errorCode: str
    errorMessage: str

class DeleteResourcePolicyRequestTypeDef(TypedDict):
    resourceArn: str
    revisionId: NotRequired[str]

class DeleteWebFunctionEndpointRequestTypeDef(TypedDict):
    functionName: str
    endpointName: str

class DeleteWebFunctionRequestTypeDef(TypedDict):
    functionName: str

class DeleteWebFunctionRevisionRequestTypeDef(TypedDict):
    functionName: str
    revisionId: str

class FilterTypeDef(TypedDict):
    name: str
    values: Sequence[str]

class FunctionSummaryTypeDef(TypedDict):
    functionName: str
    functionArn: str
    state: FunctionStateType
    stateReason: str
    createdAt: datetime
    updatedAt: datetime

class GetResourcePolicyRequestTypeDef(TypedDict):
    resourceArn: str

class GetWebFunctionEndpointRequestTypeDef(TypedDict):
    functionName: str
    endpointName: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetWebFunctionRequestTypeDef(TypedDict):
    functionName: str

class GetWebFunctionRevisionRequestTypeDef(TypedDict):
    functionName: str
    revisionId: str

class ListTagsRequestTypeDef(TypedDict):
    resource: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class LoggingConfigTypeDef(TypedDict):
    logGroup: NotRequired[str]
    applicationLogLevel: NotRequired[ApplicationLogLevelType]
    systemLogLevel: NotRequired[SystemLogLevelType]

class PutResourcePolicyRequestTypeDef(TypedDict):
    resourceArn: str
    policy: str
    revisionId: NotRequired[str]

class TagResourceRequestTypeDef(TypedDict):
    resource: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resource: str
    tagKeys: Sequence[str]

class CodeConfigTypeDef(TypedDict):
    s3Object: S3ObjectTypeDef

class CreateWebFunctionEndpointRequestTypeDef(TypedDict):
    functionName: str
    endpointName: str
    endpointType: EndpointTypeType
    authType: AuthTypeType
    description: NotRequired[str]
    autoDeploymentMode: NotRequired[AutoDeploymentModeType]
    revisionWeights: NotRequired[Sequence[RevisionWeightTypeDef]]
    regions: NotRequired[Sequence[str]]
    scalingConfig: NotRequired[ScalingConfigTypeDef]
    throttleConfig: NotRequired[ThrottleConfigTypeDef]

class EndpointConfigTypeDef(TypedDict):
    endpointName: str
    endpointType: EndpointTypeType
    authType: AuthTypeType
    description: NotRequired[str]
    autoDeploymentMode: NotRequired[AutoDeploymentModeType]
    regions: NotRequired[Sequence[str]]
    scalingConfig: NotRequired[ScalingConfigTypeDef]
    throttleConfig: NotRequired[ThrottleConfigTypeDef]

class FunctionEndpointSummaryTypeDef(TypedDict):
    endpointArn: str
    endpointName: str
    endpointType: EndpointTypeType
    domainName: str
    authType: AuthTypeType
    autoDeploymentMode: AutoDeploymentModeType
    revisionWeights: list[RevisionWeightTypeDef]
    regions: list[str]
    state: EndpointStateType
    stateReason: str
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    scalingConfig: NotRequired[ScalingConfigTypeDef]
    throttleConfig: NotRequired[ThrottleConfigTypeDef]
    updateStatus: NotRequired[EndpointUpdateStatusType]
    updateStatusReason: NotRequired[str]

class RegionalEndpointTypeDef(TypedDict):
    authType: AuthTypeType
    revisionWeights: list[RevisionWeightTypeDef]
    state: EndpointStateType
    stateReason: str
    domainName: NotRequired[str]
    scalingConfig: NotRequired[ScalingConfigTypeDef]
    throttleConfig: NotRequired[ThrottleConfigTypeDef]
    updateStatus: NotRequired[EndpointUpdateStatusType]
    updateStatusReason: NotRequired[str]

class UpdateWebFunctionEndpointRequestTypeDef(TypedDict):
    functionName: str
    endpointName: str
    description: NotRequired[str]
    authType: NotRequired[AuthTypeType]
    autoDeploymentMode: NotRequired[AutoDeploymentModeType]
    revisionWeights: NotRequired[Sequence[RevisionWeightTypeDef]]
    scalingConfig: NotRequired[ScalingConfigTypeDef]
    throttleConfig: NotRequired[ThrottleConfigTypeDef]

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyResponseTypeDef(TypedDict):
    policy: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetWebAccountSettingsResponseTypeDef(TypedDict):
    accountQuotas: AccountQuotasTypeDef
    accountUsage: AccountUsageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetWebFunctionResponseTypeDef(TypedDict):
    functionName: str
    functionArn: str
    state: FunctionStateType
    stateReason: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutResourcePolicyResponseTypeDef(TypedDict):
    policy: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListWebFunctionRevisionsResponseTypeDef(TypedDict):
    revisions: list[FunctionRevisionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWebFunctionEndpointsRequestTypeDef(TypedDict):
    functionName: str
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListWebFunctionRevisionsRequestTypeDef(TypedDict):
    functionName: str
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListWebFunctionsRequestTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListWebFunctionsResponseTypeDef(TypedDict):
    functions: list[FunctionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetWebFunctionEndpointRequestWaitExtraExtraTypeDef(TypedDict):
    functionName: str
    endpointName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetWebFunctionEndpointRequestWaitExtraTypeDef(TypedDict):
    functionName: str
    endpointName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetWebFunctionEndpointRequestWaitTypeDef(TypedDict):
    functionName: str
    endpointName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetWebFunctionRequestWaitExtraTypeDef(TypedDict):
    functionName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetWebFunctionRequestWaitTypeDef(TypedDict):
    functionName: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetWebFunctionRevisionRequestWaitTypeDef(TypedDict):
    functionName: str
    revisionId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class ListWebFunctionEndpointsRequestPaginateTypeDef(TypedDict):
    functionName: str
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWebFunctionRevisionsRequestPaginateTypeDef(TypedDict):
    functionName: str
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWebFunctionsRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class TelemetryConfigTypeDef(TypedDict):
    loggingConfig: NotRequired[LoggingConfigTypeDef]

class BuildConfigTypeDef(TypedDict):
    codeConfig: CodeConfigTypeDef
    runtimeConfig: RuntimeConfigTypeDef

class CreateWebFunctionResponseTypeDef(TypedDict):
    functionName: str
    functionArn: str
    state: FunctionStateType
    stateReason: str
    createdAt: datetime
    updatedAt: datetime
    revision: FunctionRevisionSummaryTypeDef
    endpoint: FunctionEndpointSummaryTypeDef
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListWebFunctionEndpointsResponseTypeDef(TypedDict):
    endpoints: list[FunctionEndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateWebFunctionEndpointResponseTypeDef(TypedDict):
    functionArn: str
    endpointArn: str
    endpointName: str
    description: str
    endpointType: EndpointTypeType
    domainName: str
    authType: AuthTypeType
    autoDeploymentMode: AutoDeploymentModeType
    revisionWeights: list[RevisionWeightTypeDef]
    regions: list[str]
    scalingConfig: ScalingConfigTypeDef
    throttleConfig: ThrottleConfigTypeDef
    state: EndpointStateType
    stateReason: str
    updateStatus: EndpointUpdateStatusType
    updateStatusReason: str
    regionalEndpoints: dict[str, RegionalEndpointTypeDef]
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetWebFunctionEndpointResponseTypeDef(TypedDict):
    functionArn: str
    endpointArn: str
    endpointName: str
    description: str
    endpointType: EndpointTypeType
    domainName: str
    authType: AuthTypeType
    autoDeploymentMode: AutoDeploymentModeType
    revisionWeights: list[RevisionWeightTypeDef]
    regions: list[str]
    scalingConfig: ScalingConfigTypeDef
    throttleConfig: ThrottleConfigTypeDef
    state: EndpointStateType
    stateReason: str
    updateStatus: EndpointUpdateStatusType
    updateStatusReason: str
    regionalEndpoints: dict[str, RegionalEndpointTypeDef]
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateWebFunctionEndpointResponseTypeDef(TypedDict):
    functionArn: str
    endpointArn: str
    endpointName: str
    description: str
    endpointType: EndpointTypeType
    domainName: str
    authType: AuthTypeType
    autoDeploymentMode: AutoDeploymentModeType
    revisionWeights: list[RevisionWeightTypeDef]
    regions: list[str]
    scalingConfig: ScalingConfigTypeDef
    throttleConfig: ThrottleConfigTypeDef
    state: EndpointStateType
    stateReason: str
    updateStatus: EndpointUpdateStatusType
    updateStatusReason: str
    regionalEndpoints: dict[str, RegionalEndpointTypeDef]
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ServiceConfigOutputTypeDef(TypedDict):
    executionRoleArn: str
    timeoutSeconds: NotRequired[int]
    maxConcurrencyPerEnvironment: NotRequired[int]
    environmentVariables: NotRequired[dict[str, str]]
    telemetryConfig: NotRequired[TelemetryConfigTypeDef]

class ServiceConfigTypeDef(TypedDict):
    executionRoleArn: str
    timeoutSeconds: NotRequired[int]
    maxConcurrencyPerEnvironment: NotRequired[int]
    environmentVariables: NotRequired[Mapping[str, str]]
    telemetryConfig: NotRequired[TelemetryConfigTypeDef]

class CreateWebFunctionRevisionResponseTypeDef(TypedDict):
    functionArn: str
    revisionArn: str
    revisionId: str
    description: str
    kmsKeyArn: str
    buildConfig: BuildConfigTypeDef
    serviceConfig: ServiceConfigOutputTypeDef
    state: RevisionStateType
    stateReason: str
    errors: list[RevisionErrorTypeDef]
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetWebFunctionRevisionResponseTypeDef(TypedDict):
    functionArn: str
    revisionArn: str
    revisionId: str
    description: str
    kmsKeyArn: str
    buildConfig: BuildConfigTypeDef
    serviceConfig: ServiceConfigOutputTypeDef
    state: RevisionStateType
    stateReason: str
    errors: list[RevisionErrorTypeDef]
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

ServiceConfigUnionTypeDef = Union[ServiceConfigTypeDef, ServiceConfigOutputTypeDef]

class CreateWebFunctionRevisionRequestTypeDef(TypedDict):
    functionName: str
    buildConfig: BuildConfigTypeDef
    serviceConfig: ServiceConfigUnionTypeDef
    description: NotRequired[str]
    kmsKeyArn: NotRequired[str]

class RevisionConfigTypeDef(TypedDict):
    buildConfig: BuildConfigTypeDef
    serviceConfig: ServiceConfigUnionTypeDef
    description: NotRequired[str]
    kmsKeyArn: NotRequired[str]

class CreateWebFunctionRequestTypeDef(TypedDict):
    functionName: str
    revisionConfig: NotRequired[RevisionConfigTypeDef]
    endpointConfig: NotRequired[EndpointConfigTypeDef]
    tags: NotRequired[Mapping[str, str]]
