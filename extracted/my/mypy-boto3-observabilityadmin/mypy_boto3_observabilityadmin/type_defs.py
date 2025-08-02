"""
Type annotations for observabilityadmin service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_observabilityadmin.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

from __future__ import annotations

import sys

from .literals import ResourceTypeType, StatusType, TelemetryStateType, TelemetryTypeType

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
    "CreateTelemetryRuleForOrganizationInputTypeDef",
    "CreateTelemetryRuleForOrganizationOutputTypeDef",
    "CreateTelemetryRuleInputTypeDef",
    "CreateTelemetryRuleOutputTypeDef",
    "DeleteTelemetryRuleForOrganizationInputTypeDef",
    "DeleteTelemetryRuleInputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetTelemetryEvaluationStatusForOrganizationOutputTypeDef",
    "GetTelemetryEvaluationStatusOutputTypeDef",
    "GetTelemetryRuleForOrganizationInputTypeDef",
    "GetTelemetryRuleForOrganizationOutputTypeDef",
    "GetTelemetryRuleInputTypeDef",
    "GetTelemetryRuleOutputTypeDef",
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
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceInputTypeDef",
    "TelemetryConfigurationTypeDef",
    "TelemetryDestinationConfigurationTypeDef",
    "TelemetryRuleSummaryTypeDef",
    "TelemetryRuleTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateTelemetryRuleForOrganizationInputTypeDef",
    "UpdateTelemetryRuleForOrganizationOutputTypeDef",
    "UpdateTelemetryRuleInputTypeDef",
    "UpdateTelemetryRuleOutputTypeDef",
    "VPCFlowLogParametersTypeDef",
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteTelemetryRuleForOrganizationInputTypeDef(TypedDict):
    RuleIdentifier: str


class DeleteTelemetryRuleInputTypeDef(TypedDict):
    RuleIdentifier: str


class GetTelemetryRuleForOrganizationInputTypeDef(TypedDict):
    RuleIdentifier: str


class GetTelemetryRuleInputTypeDef(TypedDict):
    RuleIdentifier: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


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


class ListTagsForResourceOutputTypeDef(TypedDict):
    Tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTelemetryRuleForOrganizationOutputTypeDef(TypedDict):
    RuleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTelemetryRuleOutputTypeDef(TypedDict):
    RuleArn: str
    ResponseMetadata: ResponseMetadataTypeDef


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


class TelemetryRuleTypeDef(TypedDict):
    TelemetryType: TelemetryTypeType
    ResourceType: NotRequired[ResourceTypeType]
    DestinationConfiguration: NotRequired[TelemetryDestinationConfigurationTypeDef]
    Scope: NotRequired[str]
    SelectionCriteria: NotRequired[str]


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
