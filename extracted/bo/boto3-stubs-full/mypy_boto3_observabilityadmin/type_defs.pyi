"""
Type annotations for observabilityadmin service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_observabilityadmin.type_defs import SourceLogsConfigurationTypeDef

    data: SourceLogsConfigurationTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from typing import Union

from .literals import (
    CentralizationFailureReasonType,
    EncryptedLogGroupStrategyType,
    EncryptionConflictResolutionStrategyType,
    EncryptionStrategyType,
    ResourceTypeType,
    RuleHealthType,
    StatusType,
    TelemetryStateType,
    TelemetryTypeType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "CentralizationRuleDestinationTypeDef",
    "CentralizationRuleOutputTypeDef",
    "CentralizationRuleSourceOutputTypeDef",
    "CentralizationRuleSourceTypeDef",
    "CentralizationRuleSummaryTypeDef",
    "CentralizationRuleTypeDef",
    "CentralizationRuleUnionTypeDef",
    "CreateCentralizationRuleForOrganizationInputTypeDef",
    "CreateCentralizationRuleForOrganizationOutputTypeDef",
    "CreateTelemetryRuleForOrganizationInputTypeDef",
    "CreateTelemetryRuleForOrganizationOutputTypeDef",
    "CreateTelemetryRuleInputTypeDef",
    "CreateTelemetryRuleOutputTypeDef",
    "DeleteCentralizationRuleForOrganizationInputTypeDef",
    "DeleteTelemetryRuleForOrganizationInputTypeDef",
    "DeleteTelemetryRuleInputTypeDef",
    "DestinationLogsConfigurationTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetCentralizationRuleForOrganizationInputTypeDef",
    "GetCentralizationRuleForOrganizationOutputTypeDef",
    "GetTelemetryEvaluationStatusForOrganizationOutputTypeDef",
    "GetTelemetryEvaluationStatusOutputTypeDef",
    "GetTelemetryRuleForOrganizationInputTypeDef",
    "GetTelemetryRuleForOrganizationOutputTypeDef",
    "GetTelemetryRuleInputTypeDef",
    "GetTelemetryRuleOutputTypeDef",
    "ListCentralizationRulesForOrganizationInputPaginateTypeDef",
    "ListCentralizationRulesForOrganizationInputTypeDef",
    "ListCentralizationRulesForOrganizationOutputTypeDef",
    "ListResourceTelemetryForOrganizationInputPaginateTypeDef",
    "ListResourceTelemetryForOrganizationInputTypeDef",
    "ListResourceTelemetryForOrganizationOutputTypeDef",
    "ListResourceTelemetryInputPaginateTypeDef",
    "ListResourceTelemetryInputTypeDef",
    "ListResourceTelemetryOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListTelemetryRulesForOrganizationInputPaginateTypeDef",
    "ListTelemetryRulesForOrganizationInputTypeDef",
    "ListTelemetryRulesForOrganizationOutputTypeDef",
    "ListTelemetryRulesInputPaginateTypeDef",
    "ListTelemetryRulesInputTypeDef",
    "ListTelemetryRulesOutputTypeDef",
    "LogsBackupConfigurationTypeDef",
    "LogsEncryptionConfigurationTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SourceLogsConfigurationTypeDef",
    "TagResourceInputTypeDef",
    "TelemetryConfigurationTypeDef",
    "TelemetryDestinationConfigurationTypeDef",
    "TelemetryRuleSummaryTypeDef",
    "TelemetryRuleTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateCentralizationRuleForOrganizationInputTypeDef",
    "UpdateCentralizationRuleForOrganizationOutputTypeDef",
    "UpdateTelemetryRuleForOrganizationInputTypeDef",
    "UpdateTelemetryRuleForOrganizationOutputTypeDef",
    "UpdateTelemetryRuleInputTypeDef",
    "UpdateTelemetryRuleOutputTypeDef",
    "VPCFlowLogParametersTypeDef",
)

class SourceLogsConfigurationTypeDef(TypedDict):
    LogGroupSelectionCriteria: str
    EncryptedLogGroupStrategy: EncryptedLogGroupStrategyType

class CentralizationRuleSummaryTypeDef(TypedDict):
    RuleName: NotRequired[str]
    RuleArn: NotRequired[str]
    CreatorAccountId: NotRequired[str]
    CreatedTimeStamp: NotRequired[int]
    CreatedRegion: NotRequired[str]
    LastUpdateTimeStamp: NotRequired[int]
    RuleHealth: NotRequired[RuleHealthType]
    FailureReason: NotRequired[CentralizationFailureReasonType]
    DestinationAccountId: NotRequired[str]
    DestinationRegion: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class DeleteCentralizationRuleForOrganizationInputTypeDef(TypedDict):
    RuleIdentifier: str

class DeleteTelemetryRuleForOrganizationInputTypeDef(TypedDict):
    RuleIdentifier: str

class DeleteTelemetryRuleInputTypeDef(TypedDict):
    RuleIdentifier: str

class LogsBackupConfigurationTypeDef(TypedDict):
    Region: str
    KmsKeyArn: NotRequired[str]

class LogsEncryptionConfigurationTypeDef(TypedDict):
    EncryptionStrategy: EncryptionStrategyType
    KmsKeyArn: NotRequired[str]
    EncryptionConflictResolutionStrategy: NotRequired[EncryptionConflictResolutionStrategyType]

class GetCentralizationRuleForOrganizationInputTypeDef(TypedDict):
    RuleIdentifier: str

class GetTelemetryRuleForOrganizationInputTypeDef(TypedDict):
    RuleIdentifier: str

class GetTelemetryRuleInputTypeDef(TypedDict):
    RuleIdentifier: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListCentralizationRulesForOrganizationInputTypeDef(TypedDict):
    RuleNamePrefix: NotRequired[str]
    AllRegions: NotRequired[bool]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListResourceTelemetryForOrganizationInputTypeDef(TypedDict):
    AccountIdentifiers: NotRequired[Sequence[str]]
    ResourceIdentifierPrefix: NotRequired[str]
    ResourceTypes: NotRequired[Sequence[ResourceTypeType]]
    TelemetryConfigurationState: NotRequired[Mapping[TelemetryTypeType, TelemetryStateType]]
    ResourceTags: NotRequired[Mapping[str, str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class TelemetryConfigurationTypeDef(TypedDict):
    AccountIdentifier: NotRequired[str]
    TelemetryConfigurationState: NotRequired[Dict[TelemetryTypeType, TelemetryStateType]]
    ResourceType: NotRequired[ResourceTypeType]
    ResourceIdentifier: NotRequired[str]
    ResourceTags: NotRequired[Dict[str, str]]
    LastUpdateTimeStamp: NotRequired[int]

class ListResourceTelemetryInputTypeDef(TypedDict):
    ResourceIdentifierPrefix: NotRequired[str]
    ResourceTypes: NotRequired[Sequence[ResourceTypeType]]
    TelemetryConfigurationState: NotRequired[Mapping[TelemetryTypeType, TelemetryStateType]]
    ResourceTags: NotRequired[Mapping[str, str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceInputTypeDef(TypedDict):
    ResourceARN: str

class ListTelemetryRulesForOrganizationInputTypeDef(TypedDict):
    RuleNamePrefix: NotRequired[str]
    SourceAccountIds: NotRequired[Sequence[str]]
    SourceOrganizationUnitIds: NotRequired[Sequence[str]]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class TelemetryRuleSummaryTypeDef(TypedDict):
    RuleName: NotRequired[str]
    RuleArn: NotRequired[str]
    CreatedTimeStamp: NotRequired[int]
    LastUpdateTimeStamp: NotRequired[int]
    ResourceType: NotRequired[ResourceTypeType]
    TelemetryType: NotRequired[TelemetryTypeType]

class ListTelemetryRulesInputTypeDef(TypedDict):
    RuleNamePrefix: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class TagResourceInputTypeDef(TypedDict):
    ResourceARN: str
    Tags: Mapping[str, str]

class VPCFlowLogParametersTypeDef(TypedDict):
    LogFormat: NotRequired[str]
    TrafficType: NotRequired[str]
    MaxAggregationInterval: NotRequired[int]

class UntagResourceInputTypeDef(TypedDict):
    ResourceARN: str
    TagKeys: Sequence[str]

class CentralizationRuleSourceOutputTypeDef(TypedDict):
    Regions: List[str]
    Scope: NotRequired[str]
    SourceLogsConfiguration: NotRequired[SourceLogsConfigurationTypeDef]

class CentralizationRuleSourceTypeDef(TypedDict):
    Regions: Sequence[str]
    Scope: NotRequired[str]
    SourceLogsConfiguration: NotRequired[SourceLogsConfigurationTypeDef]

class CreateCentralizationRuleForOrganizationOutputTypeDef(TypedDict):
    RuleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTelemetryRuleForOrganizationOutputTypeDef(TypedDict):
    RuleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateTelemetryRuleOutputTypeDef(TypedDict):
    RuleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetTelemetryEvaluationStatusForOrganizationOutputTypeDef(TypedDict):
    Status: StatusType
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetTelemetryEvaluationStatusOutputTypeDef(TypedDict):
    Status: StatusType
    FailureReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListCentralizationRulesForOrganizationOutputTypeDef(TypedDict):
    CentralizationRuleSummaries: List[CentralizationRuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCentralizationRuleForOrganizationOutputTypeDef(TypedDict):
    RuleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTelemetryRuleForOrganizationOutputTypeDef(TypedDict):
    RuleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTelemetryRuleOutputTypeDef(TypedDict):
    RuleArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DestinationLogsConfigurationTypeDef(TypedDict):
    LogsEncryptionConfiguration: NotRequired[LogsEncryptionConfigurationTypeDef]
    BackupConfiguration: NotRequired[LogsBackupConfigurationTypeDef]

class ListCentralizationRulesForOrganizationInputPaginateTypeDef(TypedDict):
    RuleNamePrefix: NotRequired[str]
    AllRegions: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceTelemetryForOrganizationInputPaginateTypeDef(TypedDict):
    AccountIdentifiers: NotRequired[Sequence[str]]
    ResourceIdentifierPrefix: NotRequired[str]
    ResourceTypes: NotRequired[Sequence[ResourceTypeType]]
    TelemetryConfigurationState: NotRequired[Mapping[TelemetryTypeType, TelemetryStateType]]
    ResourceTags: NotRequired[Mapping[str, str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceTelemetryInputPaginateTypeDef(TypedDict):
    ResourceIdentifierPrefix: NotRequired[str]
    ResourceTypes: NotRequired[Sequence[ResourceTypeType]]
    TelemetryConfigurationState: NotRequired[Mapping[TelemetryTypeType, TelemetryStateType]]
    ResourceTags: NotRequired[Mapping[str, str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTelemetryRulesForOrganizationInputPaginateTypeDef(TypedDict):
    RuleNamePrefix: NotRequired[str]
    SourceAccountIds: NotRequired[Sequence[str]]
    SourceOrganizationUnitIds: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTelemetryRulesInputPaginateTypeDef(TypedDict):
    RuleNamePrefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceTelemetryForOrganizationOutputTypeDef(TypedDict):
    TelemetryConfigurations: List[TelemetryConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListResourceTelemetryOutputTypeDef(TypedDict):
    TelemetryConfigurations: List[TelemetryConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTelemetryRulesForOrganizationOutputTypeDef(TypedDict):
    TelemetryRuleSummaries: List[TelemetryRuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTelemetryRulesOutputTypeDef(TypedDict):
    TelemetryRuleSummaries: List[TelemetryRuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TelemetryDestinationConfigurationTypeDef(TypedDict):
    DestinationType: NotRequired[Literal["cloud-watch-logs"]]
    DestinationPattern: NotRequired[str]
    RetentionInDays: NotRequired[int]
    VPCFlowLogParameters: NotRequired[VPCFlowLogParametersTypeDef]

class CentralizationRuleDestinationTypeDef(TypedDict):
    Region: str
    Account: NotRequired[str]
    DestinationLogsConfiguration: NotRequired[DestinationLogsConfigurationTypeDef]

class TelemetryRuleTypeDef(TypedDict):
    TelemetryType: TelemetryTypeType
    ResourceType: NotRequired[ResourceTypeType]
    DestinationConfiguration: NotRequired[TelemetryDestinationConfigurationTypeDef]
    Scope: NotRequired[str]
    SelectionCriteria: NotRequired[str]

class CentralizationRuleOutputTypeDef(TypedDict):
    Source: CentralizationRuleSourceOutputTypeDef
    Destination: CentralizationRuleDestinationTypeDef

class CentralizationRuleTypeDef(TypedDict):
    Source: CentralizationRuleSourceTypeDef
    Destination: CentralizationRuleDestinationTypeDef

class CreateTelemetryRuleForOrganizationInputTypeDef(TypedDict):
    RuleName: str
    Rule: TelemetryRuleTypeDef
    Tags: NotRequired[Mapping[str, str]]

class CreateTelemetryRuleInputTypeDef(TypedDict):
    RuleName: str
    Rule: TelemetryRuleTypeDef
    Tags: NotRequired[Mapping[str, str]]

class GetTelemetryRuleForOrganizationOutputTypeDef(TypedDict):
    RuleName: str
    RuleArn: str
    CreatedTimeStamp: int
    LastUpdateTimeStamp: int
    TelemetryRule: TelemetryRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetTelemetryRuleOutputTypeDef(TypedDict):
    RuleName: str
    RuleArn: str
    CreatedTimeStamp: int
    LastUpdateTimeStamp: int
    TelemetryRule: TelemetryRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateTelemetryRuleForOrganizationInputTypeDef(TypedDict):
    RuleIdentifier: str
    Rule: TelemetryRuleTypeDef

class UpdateTelemetryRuleInputTypeDef(TypedDict):
    RuleIdentifier: str
    Rule: TelemetryRuleTypeDef

class GetCentralizationRuleForOrganizationOutputTypeDef(TypedDict):
    RuleName: str
    RuleArn: str
    CreatorAccountId: str
    CreatedTimeStamp: int
    CreatedRegion: str
    LastUpdateTimeStamp: int
    RuleHealth: RuleHealthType
    FailureReason: CentralizationFailureReasonType
    CentralizationRule: CentralizationRuleOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

CentralizationRuleUnionTypeDef = Union[CentralizationRuleTypeDef, CentralizationRuleOutputTypeDef]

class CreateCentralizationRuleForOrganizationInputTypeDef(TypedDict):
    RuleName: str
    Rule: CentralizationRuleUnionTypeDef
    Tags: NotRequired[Mapping[str, str]]

class UpdateCentralizationRuleForOrganizationInputTypeDef(TypedDict):
    RuleIdentifier: str
    Rule: CentralizationRuleUnionTypeDef
