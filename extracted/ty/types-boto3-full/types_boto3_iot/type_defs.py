"""
Type annotations for iot service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_iot.type_defs import AbortCriteriaTypeDef

    data: AbortCriteriaTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    ActionTypeType,
    AggregationTypeNameType,
    ApplicationProtocolType,
    AuditCheckRunStatusType,
    AuditFindingSeverityType,
    AuditFrequencyType,
    AuditMitigationActionsExecutionStatusType,
    AuditMitigationActionsTaskStatusType,
    AuditTaskStatusType,
    AuditTaskTypeType,
    AuthDecisionType,
    AuthenticationTypeType,
    AuthorizerStatusType,
    AutoRegistrationStatusType,
    AwsJobAbortCriteriaFailureTypeType,
    BehaviorCriteriaTypeType,
    CACertificateStatusType,
    CannedAccessControlListType,
    CertificateModeType,
    CertificateStatusType,
    CommandExecutionStatusType,
    CommandNamespaceType,
    ComparisonOperatorType,
    ConfidenceLevelType,
    ConfigNameType,
    CustomMetricTypeType,
    DayOfWeekType,
    DetectMitigationActionExecutionStatusType,
    DetectMitigationActionsTaskStatusType,
    DeviceDefenderIndexingModeType,
    DimensionValueOperatorType,
    DisconnectReasonValueType,
    DomainConfigurationStatusType,
    DomainTypeType,
    DynamicGroupStatusType,
    DynamoKeyTypeType,
    EventTypeType,
    FieldTypeType,
    FleetMetricUnitType,
    IndexStatusType,
    JobEndBehaviorType,
    JobExecutionFailureTypeType,
    JobExecutionStatusType,
    JobStatusType,
    LogLevelType,
    LogTargetTypeType,
    MessageFormatType,
    MitigationActionTypeType,
    ModelStatusType,
    NamedShadowIndexingModeType,
    OTAUpdateStatusType,
    PackageVersionActionType,
    PackageVersionStatusType,
    ProtocolType,
    ReportTypeType,
    ResourceTypeType,
    RetryableFailureTypeType,
    SbomValidationErrorCodeType,
    SbomValidationResultType,
    SbomValidationStatusType,
    ServerCertificateStatusType,
    ServiceTypeType,
    SortOrderType,
    StatusType,
    TargetFieldOrderType,
    TargetSelectionType,
    TemplateTypeType,
    ThingConnectivityIndexingModeType,
    ThingGroupIndexingModeType,
    ThingIndexingModeType,
    ThingPrincipalTypeType,
    TopicRuleDestinationStatusType,
    VerificationStateType,
    ViolationEventTypeType,
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
    "AbortConfigOutputTypeDef",
    "AbortConfigTypeDef",
    "AbortConfigUnionTypeDef",
    "AbortCriteriaTypeDef",
    "AcceptCertificateTransferRequestTypeDef",
    "ActionOutputTypeDef",
    "ActionTypeDef",
    "ActionUnionTypeDef",
    "ActiveViolationTypeDef",
    "AddThingToBillingGroupRequestTypeDef",
    "AddThingToThingGroupRequestTypeDef",
    "AddThingsToThingGroupParamsOutputTypeDef",
    "AddThingsToThingGroupParamsTypeDef",
    "AggregationTypeOutputTypeDef",
    "AggregationTypeTypeDef",
    "AggregationTypeUnionTypeDef",
    "AlertTargetTypeDef",
    "AllowedTypeDef",
    "AssetPropertyTimestampTypeDef",
    "AssetPropertyValueTypeDef",
    "AssetPropertyVariantTypeDef",
    "AssociateSbomWithPackageVersionRequestTypeDef",
    "AssociateSbomWithPackageVersionResponseTypeDef",
    "AssociateTargetsWithJobRequestTypeDef",
    "AssociateTargetsWithJobResponseTypeDef",
    "AttachPolicyRequestTypeDef",
    "AttachPrincipalPolicyRequestTypeDef",
    "AttachSecurityProfileRequestTypeDef",
    "AttachThingPrincipalRequestTypeDef",
    "AttributePayloadOutputTypeDef",
    "AttributePayloadTypeDef",
    "AttributePayloadUnionTypeDef",
    "AuditCheckConfigurationOutputTypeDef",
    "AuditCheckConfigurationTypeDef",
    "AuditCheckConfigurationUnionTypeDef",
    "AuditCheckDetailsTypeDef",
    "AuditFindingTypeDef",
    "AuditMitigationActionExecutionMetadataTypeDef",
    "AuditMitigationActionsTaskMetadataTypeDef",
    "AuditMitigationActionsTaskTargetOutputTypeDef",
    "AuditMitigationActionsTaskTargetTypeDef",
    "AuditMitigationActionsTaskTargetUnionTypeDef",
    "AuditNotificationTargetTypeDef",
    "AuditSuppressionTypeDef",
    "AuditTaskMetadataTypeDef",
    "AuthInfoOutputTypeDef",
    "AuthInfoTypeDef",
    "AuthInfoUnionTypeDef",
    "AuthResultTypeDef",
    "AuthorizerConfigTypeDef",
    "AuthorizerDescriptionTypeDef",
    "AuthorizerSummaryTypeDef",
    "AwsJobAbortConfigTypeDef",
    "AwsJobAbortCriteriaTypeDef",
    "AwsJobExecutionsRolloutConfigTypeDef",
    "AwsJobExponentialRolloutRateTypeDef",
    "AwsJobPresignedUrlConfigTypeDef",
    "AwsJobRateIncreaseCriteriaTypeDef",
    "AwsJobTimeoutConfigTypeDef",
    "BehaviorCriteriaOutputTypeDef",
    "BehaviorCriteriaTypeDef",
    "BehaviorCriteriaUnionTypeDef",
    "BehaviorModelTrainingSummaryTypeDef",
    "BehaviorOutputTypeDef",
    "BehaviorTypeDef",
    "BehaviorUnionTypeDef",
    "BillingGroupMetadataTypeDef",
    "BillingGroupPropertiesTypeDef",
    "BlobTypeDef",
    "BucketTypeDef",
    "BucketsAggregationTypeTypeDef",
    "CACertificateDescriptionTypeDef",
    "CACertificateTypeDef",
    "CancelAuditMitigationActionsTaskRequestTypeDef",
    "CancelAuditTaskRequestTypeDef",
    "CancelCertificateTransferRequestTypeDef",
    "CancelDetectMitigationActionsTaskRequestTypeDef",
    "CancelJobExecutionRequestTypeDef",
    "CancelJobRequestTypeDef",
    "CancelJobResponseTypeDef",
    "CertificateDescriptionTypeDef",
    "CertificateProviderSummaryTypeDef",
    "CertificateTypeDef",
    "CertificateValidityTypeDef",
    "ClientCertificateConfigTypeDef",
    "CloudwatchAlarmActionTypeDef",
    "CloudwatchLogsActionTypeDef",
    "CloudwatchMetricActionTypeDef",
    "CodeSigningCertificateChainTypeDef",
    "CodeSigningOutputTypeDef",
    "CodeSigningSignatureOutputTypeDef",
    "CodeSigningSignatureTypeDef",
    "CodeSigningSignatureUnionTypeDef",
    "CodeSigningTypeDef",
    "CodeSigningUnionTypeDef",
    "CommandExecutionResultTypeDef",
    "CommandExecutionSummaryTypeDef",
    "CommandParameterOutputTypeDef",
    "CommandParameterTypeDef",
    "CommandParameterUnionTypeDef",
    "CommandParameterValueOutputTypeDef",
    "CommandParameterValueTypeDef",
    "CommandParameterValueUnionTypeDef",
    "CommandPayloadOutputTypeDef",
    "CommandPayloadTypeDef",
    "CommandPayloadUnionTypeDef",
    "CommandSummaryTypeDef",
    "ConfigurationTypeDef",
    "ConfirmTopicRuleDestinationRequestTypeDef",
    "CreateAuditSuppressionRequestTypeDef",
    "CreateAuthorizerRequestTypeDef",
    "CreateAuthorizerResponseTypeDef",
    "CreateBillingGroupRequestTypeDef",
    "CreateBillingGroupResponseTypeDef",
    "CreateCertificateFromCsrRequestTypeDef",
    "CreateCertificateFromCsrResponseTypeDef",
    "CreateCertificateProviderRequestTypeDef",
    "CreateCertificateProviderResponseTypeDef",
    "CreateCommandRequestTypeDef",
    "CreateCommandResponseTypeDef",
    "CreateCustomMetricRequestTypeDef",
    "CreateCustomMetricResponseTypeDef",
    "CreateDimensionRequestTypeDef",
    "CreateDimensionResponseTypeDef",
    "CreateDomainConfigurationRequestTypeDef",
    "CreateDomainConfigurationResponseTypeDef",
    "CreateDynamicThingGroupRequestTypeDef",
    "CreateDynamicThingGroupResponseTypeDef",
    "CreateFleetMetricRequestTypeDef",
    "CreateFleetMetricResponseTypeDef",
    "CreateJobRequestTypeDef",
    "CreateJobResponseTypeDef",
    "CreateJobTemplateRequestTypeDef",
    "CreateJobTemplateResponseTypeDef",
    "CreateKeysAndCertificateRequestTypeDef",
    "CreateKeysAndCertificateResponseTypeDef",
    "CreateMitigationActionRequestTypeDef",
    "CreateMitigationActionResponseTypeDef",
    "CreateOTAUpdateRequestTypeDef",
    "CreateOTAUpdateResponseTypeDef",
    "CreatePackageRequestTypeDef",
    "CreatePackageResponseTypeDef",
    "CreatePackageVersionRequestTypeDef",
    "CreatePackageVersionResponseTypeDef",
    "CreatePolicyRequestTypeDef",
    "CreatePolicyResponseTypeDef",
    "CreatePolicyVersionRequestTypeDef",
    "CreatePolicyVersionResponseTypeDef",
    "CreateProvisioningClaimRequestTypeDef",
    "CreateProvisioningClaimResponseTypeDef",
    "CreateProvisioningTemplateRequestTypeDef",
    "CreateProvisioningTemplateResponseTypeDef",
    "CreateProvisioningTemplateVersionRequestTypeDef",
    "CreateProvisioningTemplateVersionResponseTypeDef",
    "CreateRoleAliasRequestTypeDef",
    "CreateRoleAliasResponseTypeDef",
    "CreateScheduledAuditRequestTypeDef",
    "CreateScheduledAuditResponseTypeDef",
    "CreateSecurityProfileRequestTypeDef",
    "CreateSecurityProfileResponseTypeDef",
    "CreateStreamRequestTypeDef",
    "CreateStreamResponseTypeDef",
    "CreateThingGroupRequestTypeDef",
    "CreateThingGroupResponseTypeDef",
    "CreateThingRequestTypeDef",
    "CreateThingResponseTypeDef",
    "CreateThingTypeRequestTypeDef",
    "CreateThingTypeResponseTypeDef",
    "CreateTopicRuleDestinationRequestTypeDef",
    "CreateTopicRuleDestinationResponseTypeDef",
    "CreateTopicRuleRequestTypeDef",
    "CustomCodeSigningOutputTypeDef",
    "CustomCodeSigningTypeDef",
    "CustomCodeSigningUnionTypeDef",
    "DeleteAccountAuditConfigurationRequestTypeDef",
    "DeleteAuditSuppressionRequestTypeDef",
    "DeleteAuthorizerRequestTypeDef",
    "DeleteBillingGroupRequestTypeDef",
    "DeleteCACertificateRequestTypeDef",
    "DeleteCertificateProviderRequestTypeDef",
    "DeleteCertificateRequestTypeDef",
    "DeleteCommandExecutionRequestTypeDef",
    "DeleteCommandRequestTypeDef",
    "DeleteCommandResponseTypeDef",
    "DeleteCustomMetricRequestTypeDef",
    "DeleteDimensionRequestTypeDef",
    "DeleteDomainConfigurationRequestTypeDef",
    "DeleteDynamicThingGroupRequestTypeDef",
    "DeleteFleetMetricRequestTypeDef",
    "DeleteJobExecutionRequestTypeDef",
    "DeleteJobRequestTypeDef",
    "DeleteJobTemplateRequestTypeDef",
    "DeleteMitigationActionRequestTypeDef",
    "DeleteOTAUpdateRequestTypeDef",
    "DeletePackageRequestTypeDef",
    "DeletePackageVersionRequestTypeDef",
    "DeletePolicyRequestTypeDef",
    "DeletePolicyVersionRequestTypeDef",
    "DeleteProvisioningTemplateRequestTypeDef",
    "DeleteProvisioningTemplateVersionRequestTypeDef",
    "DeleteRoleAliasRequestTypeDef",
    "DeleteScheduledAuditRequestTypeDef",
    "DeleteSecurityProfileRequestTypeDef",
    "DeleteStreamRequestTypeDef",
    "DeleteThingGroupRequestTypeDef",
    "DeleteThingRequestTypeDef",
    "DeleteThingTypeRequestTypeDef",
    "DeleteTopicRuleDestinationRequestTypeDef",
    "DeleteTopicRuleRequestTypeDef",
    "DeleteV2LoggingLevelRequestTypeDef",
    "DeniedTypeDef",
    "DeprecateThingTypeRequestTypeDef",
    "DescribeAccountAuditConfigurationResponseTypeDef",
    "DescribeAuditFindingRequestTypeDef",
    "DescribeAuditFindingResponseTypeDef",
    "DescribeAuditMitigationActionsTaskRequestTypeDef",
    "DescribeAuditMitigationActionsTaskResponseTypeDef",
    "DescribeAuditSuppressionRequestTypeDef",
    "DescribeAuditSuppressionResponseTypeDef",
    "DescribeAuditTaskRequestTypeDef",
    "DescribeAuditTaskResponseTypeDef",
    "DescribeAuthorizerRequestTypeDef",
    "DescribeAuthorizerResponseTypeDef",
    "DescribeBillingGroupRequestTypeDef",
    "DescribeBillingGroupResponseTypeDef",
    "DescribeCACertificateRequestTypeDef",
    "DescribeCACertificateResponseTypeDef",
    "DescribeCertificateProviderRequestTypeDef",
    "DescribeCertificateProviderResponseTypeDef",
    "DescribeCertificateRequestTypeDef",
    "DescribeCertificateResponseTypeDef",
    "DescribeCustomMetricRequestTypeDef",
    "DescribeCustomMetricResponseTypeDef",
    "DescribeDefaultAuthorizerResponseTypeDef",
    "DescribeDetectMitigationActionsTaskRequestTypeDef",
    "DescribeDetectMitigationActionsTaskResponseTypeDef",
    "DescribeDimensionRequestTypeDef",
    "DescribeDimensionResponseTypeDef",
    "DescribeDomainConfigurationRequestTypeDef",
    "DescribeDomainConfigurationResponseTypeDef",
    "DescribeEndpointRequestTypeDef",
    "DescribeEndpointResponseTypeDef",
    "DescribeEventConfigurationsResponseTypeDef",
    "DescribeFleetMetricRequestTypeDef",
    "DescribeFleetMetricResponseTypeDef",
    "DescribeIndexRequestTypeDef",
    "DescribeIndexResponseTypeDef",
    "DescribeJobExecutionRequestTypeDef",
    "DescribeJobExecutionResponseTypeDef",
    "DescribeJobRequestTypeDef",
    "DescribeJobResponseTypeDef",
    "DescribeJobTemplateRequestTypeDef",
    "DescribeJobTemplateResponseTypeDef",
    "DescribeManagedJobTemplateRequestTypeDef",
    "DescribeManagedJobTemplateResponseTypeDef",
    "DescribeMitigationActionRequestTypeDef",
    "DescribeMitigationActionResponseTypeDef",
    "DescribeProvisioningTemplateRequestTypeDef",
    "DescribeProvisioningTemplateResponseTypeDef",
    "DescribeProvisioningTemplateVersionRequestTypeDef",
    "DescribeProvisioningTemplateVersionResponseTypeDef",
    "DescribeRoleAliasRequestTypeDef",
    "DescribeRoleAliasResponseTypeDef",
    "DescribeScheduledAuditRequestTypeDef",
    "DescribeScheduledAuditResponseTypeDef",
    "DescribeSecurityProfileRequestTypeDef",
    "DescribeSecurityProfileResponseTypeDef",
    "DescribeStreamRequestTypeDef",
    "DescribeStreamResponseTypeDef",
    "DescribeThingGroupRequestTypeDef",
    "DescribeThingGroupResponseTypeDef",
    "DescribeThingRegistrationTaskRequestTypeDef",
    "DescribeThingRegistrationTaskResponseTypeDef",
    "DescribeThingRequestTypeDef",
    "DescribeThingResponseTypeDef",
    "DescribeThingTypeRequestTypeDef",
    "DescribeThingTypeResponseTypeDef",
    "DestinationTypeDef",
    "DetachPolicyRequestTypeDef",
    "DetachPrincipalPolicyRequestTypeDef",
    "DetachSecurityProfileRequestTypeDef",
    "DetachThingPrincipalRequestTypeDef",
    "DetectMitigationActionExecutionTypeDef",
    "DetectMitigationActionsTaskStatisticsTypeDef",
    "DetectMitigationActionsTaskSummaryTypeDef",
    "DetectMitigationActionsTaskTargetOutputTypeDef",
    "DetectMitigationActionsTaskTargetTypeDef",
    "DetectMitigationActionsTaskTargetUnionTypeDef",
    "DisableTopicRuleRequestTypeDef",
    "DisassociateSbomFromPackageVersionRequestTypeDef",
    "DocumentParameterTypeDef",
    "DomainConfigurationSummaryTypeDef",
    "DynamoDBActionTypeDef",
    "DynamoDBv2ActionTypeDef",
    "EffectivePolicyTypeDef",
    "ElasticsearchActionTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EnableIoTLoggingParamsTypeDef",
    "EnableTopicRuleRequestTypeDef",
    "ErrorInfoTypeDef",
    "ExplicitDenyTypeDef",
    "ExponentialRolloutRateTypeDef",
    "FieldTypeDef",
    "FileLocationTypeDef",
    "FirehoseActionTypeDef",
    "FleetMetricNameAndArnTypeDef",
    "GeoLocationTargetTypeDef",
    "GetBehaviorModelTrainingSummariesRequestPaginateTypeDef",
    "GetBehaviorModelTrainingSummariesRequestTypeDef",
    "GetBehaviorModelTrainingSummariesResponseTypeDef",
    "GetBucketsAggregationRequestTypeDef",
    "GetBucketsAggregationResponseTypeDef",
    "GetCardinalityRequestTypeDef",
    "GetCardinalityResponseTypeDef",
    "GetCommandExecutionRequestTypeDef",
    "GetCommandExecutionResponseTypeDef",
    "GetCommandRequestTypeDef",
    "GetCommandResponseTypeDef",
    "GetEffectivePoliciesRequestTypeDef",
    "GetEffectivePoliciesResponseTypeDef",
    "GetIndexingConfigurationResponseTypeDef",
    "GetJobDocumentRequestTypeDef",
    "GetJobDocumentResponseTypeDef",
    "GetLoggingOptionsResponseTypeDef",
    "GetOTAUpdateRequestTypeDef",
    "GetOTAUpdateResponseTypeDef",
    "GetPackageConfigurationResponseTypeDef",
    "GetPackageRequestTypeDef",
    "GetPackageResponseTypeDef",
    "GetPackageVersionRequestTypeDef",
    "GetPackageVersionResponseTypeDef",
    "GetPercentilesRequestTypeDef",
    "GetPercentilesResponseTypeDef",
    "GetPolicyRequestTypeDef",
    "GetPolicyResponseTypeDef",
    "GetPolicyVersionRequestTypeDef",
    "GetPolicyVersionResponseTypeDef",
    "GetRegistrationCodeResponseTypeDef",
    "GetStatisticsRequestTypeDef",
    "GetStatisticsResponseTypeDef",
    "GetThingConnectivityDataRequestTypeDef",
    "GetThingConnectivityDataResponseTypeDef",
    "GetTopicRuleDestinationRequestTypeDef",
    "GetTopicRuleDestinationResponseTypeDef",
    "GetTopicRuleRequestTypeDef",
    "GetTopicRuleResponseTypeDef",
    "GetV2LoggingOptionsResponseTypeDef",
    "GroupNameAndArnTypeDef",
    "HttpActionHeaderTypeDef",
    "HttpActionOutputTypeDef",
    "HttpActionTypeDef",
    "HttpActionUnionTypeDef",
    "HttpAuthorizationTypeDef",
    "HttpContextTypeDef",
    "HttpUrlDestinationConfigurationTypeDef",
    "HttpUrlDestinationPropertiesTypeDef",
    "HttpUrlDestinationSummaryTypeDef",
    "ImplicitDenyTypeDef",
    "IndexingFilterOutputTypeDef",
    "IndexingFilterTypeDef",
    "IotAnalyticsActionTypeDef",
    "IotEventsActionTypeDef",
    "IotSiteWiseActionOutputTypeDef",
    "IotSiteWiseActionTypeDef",
    "IotSiteWiseActionUnionTypeDef",
    "IssuerCertificateIdentifierTypeDef",
    "JobExecutionStatusDetailsTypeDef",
    "JobExecutionSummaryForJobTypeDef",
    "JobExecutionSummaryForThingTypeDef",
    "JobExecutionSummaryTypeDef",
    "JobExecutionTypeDef",
    "JobExecutionsRetryConfigOutputTypeDef",
    "JobExecutionsRetryConfigTypeDef",
    "JobExecutionsRetryConfigUnionTypeDef",
    "JobExecutionsRolloutConfigTypeDef",
    "JobProcessDetailsTypeDef",
    "JobSummaryTypeDef",
    "JobTemplateSummaryTypeDef",
    "JobTypeDef",
    "KafkaActionHeaderTypeDef",
    "KafkaActionOutputTypeDef",
    "KafkaActionTypeDef",
    "KafkaActionUnionTypeDef",
    "KeyPairTypeDef",
    "KinesisActionTypeDef",
    "LambdaActionTypeDef",
    "ListActiveViolationsRequestPaginateTypeDef",
    "ListActiveViolationsRequestTypeDef",
    "ListActiveViolationsResponseTypeDef",
    "ListAttachedPoliciesRequestPaginateTypeDef",
    "ListAttachedPoliciesRequestTypeDef",
    "ListAttachedPoliciesResponseTypeDef",
    "ListAuditFindingsRequestPaginateTypeDef",
    "ListAuditFindingsRequestTypeDef",
    "ListAuditFindingsResponseTypeDef",
    "ListAuditMitigationActionsExecutionsRequestPaginateTypeDef",
    "ListAuditMitigationActionsExecutionsRequestTypeDef",
    "ListAuditMitigationActionsExecutionsResponseTypeDef",
    "ListAuditMitigationActionsTasksRequestPaginateTypeDef",
    "ListAuditMitigationActionsTasksRequestTypeDef",
    "ListAuditMitigationActionsTasksResponseTypeDef",
    "ListAuditSuppressionsRequestPaginateTypeDef",
    "ListAuditSuppressionsRequestTypeDef",
    "ListAuditSuppressionsResponseTypeDef",
    "ListAuditTasksRequestPaginateTypeDef",
    "ListAuditTasksRequestTypeDef",
    "ListAuditTasksResponseTypeDef",
    "ListAuthorizersRequestPaginateTypeDef",
    "ListAuthorizersRequestTypeDef",
    "ListAuthorizersResponseTypeDef",
    "ListBillingGroupsRequestPaginateTypeDef",
    "ListBillingGroupsRequestTypeDef",
    "ListBillingGroupsResponseTypeDef",
    "ListCACertificatesRequestPaginateTypeDef",
    "ListCACertificatesRequestTypeDef",
    "ListCACertificatesResponseTypeDef",
    "ListCertificateProvidersRequestTypeDef",
    "ListCertificateProvidersResponseTypeDef",
    "ListCertificatesByCARequestPaginateTypeDef",
    "ListCertificatesByCARequestTypeDef",
    "ListCertificatesByCAResponseTypeDef",
    "ListCertificatesRequestPaginateTypeDef",
    "ListCertificatesRequestTypeDef",
    "ListCertificatesResponseTypeDef",
    "ListCommandExecutionsRequestPaginateTypeDef",
    "ListCommandExecutionsRequestTypeDef",
    "ListCommandExecutionsResponseTypeDef",
    "ListCommandsRequestPaginateTypeDef",
    "ListCommandsRequestTypeDef",
    "ListCommandsResponseTypeDef",
    "ListCustomMetricsRequestPaginateTypeDef",
    "ListCustomMetricsRequestTypeDef",
    "ListCustomMetricsResponseTypeDef",
    "ListDetectMitigationActionsExecutionsRequestPaginateTypeDef",
    "ListDetectMitigationActionsExecutionsRequestTypeDef",
    "ListDetectMitigationActionsExecutionsResponseTypeDef",
    "ListDetectMitigationActionsTasksRequestPaginateTypeDef",
    "ListDetectMitigationActionsTasksRequestTypeDef",
    "ListDetectMitigationActionsTasksResponseTypeDef",
    "ListDimensionsRequestPaginateTypeDef",
    "ListDimensionsRequestTypeDef",
    "ListDimensionsResponseTypeDef",
    "ListDomainConfigurationsRequestPaginateTypeDef",
    "ListDomainConfigurationsRequestTypeDef",
    "ListDomainConfigurationsResponseTypeDef",
    "ListFleetMetricsRequestPaginateTypeDef",
    "ListFleetMetricsRequestTypeDef",
    "ListFleetMetricsResponseTypeDef",
    "ListIndicesRequestPaginateTypeDef",
    "ListIndicesRequestTypeDef",
    "ListIndicesResponseTypeDef",
    "ListJobExecutionsForJobRequestPaginateTypeDef",
    "ListJobExecutionsForJobRequestTypeDef",
    "ListJobExecutionsForJobResponseTypeDef",
    "ListJobExecutionsForThingRequestPaginateTypeDef",
    "ListJobExecutionsForThingRequestTypeDef",
    "ListJobExecutionsForThingResponseTypeDef",
    "ListJobTemplatesRequestPaginateTypeDef",
    "ListJobTemplatesRequestTypeDef",
    "ListJobTemplatesResponseTypeDef",
    "ListJobsRequestPaginateTypeDef",
    "ListJobsRequestTypeDef",
    "ListJobsResponseTypeDef",
    "ListManagedJobTemplatesRequestPaginateTypeDef",
    "ListManagedJobTemplatesRequestTypeDef",
    "ListManagedJobTemplatesResponseTypeDef",
    "ListMetricValuesRequestPaginateTypeDef",
    "ListMetricValuesRequestTypeDef",
    "ListMetricValuesResponseTypeDef",
    "ListMitigationActionsRequestPaginateTypeDef",
    "ListMitigationActionsRequestTypeDef",
    "ListMitigationActionsResponseTypeDef",
    "ListOTAUpdatesRequestPaginateTypeDef",
    "ListOTAUpdatesRequestTypeDef",
    "ListOTAUpdatesResponseTypeDef",
    "ListOutgoingCertificatesRequestPaginateTypeDef",
    "ListOutgoingCertificatesRequestTypeDef",
    "ListOutgoingCertificatesResponseTypeDef",
    "ListPackageVersionsRequestPaginateTypeDef",
    "ListPackageVersionsRequestTypeDef",
    "ListPackageVersionsResponseTypeDef",
    "ListPackagesRequestPaginateTypeDef",
    "ListPackagesRequestTypeDef",
    "ListPackagesResponseTypeDef",
    "ListPoliciesRequestPaginateTypeDef",
    "ListPoliciesRequestTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListPolicyPrincipalsRequestPaginateTypeDef",
    "ListPolicyPrincipalsRequestTypeDef",
    "ListPolicyPrincipalsResponseTypeDef",
    "ListPolicyVersionsRequestTypeDef",
    "ListPolicyVersionsResponseTypeDef",
    "ListPrincipalPoliciesRequestPaginateTypeDef",
    "ListPrincipalPoliciesRequestTypeDef",
    "ListPrincipalPoliciesResponseTypeDef",
    "ListPrincipalThingsRequestPaginateTypeDef",
    "ListPrincipalThingsRequestTypeDef",
    "ListPrincipalThingsResponseTypeDef",
    "ListPrincipalThingsV2RequestPaginateTypeDef",
    "ListPrincipalThingsV2RequestTypeDef",
    "ListPrincipalThingsV2ResponseTypeDef",
    "ListProvisioningTemplateVersionsRequestPaginateTypeDef",
    "ListProvisioningTemplateVersionsRequestTypeDef",
    "ListProvisioningTemplateVersionsResponseTypeDef",
    "ListProvisioningTemplatesRequestPaginateTypeDef",
    "ListProvisioningTemplatesRequestTypeDef",
    "ListProvisioningTemplatesResponseTypeDef",
    "ListRelatedResourcesForAuditFindingRequestPaginateTypeDef",
    "ListRelatedResourcesForAuditFindingRequestTypeDef",
    "ListRelatedResourcesForAuditFindingResponseTypeDef",
    "ListRoleAliasesRequestPaginateTypeDef",
    "ListRoleAliasesRequestTypeDef",
    "ListRoleAliasesResponseTypeDef",
    "ListSbomValidationResultsRequestPaginateTypeDef",
    "ListSbomValidationResultsRequestTypeDef",
    "ListSbomValidationResultsResponseTypeDef",
    "ListScheduledAuditsRequestPaginateTypeDef",
    "ListScheduledAuditsRequestTypeDef",
    "ListScheduledAuditsResponseTypeDef",
    "ListSecurityProfilesForTargetRequestPaginateTypeDef",
    "ListSecurityProfilesForTargetRequestTypeDef",
    "ListSecurityProfilesForTargetResponseTypeDef",
    "ListSecurityProfilesRequestPaginateTypeDef",
    "ListSecurityProfilesRequestTypeDef",
    "ListSecurityProfilesResponseTypeDef",
    "ListStreamsRequestPaginateTypeDef",
    "ListStreamsRequestTypeDef",
    "ListStreamsResponseTypeDef",
    "ListTagsForResourceRequestPaginateTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTargetsForPolicyRequestPaginateTypeDef",
    "ListTargetsForPolicyRequestTypeDef",
    "ListTargetsForPolicyResponseTypeDef",
    "ListTargetsForSecurityProfileRequestPaginateTypeDef",
    "ListTargetsForSecurityProfileRequestTypeDef",
    "ListTargetsForSecurityProfileResponseTypeDef",
    "ListThingGroupsForThingRequestPaginateTypeDef",
    "ListThingGroupsForThingRequestTypeDef",
    "ListThingGroupsForThingResponseTypeDef",
    "ListThingGroupsRequestPaginateTypeDef",
    "ListThingGroupsRequestTypeDef",
    "ListThingGroupsResponseTypeDef",
    "ListThingPrincipalsRequestPaginateTypeDef",
    "ListThingPrincipalsRequestTypeDef",
    "ListThingPrincipalsResponseTypeDef",
    "ListThingPrincipalsV2RequestPaginateTypeDef",
    "ListThingPrincipalsV2RequestTypeDef",
    "ListThingPrincipalsV2ResponseTypeDef",
    "ListThingRegistrationTaskReportsRequestPaginateTypeDef",
    "ListThingRegistrationTaskReportsRequestTypeDef",
    "ListThingRegistrationTaskReportsResponseTypeDef",
    "ListThingRegistrationTasksRequestPaginateTypeDef",
    "ListThingRegistrationTasksRequestTypeDef",
    "ListThingRegistrationTasksResponseTypeDef",
    "ListThingTypesRequestPaginateTypeDef",
    "ListThingTypesRequestTypeDef",
    "ListThingTypesResponseTypeDef",
    "ListThingsInBillingGroupRequestPaginateTypeDef",
    "ListThingsInBillingGroupRequestTypeDef",
    "ListThingsInBillingGroupResponseTypeDef",
    "ListThingsInThingGroupRequestPaginateTypeDef",
    "ListThingsInThingGroupRequestTypeDef",
    "ListThingsInThingGroupResponseTypeDef",
    "ListThingsRequestPaginateTypeDef",
    "ListThingsRequestTypeDef",
    "ListThingsResponseTypeDef",
    "ListTopicRuleDestinationsRequestPaginateTypeDef",
    "ListTopicRuleDestinationsRequestTypeDef",
    "ListTopicRuleDestinationsResponseTypeDef",
    "ListTopicRulesRequestPaginateTypeDef",
    "ListTopicRulesRequestTypeDef",
    "ListTopicRulesResponseTypeDef",
    "ListV2LoggingLevelsRequestPaginateTypeDef",
    "ListV2LoggingLevelsRequestTypeDef",
    "ListV2LoggingLevelsResponseTypeDef",
    "ListViolationEventsRequestPaginateTypeDef",
    "ListViolationEventsRequestTypeDef",
    "ListViolationEventsResponseTypeDef",
    "LocationActionTypeDef",
    "LocationTimestampTypeDef",
    "LogTargetConfigurationTypeDef",
    "LogTargetTypeDef",
    "LoggingOptionsPayloadTypeDef",
    "MachineLearningDetectionConfigTypeDef",
    "MaintenanceWindowTypeDef",
    "ManagedJobTemplateSummaryTypeDef",
    "MetricDatumTypeDef",
    "MetricDimensionTypeDef",
    "MetricToRetainTypeDef",
    "MetricValueOutputTypeDef",
    "MetricValueTypeDef",
    "MetricValueUnionTypeDef",
    "MetricsExportConfigTypeDef",
    "MitigationActionIdentifierTypeDef",
    "MitigationActionParamsOutputTypeDef",
    "MitigationActionParamsTypeDef",
    "MitigationActionParamsUnionTypeDef",
    "MitigationActionTypeDef",
    "Mqtt5ConfigurationOutputTypeDef",
    "Mqtt5ConfigurationTypeDef",
    "MqttContextTypeDef",
    "MqttHeadersOutputTypeDef",
    "MqttHeadersTypeDef",
    "MqttHeadersUnionTypeDef",
    "NonCompliantResourceTypeDef",
    "OTAUpdateFileOutputTypeDef",
    "OTAUpdateFileTypeDef",
    "OTAUpdateFileUnionTypeDef",
    "OTAUpdateInfoTypeDef",
    "OTAUpdateSummaryTypeDef",
    "OpenSearchActionTypeDef",
    "OutgoingCertificateTypeDef",
    "PackageSummaryTypeDef",
    "PackageVersionArtifactTypeDef",
    "PackageVersionSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PercentPairTypeDef",
    "PolicyTypeDef",
    "PolicyVersionIdentifierTypeDef",
    "PolicyVersionTypeDef",
    "PresignedUrlConfigTypeDef",
    "PrincipalThingObjectTypeDef",
    "PropagatingAttributeTypeDef",
    "ProvisioningHookTypeDef",
    "ProvisioningTemplateSummaryTypeDef",
    "ProvisioningTemplateVersionSummaryTypeDef",
    "PublishFindingToSnsParamsTypeDef",
    "PutAssetPropertyValueEntryOutputTypeDef",
    "PutAssetPropertyValueEntryTypeDef",
    "PutAssetPropertyValueEntryUnionTypeDef",
    "PutItemInputTypeDef",
    "PutVerificationStateOnViolationRequestTypeDef",
    "RateIncreaseCriteriaTypeDef",
    "RegisterCACertificateRequestTypeDef",
    "RegisterCACertificateResponseTypeDef",
    "RegisterCertificateRequestTypeDef",
    "RegisterCertificateResponseTypeDef",
    "RegisterCertificateWithoutCARequestTypeDef",
    "RegisterCertificateWithoutCAResponseTypeDef",
    "RegisterThingRequestTypeDef",
    "RegisterThingResponseTypeDef",
    "RegistrationConfigTypeDef",
    "RejectCertificateTransferRequestTypeDef",
    "RelatedResourceTypeDef",
    "RemoveThingFromBillingGroupRequestTypeDef",
    "RemoveThingFromThingGroupRequestTypeDef",
    "ReplaceDefaultPolicyVersionParamsTypeDef",
    "ReplaceTopicRuleRequestTypeDef",
    "RepublishActionOutputTypeDef",
    "RepublishActionTypeDef",
    "RepublishActionUnionTypeDef",
    "ResourceIdentifierTypeDef",
    "ResponseMetadataTypeDef",
    "RetryCriteriaTypeDef",
    "RoleAliasDescriptionTypeDef",
    "S3ActionTypeDef",
    "S3DestinationTypeDef",
    "S3LocationTypeDef",
    "SalesforceActionTypeDef",
    "SbomTypeDef",
    "SbomValidationResultSummaryTypeDef",
    "ScheduledAuditMetadataTypeDef",
    "ScheduledJobRolloutTypeDef",
    "SchedulingConfigOutputTypeDef",
    "SchedulingConfigTypeDef",
    "SchedulingConfigUnionTypeDef",
    "SearchIndexRequestTypeDef",
    "SearchIndexResponseTypeDef",
    "SecurityProfileIdentifierTypeDef",
    "SecurityProfileTargetMappingTypeDef",
    "SecurityProfileTargetTypeDef",
    "ServerCertificateConfigTypeDef",
    "ServerCertificateSummaryTypeDef",
    "SetDefaultAuthorizerRequestTypeDef",
    "SetDefaultAuthorizerResponseTypeDef",
    "SetDefaultPolicyVersionRequestTypeDef",
    "SetLoggingOptionsRequestTypeDef",
    "SetV2LoggingLevelRequestTypeDef",
    "SetV2LoggingOptionsRequestTypeDef",
    "SigV4AuthorizationTypeDef",
    "SigningProfileParameterTypeDef",
    "SnsActionTypeDef",
    "SqsActionTypeDef",
    "StartAuditMitigationActionsTaskRequestTypeDef",
    "StartAuditMitigationActionsTaskResponseTypeDef",
    "StartDetectMitigationActionsTaskRequestTypeDef",
    "StartDetectMitigationActionsTaskResponseTypeDef",
    "StartOnDemandAuditTaskRequestTypeDef",
    "StartOnDemandAuditTaskResponseTypeDef",
    "StartSigningJobParameterTypeDef",
    "StartThingRegistrationTaskRequestTypeDef",
    "StartThingRegistrationTaskResponseTypeDef",
    "StatisticalThresholdTypeDef",
    "StatisticsTypeDef",
    "StatusReasonTypeDef",
    "StepFunctionsActionTypeDef",
    "StopThingRegistrationTaskRequestTypeDef",
    "StreamFileTypeDef",
    "StreamInfoTypeDef",
    "StreamSummaryTypeDef",
    "StreamTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "TaskStatisticsForAuditCheckTypeDef",
    "TaskStatisticsTypeDef",
    "TermsAggregationTypeDef",
    "TestAuthorizationRequestTypeDef",
    "TestAuthorizationResponseTypeDef",
    "TestInvokeAuthorizerRequestTypeDef",
    "TestInvokeAuthorizerResponseTypeDef",
    "ThingAttributeTypeDef",
    "ThingConnectivityTypeDef",
    "ThingDocumentTypeDef",
    "ThingGroupDocumentTypeDef",
    "ThingGroupIndexingConfigurationOutputTypeDef",
    "ThingGroupIndexingConfigurationTypeDef",
    "ThingGroupIndexingConfigurationUnionTypeDef",
    "ThingGroupMetadataTypeDef",
    "ThingGroupPropertiesOutputTypeDef",
    "ThingGroupPropertiesTypeDef",
    "ThingGroupPropertiesUnionTypeDef",
    "ThingIndexingConfigurationOutputTypeDef",
    "ThingIndexingConfigurationTypeDef",
    "ThingIndexingConfigurationUnionTypeDef",
    "ThingPrincipalObjectTypeDef",
    "ThingTypeDefinitionTypeDef",
    "ThingTypeMetadataTypeDef",
    "ThingTypePropertiesOutputTypeDef",
    "ThingTypePropertiesTypeDef",
    "ThingTypePropertiesUnionTypeDef",
    "TimeFilterTypeDef",
    "TimeoutConfigTypeDef",
    "TimestampTypeDef",
    "TimestreamActionOutputTypeDef",
    "TimestreamActionTypeDef",
    "TimestreamActionUnionTypeDef",
    "TimestreamDimensionTypeDef",
    "TimestreamTimestampTypeDef",
    "TlsConfigTypeDef",
    "TlsContextTypeDef",
    "TopicRuleDestinationConfigurationTypeDef",
    "TopicRuleDestinationSummaryTypeDef",
    "TopicRuleDestinationTypeDef",
    "TopicRuleListItemTypeDef",
    "TopicRulePayloadTypeDef",
    "TopicRuleTypeDef",
    "TransferCertificateRequestTypeDef",
    "TransferCertificateResponseTypeDef",
    "TransferDataTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAccountAuditConfigurationRequestTypeDef",
    "UpdateAuditSuppressionRequestTypeDef",
    "UpdateAuthorizerRequestTypeDef",
    "UpdateAuthorizerResponseTypeDef",
    "UpdateBillingGroupRequestTypeDef",
    "UpdateBillingGroupResponseTypeDef",
    "UpdateCACertificateParamsTypeDef",
    "UpdateCACertificateRequestTypeDef",
    "UpdateCertificateProviderRequestTypeDef",
    "UpdateCertificateProviderResponseTypeDef",
    "UpdateCertificateRequestTypeDef",
    "UpdateCommandRequestTypeDef",
    "UpdateCommandResponseTypeDef",
    "UpdateCustomMetricRequestTypeDef",
    "UpdateCustomMetricResponseTypeDef",
    "UpdateDeviceCertificateParamsTypeDef",
    "UpdateDimensionRequestTypeDef",
    "UpdateDimensionResponseTypeDef",
    "UpdateDomainConfigurationRequestTypeDef",
    "UpdateDomainConfigurationResponseTypeDef",
    "UpdateDynamicThingGroupRequestTypeDef",
    "UpdateDynamicThingGroupResponseTypeDef",
    "UpdateEventConfigurationsRequestTypeDef",
    "UpdateFleetMetricRequestTypeDef",
    "UpdateIndexingConfigurationRequestTypeDef",
    "UpdateJobRequestTypeDef",
    "UpdateMitigationActionRequestTypeDef",
    "UpdateMitigationActionResponseTypeDef",
    "UpdatePackageConfigurationRequestTypeDef",
    "UpdatePackageRequestTypeDef",
    "UpdatePackageVersionRequestTypeDef",
    "UpdateProvisioningTemplateRequestTypeDef",
    "UpdateRoleAliasRequestTypeDef",
    "UpdateRoleAliasResponseTypeDef",
    "UpdateScheduledAuditRequestTypeDef",
    "UpdateScheduledAuditResponseTypeDef",
    "UpdateSecurityProfileRequestTypeDef",
    "UpdateSecurityProfileResponseTypeDef",
    "UpdateStreamRequestTypeDef",
    "UpdateStreamResponseTypeDef",
    "UpdateThingGroupRequestTypeDef",
    "UpdateThingGroupResponseTypeDef",
    "UpdateThingGroupsForThingRequestTypeDef",
    "UpdateThingRequestTypeDef",
    "UpdateThingTypeRequestTypeDef",
    "UpdateTopicRuleDestinationRequestTypeDef",
    "UserPropertyTypeDef",
    "ValidateSecurityProfileBehaviorsRequestTypeDef",
    "ValidateSecurityProfileBehaviorsResponseTypeDef",
    "ValidationErrorTypeDef",
    "VersionUpdateByJobsConfigTypeDef",
    "ViolationEventAdditionalInfoTypeDef",
    "ViolationEventOccurrenceRangeOutputTypeDef",
    "ViolationEventOccurrenceRangeTypeDef",
    "ViolationEventOccurrenceRangeUnionTypeDef",
    "ViolationEventTypeDef",
    "VpcDestinationConfigurationTypeDef",
    "VpcDestinationPropertiesTypeDef",
    "VpcDestinationSummaryTypeDef",
)


class AbortCriteriaTypeDef(TypedDict):
    failureType: JobExecutionFailureTypeType
    action: Literal["CANCEL"]
    thresholdPercentage: float
    minNumberOfExecutedThings: int


class AcceptCertificateTransferRequestTypeDef(TypedDict):
    certificateId: str
    setAsActive: NotRequired[bool]


class CloudwatchAlarmActionTypeDef(TypedDict):
    roleArn: str
    alarmName: str
    stateReason: str
    stateValue: str


class CloudwatchLogsActionTypeDef(TypedDict):
    roleArn: str
    logGroupName: str
    batchMode: NotRequired[bool]


class CloudwatchMetricActionTypeDef(TypedDict):
    roleArn: str
    metricNamespace: str
    metricName: str
    metricValue: str
    metricUnit: str
    metricTimestamp: NotRequired[str]


class DynamoDBActionTypeDef(TypedDict):
    tableName: str
    roleArn: str
    hashKeyField: str
    hashKeyValue: str
    operation: NotRequired[str]
    hashKeyType: NotRequired[DynamoKeyTypeType]
    rangeKeyField: NotRequired[str]
    rangeKeyValue: NotRequired[str]
    rangeKeyType: NotRequired[DynamoKeyTypeType]
    payloadField: NotRequired[str]


ElasticsearchActionTypeDef = TypedDict(
    "ElasticsearchActionTypeDef",
    {
        "roleArn": str,
        "endpoint": str,
        "index": str,
        "type": str,
        "id": str,
    },
)


class FirehoseActionTypeDef(TypedDict):
    roleArn: str
    deliveryStreamName: str
    separator: NotRequired[str]
    batchMode: NotRequired[bool]


class IotAnalyticsActionTypeDef(TypedDict):
    channelArn: NotRequired[str]
    channelName: NotRequired[str]
    batchMode: NotRequired[bool]
    roleArn: NotRequired[str]


class IotEventsActionTypeDef(TypedDict):
    inputName: str
    roleArn: str
    messageId: NotRequired[str]
    batchMode: NotRequired[bool]


class KinesisActionTypeDef(TypedDict):
    roleArn: str
    streamName: str
    partitionKey: NotRequired[str]


class LambdaActionTypeDef(TypedDict):
    functionArn: str


OpenSearchActionTypeDef = TypedDict(
    "OpenSearchActionTypeDef",
    {
        "roleArn": str,
        "endpoint": str,
        "index": str,
        "type": str,
        "id": str,
    },
)


class S3ActionTypeDef(TypedDict):
    roleArn: str
    bucketName: str
    key: str
    cannedAcl: NotRequired[CannedAccessControlListType]


class SalesforceActionTypeDef(TypedDict):
    token: str
    url: str


class SnsActionTypeDef(TypedDict):
    targetArn: str
    roleArn: str
    messageFormat: NotRequired[MessageFormatType]


class SqsActionTypeDef(TypedDict):
    roleArn: str
    queueUrl: str
    useBase64: NotRequired[bool]


class StepFunctionsActionTypeDef(TypedDict):
    stateMachineName: str
    roleArn: str
    executionNamePrefix: NotRequired[str]


class MetricValueOutputTypeDef(TypedDict):
    count: NotRequired[int]
    cidrs: NotRequired[List[str]]
    ports: NotRequired[List[int]]
    number: NotRequired[float]
    numbers: NotRequired[List[float]]
    strings: NotRequired[List[str]]


class ViolationEventAdditionalInfoTypeDef(TypedDict):
    confidenceLevel: NotRequired[ConfidenceLevelType]


class AddThingToBillingGroupRequestTypeDef(TypedDict):
    billingGroupName: NotRequired[str]
    billingGroupArn: NotRequired[str]
    thingName: NotRequired[str]
    thingArn: NotRequired[str]


class AddThingToThingGroupRequestTypeDef(TypedDict):
    thingGroupName: NotRequired[str]
    thingGroupArn: NotRequired[str]
    thingName: NotRequired[str]
    thingArn: NotRequired[str]
    overrideDynamicGroups: NotRequired[bool]


class AddThingsToThingGroupParamsOutputTypeDef(TypedDict):
    thingGroupNames: List[str]
    overrideDynamicGroups: NotRequired[bool]


class AddThingsToThingGroupParamsTypeDef(TypedDict):
    thingGroupNames: Sequence[str]
    overrideDynamicGroups: NotRequired[bool]


class AggregationTypeOutputTypeDef(TypedDict):
    name: AggregationTypeNameType
    values: NotRequired[List[str]]


class AggregationTypeTypeDef(TypedDict):
    name: AggregationTypeNameType
    values: NotRequired[Sequence[str]]


class AlertTargetTypeDef(TypedDict):
    alertTargetArn: str
    roleArn: str


class PolicyTypeDef(TypedDict):
    policyName: NotRequired[str]
    policyArn: NotRequired[str]


class AssetPropertyTimestampTypeDef(TypedDict):
    timeInSeconds: str
    offsetInNanos: NotRequired[str]


class AssetPropertyVariantTypeDef(TypedDict):
    stringValue: NotRequired[str]
    integerValue: NotRequired[str]
    doubleValue: NotRequired[str]
    booleanValue: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AssociateTargetsWithJobRequestTypeDef(TypedDict):
    targets: Sequence[str]
    jobId: str
    comment: NotRequired[str]
    namespaceId: NotRequired[str]


class AttachPolicyRequestTypeDef(TypedDict):
    policyName: str
    target: str


class AttachPrincipalPolicyRequestTypeDef(TypedDict):
    policyName: str
    principal: str


class AttachSecurityProfileRequestTypeDef(TypedDict):
    securityProfileName: str
    securityProfileTargetArn: str


class AttachThingPrincipalRequestTypeDef(TypedDict):
    thingName: str
    principal: str
    thingPrincipalType: NotRequired[ThingPrincipalTypeType]


class AttributePayloadOutputTypeDef(TypedDict):
    attributes: NotRequired[Dict[str, str]]
    merge: NotRequired[bool]


class AttributePayloadTypeDef(TypedDict):
    attributes: NotRequired[Mapping[str, str]]
    merge: NotRequired[bool]


class AuditCheckConfigurationOutputTypeDef(TypedDict):
    enabled: NotRequired[bool]
    configuration: NotRequired[Dict[ConfigNameType, str]]


class AuditCheckConfigurationTypeDef(TypedDict):
    enabled: NotRequired[bool]
    configuration: NotRequired[Mapping[ConfigNameType, str]]


class AuditCheckDetailsTypeDef(TypedDict):
    checkRunStatus: NotRequired[AuditCheckRunStatusType]
    checkCompliant: NotRequired[bool]
    totalResourcesCount: NotRequired[int]
    nonCompliantResourcesCount: NotRequired[int]
    suppressedNonCompliantResourcesCount: NotRequired[int]
    errorCode: NotRequired[str]
    message: NotRequired[str]


class AuditMitigationActionExecutionMetadataTypeDef(TypedDict):
    taskId: NotRequired[str]
    findingId: NotRequired[str]
    actionName: NotRequired[str]
    actionId: NotRequired[str]
    status: NotRequired[AuditMitigationActionsExecutionStatusType]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]
    errorCode: NotRequired[str]
    message: NotRequired[str]


class AuditMitigationActionsTaskMetadataTypeDef(TypedDict):
    taskId: NotRequired[str]
    startTime: NotRequired[datetime]
    taskStatus: NotRequired[AuditMitigationActionsTaskStatusType]


class AuditMitigationActionsTaskTargetOutputTypeDef(TypedDict):
    auditTaskId: NotRequired[str]
    findingIds: NotRequired[List[str]]
    auditCheckToReasonCodeFilter: NotRequired[Dict[str, List[str]]]


class AuditMitigationActionsTaskTargetTypeDef(TypedDict):
    auditTaskId: NotRequired[str]
    findingIds: NotRequired[Sequence[str]]
    auditCheckToReasonCodeFilter: NotRequired[Mapping[str, Sequence[str]]]


class AuditNotificationTargetTypeDef(TypedDict):
    targetArn: NotRequired[str]
    roleArn: NotRequired[str]
    enabled: NotRequired[bool]


class AuditTaskMetadataTypeDef(TypedDict):
    taskId: NotRequired[str]
    taskStatus: NotRequired[AuditTaskStatusType]
    taskType: NotRequired[AuditTaskTypeType]


class AuthInfoOutputTypeDef(TypedDict):
    resources: List[str]
    actionType: NotRequired[ActionTypeType]


class AuthInfoTypeDef(TypedDict):
    resources: Sequence[str]
    actionType: NotRequired[ActionTypeType]


class AuthorizerConfigTypeDef(TypedDict):
    defaultAuthorizerName: NotRequired[str]
    allowAuthorizerOverride: NotRequired[bool]


class AuthorizerDescriptionTypeDef(TypedDict):
    authorizerName: NotRequired[str]
    authorizerArn: NotRequired[str]
    authorizerFunctionArn: NotRequired[str]
    tokenKeyName: NotRequired[str]
    tokenSigningPublicKeys: NotRequired[Dict[str, str]]
    status: NotRequired[AuthorizerStatusType]
    creationDate: NotRequired[datetime]
    lastModifiedDate: NotRequired[datetime]
    signingDisabled: NotRequired[bool]
    enableCachingForHttp: NotRequired[bool]


class AuthorizerSummaryTypeDef(TypedDict):
    authorizerName: NotRequired[str]
    authorizerArn: NotRequired[str]


class AwsJobAbortCriteriaTypeDef(TypedDict):
    failureType: AwsJobAbortCriteriaFailureTypeType
    action: Literal["CANCEL"]
    thresholdPercentage: float
    minNumberOfExecutedThings: int


class AwsJobRateIncreaseCriteriaTypeDef(TypedDict):
    numberOfNotifiedThings: NotRequired[int]
    numberOfSucceededThings: NotRequired[int]


class AwsJobPresignedUrlConfigTypeDef(TypedDict):
    expiresInSec: NotRequired[int]


class AwsJobTimeoutConfigTypeDef(TypedDict):
    inProgressTimeoutInMinutes: NotRequired[int]


class MachineLearningDetectionConfigTypeDef(TypedDict):
    confidenceLevel: ConfidenceLevelType


class StatisticalThresholdTypeDef(TypedDict):
    statistic: NotRequired[str]


class BehaviorModelTrainingSummaryTypeDef(TypedDict):
    securityProfileName: NotRequired[str]
    behaviorName: NotRequired[str]
    trainingDataCollectionStartDate: NotRequired[datetime]
    modelStatus: NotRequired[ModelStatusType]
    datapointsCollectionPercentage: NotRequired[float]
    lastModelRefreshDate: NotRequired[datetime]


MetricDimensionTypeDef = TypedDict(
    "MetricDimensionTypeDef",
    {
        "dimensionName": str,
        "operator": NotRequired[DimensionValueOperatorType],
    },
)


class BillingGroupMetadataTypeDef(TypedDict):
    creationDate: NotRequired[datetime]


class BillingGroupPropertiesTypeDef(TypedDict):
    billingGroupDescription: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class BucketTypeDef(TypedDict):
    keyValue: NotRequired[str]
    count: NotRequired[int]


class TermsAggregationTypeDef(TypedDict):
    maxBuckets: NotRequired[int]


class CertificateValidityTypeDef(TypedDict):
    notBefore: NotRequired[datetime]
    notAfter: NotRequired[datetime]


class CACertificateTypeDef(TypedDict):
    certificateArn: NotRequired[str]
    certificateId: NotRequired[str]
    status: NotRequired[CACertificateStatusType]
    creationDate: NotRequired[datetime]


class CancelAuditMitigationActionsTaskRequestTypeDef(TypedDict):
    taskId: str


class CancelAuditTaskRequestTypeDef(TypedDict):
    taskId: str


class CancelCertificateTransferRequestTypeDef(TypedDict):
    certificateId: str


class CancelDetectMitigationActionsTaskRequestTypeDef(TypedDict):
    taskId: str


class CancelJobExecutionRequestTypeDef(TypedDict):
    jobId: str
    thingName: str
    force: NotRequired[bool]
    expectedVersion: NotRequired[int]
    statusDetails: NotRequired[Mapping[str, str]]


class CancelJobRequestTypeDef(TypedDict):
    jobId: str
    reasonCode: NotRequired[str]
    comment: NotRequired[str]
    force: NotRequired[bool]


class TransferDataTypeDef(TypedDict):
    transferMessage: NotRequired[str]
    rejectReason: NotRequired[str]
    transferDate: NotRequired[datetime]
    acceptDate: NotRequired[datetime]
    rejectDate: NotRequired[datetime]


class CertificateProviderSummaryTypeDef(TypedDict):
    certificateProviderName: NotRequired[str]
    certificateProviderArn: NotRequired[str]


class CertificateTypeDef(TypedDict):
    certificateArn: NotRequired[str]
    certificateId: NotRequired[str]
    status: NotRequired[CertificateStatusType]
    certificateMode: NotRequired[CertificateModeType]
    creationDate: NotRequired[datetime]


class ClientCertificateConfigTypeDef(TypedDict):
    clientCertificateCallbackArn: NotRequired[str]


class CodeSigningCertificateChainTypeDef(TypedDict):
    certificateName: NotRequired[str]
    inlineDocument: NotRequired[str]


class CodeSigningSignatureOutputTypeDef(TypedDict):
    inlineDocument: NotRequired[bytes]


class CommandExecutionResultTypeDef(TypedDict):
    S: NotRequired[str]
    B: NotRequired[bool]
    BIN: NotRequired[bytes]


class CommandExecutionSummaryTypeDef(TypedDict):
    commandArn: NotRequired[str]
    executionId: NotRequired[str]
    targetArn: NotRequired[str]
    status: NotRequired[CommandExecutionStatusType]
    createdAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    completedAt: NotRequired[datetime]


class CommandParameterValueOutputTypeDef(TypedDict):
    S: NotRequired[str]
    B: NotRequired[bool]
    I: NotRequired[int]
    L: NotRequired[int]
    D: NotRequired[float]
    BIN: NotRequired[bytes]
    UL: NotRequired[str]


class CommandPayloadOutputTypeDef(TypedDict):
    content: NotRequired[bytes]
    contentType: NotRequired[str]


class CommandSummaryTypeDef(TypedDict):
    commandArn: NotRequired[str]
    commandId: NotRequired[str]
    displayName: NotRequired[str]
    deprecated: NotRequired[bool]
    createdAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    pendingDeletion: NotRequired[bool]


class ConfigurationTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class ConfirmTopicRuleDestinationRequestTypeDef(TypedDict):
    confirmationToken: str


TimestampTypeDef = Union[datetime, str]


class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]


class CreateCertificateFromCsrRequestTypeDef(TypedDict):
    certificateSigningRequest: str
    setAsActive: NotRequired[bool]


class ServerCertificateConfigTypeDef(TypedDict):
    enableOCSPCheck: NotRequired[bool]
    ocspLambdaArn: NotRequired[str]
    ocspAuthorizedResponderArn: NotRequired[str]


class TlsConfigTypeDef(TypedDict):
    securityPolicy: NotRequired[str]


class PresignedUrlConfigTypeDef(TypedDict):
    roleArn: NotRequired[str]
    expiresInSec: NotRequired[int]


class TimeoutConfigTypeDef(TypedDict):
    inProgressTimeoutInMinutes: NotRequired[int]


class MaintenanceWindowTypeDef(TypedDict):
    startTime: str
    durationInMinutes: int


class CreateKeysAndCertificateRequestTypeDef(TypedDict):
    setAsActive: NotRequired[bool]


class KeyPairTypeDef(TypedDict):
    PublicKey: NotRequired[str]
    PrivateKey: NotRequired[str]


class CreatePackageRequestTypeDef(TypedDict):
    packageName: str
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class CreatePolicyVersionRequestTypeDef(TypedDict):
    policyName: str
    policyDocument: str
    setAsDefault: NotRequired[bool]


class CreateProvisioningClaimRequestTypeDef(TypedDict):
    templateName: str


class ProvisioningHookTypeDef(TypedDict):
    targetArn: str
    payloadVersion: NotRequired[str]


class CreateProvisioningTemplateVersionRequestTypeDef(TypedDict):
    templateName: str
    templateBody: str
    setAsDefault: NotRequired[bool]


class MetricsExportConfigTypeDef(TypedDict):
    mqttTopic: str
    roleArn: str


class DeleteAccountAuditConfigurationRequestTypeDef(TypedDict):
    deleteScheduledAudits: NotRequired[bool]


class DeleteAuthorizerRequestTypeDef(TypedDict):
    authorizerName: str


class DeleteBillingGroupRequestTypeDef(TypedDict):
    billingGroupName: str
    expectedVersion: NotRequired[int]


class DeleteCACertificateRequestTypeDef(TypedDict):
    certificateId: str


class DeleteCertificateProviderRequestTypeDef(TypedDict):
    certificateProviderName: str


class DeleteCertificateRequestTypeDef(TypedDict):
    certificateId: str
    forceDelete: NotRequired[bool]


class DeleteCommandExecutionRequestTypeDef(TypedDict):
    executionId: str
    targetArn: str


class DeleteCommandRequestTypeDef(TypedDict):
    commandId: str


class DeleteCustomMetricRequestTypeDef(TypedDict):
    metricName: str


class DeleteDimensionRequestTypeDef(TypedDict):
    name: str


class DeleteDomainConfigurationRequestTypeDef(TypedDict):
    domainConfigurationName: str


class DeleteDynamicThingGroupRequestTypeDef(TypedDict):
    thingGroupName: str
    expectedVersion: NotRequired[int]


class DeleteFleetMetricRequestTypeDef(TypedDict):
    metricName: str
    expectedVersion: NotRequired[int]


class DeleteJobExecutionRequestTypeDef(TypedDict):
    jobId: str
    thingName: str
    executionNumber: int
    force: NotRequired[bool]
    namespaceId: NotRequired[str]


class DeleteJobRequestTypeDef(TypedDict):
    jobId: str
    force: NotRequired[bool]
    namespaceId: NotRequired[str]


class DeleteJobTemplateRequestTypeDef(TypedDict):
    jobTemplateId: str


class DeleteMitigationActionRequestTypeDef(TypedDict):
    actionName: str


class DeleteOTAUpdateRequestTypeDef(TypedDict):
    otaUpdateId: str
    deleteStream: NotRequired[bool]
    forceDeleteAWSJob: NotRequired[bool]


class DeletePackageRequestTypeDef(TypedDict):
    packageName: str
    clientToken: NotRequired[str]


class DeletePackageVersionRequestTypeDef(TypedDict):
    packageName: str
    versionName: str
    clientToken: NotRequired[str]


class DeletePolicyRequestTypeDef(TypedDict):
    policyName: str


class DeletePolicyVersionRequestTypeDef(TypedDict):
    policyName: str
    policyVersionId: str


class DeleteProvisioningTemplateRequestTypeDef(TypedDict):
    templateName: str


class DeleteProvisioningTemplateVersionRequestTypeDef(TypedDict):
    templateName: str
    versionId: int


class DeleteRoleAliasRequestTypeDef(TypedDict):
    roleAlias: str


class DeleteScheduledAuditRequestTypeDef(TypedDict):
    scheduledAuditName: str


class DeleteSecurityProfileRequestTypeDef(TypedDict):
    securityProfileName: str
    expectedVersion: NotRequired[int]


class DeleteStreamRequestTypeDef(TypedDict):
    streamId: str


class DeleteThingGroupRequestTypeDef(TypedDict):
    thingGroupName: str
    expectedVersion: NotRequired[int]


class DeleteThingRequestTypeDef(TypedDict):
    thingName: str
    expectedVersion: NotRequired[int]


class DeleteThingTypeRequestTypeDef(TypedDict):
    thingTypeName: str


class DeleteTopicRuleDestinationRequestTypeDef(TypedDict):
    arn: str


class DeleteTopicRuleRequestTypeDef(TypedDict):
    ruleName: str


class DeleteV2LoggingLevelRequestTypeDef(TypedDict):
    targetType: LogTargetTypeType
    targetName: str


class DeprecateThingTypeRequestTypeDef(TypedDict):
    thingTypeName: str
    undoDeprecate: NotRequired[bool]


class DescribeAuditFindingRequestTypeDef(TypedDict):
    findingId: str


class DescribeAuditMitigationActionsTaskRequestTypeDef(TypedDict):
    taskId: str


class TaskStatisticsForAuditCheckTypeDef(TypedDict):
    totalFindingsCount: NotRequired[int]
    failedFindingsCount: NotRequired[int]
    succeededFindingsCount: NotRequired[int]
    skippedFindingsCount: NotRequired[int]
    canceledFindingsCount: NotRequired[int]


class DescribeAuditTaskRequestTypeDef(TypedDict):
    taskId: str


class TaskStatisticsTypeDef(TypedDict):
    totalChecks: NotRequired[int]
    inProgressChecks: NotRequired[int]
    waitingForDataCollectionChecks: NotRequired[int]
    compliantChecks: NotRequired[int]
    nonCompliantChecks: NotRequired[int]
    failedChecks: NotRequired[int]
    canceledChecks: NotRequired[int]


class DescribeAuthorizerRequestTypeDef(TypedDict):
    authorizerName: str


class DescribeBillingGroupRequestTypeDef(TypedDict):
    billingGroupName: str


class DescribeCACertificateRequestTypeDef(TypedDict):
    certificateId: str


class RegistrationConfigTypeDef(TypedDict):
    templateBody: NotRequired[str]
    roleArn: NotRequired[str]
    templateName: NotRequired[str]


class DescribeCertificateProviderRequestTypeDef(TypedDict):
    certificateProviderName: str


class DescribeCertificateRequestTypeDef(TypedDict):
    certificateId: str


class DescribeCustomMetricRequestTypeDef(TypedDict):
    metricName: str


class DescribeDetectMitigationActionsTaskRequestTypeDef(TypedDict):
    taskId: str


class DescribeDimensionRequestTypeDef(TypedDict):
    name: str


class DescribeDomainConfigurationRequestTypeDef(TypedDict):
    domainConfigurationName: str


class ServerCertificateSummaryTypeDef(TypedDict):
    serverCertificateArn: NotRequired[str]
    serverCertificateStatus: NotRequired[ServerCertificateStatusType]
    serverCertificateStatusDetail: NotRequired[str]


class DescribeEndpointRequestTypeDef(TypedDict):
    endpointType: NotRequired[str]


class DescribeFleetMetricRequestTypeDef(TypedDict):
    metricName: str


class DescribeIndexRequestTypeDef(TypedDict):
    indexName: str


class DescribeJobExecutionRequestTypeDef(TypedDict):
    jobId: str
    thingName: str
    executionNumber: NotRequired[int]


class DescribeJobRequestTypeDef(TypedDict):
    jobId: str
    beforeSubstitution: NotRequired[bool]


class DescribeJobTemplateRequestTypeDef(TypedDict):
    jobTemplateId: str


class DescribeManagedJobTemplateRequestTypeDef(TypedDict):
    templateName: str
    templateVersion: NotRequired[str]


class DocumentParameterTypeDef(TypedDict):
    key: NotRequired[str]
    description: NotRequired[str]
    regex: NotRequired[str]
    example: NotRequired[str]
    optional: NotRequired[bool]


class DescribeMitigationActionRequestTypeDef(TypedDict):
    actionName: str


class DescribeProvisioningTemplateRequestTypeDef(TypedDict):
    templateName: str


class DescribeProvisioningTemplateVersionRequestTypeDef(TypedDict):
    templateName: str
    versionId: int


class DescribeRoleAliasRequestTypeDef(TypedDict):
    roleAlias: str


class RoleAliasDescriptionTypeDef(TypedDict):
    roleAlias: NotRequired[str]
    roleAliasArn: NotRequired[str]
    roleArn: NotRequired[str]
    owner: NotRequired[str]
    credentialDurationSeconds: NotRequired[int]
    creationDate: NotRequired[datetime]
    lastModifiedDate: NotRequired[datetime]


class DescribeScheduledAuditRequestTypeDef(TypedDict):
    scheduledAuditName: str


class DescribeSecurityProfileRequestTypeDef(TypedDict):
    securityProfileName: str


class DescribeStreamRequestTypeDef(TypedDict):
    streamId: str


class DescribeThingGroupRequestTypeDef(TypedDict):
    thingGroupName: str


class DescribeThingRegistrationTaskRequestTypeDef(TypedDict):
    taskId: str


class DescribeThingRequestTypeDef(TypedDict):
    thingName: str


class DescribeThingTypeRequestTypeDef(TypedDict):
    thingTypeName: str


class ThingTypeMetadataTypeDef(TypedDict):
    deprecated: NotRequired[bool]
    deprecationDate: NotRequired[datetime]
    creationDate: NotRequired[datetime]


class S3DestinationTypeDef(TypedDict):
    bucket: NotRequired[str]
    prefix: NotRequired[str]


class DetachPolicyRequestTypeDef(TypedDict):
    policyName: str
    target: str


class DetachPrincipalPolicyRequestTypeDef(TypedDict):
    policyName: str
    principal: str


class DetachSecurityProfileRequestTypeDef(TypedDict):
    securityProfileName: str
    securityProfileTargetArn: str


class DetachThingPrincipalRequestTypeDef(TypedDict):
    thingName: str
    principal: str


class DetectMitigationActionExecutionTypeDef(TypedDict):
    taskId: NotRequired[str]
    violationId: NotRequired[str]
    actionName: NotRequired[str]
    thingName: NotRequired[str]
    executionStartDate: NotRequired[datetime]
    executionEndDate: NotRequired[datetime]
    status: NotRequired[DetectMitigationActionExecutionStatusType]
    errorCode: NotRequired[str]
    message: NotRequired[str]


class DetectMitigationActionsTaskStatisticsTypeDef(TypedDict):
    actionsExecuted: NotRequired[int]
    actionsSkipped: NotRequired[int]
    actionsFailed: NotRequired[int]


class DetectMitigationActionsTaskTargetOutputTypeDef(TypedDict):
    violationIds: NotRequired[List[str]]
    securityProfileName: NotRequired[str]
    behaviorName: NotRequired[str]


class ViolationEventOccurrenceRangeOutputTypeDef(TypedDict):
    startTime: datetime
    endTime: datetime


class DetectMitigationActionsTaskTargetTypeDef(TypedDict):
    violationIds: NotRequired[Sequence[str]]
    securityProfileName: NotRequired[str]
    behaviorName: NotRequired[str]


class DisableTopicRuleRequestTypeDef(TypedDict):
    ruleName: str


class DisassociateSbomFromPackageVersionRequestTypeDef(TypedDict):
    packageName: str
    versionName: str
    clientToken: NotRequired[str]


class DomainConfigurationSummaryTypeDef(TypedDict):
    domainConfigurationName: NotRequired[str]
    domainConfigurationArn: NotRequired[str]
    serviceType: NotRequired[ServiceTypeType]


class PutItemInputTypeDef(TypedDict):
    tableName: str


class EffectivePolicyTypeDef(TypedDict):
    policyName: NotRequired[str]
    policyArn: NotRequired[str]
    policyDocument: NotRequired[str]


class EnableIoTLoggingParamsTypeDef(TypedDict):
    roleArnForLogging: str
    logLevel: LogLevelType


class EnableTopicRuleRequestTypeDef(TypedDict):
    ruleName: str


class ErrorInfoTypeDef(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]


class RateIncreaseCriteriaTypeDef(TypedDict):
    numberOfNotifiedThings: NotRequired[int]
    numberOfSucceededThings: NotRequired[int]


FieldTypeDef = TypedDict(
    "FieldTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[FieldTypeType],
    },
)


class S3LocationTypeDef(TypedDict):
    bucket: NotRequired[str]
    key: NotRequired[str]
    version: NotRequired[str]


class StreamTypeDef(TypedDict):
    streamId: NotRequired[str]
    fileId: NotRequired[int]


class FleetMetricNameAndArnTypeDef(TypedDict):
    metricName: NotRequired[str]
    metricArn: NotRequired[str]


class GeoLocationTargetTypeDef(TypedDict):
    name: NotRequired[str]
    order: NotRequired[TargetFieldOrderType]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class GetBehaviorModelTrainingSummariesRequestTypeDef(TypedDict):
    securityProfileName: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class GetCardinalityRequestTypeDef(TypedDict):
    queryString: str
    indexName: NotRequired[str]
    aggregationField: NotRequired[str]
    queryVersion: NotRequired[str]


class GetCommandExecutionRequestTypeDef(TypedDict):
    executionId: str
    targetArn: str
    includeResult: NotRequired[bool]


class StatusReasonTypeDef(TypedDict):
    reasonCode: str
    reasonDescription: NotRequired[str]


class GetCommandRequestTypeDef(TypedDict):
    commandId: str


class GetEffectivePoliciesRequestTypeDef(TypedDict):
    principal: NotRequired[str]
    cognitoIdentityPoolId: NotRequired[str]
    thingName: NotRequired[str]


class GetJobDocumentRequestTypeDef(TypedDict):
    jobId: str
    beforeSubstitution: NotRequired[bool]


class GetOTAUpdateRequestTypeDef(TypedDict):
    otaUpdateId: str


class VersionUpdateByJobsConfigTypeDef(TypedDict):
    enabled: NotRequired[bool]
    roleArn: NotRequired[str]


class GetPackageRequestTypeDef(TypedDict):
    packageName: str


class GetPackageVersionRequestTypeDef(TypedDict):
    packageName: str
    versionName: str


class GetPercentilesRequestTypeDef(TypedDict):
    queryString: str
    indexName: NotRequired[str]
    aggregationField: NotRequired[str]
    queryVersion: NotRequired[str]
    percents: NotRequired[Sequence[float]]


class PercentPairTypeDef(TypedDict):
    percent: NotRequired[float]
    value: NotRequired[float]


class GetPolicyRequestTypeDef(TypedDict):
    policyName: str


class GetPolicyVersionRequestTypeDef(TypedDict):
    policyName: str
    policyVersionId: str


class GetStatisticsRequestTypeDef(TypedDict):
    queryString: str
    indexName: NotRequired[str]
    aggregationField: NotRequired[str]
    queryVersion: NotRequired[str]


StatisticsTypeDef = TypedDict(
    "StatisticsTypeDef",
    {
        "count": NotRequired[int],
        "average": NotRequired[float],
        "sum": NotRequired[float],
        "minimum": NotRequired[float],
        "maximum": NotRequired[float],
        "sumOfSquares": NotRequired[float],
        "variance": NotRequired[float],
        "stdDeviation": NotRequired[float],
    },
)


class GetThingConnectivityDataRequestTypeDef(TypedDict):
    thingName: str


class GetTopicRuleDestinationRequestTypeDef(TypedDict):
    arn: str


class GetTopicRuleRequestTypeDef(TypedDict):
    ruleName: str


class GroupNameAndArnTypeDef(TypedDict):
    groupName: NotRequired[str]
    groupArn: NotRequired[str]


class HttpActionHeaderTypeDef(TypedDict):
    key: str
    value: str


class SigV4AuthorizationTypeDef(TypedDict):
    signingRegion: str
    serviceName: str
    roleArn: str


class HttpContextTypeDef(TypedDict):
    headers: NotRequired[Mapping[str, str]]
    queryString: NotRequired[str]


class HttpUrlDestinationConfigurationTypeDef(TypedDict):
    confirmationUrl: str


class HttpUrlDestinationPropertiesTypeDef(TypedDict):
    confirmationUrl: NotRequired[str]


class HttpUrlDestinationSummaryTypeDef(TypedDict):
    confirmationUrl: NotRequired[str]


class IssuerCertificateIdentifierTypeDef(TypedDict):
    issuerCertificateSubject: NotRequired[str]
    issuerId: NotRequired[str]
    issuerCertificateSerialNumber: NotRequired[str]


class JobExecutionStatusDetailsTypeDef(TypedDict):
    detailsMap: NotRequired[Dict[str, str]]


class JobExecutionSummaryTypeDef(TypedDict):
    status: NotRequired[JobExecutionStatusType]
    queuedAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    executionNumber: NotRequired[int]
    retryAttempt: NotRequired[int]


class RetryCriteriaTypeDef(TypedDict):
    failureType: RetryableFailureTypeType
    numberOfRetries: int


class JobProcessDetailsTypeDef(TypedDict):
    processingTargets: NotRequired[List[str]]
    numberOfCanceledThings: NotRequired[int]
    numberOfSucceededThings: NotRequired[int]
    numberOfFailedThings: NotRequired[int]
    numberOfRejectedThings: NotRequired[int]
    numberOfQueuedThings: NotRequired[int]
    numberOfInProgressThings: NotRequired[int]
    numberOfRemovedThings: NotRequired[int]
    numberOfTimedOutThings: NotRequired[int]


class JobSummaryTypeDef(TypedDict):
    jobArn: NotRequired[str]
    jobId: NotRequired[str]
    thingGroupId: NotRequired[str]
    targetSelection: NotRequired[TargetSelectionType]
    status: NotRequired[JobStatusType]
    createdAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    completedAt: NotRequired[datetime]
    isConcurrent: NotRequired[bool]


class JobTemplateSummaryTypeDef(TypedDict):
    jobTemplateArn: NotRequired[str]
    jobTemplateId: NotRequired[str]
    description: NotRequired[str]
    createdAt: NotRequired[datetime]


class ScheduledJobRolloutTypeDef(TypedDict):
    startTime: NotRequired[str]


class KafkaActionHeaderTypeDef(TypedDict):
    key: str
    value: str


class ListActiveViolationsRequestTypeDef(TypedDict):
    thingName: NotRequired[str]
    securityProfileName: NotRequired[str]
    behaviorCriteriaType: NotRequired[BehaviorCriteriaTypeType]
    listSuppressedAlerts: NotRequired[bool]
    verificationState: NotRequired[VerificationStateType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAttachedPoliciesRequestTypeDef(TypedDict):
    target: str
    recursive: NotRequired[bool]
    marker: NotRequired[str]
    pageSize: NotRequired[int]


class ListAuditMitigationActionsExecutionsRequestTypeDef(TypedDict):
    taskId: str
    findingId: str
    actionStatus: NotRequired[AuditMitigationActionsExecutionStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAuthorizersRequestTypeDef(TypedDict):
    pageSize: NotRequired[int]
    marker: NotRequired[str]
    ascendingOrder: NotRequired[bool]
    status: NotRequired[AuthorizerStatusType]


class ListBillingGroupsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    namePrefixFilter: NotRequired[str]


class ListCACertificatesRequestTypeDef(TypedDict):
    pageSize: NotRequired[int]
    marker: NotRequired[str]
    ascendingOrder: NotRequired[bool]
    templateName: NotRequired[str]


class ListCertificateProvidersRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    ascendingOrder: NotRequired[bool]


class ListCertificatesByCARequestTypeDef(TypedDict):
    caCertificateId: str
    pageSize: NotRequired[int]
    marker: NotRequired[str]
    ascendingOrder: NotRequired[bool]


class ListCertificatesRequestTypeDef(TypedDict):
    pageSize: NotRequired[int]
    marker: NotRequired[str]
    ascendingOrder: NotRequired[bool]


class TimeFilterTypeDef(TypedDict):
    after: NotRequired[str]
    before: NotRequired[str]


class ListCommandsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    namespace: NotRequired[CommandNamespaceType]
    commandParameterName: NotRequired[str]
    sortOrder: NotRequired[SortOrderType]


class ListCustomMetricsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDimensionsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDomainConfigurationsRequestTypeDef(TypedDict):
    marker: NotRequired[str]
    pageSize: NotRequired[int]
    serviceType: NotRequired[ServiceTypeType]


class ListFleetMetricsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListIndicesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListJobExecutionsForJobRequestTypeDef(TypedDict):
    jobId: str
    status: NotRequired[JobExecutionStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListJobExecutionsForThingRequestTypeDef(TypedDict):
    thingName: str
    status: NotRequired[JobExecutionStatusType]
    namespaceId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    jobId: NotRequired[str]


class ListJobTemplatesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListJobsRequestTypeDef(TypedDict):
    status: NotRequired[JobStatusType]
    targetSelection: NotRequired[TargetSelectionType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    thingGroupName: NotRequired[str]
    thingGroupId: NotRequired[str]
    namespaceId: NotRequired[str]


class ListManagedJobTemplatesRequestTypeDef(TypedDict):
    templateName: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ManagedJobTemplateSummaryTypeDef(TypedDict):
    templateArn: NotRequired[str]
    templateName: NotRequired[str]
    description: NotRequired[str]
    environments: NotRequired[List[str]]
    templateVersion: NotRequired[str]


class ListMitigationActionsRequestTypeDef(TypedDict):
    actionType: NotRequired[MitigationActionTypeType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class MitigationActionIdentifierTypeDef(TypedDict):
    actionName: NotRequired[str]
    actionArn: NotRequired[str]
    creationDate: NotRequired[datetime]


class ListOTAUpdatesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    otaUpdateStatus: NotRequired[OTAUpdateStatusType]


class OTAUpdateSummaryTypeDef(TypedDict):
    otaUpdateId: NotRequired[str]
    otaUpdateArn: NotRequired[str]
    creationDate: NotRequired[datetime]


class ListOutgoingCertificatesRequestTypeDef(TypedDict):
    pageSize: NotRequired[int]
    marker: NotRequired[str]
    ascendingOrder: NotRequired[bool]


class OutgoingCertificateTypeDef(TypedDict):
    certificateArn: NotRequired[str]
    certificateId: NotRequired[str]
    transferredTo: NotRequired[str]
    transferDate: NotRequired[datetime]
    transferMessage: NotRequired[str]
    creationDate: NotRequired[datetime]


class ListPackageVersionsRequestTypeDef(TypedDict):
    packageName: str
    status: NotRequired[PackageVersionStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class PackageVersionSummaryTypeDef(TypedDict):
    packageName: NotRequired[str]
    versionName: NotRequired[str]
    status: NotRequired[PackageVersionStatusType]
    creationDate: NotRequired[datetime]
    lastModifiedDate: NotRequired[datetime]


class ListPackagesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class PackageSummaryTypeDef(TypedDict):
    packageName: NotRequired[str]
    defaultVersionName: NotRequired[str]
    creationDate: NotRequired[datetime]
    lastModifiedDate: NotRequired[datetime]


class ListPoliciesRequestTypeDef(TypedDict):
    marker: NotRequired[str]
    pageSize: NotRequired[int]
    ascendingOrder: NotRequired[bool]


class ListPolicyPrincipalsRequestTypeDef(TypedDict):
    policyName: str
    marker: NotRequired[str]
    pageSize: NotRequired[int]
    ascendingOrder: NotRequired[bool]


class ListPolicyVersionsRequestTypeDef(TypedDict):
    policyName: str


class PolicyVersionTypeDef(TypedDict):
    versionId: NotRequired[str]
    isDefaultVersion: NotRequired[bool]
    createDate: NotRequired[datetime]


class ListPrincipalPoliciesRequestTypeDef(TypedDict):
    principal: str
    marker: NotRequired[str]
    pageSize: NotRequired[int]
    ascendingOrder: NotRequired[bool]


class ListPrincipalThingsRequestTypeDef(TypedDict):
    principal: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListPrincipalThingsV2RequestTypeDef(TypedDict):
    principal: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    thingPrincipalType: NotRequired[ThingPrincipalTypeType]


class PrincipalThingObjectTypeDef(TypedDict):
    thingName: str
    thingPrincipalType: NotRequired[ThingPrincipalTypeType]


class ListProvisioningTemplateVersionsRequestTypeDef(TypedDict):
    templateName: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ProvisioningTemplateVersionSummaryTypeDef(TypedDict):
    versionId: NotRequired[int]
    creationDate: NotRequired[datetime]
    isDefaultVersion: NotRequired[bool]


class ListProvisioningTemplatesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


ProvisioningTemplateSummaryTypeDef = TypedDict(
    "ProvisioningTemplateSummaryTypeDef",
    {
        "templateArn": NotRequired[str],
        "templateName": NotRequired[str],
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastModifiedDate": NotRequired[datetime],
        "enabled": NotRequired[bool],
        "type": NotRequired[TemplateTypeType],
    },
)


class ListRelatedResourcesForAuditFindingRequestTypeDef(TypedDict):
    findingId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListRoleAliasesRequestTypeDef(TypedDict):
    pageSize: NotRequired[int]
    marker: NotRequired[str]
    ascendingOrder: NotRequired[bool]


class ListSbomValidationResultsRequestTypeDef(TypedDict):
    packageName: str
    versionName: str
    validationResult: NotRequired[SbomValidationResultType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SbomValidationResultSummaryTypeDef(TypedDict):
    fileName: NotRequired[str]
    validationResult: NotRequired[SbomValidationResultType]
    errorCode: NotRequired[SbomValidationErrorCodeType]
    errorMessage: NotRequired[str]


class ListScheduledAuditsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ScheduledAuditMetadataTypeDef(TypedDict):
    scheduledAuditName: NotRequired[str]
    scheduledAuditArn: NotRequired[str]
    frequency: NotRequired[AuditFrequencyType]
    dayOfMonth: NotRequired[str]
    dayOfWeek: NotRequired[DayOfWeekType]


class ListSecurityProfilesForTargetRequestTypeDef(TypedDict):
    securityProfileTargetArn: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    recursive: NotRequired[bool]


class ListSecurityProfilesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    dimensionName: NotRequired[str]
    metricName: NotRequired[str]


class SecurityProfileIdentifierTypeDef(TypedDict):
    name: str
    arn: str


class ListStreamsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    ascendingOrder: NotRequired[bool]


class StreamSummaryTypeDef(TypedDict):
    streamId: NotRequired[str]
    streamArn: NotRequired[str]
    streamVersion: NotRequired[int]
    description: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str
    nextToken: NotRequired[str]


class ListTargetsForPolicyRequestTypeDef(TypedDict):
    policyName: str
    marker: NotRequired[str]
    pageSize: NotRequired[int]


class ListTargetsForSecurityProfileRequestTypeDef(TypedDict):
    securityProfileName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class SecurityProfileTargetTypeDef(TypedDict):
    arn: str


class ListThingGroupsForThingRequestTypeDef(TypedDict):
    thingName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListThingGroupsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    parentGroup: NotRequired[str]
    namePrefixFilter: NotRequired[str]
    recursive: NotRequired[bool]


class ListThingPrincipalsRequestTypeDef(TypedDict):
    thingName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListThingPrincipalsV2RequestTypeDef(TypedDict):
    thingName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    thingPrincipalType: NotRequired[ThingPrincipalTypeType]


class ThingPrincipalObjectTypeDef(TypedDict):
    principal: str
    thingPrincipalType: NotRequired[ThingPrincipalTypeType]


class ListThingRegistrationTaskReportsRequestTypeDef(TypedDict):
    taskId: str
    reportType: ReportTypeType
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListThingRegistrationTasksRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    status: NotRequired[StatusType]


class ListThingTypesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    thingTypeName: NotRequired[str]


class ListThingsInBillingGroupRequestTypeDef(TypedDict):
    billingGroupName: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListThingsInThingGroupRequestTypeDef(TypedDict):
    thingGroupName: str
    recursive: NotRequired[bool]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListThingsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    attributeName: NotRequired[str]
    attributeValue: NotRequired[str]
    thingTypeName: NotRequired[str]
    usePrefixAttributeValue: NotRequired[bool]


class ThingAttributeTypeDef(TypedDict):
    thingName: NotRequired[str]
    thingTypeName: NotRequired[str]
    thingArn: NotRequired[str]
    attributes: NotRequired[Dict[str, str]]
    version: NotRequired[int]


class ListTopicRuleDestinationsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTopicRulesRequestTypeDef(TypedDict):
    topic: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    ruleDisabled: NotRequired[bool]


class TopicRuleListItemTypeDef(TypedDict):
    ruleArn: NotRequired[str]
    ruleName: NotRequired[str]
    topicPattern: NotRequired[str]
    createdAt: NotRequired[datetime]
    ruleDisabled: NotRequired[bool]


class ListV2LoggingLevelsRequestTypeDef(TypedDict):
    targetType: NotRequired[LogTargetTypeType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class LocationTimestampTypeDef(TypedDict):
    value: str
    unit: NotRequired[str]


class LogTargetTypeDef(TypedDict):
    targetType: LogTargetTypeType
    targetName: NotRequired[str]


class LoggingOptionsPayloadTypeDef(TypedDict):
    roleArn: str
    logLevel: NotRequired[LogLevelType]


class MetricValueTypeDef(TypedDict):
    count: NotRequired[int]
    cidrs: NotRequired[Sequence[str]]
    ports: NotRequired[Sequence[int]]
    number: NotRequired[float]
    numbers: NotRequired[Sequence[float]]
    strings: NotRequired[Sequence[str]]


class PublishFindingToSnsParamsTypeDef(TypedDict):
    topicArn: str


class ReplaceDefaultPolicyVersionParamsTypeDef(TypedDict):
    templateName: Literal["BLANK_POLICY"]


class UpdateCACertificateParamsTypeDef(TypedDict):
    action: Literal["DEACTIVATE"]


class UpdateDeviceCertificateParamsTypeDef(TypedDict):
    action: Literal["DEACTIVATE"]


class PropagatingAttributeTypeDef(TypedDict):
    userPropertyKey: NotRequired[str]
    thingAttribute: NotRequired[str]
    connectionAttribute: NotRequired[str]


class UserPropertyTypeDef(TypedDict):
    key: str
    value: str


class PolicyVersionIdentifierTypeDef(TypedDict):
    policyName: NotRequired[str]
    policyVersionId: NotRequired[str]


class PutVerificationStateOnViolationRequestTypeDef(TypedDict):
    violationId: str
    verificationState: VerificationStateType
    verificationStateDescription: NotRequired[str]


class RegisterCertificateRequestTypeDef(TypedDict):
    certificatePem: str
    caCertificatePem: NotRequired[str]
    setAsActive: NotRequired[bool]
    status: NotRequired[CertificateStatusType]


class RegisterCertificateWithoutCARequestTypeDef(TypedDict):
    certificatePem: str
    status: NotRequired[CertificateStatusType]


class RegisterThingRequestTypeDef(TypedDict):
    templateBody: str
    parameters: NotRequired[Mapping[str, str]]


class RejectCertificateTransferRequestTypeDef(TypedDict):
    certificateId: str
    rejectReason: NotRequired[str]


class RemoveThingFromBillingGroupRequestTypeDef(TypedDict):
    billingGroupName: NotRequired[str]
    billingGroupArn: NotRequired[str]
    thingName: NotRequired[str]
    thingArn: NotRequired[str]


class RemoveThingFromThingGroupRequestTypeDef(TypedDict):
    thingGroupName: NotRequired[str]
    thingGroupArn: NotRequired[str]
    thingName: NotRequired[str]
    thingArn: NotRequired[str]


class SearchIndexRequestTypeDef(TypedDict):
    queryString: str
    indexName: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    queryVersion: NotRequired[str]


class ThingGroupDocumentTypeDef(TypedDict):
    thingGroupName: NotRequired[str]
    thingGroupId: NotRequired[str]
    thingGroupDescription: NotRequired[str]
    attributes: NotRequired[Dict[str, str]]
    parentGroupNames: NotRequired[List[str]]


class SetDefaultAuthorizerRequestTypeDef(TypedDict):
    authorizerName: str


class SetDefaultPolicyVersionRequestTypeDef(TypedDict):
    policyName: str
    policyVersionId: str


class SetV2LoggingOptionsRequestTypeDef(TypedDict):
    roleArn: NotRequired[str]
    defaultLogLevel: NotRequired[LogLevelType]
    disableAllLogs: NotRequired[bool]


class SigningProfileParameterTypeDef(TypedDict):
    certificateArn: NotRequired[str]
    platform: NotRequired[str]
    certificatePathOnDevice: NotRequired[str]


class StartOnDemandAuditTaskRequestTypeDef(TypedDict):
    targetCheckNames: Sequence[str]


class StartThingRegistrationTaskRequestTypeDef(TypedDict):
    templateBody: str
    inputFileBucket: str
    inputFileKey: str
    roleArn: str


class StopThingRegistrationTaskRequestTypeDef(TypedDict):
    taskId: str


class TlsContextTypeDef(TypedDict):
    serverName: NotRequired[str]


class ThingConnectivityTypeDef(TypedDict):
    connected: NotRequired[bool]
    timestamp: NotRequired[int]
    disconnectReason: NotRequired[str]


class TimestreamDimensionTypeDef(TypedDict):
    name: str
    value: str


class TimestreamTimestampTypeDef(TypedDict):
    value: str
    unit: str


class VpcDestinationConfigurationTypeDef(TypedDict):
    subnetIds: Sequence[str]
    vpcId: str
    roleArn: str
    securityGroups: NotRequired[Sequence[str]]


class VpcDestinationSummaryTypeDef(TypedDict):
    subnetIds: NotRequired[List[str]]
    securityGroups: NotRequired[List[str]]
    vpcId: NotRequired[str]
    roleArn: NotRequired[str]


class VpcDestinationPropertiesTypeDef(TypedDict):
    subnetIds: NotRequired[List[str]]
    securityGroups: NotRequired[List[str]]
    vpcId: NotRequired[str]
    roleArn: NotRequired[str]


class TransferCertificateRequestTypeDef(TypedDict):
    certificateId: str
    targetAwsAccount: str
    transferMessage: NotRequired[str]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateAuthorizerRequestTypeDef(TypedDict):
    authorizerName: str
    authorizerFunctionArn: NotRequired[str]
    tokenKeyName: NotRequired[str]
    tokenSigningPublicKeys: NotRequired[Mapping[str, str]]
    status: NotRequired[AuthorizerStatusType]
    enableCachingForHttp: NotRequired[bool]


class UpdateCertificateProviderRequestTypeDef(TypedDict):
    certificateProviderName: str
    lambdaFunctionArn: NotRequired[str]
    accountDefaultForOperations: NotRequired[Sequence[Literal["CreateCertificateFromCsr"]]]


class UpdateCertificateRequestTypeDef(TypedDict):
    certificateId: str
    newStatus: CertificateStatusType


class UpdateCommandRequestTypeDef(TypedDict):
    commandId: str
    displayName: NotRequired[str]
    description: NotRequired[str]
    deprecated: NotRequired[bool]


class UpdateCustomMetricRequestTypeDef(TypedDict):
    metricName: str
    displayName: str


class UpdateDimensionRequestTypeDef(TypedDict):
    name: str
    stringValues: Sequence[str]


class UpdatePackageRequestTypeDef(TypedDict):
    packageName: str
    description: NotRequired[str]
    defaultVersionName: NotRequired[str]
    unsetDefaultVersion: NotRequired[bool]
    clientToken: NotRequired[str]


class UpdateRoleAliasRequestTypeDef(TypedDict):
    roleAlias: str
    roleArn: NotRequired[str]
    credentialDurationSeconds: NotRequired[int]


class UpdateScheduledAuditRequestTypeDef(TypedDict):
    scheduledAuditName: str
    frequency: NotRequired[AuditFrequencyType]
    dayOfMonth: NotRequired[str]
    dayOfWeek: NotRequired[DayOfWeekType]
    targetCheckNames: NotRequired[Sequence[str]]


class UpdateThingGroupsForThingRequestTypeDef(TypedDict):
    thingName: NotRequired[str]
    thingGroupsToAdd: NotRequired[Sequence[str]]
    thingGroupsToRemove: NotRequired[Sequence[str]]
    overrideDynamicGroups: NotRequired[bool]


class UpdateTopicRuleDestinationRequestTypeDef(TypedDict):
    arn: str
    status: TopicRuleDestinationStatusType


class ValidationErrorTypeDef(TypedDict):
    errorMessage: NotRequired[str]


class AbortConfigOutputTypeDef(TypedDict):
    criteriaList: List[AbortCriteriaTypeDef]


class AbortConfigTypeDef(TypedDict):
    criteriaList: Sequence[AbortCriteriaTypeDef]


class MetricDatumTypeDef(TypedDict):
    timestamp: NotRequired[datetime]
    value: NotRequired[MetricValueOutputTypeDef]


AggregationTypeUnionTypeDef = Union[AggregationTypeTypeDef, AggregationTypeOutputTypeDef]


class AllowedTypeDef(TypedDict):
    policies: NotRequired[List[PolicyTypeDef]]


class ExplicitDenyTypeDef(TypedDict):
    policies: NotRequired[List[PolicyTypeDef]]


class ImplicitDenyTypeDef(TypedDict):
    policies: NotRequired[List[PolicyTypeDef]]


class AssetPropertyValueTypeDef(TypedDict):
    value: AssetPropertyVariantTypeDef
    timestamp: AssetPropertyTimestampTypeDef
    quality: NotRequired[str]


class AssociateTargetsWithJobResponseTypeDef(TypedDict):
    jobArn: str
    jobId: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class CancelJobResponseTypeDef(TypedDict):
    jobArn: str
    jobId: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAuthorizerResponseTypeDef(TypedDict):
    authorizerName: str
    authorizerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateBillingGroupResponseTypeDef(TypedDict):
    billingGroupName: str
    billingGroupArn: str
    billingGroupId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCertificateFromCsrResponseTypeDef(TypedDict):
    certificateArn: str
    certificateId: str
    certificatePem: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCertificateProviderResponseTypeDef(TypedDict):
    certificateProviderName: str
    certificateProviderArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCommandResponseTypeDef(TypedDict):
    commandId: str
    commandArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateCustomMetricResponseTypeDef(TypedDict):
    metricName: str
    metricArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDimensionResponseTypeDef(TypedDict):
    name: str
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDomainConfigurationResponseTypeDef(TypedDict):
    domainConfigurationName: str
    domainConfigurationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDynamicThingGroupResponseTypeDef(TypedDict):
    thingGroupName: str
    thingGroupArn: str
    thingGroupId: str
    indexName: str
    queryString: str
    queryVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFleetMetricResponseTypeDef(TypedDict):
    metricName: str
    metricArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateJobResponseTypeDef(TypedDict):
    jobArn: str
    jobId: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateJobTemplateResponseTypeDef(TypedDict):
    jobTemplateArn: str
    jobTemplateId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMitigationActionResponseTypeDef(TypedDict):
    actionArn: str
    actionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateOTAUpdateResponseTypeDef(TypedDict):
    otaUpdateId: str
    awsIotJobId: str
    otaUpdateArn: str
    awsIotJobArn: str
    otaUpdateStatus: OTAUpdateStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePackageResponseTypeDef(TypedDict):
    packageName: str
    packageArn: str
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePackageVersionResponseTypeDef(TypedDict):
    packageVersionArn: str
    packageName: str
    versionName: str
    description: str
    attributes: Dict[str, str]
    status: PackageVersionStatusType
    errorReason: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePolicyResponseTypeDef(TypedDict):
    policyName: str
    policyArn: str
    policyDocument: str
    policyVersionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreatePolicyVersionResponseTypeDef(TypedDict):
    policyArn: str
    policyDocument: str
    policyVersionId: str
    isDefaultVersion: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProvisioningTemplateResponseTypeDef(TypedDict):
    templateArn: str
    templateName: str
    defaultVersionId: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProvisioningTemplateVersionResponseTypeDef(TypedDict):
    templateArn: str
    templateName: str
    versionId: int
    isDefaultVersion: bool
    ResponseMetadata: ResponseMetadataTypeDef


class CreateRoleAliasResponseTypeDef(TypedDict):
    roleAlias: str
    roleAliasArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateScheduledAuditResponseTypeDef(TypedDict):
    scheduledAuditArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSecurityProfileResponseTypeDef(TypedDict):
    securityProfileName: str
    securityProfileArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamResponseTypeDef(TypedDict):
    streamId: str
    streamArn: str
    description: str
    streamVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class CreateThingGroupResponseTypeDef(TypedDict):
    thingGroupName: str
    thingGroupArn: str
    thingGroupId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateThingResponseTypeDef(TypedDict):
    thingName: str
    thingArn: str
    thingId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateThingTypeResponseTypeDef(TypedDict):
    thingTypeName: str
    thingTypeArn: str
    thingTypeId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCommandResponseTypeDef(TypedDict):
    statusCode: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCertificateProviderResponseTypeDef(TypedDict):
    certificateProviderName: str
    certificateProviderArn: str
    lambdaFunctionArn: str
    accountDefaultForOperations: List[Literal["CreateCertificateFromCsr"]]
    creationDate: datetime
    lastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCustomMetricResponseTypeDef(TypedDict):
    metricName: str
    metricArn: str
    metricType: CustomMetricTypeType
    displayName: str
    creationDate: datetime
    lastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


DescribeDimensionResponseTypeDef = TypedDict(
    "DescribeDimensionResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "type": Literal["TOPIC_FILTER"],
        "stringValues": List[str],
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DescribeEndpointResponseTypeDef(TypedDict):
    endpointAddress: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFleetMetricResponseTypeDef(TypedDict):
    metricName: str
    queryString: str
    aggregationType: AggregationTypeOutputTypeDef
    period: int
    aggregationField: str
    description: str
    queryVersion: str
    indexName: str
    creationDate: datetime
    lastModifiedDate: datetime
    unit: FleetMetricUnitType
    version: int
    metricArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeIndexResponseTypeDef(TypedDict):
    indexName: str
    indexStatus: IndexStatusType
    schema: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeProvisioningTemplateVersionResponseTypeDef(TypedDict):
    versionId: int
    creationDate: datetime
    templateBody: str
    isDefaultVersion: bool
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeScheduledAuditResponseTypeDef(TypedDict):
    frequency: AuditFrequencyType
    dayOfMonth: str
    dayOfWeek: DayOfWeekType
    targetCheckNames: List[str]
    scheduledAuditName: str
    scheduledAuditArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeThingRegistrationTaskResponseTypeDef(TypedDict):
    taskId: str
    creationDate: datetime
    lastModifiedDate: datetime
    templateBody: str
    inputFileBucket: str
    inputFileKey: str
    roleArn: str
    status: StatusType
    message: str
    successCount: int
    failureCount: int
    percentageProgress: int
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeThingResponseTypeDef(TypedDict):
    defaultClientId: str
    thingName: str
    thingId: str
    thingArn: str
    thingTypeName: str
    attributes: Dict[str, str]
    version: int
    billingGroupName: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetCardinalityResponseTypeDef(TypedDict):
    cardinality: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetJobDocumentResponseTypeDef(TypedDict):
    document: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetLoggingOptionsResponseTypeDef(TypedDict):
    roleArn: str
    logLevel: LogLevelType
    ResponseMetadata: ResponseMetadataTypeDef


class GetPackageResponseTypeDef(TypedDict):
    packageName: str
    packageArn: str
    description: str
    defaultVersionName: str
    creationDate: datetime
    lastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetPolicyResponseTypeDef(TypedDict):
    policyName: str
    policyArn: str
    policyDocument: str
    defaultVersionId: str
    creationDate: datetime
    lastModifiedDate: datetime
    generationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetPolicyVersionResponseTypeDef(TypedDict):
    policyArn: str
    policyName: str
    policyDocument: str
    policyVersionId: str
    isDefaultVersion: bool
    creationDate: datetime
    lastModifiedDate: datetime
    generationId: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRegistrationCodeResponseTypeDef(TypedDict):
    registrationCode: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetThingConnectivityDataResponseTypeDef(TypedDict):
    thingName: str
    connected: bool
    timestamp: datetime
    disconnectReason: DisconnectReasonValueType
    ResponseMetadata: ResponseMetadataTypeDef


class GetV2LoggingOptionsResponseTypeDef(TypedDict):
    roleArn: str
    defaultLogLevel: LogLevelType
    disableAllLogs: bool
    ResponseMetadata: ResponseMetadataTypeDef


class ListAttachedPoliciesResponseTypeDef(TypedDict):
    policies: List[PolicyTypeDef]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListCustomMetricsResponseTypeDef(TypedDict):
    metricNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDimensionsResponseTypeDef(TypedDict):
    dimensionNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListIndicesResponseTypeDef(TypedDict):
    indexNames: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPoliciesResponseTypeDef(TypedDict):
    policies: List[PolicyTypeDef]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListPolicyPrincipalsResponseTypeDef(TypedDict):
    principals: List[str]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListPrincipalPoliciesResponseTypeDef(TypedDict):
    policies: List[PolicyTypeDef]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListPrincipalThingsResponseTypeDef(TypedDict):
    things: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListRoleAliasesResponseTypeDef(TypedDict):
    roleAliases: List[str]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTargetsForPolicyResponseTypeDef(TypedDict):
    targets: List[str]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListThingPrincipalsResponseTypeDef(TypedDict):
    principals: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListThingRegistrationTaskReportsResponseTypeDef(TypedDict):
    resourceLinks: List[str]
    reportType: ReportTypeType
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListThingRegistrationTasksResponseTypeDef(TypedDict):
    taskIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListThingsInBillingGroupResponseTypeDef(TypedDict):
    things: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListThingsInThingGroupResponseTypeDef(TypedDict):
    things: List[str]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RegisterCACertificateResponseTypeDef(TypedDict):
    certificateArn: str
    certificateId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterCertificateResponseTypeDef(TypedDict):
    certificateArn: str
    certificateId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterCertificateWithoutCAResponseTypeDef(TypedDict):
    certificateArn: str
    certificateId: str
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterThingResponseTypeDef(TypedDict):
    certificatePem: str
    resourceArns: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class SetDefaultAuthorizerResponseTypeDef(TypedDict):
    authorizerName: str
    authorizerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartAuditMitigationActionsTaskResponseTypeDef(TypedDict):
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartDetectMitigationActionsTaskResponseTypeDef(TypedDict):
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartOnDemandAuditTaskResponseTypeDef(TypedDict):
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartThingRegistrationTaskResponseTypeDef(TypedDict):
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class TestInvokeAuthorizerResponseTypeDef(TypedDict):
    isAuthenticated: bool
    principalId: str
    policyDocuments: List[str]
    refreshAfterInSeconds: int
    disconnectAfterInSeconds: int
    ResponseMetadata: ResponseMetadataTypeDef


class TransferCertificateResponseTypeDef(TypedDict):
    transferredCertificateArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAuthorizerResponseTypeDef(TypedDict):
    authorizerName: str
    authorizerArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBillingGroupResponseTypeDef(TypedDict):
    version: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCertificateProviderResponseTypeDef(TypedDict):
    certificateProviderName: str
    certificateProviderArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCommandResponseTypeDef(TypedDict):
    commandId: str
    displayName: str
    description: str
    deprecated: bool
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateCustomMetricResponseTypeDef(TypedDict):
    metricName: str
    metricArn: str
    metricType: CustomMetricTypeType
    displayName: str
    creationDate: datetime
    lastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


UpdateDimensionResponseTypeDef = TypedDict(
    "UpdateDimensionResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "type": Literal["TOPIC_FILTER"],
        "stringValues": List[str],
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdateDomainConfigurationResponseTypeDef(TypedDict):
    domainConfigurationName: str
    domainConfigurationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateDynamicThingGroupResponseTypeDef(TypedDict):
    version: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMitigationActionResponseTypeDef(TypedDict):
    actionArn: str
    actionId: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRoleAliasResponseTypeDef(TypedDict):
    roleAlias: str
    roleAliasArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateScheduledAuditResponseTypeDef(TypedDict):
    scheduledAuditArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateStreamResponseTypeDef(TypedDict):
    streamId: str
    streamArn: str
    description: str
    streamVersion: int
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateThingGroupResponseTypeDef(TypedDict):
    version: int
    ResponseMetadata: ResponseMetadataTypeDef


class ThingGroupPropertiesOutputTypeDef(TypedDict):
    thingGroupDescription: NotRequired[str]
    attributePayload: NotRequired[AttributePayloadOutputTypeDef]


AttributePayloadUnionTypeDef = Union[AttributePayloadTypeDef, AttributePayloadOutputTypeDef]


class ThingGroupPropertiesTypeDef(TypedDict):
    thingGroupDescription: NotRequired[str]
    attributePayload: NotRequired[AttributePayloadTypeDef]


AuditCheckConfigurationUnionTypeDef = Union[
    AuditCheckConfigurationTypeDef, AuditCheckConfigurationOutputTypeDef
]


class ListAuditMitigationActionsExecutionsResponseTypeDef(TypedDict):
    actionsExecutions: List[AuditMitigationActionExecutionMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAuditMitigationActionsTasksResponseTypeDef(TypedDict):
    tasks: List[AuditMitigationActionsTaskMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AuditMitigationActionsTaskTargetUnionTypeDef = Union[
    AuditMitigationActionsTaskTargetTypeDef, AuditMitigationActionsTaskTargetOutputTypeDef
]


class DescribeAccountAuditConfigurationResponseTypeDef(TypedDict):
    roleArn: str
    auditNotificationTargetConfigurations: Dict[Literal["SNS"], AuditNotificationTargetTypeDef]
    auditCheckConfigurations: Dict[str, AuditCheckConfigurationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListAuditTasksResponseTypeDef(TypedDict):
    tasks: List[AuditTaskMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


AuthInfoUnionTypeDef = Union[AuthInfoTypeDef, AuthInfoOutputTypeDef]


class DescribeAuthorizerResponseTypeDef(TypedDict):
    authorizerDescription: AuthorizerDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDefaultAuthorizerResponseTypeDef(TypedDict):
    authorizerDescription: AuthorizerDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAuthorizersResponseTypeDef(TypedDict):
    authorizers: List[AuthorizerSummaryTypeDef]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class AwsJobAbortConfigTypeDef(TypedDict):
    abortCriteriaList: Sequence[AwsJobAbortCriteriaTypeDef]


class AwsJobExponentialRolloutRateTypeDef(TypedDict):
    baseRatePerMinute: int
    incrementFactor: float
    rateIncreaseCriteria: AwsJobRateIncreaseCriteriaTypeDef


class BehaviorCriteriaOutputTypeDef(TypedDict):
    comparisonOperator: NotRequired[ComparisonOperatorType]
    value: NotRequired[MetricValueOutputTypeDef]
    durationSeconds: NotRequired[int]
    consecutiveDatapointsToAlarm: NotRequired[int]
    consecutiveDatapointsToClear: NotRequired[int]
    statisticalThreshold: NotRequired[StatisticalThresholdTypeDef]
    mlDetectionConfig: NotRequired[MachineLearningDetectionConfigTypeDef]


class GetBehaviorModelTrainingSummariesResponseTypeDef(TypedDict):
    summaries: List[BehaviorModelTrainingSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class MetricToRetainTypeDef(TypedDict):
    metric: str
    metricDimension: NotRequired[MetricDimensionTypeDef]
    exportMetric: NotRequired[bool]


class DescribeBillingGroupResponseTypeDef(TypedDict):
    billingGroupName: str
    billingGroupId: str
    billingGroupArn: str
    version: int
    billingGroupProperties: BillingGroupPropertiesTypeDef
    billingGroupMetadata: BillingGroupMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBillingGroupRequestTypeDef(TypedDict):
    billingGroupName: str
    billingGroupProperties: BillingGroupPropertiesTypeDef
    expectedVersion: NotRequired[int]


class CodeSigningSignatureTypeDef(TypedDict):
    inlineDocument: NotRequired[BlobTypeDef]


class CommandParameterValueTypeDef(TypedDict):
    S: NotRequired[str]
    B: NotRequired[bool]
    I: NotRequired[int]
    L: NotRequired[int]
    D: NotRequired[float]
    BIN: NotRequired[BlobTypeDef]
    UL: NotRequired[str]


class CommandPayloadTypeDef(TypedDict):
    content: NotRequired[BlobTypeDef]
    contentType: NotRequired[str]


class MqttContextTypeDef(TypedDict):
    username: NotRequired[str]
    password: NotRequired[BlobTypeDef]
    clientId: NotRequired[str]


class GetBucketsAggregationResponseTypeDef(TypedDict):
    totalCount: int
    buckets: List[BucketTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BucketsAggregationTypeTypeDef(TypedDict):
    termsAggregation: NotRequired[TermsAggregationTypeDef]


class CACertificateDescriptionTypeDef(TypedDict):
    certificateArn: NotRequired[str]
    certificateId: NotRequired[str]
    status: NotRequired[CACertificateStatusType]
    certificatePem: NotRequired[str]
    ownedBy: NotRequired[str]
    creationDate: NotRequired[datetime]
    autoRegistrationStatus: NotRequired[AutoRegistrationStatusType]
    lastModifiedDate: NotRequired[datetime]
    customerVersion: NotRequired[int]
    generationId: NotRequired[str]
    validity: NotRequired[CertificateValidityTypeDef]
    certificateMode: NotRequired[CertificateModeType]


class ListCACertificatesResponseTypeDef(TypedDict):
    certificates: List[CACertificateTypeDef]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class CertificateDescriptionTypeDef(TypedDict):
    certificateArn: NotRequired[str]
    certificateId: NotRequired[str]
    caCertificateId: NotRequired[str]
    status: NotRequired[CertificateStatusType]
    certificatePem: NotRequired[str]
    ownedBy: NotRequired[str]
    previousOwnedBy: NotRequired[str]
    creationDate: NotRequired[datetime]
    lastModifiedDate: NotRequired[datetime]
    customerVersion: NotRequired[int]
    transferData: NotRequired[TransferDataTypeDef]
    generationId: NotRequired[str]
    validity: NotRequired[CertificateValidityTypeDef]
    certificateMode: NotRequired[CertificateModeType]


class ListCertificateProvidersResponseTypeDef(TypedDict):
    certificateProviders: List[CertificateProviderSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListCertificatesByCAResponseTypeDef(TypedDict):
    certificates: List[CertificateTypeDef]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListCertificatesResponseTypeDef(TypedDict):
    certificates: List[CertificateTypeDef]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class CustomCodeSigningOutputTypeDef(TypedDict):
    signature: NotRequired[CodeSigningSignatureOutputTypeDef]
    certificateChain: NotRequired[CodeSigningCertificateChainTypeDef]
    hashAlgorithm: NotRequired[str]
    signatureAlgorithm: NotRequired[str]


class ListCommandExecutionsResponseTypeDef(TypedDict):
    commandExecutions: List[CommandExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CommandParameterOutputTypeDef(TypedDict):
    name: str
    value: NotRequired[CommandParameterValueOutputTypeDef]
    defaultValue: NotRequired[CommandParameterValueOutputTypeDef]
    description: NotRequired[str]


class ListCommandsResponseTypeDef(TypedDict):
    commands: List[CommandSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DescribeEventConfigurationsResponseTypeDef(TypedDict):
    eventConfigurations: Dict[EventTypeType, ConfigurationTypeDef]
    creationDate: datetime
    lastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateEventConfigurationsRequestTypeDef(TypedDict):
    eventConfigurations: NotRequired[Mapping[EventTypeType, ConfigurationTypeDef]]


class ListAuditMitigationActionsTasksRequestTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    auditTaskId: NotRequired[str]
    findingId: NotRequired[str]
    taskStatus: NotRequired[AuditMitigationActionsTaskStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListAuditTasksRequestTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    taskType: NotRequired[AuditTaskTypeType]
    taskStatus: NotRequired[AuditTaskStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDetectMitigationActionsExecutionsRequestTypeDef(TypedDict):
    taskId: NotRequired[str]
    violationId: NotRequired[str]
    thingName: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListDetectMitigationActionsTasksRequestTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListMetricValuesRequestTypeDef(TypedDict):
    thingName: str
    metricName: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    dimensionName: NotRequired[str]
    dimensionValueOperator: NotRequired[DimensionValueOperatorType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListViolationEventsRequestTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    thingName: NotRequired[str]
    securityProfileName: NotRequired[str]
    behaviorCriteriaType: NotRequired[BehaviorCriteriaTypeType]
    listSuppressedAlerts: NotRequired[bool]
    verificationState: NotRequired[VerificationStateType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ViolationEventOccurrenceRangeTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef


class CreateAuthorizerRequestTypeDef(TypedDict):
    authorizerName: str
    authorizerFunctionArn: str
    tokenKeyName: NotRequired[str]
    tokenSigningPublicKeys: NotRequired[Mapping[str, str]]
    status: NotRequired[AuthorizerStatusType]
    tags: NotRequired[Sequence[TagTypeDef]]
    signingDisabled: NotRequired[bool]
    enableCachingForHttp: NotRequired[bool]


class CreateBillingGroupRequestTypeDef(TypedDict):
    billingGroupName: str
    billingGroupProperties: NotRequired[BillingGroupPropertiesTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateCertificateProviderRequestTypeDef(TypedDict):
    certificateProviderName: str
    lambdaFunctionArn: str
    accountDefaultForOperations: Sequence[Literal["CreateCertificateFromCsr"]]
    clientToken: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateCustomMetricRequestTypeDef(TypedDict):
    metricName: str
    metricType: CustomMetricTypeType
    clientRequestToken: str
    displayName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


CreateDimensionRequestTypeDef = TypedDict(
    "CreateDimensionRequestTypeDef",
    {
        "name": str,
        "type": Literal["TOPIC_FILTER"],
        "stringValues": Sequence[str],
        "clientRequestToken": str,
        "tags": NotRequired[Sequence[TagTypeDef]],
    },
)


class CreatePolicyRequestTypeDef(TypedDict):
    policyName: str
    policyDocument: str
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateRoleAliasRequestTypeDef(TypedDict):
    roleAlias: str
    roleArn: str
    credentialDurationSeconds: NotRequired[int]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateScheduledAuditRequestTypeDef(TypedDict):
    frequency: AuditFrequencyType
    targetCheckNames: Sequence[str]
    scheduledAuditName: str
    dayOfMonth: NotRequired[str]
    dayOfWeek: NotRequired[DayOfWeekType]
    tags: NotRequired[Sequence[TagTypeDef]]


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


class CreateDomainConfigurationRequestTypeDef(TypedDict):
    domainConfigurationName: str
    domainName: NotRequired[str]
    serverCertificateArns: NotRequired[Sequence[str]]
    validationCertificateArn: NotRequired[str]
    authorizerConfig: NotRequired[AuthorizerConfigTypeDef]
    serviceType: NotRequired[ServiceTypeType]
    tags: NotRequired[Sequence[TagTypeDef]]
    tlsConfig: NotRequired[TlsConfigTypeDef]
    serverCertificateConfig: NotRequired[ServerCertificateConfigTypeDef]
    authenticationType: NotRequired[AuthenticationTypeType]
    applicationProtocol: NotRequired[ApplicationProtocolType]
    clientCertificateConfig: NotRequired[ClientCertificateConfigTypeDef]


class UpdateDomainConfigurationRequestTypeDef(TypedDict):
    domainConfigurationName: str
    authorizerConfig: NotRequired[AuthorizerConfigTypeDef]
    domainConfigurationStatus: NotRequired[DomainConfigurationStatusType]
    removeAuthorizerConfig: NotRequired[bool]
    tlsConfig: NotRequired[TlsConfigTypeDef]
    serverCertificateConfig: NotRequired[ServerCertificateConfigTypeDef]
    authenticationType: NotRequired[AuthenticationTypeType]
    applicationProtocol: NotRequired[ApplicationProtocolType]
    clientCertificateConfig: NotRequired[ClientCertificateConfigTypeDef]


class SchedulingConfigOutputTypeDef(TypedDict):
    startTime: NotRequired[str]
    endTime: NotRequired[str]
    endBehavior: NotRequired[JobEndBehaviorType]
    maintenanceWindows: NotRequired[List[MaintenanceWindowTypeDef]]


class SchedulingConfigTypeDef(TypedDict):
    startTime: NotRequired[str]
    endTime: NotRequired[str]
    endBehavior: NotRequired[JobEndBehaviorType]
    maintenanceWindows: NotRequired[Sequence[MaintenanceWindowTypeDef]]


class CreateKeysAndCertificateResponseTypeDef(TypedDict):
    certificateArn: str
    certificateId: str
    certificatePem: str
    keyPair: KeyPairTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateProvisioningClaimResponseTypeDef(TypedDict):
    certificateId: str
    certificatePem: str
    keyPair: KeyPairTypeDef
    expiration: datetime
    ResponseMetadata: ResponseMetadataTypeDef


CreateProvisioningTemplateRequestTypeDef = TypedDict(
    "CreateProvisioningTemplateRequestTypeDef",
    {
        "templateName": str,
        "templateBody": str,
        "provisioningRoleArn": str,
        "description": NotRequired[str],
        "enabled": NotRequired[bool],
        "preProvisioningHook": NotRequired[ProvisioningHookTypeDef],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "type": NotRequired[TemplateTypeType],
    },
)
DescribeProvisioningTemplateResponseTypeDef = TypedDict(
    "DescribeProvisioningTemplateResponseTypeDef",
    {
        "templateArn": str,
        "templateName": str,
        "description": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "defaultVersionId": int,
        "templateBody": str,
        "enabled": bool,
        "provisioningRoleArn": str,
        "preProvisioningHook": ProvisioningHookTypeDef,
        "type": TemplateTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdateProvisioningTemplateRequestTypeDef(TypedDict):
    templateName: str
    description: NotRequired[str]
    enabled: NotRequired[bool]
    defaultVersionId: NotRequired[int]
    provisioningRoleArn: NotRequired[str]
    preProvisioningHook: NotRequired[ProvisioningHookTypeDef]
    removePreProvisioningHook: NotRequired[bool]


class DescribeAuditTaskResponseTypeDef(TypedDict):
    taskStatus: AuditTaskStatusType
    taskType: AuditTaskTypeType
    taskStartTime: datetime
    taskStatistics: TaskStatisticsTypeDef
    scheduledAuditName: str
    auditDetails: Dict[str, AuditCheckDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RegisterCACertificateRequestTypeDef(TypedDict):
    caCertificate: str
    verificationCertificate: NotRequired[str]
    setAsActive: NotRequired[bool]
    allowAutoRegistration: NotRequired[bool]
    registrationConfig: NotRequired[RegistrationConfigTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    certificateMode: NotRequired[CertificateModeType]


class UpdateCACertificateRequestTypeDef(TypedDict):
    certificateId: str
    newStatus: NotRequired[CACertificateStatusType]
    newAutoRegistrationStatus: NotRequired[AutoRegistrationStatusType]
    registrationConfig: NotRequired[RegistrationConfigTypeDef]
    removeAutoRegistration: NotRequired[bool]


class DescribeDomainConfigurationResponseTypeDef(TypedDict):
    domainConfigurationName: str
    domainConfigurationArn: str
    domainName: str
    serverCertificates: List[ServerCertificateSummaryTypeDef]
    authorizerConfig: AuthorizerConfigTypeDef
    domainConfigurationStatus: DomainConfigurationStatusType
    serviceType: ServiceTypeType
    domainType: DomainTypeType
    lastStatusChangeDate: datetime
    tlsConfig: TlsConfigTypeDef
    serverCertificateConfig: ServerCertificateConfigTypeDef
    authenticationType: AuthenticationTypeType
    applicationProtocol: ApplicationProtocolType
    clientCertificateConfig: ClientCertificateConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeManagedJobTemplateResponseTypeDef(TypedDict):
    templateName: str
    templateArn: str
    description: str
    templateVersion: str
    environments: List[str]
    documentParameters: List[DocumentParameterTypeDef]
    document: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRoleAliasResponseTypeDef(TypedDict):
    roleAliasDescription: RoleAliasDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DestinationTypeDef(TypedDict):
    s3Destination: NotRequired[S3DestinationTypeDef]


class ListDetectMitigationActionsExecutionsResponseTypeDef(TypedDict):
    actionsExecutions: List[DetectMitigationActionExecutionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


DetectMitigationActionsTaskTargetUnionTypeDef = Union[
    DetectMitigationActionsTaskTargetTypeDef, DetectMitigationActionsTaskTargetOutputTypeDef
]


class ListDomainConfigurationsResponseTypeDef(TypedDict):
    domainConfigurations: List[DomainConfigurationSummaryTypeDef]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DynamoDBv2ActionTypeDef(TypedDict):
    roleArn: str
    putItem: PutItemInputTypeDef


class GetEffectivePoliciesResponseTypeDef(TypedDict):
    effectivePolicies: List[EffectivePolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ExponentialRolloutRateTypeDef(TypedDict):
    baseRatePerMinute: int
    incrementFactor: float
    rateIncreaseCriteria: RateIncreaseCriteriaTypeDef


class ThingGroupIndexingConfigurationOutputTypeDef(TypedDict):
    thingGroupIndexingMode: ThingGroupIndexingModeType
    managedFields: NotRequired[List[FieldTypeDef]]
    customFields: NotRequired[List[FieldTypeDef]]


class ThingGroupIndexingConfigurationTypeDef(TypedDict):
    thingGroupIndexingMode: ThingGroupIndexingModeType
    managedFields: NotRequired[Sequence[FieldTypeDef]]
    customFields: NotRequired[Sequence[FieldTypeDef]]


class PackageVersionArtifactTypeDef(TypedDict):
    s3Location: NotRequired[S3LocationTypeDef]


class SbomTypeDef(TypedDict):
    s3Location: NotRequired[S3LocationTypeDef]


class StreamFileTypeDef(TypedDict):
    fileId: NotRequired[int]
    s3Location: NotRequired[S3LocationTypeDef]


class FileLocationTypeDef(TypedDict):
    stream: NotRequired[StreamTypeDef]
    s3Location: NotRequired[S3LocationTypeDef]


class ListFleetMetricsResponseTypeDef(TypedDict):
    fleetMetrics: List[FleetMetricNameAndArnTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class IndexingFilterOutputTypeDef(TypedDict):
    namedShadowNames: NotRequired[List[str]]
    geoLocations: NotRequired[List[GeoLocationTargetTypeDef]]


class IndexingFilterTypeDef(TypedDict):
    namedShadowNames: NotRequired[Sequence[str]]
    geoLocations: NotRequired[Sequence[GeoLocationTargetTypeDef]]


class GetBehaviorModelTrainingSummariesRequestPaginateTypeDef(TypedDict):
    securityProfileName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListActiveViolationsRequestPaginateTypeDef(TypedDict):
    thingName: NotRequired[str]
    securityProfileName: NotRequired[str]
    behaviorCriteriaType: NotRequired[BehaviorCriteriaTypeType]
    listSuppressedAlerts: NotRequired[bool]
    verificationState: NotRequired[VerificationStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAttachedPoliciesRequestPaginateTypeDef(TypedDict):
    target: str
    recursive: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAuditMitigationActionsExecutionsRequestPaginateTypeDef(TypedDict):
    taskId: str
    findingId: str
    actionStatus: NotRequired[AuditMitigationActionsExecutionStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAuditMitigationActionsTasksRequestPaginateTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    auditTaskId: NotRequired[str]
    findingId: NotRequired[str]
    taskStatus: NotRequired[AuditMitigationActionsTaskStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAuditTasksRequestPaginateTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    taskType: NotRequired[AuditTaskTypeType]
    taskStatus: NotRequired[AuditTaskStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAuthorizersRequestPaginateTypeDef(TypedDict):
    ascendingOrder: NotRequired[bool]
    status: NotRequired[AuthorizerStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListBillingGroupsRequestPaginateTypeDef(TypedDict):
    namePrefixFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCACertificatesRequestPaginateTypeDef(TypedDict):
    ascendingOrder: NotRequired[bool]
    templateName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCertificatesByCARequestPaginateTypeDef(TypedDict):
    caCertificateId: str
    ascendingOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCertificatesRequestPaginateTypeDef(TypedDict):
    ascendingOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCommandsRequestPaginateTypeDef(TypedDict):
    namespace: NotRequired[CommandNamespaceType]
    commandParameterName: NotRequired[str]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCustomMetricsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDetectMitigationActionsExecutionsRequestPaginateTypeDef(TypedDict):
    taskId: NotRequired[str]
    violationId: NotRequired[str]
    thingName: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDetectMitigationActionsTasksRequestPaginateTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDimensionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainConfigurationsRequestPaginateTypeDef(TypedDict):
    serviceType: NotRequired[ServiceTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListFleetMetricsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListIndicesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJobExecutionsForJobRequestPaginateTypeDef(TypedDict):
    jobId: str
    status: NotRequired[JobExecutionStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJobExecutionsForThingRequestPaginateTypeDef(TypedDict):
    thingName: str
    status: NotRequired[JobExecutionStatusType]
    namespaceId: NotRequired[str]
    jobId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJobTemplatesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJobsRequestPaginateTypeDef(TypedDict):
    status: NotRequired[JobStatusType]
    targetSelection: NotRequired[TargetSelectionType]
    thingGroupName: NotRequired[str]
    thingGroupId: NotRequired[str]
    namespaceId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListManagedJobTemplatesRequestPaginateTypeDef(TypedDict):
    templateName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMetricValuesRequestPaginateTypeDef(TypedDict):
    thingName: str
    metricName: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    dimensionName: NotRequired[str]
    dimensionValueOperator: NotRequired[DimensionValueOperatorType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListMitigationActionsRequestPaginateTypeDef(TypedDict):
    actionType: NotRequired[MitigationActionTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOTAUpdatesRequestPaginateTypeDef(TypedDict):
    otaUpdateStatus: NotRequired[OTAUpdateStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListOutgoingCertificatesRequestPaginateTypeDef(TypedDict):
    ascendingOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPackageVersionsRequestPaginateTypeDef(TypedDict):
    packageName: str
    status: NotRequired[PackageVersionStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPackagesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPoliciesRequestPaginateTypeDef(TypedDict):
    ascendingOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPolicyPrincipalsRequestPaginateTypeDef(TypedDict):
    policyName: str
    ascendingOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPrincipalPoliciesRequestPaginateTypeDef(TypedDict):
    principal: str
    ascendingOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPrincipalThingsRequestPaginateTypeDef(TypedDict):
    principal: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListPrincipalThingsV2RequestPaginateTypeDef(TypedDict):
    principal: str
    thingPrincipalType: NotRequired[ThingPrincipalTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProvisioningTemplateVersionsRequestPaginateTypeDef(TypedDict):
    templateName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProvisioningTemplatesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRelatedResourcesForAuditFindingRequestPaginateTypeDef(TypedDict):
    findingId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRoleAliasesRequestPaginateTypeDef(TypedDict):
    ascendingOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSbomValidationResultsRequestPaginateTypeDef(TypedDict):
    packageName: str
    versionName: str
    validationResult: NotRequired[SbomValidationResultType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListScheduledAuditsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSecurityProfilesForTargetRequestPaginateTypeDef(TypedDict):
    securityProfileTargetArn: str
    recursive: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSecurityProfilesRequestPaginateTypeDef(TypedDict):
    dimensionName: NotRequired[str]
    metricName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListStreamsRequestPaginateTypeDef(TypedDict):
    ascendingOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTagsForResourceRequestPaginateTypeDef(TypedDict):
    resourceArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTargetsForPolicyRequestPaginateTypeDef(TypedDict):
    policyName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTargetsForSecurityProfileRequestPaginateTypeDef(TypedDict):
    securityProfileName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingGroupsForThingRequestPaginateTypeDef(TypedDict):
    thingName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingGroupsRequestPaginateTypeDef(TypedDict):
    parentGroup: NotRequired[str]
    namePrefixFilter: NotRequired[str]
    recursive: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingPrincipalsRequestPaginateTypeDef(TypedDict):
    thingName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingPrincipalsV2RequestPaginateTypeDef(TypedDict):
    thingName: str
    thingPrincipalType: NotRequired[ThingPrincipalTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingRegistrationTaskReportsRequestPaginateTypeDef(TypedDict):
    taskId: str
    reportType: ReportTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingRegistrationTasksRequestPaginateTypeDef(TypedDict):
    status: NotRequired[StatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingTypesRequestPaginateTypeDef(TypedDict):
    thingTypeName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingsInBillingGroupRequestPaginateTypeDef(TypedDict):
    billingGroupName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingsInThingGroupRequestPaginateTypeDef(TypedDict):
    thingGroupName: str
    recursive: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListThingsRequestPaginateTypeDef(TypedDict):
    attributeName: NotRequired[str]
    attributeValue: NotRequired[str]
    thingTypeName: NotRequired[str]
    usePrefixAttributeValue: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTopicRuleDestinationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTopicRulesRequestPaginateTypeDef(TypedDict):
    topic: NotRequired[str]
    ruleDisabled: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListV2LoggingLevelsRequestPaginateTypeDef(TypedDict):
    targetType: NotRequired[LogTargetTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListViolationEventsRequestPaginateTypeDef(TypedDict):
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    thingName: NotRequired[str]
    securityProfileName: NotRequired[str]
    behaviorCriteriaType: NotRequired[BehaviorCriteriaTypeType]
    listSuppressedAlerts: NotRequired[bool]
    verificationState: NotRequired[VerificationStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class GetCommandExecutionResponseTypeDef(TypedDict):
    executionId: str
    commandArn: str
    targetArn: str
    status: CommandExecutionStatusType
    statusReason: StatusReasonTypeDef
    result: Dict[str, CommandExecutionResultTypeDef]
    parameters: Dict[str, CommandParameterValueOutputTypeDef]
    executionTimeoutSeconds: int
    createdAt: datetime
    lastUpdatedAt: datetime
    startedAt: datetime
    completedAt: datetime
    timeToLive: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class GetPackageConfigurationResponseTypeDef(TypedDict):
    versionUpdateByJobsConfig: VersionUpdateByJobsConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdatePackageConfigurationRequestTypeDef(TypedDict):
    versionUpdateByJobsConfig: NotRequired[VersionUpdateByJobsConfigTypeDef]
    clientToken: NotRequired[str]


class GetPercentilesResponseTypeDef(TypedDict):
    percentiles: List[PercentPairTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetStatisticsResponseTypeDef(TypedDict):
    statistics: StatisticsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListBillingGroupsResponseTypeDef(TypedDict):
    billingGroups: List[GroupNameAndArnTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListThingGroupsForThingResponseTypeDef(TypedDict):
    thingGroups: List[GroupNameAndArnTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListThingGroupsResponseTypeDef(TypedDict):
    thingGroups: List[GroupNameAndArnTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ThingGroupMetadataTypeDef(TypedDict):
    parentGroupName: NotRequired[str]
    rootToParentThingGroups: NotRequired[List[GroupNameAndArnTypeDef]]
    creationDate: NotRequired[datetime]


class HttpAuthorizationTypeDef(TypedDict):
    sigv4: NotRequired[SigV4AuthorizationTypeDef]


class JobExecutionTypeDef(TypedDict):
    jobId: NotRequired[str]
    status: NotRequired[JobExecutionStatusType]
    forceCanceled: NotRequired[bool]
    statusDetails: NotRequired[JobExecutionStatusDetailsTypeDef]
    thingArn: NotRequired[str]
    queuedAt: NotRequired[datetime]
    startedAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    executionNumber: NotRequired[int]
    versionNumber: NotRequired[int]
    approximateSecondsBeforeTimedOut: NotRequired[int]


class JobExecutionSummaryForJobTypeDef(TypedDict):
    thingArn: NotRequired[str]
    jobExecutionSummary: NotRequired[JobExecutionSummaryTypeDef]


class JobExecutionSummaryForThingTypeDef(TypedDict):
    jobId: NotRequired[str]
    jobExecutionSummary: NotRequired[JobExecutionSummaryTypeDef]


class JobExecutionsRetryConfigOutputTypeDef(TypedDict):
    criteriaList: List[RetryCriteriaTypeDef]


class JobExecutionsRetryConfigTypeDef(TypedDict):
    criteriaList: Sequence[RetryCriteriaTypeDef]


class ListJobsResponseTypeDef(TypedDict):
    jobs: List[JobSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListJobTemplatesResponseTypeDef(TypedDict):
    jobTemplates: List[JobTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class KafkaActionOutputTypeDef(TypedDict):
    destinationArn: str
    topic: str
    clientProperties: Dict[str, str]
    key: NotRequired[str]
    partition: NotRequired[str]
    headers: NotRequired[List[KafkaActionHeaderTypeDef]]


class KafkaActionTypeDef(TypedDict):
    destinationArn: str
    topic: str
    clientProperties: Mapping[str, str]
    key: NotRequired[str]
    partition: NotRequired[str]
    headers: NotRequired[Sequence[KafkaActionHeaderTypeDef]]


class ListCommandExecutionsRequestPaginateTypeDef(TypedDict):
    namespace: NotRequired[CommandNamespaceType]
    status: NotRequired[CommandExecutionStatusType]
    sortOrder: NotRequired[SortOrderType]
    startedTimeFilter: NotRequired[TimeFilterTypeDef]
    completedTimeFilter: NotRequired[TimeFilterTypeDef]
    targetArn: NotRequired[str]
    commandArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCommandExecutionsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    namespace: NotRequired[CommandNamespaceType]
    status: NotRequired[CommandExecutionStatusType]
    sortOrder: NotRequired[SortOrderType]
    startedTimeFilter: NotRequired[TimeFilterTypeDef]
    completedTimeFilter: NotRequired[TimeFilterTypeDef]
    targetArn: NotRequired[str]
    commandArn: NotRequired[str]


class ListManagedJobTemplatesResponseTypeDef(TypedDict):
    managedJobTemplates: List[ManagedJobTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListMitigationActionsResponseTypeDef(TypedDict):
    actionIdentifiers: List[MitigationActionIdentifierTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListOTAUpdatesResponseTypeDef(TypedDict):
    otaUpdates: List[OTAUpdateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListOutgoingCertificatesResponseTypeDef(TypedDict):
    outgoingCertificates: List[OutgoingCertificateTypeDef]
    nextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListPackageVersionsResponseTypeDef(TypedDict):
    packageVersionSummaries: List[PackageVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPackagesResponseTypeDef(TypedDict):
    packageSummaries: List[PackageSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListPolicyVersionsResponseTypeDef(TypedDict):
    policyVersions: List[PolicyVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListPrincipalThingsV2ResponseTypeDef(TypedDict):
    principalThingObjects: List[PrincipalThingObjectTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListProvisioningTemplateVersionsResponseTypeDef(TypedDict):
    versions: List[ProvisioningTemplateVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListProvisioningTemplatesResponseTypeDef(TypedDict):
    templates: List[ProvisioningTemplateSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSbomValidationResultsResponseTypeDef(TypedDict):
    validationResultSummaries: List[SbomValidationResultSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListScheduledAuditsResponseTypeDef(TypedDict):
    scheduledAudits: List[ScheduledAuditMetadataTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSecurityProfilesResponseTypeDef(TypedDict):
    securityProfileIdentifiers: List[SecurityProfileIdentifierTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListStreamsResponseTypeDef(TypedDict):
    streams: List[StreamSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTargetsForSecurityProfileResponseTypeDef(TypedDict):
    securityProfileTargets: List[SecurityProfileTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SecurityProfileTargetMappingTypeDef(TypedDict):
    securityProfileIdentifier: NotRequired[SecurityProfileIdentifierTypeDef]
    target: NotRequired[SecurityProfileTargetTypeDef]


class ListThingPrincipalsV2ResponseTypeDef(TypedDict):
    thingPrincipalObjects: List[ThingPrincipalObjectTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListThingsResponseTypeDef(TypedDict):
    things: List[ThingAttributeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTopicRulesResponseTypeDef(TypedDict):
    rules: List[TopicRuleListItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class LocationActionTypeDef(TypedDict):
    roleArn: str
    trackerName: str
    deviceId: str
    latitude: str
    longitude: str
    timestamp: NotRequired[LocationTimestampTypeDef]


class LogTargetConfigurationTypeDef(TypedDict):
    logTarget: NotRequired[LogTargetTypeDef]
    logLevel: NotRequired[LogLevelType]


class SetV2LoggingLevelRequestTypeDef(TypedDict):
    logTarget: LogTargetTypeDef
    logLevel: LogLevelType


class SetLoggingOptionsRequestTypeDef(TypedDict):
    loggingOptionsPayload: LoggingOptionsPayloadTypeDef


MetricValueUnionTypeDef = Union[MetricValueTypeDef, MetricValueOutputTypeDef]


class MitigationActionParamsOutputTypeDef(TypedDict):
    updateDeviceCertificateParams: NotRequired[UpdateDeviceCertificateParamsTypeDef]
    updateCACertificateParams: NotRequired[UpdateCACertificateParamsTypeDef]
    addThingsToThingGroupParams: NotRequired[AddThingsToThingGroupParamsOutputTypeDef]
    replaceDefaultPolicyVersionParams: NotRequired[ReplaceDefaultPolicyVersionParamsTypeDef]
    enableIoTLoggingParams: NotRequired[EnableIoTLoggingParamsTypeDef]
    publishFindingToSnsParams: NotRequired[PublishFindingToSnsParamsTypeDef]


class MitigationActionParamsTypeDef(TypedDict):
    updateDeviceCertificateParams: NotRequired[UpdateDeviceCertificateParamsTypeDef]
    updateCACertificateParams: NotRequired[UpdateCACertificateParamsTypeDef]
    addThingsToThingGroupParams: NotRequired[AddThingsToThingGroupParamsTypeDef]
    replaceDefaultPolicyVersionParams: NotRequired[ReplaceDefaultPolicyVersionParamsTypeDef]
    enableIoTLoggingParams: NotRequired[EnableIoTLoggingParamsTypeDef]
    publishFindingToSnsParams: NotRequired[PublishFindingToSnsParamsTypeDef]


class Mqtt5ConfigurationOutputTypeDef(TypedDict):
    propagatingAttributes: NotRequired[List[PropagatingAttributeTypeDef]]


class Mqtt5ConfigurationTypeDef(TypedDict):
    propagatingAttributes: NotRequired[Sequence[PropagatingAttributeTypeDef]]


class MqttHeadersOutputTypeDef(TypedDict):
    payloadFormatIndicator: NotRequired[str]
    contentType: NotRequired[str]
    responseTopic: NotRequired[str]
    correlationData: NotRequired[str]
    messageExpiry: NotRequired[str]
    userProperties: NotRequired[List[UserPropertyTypeDef]]


class MqttHeadersTypeDef(TypedDict):
    payloadFormatIndicator: NotRequired[str]
    contentType: NotRequired[str]
    responseTopic: NotRequired[str]
    correlationData: NotRequired[str]
    messageExpiry: NotRequired[str]
    userProperties: NotRequired[Sequence[UserPropertyTypeDef]]


class ResourceIdentifierTypeDef(TypedDict):
    deviceCertificateId: NotRequired[str]
    caCertificateId: NotRequired[str]
    cognitoIdentityPoolId: NotRequired[str]
    clientId: NotRequired[str]
    policyVersionIdentifier: NotRequired[PolicyVersionIdentifierTypeDef]
    account: NotRequired[str]
    iamRoleArn: NotRequired[str]
    roleAliasArn: NotRequired[str]
    issuerCertificateIdentifier: NotRequired[IssuerCertificateIdentifierTypeDef]
    deviceCertificateArn: NotRequired[str]


class ThingDocumentTypeDef(TypedDict):
    thingName: NotRequired[str]
    thingId: NotRequired[str]
    thingTypeName: NotRequired[str]
    thingGroupNames: NotRequired[List[str]]
    attributes: NotRequired[Dict[str, str]]
    shadow: NotRequired[str]
    deviceDefender: NotRequired[str]
    connectivity: NotRequired[ThingConnectivityTypeDef]


class TimestreamActionOutputTypeDef(TypedDict):
    roleArn: str
    databaseName: str
    tableName: str
    dimensions: List[TimestreamDimensionTypeDef]
    timestamp: NotRequired[TimestreamTimestampTypeDef]


class TimestreamActionTypeDef(TypedDict):
    roleArn: str
    databaseName: str
    tableName: str
    dimensions: Sequence[TimestreamDimensionTypeDef]
    timestamp: NotRequired[TimestreamTimestampTypeDef]


class TopicRuleDestinationConfigurationTypeDef(TypedDict):
    httpUrlConfiguration: NotRequired[HttpUrlDestinationConfigurationTypeDef]
    vpcConfiguration: NotRequired[VpcDestinationConfigurationTypeDef]


class TopicRuleDestinationSummaryTypeDef(TypedDict):
    arn: NotRequired[str]
    status: NotRequired[TopicRuleDestinationStatusType]
    createdAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    statusReason: NotRequired[str]
    httpUrlSummary: NotRequired[HttpUrlDestinationSummaryTypeDef]
    vpcDestinationSummary: NotRequired[VpcDestinationSummaryTypeDef]


class TopicRuleDestinationTypeDef(TypedDict):
    arn: NotRequired[str]
    status: NotRequired[TopicRuleDestinationStatusType]
    createdAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    statusReason: NotRequired[str]
    httpUrlProperties: NotRequired[HttpUrlDestinationPropertiesTypeDef]
    vpcProperties: NotRequired[VpcDestinationPropertiesTypeDef]


class ValidateSecurityProfileBehaviorsResponseTypeDef(TypedDict):
    valid: bool
    validationErrors: List[ValidationErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


AbortConfigUnionTypeDef = Union[AbortConfigTypeDef, AbortConfigOutputTypeDef]


class ListMetricValuesResponseTypeDef(TypedDict):
    metricDatumList: List[MetricDatumTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateFleetMetricRequestTypeDef(TypedDict):
    metricName: str
    queryString: str
    aggregationType: AggregationTypeUnionTypeDef
    period: int
    aggregationField: str
    description: NotRequired[str]
    queryVersion: NotRequired[str]
    indexName: NotRequired[str]
    unit: NotRequired[FleetMetricUnitType]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateFleetMetricRequestTypeDef(TypedDict):
    metricName: str
    indexName: str
    queryString: NotRequired[str]
    aggregationType: NotRequired[AggregationTypeUnionTypeDef]
    period: NotRequired[int]
    aggregationField: NotRequired[str]
    description: NotRequired[str]
    queryVersion: NotRequired[str]
    unit: NotRequired[FleetMetricUnitType]
    expectedVersion: NotRequired[int]


class DeniedTypeDef(TypedDict):
    implicitDeny: NotRequired[ImplicitDenyTypeDef]
    explicitDeny: NotRequired[ExplicitDenyTypeDef]


class PutAssetPropertyValueEntryOutputTypeDef(TypedDict):
    propertyValues: List[AssetPropertyValueTypeDef]
    entryId: NotRequired[str]
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]


class PutAssetPropertyValueEntryTypeDef(TypedDict):
    propertyValues: Sequence[AssetPropertyValueTypeDef]
    entryId: NotRequired[str]
    assetId: NotRequired[str]
    propertyId: NotRequired[str]
    propertyAlias: NotRequired[str]


class CreateThingRequestTypeDef(TypedDict):
    thingName: str
    thingTypeName: NotRequired[str]
    attributePayload: NotRequired[AttributePayloadUnionTypeDef]
    billingGroupName: NotRequired[str]


class UpdateThingRequestTypeDef(TypedDict):
    thingName: str
    thingTypeName: NotRequired[str]
    attributePayload: NotRequired[AttributePayloadUnionTypeDef]
    expectedVersion: NotRequired[int]
    removeThingType: NotRequired[bool]


ThingGroupPropertiesUnionTypeDef = Union[
    ThingGroupPropertiesTypeDef, ThingGroupPropertiesOutputTypeDef
]


class UpdateAccountAuditConfigurationRequestTypeDef(TypedDict):
    roleArn: NotRequired[str]
    auditNotificationTargetConfigurations: NotRequired[
        Mapping[Literal["SNS"], AuditNotificationTargetTypeDef]
    ]
    auditCheckConfigurations: NotRequired[Mapping[str, AuditCheckConfigurationUnionTypeDef]]


class StartAuditMitigationActionsTaskRequestTypeDef(TypedDict):
    taskId: str
    target: AuditMitigationActionsTaskTargetUnionTypeDef
    auditCheckToActionsMapping: Mapping[str, Sequence[str]]
    clientRequestToken: str


class TestAuthorizationRequestTypeDef(TypedDict):
    authInfos: Sequence[AuthInfoUnionTypeDef]
    principal: NotRequired[str]
    cognitoIdentityPoolId: NotRequired[str]
    clientId: NotRequired[str]
    policyNamesToAdd: NotRequired[Sequence[str]]
    policyNamesToSkip: NotRequired[Sequence[str]]


class AwsJobExecutionsRolloutConfigTypeDef(TypedDict):
    maximumPerMinute: NotRequired[int]
    exponentialRate: NotRequired[AwsJobExponentialRolloutRateTypeDef]


class BehaviorOutputTypeDef(TypedDict):
    name: str
    metric: NotRequired[str]
    metricDimension: NotRequired[MetricDimensionTypeDef]
    criteria: NotRequired[BehaviorCriteriaOutputTypeDef]
    suppressAlerts: NotRequired[bool]
    exportMetric: NotRequired[bool]


CodeSigningSignatureUnionTypeDef = Union[
    CodeSigningSignatureTypeDef, CodeSigningSignatureOutputTypeDef
]
CommandParameterValueUnionTypeDef = Union[
    CommandParameterValueTypeDef, CommandParameterValueOutputTypeDef
]
CommandPayloadUnionTypeDef = Union[CommandPayloadTypeDef, CommandPayloadOutputTypeDef]


class TestInvokeAuthorizerRequestTypeDef(TypedDict):
    authorizerName: str
    token: NotRequired[str]
    tokenSignature: NotRequired[str]
    httpContext: NotRequired[HttpContextTypeDef]
    mqttContext: NotRequired[MqttContextTypeDef]
    tlsContext: NotRequired[TlsContextTypeDef]


class GetBucketsAggregationRequestTypeDef(TypedDict):
    queryString: str
    aggregationField: str
    bucketsAggregationType: BucketsAggregationTypeTypeDef
    indexName: NotRequired[str]
    queryVersion: NotRequired[str]


class DescribeCACertificateResponseTypeDef(TypedDict):
    certificateDescription: CACertificateDescriptionTypeDef
    registrationConfig: RegistrationConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCertificateResponseTypeDef(TypedDict):
    certificateDescription: CertificateDescriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetCommandResponseTypeDef(TypedDict):
    commandId: str
    commandArn: str
    namespace: CommandNamespaceType
    displayName: str
    description: str
    mandatoryParameters: List[CommandParameterOutputTypeDef]
    payload: CommandPayloadOutputTypeDef
    roleArn: str
    createdAt: datetime
    lastUpdatedAt: datetime
    deprecated: bool
    pendingDeletion: bool
    ResponseMetadata: ResponseMetadataTypeDef


ViolationEventOccurrenceRangeUnionTypeDef = Union[
    ViolationEventOccurrenceRangeTypeDef, ViolationEventOccurrenceRangeOutputTypeDef
]
SchedulingConfigUnionTypeDef = Union[SchedulingConfigTypeDef, SchedulingConfigOutputTypeDef]


class StartSigningJobParameterTypeDef(TypedDict):
    signingProfileParameter: NotRequired[SigningProfileParameterTypeDef]
    signingProfileName: NotRequired[str]
    destination: NotRequired[DestinationTypeDef]


class JobExecutionsRolloutConfigTypeDef(TypedDict):
    maximumPerMinute: NotRequired[int]
    exponentialRate: NotRequired[ExponentialRolloutRateTypeDef]


ThingGroupIndexingConfigurationUnionTypeDef = Union[
    ThingGroupIndexingConfigurationTypeDef, ThingGroupIndexingConfigurationOutputTypeDef
]


class CreatePackageVersionRequestTypeDef(TypedDict):
    packageName: str
    versionName: str
    description: NotRequired[str]
    attributes: NotRequired[Mapping[str, str]]
    artifact: NotRequired[PackageVersionArtifactTypeDef]
    recipe: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    clientToken: NotRequired[str]


class UpdatePackageVersionRequestTypeDef(TypedDict):
    packageName: str
    versionName: str
    description: NotRequired[str]
    attributes: NotRequired[Mapping[str, str]]
    artifact: NotRequired[PackageVersionArtifactTypeDef]
    action: NotRequired[PackageVersionActionType]
    recipe: NotRequired[str]
    clientToken: NotRequired[str]


class AssociateSbomWithPackageVersionRequestTypeDef(TypedDict):
    packageName: str
    versionName: str
    sbom: SbomTypeDef
    clientToken: NotRequired[str]


class AssociateSbomWithPackageVersionResponseTypeDef(TypedDict):
    packageName: str
    versionName: str
    sbom: SbomTypeDef
    sbomValidationStatus: SbomValidationStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class GetPackageVersionResponseTypeDef(TypedDict):
    packageVersionArn: str
    packageName: str
    versionName: str
    description: str
    attributes: Dict[str, str]
    artifact: PackageVersionArtifactTypeDef
    status: PackageVersionStatusType
    errorReason: str
    creationDate: datetime
    lastModifiedDate: datetime
    sbom: SbomTypeDef
    sbomValidationStatus: SbomValidationStatusType
    recipe: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateStreamRequestTypeDef(TypedDict):
    streamId: str
    files: Sequence[StreamFileTypeDef]
    roleArn: str
    description: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class StreamInfoTypeDef(TypedDict):
    streamId: NotRequired[str]
    streamArn: NotRequired[str]
    streamVersion: NotRequired[int]
    description: NotRequired[str]
    files: NotRequired[List[StreamFileTypeDef]]
    createdAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    roleArn: NotRequired[str]


class UpdateStreamRequestTypeDef(TypedDict):
    streamId: str
    description: NotRequired[str]
    files: NotRequired[Sequence[StreamFileTypeDef]]
    roleArn: NotRequired[str]


ThingIndexingConfigurationOutputTypeDef = TypedDict(
    "ThingIndexingConfigurationOutputTypeDef",
    {
        "thingIndexingMode": ThingIndexingModeType,
        "thingConnectivityIndexingMode": NotRequired[ThingConnectivityIndexingModeType],
        "deviceDefenderIndexingMode": NotRequired[DeviceDefenderIndexingModeType],
        "namedShadowIndexingMode": NotRequired[NamedShadowIndexingModeType],
        "managedFields": NotRequired[List[FieldTypeDef]],
        "customFields": NotRequired[List[FieldTypeDef]],
        "filter": NotRequired[IndexingFilterOutputTypeDef],
    },
)
ThingIndexingConfigurationTypeDef = TypedDict(
    "ThingIndexingConfigurationTypeDef",
    {
        "thingIndexingMode": ThingIndexingModeType,
        "thingConnectivityIndexingMode": NotRequired[ThingConnectivityIndexingModeType],
        "deviceDefenderIndexingMode": NotRequired[DeviceDefenderIndexingModeType],
        "namedShadowIndexingMode": NotRequired[NamedShadowIndexingModeType],
        "managedFields": NotRequired[Sequence[FieldTypeDef]],
        "customFields": NotRequired[Sequence[FieldTypeDef]],
        "filter": NotRequired[IndexingFilterTypeDef],
    },
)


class DescribeThingGroupResponseTypeDef(TypedDict):
    thingGroupName: str
    thingGroupId: str
    thingGroupArn: str
    version: int
    thingGroupProperties: ThingGroupPropertiesOutputTypeDef
    thingGroupMetadata: ThingGroupMetadataTypeDef
    indexName: str
    queryString: str
    queryVersion: str
    status: DynamicGroupStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class HttpActionOutputTypeDef(TypedDict):
    url: str
    confirmationUrl: NotRequired[str]
    headers: NotRequired[List[HttpActionHeaderTypeDef]]
    auth: NotRequired[HttpAuthorizationTypeDef]


class HttpActionTypeDef(TypedDict):
    url: str
    confirmationUrl: NotRequired[str]
    headers: NotRequired[Sequence[HttpActionHeaderTypeDef]]
    auth: NotRequired[HttpAuthorizationTypeDef]


class DescribeJobExecutionResponseTypeDef(TypedDict):
    execution: JobExecutionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListJobExecutionsForJobResponseTypeDef(TypedDict):
    executionSummaries: List[JobExecutionSummaryForJobTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListJobExecutionsForThingResponseTypeDef(TypedDict):
    executionSummaries: List[JobExecutionSummaryForThingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


JobExecutionsRetryConfigUnionTypeDef = Union[
    JobExecutionsRetryConfigTypeDef, JobExecutionsRetryConfigOutputTypeDef
]
KafkaActionUnionTypeDef = Union[KafkaActionTypeDef, KafkaActionOutputTypeDef]


class ListSecurityProfilesForTargetResponseTypeDef(TypedDict):
    securityProfileTargetMappings: List[SecurityProfileTargetMappingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListV2LoggingLevelsResponseTypeDef(TypedDict):
    logTargetConfigurations: List[LogTargetConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class BehaviorCriteriaTypeDef(TypedDict):
    comparisonOperator: NotRequired[ComparisonOperatorType]
    value: NotRequired[MetricValueUnionTypeDef]
    durationSeconds: NotRequired[int]
    consecutiveDatapointsToAlarm: NotRequired[int]
    consecutiveDatapointsToClear: NotRequired[int]
    statisticalThreshold: NotRequired[StatisticalThresholdTypeDef]
    mlDetectionConfig: NotRequired[MachineLearningDetectionConfigTypeDef]


class DescribeMitigationActionResponseTypeDef(TypedDict):
    actionName: str
    actionType: MitigationActionTypeType
    actionArn: str
    actionId: str
    roleArn: str
    actionParams: MitigationActionParamsOutputTypeDef
    creationDate: datetime
    lastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef


MitigationActionTypeDef = TypedDict(
    "MitigationActionTypeDef",
    {
        "name": NotRequired[str],
        "id": NotRequired[str],
        "roleArn": NotRequired[str],
        "actionParams": NotRequired[MitigationActionParamsOutputTypeDef],
    },
)
MitigationActionParamsUnionTypeDef = Union[
    MitigationActionParamsTypeDef, MitigationActionParamsOutputTypeDef
]


class ThingTypePropertiesOutputTypeDef(TypedDict):
    thingTypeDescription: NotRequired[str]
    searchableAttributes: NotRequired[List[str]]
    mqtt5Configuration: NotRequired[Mqtt5ConfigurationOutputTypeDef]


class ThingTypePropertiesTypeDef(TypedDict):
    thingTypeDescription: NotRequired[str]
    searchableAttributes: NotRequired[Sequence[str]]
    mqtt5Configuration: NotRequired[Mqtt5ConfigurationTypeDef]


class RepublishActionOutputTypeDef(TypedDict):
    roleArn: str
    topic: str
    qos: NotRequired[int]
    headers: NotRequired[MqttHeadersOutputTypeDef]


MqttHeadersUnionTypeDef = Union[MqttHeadersTypeDef, MqttHeadersOutputTypeDef]


class AuditSuppressionTypeDef(TypedDict):
    checkName: str
    resourceIdentifier: ResourceIdentifierTypeDef
    expirationDate: NotRequired[datetime]
    suppressIndefinitely: NotRequired[bool]
    description: NotRequired[str]


class CreateAuditSuppressionRequestTypeDef(TypedDict):
    checkName: str
    resourceIdentifier: ResourceIdentifierTypeDef
    clientRequestToken: str
    expirationDate: NotRequired[TimestampTypeDef]
    suppressIndefinitely: NotRequired[bool]
    description: NotRequired[str]


class DeleteAuditSuppressionRequestTypeDef(TypedDict):
    checkName: str
    resourceIdentifier: ResourceIdentifierTypeDef


class DescribeAuditSuppressionRequestTypeDef(TypedDict):
    checkName: str
    resourceIdentifier: ResourceIdentifierTypeDef


class DescribeAuditSuppressionResponseTypeDef(TypedDict):
    checkName: str
    resourceIdentifier: ResourceIdentifierTypeDef
    expirationDate: datetime
    suppressIndefinitely: bool
    description: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListAuditFindingsRequestPaginateTypeDef(TypedDict):
    taskId: NotRequired[str]
    checkName: NotRequired[str]
    resourceIdentifier: NotRequired[ResourceIdentifierTypeDef]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    listSuppressedFindings: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAuditFindingsRequestTypeDef(TypedDict):
    taskId: NotRequired[str]
    checkName: NotRequired[str]
    resourceIdentifier: NotRequired[ResourceIdentifierTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    listSuppressedFindings: NotRequired[bool]


class ListAuditSuppressionsRequestPaginateTypeDef(TypedDict):
    checkName: NotRequired[str]
    resourceIdentifier: NotRequired[ResourceIdentifierTypeDef]
    ascendingOrder: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAuditSuppressionsRequestTypeDef(TypedDict):
    checkName: NotRequired[str]
    resourceIdentifier: NotRequired[ResourceIdentifierTypeDef]
    ascendingOrder: NotRequired[bool]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class NonCompliantResourceTypeDef(TypedDict):
    resourceType: NotRequired[ResourceTypeType]
    resourceIdentifier: NotRequired[ResourceIdentifierTypeDef]
    additionalInfo: NotRequired[Dict[str, str]]


class RelatedResourceTypeDef(TypedDict):
    resourceType: NotRequired[ResourceTypeType]
    resourceIdentifier: NotRequired[ResourceIdentifierTypeDef]
    additionalInfo: NotRequired[Dict[str, str]]


class UpdateAuditSuppressionRequestTypeDef(TypedDict):
    checkName: str
    resourceIdentifier: ResourceIdentifierTypeDef
    expirationDate: NotRequired[TimestampTypeDef]
    suppressIndefinitely: NotRequired[bool]
    description: NotRequired[str]


class SearchIndexResponseTypeDef(TypedDict):
    things: List[ThingDocumentTypeDef]
    thingGroups: List[ThingGroupDocumentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


TimestreamActionUnionTypeDef = Union[TimestreamActionTypeDef, TimestreamActionOutputTypeDef]


class CreateTopicRuleDestinationRequestTypeDef(TypedDict):
    destinationConfiguration: TopicRuleDestinationConfigurationTypeDef


class ListTopicRuleDestinationsResponseTypeDef(TypedDict):
    destinationSummaries: List[TopicRuleDestinationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateTopicRuleDestinationResponseTypeDef(TypedDict):
    topicRuleDestination: TopicRuleDestinationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetTopicRuleDestinationResponseTypeDef(TypedDict):
    topicRuleDestination: TopicRuleDestinationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AuthResultTypeDef(TypedDict):
    authInfo: NotRequired[AuthInfoOutputTypeDef]
    allowed: NotRequired[AllowedTypeDef]
    denied: NotRequired[DeniedTypeDef]
    authDecision: NotRequired[AuthDecisionType]
    missingContextValues: NotRequired[List[str]]


class IotSiteWiseActionOutputTypeDef(TypedDict):
    putAssetPropertyValueEntries: List[PutAssetPropertyValueEntryOutputTypeDef]
    roleArn: str


PutAssetPropertyValueEntryUnionTypeDef = Union[
    PutAssetPropertyValueEntryTypeDef, PutAssetPropertyValueEntryOutputTypeDef
]


class CreateDynamicThingGroupRequestTypeDef(TypedDict):
    thingGroupName: str
    queryString: str
    thingGroupProperties: NotRequired[ThingGroupPropertiesUnionTypeDef]
    indexName: NotRequired[str]
    queryVersion: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class CreateThingGroupRequestTypeDef(TypedDict):
    thingGroupName: str
    parentGroupName: NotRequired[str]
    thingGroupProperties: NotRequired[ThingGroupPropertiesUnionTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateDynamicThingGroupRequestTypeDef(TypedDict):
    thingGroupName: str
    thingGroupProperties: ThingGroupPropertiesUnionTypeDef
    expectedVersion: NotRequired[int]
    indexName: NotRequired[str]
    queryString: NotRequired[str]
    queryVersion: NotRequired[str]


class UpdateThingGroupRequestTypeDef(TypedDict):
    thingGroupName: str
    thingGroupProperties: ThingGroupPropertiesUnionTypeDef
    expectedVersion: NotRequired[int]


class ActiveViolationTypeDef(TypedDict):
    violationId: NotRequired[str]
    thingName: NotRequired[str]
    securityProfileName: NotRequired[str]
    behavior: NotRequired[BehaviorOutputTypeDef]
    lastViolationValue: NotRequired[MetricValueOutputTypeDef]
    violationEventAdditionalInfo: NotRequired[ViolationEventAdditionalInfoTypeDef]
    verificationState: NotRequired[VerificationStateType]
    verificationStateDescription: NotRequired[str]
    lastViolationTime: NotRequired[datetime]
    violationStartTime: NotRequired[datetime]


class DescribeSecurityProfileResponseTypeDef(TypedDict):
    securityProfileName: str
    securityProfileArn: str
    securityProfileDescription: str
    behaviors: List[BehaviorOutputTypeDef]
    alertTargets: Dict[Literal["SNS"], AlertTargetTypeDef]
    additionalMetricsToRetain: List[str]
    additionalMetricsToRetainV2: List[MetricToRetainTypeDef]
    version: int
    creationDate: datetime
    lastModifiedDate: datetime
    metricsExportConfig: MetricsExportConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSecurityProfileResponseTypeDef(TypedDict):
    securityProfileName: str
    securityProfileArn: str
    securityProfileDescription: str
    behaviors: List[BehaviorOutputTypeDef]
    alertTargets: Dict[Literal["SNS"], AlertTargetTypeDef]
    additionalMetricsToRetain: List[str]
    additionalMetricsToRetainV2: List[MetricToRetainTypeDef]
    version: int
    creationDate: datetime
    lastModifiedDate: datetime
    metricsExportConfig: MetricsExportConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ViolationEventTypeDef(TypedDict):
    violationId: NotRequired[str]
    thingName: NotRequired[str]
    securityProfileName: NotRequired[str]
    behavior: NotRequired[BehaviorOutputTypeDef]
    metricValue: NotRequired[MetricValueOutputTypeDef]
    violationEventAdditionalInfo: NotRequired[ViolationEventAdditionalInfoTypeDef]
    violationEventType: NotRequired[ViolationEventTypeType]
    verificationState: NotRequired[VerificationStateType]
    verificationStateDescription: NotRequired[str]
    violationEventTime: NotRequired[datetime]


class CustomCodeSigningTypeDef(TypedDict):
    signature: NotRequired[CodeSigningSignatureUnionTypeDef]
    certificateChain: NotRequired[CodeSigningCertificateChainTypeDef]
    hashAlgorithm: NotRequired[str]
    signatureAlgorithm: NotRequired[str]


class CommandParameterTypeDef(TypedDict):
    name: str
    value: NotRequired[CommandParameterValueUnionTypeDef]
    defaultValue: NotRequired[CommandParameterValueUnionTypeDef]
    description: NotRequired[str]


class StartDetectMitigationActionsTaskRequestTypeDef(TypedDict):
    taskId: str
    target: DetectMitigationActionsTaskTargetUnionTypeDef
    actions: Sequence[str]
    clientRequestToken: str
    violationEventOccurrenceRange: NotRequired[ViolationEventOccurrenceRangeUnionTypeDef]
    includeOnlyActiveViolations: NotRequired[bool]
    includeSuppressedAlerts: NotRequired[bool]


class CodeSigningOutputTypeDef(TypedDict):
    awsSignerJobId: NotRequired[str]
    startSigningJobParameter: NotRequired[StartSigningJobParameterTypeDef]
    customCodeSigning: NotRequired[CustomCodeSigningOutputTypeDef]


class DescribeJobTemplateResponseTypeDef(TypedDict):
    jobTemplateArn: str
    jobTemplateId: str
    description: str
    documentSource: str
    document: str
    createdAt: datetime
    presignedUrlConfig: PresignedUrlConfigTypeDef
    jobExecutionsRolloutConfig: JobExecutionsRolloutConfigTypeDef
    abortConfig: AbortConfigOutputTypeDef
    timeoutConfig: TimeoutConfigTypeDef
    jobExecutionsRetryConfig: JobExecutionsRetryConfigOutputTypeDef
    maintenanceWindows: List[MaintenanceWindowTypeDef]
    destinationPackageVersions: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class JobTypeDef(TypedDict):
    jobArn: NotRequired[str]
    jobId: NotRequired[str]
    targetSelection: NotRequired[TargetSelectionType]
    status: NotRequired[JobStatusType]
    forceCanceled: NotRequired[bool]
    reasonCode: NotRequired[str]
    comment: NotRequired[str]
    targets: NotRequired[List[str]]
    description: NotRequired[str]
    presignedUrlConfig: NotRequired[PresignedUrlConfigTypeDef]
    jobExecutionsRolloutConfig: NotRequired[JobExecutionsRolloutConfigTypeDef]
    abortConfig: NotRequired[AbortConfigOutputTypeDef]
    createdAt: NotRequired[datetime]
    lastUpdatedAt: NotRequired[datetime]
    completedAt: NotRequired[datetime]
    jobProcessDetails: NotRequired[JobProcessDetailsTypeDef]
    timeoutConfig: NotRequired[TimeoutConfigTypeDef]
    namespaceId: NotRequired[str]
    jobTemplateArn: NotRequired[str]
    jobExecutionsRetryConfig: NotRequired[JobExecutionsRetryConfigOutputTypeDef]
    documentParameters: NotRequired[Dict[str, str]]
    isConcurrent: NotRequired[bool]
    schedulingConfig: NotRequired[SchedulingConfigOutputTypeDef]
    scheduledJobRollouts: NotRequired[List[ScheduledJobRolloutTypeDef]]
    destinationPackageVersions: NotRequired[List[str]]


class DescribeStreamResponseTypeDef(TypedDict):
    streamInfo: StreamInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetIndexingConfigurationResponseTypeDef(TypedDict):
    thingIndexingConfiguration: ThingIndexingConfigurationOutputTypeDef
    thingGroupIndexingConfiguration: ThingGroupIndexingConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ThingIndexingConfigurationUnionTypeDef = Union[
    ThingIndexingConfigurationTypeDef, ThingIndexingConfigurationOutputTypeDef
]
HttpActionUnionTypeDef = Union[HttpActionTypeDef, HttpActionOutputTypeDef]


class CreateJobRequestTypeDef(TypedDict):
    jobId: str
    targets: Sequence[str]
    documentSource: NotRequired[str]
    document: NotRequired[str]
    description: NotRequired[str]
    presignedUrlConfig: NotRequired[PresignedUrlConfigTypeDef]
    targetSelection: NotRequired[TargetSelectionType]
    jobExecutionsRolloutConfig: NotRequired[JobExecutionsRolloutConfigTypeDef]
    abortConfig: NotRequired[AbortConfigUnionTypeDef]
    timeoutConfig: NotRequired[TimeoutConfigTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    namespaceId: NotRequired[str]
    jobTemplateArn: NotRequired[str]
    jobExecutionsRetryConfig: NotRequired[JobExecutionsRetryConfigUnionTypeDef]
    documentParameters: NotRequired[Mapping[str, str]]
    schedulingConfig: NotRequired[SchedulingConfigUnionTypeDef]
    destinationPackageVersions: NotRequired[Sequence[str]]


class CreateJobTemplateRequestTypeDef(TypedDict):
    jobTemplateId: str
    description: str
    jobArn: NotRequired[str]
    documentSource: NotRequired[str]
    document: NotRequired[str]
    presignedUrlConfig: NotRequired[PresignedUrlConfigTypeDef]
    jobExecutionsRolloutConfig: NotRequired[JobExecutionsRolloutConfigTypeDef]
    abortConfig: NotRequired[AbortConfigUnionTypeDef]
    timeoutConfig: NotRequired[TimeoutConfigTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]
    jobExecutionsRetryConfig: NotRequired[JobExecutionsRetryConfigUnionTypeDef]
    maintenanceWindows: NotRequired[Sequence[MaintenanceWindowTypeDef]]
    destinationPackageVersions: NotRequired[Sequence[str]]


class UpdateJobRequestTypeDef(TypedDict):
    jobId: str
    description: NotRequired[str]
    presignedUrlConfig: NotRequired[PresignedUrlConfigTypeDef]
    jobExecutionsRolloutConfig: NotRequired[JobExecutionsRolloutConfigTypeDef]
    abortConfig: NotRequired[AbortConfigUnionTypeDef]
    timeoutConfig: NotRequired[TimeoutConfigTypeDef]
    namespaceId: NotRequired[str]
    jobExecutionsRetryConfig: NotRequired[JobExecutionsRetryConfigUnionTypeDef]


BehaviorCriteriaUnionTypeDef = Union[BehaviorCriteriaTypeDef, BehaviorCriteriaOutputTypeDef]


class DescribeAuditMitigationActionsTaskResponseTypeDef(TypedDict):
    taskStatus: AuditMitigationActionsTaskStatusType
    startTime: datetime
    endTime: datetime
    taskStatistics: Dict[str, TaskStatisticsForAuditCheckTypeDef]
    target: AuditMitigationActionsTaskTargetOutputTypeDef
    auditCheckToActionsMapping: Dict[str, List[str]]
    actionsDefinition: List[MitigationActionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DetectMitigationActionsTaskSummaryTypeDef(TypedDict):
    taskId: NotRequired[str]
    taskStatus: NotRequired[DetectMitigationActionsTaskStatusType]
    taskStartTime: NotRequired[datetime]
    taskEndTime: NotRequired[datetime]
    target: NotRequired[DetectMitigationActionsTaskTargetOutputTypeDef]
    violationEventOccurrenceRange: NotRequired[ViolationEventOccurrenceRangeOutputTypeDef]
    onlyActiveViolationsIncluded: NotRequired[bool]
    suppressedAlertsIncluded: NotRequired[bool]
    actionsDefinition: NotRequired[List[MitigationActionTypeDef]]
    taskStatistics: NotRequired[DetectMitigationActionsTaskStatisticsTypeDef]


class CreateMitigationActionRequestTypeDef(TypedDict):
    actionName: str
    roleArn: str
    actionParams: MitigationActionParamsUnionTypeDef
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateMitigationActionRequestTypeDef(TypedDict):
    actionName: str
    roleArn: NotRequired[str]
    actionParams: NotRequired[MitigationActionParamsUnionTypeDef]


class DescribeThingTypeResponseTypeDef(TypedDict):
    thingTypeName: str
    thingTypeId: str
    thingTypeArn: str
    thingTypeProperties: ThingTypePropertiesOutputTypeDef
    thingTypeMetadata: ThingTypeMetadataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ThingTypeDefinitionTypeDef(TypedDict):
    thingTypeName: NotRequired[str]
    thingTypeArn: NotRequired[str]
    thingTypeProperties: NotRequired[ThingTypePropertiesOutputTypeDef]
    thingTypeMetadata: NotRequired[ThingTypeMetadataTypeDef]


ThingTypePropertiesUnionTypeDef = Union[
    ThingTypePropertiesTypeDef, ThingTypePropertiesOutputTypeDef
]


class RepublishActionTypeDef(TypedDict):
    roleArn: str
    topic: str
    qos: NotRequired[int]
    headers: NotRequired[MqttHeadersUnionTypeDef]


class ListAuditSuppressionsResponseTypeDef(TypedDict):
    suppressions: List[AuditSuppressionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AuditFindingTypeDef(TypedDict):
    findingId: NotRequired[str]
    taskId: NotRequired[str]
    checkName: NotRequired[str]
    taskStartTime: NotRequired[datetime]
    findingTime: NotRequired[datetime]
    severity: NotRequired[AuditFindingSeverityType]
    nonCompliantResource: NotRequired[NonCompliantResourceTypeDef]
    relatedResources: NotRequired[List[RelatedResourceTypeDef]]
    reasonForNonCompliance: NotRequired[str]
    reasonForNonComplianceCode: NotRequired[str]
    isSuppressed: NotRequired[bool]


class ListRelatedResourcesForAuditFindingResponseTypeDef(TypedDict):
    relatedResources: List[RelatedResourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class TestAuthorizationResponseTypeDef(TypedDict):
    authResults: List[AuthResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


ActionOutputTypeDef = TypedDict(
    "ActionOutputTypeDef",
    {
        "dynamoDB": NotRequired[DynamoDBActionTypeDef],
        "dynamoDBv2": NotRequired[DynamoDBv2ActionTypeDef],
        "lambda": NotRequired[LambdaActionTypeDef],
        "sns": NotRequired[SnsActionTypeDef],
        "sqs": NotRequired[SqsActionTypeDef],
        "kinesis": NotRequired[KinesisActionTypeDef],
        "republish": NotRequired[RepublishActionOutputTypeDef],
        "s3": NotRequired[S3ActionTypeDef],
        "firehose": NotRequired[FirehoseActionTypeDef],
        "cloudwatchMetric": NotRequired[CloudwatchMetricActionTypeDef],
        "cloudwatchAlarm": NotRequired[CloudwatchAlarmActionTypeDef],
        "cloudwatchLogs": NotRequired[CloudwatchLogsActionTypeDef],
        "elasticsearch": NotRequired[ElasticsearchActionTypeDef],
        "salesforce": NotRequired[SalesforceActionTypeDef],
        "iotAnalytics": NotRequired[IotAnalyticsActionTypeDef],
        "iotEvents": NotRequired[IotEventsActionTypeDef],
        "iotSiteWise": NotRequired[IotSiteWiseActionOutputTypeDef],
        "stepFunctions": NotRequired[StepFunctionsActionTypeDef],
        "timestream": NotRequired[TimestreamActionOutputTypeDef],
        "http": NotRequired[HttpActionOutputTypeDef],
        "kafka": NotRequired[KafkaActionOutputTypeDef],
        "openSearch": NotRequired[OpenSearchActionTypeDef],
        "location": NotRequired[LocationActionTypeDef],
    },
)


class IotSiteWiseActionTypeDef(TypedDict):
    putAssetPropertyValueEntries: Sequence[PutAssetPropertyValueEntryUnionTypeDef]
    roleArn: str


class ListActiveViolationsResponseTypeDef(TypedDict):
    activeViolations: List[ActiveViolationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListViolationEventsResponseTypeDef(TypedDict):
    violationEvents: List[ViolationEventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


CustomCodeSigningUnionTypeDef = Union[CustomCodeSigningTypeDef, CustomCodeSigningOutputTypeDef]
CommandParameterUnionTypeDef = Union[CommandParameterTypeDef, CommandParameterOutputTypeDef]


class OTAUpdateFileOutputTypeDef(TypedDict):
    fileName: NotRequired[str]
    fileType: NotRequired[int]
    fileVersion: NotRequired[str]
    fileLocation: NotRequired[FileLocationTypeDef]
    codeSigning: NotRequired[CodeSigningOutputTypeDef]
    attributes: NotRequired[Dict[str, str]]


class DescribeJobResponseTypeDef(TypedDict):
    documentSource: str
    job: JobTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateIndexingConfigurationRequestTypeDef(TypedDict):
    thingIndexingConfiguration: NotRequired[ThingIndexingConfigurationUnionTypeDef]
    thingGroupIndexingConfiguration: NotRequired[ThingGroupIndexingConfigurationUnionTypeDef]


class BehaviorTypeDef(TypedDict):
    name: str
    metric: NotRequired[str]
    metricDimension: NotRequired[MetricDimensionTypeDef]
    criteria: NotRequired[BehaviorCriteriaUnionTypeDef]
    suppressAlerts: NotRequired[bool]
    exportMetric: NotRequired[bool]


class DescribeDetectMitigationActionsTaskResponseTypeDef(TypedDict):
    taskSummary: DetectMitigationActionsTaskSummaryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListDetectMitigationActionsTasksResponseTypeDef(TypedDict):
    tasks: List[DetectMitigationActionsTaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListThingTypesResponseTypeDef(TypedDict):
    thingTypes: List[ThingTypeDefinitionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateThingTypeRequestTypeDef(TypedDict):
    thingTypeName: str
    thingTypeProperties: NotRequired[ThingTypePropertiesUnionTypeDef]
    tags: NotRequired[Sequence[TagTypeDef]]


class UpdateThingTypeRequestTypeDef(TypedDict):
    thingTypeName: str
    thingTypeProperties: NotRequired[ThingTypePropertiesUnionTypeDef]


RepublishActionUnionTypeDef = Union[RepublishActionTypeDef, RepublishActionOutputTypeDef]


class DescribeAuditFindingResponseTypeDef(TypedDict):
    finding: AuditFindingTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAuditFindingsResponseTypeDef(TypedDict):
    findings: List[AuditFindingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class TopicRuleTypeDef(TypedDict):
    ruleName: NotRequired[str]
    sql: NotRequired[str]
    description: NotRequired[str]
    createdAt: NotRequired[datetime]
    actions: NotRequired[List[ActionOutputTypeDef]]
    ruleDisabled: NotRequired[bool]
    awsIotSqlVersion: NotRequired[str]
    errorAction: NotRequired[ActionOutputTypeDef]


IotSiteWiseActionUnionTypeDef = Union[IotSiteWiseActionTypeDef, IotSiteWiseActionOutputTypeDef]


class CodeSigningTypeDef(TypedDict):
    awsSignerJobId: NotRequired[str]
    startSigningJobParameter: NotRequired[StartSigningJobParameterTypeDef]
    customCodeSigning: NotRequired[CustomCodeSigningUnionTypeDef]


class CreateCommandRequestTypeDef(TypedDict):
    commandId: str
    namespace: NotRequired[CommandNamespaceType]
    displayName: NotRequired[str]
    description: NotRequired[str]
    payload: NotRequired[CommandPayloadUnionTypeDef]
    mandatoryParameters: NotRequired[Sequence[CommandParameterUnionTypeDef]]
    roleArn: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]


class OTAUpdateInfoTypeDef(TypedDict):
    otaUpdateId: NotRequired[str]
    otaUpdateArn: NotRequired[str]
    creationDate: NotRequired[datetime]
    lastModifiedDate: NotRequired[datetime]
    description: NotRequired[str]
    targets: NotRequired[List[str]]
    protocols: NotRequired[List[ProtocolType]]
    awsJobExecutionsRolloutConfig: NotRequired[AwsJobExecutionsRolloutConfigTypeDef]
    awsJobPresignedUrlConfig: NotRequired[AwsJobPresignedUrlConfigTypeDef]
    targetSelection: NotRequired[TargetSelectionType]
    otaUpdateFiles: NotRequired[List[OTAUpdateFileOutputTypeDef]]
    otaUpdateStatus: NotRequired[OTAUpdateStatusType]
    awsIotJobId: NotRequired[str]
    awsIotJobArn: NotRequired[str]
    errorInfo: NotRequired[ErrorInfoTypeDef]
    additionalParameters: NotRequired[Dict[str, str]]


BehaviorUnionTypeDef = Union[BehaviorTypeDef, BehaviorOutputTypeDef]


class GetTopicRuleResponseTypeDef(TypedDict):
    ruleArn: str
    rule: TopicRuleTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "dynamoDB": NotRequired[DynamoDBActionTypeDef],
        "dynamoDBv2": NotRequired[DynamoDBv2ActionTypeDef],
        "lambda": NotRequired[LambdaActionTypeDef],
        "sns": NotRequired[SnsActionTypeDef],
        "sqs": NotRequired[SqsActionTypeDef],
        "kinesis": NotRequired[KinesisActionTypeDef],
        "republish": NotRequired[RepublishActionUnionTypeDef],
        "s3": NotRequired[S3ActionTypeDef],
        "firehose": NotRequired[FirehoseActionTypeDef],
        "cloudwatchMetric": NotRequired[CloudwatchMetricActionTypeDef],
        "cloudwatchAlarm": NotRequired[CloudwatchAlarmActionTypeDef],
        "cloudwatchLogs": NotRequired[CloudwatchLogsActionTypeDef],
        "elasticsearch": NotRequired[ElasticsearchActionTypeDef],
        "salesforce": NotRequired[SalesforceActionTypeDef],
        "iotAnalytics": NotRequired[IotAnalyticsActionTypeDef],
        "iotEvents": NotRequired[IotEventsActionTypeDef],
        "iotSiteWise": NotRequired[IotSiteWiseActionUnionTypeDef],
        "stepFunctions": NotRequired[StepFunctionsActionTypeDef],
        "timestream": NotRequired[TimestreamActionUnionTypeDef],
        "http": NotRequired[HttpActionUnionTypeDef],
        "kafka": NotRequired[KafkaActionUnionTypeDef],
        "openSearch": NotRequired[OpenSearchActionTypeDef],
        "location": NotRequired[LocationActionTypeDef],
    },
)
CodeSigningUnionTypeDef = Union[CodeSigningTypeDef, CodeSigningOutputTypeDef]


class GetOTAUpdateResponseTypeDef(TypedDict):
    otaUpdateInfo: OTAUpdateInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSecurityProfileRequestTypeDef(TypedDict):
    securityProfileName: str
    securityProfileDescription: NotRequired[str]
    behaviors: NotRequired[Sequence[BehaviorUnionTypeDef]]
    alertTargets: NotRequired[Mapping[Literal["SNS"], AlertTargetTypeDef]]
    additionalMetricsToRetain: NotRequired[Sequence[str]]
    additionalMetricsToRetainV2: NotRequired[Sequence[MetricToRetainTypeDef]]
    tags: NotRequired[Sequence[TagTypeDef]]
    metricsExportConfig: NotRequired[MetricsExportConfigTypeDef]


class UpdateSecurityProfileRequestTypeDef(TypedDict):
    securityProfileName: str
    securityProfileDescription: NotRequired[str]
    behaviors: NotRequired[Sequence[BehaviorUnionTypeDef]]
    alertTargets: NotRequired[Mapping[Literal["SNS"], AlertTargetTypeDef]]
    additionalMetricsToRetain: NotRequired[Sequence[str]]
    additionalMetricsToRetainV2: NotRequired[Sequence[MetricToRetainTypeDef]]
    deleteBehaviors: NotRequired[bool]
    deleteAlertTargets: NotRequired[bool]
    deleteAdditionalMetricsToRetain: NotRequired[bool]
    expectedVersion: NotRequired[int]
    metricsExportConfig: NotRequired[MetricsExportConfigTypeDef]
    deleteMetricsExportConfig: NotRequired[bool]


class ValidateSecurityProfileBehaviorsRequestTypeDef(TypedDict):
    behaviors: Sequence[BehaviorUnionTypeDef]


ActionUnionTypeDef = Union[ActionTypeDef, ActionOutputTypeDef]


class OTAUpdateFileTypeDef(TypedDict):
    fileName: NotRequired[str]
    fileType: NotRequired[int]
    fileVersion: NotRequired[str]
    fileLocation: NotRequired[FileLocationTypeDef]
    codeSigning: NotRequired[CodeSigningUnionTypeDef]
    attributes: NotRequired[Mapping[str, str]]


class TopicRulePayloadTypeDef(TypedDict):
    sql: str
    actions: Sequence[ActionUnionTypeDef]
    description: NotRequired[str]
    ruleDisabled: NotRequired[bool]
    awsIotSqlVersion: NotRequired[str]
    errorAction: NotRequired[ActionUnionTypeDef]


OTAUpdateFileUnionTypeDef = Union[OTAUpdateFileTypeDef, OTAUpdateFileOutputTypeDef]


class CreateTopicRuleRequestTypeDef(TypedDict):
    ruleName: str
    topicRulePayload: TopicRulePayloadTypeDef
    tags: NotRequired[str]


class ReplaceTopicRuleRequestTypeDef(TypedDict):
    ruleName: str
    topicRulePayload: TopicRulePayloadTypeDef


class CreateOTAUpdateRequestTypeDef(TypedDict):
    otaUpdateId: str
    targets: Sequence[str]
    files: Sequence[OTAUpdateFileUnionTypeDef]
    roleArn: str
    description: NotRequired[str]
    protocols: NotRequired[Sequence[ProtocolType]]
    targetSelection: NotRequired[TargetSelectionType]
    awsJobExecutionsRolloutConfig: NotRequired[AwsJobExecutionsRolloutConfigTypeDef]
    awsJobPresignedUrlConfig: NotRequired[AwsJobPresignedUrlConfigTypeDef]
    awsJobAbortConfig: NotRequired[AwsJobAbortConfigTypeDef]
    awsJobTimeoutConfig: NotRequired[AwsJobTimeoutConfigTypeDef]
    additionalParameters: NotRequired[Mapping[str, str]]
    tags: NotRequired[Sequence[TagTypeDef]]
