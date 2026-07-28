"""
Type annotations for securityagent service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_securityagent.type_defs import VpcConfigOutputTypeDef

    data: VpcConfigOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    AccessTypeType,
    ArtifactTypeType,
    AuthenticationProviderTypeType,
    CleanUpStrategyType,
    CodeRemediationStrategyType,
    CodeRemediationTaskStatusType,
    ConfidenceLevelType,
    ContextTypeType,
    DomainVerificationMethodType,
    ErrorCodeType,
    FindingStatusType,
    GitLabTokenTypeType,
    IpAddressTypeType,
    JobStatusType,
    ManagementTypeType,
    MembershipTypeFilterType,
    NetworkTrafficRuleEffectType,
    PrivateConnectionStatusType,
    PrivateConnectionTypeType,
    ProviderType,
    ProviderTypeType,
    ResourceConfigDnsResolutionType,
    ResourceTypeType,
    RiskLevelType,
    RiskTypeType,
    SecurityRequirementArtifactFormatType,
    SecurityRequirementPackImportStatusType,
    SecurityRequirementPackStatusType,
    SkillTypeType,
    StepNameType,
    StepStatusType,
    StrideCategoryType,
    TargetDomainStatusType,
    TaskExecutionStatusType,
    ThreatActorType,
    ThreatSeverityType,
    ThreatStatusType,
    ValidationModeType,
    ValidationStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AWSResourcesOutputTypeDef",
    "AWSResourcesTypeDef",
    "AWSResourcesUnionTypeDef",
    "ActorOutputTypeDef",
    "ActorTypeDef",
    "AddArtifactInputTypeDef",
    "AddArtifactOutputTypeDef",
    "AgentSpaceSummaryTypeDef",
    "AgentSpaceTypeDef",
    "ApplicationSummaryTypeDef",
    "ArtifactMetadataItemTypeDef",
    "ArtifactSummaryTypeDef",
    "ArtifactTypeDef",
    "AssetsOutputTypeDef",
    "AssetsTypeDef",
    "AssetsUnionTypeDef",
    "AuthenticationTypeDef",
    "BatchCreateSecurityRequirementResultTypeDef",
    "BatchCreateSecurityRequirementsInputTypeDef",
    "BatchCreateSecurityRequirementsOutputTypeDef",
    "BatchDeleteCodeReviewsInputTypeDef",
    "BatchDeleteCodeReviewsOutputTypeDef",
    "BatchDeletePentestsInputTypeDef",
    "BatchDeletePentestsOutputTypeDef",
    "BatchDeleteSecurityRequirementsInputTypeDef",
    "BatchDeleteSecurityRequirementsOutputTypeDef",
    "BatchDeleteThreatModelsInputTypeDef",
    "BatchDeleteThreatModelsOutputTypeDef",
    "BatchGetAgentSpacesInputTypeDef",
    "BatchGetAgentSpacesOutputTypeDef",
    "BatchGetArtifactMetadataInputTypeDef",
    "BatchGetArtifactMetadataOutputTypeDef",
    "BatchGetCodeReviewJobTasksInputTypeDef",
    "BatchGetCodeReviewJobTasksOutputTypeDef",
    "BatchGetCodeReviewJobsInputTypeDef",
    "BatchGetCodeReviewJobsOutputTypeDef",
    "BatchGetCodeReviewsInputTypeDef",
    "BatchGetCodeReviewsOutputTypeDef",
    "BatchGetFindingsInputTypeDef",
    "BatchGetFindingsOutputTypeDef",
    "BatchGetPentestJobTasksInputTypeDef",
    "BatchGetPentestJobTasksOutputTypeDef",
    "BatchGetPentestJobsInputTypeDef",
    "BatchGetPentestJobsOutputTypeDef",
    "BatchGetPentestsInputTypeDef",
    "BatchGetPentestsOutputTypeDef",
    "BatchGetSecurityRequirementResultTypeDef",
    "BatchGetSecurityRequirementsInputTypeDef",
    "BatchGetSecurityRequirementsOutputTypeDef",
    "BatchGetTargetDomainsInputTypeDef",
    "BatchGetTargetDomainsOutputTypeDef",
    "BatchGetThreatModelJobTasksInputTypeDef",
    "BatchGetThreatModelJobTasksOutputTypeDef",
    "BatchGetThreatModelJobsInputTypeDef",
    "BatchGetThreatModelJobsOutputTypeDef",
    "BatchGetThreatModelsInputTypeDef",
    "BatchGetThreatModelsOutputTypeDef",
    "BatchGetThreatsInputTypeDef",
    "BatchGetThreatsOutputTypeDef",
    "BatchSecurityRequirementErrorTypeDef",
    "BatchUpdateSecurityRequirementsInputTypeDef",
    "BatchUpdateSecurityRequirementsOutputTypeDef",
    "BitbucketIntegrationInputTypeDef",
    "BitbucketRepositoryMetadataTypeDef",
    "BitbucketRepositoryResourceTypeDef",
    "BitbucketResourceCapabilitiesTypeDef",
    "BlobTypeDef",
    "CategoryTypeDef",
    "CloudWatchLogTypeDef",
    "CodeLocationTypeDef",
    "CodeRemediationTaskDetailsTypeDef",
    "CodeRemediationTaskTypeDef",
    "CodeReviewJobSummaryTypeDef",
    "CodeReviewJobTaskSummaryTypeDef",
    "CodeReviewJobTaskTypeDef",
    "CodeReviewJobTypeDef",
    "CodeReviewSettingsTypeDef",
    "CodeReviewSummaryTypeDef",
    "CodeReviewTypeDef",
    "ConfluenceDocumentMetadataTypeDef",
    "ConfluenceDocumentResourceTypeDef",
    "ConfluenceIntegrationInputTypeDef",
    "ConfluenceResourceCapabilitiesTypeDef",
    "CreateAgentSpaceInputTypeDef",
    "CreateAgentSpaceOutputTypeDef",
    "CreateApplicationRequestTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateCodeReviewInputTypeDef",
    "CreateCodeReviewOutputTypeDef",
    "CreateIntegrationInputTypeDef",
    "CreateIntegrationOutputTypeDef",
    "CreateMembershipRequestTypeDef",
    "CreatePentestInputTypeDef",
    "CreatePentestOutputTypeDef",
    "CreatePrivateConnectionInputTypeDef",
    "CreatePrivateConnectionOutputTypeDef",
    "CreateSecurityRequirementEntryTypeDef",
    "CreateSecurityRequirementPackInputTypeDef",
    "CreateSecurityRequirementPackOutputTypeDef",
    "CreateTargetDomainInputTypeDef",
    "CreateTargetDomainOutputTypeDef",
    "CreateThreatInputTypeDef",
    "CreateThreatModelInputTypeDef",
    "CreateThreatModelOutputTypeDef",
    "CreateThreatOutputTypeDef",
    "CustomHeaderTypeDef",
    "DeleteAgentSpaceInputTypeDef",
    "DeleteAgentSpaceOutputTypeDef",
    "DeleteApplicationRequestTypeDef",
    "DeleteArtifactInputTypeDef",
    "DeleteCodeReviewFailureTypeDef",
    "DeleteIntegrationInputTypeDef",
    "DeleteMembershipRequestTypeDef",
    "DeletePentestFailureTypeDef",
    "DeletePrivateConnectionInputTypeDef",
    "DeletePrivateConnectionOutputTypeDef",
    "DeleteSecurityRequirementPackInputTypeDef",
    "DeleteTargetDomainInputTypeDef",
    "DeleteTargetDomainOutputTypeDef",
    "DeleteThreatModelFailureTypeDef",
    "DescribePrivateConnectionInputTypeDef",
    "DescribePrivateConnectionOutputTypeDef",
    "DiffSourceTypeDef",
    "DiscoveredEndpointTypeDef",
    "DnsVerificationTypeDef",
    "DocumentInfoTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointTypeDef",
    "ErrorInformationTypeDef",
    "ExecutionContextTypeDef",
    "FindingSummaryTypeDef",
    "FindingTypeDef",
    "GetApplicationRequestTypeDef",
    "GetApplicationResponseTypeDef",
    "GetArtifactInputTypeDef",
    "GetArtifactOutputTypeDef",
    "GetIntegrationInputTypeDef",
    "GetIntegrationOutputTypeDef",
    "GetSecurityRequirementPackInputTypeDef",
    "GetSecurityRequirementPackOutputTypeDef",
    "GitHubIntegrationInputTypeDef",
    "GitHubRepositoryMetadataTypeDef",
    "GitHubRepositoryResourceTypeDef",
    "GitHubResourceCapabilitiesTypeDef",
    "GitLabIntegrationInputTypeDef",
    "GitLabRepositoryMetadataTypeDef",
    "GitLabRepositoryResourceTypeDef",
    "GitLabResourceCapabilitiesTypeDef",
    "HttpVerificationTypeDef",
    "IdCConfigurationTypeDef",
    "ImportSecurityRequirementsInputTypeDef",
    "ImportSecurityRequirementsOutputTypeDef",
    "ImportSourceTypeDef",
    "InitiateProviderRegistrationInputTypeDef",
    "InitiateProviderRegistrationOutputTypeDef",
    "IntegratedDocumentTypeDef",
    "IntegratedRepositoryTypeDef",
    "IntegratedResourceInputItemTypeDef",
    "IntegratedResourceMetadataTypeDef",
    "IntegratedResourceSummaryTypeDef",
    "IntegratedResourceTypeDef",
    "IntegrationFilterTypeDef",
    "IntegrationSummaryTypeDef",
    "ListAgentSpacesInputPaginateTypeDef",
    "ListAgentSpacesInputTypeDef",
    "ListAgentSpacesOutputTypeDef",
    "ListApplicationsRequestPaginateTypeDef",
    "ListApplicationsRequestTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListArtifactsInputPaginateTypeDef",
    "ListArtifactsInputTypeDef",
    "ListArtifactsOutputTypeDef",
    "ListCodeReviewJobTasksInputPaginateTypeDef",
    "ListCodeReviewJobTasksInputTypeDef",
    "ListCodeReviewJobTasksOutputTypeDef",
    "ListCodeReviewJobsForCodeReviewInputPaginateTypeDef",
    "ListCodeReviewJobsForCodeReviewInputTypeDef",
    "ListCodeReviewJobsForCodeReviewOutputTypeDef",
    "ListCodeReviewsInputPaginateTypeDef",
    "ListCodeReviewsInputTypeDef",
    "ListCodeReviewsOutputTypeDef",
    "ListDiscoveredEndpointsInputPaginateTypeDef",
    "ListDiscoveredEndpointsInputTypeDef",
    "ListDiscoveredEndpointsOutputTypeDef",
    "ListFindingsInputPaginateTypeDef",
    "ListFindingsInputTypeDef",
    "ListFindingsOutputTypeDef",
    "ListIntegratedResourcesInputPaginateTypeDef",
    "ListIntegratedResourcesInputTypeDef",
    "ListIntegratedResourcesOutputTypeDef",
    "ListIntegrationsInputPaginateTypeDef",
    "ListIntegrationsInputTypeDef",
    "ListIntegrationsOutputTypeDef",
    "ListMembershipsRequestPaginateTypeDef",
    "ListMembershipsRequestTypeDef",
    "ListMembershipsResponseTypeDef",
    "ListPentestJobTasksInputPaginateTypeDef",
    "ListPentestJobTasksInputTypeDef",
    "ListPentestJobTasksOutputTypeDef",
    "ListPentestJobsForPentestInputPaginateTypeDef",
    "ListPentestJobsForPentestInputTypeDef",
    "ListPentestJobsForPentestOutputTypeDef",
    "ListPentestsInputPaginateTypeDef",
    "ListPentestsInputTypeDef",
    "ListPentestsOutputTypeDef",
    "ListPrivateConnectionsInputPaginateTypeDef",
    "ListPrivateConnectionsInputTypeDef",
    "ListPrivateConnectionsOutputTypeDef",
    "ListSecurityRequirementPackFilterTypeDef",
    "ListSecurityRequirementPacksInputPaginateTypeDef",
    "ListSecurityRequirementPacksInputTypeDef",
    "ListSecurityRequirementPacksOutputTypeDef",
    "ListSecurityRequirementsInputPaginateTypeDef",
    "ListSecurityRequirementsInputTypeDef",
    "ListSecurityRequirementsOutputTypeDef",
    "ListTagsForResourceInputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListTargetDomainsInputPaginateTypeDef",
    "ListTargetDomainsInputTypeDef",
    "ListTargetDomainsOutputTypeDef",
    "ListThreatModelJobTasksInputPaginateTypeDef",
    "ListThreatModelJobTasksInputTypeDef",
    "ListThreatModelJobTasksOutputTypeDef",
    "ListThreatModelJobsInputPaginateTypeDef",
    "ListThreatModelJobsInputTypeDef",
    "ListThreatModelJobsOutputTypeDef",
    "ListThreatModelsInputPaginateTypeDef",
    "ListThreatModelsInputTypeDef",
    "ListThreatModelsOutputTypeDef",
    "ListThreatsInputPaginateTypeDef",
    "ListThreatsInputTypeDef",
    "ListThreatsOutputTypeDef",
    "LogLocationTypeDef",
    "MemberMetadataTypeDef",
    "MembershipConfigTypeDef",
    "MembershipSummaryTypeDef",
    "NetworkTrafficConfigOutputTypeDef",
    "NetworkTrafficConfigTypeDef",
    "NetworkTrafficConfigUnionTypeDef",
    "NetworkTrafficRuleTypeDef",
    "PaginatorConfigTypeDef",
    "PentestJobSummaryTypeDef",
    "PentestJobTypeDef",
    "PentestSummaryTypeDef",
    "PentestTypeDef",
    "PrivateConnectionModeTypeDef",
    "PrivateConnectionSummaryTypeDef",
    "ProviderInputTypeDef",
    "ProviderResourceCapabilitiesTypeDef",
    "ReportDestinationTypeDef",
    "ResponseMetadataTypeDef",
    "SecurityRequirementArtifactTypeDef",
    "SecurityRequirementPackSummaryTypeDef",
    "SecurityRequirementSummaryTypeDef",
    "SelfManagedInputTypeDef",
    "ServiceManagedInputTypeDef",
    "SourceCodeRepositoryTypeDef",
    "StartCodeRemediationInputTypeDef",
    "StartCodeReviewJobInputTypeDef",
    "StartCodeReviewJobOutputTypeDef",
    "StartPentestJobInputTypeDef",
    "StartPentestJobOutputTypeDef",
    "StartThreatModelJobInputTypeDef",
    "StartThreatModelJobOutputTypeDef",
    "StepTypeDef",
    "StopCodeReviewJobInputTypeDef",
    "StopPentestJobInputTypeDef",
    "StopThreatModelJobInputTypeDef",
    "TagResourceInputTypeDef",
    "TargetDomainSummaryTypeDef",
    "TargetDomainTypeDef",
    "TaskSummaryTypeDef",
    "TaskTypeDef",
    "ThreatAnchorShapeTypeDef",
    "ThreatEvidenceShapeTypeDef",
    "ThreatModelJobSummaryTypeDef",
    "ThreatModelJobTaskSummaryTypeDef",
    "ThreatModelJobTaskTypeDef",
    "ThreatModelJobTypeDef",
    "ThreatModelSummaryTypeDef",
    "ThreatModelTypeDef",
    "ThreatSummaryTypeDef",
    "ThreatTypeDef",
    "UntagResourceInputTypeDef",
    "UpdateAgentSpaceInputTypeDef",
    "UpdateAgentSpaceOutputTypeDef",
    "UpdateApplicationRequestTypeDef",
    "UpdateApplicationResponseTypeDef",
    "UpdateCodeReviewInputTypeDef",
    "UpdateCodeReviewOutputTypeDef",
    "UpdateFindingInputTypeDef",
    "UpdateIntegratedResourcesInputTypeDef",
    "UpdatePentestInputTypeDef",
    "UpdatePentestOutputTypeDef",
    "UpdatePrivateConnectionCertificateInputTypeDef",
    "UpdatePrivateConnectionCertificateOutputTypeDef",
    "UpdateSecurityRequirementEntryTypeDef",
    "UpdateSecurityRequirementPackInputTypeDef",
    "UpdateSecurityRequirementPackOutputTypeDef",
    "UpdateTargetDomainInputTypeDef",
    "UpdateTargetDomainOutputTypeDef",
    "UpdateThreatInputTypeDef",
    "UpdateThreatModelInputTypeDef",
    "UpdateThreatModelOutputTypeDef",
    "UpdateThreatOutputTypeDef",
    "UserConfigTypeDef",
    "UserMetadataTypeDef",
    "VerificationDetailsTypeDef",
    "VerificationScriptEnvVarTypeDef",
    "VerificationScriptTypeDef",
    "VerifyTargetDomainInputTypeDef",
    "VerifyTargetDomainOutputTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "VpcConfigUnionTypeDef",
)

class VpcConfigOutputTypeDef(TypedDict):
    vpcArn: NotRequired[str]
    securityGroupArns: NotRequired[list[str]]
    subnetArns: NotRequired[list[str]]

class VpcConfigTypeDef(TypedDict):
    vpcArn: NotRequired[str]
    securityGroupArns: NotRequired[Sequence[str]]
    subnetArns: NotRequired[Sequence[str]]

class AuthenticationTypeDef(TypedDict):
    providerType: NotRequired[AuthenticationProviderTypeType]
    value: NotRequired[str]

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AgentSpaceSummaryTypeDef(TypedDict):
    agentSpaceId: str
    name: str
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class CodeReviewSettingsTypeDef(TypedDict):
    controlsScanning: bool
    generalPurposeScanning: bool

class ApplicationSummaryTypeDef(TypedDict):
    applicationId: str
    applicationName: str
    domain: str
    defaultKmsKeyId: NotRequired[str]

class ArtifactMetadataItemTypeDef(TypedDict):
    agentSpaceId: str
    artifactId: str
    fileName: str
    updatedAt: datetime

class ArtifactSummaryTypeDef(TypedDict):
    artifactId: str
    fileName: str
    artifactType: ArtifactTypeType

ArtifactTypeDef = TypedDict(
    "ArtifactTypeDef",
    {
        "contents": str,
        "type": ArtifactTypeType,
    },
)

class EndpointTypeDef(TypedDict):
    uri: NotRequired[str]

class IntegratedRepositoryTypeDef(TypedDict):
    integrationId: str
    providerResourceId: str

class SourceCodeRepositoryTypeDef(TypedDict):
    s3Location: NotRequired[str]

class BatchCreateSecurityRequirementResultTypeDef(TypedDict):
    packId: str
    name: str
    description: str
    domain: str
    evaluation: str
    createdAt: datetime
    updatedAt: datetime
    remediation: NotRequired[str]

class CreateSecurityRequirementEntryTypeDef(TypedDict):
    name: str
    description: str
    domain: str
    evaluation: str
    remediation: NotRequired[str]

class BatchSecurityRequirementErrorTypeDef(TypedDict):
    securityRequirementName: str
    code: str
    message: str

class BatchDeleteCodeReviewsInputTypeDef(TypedDict):
    codeReviewIds: Sequence[str]
    agentSpaceId: str

class DeleteCodeReviewFailureTypeDef(TypedDict):
    codeReviewId: NotRequired[str]
    reason: NotRequired[str]

class BatchDeletePentestsInputTypeDef(TypedDict):
    pentestIds: Sequence[str]
    agentSpaceId: str

class DeletePentestFailureTypeDef(TypedDict):
    pentestId: NotRequired[str]
    reason: NotRequired[str]

class BatchDeleteSecurityRequirementsInputTypeDef(TypedDict):
    packId: str
    securityRequirementNames: Sequence[str]

class BatchDeleteThreatModelsInputTypeDef(TypedDict):
    threatModelIds: Sequence[str]
    agentSpaceId: str

class DeleteThreatModelFailureTypeDef(TypedDict):
    threatModelId: NotRequired[str]
    reason: NotRequired[str]

class BatchGetAgentSpacesInputTypeDef(TypedDict):
    agentSpaceIds: Sequence[str]

class BatchGetArtifactMetadataInputTypeDef(TypedDict):
    agentSpaceId: str
    artifactIds: Sequence[str]

class BatchGetCodeReviewJobTasksInputTypeDef(TypedDict):
    agentSpaceId: str
    codeReviewJobTaskIds: Sequence[str]

class BatchGetCodeReviewJobsInputTypeDef(TypedDict):
    codeReviewJobIds: Sequence[str]
    agentSpaceId: str

class BatchGetCodeReviewsInputTypeDef(TypedDict):
    codeReviewIds: Sequence[str]
    agentSpaceId: str

class BatchGetFindingsInputTypeDef(TypedDict):
    findingIds: Sequence[str]
    agentSpaceId: str

class BatchGetPentestJobTasksInputTypeDef(TypedDict):
    agentSpaceId: str
    taskIds: Sequence[str]

class BatchGetPentestJobsInputTypeDef(TypedDict):
    pentestJobIds: Sequence[str]
    agentSpaceId: str

class BatchGetPentestsInputTypeDef(TypedDict):
    pentestIds: Sequence[str]
    agentSpaceId: str

class BatchGetSecurityRequirementResultTypeDef(TypedDict):
    packId: str
    name: str
    description: str
    domain: str
    evaluation: str
    createdAt: datetime
    updatedAt: datetime
    remediation: NotRequired[str]

class BatchGetSecurityRequirementsInputTypeDef(TypedDict):
    packId: str
    securityRequirementNames: Sequence[str]

class BatchGetTargetDomainsInputTypeDef(TypedDict):
    targetDomainIds: Sequence[str]

class BatchGetThreatModelJobTasksInputTypeDef(TypedDict):
    agentSpaceId: str
    threatModelJobTaskIds: Sequence[str]

class BatchGetThreatModelJobsInputTypeDef(TypedDict):
    threatModelJobIds: Sequence[str]
    agentSpaceId: str

class BatchGetThreatModelsInputTypeDef(TypedDict):
    threatModelIds: Sequence[str]
    agentSpaceId: str

class BatchGetThreatsInputTypeDef(TypedDict):
    threatIds: Sequence[str]
    agentSpaceId: str

class UpdateSecurityRequirementEntryTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    domain: NotRequired[str]
    evaluation: NotRequired[str]
    remediation: NotRequired[str]

class BitbucketIntegrationInputTypeDef(TypedDict):
    installationId: str
    workspace: str
    code: str
    state: str

class BitbucketRepositoryMetadataTypeDef(TypedDict):
    name: str
    providerResourceId: str
    workspace: str
    accessType: NotRequired[AccessTypeType]

class BitbucketRepositoryResourceTypeDef(TypedDict):
    name: str
    workspace: str

class BitbucketResourceCapabilitiesTypeDef(TypedDict):
    leaveComments: NotRequired[bool]
    remediateCode: NotRequired[bool]

class CategoryTypeDef(TypedDict):
    name: NotRequired[str]
    isPrimary: NotRequired[bool]

class CloudWatchLogTypeDef(TypedDict):
    logGroup: NotRequired[str]
    logStream: NotRequired[str]

class CodeLocationTypeDef(TypedDict):
    filePath: str
    lineStart: NotRequired[int]
    lineEnd: NotRequired[int]
    label: NotRequired[str]

class CodeRemediationTaskDetailsTypeDef(TypedDict):
    repoName: NotRequired[str]
    codeDiffLink: NotRequired[str]
    pullRequestLink: NotRequired[str]

class CodeReviewJobSummaryTypeDef(TypedDict):
    codeReviewJobId: str
    codeReviewId: str
    title: NotRequired[str]
    status: NotRequired[JobStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class CodeReviewJobTaskSummaryTypeDef(TypedDict):
    taskId: str
    codeReviewId: NotRequired[str]
    codeReviewJobId: NotRequired[str]
    agentSpaceId: NotRequired[str]
    title: NotRequired[str]
    riskType: NotRequired[RiskTypeType]
    executionStatus: NotRequired[TaskExecutionStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ErrorInformationTypeDef(TypedDict):
    code: NotRequired[ErrorCodeType]
    message: NotRequired[str]

class ExecutionContextTypeDef(TypedDict):
    contextType: NotRequired[ContextTypeType]
    context: NotRequired[str]
    timestamp: NotRequired[datetime]

class StepTypeDef(TypedDict):
    name: NotRequired[StepNameType]
    status: NotRequired[StepStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class CodeReviewSummaryTypeDef(TypedDict):
    codeReviewId: str
    agentSpaceId: str
    title: str
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ConfluenceDocumentMetadataTypeDef(TypedDict):
    name: str
    providerResourceId: str
    spaceKey: str
    pageId: str
    title: NotRequired[str]
    spaceTitle: NotRequired[str]

class ConfluenceDocumentResourceTypeDef(TypedDict):
    name: str
    spaceKey: str
    pageId: str
    title: NotRequired[str]
    spaceTitle: NotRequired[str]

class ConfluenceIntegrationInputTypeDef(TypedDict):
    installationId: str
    code: str
    state: str
    siteUrl: str

class ConfluenceResourceCapabilitiesTypeDef(TypedDict):
    fetchDocument: NotRequired[bool]
    createDocument: NotRequired[bool]
    updateDocument: NotRequired[bool]

class CreateApplicationRequestTypeDef(TypedDict):
    idcInstanceArn: NotRequired[str]
    roleArn: NotRequired[str]
    defaultKmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateSecurityRequirementPackInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    status: NotRequired[SecurityRequirementPackStatusType]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateTargetDomainInputTypeDef(TypedDict):
    targetDomainName: str
    verificationMethod: DomainVerificationMethodType
    tags: NotRequired[Mapping[str, str]]

ThreatAnchorShapeTypeDef = TypedDict(
    "ThreatAnchorShapeTypeDef",
    {
        "kind": NotRequired[str],
        "id": NotRequired[str],
        "packageId": NotRequired[str],
    },
)

class ThreatEvidenceShapeTypeDef(TypedDict):
    packageId: NotRequired[str]
    path: NotRequired[str]

class ReportDestinationTypeDef(TypedDict):
    integrationId: str
    containerId: str
    parentId: NotRequired[str]
    documentId: NotRequired[str]

class CustomHeaderTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]

class DeleteAgentSpaceInputTypeDef(TypedDict):
    agentSpaceId: str

class DeleteApplicationRequestTypeDef(TypedDict):
    applicationId: str

class DeleteArtifactInputTypeDef(TypedDict):
    agentSpaceId: str
    artifactId: str

class DeleteIntegrationInputTypeDef(TypedDict):
    integrationId: str

class DeleteMembershipRequestTypeDef(TypedDict):
    applicationId: str
    agentSpaceId: str
    membershipId: str
    memberType: NotRequired[Literal["USER"]]

class DeletePrivateConnectionInputTypeDef(TypedDict):
    privateConnectionName: str

class DeleteSecurityRequirementPackInputTypeDef(TypedDict):
    packId: str

class DeleteTargetDomainInputTypeDef(TypedDict):
    targetDomainId: str

class DescribePrivateConnectionInputTypeDef(TypedDict):
    privateConnectionName: str

class DiffSourceTypeDef(TypedDict):
    s3Uri: NotRequired[str]

class DiscoveredEndpointTypeDef(TypedDict):
    uri: str
    pentestJobId: str
    taskId: str
    agentSpaceId: str
    evidence: NotRequired[str]
    operation: NotRequired[str]
    description: NotRequired[str]

class DnsVerificationTypeDef(TypedDict):
    token: NotRequired[str]
    dnsRecordName: NotRequired[str]
    dnsRecordType: NotRequired[Literal["TXT"]]

class IntegratedDocumentTypeDef(TypedDict):
    integrationId: str
    resourceId: str

class FindingSummaryTypeDef(TypedDict):
    findingId: str
    agentSpaceId: str
    pentestId: NotRequired[str]
    pentestJobId: NotRequired[str]
    codeReviewId: NotRequired[str]
    codeReviewJobId: NotRequired[str]
    name: NotRequired[str]
    status: NotRequired[FindingStatusType]
    riskType: NotRequired[str]
    riskLevel: NotRequired[RiskLevelType]
    confidence: NotRequired[ConfidenceLevelType]
    validationStatus: NotRequired[ValidationStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class GetApplicationRequestTypeDef(TypedDict):
    applicationId: str

class IdCConfigurationTypeDef(TypedDict):
    idcApplicationArn: NotRequired[str]
    idcInstanceArn: NotRequired[str]

class GetArtifactInputTypeDef(TypedDict):
    agentSpaceId: str
    artifactId: str

class GetIntegrationInputTypeDef(TypedDict):
    integrationId: str

class GetSecurityRequirementPackInputTypeDef(TypedDict):
    packId: str

class GitHubIntegrationInputTypeDef(TypedDict):
    code: str
    state: str
    organizationName: NotRequired[str]
    targetUrl: NotRequired[str]
    installationId: NotRequired[str]

class GitHubRepositoryMetadataTypeDef(TypedDict):
    name: str
    providerResourceId: str
    owner: str
    accessType: NotRequired[AccessTypeType]

class GitHubRepositoryResourceTypeDef(TypedDict):
    name: str
    owner: str

class GitHubResourceCapabilitiesTypeDef(TypedDict):
    leaveComments: NotRequired[bool]
    remediateCode: NotRequired[bool]

class GitLabIntegrationInputTypeDef(TypedDict):
    accessToken: str
    tokenType: GitLabTokenTypeType
    targetUrl: NotRequired[str]
    groupId: NotRequired[str]

class GitLabRepositoryMetadataTypeDef(TypedDict):
    name: str
    providerResourceId: str
    namespace: str
    accessType: NotRequired[AccessTypeType]

class GitLabRepositoryResourceTypeDef(TypedDict):
    name: str
    namespace: str

class GitLabResourceCapabilitiesTypeDef(TypedDict):
    leaveComments: NotRequired[bool]
    remediateCode: NotRequired[bool]

class HttpVerificationTypeDef(TypedDict):
    token: NotRequired[str]
    routePath: NotRequired[str]

class InitiateProviderRegistrationInputTypeDef(TypedDict):
    provider: ProviderType

class IntegrationFilterTypeDef(TypedDict):
    provider: NotRequired[ProviderType]
    providerType: NotRequired[ProviderTypeType]

class IntegrationSummaryTypeDef(TypedDict):
    integrationId: str
    installationId: str
    provider: ProviderType
    providerType: ProviderTypeType
    displayName: str
    targetUrl: NotRequired[str]
    privateConnectionName: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAgentSpacesInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListApplicationsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListArtifactsInputTypeDef(TypedDict):
    agentSpaceId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListCodeReviewJobTasksInputTypeDef(TypedDict):
    agentSpaceId: str
    maxResults: NotRequired[int]
    codeReviewJobId: NotRequired[str]
    stepName: NotRequired[StepNameType]
    categoryName: NotRequired[str]
    nextToken: NotRequired[str]

class ListCodeReviewJobsForCodeReviewInputTypeDef(TypedDict):
    codeReviewId: str
    agentSpaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListCodeReviewsInputTypeDef(TypedDict):
    agentSpaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListDiscoveredEndpointsInputTypeDef(TypedDict):
    pentestJobId: str
    agentSpaceId: str
    maxResults: NotRequired[int]
    prefix: NotRequired[str]
    nextToken: NotRequired[str]

class ListFindingsInputTypeDef(TypedDict):
    agentSpaceId: str
    maxResults: NotRequired[int]
    pentestJobId: NotRequired[str]
    codeReviewJobId: NotRequired[str]
    nextToken: NotRequired[str]
    riskType: NotRequired[str]
    riskLevel: NotRequired[RiskLevelType]
    status: NotRequired[FindingStatusType]
    confidence: NotRequired[ConfidenceLevelType]
    name: NotRequired[str]

class ListIntegratedResourcesInputTypeDef(TypedDict):
    agentSpaceId: str
    integrationId: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListMembershipsRequestTypeDef(TypedDict):
    applicationId: str
    agentSpaceId: str
    memberType: NotRequired[MembershipTypeFilterType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListPentestJobTasksInputTypeDef(TypedDict):
    agentSpaceId: str
    maxResults: NotRequired[int]
    pentestJobId: NotRequired[str]
    stepName: NotRequired[StepNameType]
    categoryName: NotRequired[str]
    nextToken: NotRequired[str]

class TaskSummaryTypeDef(TypedDict):
    taskId: str
    pentestId: NotRequired[str]
    pentestJobId: NotRequired[str]
    agentSpaceId: NotRequired[str]
    title: NotRequired[str]
    riskType: NotRequired[RiskTypeType]
    executionStatus: NotRequired[TaskExecutionStatusType]
    taskHours: NotRequired[float]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ListPentestJobsForPentestInputTypeDef(TypedDict):
    pentestId: str
    agentSpaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PentestJobSummaryTypeDef(TypedDict):
    pentestJobId: str
    pentestId: str
    title: NotRequired[str]
    status: NotRequired[JobStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ListPentestsInputTypeDef(TypedDict):
    agentSpaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PentestSummaryTypeDef(TypedDict):
    pentestId: str
    agentSpaceId: str
    title: str
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ListPrivateConnectionsInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

PrivateConnectionSummaryTypeDef = TypedDict(
    "PrivateConnectionSummaryTypeDef",
    {
        "name": str,
        "type": PrivateConnectionTypeType,
        "status": PrivateConnectionStatusType,
        "resourceGatewayId": NotRequired[str],
        "hostAddress": NotRequired[str],
        "vpcId": NotRequired[str],
        "resourceConfigurationId": NotRequired[str],
        "certificateExpiryTime": NotRequired[datetime],
        "dnsResolution": NotRequired[ResourceConfigDnsResolutionType],
        "failureMessage": NotRequired[str],
        "tags": NotRequired[dict[str, str]],
    },
)

class ListSecurityRequirementPackFilterTypeDef(TypedDict):
    managementType: NotRequired[ManagementTypeType]
    status: NotRequired[SecurityRequirementPackStatusType]

class SecurityRequirementPackSummaryTypeDef(TypedDict):
    packId: str
    name: str
    managementType: ManagementTypeType
    status: SecurityRequirementPackStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    vendorName: NotRequired[str]

class ListSecurityRequirementsInputTypeDef(TypedDict):
    packId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class SecurityRequirementSummaryTypeDef(TypedDict):
    packId: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime

class ListTagsForResourceInputTypeDef(TypedDict):
    resourceArn: str

class ListTargetDomainsInputTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class TargetDomainSummaryTypeDef(TypedDict):
    targetDomainId: str
    domainName: str
    verificationStatus: NotRequired[TargetDomainStatusType]

class ListThreatModelJobTasksInputTypeDef(TypedDict):
    agentSpaceId: str
    threatModelJobId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ThreatModelJobTaskSummaryTypeDef(TypedDict):
    taskId: str
    threatModelId: NotRequired[str]
    threatModelJobId: NotRequired[str]
    agentSpaceId: NotRequired[str]
    title: NotRequired[str]
    executionStatus: NotRequired[TaskExecutionStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ListThreatModelJobsInputTypeDef(TypedDict):
    threatModelId: str
    agentSpaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ThreatModelJobSummaryTypeDef(TypedDict):
    threatModelJobId: str
    threatModelId: str
    agentSpaceId: NotRequired[str]
    title: NotRequired[str]
    status: NotRequired[JobStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ListThreatModelsInputTypeDef(TypedDict):
    agentSpaceId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ThreatModelSummaryTypeDef(TypedDict):
    threatModelId: str
    agentSpaceId: str
    title: str
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ListThreatsInputTypeDef(TypedDict):
    threatJobId: str
    agentSpaceId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ThreatSummaryTypeDef(TypedDict):
    threatId: NotRequired[str]
    threatJobId: NotRequired[str]
    title: NotRequired[str]
    statement: NotRequired[str]
    severity: NotRequired[ThreatSeverityType]
    status: NotRequired[ThreatStatusType]
    stride: NotRequired[list[StrideCategoryType]]
    createdBy: NotRequired[ThreatActorType]
    updatedBy: NotRequired[ThreatActorType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class UserMetadataTypeDef(TypedDict):
    username: str
    email: str

class UserConfigTypeDef(TypedDict):
    role: NotRequired[Literal["MEMBER"]]

class NetworkTrafficRuleTypeDef(TypedDict):
    effect: NotRequired[NetworkTrafficRuleEffectType]
    pattern: NotRequired[str]
    networkTrafficRuleType: NotRequired[Literal["URL"]]

class SelfManagedInputTypeDef(TypedDict):
    resourceConfigurationId: str
    certificate: NotRequired[str]

class ServiceManagedInputTypeDef(TypedDict):
    hostAddress: str
    vpcId: str
    subnetIds: Sequence[str]
    securityGroupIds: NotRequired[Sequence[str]]
    ipAddressType: NotRequired[IpAddressTypeType]
    ipv4AddressesPerEni: NotRequired[int]
    portRanges: NotRequired[Sequence[str]]
    certificate: NotRequired[str]
    dnsResolution: NotRequired[ResourceConfigDnsResolutionType]

class StartCodeRemediationInputTypeDef(TypedDict):
    agentSpaceId: str
    findingIds: Sequence[str]
    pentestJobId: NotRequired[str]
    codeReviewJobId: NotRequired[str]

class StartPentestJobInputTypeDef(TypedDict):
    agentSpaceId: str
    pentestId: str

class StartThreatModelJobInputTypeDef(TypedDict):
    agentSpaceId: str
    threatModelId: str

class StopCodeReviewJobInputTypeDef(TypedDict):
    agentSpaceId: str
    codeReviewJobId: str

class StopPentestJobInputTypeDef(TypedDict):
    agentSpaceId: str
    pentestJobId: str

class StopThreatModelJobInputTypeDef(TypedDict):
    agentSpaceId: str
    threatModelJobId: str

class TagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceInputTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateApplicationRequestTypeDef(TypedDict):
    applicationId: str
    roleArn: NotRequired[str]
    defaultKmsKeyId: NotRequired[str]

class UpdateFindingInputTypeDef(TypedDict):
    findingId: str
    agentSpaceId: str
    name: NotRequired[str]
    description: NotRequired[str]
    riskType: NotRequired[str]
    riskLevel: NotRequired[RiskLevelType]
    riskScore: NotRequired[str]
    attackScript: NotRequired[str]
    reasoning: NotRequired[str]
    status: NotRequired[FindingStatusType]
    customerNote: NotRequired[str]

class UpdatePrivateConnectionCertificateInputTypeDef(TypedDict):
    privateConnectionName: str
    certificate: str

class UpdateSecurityRequirementPackInputTypeDef(TypedDict):
    packId: str
    name: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[SecurityRequirementPackStatusType]

class UpdateTargetDomainInputTypeDef(TypedDict):
    targetDomainId: str
    verificationMethod: DomainVerificationMethodType

class VerificationScriptEnvVarTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]

class VerifyTargetDomainInputTypeDef(TypedDict):
    targetDomainId: str

class AWSResourcesOutputTypeDef(TypedDict):
    vpcs: NotRequired[list[VpcConfigOutputTypeDef]]
    logGroups: NotRequired[list[str]]
    s3Buckets: NotRequired[list[str]]
    secretArns: NotRequired[list[str]]
    lambdaFunctionArns: NotRequired[list[str]]
    iamRoles: NotRequired[list[str]]

class AWSResourcesTypeDef(TypedDict):
    vpcs: NotRequired[Sequence[VpcConfigTypeDef]]
    logGroups: NotRequired[Sequence[str]]
    s3Buckets: NotRequired[Sequence[str]]
    secretArns: NotRequired[Sequence[str]]
    lambdaFunctionArns: NotRequired[Sequence[str]]
    iamRoles: NotRequired[Sequence[str]]

VpcConfigUnionTypeDef = Union[VpcConfigTypeDef, VpcConfigOutputTypeDef]

class ActorOutputTypeDef(TypedDict):
    identifier: NotRequired[str]
    uris: NotRequired[list[str]]
    authentication: NotRequired[AuthenticationTypeDef]
    description: NotRequired[str]

class ActorTypeDef(TypedDict):
    identifier: NotRequired[str]
    uris: NotRequired[Sequence[str]]
    authentication: NotRequired[AuthenticationTypeDef]
    description: NotRequired[str]

class AddArtifactInputTypeDef(TypedDict):
    agentSpaceId: str
    artifactContent: BlobTypeDef
    artifactType: ArtifactTypeType
    fileName: str

SecurityRequirementArtifactTypeDef = TypedDict(
    "SecurityRequirementArtifactTypeDef",
    {
        "name": str,
        "format": SecurityRequirementArtifactFormatType,
        "content": BlobTypeDef,
    },
)

class AddArtifactOutputTypeDef(TypedDict):
    artifactId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApplicationResponseTypeDef(TypedDict):
    applicationId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateIntegrationOutputTypeDef(TypedDict):
    integrationId: str
    ResponseMetadata: ResponseMetadataTypeDef

CreatePrivateConnectionOutputTypeDef = TypedDict(
    "CreatePrivateConnectionOutputTypeDef",
    {
        "name": str,
        "type": PrivateConnectionTypeType,
        "status": PrivateConnectionStatusType,
        "resourceGatewayId": str,
        "hostAddress": str,
        "vpcId": str,
        "resourceConfigurationId": str,
        "certificateExpiryTime": datetime,
        "dnsResolution": ResourceConfigDnsResolutionType,
        "failureMessage": str,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class CreateSecurityRequirementPackOutputTypeDef(TypedDict):
    packId: str
    status: SecurityRequirementPackStatusType
    kmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAgentSpaceOutputTypeDef(TypedDict):
    agentSpaceId: str
    ResponseMetadata: ResponseMetadataTypeDef

DeletePrivateConnectionOutputTypeDef = TypedDict(
    "DeletePrivateConnectionOutputTypeDef",
    {
        "name": str,
        "type": PrivateConnectionTypeType,
        "status": PrivateConnectionStatusType,
        "resourceGatewayId": str,
        "hostAddress": str,
        "vpcId": str,
        "resourceConfigurationId": str,
        "certificateExpiryTime": datetime,
        "dnsResolution": ResourceConfigDnsResolutionType,
        "failureMessage": str,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class DeleteTargetDomainOutputTypeDef(TypedDict):
    targetDomainId: str
    ResponseMetadata: ResponseMetadataTypeDef

DescribePrivateConnectionOutputTypeDef = TypedDict(
    "DescribePrivateConnectionOutputTypeDef",
    {
        "name": str,
        "type": PrivateConnectionTypeType,
        "status": PrivateConnectionStatusType,
        "resourceGatewayId": str,
        "hostAddress": str,
        "vpcId": str,
        "resourceConfigurationId": str,
        "certificateExpiryTime": datetime,
        "dnsResolution": ResourceConfigDnsResolutionType,
        "failureMessage": str,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef

class GetIntegrationOutputTypeDef(TypedDict):
    integrationId: str
    installationId: str
    provider: ProviderType
    providerType: ProviderTypeType
    displayName: str
    kmsKeyId: str
    targetUrl: str
    privateConnectionName: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSecurityRequirementPackOutputTypeDef(TypedDict):
    packId: str
    name: str
    description: str
    vendorName: str
    managementType: ManagementTypeType
    status: SecurityRequirementPackStatusType
    importStatus: SecurityRequirementPackImportStatusType
    createdAt: datetime
    updatedAt: datetime
    kmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportSecurityRequirementsOutputTypeDef(TypedDict):
    packId: str
    importStatus: SecurityRequirementPackImportStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class InitiateProviderRegistrationOutputTypeDef(TypedDict):
    redirectTo: str
    csrfState: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class StartCodeReviewJobOutputTypeDef(TypedDict):
    title: str
    status: JobStatusType
    createdAt: datetime
    updatedAt: datetime
    codeReviewId: str
    codeReviewJobId: str
    agentSpaceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartPentestJobOutputTypeDef(TypedDict):
    title: str
    status: JobStatusType
    createdAt: datetime
    updatedAt: datetime
    pentestId: str
    pentestJobId: str
    agentSpaceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class StartThreatModelJobOutputTypeDef(TypedDict):
    title: str
    status: JobStatusType
    createdAt: datetime
    updatedAt: datetime
    threatModelId: str
    threatModelJobId: str
    agentSpaceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApplicationResponseTypeDef(TypedDict):
    applicationId: str
    ResponseMetadata: ResponseMetadataTypeDef

UpdatePrivateConnectionCertificateOutputTypeDef = TypedDict(
    "UpdatePrivateConnectionCertificateOutputTypeDef",
    {
        "name": str,
        "type": PrivateConnectionTypeType,
        "status": PrivateConnectionStatusType,
        "resourceGatewayId": str,
        "hostAddress": str,
        "vpcId": str,
        "resourceConfigurationId": str,
        "certificateExpiryTime": datetime,
        "dnsResolution": ResourceConfigDnsResolutionType,
        "failureMessage": str,
        "tags": dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class UpdateSecurityRequirementPackOutputTypeDef(TypedDict):
    packId: str
    name: str
    description: str
    status: SecurityRequirementPackStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class VerifyTargetDomainOutputTypeDef(TypedDict):
    targetDomainId: str
    domainName: str
    createdAt: datetime
    updatedAt: datetime
    verifiedAt: datetime
    status: TargetDomainStatusType
    verificationStatusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class ListAgentSpacesOutputTypeDef(TypedDict):
    agentSpaceSummaries: list[AgentSpaceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListApplicationsResponseTypeDef(TypedDict):
    applicationSummaries: list[ApplicationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchGetArtifactMetadataOutputTypeDef(TypedDict):
    artifactMetadataList: list[ArtifactMetadataItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ListArtifactsOutputTypeDef(TypedDict):
    artifactSummaries: list[ArtifactSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetArtifactOutputTypeDef(TypedDict):
    agentSpaceId: str
    artifactId: str
    artifact: ArtifactTypeDef
    fileName: str
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class BatchCreateSecurityRequirementsInputTypeDef(TypedDict):
    packId: str
    securityRequirements: Sequence[CreateSecurityRequirementEntryTypeDef]

class BatchCreateSecurityRequirementsOutputTypeDef(TypedDict):
    securityRequirements: list[BatchCreateSecurityRequirementResultTypeDef]
    errors: list[BatchSecurityRequirementErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteSecurityRequirementsOutputTypeDef(TypedDict):
    deletedSecurityRequirementNames: list[str]
    errors: list[BatchSecurityRequirementErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdateSecurityRequirementsOutputTypeDef(TypedDict):
    updatedSecurityRequirementNames: list[str]
    errors: list[BatchSecurityRequirementErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteCodeReviewsOutputTypeDef(TypedDict):
    deleted: list[str]
    failed: list[DeleteCodeReviewFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeleteThreatModelsOutputTypeDef(TypedDict):
    deleted: list[str]
    failed: list[DeleteThreatModelFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetSecurityRequirementsOutputTypeDef(TypedDict):
    securityRequirements: list[BatchGetSecurityRequirementResultTypeDef]
    errors: list[BatchSecurityRequirementErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchUpdateSecurityRequirementsInputTypeDef(TypedDict):
    packId: str
    securityRequirements: Sequence[UpdateSecurityRequirementEntryTypeDef]

class LogLocationTypeDef(TypedDict):
    logType: NotRequired[Literal["CLOUDWATCH"]]
    cloudWatchLog: NotRequired[CloudWatchLogTypeDef]

class CodeRemediationTaskTypeDef(TypedDict):
    status: CodeRemediationTaskStatusType
    statusReason: NotRequired[str]
    taskDetails: NotRequired[list[CodeRemediationTaskDetailsTypeDef]]

class ListCodeReviewJobsForCodeReviewOutputTypeDef(TypedDict):
    codeReviewJobSummaries: list[CodeReviewJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCodeReviewJobTasksOutputTypeDef(TypedDict):
    codeReviewJobTaskSummaries: list[CodeReviewJobTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCodeReviewsOutputTypeDef(TypedDict):
    codeReviewSummaries: list[CodeReviewSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CreateThreatInputTypeDef(TypedDict):
    agentSpaceId: str
    threatJobId: str
    title: NotRequired[str]
    statement: NotRequired[str]
    severity: NotRequired[ThreatSeverityType]
    comments: NotRequired[str]
    stride: NotRequired[Sequence[StrideCategoryType]]
    threatSource: NotRequired[str]
    prerequisites: NotRequired[str]
    threatAction: NotRequired[str]
    threatImpact: NotRequired[str]
    impactedGoal: NotRequired[Sequence[str]]
    impactedAssets: NotRequired[Sequence[str]]
    anchor: NotRequired[ThreatAnchorShapeTypeDef]
    evidence: NotRequired[Sequence[ThreatEvidenceShapeTypeDef]]
    recommendation: NotRequired[str]

class CreateThreatOutputTypeDef(TypedDict):
    threatId: str
    threatJobId: str
    title: str
    statement: str
    severity: ThreatSeverityType
    status: ThreatStatusType
    comments: str
    stride: list[StrideCategoryType]
    threatSource: str
    prerequisites: str
    threatAction: str
    threatImpact: str
    impactedGoal: list[str]
    impactedAssets: list[str]
    anchor: ThreatAnchorShapeTypeDef
    evidence: list[ThreatEvidenceShapeTypeDef]
    recommendation: str
    createdBy: ThreatActorType
    updatedBy: ThreatActorType
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ThreatTypeDef(TypedDict):
    threatId: NotRequired[str]
    threatJobId: NotRequired[str]
    title: NotRequired[str]
    statement: NotRequired[str]
    severity: NotRequired[ThreatSeverityType]
    status: NotRequired[ThreatStatusType]
    comments: NotRequired[str]
    threatSource: NotRequired[str]
    prerequisites: NotRequired[str]
    threatAction: NotRequired[str]
    threatImpact: NotRequired[str]
    impactedGoal: NotRequired[list[str]]
    impactedAssets: NotRequired[list[str]]
    anchor: NotRequired[ThreatAnchorShapeTypeDef]
    evidence: NotRequired[list[ThreatEvidenceShapeTypeDef]]
    stride: NotRequired[list[StrideCategoryType]]
    recommendation: NotRequired[str]
    createdBy: NotRequired[ThreatActorType]
    updatedBy: NotRequired[ThreatActorType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class UpdateThreatInputTypeDef(TypedDict):
    threatId: str
    agentSpaceId: str
    title: NotRequired[str]
    status: NotRequired[ThreatStatusType]
    comments: NotRequired[str]
    statement: NotRequired[str]
    severity: NotRequired[ThreatSeverityType]
    threatSource: NotRequired[str]
    prerequisites: NotRequired[str]
    threatAction: NotRequired[str]
    threatImpact: NotRequired[str]
    impactedGoal: NotRequired[Sequence[str]]
    impactedAssets: NotRequired[Sequence[str]]
    anchor: NotRequired[ThreatAnchorShapeTypeDef]
    evidence: NotRequired[Sequence[ThreatEvidenceShapeTypeDef]]
    recommendation: NotRequired[str]

class UpdateThreatOutputTypeDef(TypedDict):
    threatId: str
    threatJobId: str
    title: str
    statement: str
    severity: ThreatSeverityType
    status: ThreatStatusType
    comments: str
    stride: list[StrideCategoryType]
    threatSource: str
    prerequisites: str
    threatAction: str
    threatImpact: str
    impactedGoal: list[str]
    impactedAssets: list[str]
    anchor: ThreatAnchorShapeTypeDef
    evidence: list[ThreatEvidenceShapeTypeDef]
    recommendation: str
    createdBy: ThreatActorType
    updatedBy: ThreatActorType
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StartCodeReviewJobInputTypeDef(TypedDict):
    agentSpaceId: str
    codeReviewId: str
    diffSource: NotRequired[DiffSourceTypeDef]

class ListDiscoveredEndpointsOutputTypeDef(TypedDict):
    discoveredEndpoints: list[DiscoveredEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class DocumentInfoTypeDef(TypedDict):
    s3Location: NotRequired[str]
    artifactId: NotRequired[str]
    integratedDocument: NotRequired[IntegratedDocumentTypeDef]

class ListFindingsOutputTypeDef(TypedDict):
    findingsSummaries: list[FindingSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetApplicationResponseTypeDef(TypedDict):
    applicationId: str
    domain: str
    applicationName: str
    idcConfiguration: IdCConfigurationTypeDef
    roleArn: str
    defaultKmsKeyId: str
    ResponseMetadata: ResponseMetadataTypeDef

class ProviderInputTypeDef(TypedDict):
    github: NotRequired[GitHubIntegrationInputTypeDef]
    gitlab: NotRequired[GitLabIntegrationInputTypeDef]
    bitbucket: NotRequired[BitbucketIntegrationInputTypeDef]
    confluence: NotRequired[ConfluenceIntegrationInputTypeDef]

class IntegratedResourceMetadataTypeDef(TypedDict):
    githubRepository: NotRequired[GitHubRepositoryMetadataTypeDef]
    gitlabRepository: NotRequired[GitLabRepositoryMetadataTypeDef]
    bitbucketRepository: NotRequired[BitbucketRepositoryMetadataTypeDef]
    confluenceDocument: NotRequired[ConfluenceDocumentMetadataTypeDef]

class IntegratedResourceTypeDef(TypedDict):
    githubRepository: NotRequired[GitHubRepositoryResourceTypeDef]
    gitlabRepository: NotRequired[GitLabRepositoryResourceTypeDef]
    bitbucketRepository: NotRequired[BitbucketRepositoryResourceTypeDef]
    confluenceDocument: NotRequired[ConfluenceDocumentResourceTypeDef]

class ProviderResourceCapabilitiesTypeDef(TypedDict):
    github: NotRequired[GitHubResourceCapabilitiesTypeDef]
    gitlab: NotRequired[GitLabResourceCapabilitiesTypeDef]
    bitbucket: NotRequired[BitbucketResourceCapabilitiesTypeDef]
    confluence: NotRequired[ConfluenceResourceCapabilitiesTypeDef]

class VerificationDetailsTypeDef(TypedDict):
    method: NotRequired[DomainVerificationMethodType]
    dnsTxt: NotRequired[DnsVerificationTypeDef]
    httpRoute: NotRequired[HttpVerificationTypeDef]

ListIntegrationsInputTypeDef = TypedDict(
    "ListIntegrationsInputTypeDef",
    {
        "filter": NotRequired[IntegrationFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class ListIntegrationsOutputTypeDef(TypedDict):
    integrationSummaries: list[IntegrationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAgentSpacesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApplicationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListArtifactsInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCodeReviewJobTasksInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    codeReviewJobId: NotRequired[str]
    stepName: NotRequired[StepNameType]
    categoryName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCodeReviewJobsForCodeReviewInputPaginateTypeDef(TypedDict):
    codeReviewId: str
    agentSpaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListCodeReviewsInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListDiscoveredEndpointsInputPaginateTypeDef(TypedDict):
    pentestJobId: str
    agentSpaceId: str
    prefix: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListFindingsInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    pentestJobId: NotRequired[str]
    codeReviewJobId: NotRequired[str]
    riskType: NotRequired[str]
    riskLevel: NotRequired[RiskLevelType]
    status: NotRequired[FindingStatusType]
    confidence: NotRequired[ConfidenceLevelType]
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListIntegratedResourcesInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    integrationId: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListIntegrationsInputPaginateTypeDef = TypedDict(
    "ListIntegrationsInputPaginateTypeDef",
    {
        "filter": NotRequired[IntegrationFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListMembershipsRequestPaginateTypeDef(TypedDict):
    applicationId: str
    agentSpaceId: str
    memberType: NotRequired[MembershipTypeFilterType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPentestJobTasksInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    pentestJobId: NotRequired[str]
    stepName: NotRequired[StepNameType]
    categoryName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPentestJobsForPentestInputPaginateTypeDef(TypedDict):
    pentestId: str
    agentSpaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPentestsInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPrivateConnectionsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListSecurityRequirementsInputPaginateTypeDef(TypedDict):
    packId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTargetDomainsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListThreatModelJobTasksInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    threatModelJobId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListThreatModelJobsInputPaginateTypeDef(TypedDict):
    threatModelId: str
    agentSpaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListThreatModelsInputPaginateTypeDef(TypedDict):
    agentSpaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListThreatsInputPaginateTypeDef(TypedDict):
    threatJobId: str
    agentSpaceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPentestJobTasksOutputTypeDef(TypedDict):
    taskSummaries: list[TaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPentestJobsForPentestOutputTypeDef(TypedDict):
    pentestJobSummaries: list[PentestJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPentestsOutputTypeDef(TypedDict):
    pentestSummaries: list[PentestSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPrivateConnectionsOutputTypeDef(TypedDict):
    privateConnections: list[PrivateConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ListSecurityRequirementPacksInputPaginateTypeDef = TypedDict(
    "ListSecurityRequirementPacksInputPaginateTypeDef",
    {
        "filter": NotRequired[ListSecurityRequirementPackFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListSecurityRequirementPacksInputTypeDef = TypedDict(
    "ListSecurityRequirementPacksInputTypeDef",
    {
        "filter": NotRequired[ListSecurityRequirementPackFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

class ListSecurityRequirementPacksOutputTypeDef(TypedDict):
    securityRequirementPackSummaries: list[SecurityRequirementPackSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListSecurityRequirementsOutputTypeDef(TypedDict):
    securityRequirementSummaries: list[SecurityRequirementSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTargetDomainsOutputTypeDef(TypedDict):
    targetDomainSummaries: list[TargetDomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListThreatModelJobTasksOutputTypeDef(TypedDict):
    threatModelJobTaskSummaries: list[ThreatModelJobTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListThreatModelJobsOutputTypeDef(TypedDict):
    threatModelJobSummaries: list[ThreatModelJobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListThreatModelsOutputTypeDef(TypedDict):
    threatModelSummaries: list[ThreatModelSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListThreatsOutputTypeDef(TypedDict):
    threats: list[ThreatSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class MemberMetadataTypeDef(TypedDict):
    user: NotRequired[UserMetadataTypeDef]

class MembershipConfigTypeDef(TypedDict):
    user: NotRequired[UserConfigTypeDef]

class NetworkTrafficConfigOutputTypeDef(TypedDict):
    rules: NotRequired[list[NetworkTrafficRuleTypeDef]]
    customHeaders: NotRequired[list[CustomHeaderTypeDef]]

class NetworkTrafficConfigTypeDef(TypedDict):
    rules: NotRequired[Sequence[NetworkTrafficRuleTypeDef]]
    customHeaders: NotRequired[Sequence[CustomHeaderTypeDef]]

class PrivateConnectionModeTypeDef(TypedDict):
    serviceManaged: NotRequired[ServiceManagedInputTypeDef]
    selfManaged: NotRequired[SelfManagedInputTypeDef]

class VerificationScriptTypeDef(TypedDict):
    scriptType: NotRequired[str]
    scriptUrl: NotRequired[str]
    instructions: NotRequired[str]
    envVars: NotRequired[list[VerificationScriptEnvVarTypeDef]]

class AgentSpaceTypeDef(TypedDict):
    agentSpaceId: str
    name: str
    description: NotRequired[str]
    awsResources: NotRequired[AWSResourcesOutputTypeDef]
    targetDomainIds: NotRequired[list[str]]
    codeReviewSettings: NotRequired[CodeReviewSettingsTypeDef]
    kmsKeyId: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class CreateAgentSpaceOutputTypeDef(TypedDict):
    agentSpaceId: str
    name: str
    description: str
    awsResources: AWSResourcesOutputTypeDef
    targetDomainIds: list[str]
    codeReviewSettings: CodeReviewSettingsTypeDef
    kmsKeyId: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAgentSpaceOutputTypeDef(TypedDict):
    agentSpaceId: str
    name: str
    description: str
    awsResources: AWSResourcesOutputTypeDef
    targetDomainIds: list[str]
    codeReviewSettings: CodeReviewSettingsTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

AWSResourcesUnionTypeDef = Union[AWSResourcesTypeDef, AWSResourcesOutputTypeDef]

class ImportSourceTypeDef(TypedDict):
    documents: NotRequired[Sequence[SecurityRequirementArtifactTypeDef]]

class CodeReviewJobTaskTypeDef(TypedDict):
    taskId: str
    codeReviewId: NotRequired[str]
    codeReviewJobId: NotRequired[str]
    agentSpaceId: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    categories: NotRequired[list[CategoryTypeDef]]
    riskType: NotRequired[RiskTypeType]
    executionStatus: NotRequired[TaskExecutionStatusType]
    logsLocation: NotRequired[LogLocationTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class TaskTypeDef(TypedDict):
    taskId: str
    pentestId: NotRequired[str]
    pentestJobId: NotRequired[str]
    agentSpaceId: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    categories: NotRequired[list[CategoryTypeDef]]
    riskType: NotRequired[RiskTypeType]
    targetEndpoint: NotRequired[EndpointTypeDef]
    executionStatus: NotRequired[TaskExecutionStatusType]
    logsLocation: NotRequired[LogLocationTypeDef]
    taskHours: NotRequired[float]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ThreatModelJobTaskTypeDef(TypedDict):
    taskId: str
    threatModelId: NotRequired[str]
    threatModelJobId: NotRequired[str]
    agentSpaceId: NotRequired[str]
    title: NotRequired[str]
    description: NotRequired[str]
    executionStatus: NotRequired[TaskExecutionStatusType]
    logsLocation: NotRequired[LogLocationTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class BatchGetThreatsOutputTypeDef(TypedDict):
    threats: list[ThreatTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class AssetsOutputTypeDef(TypedDict):
    endpoints: NotRequired[list[EndpointTypeDef]]
    actors: NotRequired[list[ActorOutputTypeDef]]
    documents: NotRequired[list[DocumentInfoTypeDef]]
    sourceCode: NotRequired[list[SourceCodeRepositoryTypeDef]]
    integratedRepositories: NotRequired[list[IntegratedRepositoryTypeDef]]

class AssetsTypeDef(TypedDict):
    endpoints: NotRequired[Sequence[EndpointTypeDef]]
    actors: NotRequired[Sequence[ActorTypeDef]]
    documents: NotRequired[Sequence[DocumentInfoTypeDef]]
    sourceCode: NotRequired[Sequence[SourceCodeRepositoryTypeDef]]
    integratedRepositories: NotRequired[Sequence[IntegratedRepositoryTypeDef]]

class CodeReviewJobTypeDef(TypedDict):
    codeReviewJobId: NotRequired[str]
    codeReviewId: NotRequired[str]
    title: NotRequired[str]
    overview: NotRequired[str]
    status: NotRequired[JobStatusType]
    documents: NotRequired[list[DocumentInfoTypeDef]]
    sourceCode: NotRequired[list[SourceCodeRepositoryTypeDef]]
    steps: NotRequired[list[StepTypeDef]]
    executionContext: NotRequired[list[ExecutionContextTypeDef]]
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    errorInformation: NotRequired[ErrorInformationTypeDef]
    integratedRepositories: NotRequired[list[IntegratedRepositoryTypeDef]]
    codeRemediationStrategy: NotRequired[CodeRemediationStrategyType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ThreatModelJobTypeDef(TypedDict):
    threatModelJobId: NotRequired[str]
    threatModelId: NotRequired[str]
    agentSpaceId: NotRequired[str]
    title: NotRequired[str]
    status: NotRequired[JobStatusType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    executionStartTime: NotRequired[datetime]
    executionEndTime: NotRequired[datetime]
    sourceCode: NotRequired[list[SourceCodeRepositoryTypeDef]]
    integratedRepositories: NotRequired[list[IntegratedRepositoryTypeDef]]
    documents: NotRequired[list[DocumentInfoTypeDef]]
    scopeDocs: NotRequired[list[DocumentInfoTypeDef]]
    errorInformation: NotRequired[ErrorInformationTypeDef]
    systemOverview: NotRequired[str]

CreateIntegrationInputTypeDef = TypedDict(
    "CreateIntegrationInputTypeDef",
    {
        "provider": ProviderType,
        "input": ProviderInputTypeDef,
        "integrationDisplayName": str,
        "kmsKeyId": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "privateConnectionName": NotRequired[str],
    },
)

class IntegratedResourceInputItemTypeDef(TypedDict):
    resource: IntegratedResourceTypeDef
    capabilities: NotRequired[ProviderResourceCapabilitiesTypeDef]

class IntegratedResourceSummaryTypeDef(TypedDict):
    integrationId: str
    resource: IntegratedResourceMetadataTypeDef
    capabilities: NotRequired[ProviderResourceCapabilitiesTypeDef]

class CreateTargetDomainOutputTypeDef(TypedDict):
    targetDomainId: str
    domainName: str
    verificationStatus: TargetDomainStatusType
    verificationStatusReason: str
    verificationDetails: VerificationDetailsTypeDef
    createdAt: datetime
    verifiedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class TargetDomainTypeDef(TypedDict):
    targetDomainId: str
    domainName: str
    verificationStatus: NotRequired[TargetDomainStatusType]
    verificationStatusReason: NotRequired[str]
    verificationDetails: NotRequired[VerificationDetailsTypeDef]
    createdAt: NotRequired[datetime]
    verifiedAt: NotRequired[datetime]

class UpdateTargetDomainOutputTypeDef(TypedDict):
    targetDomainId: str
    domainName: str
    verificationStatus: TargetDomainStatusType
    verificationStatusReason: str
    verificationDetails: VerificationDetailsTypeDef
    createdAt: datetime
    verifiedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateMembershipRequestTypeDef(TypedDict):
    applicationId: str
    agentSpaceId: str
    membershipId: str
    memberType: Literal["USER"]
    config: NotRequired[MembershipConfigTypeDef]

class MembershipSummaryTypeDef(TypedDict):
    membershipId: str
    applicationId: str
    agentSpaceId: str
    memberType: Literal["USER"]
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    updatedBy: str
    config: NotRequired[MembershipConfigTypeDef]
    metadata: NotRequired[MemberMetadataTypeDef]

class PentestJobTypeDef(TypedDict):
    pentestJobId: NotRequired[str]
    pentestId: NotRequired[str]
    title: NotRequired[str]
    overview: NotRequired[str]
    status: NotRequired[JobStatusType]
    endpoints: NotRequired[list[EndpointTypeDef]]
    actors: NotRequired[list[ActorOutputTypeDef]]
    documents: NotRequired[list[DocumentInfoTypeDef]]
    sourceCode: NotRequired[list[SourceCodeRepositoryTypeDef]]
    excludePaths: NotRequired[list[EndpointTypeDef]]
    allowedDomains: NotRequired[list[EndpointTypeDef]]
    excludeRiskTypes: NotRequired[list[RiskTypeType]]
    steps: NotRequired[list[StepTypeDef]]
    executionContext: NotRequired[list[ExecutionContextTypeDef]]
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    vpcConfig: NotRequired[VpcConfigOutputTypeDef]
    networkTrafficConfig: NotRequired[NetworkTrafficConfigOutputTypeDef]
    errorInformation: NotRequired[ErrorInformationTypeDef]
    integratedRepositories: NotRequired[list[IntegratedRepositoryTypeDef]]
    codeRemediationStrategy: NotRequired[CodeRemediationStrategyType]
    cleanUpStrategy: NotRequired[CleanUpStrategyType]
    disableManagedSkills: NotRequired[list[SkillTypeType]]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

NetworkTrafficConfigUnionTypeDef = Union[
    NetworkTrafficConfigTypeDef, NetworkTrafficConfigOutputTypeDef
]

class CreatePrivateConnectionInputTypeDef(TypedDict):
    privateConnectionName: str
    mode: PrivateConnectionModeTypeDef
    tags: NotRequired[Mapping[str, str]]

class FindingTypeDef(TypedDict):
    findingId: str
    agentSpaceId: str
    pentestId: NotRequired[str]
    pentestJobId: NotRequired[str]
    codeReviewId: NotRequired[str]
    codeReviewJobId: NotRequired[str]
    taskId: NotRequired[str]
    name: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[FindingStatusType]
    riskType: NotRequired[str]
    riskLevel: NotRequired[RiskLevelType]
    riskScore: NotRequired[str]
    reasoning: NotRequired[str]
    confidence: NotRequired[ConfidenceLevelType]
    validationStatus: NotRequired[ValidationStatusType]
    attackScript: NotRequired[str]
    codeRemediationTask: NotRequired[CodeRemediationTaskTypeDef]
    lastUpdatedBy: NotRequired[str]
    customerNote: NotRequired[str]
    codeLocations: NotRequired[list[CodeLocationTypeDef]]
    verificationScript: NotRequired[VerificationScriptTypeDef]
    alignmentRationale: NotRequired[str]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class BatchGetAgentSpacesOutputTypeDef(TypedDict):
    agentSpaces: list[AgentSpaceTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAgentSpaceInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    awsResources: NotRequired[AWSResourcesUnionTypeDef]
    targetDomainIds: NotRequired[Sequence[str]]
    codeReviewSettings: NotRequired[CodeReviewSettingsTypeDef]
    kmsKeyId: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateAgentSpaceInputTypeDef(TypedDict):
    agentSpaceId: str
    name: NotRequired[str]
    description: NotRequired[str]
    awsResources: NotRequired[AWSResourcesUnionTypeDef]
    targetDomainIds: NotRequired[Sequence[str]]
    codeReviewSettings: NotRequired[CodeReviewSettingsTypeDef]

ImportSecurityRequirementsInputTypeDef = TypedDict(
    "ImportSecurityRequirementsInputTypeDef",
    {
        "packId": str,
        "input": ImportSourceTypeDef,
    },
)

class BatchGetCodeReviewJobTasksOutputTypeDef(TypedDict):
    codeReviewJobTasks: list[CodeReviewJobTaskTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetPentestJobTasksOutputTypeDef(TypedDict):
    tasks: list[TaskTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetThreatModelJobTasksOutputTypeDef(TypedDict):
    threatModelJobTasks: list[ThreatModelJobTaskTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CodeReviewTypeDef(TypedDict):
    codeReviewId: str
    agentSpaceId: str
    title: str
    assets: AssetsOutputTypeDef
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    codeRemediationStrategy: NotRequired[CodeRemediationStrategyType]
    validationMode: NotRequired[ValidationModeType]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class CreateCodeReviewOutputTypeDef(TypedDict):
    codeReviewId: str
    title: str
    createdAt: datetime
    updatedAt: datetime
    assets: AssetsOutputTypeDef
    serviceRole: str
    logConfig: CloudWatchLogTypeDef
    agentSpaceId: str
    codeRemediationStrategy: CodeRemediationStrategyType
    validationMode: ValidationModeType
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePentestOutputTypeDef(TypedDict):
    pentestId: str
    title: str
    createdAt: datetime
    updatedAt: datetime
    assets: AssetsOutputTypeDef
    excludeRiskTypes: list[RiskTypeType]
    serviceRole: str
    logConfig: CloudWatchLogTypeDef
    agentSpaceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateThreatModelOutputTypeDef(TypedDict):
    threatModelId: str
    title: str
    agentSpaceId: str
    description: str
    assets: AssetsOutputTypeDef
    scopeDocs: list[DocumentInfoTypeDef]
    serviceRole: str
    logConfig: CloudWatchLogTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class PentestTypeDef(TypedDict):
    pentestId: str
    agentSpaceId: str
    title: str
    assets: AssetsOutputTypeDef
    excludeRiskTypes: NotRequired[list[RiskTypeType]]
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    vpcConfig: NotRequired[VpcConfigOutputTypeDef]
    networkTrafficConfig: NotRequired[NetworkTrafficConfigOutputTypeDef]
    codeRemediationStrategy: NotRequired[CodeRemediationStrategyType]
    cleanUpStrategy: NotRequired[CleanUpStrategyType]
    disableManagedSkills: NotRequired[list[SkillTypeType]]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class ThreatModelTypeDef(TypedDict):
    threatModelId: str
    agentSpaceId: str
    title: str
    assets: AssetsOutputTypeDef
    description: NotRequired[str]
    scopeDocs: NotRequired[list[DocumentInfoTypeDef]]
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]

class UpdateCodeReviewOutputTypeDef(TypedDict):
    codeReviewId: str
    title: str
    createdAt: datetime
    updatedAt: datetime
    assets: AssetsOutputTypeDef
    serviceRole: str
    logConfig: CloudWatchLogTypeDef
    agentSpaceId: str
    codeRemediationStrategy: CodeRemediationStrategyType
    validationMode: ValidationModeType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePentestOutputTypeDef(TypedDict):
    pentestId: str
    title: str
    createdAt: datetime
    updatedAt: datetime
    assets: AssetsOutputTypeDef
    excludeRiskTypes: list[RiskTypeType]
    serviceRole: str
    logConfig: CloudWatchLogTypeDef
    agentSpaceId: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateThreatModelOutputTypeDef(TypedDict):
    threatModelId: str
    title: str
    agentSpaceId: str
    description: str
    assets: AssetsOutputTypeDef
    scopeDocs: list[DocumentInfoTypeDef]
    serviceRole: str
    logConfig: CloudWatchLogTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

AssetsUnionTypeDef = Union[AssetsTypeDef, AssetsOutputTypeDef]

class BatchGetCodeReviewJobsOutputTypeDef(TypedDict):
    codeReviewJobs: list[CodeReviewJobTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetThreatModelJobsOutputTypeDef(TypedDict):
    threatModelJobs: list[ThreatModelJobTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateIntegratedResourcesInputTypeDef(TypedDict):
    agentSpaceId: str
    integrationId: str
    items: Sequence[IntegratedResourceInputItemTypeDef]

class ListIntegratedResourcesOutputTypeDef(TypedDict):
    integratedResourceSummaries: list[IntegratedResourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchGetTargetDomainsOutputTypeDef(TypedDict):
    targetDomains: list[TargetDomainTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class ListMembershipsResponseTypeDef(TypedDict):
    membershipSummaries: list[MembershipSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class BatchGetPentestJobsOutputTypeDef(TypedDict):
    pentestJobs: list[PentestJobTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetFindingsOutputTypeDef(TypedDict):
    findings: list[FindingTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetCodeReviewsOutputTypeDef(TypedDict):
    codeReviews: list[CodeReviewTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchDeletePentestsOutputTypeDef(TypedDict):
    deleted: list[PentestTypeDef]
    failed: list[DeletePentestFailureTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetPentestsOutputTypeDef(TypedDict):
    pentests: list[PentestTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class BatchGetThreatModelsOutputTypeDef(TypedDict):
    threatModels: list[ThreatModelTypeDef]
    notFound: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCodeReviewInputTypeDef(TypedDict):
    title: str
    agentSpaceId: str
    assets: AssetsUnionTypeDef
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    codeRemediationStrategy: NotRequired[CodeRemediationStrategyType]
    validationMode: NotRequired[ValidationModeType]

class CreatePentestInputTypeDef(TypedDict):
    title: str
    agentSpaceId: str
    assets: NotRequired[AssetsUnionTypeDef]
    excludeRiskTypes: NotRequired[Sequence[RiskTypeType]]
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    vpcConfig: NotRequired[VpcConfigUnionTypeDef]
    networkTrafficConfig: NotRequired[NetworkTrafficConfigUnionTypeDef]
    codeRemediationStrategy: NotRequired[CodeRemediationStrategyType]
    disableManagedSkills: NotRequired[Sequence[SkillTypeType]]

class CreateThreatModelInputTypeDef(TypedDict):
    title: str
    agentSpaceId: str
    serviceRole: str
    description: NotRequired[str]
    assets: NotRequired[AssetsUnionTypeDef]
    scopeDocs: NotRequired[Sequence[DocumentInfoTypeDef]]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    reportDestination: NotRequired[ReportDestinationTypeDef]

class UpdateCodeReviewInputTypeDef(TypedDict):
    codeReviewId: str
    agentSpaceId: str
    title: NotRequired[str]
    assets: NotRequired[AssetsUnionTypeDef]
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    codeRemediationStrategy: NotRequired[CodeRemediationStrategyType]
    validationMode: NotRequired[ValidationModeType]

class UpdatePentestInputTypeDef(TypedDict):
    pentestId: str
    agentSpaceId: str
    title: NotRequired[str]
    assets: NotRequired[AssetsUnionTypeDef]
    excludeRiskTypes: NotRequired[Sequence[RiskTypeType]]
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
    vpcConfig: NotRequired[VpcConfigUnionTypeDef]
    networkTrafficConfig: NotRequired[NetworkTrafficConfigUnionTypeDef]
    codeRemediationStrategy: NotRequired[CodeRemediationStrategyType]
    disableManagedSkills: NotRequired[Sequence[SkillTypeType]]

class UpdateThreatModelInputTypeDef(TypedDict):
    threatModelId: str
    agentSpaceId: str
    title: NotRequired[str]
    description: NotRequired[str]
    assets: NotRequired[AssetsUnionTypeDef]
    scopeDocs: NotRequired[Sequence[DocumentInfoTypeDef]]
    serviceRole: NotRequired[str]
    logConfig: NotRequired[CloudWatchLogTypeDef]
