"""
Type annotations for iotdeviceadvisor service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iotdeviceadvisor/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_iotdeviceadvisor.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AuthenticationMethodType,
    ProtocolType,
    StatusType,
    SuiteRunStatusType,
    TestCaseScenarioStatusType,
    TestCaseScenarioTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CreateSuiteDefinitionRequestTypeDef",
    "CreateSuiteDefinitionResponseTypeDef",
    "DeleteSuiteDefinitionRequestTypeDef",
    "DeviceUnderTestTypeDef",
    "GetEndpointRequestTypeDef",
    "GetEndpointResponseTypeDef",
    "GetSuiteDefinitionRequestTypeDef",
    "GetSuiteDefinitionResponseTypeDef",
    "GetSuiteRunReportRequestTypeDef",
    "GetSuiteRunReportResponseTypeDef",
    "GetSuiteRunRequestTypeDef",
    "GetSuiteRunResponseTypeDef",
    "GroupResultTypeDef",
    "ListSuiteDefinitionsRequestTypeDef",
    "ListSuiteDefinitionsResponseTypeDef",
    "ListSuiteRunsRequestTypeDef",
    "ListSuiteRunsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ResponseMetadataTypeDef",
    "StartSuiteRunRequestTypeDef",
    "StartSuiteRunResponseTypeDef",
    "StopSuiteRunRequestTypeDef",
    "SuiteDefinitionConfigurationOutputTypeDef",
    "SuiteDefinitionConfigurationTypeDef",
    "SuiteDefinitionConfigurationUnionTypeDef",
    "SuiteDefinitionInformationTypeDef",
    "SuiteRunConfigurationOutputTypeDef",
    "SuiteRunConfigurationTypeDef",
    "SuiteRunConfigurationUnionTypeDef",
    "SuiteRunInformationTypeDef",
    "TagResourceRequestTypeDef",
    "TestCaseRunTypeDef",
    "TestCaseScenarioTypeDef",
    "TestResultTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateSuiteDefinitionRequestTypeDef",
    "UpdateSuiteDefinitionResponseTypeDef",
)

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteSuiteDefinitionRequestTypeDef(TypedDict):
    suiteDefinitionId: str

class DeviceUnderTestTypeDef(TypedDict):
    thingArn: NotRequired[str]
    certificateArn: NotRequired[str]
    deviceRoleArn: NotRequired[str]

class GetEndpointRequestTypeDef(TypedDict):
    thingArn: NotRequired[str]
    certificateArn: NotRequired[str]
    deviceRoleArn: NotRequired[str]
    authenticationMethod: NotRequired[AuthenticationMethodType]

class GetSuiteDefinitionRequestTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteDefinitionVersion: NotRequired[str]

class GetSuiteRunReportRequestTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteRunId: str

class GetSuiteRunRequestTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteRunId: str

class ListSuiteDefinitionsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListSuiteRunsRequestTypeDef(TypedDict):
    suiteDefinitionId: NotRequired[str]
    suiteDefinitionVersion: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class SuiteRunInformationTypeDef(TypedDict):
    suiteDefinitionId: NotRequired[str]
    suiteDefinitionVersion: NotRequired[str]
    suiteDefinitionName: NotRequired[str]
    suiteRunId: NotRequired[str]
    createdAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    endAt: NotRequired[datetime]
    status: NotRequired[SuiteRunStatusType]
    passed: NotRequired[int]
    failed: NotRequired[int]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class StopSuiteRunRequestTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteRunId: str

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TestCaseScenarioTypeDef(TypedDict):
    testCaseScenarioId: NotRequired[str]
    testCaseScenarioType: NotRequired[TestCaseScenarioTypeType]
    status: NotRequired[TestCaseScenarioStatusType]
    failure: NotRequired[str]
    systemMessage: NotRequired[str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class CreateSuiteDefinitionResponseTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteDefinitionArn: str
    suiteDefinitionName: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetEndpointResponseTypeDef(TypedDict):
    endpoint: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSuiteRunReportResponseTypeDef(TypedDict):
    qualificationReportDownloadUrl: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartSuiteRunResponseTypeDef(TypedDict):
    suiteRunId: str
    suiteRunArn: str
    createdAt: datetime
    endpoint: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateSuiteDefinitionResponseTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteDefinitionArn: str
    suiteDefinitionName: str
    suiteDefinitionVersion: str
    createdAt: datetime
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class SuiteDefinitionConfigurationOutputTypeDef(TypedDict):
    suiteDefinitionName: str
    rootGroup: str
    devicePermissionRoleArn: str
    devices: NotRequired[list[DeviceUnderTestTypeDef]]
    intendedForQualification: NotRequired[bool]
    isLongDurationTest: NotRequired[bool]
    protocol: NotRequired[ProtocolType]

class SuiteDefinitionConfigurationTypeDef(TypedDict):
    suiteDefinitionName: str
    rootGroup: str
    devicePermissionRoleArn: str
    devices: NotRequired[Sequence[DeviceUnderTestTypeDef]]
    intendedForQualification: NotRequired[bool]
    isLongDurationTest: NotRequired[bool]
    protocol: NotRequired[ProtocolType]

class SuiteDefinitionInformationTypeDef(TypedDict):
    suiteDefinitionId: NotRequired[str]
    suiteDefinitionName: NotRequired[str]
    defaultDevices: NotRequired[list[DeviceUnderTestTypeDef]]
    intendedForQualification: NotRequired[bool]
    isLongDurationTest: NotRequired[bool]
    protocol: NotRequired[ProtocolType]
    createdAt: NotRequired[datetime]

class SuiteRunConfigurationOutputTypeDef(TypedDict):
    primaryDevice: DeviceUnderTestTypeDef
    selectedTestList: NotRequired[list[str]]
    parallelRun: NotRequired[bool]

class SuiteRunConfigurationTypeDef(TypedDict):
    primaryDevice: DeviceUnderTestTypeDef
    selectedTestList: NotRequired[Sequence[str]]
    parallelRun: NotRequired[bool]

class ListSuiteRunsResponseTypeDef(TypedDict):
    suiteRunsList: list[SuiteRunInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class TestCaseRunTypeDef(TypedDict):
    testCaseRunId: NotRequired[str]
    testCaseDefinitionId: NotRequired[str]
    testCaseDefinitionName: NotRequired[str]
    status: NotRequired[StatusType]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    logUrl: NotRequired[str]
    warnings: NotRequired[str]
    failure: NotRequired[str]
    testScenarios: NotRequired[list[TestCaseScenarioTypeDef]]

class GetSuiteDefinitionResponseTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteDefinitionArn: str
    suiteDefinitionVersion: str
    latestVersion: str
    suiteDefinitionConfiguration: SuiteDefinitionConfigurationOutputTypeDef
    createdAt: datetime
    lastModifiedAt: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

SuiteDefinitionConfigurationUnionTypeDef = Union[
    SuiteDefinitionConfigurationTypeDef, SuiteDefinitionConfigurationOutputTypeDef
]

class ListSuiteDefinitionsResponseTypeDef(TypedDict):
    suiteDefinitionInformationList: list[SuiteDefinitionInformationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

SuiteRunConfigurationUnionTypeDef = Union[
    SuiteRunConfigurationTypeDef, SuiteRunConfigurationOutputTypeDef
]

class GroupResultTypeDef(TypedDict):
    groupId: NotRequired[str]
    groupName: NotRequired[str]
    tests: NotRequired[list[TestCaseRunTypeDef]]

class CreateSuiteDefinitionRequestTypeDef(TypedDict):
    suiteDefinitionConfiguration: SuiteDefinitionConfigurationUnionTypeDef
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]

class UpdateSuiteDefinitionRequestTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteDefinitionConfiguration: SuiteDefinitionConfigurationUnionTypeDef

class StartSuiteRunRequestTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteRunConfiguration: SuiteRunConfigurationUnionTypeDef
    suiteDefinitionVersion: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class TestResultTypeDef(TypedDict):
    groups: NotRequired[list[GroupResultTypeDef]]

class GetSuiteRunResponseTypeDef(TypedDict):
    suiteDefinitionId: str
    suiteDefinitionVersion: str
    suiteRunId: str
    suiteRunArn: str
    suiteRunConfiguration: SuiteRunConfigurationOutputTypeDef
    testResult: TestResultTypeDef
    startTime: datetime
    endTime: datetime
    status: SuiteRunStatusType
    errorReason: str
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef
