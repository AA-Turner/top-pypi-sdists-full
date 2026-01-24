"""
Type annotations for route53-recovery-readiness service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_route53_recovery_readiness/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_route53_recovery_readiness.type_defs import CellOutputTypeDef

    data: CellOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import ReadinessType

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "CellOutputTypeDef",
    "CreateCellRequestTypeDef",
    "CreateCellResponseTypeDef",
    "CreateCrossAccountAuthorizationRequestTypeDef",
    "CreateCrossAccountAuthorizationResponseTypeDef",
    "CreateReadinessCheckRequestTypeDef",
    "CreateReadinessCheckResponseTypeDef",
    "CreateRecoveryGroupRequestTypeDef",
    "CreateRecoveryGroupResponseTypeDef",
    "CreateResourceSetRequestTypeDef",
    "CreateResourceSetResponseTypeDef",
    "DNSTargetResourceTypeDef",
    "DeleteCellRequestTypeDef",
    "DeleteCrossAccountAuthorizationRequestTypeDef",
    "DeleteReadinessCheckRequestTypeDef",
    "DeleteRecoveryGroupRequestTypeDef",
    "DeleteResourceSetRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetArchitectureRecommendationsRequestTypeDef",
    "GetArchitectureRecommendationsResponseTypeDef",
    "GetCellReadinessSummaryRequestPaginateTypeDef",
    "GetCellReadinessSummaryRequestTypeDef",
    "GetCellReadinessSummaryResponseTypeDef",
    "GetCellRequestTypeDef",
    "GetCellResponseTypeDef",
    "GetReadinessCheckRequestTypeDef",
    "GetReadinessCheckResourceStatusRequestPaginateTypeDef",
    "GetReadinessCheckResourceStatusRequestTypeDef",
    "GetReadinessCheckResourceStatusResponseTypeDef",
    "GetReadinessCheckResponseTypeDef",
    "GetReadinessCheckStatusRequestPaginateTypeDef",
    "GetReadinessCheckStatusRequestTypeDef",
    "GetReadinessCheckStatusResponseTypeDef",
    "GetRecoveryGroupReadinessSummaryRequestPaginateTypeDef",
    "GetRecoveryGroupReadinessSummaryRequestTypeDef",
    "GetRecoveryGroupReadinessSummaryResponseTypeDef",
    "GetRecoveryGroupRequestTypeDef",
    "GetRecoveryGroupResponseTypeDef",
    "GetResourceSetRequestTypeDef",
    "GetResourceSetResponseTypeDef",
    "ListCellsRequestPaginateTypeDef",
    "ListCellsRequestTypeDef",
    "ListCellsResponseTypeDef",
    "ListCrossAccountAuthorizationsRequestPaginateTypeDef",
    "ListCrossAccountAuthorizationsRequestTypeDef",
    "ListCrossAccountAuthorizationsResponseTypeDef",
    "ListReadinessChecksRequestPaginateTypeDef",
    "ListReadinessChecksRequestTypeDef",
    "ListReadinessChecksResponseTypeDef",
    "ListRecoveryGroupsRequestPaginateTypeDef",
    "ListRecoveryGroupsRequestTypeDef",
    "ListRecoveryGroupsResponseTypeDef",
    "ListResourceSetsRequestPaginateTypeDef",
    "ListResourceSetsRequestTypeDef",
    "ListResourceSetsResponseTypeDef",
    "ListRulesOutputTypeDef",
    "ListRulesRequestPaginateTypeDef",
    "ListRulesRequestTypeDef",
    "ListRulesResponseTypeDef",
    "ListTagsForResourcesRequestTypeDef",
    "ListTagsForResourcesResponseTypeDef",
    "MessageTypeDef",
    "NLBResourceTypeDef",
    "PaginatorConfigTypeDef",
    "R53ResourceRecordTypeDef",
    "ReadinessCheckOutputTypeDef",
    "ReadinessCheckSummaryTypeDef",
    "RecommendationTypeDef",
    "RecoveryGroupOutputTypeDef",
    "ResourceOutputTypeDef",
    "ResourceResultTypeDef",
    "ResourceSetOutputTypeDef",
    "ResourceTypeDef",
    "ResourceUnionTypeDef",
    "ResponseMetadataTypeDef",
    "RuleResultTypeDef",
    "TagResourceRequestTypeDef",
    "TargetResourceTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateCellRequestTypeDef",
    "UpdateCellResponseTypeDef",
    "UpdateReadinessCheckRequestTypeDef",
    "UpdateReadinessCheckResponseTypeDef",
    "UpdateRecoveryGroupRequestTypeDef",
    "UpdateRecoveryGroupResponseTypeDef",
    "UpdateResourceSetRequestTypeDef",
    "UpdateResourceSetResponseTypeDef",
)

class CellOutputTypeDef(TypedDict):
    CellArn: str
    CellName: str
    Cells: list[str]
    ParentReadinessScopes: list[str]
    Tags: NotRequired[dict[str, str]]

class CreateCellRequestTypeDef(TypedDict):
    CellName: str
    Cells: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CreateCrossAccountAuthorizationRequestTypeDef(TypedDict):
    CrossAccountAuthorization: str

class CreateReadinessCheckRequestTypeDef(TypedDict):
    ReadinessCheckName: str
    ResourceSetName: str
    Tags: NotRequired[Mapping[str, str]]

class CreateRecoveryGroupRequestTypeDef(TypedDict):
    RecoveryGroupName: str
    Cells: NotRequired[Sequence[str]]
    Tags: NotRequired[Mapping[str, str]]

class DeleteCellRequestTypeDef(TypedDict):
    CellName: str

class DeleteCrossAccountAuthorizationRequestTypeDef(TypedDict):
    CrossAccountAuthorization: str

class DeleteReadinessCheckRequestTypeDef(TypedDict):
    ReadinessCheckName: str

class DeleteRecoveryGroupRequestTypeDef(TypedDict):
    RecoveryGroupName: str

class DeleteResourceSetRequestTypeDef(TypedDict):
    ResourceSetName: str

class GetArchitectureRecommendationsRequestTypeDef(TypedDict):
    RecoveryGroupName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class RecommendationTypeDef(TypedDict):
    RecommendationText: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetCellReadinessSummaryRequestTypeDef(TypedDict):
    CellName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ReadinessCheckSummaryTypeDef(TypedDict):
    Readiness: NotRequired[ReadinessType]
    ReadinessCheckName: NotRequired[str]

class GetCellRequestTypeDef(TypedDict):
    CellName: str

class GetReadinessCheckRequestTypeDef(TypedDict):
    ReadinessCheckName: str

class GetReadinessCheckResourceStatusRequestTypeDef(TypedDict):
    ReadinessCheckName: str
    ResourceIdentifier: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class GetReadinessCheckStatusRequestTypeDef(TypedDict):
    ReadinessCheckName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class MessageTypeDef(TypedDict):
    MessageText: NotRequired[str]

class ResourceResultTypeDef(TypedDict):
    LastCheckedTimestamp: datetime
    Readiness: ReadinessType
    ComponentId: NotRequired[str]
    ResourceArn: NotRequired[str]

class GetRecoveryGroupReadinessSummaryRequestTypeDef(TypedDict):
    RecoveryGroupName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class GetRecoveryGroupRequestTypeDef(TypedDict):
    RecoveryGroupName: str

class GetResourceSetRequestTypeDef(TypedDict):
    ResourceSetName: str

class ListCellsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListCrossAccountAuthorizationsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListReadinessChecksRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ReadinessCheckOutputTypeDef(TypedDict):
    ReadinessCheckArn: str
    ResourceSet: str
    ReadinessCheckName: NotRequired[str]
    Tags: NotRequired[dict[str, str]]

class ListRecoveryGroupsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class RecoveryGroupOutputTypeDef(TypedDict):
    Cells: list[str]
    RecoveryGroupArn: str
    RecoveryGroupName: str
    Tags: NotRequired[dict[str, str]]

class ListResourceSetsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListRulesOutputTypeDef(TypedDict):
    ResourceType: str
    RuleDescription: str
    RuleId: str

class ListRulesRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ResourceType: NotRequired[str]

class ListTagsForResourcesRequestTypeDef(TypedDict):
    ResourceArn: str

class NLBResourceTypeDef(TypedDict):
    Arn: NotRequired[str]

class R53ResourceRecordTypeDef(TypedDict):
    DomainName: NotRequired[str]
    RecordSetId: NotRequired[str]

class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]

class UpdateCellRequestTypeDef(TypedDict):
    CellName: str
    Cells: Sequence[str]

class UpdateReadinessCheckRequestTypeDef(TypedDict):
    ReadinessCheckName: str
    ResourceSetName: str

class UpdateRecoveryGroupRequestTypeDef(TypedDict):
    Cells: Sequence[str]
    RecoveryGroupName: str

class CreateCellResponseTypeDef(TypedDict):
    CellArn: str
    CellName: str
    Cells: list[str]
    ParentReadinessScopes: list[str]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCrossAccountAuthorizationResponseTypeDef(TypedDict):
    CrossAccountAuthorization: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateReadinessCheckResponseTypeDef(TypedDict):
    ReadinessCheckArn: str
    ReadinessCheckName: str
    ResourceSet: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRecoveryGroupResponseTypeDef(TypedDict):
    Cells: list[str]
    RecoveryGroupArn: str
    RecoveryGroupName: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetCellResponseTypeDef(TypedDict):
    CellArn: str
    CellName: str
    Cells: list[str]
    ParentReadinessScopes: list[str]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetReadinessCheckResponseTypeDef(TypedDict):
    ReadinessCheckArn: str
    ReadinessCheckName: str
    ResourceSet: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetRecoveryGroupResponseTypeDef(TypedDict):
    Cells: list[str]
    RecoveryGroupArn: str
    RecoveryGroupName: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListCellsResponseTypeDef(TypedDict):
    Cells: list[CellOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListCrossAccountAuthorizationsResponseTypeDef(TypedDict):
    CrossAccountAuthorizations: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListTagsForResourcesResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateCellResponseTypeDef(TypedDict):
    CellArn: str
    CellName: str
    Cells: list[str]
    ParentReadinessScopes: list[str]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateReadinessCheckResponseTypeDef(TypedDict):
    ReadinessCheckArn: str
    ReadinessCheckName: str
    ResourceSet: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRecoveryGroupResponseTypeDef(TypedDict):
    Cells: list[str]
    RecoveryGroupArn: str
    RecoveryGroupName: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetArchitectureRecommendationsResponseTypeDef(TypedDict):
    LastAuditTimestamp: datetime
    Recommendations: list[RecommendationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetCellReadinessSummaryRequestPaginateTypeDef(TypedDict):
    CellName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetReadinessCheckResourceStatusRequestPaginateTypeDef(TypedDict):
    ReadinessCheckName: str
    ResourceIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetReadinessCheckStatusRequestPaginateTypeDef(TypedDict):
    ReadinessCheckName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetRecoveryGroupReadinessSummaryRequestPaginateTypeDef(TypedDict):
    RecoveryGroupName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCellsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCrossAccountAuthorizationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListReadinessChecksRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRecoveryGroupsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListResourceSetsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRulesRequestPaginateTypeDef(TypedDict):
    ResourceType: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetCellReadinessSummaryResponseTypeDef(TypedDict):
    Readiness: ReadinessType
    ReadinessChecks: list[ReadinessCheckSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class GetRecoveryGroupReadinessSummaryResponseTypeDef(TypedDict):
    Readiness: ReadinessType
    ReadinessChecks: list[ReadinessCheckSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class RuleResultTypeDef(TypedDict):
    LastCheckedTimestamp: datetime
    Messages: list[MessageTypeDef]
    Readiness: ReadinessType
    RuleId: str

class GetReadinessCheckStatusResponseTypeDef(TypedDict):
    Messages: list[MessageTypeDef]
    Readiness: ReadinessType
    Resources: list[ResourceResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListReadinessChecksResponseTypeDef(TypedDict):
    ReadinessChecks: list[ReadinessCheckOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRecoveryGroupsResponseTypeDef(TypedDict):
    RecoveryGroups: list[RecoveryGroupOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ListRulesResponseTypeDef(TypedDict):
    Rules: list[ListRulesOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class TargetResourceTypeDef(TypedDict):
    NLBResource: NotRequired[NLBResourceTypeDef]
    R53Resource: NotRequired[R53ResourceRecordTypeDef]

class GetReadinessCheckResourceStatusResponseTypeDef(TypedDict):
    Readiness: ReadinessType
    Rules: list[RuleResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class DNSTargetResourceTypeDef(TypedDict):
    DomainName: NotRequired[str]
    HostedZoneArn: NotRequired[str]
    RecordSetId: NotRequired[str]
    RecordType: NotRequired[str]
    TargetResource: NotRequired[TargetResourceTypeDef]

class ResourceOutputTypeDef(TypedDict):
    ComponentId: NotRequired[str]
    DnsTargetResource: NotRequired[DNSTargetResourceTypeDef]
    ReadinessScopes: NotRequired[list[str]]
    ResourceArn: NotRequired[str]

class ResourceTypeDef(TypedDict):
    ComponentId: NotRequired[str]
    DnsTargetResource: NotRequired[DNSTargetResourceTypeDef]
    ReadinessScopes: NotRequired[Sequence[str]]
    ResourceArn: NotRequired[str]

class CreateResourceSetResponseTypeDef(TypedDict):
    ResourceSetArn: str
    ResourceSetName: str
    ResourceSetType: str
    Resources: list[ResourceOutputTypeDef]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourceSetResponseTypeDef(TypedDict):
    ResourceSetArn: str
    ResourceSetName: str
    ResourceSetType: str
    Resources: list[ResourceOutputTypeDef]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class ResourceSetOutputTypeDef(TypedDict):
    ResourceSetArn: str
    ResourceSetName: str
    ResourceSetType: str
    Resources: list[ResourceOutputTypeDef]
    Tags: NotRequired[dict[str, str]]

class UpdateResourceSetResponseTypeDef(TypedDict):
    ResourceSetArn: str
    ResourceSetName: str
    ResourceSetType: str
    Resources: list[ResourceOutputTypeDef]
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

ResourceUnionTypeDef = Union[ResourceTypeDef, ResourceOutputTypeDef]

class ListResourceSetsResponseTypeDef(TypedDict):
    ResourceSets: list[ResourceSetOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class CreateResourceSetRequestTypeDef(TypedDict):
    ResourceSetName: str
    ResourceSetType: str
    Resources: Sequence[ResourceUnionTypeDef]
    Tags: NotRequired[Mapping[str, str]]

class UpdateResourceSetRequestTypeDef(TypedDict):
    ResourceSetName: str
    ResourceSetType: str
    Resources: Sequence[ResourceUnionTypeDef]
