"""
Type annotations for continuum service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_continuum/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_continuum.type_defs import AffectedPackageTypeDef

    data: AffectedPackageTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    ArtifactHttpMethodType,
    CollectorStatusType,
    DeliveryReasonType,
    DeliveryStatusType,
    ExploitabilityVerdictType,
    ExploitEffectType,
    FindingBlockingReasonType,
    FindingDiscardReasonType,
    FindingOcsfClassType,
    FindingSeverityAdjustmentType,
    FindingSeverityIdType,
    FindingStatusType,
    FindingTypeType,
    FindingVerdictType,
    FlowVerdictValueType,
    GitLabTargetTypeType,
    GitLabTokenRotationType,
    IntegrationTypeType,
    IssueArtifactTypeType,
    IssueEvidenceAvailabilityType,
    IssuePatchDeliveryStatusType,
    IssuePhaseType,
    IssueSeverityType,
    IssueStatusReasonType,
    IssueStatusType,
    PatchCreationPolicyType,
    PatchFormatType,
    ScanFailureStageType,
    ScanOriginType,
    ScanStatusType,
    SignalAccessLevelType,
    SignalAttackerGainsType,
    SignalBandType,
    SignalBasisType,
    SignalBlastRadiusType,
    SignalDimensionType,
    SignalStrengthType,
    SignalTargetValueType,
    ValidationConfidenceTierType,
    ValidationTerminalStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AffectedPackageTypeDef",
    "AssociateCollectorInputTypeDef",
    "AssociateCollectorOutputTypeDef",
    "AssociatedCollectorTypeDef",
    "AssociatedEnvironmentTypeDef",
    "CodeConfigurationDetailsTypeDef",
    "CodeScanDataTypeDef",
    "CodeScanSummaryTypeDef",
    "CollectorDetailsTypeDef",
    "CollectorSummaryTypeDef",
    "CreateCodeConfigurationTypeDef",
    "CreateCodeFindingInputTypeDef",
    "CreateCodeFindingOutputTypeDef",
    "CreateCodeScanInputTypeDef",
    "CreateCodeScanOutputTypeDef",
    "CreateCollectorInputTypeDef",
    "CreateCollectorOutputTypeDef",
    "CreateEnvironmentConfigurationTypeDef",
    "CreateEnvironmentInputTypeDef",
    "CreateEnvironmentOutputTypeDef",
    "CreateIntegrationInputTypeDef",
    "CreateIntegrationOutputTypeDef",
    "DeleteCollectorInputTypeDef",
    "DeleteEnvironmentInputTypeDef",
    "DeleteIntegrationInputTypeDef",
    "DestinationTargetTypeDef",
    "DisassociateCollectorInputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnvironmentConfigurationDetailsTypeDef",
    "EnvironmentConfigurationOutputTypeDef",
    "EnvironmentConfigurationTypeDef",
    "EnvironmentConfigurationUnionTypeDef",
    "EnvironmentListEntryTypeDef",
    "EnvironmentNetworkConfigurationOutputTypeDef",
    "EnvironmentNetworkConfigurationTypeDef",
    "EnvironmentNetworkConfigurationUnionTypeDef",
    "EnvironmentRepositorySourceTypeDef",
    "EnvironmentS3IntegrationSourceTypeDef",
    "EnvironmentSourceConfigurationOutputTypeDef",
    "EnvironmentSourceConfigurationTypeDef",
    "EnvironmentSourceConfigurationUnionTypeDef",
    "FindingComplianceCheckTypeDef",
    "FindingEvidenceTypeDef",
    "FindingLocationTypeDef",
    "FindingPostureTypeDef",
    "FindingResourceTypeDef",
    "FindingSummaryTypeDef",
    "FindingValidationTypeDef",
    "FindingVulnerabilityTypeDef",
    "FlowVerdictTypeDef",
    "GetCodeFindingInputTypeDef",
    "GetCodeFindingOutputTypeDef",
    "GetCodeIssueArtifactInputTypeDef",
    "GetCodeIssueArtifactOutputTypeDef",
    "GetCodeIssueInputTypeDef",
    "GetCodeIssueOutputTypeDef",
    "GetCodeScanInputTypeDef",
    "GetCodeScanInputWaitTypeDef",
    "GetCodeScanOutputTypeDef",
    "GetCollectorDataAccessAuthorizationInputTypeDef",
    "GetCollectorInputTypeDef",
    "GetCollectorOutputTypeDef",
    "GetEnvironmentInputTypeDef",
    "GetEnvironmentOutputTypeDef",
    "GetIntegrationInputTypeDef",
    "GetIntegrationOutputTypeDef",
    "GetResourcePolicyInputTypeDef",
    "GetResourcePolicyOutputTypeDef",
    "GitHubAuthorizationConfigurationTypeDef",
    "GitHubConfigurationTypeDef",
    "GitHubDetailsTypeDef",
    "GitHubTargetTypeDef",
    "GitLabConfigurationTypeDef",
    "GitLabDetailsTypeDef",
    "IntegrationSummaryTypeDef",
    "IssueArtifactBodyTypeDef",
    "IssueArtifactItemTypeDef",
    "IssueArtifactProducerSummaryTypeDef",
    "IssuePatchDeliveryTypeDef",
    "IssueSummaryTypeDef",
    "KubernetesClusterRoleConfigurationTypeDef",
    "KubernetesClusterRoleUpdateTypeDef",
    "ListAssociatedCollectorsInputPaginateTypeDef",
    "ListAssociatedCollectorsInputTypeDef",
    "ListAssociatedCollectorsOutputTypeDef",
    "ListAssociatedEnvironmentsInputPaginateTypeDef",
    "ListAssociatedEnvironmentsInputTypeDef",
    "ListAssociatedEnvironmentsOutputTypeDef",
    "ListCodeFindingsInputPaginateTypeDef",
    "ListCodeFindingsInputTypeDef",
    "ListCodeFindingsOutputTypeDef",
    "ListCodeIssueArtifactsInputPaginateTypeDef",
    "ListCodeIssueArtifactsInputTypeDef",
    "ListCodeIssueArtifactsOutputTypeDef",
    "ListCodeIssuesInputPaginateTypeDef",
    "ListCodeIssuesInputTypeDef",
    "ListCodeIssuesOutputTypeDef",
    "ListCodeScansInputPaginateTypeDef",
    "ListCodeScansInputTypeDef",
    "ListCodeScansOutputTypeDef",
    "ListCollectorsOutputTypeDef",
    "ListEnvironmentsInputPaginateTypeDef",
    "ListEnvironmentsInputTypeDef",
    "ListEnvironmentsOutputTypeDef",
    "ListIntegrationsInputPaginateTypeDef",
    "ListIntegrationsInputTypeDef",
    "ListIntegrationsOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PatchBodyTypeDef",
    "PatchDeliveryTypeDef",
    "PerFindingResultTypeDef",
    "PrevalidationSignalTypeDef",
    "PrevalidationSignalsBodyTypeDef",
    "ProviderConfigurationTypeDef",
    "ProviderDetailsTypeDef",
    "PutResourcePolicyInputTypeDef",
    "PutResourcePolicyOutputTypeDef",
    "ReasoningStepTypeDef",
    "RemediationProposalBodyTypeDef",
    "ResponseMetadataTypeDef",
    "S3ConfigurationTypeDef",
    "S3DetailsTypeDef",
    "S3TargetTypeDef",
    "SignalAccessPreconditionTypeDef",
    "SignalAttackerGainsDimensionTypeDef",
    "SignalBlastRadiusDimensionTypeDef",
    "SignalComputationTypeDef",
    "SignalConfidenceReasoningTypeDef",
    "SignalExploitabilityTypeDef",
    "SignalImpactDimensionsTypeDef",
    "SignalPreconditionTypeDef",
    "SignalPreconditionsTypeDef",
    "SignalTargetValueDimensionTypeDef",
    "StartIntegrationAuthorizationInputTypeDef",
    "StartIntegrationAuthorizationOutputTypeDef",
    "UpdateCodeConfigurationTypeDef",
    "UpdateCollectorInputTypeDef",
    "UpdateCollectorOutputTypeDef",
    "UpdateEnvironmentConfigurationTypeDef",
    "UpdateEnvironmentInputTypeDef",
    "UpdateEnvironmentOutputTypeDef",
    "UpdateIntegrationInputTypeDef",
    "UpdateIntegrationOutputTypeDef",
    "UpdateProviderConfigurationTypeDef",
    "UpdateS3ConfigurationTypeDef",
    "ValidationEvidenceBodyTypeDef",
    "ValidationExecutedProofTypeDef",
    "ValidationExploitArtifactTypeDef",
    "ValidationProofCodeTypeDef",
    "ValidationProofMaterialTypeDef",
    "ValidationProofOutputTypeDef",
    "ValidationSourceAnalysisTypeDef",
    "WaiterConfigTypeDef",
)

class AffectedPackageTypeDef(TypedDict):
    name: str
    version: NotRequired[str]
    fixedInVersion: NotRequired[str]
    packageManager: NotRequired[str]

class AssociateCollectorInputTypeDef(TypedDict):
    environmentId: str
    collectorArn: str
    collectorDataAccessRoleArn: str
    clientToken: NotRequired[str]

class AssociatedCollectorTypeDef(TypedDict):
    collectorId: str
    collectorArn: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AssociatedEnvironmentTypeDef(TypedDict):
    environmentId: str
    environmentArn: str
    name: str
    status: Literal["ACTIVE"]
    createdAt: datetime

class CodeScanSummaryTypeDef(TypedDict):
    scanRunId: str
    status: ScanStatusType
    origin: ScanOriginType
    createdAt: datetime
    completedAt: NotRequired[datetime]
    failureMessage: NotRequired[str]
    failureStage: NotRequired[ScanFailureStageType]

class CollectorDetailsTypeDef(TypedDict):
    collectorDataAccessRoleArn: NotRequired[str]

class CodeScanDataTypeDef(TypedDict):
    scanRunId: str
    status: ScanStatusType
    origin: ScanOriginType
    createdAt: datetime
    completedAt: NotRequired[datetime]
    failureMessage: NotRequired[str]
    failureStage: NotRequired[ScanFailureStageType]

CollectorSummaryTypeDef = TypedDict(
    "CollectorSummaryTypeDef",
    {
        "collectorId": str,
        "collectorArn": str,
        "type": Literal["AWS_COLLECTOR"],
        "status": CollectorStatusType,
        "createdAt": datetime,
    },
)

class CreateCodeFindingInputTypeDef(TypedDict):
    environmentId: str
    ocsfDocument: Mapping[str, Any]
    clientToken: NotRequired[str]

class CreateCodeScanInputTypeDef(TypedDict):
    environmentId: str
    clientToken: NotRequired[str]

class KubernetesClusterRoleConfigurationTypeDef(TypedDict):
    roleArn: str
    externalId: NotRequired[str]

class DeleteCollectorInputTypeDef(TypedDict):
    collectorId: str

class DeleteEnvironmentInputTypeDef(TypedDict):
    environmentId: str

class DeleteIntegrationInputTypeDef(TypedDict):
    integrationId: str

class GitHubTargetTypeDef(TypedDict):
    owner: str
    repository: str
    pullRequestNumber: NotRequired[int]
    headSha: NotRequired[str]

class S3TargetTypeDef(TypedDict):
    bucket: str
    key: str
    version: NotRequired[str]

class DisassociateCollectorInputTypeDef(TypedDict):
    environmentId: str
    collectorArn: str

class EnvironmentNetworkConfigurationOutputTypeDef(TypedDict):
    allowedDomains: NotRequired[list[str]]

class EnvironmentListEntryTypeDef(TypedDict):
    environmentId: str
    environmentArn: str
    name: str
    status: Literal["ACTIVE"]
    createdAt: datetime

class EnvironmentNetworkConfigurationTypeDef(TypedDict):
    allowedDomains: NotRequired[Sequence[str]]

class EnvironmentRepositorySourceTypeDef(TypedDict):
    integrationId: str
    repository: str
    defaultBranch: NotRequired[str]

class EnvironmentS3IntegrationSourceTypeDef(TypedDict):
    integrationId: str
    codePrefix: NotRequired[str]
    contextPrefix: NotRequired[str]

class FindingComplianceCheckTypeDef(TypedDict):
    uid: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]

class FindingEvidenceTypeDef(TypedDict):
    file: NotRequired[str]
    line: NotRequired[int]
    snippet: NotRequired[str]

class FindingLocationTypeDef(TypedDict):
    filePath: NotRequired[str]
    startLine: NotRequired[int]
    endLine: NotRequired[int]

FindingResourceTypeDef = TypedDict(
    "FindingResourceTypeDef",
    {
        "uid": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[str],
        "region": NotRequired[str],
    },
)
FindingSummaryTypeDef = TypedDict(
    "FindingSummaryTypeDef",
    {
        "findingId": str,
        "findingArn": str,
        "environmentId": str,
        "source": str,
        "sourceFindingId": str,
        "reportedAt": datetime,
        "status": FindingStatusType,
        "statusUpdatedAt": datetime,
        "createdAt": datetime,
        "type": FindingTypeType,
        "title": str,
        "severity": FindingSeverityIdType,
        "scanRunId": NotRequired[str],
        "statusMessage": NotRequired[str],
        "discardReason": NotRequired[FindingDiscardReasonType],
        "discardReasoning": NotRequired[str],
        "duplicateOfIssueId": NotRequired[str],
        "createdIssueId": NotRequired[str],
        "completedAt": NotRequired[datetime],
        "category": NotRequired[str],
        "filePath": NotRequired[str],
    },
)

class FlowVerdictTypeDef(TypedDict):
    flowId: str
    verdict: FlowVerdictValueType
    confidence: NotRequired[float]
    evidence: NotRequired[list[str]]

class GetCodeFindingInputTypeDef(TypedDict):
    environmentId: str
    findingId: str

class GetCodeIssueArtifactInputTypeDef(TypedDict):
    environmentId: str
    issueId: str
    artifactId: str

class IssueArtifactProducerSummaryTypeDef(TypedDict):
    agent: str

class GetCodeIssueInputTypeDef(TypedDict):
    environmentId: str
    issueId: str

class IssuePatchDeliveryTypeDef(TypedDict):
    status: IssuePatchDeliveryStatusType
    patchCount: int
    succeededCount: int
    failedCount: int
    failureReasons: NotRequired[list[DeliveryReasonType]]

class GetCodeScanInputTypeDef(TypedDict):
    environmentId: str
    scanRunId: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetCollectorDataAccessAuthorizationInputTypeDef(TypedDict):
    accountId: str
    collectorId: str
    environmentArn: NotRequired[str]

class GetCollectorInputTypeDef(TypedDict):
    collectorId: str

class GetEnvironmentInputTypeDef(TypedDict):
    environmentId: str

class GetIntegrationInputTypeDef(TypedDict):
    integrationId: str

class GetResourcePolicyInputTypeDef(TypedDict):
    arn: str

class GitHubAuthorizationConfigurationTypeDef(TypedDict):
    authorizationCode: str
    state: str
    redirectUrl: NotRequired[str]

class GitHubDetailsTypeDef(TypedDict):
    organizationName: NotRequired[str]

class GitLabConfigurationTypeDef(TypedDict):
    instanceUrl: str
    targetType: GitLabTargetTypeType
    targetPath: str
    accessToken: str

class GitLabDetailsTypeDef(TypedDict):
    instanceUrl: str
    targetType: GitLabTargetTypeType
    targetPath: str
    tokenRotation: GitLabTokenRotationType
    expiresAt: NotRequired[datetime]

RemediationProposalBodyTypeDef = TypedDict(
    "RemediationProposalBodyTypeDef",
    {
        "patch": str,
        "format": NotRequired[PatchFormatType],
        "filename": NotRequired[str],
        "patchSha256": NotRequired[str],
    },
)

class IssueSummaryTypeDef(TypedDict):
    issueId: str
    issueArn: str
    name: str
    status: IssueStatusType
    statusUpdatedAt: datetime
    createdAt: datetime
    severity: NotRequired[IssueSeverityType]
    confidence: NotRequired[int]
    phase: NotRequired[IssuePhaseType]
    statusReason: NotRequired[IssueStatusReasonType]
    statusMessage: NotRequired[str]
    updatedAt: NotRequired[datetime]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAssociatedCollectorsInputTypeDef(TypedDict):
    environmentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAssociatedEnvironmentsInputTypeDef(TypedDict):
    collectorId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCodeFindingsInputTypeDef(TypedDict):
    environmentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCodeIssueArtifactsInputTypeDef(TypedDict):
    environmentId: str
    issueId: str
    artifactType: NotRequired[IssueArtifactTypeType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCodeIssuesInputTypeDef(TypedDict):
    environmentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCodeScansInputTypeDef(TypedDict):
    environmentId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListEnvironmentsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListIntegrationsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ReasoningStepTypeDef(TypedDict):
    step: int
    claim: str
    source: str
    confidence: NotRequired[float]

class ValidationExploitArtifactTypeDef(TypedDict):
    payload: str
    targetUrl: str
    httpMethod: ArtifactHttpMethodType
    effect: ExploitEffectType
    headers: NotRequired[dict[str, str]]
    responseStatus: NotRequired[int]
    responseSnippet: NotRequired[str]

class SignalComputationTypeDef(TypedDict):
    likelihoodBand: NotRequired[SignalBandType]
    impactBand: NotRequired[SignalBandType]
    barriers: NotRequired[int]

class SignalConfidenceReasoningTypeDef(TypedDict):
    summary: str
    factors: NotRequired[list[str]]

class SignalExploitabilityTypeDef(TypedDict):
    verdict: NotRequired[ExploitabilityVerdictType]
    reachedCrownJewels: NotRequired[bool]
    highestLayerReached: NotRequired[int]
    confidenceTier: NotRequired[ValidationConfidenceTierType]
    scriptable: NotRequired[bool]
    sourceValidationArtifactId: NotRequired[str]

class S3ConfigurationTypeDef(TypedDict):
    bucket: str
    roleArn: str
    externalId: str

class S3DetailsTypeDef(TypedDict):
    bucket: str
    roleArn: str

class PutResourcePolicyInputTypeDef(TypedDict):
    arn: str
    policy: NotRequired[str]
    expectedRevisionId: NotRequired[str]

class SignalAccessPreconditionTypeDef(TypedDict):
    value: NotRequired[SignalAccessLevelType]
    basis: NotRequired[SignalBasisType]
    reason: NotRequired[str]
    missingInfo: NotRequired[str]

class SignalAttackerGainsDimensionTypeDef(TypedDict):
    value: NotRequired[SignalAttackerGainsType]
    basis: NotRequired[SignalBasisType]
    reason: NotRequired[str]
    missingInfo: NotRequired[str]

class SignalBlastRadiusDimensionTypeDef(TypedDict):
    value: NotRequired[SignalBlastRadiusType]
    basis: NotRequired[SignalBasisType]
    reason: NotRequired[str]
    missingInfo: NotRequired[str]

class SignalTargetValueDimensionTypeDef(TypedDict):
    value: NotRequired[SignalTargetValueType]
    basis: NotRequired[SignalBasisType]
    reason: NotRequired[str]
    missingInfo: NotRequired[str]

class SignalPreconditionTypeDef(TypedDict):
    value: NotRequired[bool]
    basis: NotRequired[SignalBasisType]
    reason: NotRequired[str]
    missingInfo: NotRequired[str]

class StartIntegrationAuthorizationInputTypeDef(TypedDict):
    providerType: Literal["GITHUB"]
    name: NotRequired[str]

class UpdateS3ConfigurationTypeDef(TypedDict):
    roleArn: str
    externalId: NotRequired[str]

class ValidationSourceAnalysisTypeDef(TypedDict):
    summary: str
    inferredEffect: NotRequired[ExploitEffectType]

class ValidationProofOutputTypeDef(TypedDict):
    consoleOutput: str

class ValidationProofMaterialTypeDef(TypedDict):
    content: str

class AssociateCollectorOutputTypeDef(TypedDict):
    environmentId: str
    environmentArn: str
    associatedCollector: AssociatedCollectorTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCodeFindingOutputTypeDef(TypedDict):
    findingId: str
    findingArn: str
    title: str
    status: FindingStatusType
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

CreateCollectorOutputTypeDef = TypedDict(
    "CreateCollectorOutputTypeDef",
    {
        "collectorId": str,
        "collectorArn": str,
        "type": Literal["AWS_COLLECTOR"],
        "status": CollectorStatusType,
        "createdAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateEnvironmentOutputTypeDef(TypedDict):
    environmentId: str
    environmentArn: str
    status: Literal["ACTIVE"]
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateIntegrationOutputTypeDef(TypedDict):
    integrationId: str
    integrationArn: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

GetCollectorOutputTypeDef = TypedDict(
    "GetCollectorOutputTypeDef",
    {
        "collectorId": str,
        "collectorArn": str,
        "type": Literal["AWS_COLLECTOR"],
        "status": CollectorStatusType,
        "configRecorderArn": str,
        "kubernetesClusterRoleArn": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetResourcePolicyOutputTypeDef(TypedDict):
    arn: str
    policy: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAssociatedCollectorsOutputTypeDef(TypedDict):
    associatedCollectors: list[AssociatedCollectorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PutResourcePolicyOutputTypeDef(TypedDict):
    arn: str
    policy: str
    revisionId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartIntegrationAuthorizationOutputTypeDef(TypedDict):
    state: str
    codeChallenge: str
    codeChallengeMethod: Literal["S256"]
    expiresAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

UpdateCollectorOutputTypeDef = TypedDict(
    "UpdateCollectorOutputTypeDef",
    {
        "collectorId": str,
        "collectorArn": str,
        "type": Literal["AWS_COLLECTOR"],
        "status": CollectorStatusType,
        "configRecorderArn": str,
        "kubernetesClusterRoleArn": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListAssociatedEnvironmentsOutputTypeDef(TypedDict):
    associatedEnvironments: list[AssociatedEnvironmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateCodeScanOutputTypeDef(TypedDict):
    scan: CodeScanSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCodeScansOutputTypeDef(TypedDict):
    scans: list[CodeScanSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetCodeScanOutputTypeDef(TypedDict):
    scan: CodeScanDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class ListCollectorsOutputTypeDef(TypedDict):
    items: list[CollectorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

CreateCollectorInputTypeDef = TypedDict(
    "CreateCollectorInputTypeDef",
    {
        "type": NotRequired[Literal["AWS_COLLECTOR"]],
        "kubernetesClusterRole": NotRequired[KubernetesClusterRoleConfigurationTypeDef],
        "clientToken": NotRequired[str],
    },
)
KubernetesClusterRoleUpdateTypeDef = TypedDict(
    "KubernetesClusterRoleUpdateTypeDef",
    {
        "set": NotRequired[KubernetesClusterRoleConfigurationTypeDef],
        "remove": NotRequired[Mapping[str, Any]],
    },
)

class DestinationTargetTypeDef(TypedDict):
    s3: NotRequired[S3TargetTypeDef]
    github: NotRequired[GitHubTargetTypeDef]

class EnvironmentConfigurationOutputTypeDef(TypedDict):
    network: NotRequired[EnvironmentNetworkConfigurationOutputTypeDef]
    scanFrequency: NotRequired[str]
    patchCreationPolicy: NotRequired[PatchCreationPolicyType]

class ListEnvironmentsOutputTypeDef(TypedDict):
    items: list[EnvironmentListEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

EnvironmentNetworkConfigurationUnionTypeDef = Union[
    EnvironmentNetworkConfigurationTypeDef, EnvironmentNetworkConfigurationOutputTypeDef
]

class EnvironmentSourceConfigurationOutputTypeDef(TypedDict):
    s3Sources: NotRequired[list[EnvironmentS3IntegrationSourceTypeDef]]
    repositorySources: NotRequired[list[EnvironmentRepositorySourceTypeDef]]

class EnvironmentSourceConfigurationTypeDef(TypedDict):
    s3Sources: NotRequired[Sequence[EnvironmentS3IntegrationSourceTypeDef]]
    repositorySources: NotRequired[Sequence[EnvironmentRepositorySourceTypeDef]]

class FindingPostureTypeDef(TypedDict):
    application: NotRequired[str]
    applicationUid: NotRequired[str]
    applicationVersion: NotRequired[str]
    control: NotRequired[str]
    description: NotRequired[str]
    standards: NotRequired[list[str]]
    requirements: NotRequired[list[str]]
    checks: NotRequired[list[FindingComplianceCheckTypeDef]]
    status: NotRequired[str]
    statusId: NotRequired[int]
    remediation: NotRequired[str]
    remediationReferences: NotRequired[list[str]]

class FindingValidationTypeDef(TypedDict):
    verdict: FindingVerdictType
    blockingReason: NotRequired[FindingBlockingReasonType]
    confidence: NotRequired[float]
    rationale: NotRequired[str]
    severityAdjustment: NotRequired[FindingSeverityAdjustmentType]
    mitigatingControls: NotRequired[list[str]]
    preconditions: NotRequired[list[str]]
    evidence: NotRequired[list[FindingEvidenceTypeDef]]

class FindingVulnerabilityTypeDef(TypedDict):
    title: NotRequired[str]
    description: NotRequired[str]
    cweId: NotRequired[str]
    cweCaption: NotRequired[str]
    additionalCweIds: NotRequired[list[str]]
    cveId: NotRequired[str]
    cvssBaseScore: NotRequired[float]
    fixCoverage: NotRequired[str]
    fixCoverageId: NotRequired[int]
    locations: NotRequired[list[FindingLocationTypeDef]]
    remediation: NotRequired[str]
    remediationReferences: NotRequired[list[str]]
    code: NotRequired[str]
    details: NotRequired[str]
    affectedPackages: NotRequired[list[AffectedPackageTypeDef]]

class ListCodeFindingsOutputTypeDef(TypedDict):
    items: list[FindingSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class IssueArtifactItemTypeDef(TypedDict):
    artifactId: str
    artifactType: IssueArtifactTypeType
    mediaType: str
    producer: IssueArtifactProducerSummaryTypeDef
    contentSizeBytes: int
    createdAt: datetime

class GetCodeIssueOutputTypeDef(TypedDict):
    issueId: str
    issueArn: str
    name: str
    synopsis: str
    severity: IssueSeverityType
    confidence: int
    severityReasoning: str
    summary: str
    findingIds: list[str]
    status: IssueStatusType
    phase: IssuePhaseType
    statusReason: IssueStatusReasonType
    statusMessage: str
    statusUpdatedAt: datetime
    createdAt: datetime
    updatedAt: datetime
    evidenceAvailability: IssueEvidenceAvailabilityType
    patchDelivery: IssuePatchDeliveryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetCodeScanInputWaitTypeDef(TypedDict):
    environmentId: str
    scanRunId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GitHubConfigurationTypeDef(TypedDict):
    authorization: GitHubAuthorizationConfigurationTypeDef
    organizationName: NotRequired[str]

class ListCodeIssuesOutputTypeDef(TypedDict):
    items: list[IssueSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAssociatedCollectorsInputPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAssociatedEnvironmentsInputPaginateTypeDef(TypedDict):
    collectorId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCodeFindingsInputPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCodeIssueArtifactsInputPaginateTypeDef(TypedDict):
    environmentId: str
    issueId: str
    artifactType: NotRequired[IssueArtifactTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCodeIssuesInputPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCodeScansInputPaginateTypeDef(TypedDict):
    environmentId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEnvironmentsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIntegrationsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class PerFindingResultTypeDef(TypedDict):
    findingId: str
    exploitable: ExploitabilityVerdictType
    confidence: NotRequired[float]
    flowVerdicts: NotRequired[list[FlowVerdictTypeDef]]
    reasoningChain: NotRequired[list[ReasoningStepTypeDef]]
    exploitArtifact: NotRequired[ValidationExploitArtifactTypeDef]

class ProviderDetailsTypeDef(TypedDict):
    github: NotRequired[GitHubDetailsTypeDef]
    gitlab: NotRequired[GitLabDetailsTypeDef]
    s3: NotRequired[S3DetailsTypeDef]

class SignalImpactDimensionsTypeDef(TypedDict):
    attackerGains: NotRequired[SignalAttackerGainsDimensionTypeDef]
    blastRadius: NotRequired[SignalBlastRadiusDimensionTypeDef]
    targetValue: NotRequired[SignalTargetValueDimensionTypeDef]

class SignalPreconditionsTypeDef(TypedDict):
    reachableFromAttacker: NotRequired[SignalPreconditionTypeDef]
    configurationNeeded: NotRequired[SignalPreconditionTypeDef]
    accessLevel: NotRequired[SignalAccessPreconditionTypeDef]
    userInteractionRequired: NotRequired[SignalPreconditionTypeDef]

class UpdateProviderConfigurationTypeDef(TypedDict):
    s3: NotRequired[UpdateS3ConfigurationTypeDef]

class ValidationProofCodeTypeDef(TypedDict):
    proofCode: list[ValidationProofMaterialTypeDef]

class UpdateCollectorInputTypeDef(TypedDict):
    collectorId: str
    name: NotRequired[str]
    kubernetesClusterRole: NotRequired[KubernetesClusterRoleUpdateTypeDef]

class PatchDeliveryTypeDef(TypedDict):
    status: DeliveryStatusType
    updatedAt: datetime
    target: NotRequired[DestinationTargetTypeDef]

class EnvironmentConfigurationTypeDef(TypedDict):
    network: NotRequired[EnvironmentNetworkConfigurationUnionTypeDef]
    scanFrequency: NotRequired[str]
    patchCreationPolicy: NotRequired[PatchCreationPolicyType]

class CodeConfigurationDetailsTypeDef(TypedDict):
    collectorDetails: NotRequired[CollectorDetailsTypeDef]
    sourceConfiguration: NotRequired[EnvironmentSourceConfigurationOutputTypeDef]
    environmentConfiguration: NotRequired[EnvironmentConfigurationOutputTypeDef]
    latestScan: NotRequired[CodeScanSummaryTypeDef]

EnvironmentSourceConfigurationUnionTypeDef = Union[
    EnvironmentSourceConfigurationTypeDef, EnvironmentSourceConfigurationOutputTypeDef
]
GetCodeFindingOutputTypeDef = TypedDict(
    "GetCodeFindingOutputTypeDef",
    {
        "type": FindingTypeType,
        "title": str,
        "severity": FindingSeverityIdType,
        "summary": str,
        "detailedDescription": str,
        "category": str,
        "subCategory": str,
        "cweIds": list[str],
        "owaspCategory": str,
        "mitigation": str,
        "filePath": str,
        "lineNumber": int,
        "cveId": str,
        "cvssBaseScore": float,
        "affectedPackages": list[AffectedPackageTypeDef],
        "vulnerableCode": str,
        "relevantInputs": list[str],
        "stepsToReproduce": list[str],
        "validation": FindingValidationTypeDef,
        "endLine": int,
        "mitreTechniques": list[str],
        "remediationReferences": list[str],
        "ocsfClass": FindingOcsfClassType,
        "ocsfSchemaVersion": str,
        "productName": str,
        "productVendorName": str,
        "productVersion": str,
        "sourceStatus": str,
        "sourceStatusId": int,
        "firstSeenAt": datetime,
        "findingTypes": list[str],
        "vulnerabilities": list[FindingVulnerabilityTypeDef],
        "resources": list[FindingResourceTypeDef],
        "posture": FindingPostureTypeDef,
        "findingId": str,
        "findingArn": str,
        "environmentId": str,
        "source": str,
        "sourceFindingId": str,
        "reportedAt": datetime,
        "status": FindingStatusType,
        "statusUpdatedAt": datetime,
        "createdAt": datetime,
        "scanRunId": str,
        "statusMessage": str,
        "discardReason": FindingDiscardReasonType,
        "discardReasoning": str,
        "duplicateOfIssueId": str,
        "createdIssueId": str,
        "completedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ListCodeIssueArtifactsOutputTypeDef(TypedDict):
    items: list[IssueArtifactItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ProviderConfigurationTypeDef(TypedDict):
    github: NotRequired[GitHubConfigurationTypeDef]
    gitlab: NotRequired[GitLabConfigurationTypeDef]
    s3: NotRequired[S3ConfigurationTypeDef]

class GetIntegrationOutputTypeDef(TypedDict):
    integrationId: str
    integrationArn: str
    name: str
    integrationType: IntegrationTypeType
    providerDetails: ProviderDetailsTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class IntegrationSummaryTypeDef(TypedDict):
    integrationId: str
    integrationArn: str
    name: str
    integrationType: IntegrationTypeType
    providerDetails: ProviderDetailsTypeDef
    createdAt: datetime
    updatedAt: datetime

class UpdateIntegrationOutputTypeDef(TypedDict):
    integrationId: str
    integrationArn: str
    name: str
    integrationType: IntegrationTypeType
    providerDetails: ProviderDetailsTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PrevalidationSignalTypeDef(TypedDict):
    subjectRef: NotRequired[str]
    dimension: NotRequired[SignalDimensionType]
    signalStrength: NotRequired[SignalStrengthType]
    conclusion: NotRequired[str]
    producerId: NotRequired[str]
    producerVersion: NotRequired[str]
    confidence: NotRequired[float]
    confidenceReasoning: NotRequired[SignalConfidenceReasoningTypeDef]
    computed: NotRequired[SignalComputationTypeDef]
    preconditions: NotRequired[SignalPreconditionsTypeDef]
    impactDimensions: NotRequired[SignalImpactDimensionsTypeDef]
    exploitability: NotRequired[SignalExploitabilityTypeDef]

class UpdateIntegrationInputTypeDef(TypedDict):
    integrationId: str
    providerConfiguration: UpdateProviderConfigurationTypeDef

class ValidationExecutedProofTypeDef(TypedDict):
    code: ValidationProofCodeTypeDef
    output: NotRequired[ValidationProofOutputTypeDef]
    observedEffect: NotRequired[ExploitEffectType]

PatchBodyTypeDef = TypedDict(
    "PatchBodyTypeDef",
    {
        "patch": str,
        "patchSha256": str,
        "sizeBytes": int,
        "format": NotRequired[PatchFormatType],
        "repositoryName": NotRequired[str],
        "delivery": NotRequired[PatchDeliveryTypeDef],
    },
)
EnvironmentConfigurationUnionTypeDef = Union[
    EnvironmentConfigurationTypeDef, EnvironmentConfigurationOutputTypeDef
]

class EnvironmentConfigurationDetailsTypeDef(TypedDict):
    codeConfiguration: NotRequired[CodeConfigurationDetailsTypeDef]

class CreateIntegrationInputTypeDef(TypedDict):
    name: str
    providerConfiguration: ProviderConfigurationTypeDef
    clientToken: NotRequired[str]

class ListIntegrationsOutputTypeDef(TypedDict):
    items: list[IntegrationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class PrevalidationSignalsBodyTypeDef(TypedDict):
    producedBy: NotRequired[str]
    signals: NotRequired[list[PrevalidationSignalTypeDef]]

class ValidationEvidenceBodyTypeDef(TypedDict):
    exploitable: ExploitabilityVerdictType
    terminalStatus: NotRequired[ValidationTerminalStatusType]
    flowVerdicts: NotRequired[list[FlowVerdictTypeDef]]
    attackFlowsConfirmed: NotRequired[list[str]]
    exploitArtifact: NotRequired[ValidationExploitArtifactTypeDef]
    executedProof: NotRequired[ValidationExecutedProofTypeDef]
    sourceAnalysis: NotRequired[ValidationSourceAnalysisTypeDef]
    perFindingResults: NotRequired[list[PerFindingResultTypeDef]]

class CreateCodeConfigurationTypeDef(TypedDict):
    sourceConfiguration: NotRequired[EnvironmentSourceConfigurationUnionTypeDef]
    environmentConfiguration: NotRequired[EnvironmentConfigurationUnionTypeDef]

class UpdateCodeConfigurationTypeDef(TypedDict):
    sourceConfiguration: NotRequired[EnvironmentSourceConfigurationUnionTypeDef]
    environmentConfiguration: NotRequired[EnvironmentConfigurationUnionTypeDef]

class GetEnvironmentOutputTypeDef(TypedDict):
    environmentId: str
    environmentArn: str
    name: str
    status: Literal["ACTIVE"]
    statusMessage: str
    statusUpdatedAt: datetime
    createdAt: datetime
    updatedAt: datetime
    configuration: EnvironmentConfigurationDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEnvironmentOutputTypeDef(TypedDict):
    environmentId: str
    environmentArn: str
    name: str
    status: Literal["ACTIVE"]
    statusMessage: str
    statusUpdatedAt: datetime
    createdAt: datetime
    configuration: EnvironmentConfigurationDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class IssueArtifactBodyTypeDef(TypedDict):
    validationEvidence: NotRequired[ValidationEvidenceBodyTypeDef]
    prevalidationSignals: NotRequired[PrevalidationSignalsBodyTypeDef]
    remediationProposal: NotRequired[RemediationProposalBodyTypeDef]
    patch: NotRequired[PatchBodyTypeDef]
    raw: NotRequired[str]

class CreateEnvironmentConfigurationTypeDef(TypedDict):
    codeConfiguration: NotRequired[CreateCodeConfigurationTypeDef]

class UpdateEnvironmentConfigurationTypeDef(TypedDict):
    codeConfiguration: NotRequired[UpdateCodeConfigurationTypeDef]

class GetCodeIssueArtifactOutputTypeDef(TypedDict):
    artifactId: str
    artifactType: IssueArtifactTypeType
    mediaType: str
    body: IssueArtifactBodyTypeDef
    metadata: dict[str, Any]
    producer: IssueArtifactProducerSummaryTypeDef
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateEnvironmentInputTypeDef(TypedDict):
    name: str
    configuration: NotRequired[CreateEnvironmentConfigurationTypeDef]

class UpdateEnvironmentInputTypeDef(TypedDict):
    environmentId: str
    name: NotRequired[str]
    configuration: NotRequired[UpdateEnvironmentConfigurationTypeDef]
