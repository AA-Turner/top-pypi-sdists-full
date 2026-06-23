"""
Type annotations for lambda-microvms service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_lambda_microvms.type_defs import CloudWatchLoggingTypeDef

    data: CloudWatchLoggingTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    BuildStateType,
    HookStateType,
    MicrovmImageStateType,
    MicrovmImageVersionStateType,
    MicrovmImageVersionStatusType,
    MicrovmStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "CloudWatchLoggingTypeDef",
    "CodeArtifactTypeDef",
    "CpuConfigurationTypeDef",
    "CreateMicrovmAuthTokenRequestTypeDef",
    "CreateMicrovmAuthTokenResponseTypeDef",
    "CreateMicrovmImageRequestTypeDef",
    "CreateMicrovmImageResponseTypeDef",
    "CreateMicrovmShellAuthTokenRequestTypeDef",
    "CreateMicrovmShellAuthTokenResponseTypeDef",
    "DeleteMicrovmImageInputTypeDef",
    "DeleteMicrovmImageOutputTypeDef",
    "DeleteMicrovmImageVersionInputTypeDef",
    "DeleteMicrovmImageVersionOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetMicrovmImageBuildInputTypeDef",
    "GetMicrovmImageBuildOutputTypeDef",
    "GetMicrovmImageInputTypeDef",
    "GetMicrovmImageOutputTypeDef",
    "GetMicrovmImageVersionInputTypeDef",
    "GetMicrovmImageVersionOutputTypeDef",
    "GetMicrovmRequestTypeDef",
    "GetMicrovmResponseTypeDef",
    "HooksTypeDef",
    "IdlePolicyTypeDef",
    "ListManagedMicrovmImageVersionsInputPaginateTypeDef",
    "ListManagedMicrovmImageVersionsInputTypeDef",
    "ListManagedMicrovmImageVersionsOutputTypeDef",
    "ListManagedMicrovmImagesInputPaginateTypeDef",
    "ListManagedMicrovmImagesInputTypeDef",
    "ListManagedMicrovmImagesOutputTypeDef",
    "ListMicrovmImageBuildsInputPaginateTypeDef",
    "ListMicrovmImageBuildsInputTypeDef",
    "ListMicrovmImageBuildsOutputTypeDef",
    "ListMicrovmImageVersionsInputPaginateTypeDef",
    "ListMicrovmImageVersionsInputTypeDef",
    "ListMicrovmImageVersionsOutputTypeDef",
    "ListMicrovmImagesRequestPaginateTypeDef",
    "ListMicrovmImagesRequestTypeDef",
    "ListMicrovmImagesResponseTypeDef",
    "ListMicrovmsRequestPaginateTypeDef",
    "ListMicrovmsRequestTypeDef",
    "ListMicrovmsResponseTypeDef",
    "ListTagsRequestTypeDef",
    "ListTagsResponseTypeDef",
    "LoggingOutputTypeDef",
    "LoggingTypeDef",
    "LoggingUnionTypeDef",
    "ManagedMicrovmImageSummaryTypeDef",
    "ManagedMicrovmImageVersionTypeDef",
    "MicrovmHooksTypeDef",
    "MicrovmImageBuildSummaryTypeDef",
    "MicrovmImageHooksTypeDef",
    "MicrovmImageSummaryTypeDef",
    "MicrovmImageVersionSummaryTypeDef",
    "MicrovmItemTypeDef",
    "PaginatorConfigTypeDef",
    "PortRangeTypeDef",
    "PortSpecificationTypeDef",
    "ResourcesTypeDef",
    "ResponseMetadataTypeDef",
    "ResumeMicrovmRequestTypeDef",
    "RunMicrovmRequestTypeDef",
    "RunMicrovmResponseTypeDef",
    "SnapshotBuildTypeDef",
    "SuspendMicrovmRequestTypeDef",
    "TagResourceRequestTypeDef",
    "TerminateMicrovmRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateMicrovmImageRequestTypeDef",
    "UpdateMicrovmImageResponseTypeDef",
    "UpdateMicrovmImageVersionRequestTypeDef",
    "UpdateMicrovmImageVersionResponseTypeDef",
)


class CloudWatchLoggingTypeDef(TypedDict):
    logGroup: NotRequired[str]
    logStream: NotRequired[str]


class CodeArtifactTypeDef(TypedDict):
    uri: NotRequired[str]


class CpuConfigurationTypeDef(TypedDict):
    architecture: Literal["ARM_64"]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class ResourcesTypeDef(TypedDict):
    minimumMemoryInMiB: int


class CreateMicrovmShellAuthTokenRequestTypeDef(TypedDict):
    microvmIdentifier: str
    expirationInMinutes: int


class DeleteMicrovmImageInputTypeDef(TypedDict):
    imageIdentifier: str


class DeleteMicrovmImageVersionInputTypeDef(TypedDict):
    imageIdentifier: str
    imageVersion: str


class GetMicrovmImageBuildInputTypeDef(TypedDict):
    imageIdentifier: str
    imageVersion: str
    buildId: str


class SnapshotBuildTypeDef(TypedDict):
    memorySnapshotSizeInBytes: NotRequired[int]
    codeInstallSizeInBytes: NotRequired[int]
    diskSnapshotSizeInBytes: NotRequired[int]


class GetMicrovmImageInputTypeDef(TypedDict):
    imageIdentifier: str


class GetMicrovmImageVersionInputTypeDef(TypedDict):
    imageIdentifier: str
    imageVersion: str


class GetMicrovmRequestTypeDef(TypedDict):
    microvmIdentifier: str


class IdlePolicyTypeDef(TypedDict):
    maxIdleDurationSeconds: int
    suspendedDurationSeconds: int
    autoResumeEnabled: bool


class MicrovmHooksTypeDef(TypedDict):
    run: NotRequired[HookStateType]
    runTimeoutInSeconds: NotRequired[int]
    resume: NotRequired[HookStateType]
    resumeTimeoutInSeconds: NotRequired[int]
    suspend: NotRequired[HookStateType]
    suspendTimeoutInSeconds: NotRequired[int]
    terminate: NotRequired[HookStateType]
    terminateTimeoutInSeconds: NotRequired[int]


class MicrovmImageHooksTypeDef(TypedDict):
    ready: NotRequired[HookStateType]
    readyTimeoutInSeconds: NotRequired[int]
    validate: NotRequired[HookStateType]
    validateTimeoutInSeconds: NotRequired[int]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListManagedMicrovmImageVersionsInputTypeDef(TypedDict):
    imageIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ManagedMicrovmImageVersionTypeDef(TypedDict):
    imageArn: str
    imageVersion: str
    createdAt: datetime
    updatedAt: NotRequired[datetime]


class ListManagedMicrovmImagesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ManagedMicrovmImageSummaryTypeDef(TypedDict):
    imageArn: str
    createdAt: datetime
    updatedAt: NotRequired[datetime]


class ListMicrovmImageBuildsInputTypeDef(TypedDict):
    imageIdentifier: str
    imageVersion: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    architecture: NotRequired[Literal["ARM_64"]]
    chipset: NotRequired[Literal["GRAVITON"]]
    chipsetGeneration: NotRequired[str]


class MicrovmImageBuildSummaryTypeDef(TypedDict):
    imageArn: str
    imageVersion: str
    buildId: str
    buildState: BuildStateType
    architecture: Literal["ARM_64"]
    chipset: Literal["GRAVITON"]
    chipsetGeneration: str
    createdAt: datetime
    stateReason: NotRequired[str]


class ListMicrovmImageVersionsInputTypeDef(TypedDict):
    imageIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListMicrovmImagesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    nameFilter: NotRequired[str]


class MicrovmImageSummaryTypeDef(TypedDict):
    imageArn: str
    name: str
    state: MicrovmImageStateType
    createdAt: datetime
    latestActiveImageVersion: NotRequired[str]
    latestFailedImageVersion: NotRequired[str]


class ListMicrovmsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    imageIdentifier: NotRequired[str]
    imageVersion: NotRequired[str]


class MicrovmItemTypeDef(TypedDict):
    microvmId: str
    state: MicrovmStateType
    imageArn: str
    imageVersion: str
    startedAt: datetime


class ListTagsRequestTypeDef(TypedDict):
    Resource: str


class PortRangeTypeDef(TypedDict):
    startPort: int
    endPort: int


class ResumeMicrovmRequestTypeDef(TypedDict):
    microvmIdentifier: str


class SuspendMicrovmRequestTypeDef(TypedDict):
    microvmIdentifier: str


class TagResourceRequestTypeDef(TypedDict):
    Resource: str
    Tags: Mapping[str, str]


class TerminateMicrovmRequestTypeDef(TypedDict):
    microvmIdentifier: str


class UntagResourceRequestTypeDef(TypedDict):
    Resource: str
    TagKeys: Sequence[str]


class UpdateMicrovmImageVersionRequestTypeDef(TypedDict):
    imageIdentifier: str
    imageVersion: str
    status: MicrovmImageVersionStatusType


class LoggingOutputTypeDef(TypedDict):
    disabled: NotRequired[dict[str, Any]]
    cloudWatch: NotRequired[CloudWatchLoggingTypeDef]


class LoggingTypeDef(TypedDict):
    disabled: NotRequired[Mapping[str, Any]]
    cloudWatch: NotRequired[CloudWatchLoggingTypeDef]


class CreateMicrovmAuthTokenResponseTypeDef(TypedDict):
    authToken: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMicrovmShellAuthTokenResponseTypeDef(TypedDict):
    authToken: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMicrovmImageOutputTypeDef(TypedDict):
    imageIdentifier: str
    state: MicrovmImageStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMicrovmImageVersionOutputTypeDef(TypedDict):
    imageIdentifier: str
    imageVersion: str
    state: MicrovmImageVersionStateType
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetMicrovmImageOutputTypeDef(TypedDict):
    imageArn: str
    name: str
    state: MicrovmImageStateType
    latestActiveImageVersion: str
    latestFailedImageVersion: str
    createdAt: datetime
    tags: dict[str, str]
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetMicrovmImageBuildOutputTypeDef(TypedDict):
    imageArn: str
    imageVersion: str
    buildId: str
    buildState: BuildStateType
    architecture: Literal["ARM_64"]
    chipset: Literal["GRAVITON"]
    chipsetGeneration: str
    stateReason: str
    createdAt: datetime
    snapshotBuild: SnapshotBuildTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetMicrovmResponseTypeDef(TypedDict):
    microvmId: str
    state: MicrovmStateType
    endpoint: str
    imageArn: str
    imageVersion: str
    executionRoleArn: str
    idlePolicy: IdlePolicyTypeDef
    maximumDurationInSeconds: int
    startedAt: datetime
    terminatedAt: datetime
    stateReason: str
    ingressNetworkConnectors: list[str]
    egressNetworkConnectors: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class RunMicrovmResponseTypeDef(TypedDict):
    microvmId: str
    state: MicrovmStateType
    endpoint: str
    imageArn: str
    imageVersion: str
    executionRoleArn: str
    idlePolicy: IdlePolicyTypeDef
    maximumDurationInSeconds: int
    startedAt: datetime
    terminatedAt: datetime
    stateReason: str
    ingressNetworkConnectors: list[str]
    egressNetworkConnectors: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class HooksTypeDef(TypedDict):
    port: NotRequired[int]
    microvmHooks: NotRequired[MicrovmHooksTypeDef]
    microvmImageHooks: NotRequired[MicrovmImageHooksTypeDef]


class ListManagedMicrovmImageVersionsInputPaginateTypeDef(TypedDict):
    imageIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedMicrovmImagesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMicrovmImageBuildsInputPaginateTypeDef(TypedDict):
    imageIdentifier: str
    imageVersion: str
    architecture: NotRequired[Literal["ARM_64"]]
    chipset: NotRequired[Literal["GRAVITON"]]
    chipsetGeneration: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMicrovmImageVersionsInputPaginateTypeDef(TypedDict):
    imageIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMicrovmImagesRequestPaginateTypeDef(TypedDict):
    nameFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMicrovmsRequestPaginateTypeDef(TypedDict):
    imageIdentifier: NotRequired[str]
    imageVersion: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedMicrovmImageVersionsOutputTypeDef(TypedDict):
    items: list[ManagedMicrovmImageVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListManagedMicrovmImagesOutputTypeDef(TypedDict):
    items: list[ManagedMicrovmImageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMicrovmImageBuildsOutputTypeDef(TypedDict):
    items: list[MicrovmImageBuildSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMicrovmImagesResponseTypeDef(TypedDict):
    items: list[MicrovmImageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMicrovmsResponseTypeDef(TypedDict):
    items: list[MicrovmItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


PortSpecificationTypeDef = TypedDict(
    "PortSpecificationTypeDef",
    {
        "port": NotRequired[int],
        "range": NotRequired[PortRangeTypeDef],
        "allPorts": NotRequired[Mapping[str, Any]],
    },
)
LoggingUnionTypeDef = Union[LoggingTypeDef, LoggingOutputTypeDef]


class CreateMicrovmImageResponseTypeDef(TypedDict):
    imageArn: str
    name: str
    state: MicrovmImageStateType
    latestActiveImageVersion: str
    latestFailedImageVersion: str
    createdAt: datetime
    baseImageArn: str
    baseImageVersion: str
    buildRoleArn: str
    description: str
    codeArtifact: CodeArtifactTypeDef
    logging: LoggingOutputTypeDef
    egressNetworkConnectors: list[str]
    cpuConfigurations: list[CpuConfigurationTypeDef]
    resources: list[ResourcesTypeDef]
    additionalOsCapabilities: list[Literal["ALL"]]
    hooks: HooksTypeDef
    environmentVariables: dict[str, str]
    tags: dict[str, str]
    updatedAt: datetime
    imageVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetMicrovmImageVersionOutputTypeDef(TypedDict):
    baseImageArn: str
    baseImageVersion: str
    buildRoleArn: str
    description: str
    codeArtifact: CodeArtifactTypeDef
    logging: LoggingOutputTypeDef
    egressNetworkConnectors: list[str]
    cpuConfigurations: list[CpuConfigurationTypeDef]
    resources: list[ResourcesTypeDef]
    additionalOsCapabilities: list[Literal["ALL"]]
    hooks: HooksTypeDef
    environmentVariables: dict[str, str]
    imageArn: str
    imageVersion: str
    state: MicrovmImageVersionStateType
    status: MicrovmImageVersionStatusType
    createdAt: datetime
    updatedAt: datetime
    stateReason: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class MicrovmImageVersionSummaryTypeDef(TypedDict):
    baseImageArn: str
    buildRoleArn: str
    codeArtifact: CodeArtifactTypeDef
    imageArn: str
    imageVersion: str
    state: MicrovmImageVersionStateType
    status: MicrovmImageVersionStatusType
    createdAt: datetime
    baseImageVersion: NotRequired[str]
    description: NotRequired[str]
    logging: NotRequired[LoggingOutputTypeDef]
    egressNetworkConnectors: NotRequired[list[str]]
    cpuConfigurations: NotRequired[list[CpuConfigurationTypeDef]]
    resources: NotRequired[list[ResourcesTypeDef]]
    additionalOsCapabilities: NotRequired[list[Literal["ALL"]]]
    hooks: NotRequired[HooksTypeDef]
    environmentVariables: NotRequired[dict[str, str]]
    updatedAt: NotRequired[datetime]
    stateReason: NotRequired[str]
    tags: NotRequired[dict[str, str]]


class UpdateMicrovmImageResponseTypeDef(TypedDict):
    imageArn: str
    name: str
    state: MicrovmImageStateType
    latestActiveImageVersion: str
    latestFailedImageVersion: str
    createdAt: datetime
    baseImageArn: str
    baseImageVersion: str
    buildRoleArn: str
    description: str
    codeArtifact: CodeArtifactTypeDef
    logging: LoggingOutputTypeDef
    egressNetworkConnectors: list[str]
    cpuConfigurations: list[CpuConfigurationTypeDef]
    resources: list[ResourcesTypeDef]
    additionalOsCapabilities: list[Literal["ALL"]]
    hooks: HooksTypeDef
    environmentVariables: dict[str, str]
    updatedAt: datetime
    imageVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMicrovmImageVersionResponseTypeDef(TypedDict):
    baseImageArn: str
    baseImageVersion: str
    buildRoleArn: str
    description: str
    codeArtifact: CodeArtifactTypeDef
    logging: LoggingOutputTypeDef
    egressNetworkConnectors: list[str]
    cpuConfigurations: list[CpuConfigurationTypeDef]
    resources: list[ResourcesTypeDef]
    additionalOsCapabilities: list[Literal["ALL"]]
    hooks: HooksTypeDef
    environmentVariables: dict[str, str]
    imageArn: str
    imageVersion: str
    state: MicrovmImageVersionStateType
    status: MicrovmImageVersionStatusType
    createdAt: datetime
    updatedAt: datetime
    stateReason: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMicrovmAuthTokenRequestTypeDef(TypedDict):
    microvmIdentifier: str
    expirationInMinutes: int
    allowedPorts: Sequence[PortSpecificationTypeDef]


class CreateMicrovmImageRequestTypeDef(TypedDict):
    baseImageArn: str
    buildRoleArn: str
    codeArtifact: CodeArtifactTypeDef
    name: str
    baseImageVersion: NotRequired[str]
    description: NotRequired[str]
    logging: NotRequired[LoggingUnionTypeDef]
    egressNetworkConnectors: NotRequired[Sequence[str]]
    cpuConfigurations: NotRequired[Sequence[CpuConfigurationTypeDef]]
    resources: NotRequired[Sequence[ResourcesTypeDef]]
    additionalOsCapabilities: NotRequired[Sequence[Literal["ALL"]]]
    hooks: NotRequired[HooksTypeDef]
    environmentVariables: NotRequired[Mapping[str, str]]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class RunMicrovmRequestTypeDef(TypedDict):
    imageIdentifier: str
    ingressNetworkConnectors: NotRequired[Sequence[str]]
    egressNetworkConnectors: NotRequired[Sequence[str]]
    imageVersion: NotRequired[str]
    executionRoleArn: NotRequired[str]
    idlePolicy: NotRequired[IdlePolicyTypeDef]
    logging: NotRequired[LoggingUnionTypeDef]
    runHookPayload: NotRequired[str]
    maximumDurationInSeconds: NotRequired[int]
    clientToken: NotRequired[str]


class UpdateMicrovmImageRequestTypeDef(TypedDict):
    baseImageArn: str
    buildRoleArn: str
    codeArtifact: CodeArtifactTypeDef
    imageIdentifier: str
    baseImageVersion: NotRequired[str]
    description: NotRequired[str]
    logging: NotRequired[LoggingUnionTypeDef]
    egressNetworkConnectors: NotRequired[Sequence[str]]
    cpuConfigurations: NotRequired[Sequence[CpuConfigurationTypeDef]]
    resources: NotRequired[Sequence[ResourcesTypeDef]]
    additionalOsCapabilities: NotRequired[Sequence[Literal["ALL"]]]
    hooks: NotRequired[HooksTypeDef]
    environmentVariables: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class ListMicrovmImageVersionsOutputTypeDef(TypedDict):
    items: list[MicrovmImageVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]
