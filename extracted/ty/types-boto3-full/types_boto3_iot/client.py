"""
Type annotations for iot service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iot.client import IoTClient

    session = Session()
    client: IoTClient = session.client("iot")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    GetBehaviorModelTrainingSummariesPaginator,
    ListActiveViolationsPaginator,
    ListAttachedPoliciesPaginator,
    ListAuditFindingsPaginator,
    ListAuditMitigationActionsExecutionsPaginator,
    ListAuditMitigationActionsTasksPaginator,
    ListAuditSuppressionsPaginator,
    ListAuditTasksPaginator,
    ListAuthorizersPaginator,
    ListBillingGroupsPaginator,
    ListCACertificatesPaginator,
    ListCertificatesByCAPaginator,
    ListCertificatesPaginator,
    ListCommandExecutionsPaginator,
    ListCommandsPaginator,
    ListCustomMetricsPaginator,
    ListDetectMitigationActionsExecutionsPaginator,
    ListDetectMitigationActionsTasksPaginator,
    ListDimensionsPaginator,
    ListDomainConfigurationsPaginator,
    ListFleetMetricsPaginator,
    ListIndicesPaginator,
    ListJobExecutionsForJobPaginator,
    ListJobExecutionsForThingPaginator,
    ListJobsPaginator,
    ListJobTemplatesPaginator,
    ListManagedJobTemplatesPaginator,
    ListMetricValuesPaginator,
    ListMitigationActionsPaginator,
    ListOTAUpdatesPaginator,
    ListOutgoingCertificatesPaginator,
    ListPackagesPaginator,
    ListPackageVersionsPaginator,
    ListPoliciesPaginator,
    ListPolicyPrincipalsPaginator,
    ListPrincipalPoliciesPaginator,
    ListPrincipalThingsPaginator,
    ListPrincipalThingsV2Paginator,
    ListProvisioningTemplatesPaginator,
    ListProvisioningTemplateVersionsPaginator,
    ListRelatedResourcesForAuditFindingPaginator,
    ListRoleAliasesPaginator,
    ListSbomValidationResultsPaginator,
    ListScheduledAuditsPaginator,
    ListSecurityProfilesForTargetPaginator,
    ListSecurityProfilesPaginator,
    ListStreamsPaginator,
    ListTagsForResourcePaginator,
    ListTargetsForPolicyPaginator,
    ListTargetsForSecurityProfilePaginator,
    ListThingGroupsForThingPaginator,
    ListThingGroupsPaginator,
    ListThingPrincipalsPaginator,
    ListThingPrincipalsV2Paginator,
    ListThingRegistrationTaskReportsPaginator,
    ListThingRegistrationTasksPaginator,
    ListThingsInBillingGroupPaginator,
    ListThingsInThingGroupPaginator,
    ListThingsPaginator,
    ListThingTypesPaginator,
    ListTopicRuleDestinationsPaginator,
    ListTopicRulesPaginator,
    ListV2LoggingLevelsPaginator,
    ListViolationEventsPaginator,
)
from .type_defs import (
    AcceptCertificateTransferRequestTypeDef,
    AddThingToBillingGroupRequestTypeDef,
    AddThingToThingGroupRequestTypeDef,
    AssociateSbomWithPackageVersionRequestTypeDef,
    AssociateSbomWithPackageVersionResponseTypeDef,
    AssociateTargetsWithJobRequestTypeDef,
    AssociateTargetsWithJobResponseTypeDef,
    AttachPolicyRequestTypeDef,
    AttachPrincipalPolicyRequestTypeDef,
    AttachSecurityProfileRequestTypeDef,
    AttachThingPrincipalRequestTypeDef,
    CancelAuditMitigationActionsTaskRequestTypeDef,
    CancelAuditTaskRequestTypeDef,
    CancelCertificateTransferRequestTypeDef,
    CancelDetectMitigationActionsTaskRequestTypeDef,
    CancelJobExecutionRequestTypeDef,
    CancelJobRequestTypeDef,
    CancelJobResponseTypeDef,
    ConfirmTopicRuleDestinationRequestTypeDef,
    CreateAuditSuppressionRequestTypeDef,
    CreateAuthorizerRequestTypeDef,
    CreateAuthorizerResponseTypeDef,
    CreateBillingGroupRequestTypeDef,
    CreateBillingGroupResponseTypeDef,
    CreateCertificateFromCsrRequestTypeDef,
    CreateCertificateFromCsrResponseTypeDef,
    CreateCertificateProviderRequestTypeDef,
    CreateCertificateProviderResponseTypeDef,
    CreateCommandRequestTypeDef,
    CreateCommandResponseTypeDef,
    CreateCustomMetricRequestTypeDef,
    CreateCustomMetricResponseTypeDef,
    CreateDimensionRequestTypeDef,
    CreateDimensionResponseTypeDef,
    CreateDomainConfigurationRequestTypeDef,
    CreateDomainConfigurationResponseTypeDef,
    CreateDynamicThingGroupRequestTypeDef,
    CreateDynamicThingGroupResponseTypeDef,
    CreateFleetMetricRequestTypeDef,
    CreateFleetMetricResponseTypeDef,
    CreateJobRequestTypeDef,
    CreateJobResponseTypeDef,
    CreateJobTemplateRequestTypeDef,
    CreateJobTemplateResponseTypeDef,
    CreateKeysAndCertificateRequestTypeDef,
    CreateKeysAndCertificateResponseTypeDef,
    CreateMitigationActionRequestTypeDef,
    CreateMitigationActionResponseTypeDef,
    CreateOTAUpdateRequestTypeDef,
    CreateOTAUpdateResponseTypeDef,
    CreatePackageRequestTypeDef,
    CreatePackageResponseTypeDef,
    CreatePackageVersionRequestTypeDef,
    CreatePackageVersionResponseTypeDef,
    CreatePolicyRequestTypeDef,
    CreatePolicyResponseTypeDef,
    CreatePolicyVersionRequestTypeDef,
    CreatePolicyVersionResponseTypeDef,
    CreateProvisioningClaimRequestTypeDef,
    CreateProvisioningClaimResponseTypeDef,
    CreateProvisioningTemplateRequestTypeDef,
    CreateProvisioningTemplateResponseTypeDef,
    CreateProvisioningTemplateVersionRequestTypeDef,
    CreateProvisioningTemplateVersionResponseTypeDef,
    CreateRoleAliasRequestTypeDef,
    CreateRoleAliasResponseTypeDef,
    CreateScheduledAuditRequestTypeDef,
    CreateScheduledAuditResponseTypeDef,
    CreateSecurityProfileRequestTypeDef,
    CreateSecurityProfileResponseTypeDef,
    CreateStreamRequestTypeDef,
    CreateStreamResponseTypeDef,
    CreateThingGroupRequestTypeDef,
    CreateThingGroupResponseTypeDef,
    CreateThingRequestTypeDef,
    CreateThingResponseTypeDef,
    CreateThingTypeRequestTypeDef,
    CreateThingTypeResponseTypeDef,
    CreateTopicRuleDestinationRequestTypeDef,
    CreateTopicRuleDestinationResponseTypeDef,
    CreateTopicRuleRequestTypeDef,
    DeleteAccountAuditConfigurationRequestTypeDef,
    DeleteAuditSuppressionRequestTypeDef,
    DeleteAuthorizerRequestTypeDef,
    DeleteBillingGroupRequestTypeDef,
    DeleteCACertificateRequestTypeDef,
    DeleteCertificateProviderRequestTypeDef,
    DeleteCertificateRequestTypeDef,
    DeleteCommandExecutionRequestTypeDef,
    DeleteCommandRequestTypeDef,
    DeleteCommandResponseTypeDef,
    DeleteCustomMetricRequestTypeDef,
    DeleteDimensionRequestTypeDef,
    DeleteDomainConfigurationRequestTypeDef,
    DeleteDynamicThingGroupRequestTypeDef,
    DeleteFleetMetricRequestTypeDef,
    DeleteJobExecutionRequestTypeDef,
    DeleteJobRequestTypeDef,
    DeleteJobTemplateRequestTypeDef,
    DeleteMitigationActionRequestTypeDef,
    DeleteOTAUpdateRequestTypeDef,
    DeletePackageRequestTypeDef,
    DeletePackageVersionRequestTypeDef,
    DeletePolicyRequestTypeDef,
    DeletePolicyVersionRequestTypeDef,
    DeleteProvisioningTemplateRequestTypeDef,
    DeleteProvisioningTemplateVersionRequestTypeDef,
    DeleteRoleAliasRequestTypeDef,
    DeleteScheduledAuditRequestTypeDef,
    DeleteSecurityProfileRequestTypeDef,
    DeleteStreamRequestTypeDef,
    DeleteThingGroupRequestTypeDef,
    DeleteThingRequestTypeDef,
    DeleteThingTypeRequestTypeDef,
    DeleteTopicRuleDestinationRequestTypeDef,
    DeleteTopicRuleRequestTypeDef,
    DeleteV2LoggingLevelRequestTypeDef,
    DeprecateThingTypeRequestTypeDef,
    DescribeAccountAuditConfigurationResponseTypeDef,
    DescribeAuditFindingRequestTypeDef,
    DescribeAuditFindingResponseTypeDef,
    DescribeAuditMitigationActionsTaskRequestTypeDef,
    DescribeAuditMitigationActionsTaskResponseTypeDef,
    DescribeAuditSuppressionRequestTypeDef,
    DescribeAuditSuppressionResponseTypeDef,
    DescribeAuditTaskRequestTypeDef,
    DescribeAuditTaskResponseTypeDef,
    DescribeAuthorizerRequestTypeDef,
    DescribeAuthorizerResponseTypeDef,
    DescribeBillingGroupRequestTypeDef,
    DescribeBillingGroupResponseTypeDef,
    DescribeCACertificateRequestTypeDef,
    DescribeCACertificateResponseTypeDef,
    DescribeCertificateProviderRequestTypeDef,
    DescribeCertificateProviderResponseTypeDef,
    DescribeCertificateRequestTypeDef,
    DescribeCertificateResponseTypeDef,
    DescribeCustomMetricRequestTypeDef,
    DescribeCustomMetricResponseTypeDef,
    DescribeDefaultAuthorizerResponseTypeDef,
    DescribeDetectMitigationActionsTaskRequestTypeDef,
    DescribeDetectMitigationActionsTaskResponseTypeDef,
    DescribeDimensionRequestTypeDef,
    DescribeDimensionResponseTypeDef,
    DescribeDomainConfigurationRequestTypeDef,
    DescribeDomainConfigurationResponseTypeDef,
    DescribeEndpointRequestTypeDef,
    DescribeEndpointResponseTypeDef,
    DescribeEventConfigurationsResponseTypeDef,
    DescribeFleetMetricRequestTypeDef,
    DescribeFleetMetricResponseTypeDef,
    DescribeIndexRequestTypeDef,
    DescribeIndexResponseTypeDef,
    DescribeJobExecutionRequestTypeDef,
    DescribeJobExecutionResponseTypeDef,
    DescribeJobRequestTypeDef,
    DescribeJobResponseTypeDef,
    DescribeJobTemplateRequestTypeDef,
    DescribeJobTemplateResponseTypeDef,
    DescribeManagedJobTemplateRequestTypeDef,
    DescribeManagedJobTemplateResponseTypeDef,
    DescribeMitigationActionRequestTypeDef,
    DescribeMitigationActionResponseTypeDef,
    DescribeProvisioningTemplateRequestTypeDef,
    DescribeProvisioningTemplateResponseTypeDef,
    DescribeProvisioningTemplateVersionRequestTypeDef,
    DescribeProvisioningTemplateVersionResponseTypeDef,
    DescribeRoleAliasRequestTypeDef,
    DescribeRoleAliasResponseTypeDef,
    DescribeScheduledAuditRequestTypeDef,
    DescribeScheduledAuditResponseTypeDef,
    DescribeSecurityProfileRequestTypeDef,
    DescribeSecurityProfileResponseTypeDef,
    DescribeStreamRequestTypeDef,
    DescribeStreamResponseTypeDef,
    DescribeThingGroupRequestTypeDef,
    DescribeThingGroupResponseTypeDef,
    DescribeThingRegistrationTaskRequestTypeDef,
    DescribeThingRegistrationTaskResponseTypeDef,
    DescribeThingRequestTypeDef,
    DescribeThingResponseTypeDef,
    DescribeThingTypeRequestTypeDef,
    DescribeThingTypeResponseTypeDef,
    DetachPolicyRequestTypeDef,
    DetachPrincipalPolicyRequestTypeDef,
    DetachSecurityProfileRequestTypeDef,
    DetachThingPrincipalRequestTypeDef,
    DisableTopicRuleRequestTypeDef,
    DisassociateSbomFromPackageVersionRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableTopicRuleRequestTypeDef,
    GetBehaviorModelTrainingSummariesRequestTypeDef,
    GetBehaviorModelTrainingSummariesResponseTypeDef,
    GetBucketsAggregationRequestTypeDef,
    GetBucketsAggregationResponseTypeDef,
    GetCardinalityRequestTypeDef,
    GetCardinalityResponseTypeDef,
    GetCommandExecutionRequestTypeDef,
    GetCommandExecutionResponseTypeDef,
    GetCommandRequestTypeDef,
    GetCommandResponseTypeDef,
    GetEffectivePoliciesRequestTypeDef,
    GetEffectivePoliciesResponseTypeDef,
    GetIndexingConfigurationResponseTypeDef,
    GetJobDocumentRequestTypeDef,
    GetJobDocumentResponseTypeDef,
    GetLoggingOptionsResponseTypeDef,
    GetOTAUpdateRequestTypeDef,
    GetOTAUpdateResponseTypeDef,
    GetPackageConfigurationResponseTypeDef,
    GetPackageRequestTypeDef,
    GetPackageResponseTypeDef,
    GetPackageVersionRequestTypeDef,
    GetPackageVersionResponseTypeDef,
    GetPercentilesRequestTypeDef,
    GetPercentilesResponseTypeDef,
    GetPolicyRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetPolicyVersionRequestTypeDef,
    GetPolicyVersionResponseTypeDef,
    GetRegistrationCodeResponseTypeDef,
    GetStatisticsRequestTypeDef,
    GetStatisticsResponseTypeDef,
    GetThingConnectivityDataRequestTypeDef,
    GetThingConnectivityDataResponseTypeDef,
    GetTopicRuleDestinationRequestTypeDef,
    GetTopicRuleDestinationResponseTypeDef,
    GetTopicRuleRequestTypeDef,
    GetTopicRuleResponseTypeDef,
    GetV2LoggingOptionsResponseTypeDef,
    ListActiveViolationsRequestTypeDef,
    ListActiveViolationsResponseTypeDef,
    ListAttachedPoliciesRequestTypeDef,
    ListAttachedPoliciesResponseTypeDef,
    ListAuditFindingsRequestTypeDef,
    ListAuditFindingsResponseTypeDef,
    ListAuditMitigationActionsExecutionsRequestTypeDef,
    ListAuditMitigationActionsExecutionsResponseTypeDef,
    ListAuditMitigationActionsTasksRequestTypeDef,
    ListAuditMitigationActionsTasksResponseTypeDef,
    ListAuditSuppressionsRequestTypeDef,
    ListAuditSuppressionsResponseTypeDef,
    ListAuditTasksRequestTypeDef,
    ListAuditTasksResponseTypeDef,
    ListAuthorizersRequestTypeDef,
    ListAuthorizersResponseTypeDef,
    ListBillingGroupsRequestTypeDef,
    ListBillingGroupsResponseTypeDef,
    ListCACertificatesRequestTypeDef,
    ListCACertificatesResponseTypeDef,
    ListCertificateProvidersRequestTypeDef,
    ListCertificateProvidersResponseTypeDef,
    ListCertificatesByCARequestTypeDef,
    ListCertificatesByCAResponseTypeDef,
    ListCertificatesRequestTypeDef,
    ListCertificatesResponseTypeDef,
    ListCommandExecutionsRequestTypeDef,
    ListCommandExecutionsResponseTypeDef,
    ListCommandsRequestTypeDef,
    ListCommandsResponseTypeDef,
    ListCustomMetricsRequestTypeDef,
    ListCustomMetricsResponseTypeDef,
    ListDetectMitigationActionsExecutionsRequestTypeDef,
    ListDetectMitigationActionsExecutionsResponseTypeDef,
    ListDetectMitigationActionsTasksRequestTypeDef,
    ListDetectMitigationActionsTasksResponseTypeDef,
    ListDimensionsRequestTypeDef,
    ListDimensionsResponseTypeDef,
    ListDomainConfigurationsRequestTypeDef,
    ListDomainConfigurationsResponseTypeDef,
    ListFleetMetricsRequestTypeDef,
    ListFleetMetricsResponseTypeDef,
    ListIndicesRequestTypeDef,
    ListIndicesResponseTypeDef,
    ListJobExecutionsForJobRequestTypeDef,
    ListJobExecutionsForJobResponseTypeDef,
    ListJobExecutionsForThingRequestTypeDef,
    ListJobExecutionsForThingResponseTypeDef,
    ListJobsRequestTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesRequestTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListManagedJobTemplatesRequestTypeDef,
    ListManagedJobTemplatesResponseTypeDef,
    ListMetricValuesRequestTypeDef,
    ListMetricValuesResponseTypeDef,
    ListMitigationActionsRequestTypeDef,
    ListMitigationActionsResponseTypeDef,
    ListOTAUpdatesRequestTypeDef,
    ListOTAUpdatesResponseTypeDef,
    ListOutgoingCertificatesRequestTypeDef,
    ListOutgoingCertificatesResponseTypeDef,
    ListPackagesRequestTypeDef,
    ListPackagesResponseTypeDef,
    ListPackageVersionsRequestTypeDef,
    ListPackageVersionsResponseTypeDef,
    ListPoliciesRequestTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyPrincipalsRequestTypeDef,
    ListPolicyPrincipalsResponseTypeDef,
    ListPolicyVersionsRequestTypeDef,
    ListPolicyVersionsResponseTypeDef,
    ListPrincipalPoliciesRequestTypeDef,
    ListPrincipalPoliciesResponseTypeDef,
    ListPrincipalThingsRequestTypeDef,
    ListPrincipalThingsResponseTypeDef,
    ListPrincipalThingsV2RequestTypeDef,
    ListPrincipalThingsV2ResponseTypeDef,
    ListProvisioningTemplatesRequestTypeDef,
    ListProvisioningTemplatesResponseTypeDef,
    ListProvisioningTemplateVersionsRequestTypeDef,
    ListProvisioningTemplateVersionsResponseTypeDef,
    ListRelatedResourcesForAuditFindingRequestTypeDef,
    ListRelatedResourcesForAuditFindingResponseTypeDef,
    ListRoleAliasesRequestTypeDef,
    ListRoleAliasesResponseTypeDef,
    ListSbomValidationResultsRequestTypeDef,
    ListSbomValidationResultsResponseTypeDef,
    ListScheduledAuditsRequestTypeDef,
    ListScheduledAuditsResponseTypeDef,
    ListSecurityProfilesForTargetRequestTypeDef,
    ListSecurityProfilesForTargetResponseTypeDef,
    ListSecurityProfilesRequestTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListStreamsRequestTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyRequestTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    ListTargetsForSecurityProfileRequestTypeDef,
    ListTargetsForSecurityProfileResponseTypeDef,
    ListThingGroupsForThingRequestTypeDef,
    ListThingGroupsForThingResponseTypeDef,
    ListThingGroupsRequestTypeDef,
    ListThingGroupsResponseTypeDef,
    ListThingPrincipalsRequestTypeDef,
    ListThingPrincipalsResponseTypeDef,
    ListThingPrincipalsV2RequestTypeDef,
    ListThingPrincipalsV2ResponseTypeDef,
    ListThingRegistrationTaskReportsRequestTypeDef,
    ListThingRegistrationTaskReportsResponseTypeDef,
    ListThingRegistrationTasksRequestTypeDef,
    ListThingRegistrationTasksResponseTypeDef,
    ListThingsInBillingGroupRequestTypeDef,
    ListThingsInBillingGroupResponseTypeDef,
    ListThingsInThingGroupRequestTypeDef,
    ListThingsInThingGroupResponseTypeDef,
    ListThingsRequestTypeDef,
    ListThingsResponseTypeDef,
    ListThingTypesRequestTypeDef,
    ListThingTypesResponseTypeDef,
    ListTopicRuleDestinationsRequestTypeDef,
    ListTopicRuleDestinationsResponseTypeDef,
    ListTopicRulesRequestTypeDef,
    ListTopicRulesResponseTypeDef,
    ListV2LoggingLevelsRequestTypeDef,
    ListV2LoggingLevelsResponseTypeDef,
    ListViolationEventsRequestTypeDef,
    ListViolationEventsResponseTypeDef,
    PutVerificationStateOnViolationRequestTypeDef,
    RegisterCACertificateRequestTypeDef,
    RegisterCACertificateResponseTypeDef,
    RegisterCertificateRequestTypeDef,
    RegisterCertificateResponseTypeDef,
    RegisterCertificateWithoutCARequestTypeDef,
    RegisterCertificateWithoutCAResponseTypeDef,
    RegisterThingRequestTypeDef,
    RegisterThingResponseTypeDef,
    RejectCertificateTransferRequestTypeDef,
    RemoveThingFromBillingGroupRequestTypeDef,
    RemoveThingFromThingGroupRequestTypeDef,
    ReplaceTopicRuleRequestTypeDef,
    SearchIndexRequestTypeDef,
    SearchIndexResponseTypeDef,
    SetDefaultAuthorizerRequestTypeDef,
    SetDefaultAuthorizerResponseTypeDef,
    SetDefaultPolicyVersionRequestTypeDef,
    SetLoggingOptionsRequestTypeDef,
    SetV2LoggingLevelRequestTypeDef,
    SetV2LoggingOptionsRequestTypeDef,
    StartAuditMitigationActionsTaskRequestTypeDef,
    StartAuditMitigationActionsTaskResponseTypeDef,
    StartDetectMitigationActionsTaskRequestTypeDef,
    StartDetectMitigationActionsTaskResponseTypeDef,
    StartOnDemandAuditTaskRequestTypeDef,
    StartOnDemandAuditTaskResponseTypeDef,
    StartThingRegistrationTaskRequestTypeDef,
    StartThingRegistrationTaskResponseTypeDef,
    StopThingRegistrationTaskRequestTypeDef,
    TagResourceRequestTypeDef,
    TestAuthorizationRequestTypeDef,
    TestAuthorizationResponseTypeDef,
    TestInvokeAuthorizerRequestTypeDef,
    TestInvokeAuthorizerResponseTypeDef,
    TransferCertificateRequestTypeDef,
    TransferCertificateResponseTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAccountAuditConfigurationRequestTypeDef,
    UpdateAuditSuppressionRequestTypeDef,
    UpdateAuthorizerRequestTypeDef,
    UpdateAuthorizerResponseTypeDef,
    UpdateBillingGroupRequestTypeDef,
    UpdateBillingGroupResponseTypeDef,
    UpdateCACertificateRequestTypeDef,
    UpdateCertificateProviderRequestTypeDef,
    UpdateCertificateProviderResponseTypeDef,
    UpdateCertificateRequestTypeDef,
    UpdateCommandRequestTypeDef,
    UpdateCommandResponseTypeDef,
    UpdateCustomMetricRequestTypeDef,
    UpdateCustomMetricResponseTypeDef,
    UpdateDimensionRequestTypeDef,
    UpdateDimensionResponseTypeDef,
    UpdateDomainConfigurationRequestTypeDef,
    UpdateDomainConfigurationResponseTypeDef,
    UpdateDynamicThingGroupRequestTypeDef,
    UpdateDynamicThingGroupResponseTypeDef,
    UpdateEventConfigurationsRequestTypeDef,
    UpdateFleetMetricRequestTypeDef,
    UpdateIndexingConfigurationRequestTypeDef,
    UpdateJobRequestTypeDef,
    UpdateMitigationActionRequestTypeDef,
    UpdateMitigationActionResponseTypeDef,
    UpdatePackageConfigurationRequestTypeDef,
    UpdatePackageRequestTypeDef,
    UpdatePackageVersionRequestTypeDef,
    UpdateProvisioningTemplateRequestTypeDef,
    UpdateRoleAliasRequestTypeDef,
    UpdateRoleAliasResponseTypeDef,
    UpdateScheduledAuditRequestTypeDef,
    UpdateScheduledAuditResponseTypeDef,
    UpdateSecurityProfileRequestTypeDef,
    UpdateSecurityProfileResponseTypeDef,
    UpdateStreamRequestTypeDef,
    UpdateStreamResponseTypeDef,
    UpdateThingGroupRequestTypeDef,
    UpdateThingGroupResponseTypeDef,
    UpdateThingGroupsForThingRequestTypeDef,
    UpdateThingRequestTypeDef,
    UpdateThingTypeRequestTypeDef,
    UpdateTopicRuleDestinationRequestTypeDef,
    ValidateSecurityProfileBehaviorsRequestTypeDef,
    ValidateSecurityProfileBehaviorsResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("IoTClient",)


class Exceptions(BaseClientExceptions):
    CertificateConflictException: Type[BotocoreClientError]
    CertificateStateException: Type[BotocoreClientError]
    CertificateValidationException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ConflictingResourceUpdateException: Type[BotocoreClientError]
    DeleteConflictException: Type[BotocoreClientError]
    IndexNotReadyException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidAggregationException: Type[BotocoreClientError]
    InvalidQueryException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    InvalidResponseException: Type[BotocoreClientError]
    InvalidStateTransitionException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyException: Type[BotocoreClientError]
    NotConfiguredException: Type[BotocoreClientError]
    RegistrationCodeValidationException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceRegistrationFailureException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    SqlParseException: Type[BotocoreClientError]
    TaskAlreadyExistsException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TransferAlreadyCompletedException: Type[BotocoreClientError]
    TransferConflictException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]
    VersionConflictException: Type[BotocoreClientError]
    VersionsLimitExceededException: Type[BotocoreClientError]


class IoTClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html#IoT.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#generate_presigned_url)
        """

    def accept_certificate_transfer(
        self, **kwargs: Unpack[AcceptCertificateTransferRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Accepts a pending certificate transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/accept_certificate_transfer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#accept_certificate_transfer)
        """

    def add_thing_to_billing_group(
        self, **kwargs: Unpack[AddThingToBillingGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a thing to a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/add_thing_to_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#add_thing_to_billing_group)
        """

    def add_thing_to_thing_group(
        self, **kwargs: Unpack[AddThingToThingGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a thing to a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/add_thing_to_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#add_thing_to_thing_group)
        """

    def associate_sbom_with_package_version(
        self, **kwargs: Unpack[AssociateSbomWithPackageVersionRequestTypeDef]
    ) -> AssociateSbomWithPackageVersionResponseTypeDef:
        """
        Associates the selected software bill of materials (SBOM) with a specific
        software package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/associate_sbom_with_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#associate_sbom_with_package_version)
        """

    def associate_targets_with_job(
        self, **kwargs: Unpack[AssociateTargetsWithJobRequestTypeDef]
    ) -> AssociateTargetsWithJobResponseTypeDef:
        """
        Associates a group with a continuous job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/associate_targets_with_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#associate_targets_with_job)
        """

    def attach_policy(
        self, **kwargs: Unpack[AttachPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches the specified policy to the specified principal (certificate or other
        credential).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/attach_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#attach_policy)
        """

    def attach_principal_policy(
        self, **kwargs: Unpack[AttachPrincipalPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches the specified policy to the specified principal (certificate or other
        credential).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/attach_principal_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#attach_principal_policy)
        """

    def attach_security_profile(
        self, **kwargs: Unpack[AttachSecurityProfileRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a Device Defender security profile with a thing group or this
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/attach_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#attach_security_profile)
        """

    def attach_thing_principal(
        self, **kwargs: Unpack[AttachThingPrincipalRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Attaches the specified principal to the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/attach_thing_principal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#attach_thing_principal)
        """

    def cancel_audit_mitigation_actions_task(
        self, **kwargs: Unpack[CancelAuditMitigationActionsTaskRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a mitigation action task that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_audit_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_audit_mitigation_actions_task)
        """

    def cancel_audit_task(self, **kwargs: Unpack[CancelAuditTaskRequestTypeDef]) -> Dict[str, Any]:
        """
        Cancels an audit that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_audit_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_audit_task)
        """

    def cancel_certificate_transfer(
        self, **kwargs: Unpack[CancelCertificateTransferRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels a pending transfer for the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_certificate_transfer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_certificate_transfer)
        """

    def cancel_detect_mitigation_actions_task(
        self, **kwargs: Unpack[CancelDetectMitigationActionsTaskRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a Device Defender ML Detect mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_detect_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_detect_mitigation_actions_task)
        """

    def cancel_job(self, **kwargs: Unpack[CancelJobRequestTypeDef]) -> CancelJobResponseTypeDef:
        """
        Cancels a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_job)
        """

    def cancel_job_execution(
        self, **kwargs: Unpack[CancelJobExecutionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels the execution of a job for a given thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/cancel_job_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#cancel_job_execution)
        """

    def clear_default_authorizer(self) -> Dict[str, Any]:
        """
        Clears the default authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/clear_default_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#clear_default_authorizer)
        """

    def confirm_topic_rule_destination(
        self, **kwargs: Unpack[ConfirmTopicRuleDestinationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Confirms a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/confirm_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#confirm_topic_rule_destination)
        """

    def create_audit_suppression(
        self, **kwargs: Unpack[CreateAuditSuppressionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_audit_suppression.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_audit_suppression)
        """

    def create_authorizer(
        self, **kwargs: Unpack[CreateAuthorizerRequestTypeDef]
    ) -> CreateAuthorizerResponseTypeDef:
        """
        Creates an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_authorizer)
        """

    def create_billing_group(
        self, **kwargs: Unpack[CreateBillingGroupRequestTypeDef]
    ) -> CreateBillingGroupResponseTypeDef:
        """
        Creates a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_billing_group)
        """

    def create_certificate_from_csr(
        self, **kwargs: Unpack[CreateCertificateFromCsrRequestTypeDef]
    ) -> CreateCertificateFromCsrResponseTypeDef:
        """
        Creates an X.509 certificate using the specified certificate signing request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_certificate_from_csr.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_certificate_from_csr)
        """

    def create_certificate_provider(
        self, **kwargs: Unpack[CreateCertificateProviderRequestTypeDef]
    ) -> CreateCertificateProviderResponseTypeDef:
        """
        Creates an Amazon Web Services IoT Core certificate provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_certificate_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_certificate_provider)
        """

    def create_command(
        self, **kwargs: Unpack[CreateCommandRequestTypeDef]
    ) -> CreateCommandResponseTypeDef:
        """
        Creates a command.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_command)
        """

    def create_custom_metric(
        self, **kwargs: Unpack[CreateCustomMetricRequestTypeDef]
    ) -> CreateCustomMetricResponseTypeDef:
        """
        Use this API to define a Custom Metric published by your devices to Device
        Defender.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_custom_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_custom_metric)
        """

    def create_dimension(
        self, **kwargs: Unpack[CreateDimensionRequestTypeDef]
    ) -> CreateDimensionResponseTypeDef:
        """
        Create a dimension that you can use to limit the scope of a metric used in a
        security profile for IoT Device Defender.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_dimension.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_dimension)
        """

    def create_domain_configuration(
        self, **kwargs: Unpack[CreateDomainConfigurationRequestTypeDef]
    ) -> CreateDomainConfigurationResponseTypeDef:
        """
        Creates a domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_domain_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_domain_configuration)
        """

    def create_dynamic_thing_group(
        self, **kwargs: Unpack[CreateDynamicThingGroupRequestTypeDef]
    ) -> CreateDynamicThingGroupResponseTypeDef:
        """
        Creates a dynamic thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_dynamic_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_dynamic_thing_group)
        """

    def create_fleet_metric(
        self, **kwargs: Unpack[CreateFleetMetricRequestTypeDef]
    ) -> CreateFleetMetricResponseTypeDef:
        """
        Creates a fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_fleet_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_fleet_metric)
        """

    def create_job(self, **kwargs: Unpack[CreateJobRequestTypeDef]) -> CreateJobResponseTypeDef:
        """
        Creates a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_job)
        """

    def create_job_template(
        self, **kwargs: Unpack[CreateJobTemplateRequestTypeDef]
    ) -> CreateJobTemplateResponseTypeDef:
        """
        Creates a job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_job_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_job_template)
        """

    def create_keys_and_certificate(
        self, **kwargs: Unpack[CreateKeysAndCertificateRequestTypeDef]
    ) -> CreateKeysAndCertificateResponseTypeDef:
        """
        Creates a 2048-bit RSA key pair and issues an X.509 certificate using the
        issued public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_keys_and_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_keys_and_certificate)
        """

    def create_mitigation_action(
        self, **kwargs: Unpack[CreateMitigationActionRequestTypeDef]
    ) -> CreateMitigationActionResponseTypeDef:
        """
        Defines an action that can be applied to audit findings by using
        StartAuditMitigationActionsTask.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_mitigation_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_mitigation_action)
        """

    def create_ota_update(
        self, **kwargs: Unpack[CreateOTAUpdateRequestTypeDef]
    ) -> CreateOTAUpdateResponseTypeDef:
        """
        Creates an IoT OTA update on a target group of things or groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_ota_update.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_ota_update)
        """

    def create_package(
        self, **kwargs: Unpack[CreatePackageRequestTypeDef]
    ) -> CreatePackageResponseTypeDef:
        """
        Creates an IoT software package that can be deployed to your fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_package)
        """

    def create_package_version(
        self, **kwargs: Unpack[CreatePackageVersionRequestTypeDef]
    ) -> CreatePackageVersionResponseTypeDef:
        """
        Creates a new version for an existing IoT software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_package_version)
        """

    def create_policy(
        self, **kwargs: Unpack[CreatePolicyRequestTypeDef]
    ) -> CreatePolicyResponseTypeDef:
        """
        Creates an IoT policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_policy)
        """

    def create_policy_version(
        self, **kwargs: Unpack[CreatePolicyVersionRequestTypeDef]
    ) -> CreatePolicyVersionResponseTypeDef:
        """
        Creates a new version of the specified IoT policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_policy_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_policy_version)
        """

    def create_provisioning_claim(
        self, **kwargs: Unpack[CreateProvisioningClaimRequestTypeDef]
    ) -> CreateProvisioningClaimResponseTypeDef:
        """
        Creates a provisioning claim.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_provisioning_claim.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_provisioning_claim)
        """

    def create_provisioning_template(
        self, **kwargs: Unpack[CreateProvisioningTemplateRequestTypeDef]
    ) -> CreateProvisioningTemplateResponseTypeDef:
        """
        Creates a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_provisioning_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_provisioning_template)
        """

    def create_provisioning_template_version(
        self, **kwargs: Unpack[CreateProvisioningTemplateVersionRequestTypeDef]
    ) -> CreateProvisioningTemplateVersionResponseTypeDef:
        """
        Creates a new version of a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_provisioning_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_provisioning_template_version)
        """

    def create_role_alias(
        self, **kwargs: Unpack[CreateRoleAliasRequestTypeDef]
    ) -> CreateRoleAliasResponseTypeDef:
        """
        Creates a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_role_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_role_alias)
        """

    def create_scheduled_audit(
        self, **kwargs: Unpack[CreateScheduledAuditRequestTypeDef]
    ) -> CreateScheduledAuditResponseTypeDef:
        """
        Creates a scheduled audit that is run at a specified time interval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_scheduled_audit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_scheduled_audit)
        """

    def create_security_profile(
        self, **kwargs: Unpack[CreateSecurityProfileRequestTypeDef]
    ) -> CreateSecurityProfileResponseTypeDef:
        """
        Creates a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_security_profile)
        """

    def create_stream(
        self, **kwargs: Unpack[CreateStreamRequestTypeDef]
    ) -> CreateStreamResponseTypeDef:
        """
        Creates a stream for delivering one or more large files in chunks over MQTT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_stream)
        """

    def create_thing(
        self, **kwargs: Unpack[CreateThingRequestTypeDef]
    ) -> CreateThingResponseTypeDef:
        """
        Creates a thing record in the registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_thing)
        """

    def create_thing_group(
        self, **kwargs: Unpack[CreateThingGroupRequestTypeDef]
    ) -> CreateThingGroupResponseTypeDef:
        """
        Create a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_thing_group)
        """

    def create_thing_type(
        self, **kwargs: Unpack[CreateThingTypeRequestTypeDef]
    ) -> CreateThingTypeResponseTypeDef:
        """
        Creates a new thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_thing_type)
        """

    def create_topic_rule(
        self, **kwargs: Unpack[CreateTopicRuleRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_topic_rule)
        """

    def create_topic_rule_destination(
        self, **kwargs: Unpack[CreateTopicRuleDestinationRequestTypeDef]
    ) -> CreateTopicRuleDestinationResponseTypeDef:
        """
        Creates a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/create_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#create_topic_rule_destination)
        """

    def delete_account_audit_configuration(
        self, **kwargs: Unpack[DeleteAccountAuditConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Restores the default settings for Device Defender audits for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_account_audit_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_account_audit_configuration)
        """

    def delete_audit_suppression(
        self, **kwargs: Unpack[DeleteAuditSuppressionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_audit_suppression.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_audit_suppression)
        """

    def delete_authorizer(self, **kwargs: Unpack[DeleteAuthorizerRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_authorizer)
        """

    def delete_billing_group(
        self, **kwargs: Unpack[DeleteBillingGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_billing_group)
        """

    def delete_ca_certificate(
        self, **kwargs: Unpack[DeleteCACertificateRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a registered CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_ca_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_ca_certificate)
        """

    def delete_certificate(
        self, **kwargs: Unpack[DeleteCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_certificate)
        """

    def delete_certificate_provider(
        self, **kwargs: Unpack[DeleteCertificateProviderRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a certificate provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_certificate_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_certificate_provider)
        """

    def delete_command(
        self, **kwargs: Unpack[DeleteCommandRequestTypeDef]
    ) -> DeleteCommandResponseTypeDef:
        """
        Delete a command resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_command)
        """

    def delete_command_execution(
        self, **kwargs: Unpack[DeleteCommandExecutionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a command execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_command_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_command_execution)
        """

    def delete_custom_metric(
        self, **kwargs: Unpack[DeleteCustomMetricRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Device Defender detect custom metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_custom_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_custom_metric)
        """

    def delete_dimension(self, **kwargs: Unpack[DeleteDimensionRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified dimension from your Amazon Web Services accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_dimension.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_dimension)
        """

    def delete_domain_configuration(
        self, **kwargs: Unpack[DeleteDomainConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_domain_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_domain_configuration)
        """

    def delete_dynamic_thing_group(
        self, **kwargs: Unpack[DeleteDynamicThingGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a dynamic thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_dynamic_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_dynamic_thing_group)
        """

    def delete_fleet_metric(
        self, **kwargs: Unpack[DeleteFleetMetricRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_fleet_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_fleet_metric)
        """

    def delete_job(self, **kwargs: Unpack[DeleteJobRequestTypeDef]) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a job and its related job executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_job)
        """

    def delete_job_execution(
        self, **kwargs: Unpack[DeleteJobExecutionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_job_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_job_execution)
        """

    def delete_job_template(
        self, **kwargs: Unpack[DeleteJobTemplateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_job_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_job_template)
        """

    def delete_mitigation_action(
        self, **kwargs: Unpack[DeleteMitigationActionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a defined mitigation action from your Amazon Web Services accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_mitigation_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_mitigation_action)
        """

    def delete_ota_update(self, **kwargs: Unpack[DeleteOTAUpdateRequestTypeDef]) -> Dict[str, Any]:
        """
        Delete an OTA update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_ota_update.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_ota_update)
        """

    def delete_package(self, **kwargs: Unpack[DeletePackageRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a specific version from a software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_package)
        """

    def delete_package_version(
        self, **kwargs: Unpack[DeletePackageVersionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specific version from a software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_package_version)
        """

    def delete_policy(
        self, **kwargs: Unpack[DeletePolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_policy)
        """

    def delete_policy_version(
        self, **kwargs: Unpack[DeletePolicyVersionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified version of the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_policy_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_policy_version)
        """

    def delete_provisioning_template(
        self, **kwargs: Unpack[DeleteProvisioningTemplateRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_provisioning_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_provisioning_template)
        """

    def delete_provisioning_template_version(
        self, **kwargs: Unpack[DeleteProvisioningTemplateVersionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a provisioning template version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_provisioning_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_provisioning_template_version)
        """

    def delete_registration_code(self) -> Dict[str, Any]:
        """
        Deletes a CA certificate registration code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_registration_code.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_registration_code)
        """

    def delete_role_alias(self, **kwargs: Unpack[DeleteRoleAliasRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_role_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_role_alias)
        """

    def delete_scheduled_audit(
        self, **kwargs: Unpack[DeleteScheduledAuditRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a scheduled audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_scheduled_audit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_scheduled_audit)
        """

    def delete_security_profile(
        self, **kwargs: Unpack[DeleteSecurityProfileRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_security_profile)
        """

    def delete_stream(self, **kwargs: Unpack[DeleteStreamRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_stream)
        """

    def delete_thing(self, **kwargs: Unpack[DeleteThingRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_thing)
        """

    def delete_thing_group(
        self, **kwargs: Unpack[DeleteThingGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_thing_group)
        """

    def delete_thing_type(self, **kwargs: Unpack[DeleteThingTypeRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_thing_type)
        """

    def delete_topic_rule(
        self, **kwargs: Unpack[DeleteTopicRuleRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_topic_rule)
        """

    def delete_topic_rule_destination(
        self, **kwargs: Unpack[DeleteTopicRuleDestinationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_topic_rule_destination)
        """

    def delete_v2_logging_level(
        self, **kwargs: Unpack[DeleteV2LoggingLevelRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a logging level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/delete_v2_logging_level.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#delete_v2_logging_level)
        """

    def deprecate_thing_type(
        self, **kwargs: Unpack[DeprecateThingTypeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deprecates a thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/deprecate_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#deprecate_thing_type)
        """

    def describe_account_audit_configuration(
        self,
    ) -> DescribeAccountAuditConfigurationResponseTypeDef:
        """
        Gets information about the Device Defender audit settings for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_account_audit_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_account_audit_configuration)
        """

    def describe_audit_finding(
        self, **kwargs: Unpack[DescribeAuditFindingRequestTypeDef]
    ) -> DescribeAuditFindingResponseTypeDef:
        """
        Gets information about a single audit finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_audit_finding.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_audit_finding)
        """

    def describe_audit_mitigation_actions_task(
        self, **kwargs: Unpack[DescribeAuditMitigationActionsTaskRequestTypeDef]
    ) -> DescribeAuditMitigationActionsTaskResponseTypeDef:
        """
        Gets information about an audit mitigation task that is used to apply
        mitigation actions to a set of audit findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_audit_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_audit_mitigation_actions_task)
        """

    def describe_audit_suppression(
        self, **kwargs: Unpack[DescribeAuditSuppressionRequestTypeDef]
    ) -> DescribeAuditSuppressionResponseTypeDef:
        """
        Gets information about a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_audit_suppression.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_audit_suppression)
        """

    def describe_audit_task(
        self, **kwargs: Unpack[DescribeAuditTaskRequestTypeDef]
    ) -> DescribeAuditTaskResponseTypeDef:
        """
        Gets information about a Device Defender audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_audit_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_audit_task)
        """

    def describe_authorizer(
        self, **kwargs: Unpack[DescribeAuthorizerRequestTypeDef]
    ) -> DescribeAuthorizerResponseTypeDef:
        """
        Describes an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_authorizer)
        """

    def describe_billing_group(
        self, **kwargs: Unpack[DescribeBillingGroupRequestTypeDef]
    ) -> DescribeBillingGroupResponseTypeDef:
        """
        Returns information about a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_billing_group)
        """

    def describe_ca_certificate(
        self, **kwargs: Unpack[DescribeCACertificateRequestTypeDef]
    ) -> DescribeCACertificateResponseTypeDef:
        """
        Describes a registered CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_ca_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_ca_certificate)
        """

    def describe_certificate(
        self, **kwargs: Unpack[DescribeCertificateRequestTypeDef]
    ) -> DescribeCertificateResponseTypeDef:
        """
        Gets information about the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_certificate)
        """

    def describe_certificate_provider(
        self, **kwargs: Unpack[DescribeCertificateProviderRequestTypeDef]
    ) -> DescribeCertificateProviderResponseTypeDef:
        """
        Describes a certificate provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_certificate_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_certificate_provider)
        """

    def describe_custom_metric(
        self, **kwargs: Unpack[DescribeCustomMetricRequestTypeDef]
    ) -> DescribeCustomMetricResponseTypeDef:
        """
        Gets information about a Device Defender detect custom metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_custom_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_custom_metric)
        """

    def describe_default_authorizer(self) -> DescribeDefaultAuthorizerResponseTypeDef:
        """
        Describes the default authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_default_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_default_authorizer)
        """

    def describe_detect_mitigation_actions_task(
        self, **kwargs: Unpack[DescribeDetectMitigationActionsTaskRequestTypeDef]
    ) -> DescribeDetectMitigationActionsTaskResponseTypeDef:
        """
        Gets information about a Device Defender ML Detect mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_detect_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_detect_mitigation_actions_task)
        """

    def describe_dimension(
        self, **kwargs: Unpack[DescribeDimensionRequestTypeDef]
    ) -> DescribeDimensionResponseTypeDef:
        """
        Provides details about a dimension that is defined in your Amazon Web Services
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_dimension.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_dimension)
        """

    def describe_domain_configuration(
        self, **kwargs: Unpack[DescribeDomainConfigurationRequestTypeDef]
    ) -> DescribeDomainConfigurationResponseTypeDef:
        """
        Gets summary information about a domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_domain_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_domain_configuration)
        """

    def describe_endpoint(
        self, **kwargs: Unpack[DescribeEndpointRequestTypeDef]
    ) -> DescribeEndpointResponseTypeDef:
        """
        Returns or creates a unique endpoint specific to the Amazon Web Services
        account making the call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_endpoint)
        """

    def describe_event_configurations(self) -> DescribeEventConfigurationsResponseTypeDef:
        """
        Describes event configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_event_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_event_configurations)
        """

    def describe_fleet_metric(
        self, **kwargs: Unpack[DescribeFleetMetricRequestTypeDef]
    ) -> DescribeFleetMetricResponseTypeDef:
        """
        Gets information about the specified fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_fleet_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_fleet_metric)
        """

    def describe_index(
        self, **kwargs: Unpack[DescribeIndexRequestTypeDef]
    ) -> DescribeIndexResponseTypeDef:
        """
        Describes a search index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_index.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_index)
        """

    def describe_job(
        self, **kwargs: Unpack[DescribeJobRequestTypeDef]
    ) -> DescribeJobResponseTypeDef:
        """
        Describes a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_job)
        """

    def describe_job_execution(
        self, **kwargs: Unpack[DescribeJobExecutionRequestTypeDef]
    ) -> DescribeJobExecutionResponseTypeDef:
        """
        Describes a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_job_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_job_execution)
        """

    def describe_job_template(
        self, **kwargs: Unpack[DescribeJobTemplateRequestTypeDef]
    ) -> DescribeJobTemplateResponseTypeDef:
        """
        Returns information about a job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_job_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_job_template)
        """

    def describe_managed_job_template(
        self, **kwargs: Unpack[DescribeManagedJobTemplateRequestTypeDef]
    ) -> DescribeManagedJobTemplateResponseTypeDef:
        """
        View details of a managed job template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_managed_job_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_managed_job_template)
        """

    def describe_mitigation_action(
        self, **kwargs: Unpack[DescribeMitigationActionRequestTypeDef]
    ) -> DescribeMitigationActionResponseTypeDef:
        """
        Gets information about a mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_mitigation_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_mitigation_action)
        """

    def describe_provisioning_template(
        self, **kwargs: Unpack[DescribeProvisioningTemplateRequestTypeDef]
    ) -> DescribeProvisioningTemplateResponseTypeDef:
        """
        Returns information about a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_provisioning_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_provisioning_template)
        """

    def describe_provisioning_template_version(
        self, **kwargs: Unpack[DescribeProvisioningTemplateVersionRequestTypeDef]
    ) -> DescribeProvisioningTemplateVersionResponseTypeDef:
        """
        Returns information about a provisioning template version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_provisioning_template_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_provisioning_template_version)
        """

    def describe_role_alias(
        self, **kwargs: Unpack[DescribeRoleAliasRequestTypeDef]
    ) -> DescribeRoleAliasResponseTypeDef:
        """
        Describes a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_role_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_role_alias)
        """

    def describe_scheduled_audit(
        self, **kwargs: Unpack[DescribeScheduledAuditRequestTypeDef]
    ) -> DescribeScheduledAuditResponseTypeDef:
        """
        Gets information about a scheduled audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_scheduled_audit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_scheduled_audit)
        """

    def describe_security_profile(
        self, **kwargs: Unpack[DescribeSecurityProfileRequestTypeDef]
    ) -> DescribeSecurityProfileResponseTypeDef:
        """
        Gets information about a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_security_profile)
        """

    def describe_stream(
        self, **kwargs: Unpack[DescribeStreamRequestTypeDef]
    ) -> DescribeStreamResponseTypeDef:
        """
        Gets information about a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_stream)
        """

    def describe_thing(
        self, **kwargs: Unpack[DescribeThingRequestTypeDef]
    ) -> DescribeThingResponseTypeDef:
        """
        Gets information about the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_thing)
        """

    def describe_thing_group(
        self, **kwargs: Unpack[DescribeThingGroupRequestTypeDef]
    ) -> DescribeThingGroupResponseTypeDef:
        """
        Describe a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_thing_group)
        """

    def describe_thing_registration_task(
        self, **kwargs: Unpack[DescribeThingRegistrationTaskRequestTypeDef]
    ) -> DescribeThingRegistrationTaskResponseTypeDef:
        """
        Describes a bulk thing provisioning task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_thing_registration_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_thing_registration_task)
        """

    def describe_thing_type(
        self, **kwargs: Unpack[DescribeThingTypeRequestTypeDef]
    ) -> DescribeThingTypeResponseTypeDef:
        """
        Gets information about the specified thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/describe_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#describe_thing_type)
        """

    def detach_policy(
        self, **kwargs: Unpack[DetachPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a policy from the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/detach_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#detach_policy)
        """

    def detach_principal_policy(
        self, **kwargs: Unpack[DetachPrincipalPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified policy from the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/detach_principal_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#detach_principal_policy)
        """

    def detach_security_profile(
        self, **kwargs: Unpack[DetachSecurityProfileRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a Device Defender security profile from a thing group or from
        this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/detach_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#detach_security_profile)
        """

    def detach_thing_principal(
        self, **kwargs: Unpack[DetachThingPrincipalRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Detaches the specified principal from the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/detach_thing_principal.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#detach_thing_principal)
        """

    def disable_topic_rule(
        self, **kwargs: Unpack[DisableTopicRuleRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/disable_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#disable_topic_rule)
        """

    def disassociate_sbom_from_package_version(
        self, **kwargs: Unpack[DisassociateSbomFromPackageVersionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the selected software bill of materials (SBOM) from a specific
        software package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/disassociate_sbom_from_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#disassociate_sbom_from_package_version)
        """

    def enable_topic_rule(
        self, **kwargs: Unpack[EnableTopicRuleRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/enable_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#enable_topic_rule)
        """

    def get_behavior_model_training_summaries(
        self, **kwargs: Unpack[GetBehaviorModelTrainingSummariesRequestTypeDef]
    ) -> GetBehaviorModelTrainingSummariesResponseTypeDef:
        """
        Returns a Device Defender's ML Detect Security Profile training model's status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_behavior_model_training_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_behavior_model_training_summaries)
        """

    def get_buckets_aggregation(
        self, **kwargs: Unpack[GetBucketsAggregationRequestTypeDef]
    ) -> GetBucketsAggregationResponseTypeDef:
        """
        Aggregates on indexed data with search queries pertaining to particular fields.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_buckets_aggregation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_buckets_aggregation)
        """

    def get_cardinality(
        self, **kwargs: Unpack[GetCardinalityRequestTypeDef]
    ) -> GetCardinalityResponseTypeDef:
        """
        Returns the approximate count of unique values that match the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_cardinality.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_cardinality)
        """

    def get_command(self, **kwargs: Unpack[GetCommandRequestTypeDef]) -> GetCommandResponseTypeDef:
        """
        Gets information about the specified command.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_command)
        """

    def get_command_execution(
        self, **kwargs: Unpack[GetCommandExecutionRequestTypeDef]
    ) -> GetCommandExecutionResponseTypeDef:
        """
        Gets information about the specific command execution on a single device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_command_execution.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_command_execution)
        """

    def get_effective_policies(
        self, **kwargs: Unpack[GetEffectivePoliciesRequestTypeDef]
    ) -> GetEffectivePoliciesResponseTypeDef:
        """
        Gets a list of the policies that have an effect on the authorization behavior
        of the specified device when it connects to the IoT device gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_effective_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_effective_policies)
        """

    def get_indexing_configuration(self) -> GetIndexingConfigurationResponseTypeDef:
        """
        Gets the indexing configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_indexing_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_indexing_configuration)
        """

    def get_job_document(
        self, **kwargs: Unpack[GetJobDocumentRequestTypeDef]
    ) -> GetJobDocumentResponseTypeDef:
        """
        Gets a job document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_job_document.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_job_document)
        """

    def get_logging_options(self) -> GetLoggingOptionsResponseTypeDef:
        """
        Gets the logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_logging_options)
        """

    def get_ota_update(
        self, **kwargs: Unpack[GetOTAUpdateRequestTypeDef]
    ) -> GetOTAUpdateResponseTypeDef:
        """
        Gets an OTA update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_ota_update.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_ota_update)
        """

    def get_package(self, **kwargs: Unpack[GetPackageRequestTypeDef]) -> GetPackageResponseTypeDef:
        """
        Gets information about the specified software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_package)
        """

    def get_package_configuration(self) -> GetPackageConfigurationResponseTypeDef:
        """
        Gets information about the specified software package's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_package_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_package_configuration)
        """

    def get_package_version(
        self, **kwargs: Unpack[GetPackageVersionRequestTypeDef]
    ) -> GetPackageVersionResponseTypeDef:
        """
        Gets information about the specified package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_package_version)
        """

    def get_percentiles(
        self, **kwargs: Unpack[GetPercentilesRequestTypeDef]
    ) -> GetPercentilesResponseTypeDef:
        """
        Groups the aggregated values that match the query into percentile groupings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_percentiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_percentiles)
        """

    def get_policy(self, **kwargs: Unpack[GetPolicyRequestTypeDef]) -> GetPolicyResponseTypeDef:
        """
        Gets information about the specified policy with the policy document of the
        default version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_policy)
        """

    def get_policy_version(
        self, **kwargs: Unpack[GetPolicyVersionRequestTypeDef]
    ) -> GetPolicyVersionResponseTypeDef:
        """
        Gets information about the specified policy version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_policy_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_policy_version)
        """

    def get_registration_code(self) -> GetRegistrationCodeResponseTypeDef:
        """
        Gets a registration code used to register a CA certificate with IoT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_registration_code.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_registration_code)
        """

    def get_statistics(
        self, **kwargs: Unpack[GetStatisticsRequestTypeDef]
    ) -> GetStatisticsResponseTypeDef:
        """
        Returns the count, average, sum, minimum, maximum, sum of squares, variance,
        and standard deviation for the specified aggregated field.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_statistics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_statistics)
        """

    def get_thing_connectivity_data(
        self, **kwargs: Unpack[GetThingConnectivityDataRequestTypeDef]
    ) -> GetThingConnectivityDataResponseTypeDef:
        """
        Retrieves the live connectivity status per device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_thing_connectivity_data.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_thing_connectivity_data)
        """

    def get_topic_rule(
        self, **kwargs: Unpack[GetTopicRuleRequestTypeDef]
    ) -> GetTopicRuleResponseTypeDef:
        """
        Gets information about the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_topic_rule)
        """

    def get_topic_rule_destination(
        self, **kwargs: Unpack[GetTopicRuleDestinationRequestTypeDef]
    ) -> GetTopicRuleDestinationResponseTypeDef:
        """
        Gets information about a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_topic_rule_destination)
        """

    def get_v2_logging_options(self) -> GetV2LoggingOptionsResponseTypeDef:
        """
        Gets the fine grained logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_v2_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_v2_logging_options)
        """

    def list_active_violations(
        self, **kwargs: Unpack[ListActiveViolationsRequestTypeDef]
    ) -> ListActiveViolationsResponseTypeDef:
        """
        Lists the active violations for a given Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_active_violations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_active_violations)
        """

    def list_attached_policies(
        self, **kwargs: Unpack[ListAttachedPoliciesRequestTypeDef]
    ) -> ListAttachedPoliciesResponseTypeDef:
        """
        Lists the policies attached to the specified thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_attached_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_attached_policies)
        """

    def list_audit_findings(
        self, **kwargs: Unpack[ListAuditFindingsRequestTypeDef]
    ) -> ListAuditFindingsResponseTypeDef:
        """
        Lists the findings (results) of a Device Defender audit or of the audits
        performed during a specified time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_findings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_findings)
        """

    def list_audit_mitigation_actions_executions(
        self, **kwargs: Unpack[ListAuditMitigationActionsExecutionsRequestTypeDef]
    ) -> ListAuditMitigationActionsExecutionsResponseTypeDef:
        """
        Gets the status of audit mitigation action tasks that were executed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_mitigation_actions_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_mitigation_actions_executions)
        """

    def list_audit_mitigation_actions_tasks(
        self, **kwargs: Unpack[ListAuditMitigationActionsTasksRequestTypeDef]
    ) -> ListAuditMitigationActionsTasksResponseTypeDef:
        """
        Gets a list of audit mitigation action tasks that match the specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_mitigation_actions_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_mitigation_actions_tasks)
        """

    def list_audit_suppressions(
        self, **kwargs: Unpack[ListAuditSuppressionsRequestTypeDef]
    ) -> ListAuditSuppressionsResponseTypeDef:
        """
        Lists your Device Defender audit listings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_suppressions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_suppressions)
        """

    def list_audit_tasks(
        self, **kwargs: Unpack[ListAuditTasksRequestTypeDef]
    ) -> ListAuditTasksResponseTypeDef:
        """
        Lists the Device Defender audits that have been performed during a given time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_audit_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_audit_tasks)
        """

    def list_authorizers(
        self, **kwargs: Unpack[ListAuthorizersRequestTypeDef]
    ) -> ListAuthorizersResponseTypeDef:
        """
        Lists the authorizers registered in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_authorizers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_authorizers)
        """

    def list_billing_groups(
        self, **kwargs: Unpack[ListBillingGroupsRequestTypeDef]
    ) -> ListBillingGroupsResponseTypeDef:
        """
        Lists the billing groups you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_billing_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_billing_groups)
        """

    def list_ca_certificates(
        self, **kwargs: Unpack[ListCACertificatesRequestTypeDef]
    ) -> ListCACertificatesResponseTypeDef:
        """
        Lists the CA certificates registered for your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_ca_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_ca_certificates)
        """

    def list_certificate_providers(
        self, **kwargs: Unpack[ListCertificateProvidersRequestTypeDef]
    ) -> ListCertificateProvidersResponseTypeDef:
        """
        Lists all your certificate providers in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_certificate_providers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_certificate_providers)
        """

    def list_certificates(
        self, **kwargs: Unpack[ListCertificatesRequestTypeDef]
    ) -> ListCertificatesResponseTypeDef:
        """
        Lists the certificates registered in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_certificates)
        """

    def list_certificates_by_ca(
        self, **kwargs: Unpack[ListCertificatesByCARequestTypeDef]
    ) -> ListCertificatesByCAResponseTypeDef:
        """
        List the device certificates signed by the specified CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_certificates_by_ca.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_certificates_by_ca)
        """

    def list_command_executions(
        self, **kwargs: Unpack[ListCommandExecutionsRequestTypeDef]
    ) -> ListCommandExecutionsResponseTypeDef:
        """
        List all command executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_command_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_command_executions)
        """

    def list_commands(
        self, **kwargs: Unpack[ListCommandsRequestTypeDef]
    ) -> ListCommandsResponseTypeDef:
        """
        List all commands in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_commands.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_commands)
        """

    def list_custom_metrics(
        self, **kwargs: Unpack[ListCustomMetricsRequestTypeDef]
    ) -> ListCustomMetricsResponseTypeDef:
        """
        Lists your Device Defender detect custom metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_custom_metrics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_custom_metrics)
        """

    def list_detect_mitigation_actions_executions(
        self, **kwargs: Unpack[ListDetectMitigationActionsExecutionsRequestTypeDef]
    ) -> ListDetectMitigationActionsExecutionsResponseTypeDef:
        """
        Lists mitigation actions executions for a Device Defender ML Detect Security
        Profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_detect_mitigation_actions_executions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_detect_mitigation_actions_executions)
        """

    def list_detect_mitigation_actions_tasks(
        self, **kwargs: Unpack[ListDetectMitigationActionsTasksRequestTypeDef]
    ) -> ListDetectMitigationActionsTasksResponseTypeDef:
        """
        List of Device Defender ML Detect mitigation actions tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_detect_mitigation_actions_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_detect_mitigation_actions_tasks)
        """

    def list_dimensions(
        self, **kwargs: Unpack[ListDimensionsRequestTypeDef]
    ) -> ListDimensionsResponseTypeDef:
        """
        List the set of dimensions that are defined for your Amazon Web Services
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_dimensions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_dimensions)
        """

    def list_domain_configurations(
        self, **kwargs: Unpack[ListDomainConfigurationsRequestTypeDef]
    ) -> ListDomainConfigurationsResponseTypeDef:
        """
        Gets a list of domain configurations for the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_domain_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_domain_configurations)
        """

    def list_fleet_metrics(
        self, **kwargs: Unpack[ListFleetMetricsRequestTypeDef]
    ) -> ListFleetMetricsResponseTypeDef:
        """
        Lists all your fleet metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_fleet_metrics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_fleet_metrics)
        """

    def list_indices(
        self, **kwargs: Unpack[ListIndicesRequestTypeDef]
    ) -> ListIndicesResponseTypeDef:
        """
        Lists the search indices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_indices.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_indices)
        """

    def list_job_executions_for_job(
        self, **kwargs: Unpack[ListJobExecutionsForJobRequestTypeDef]
    ) -> ListJobExecutionsForJobResponseTypeDef:
        """
        Lists the job executions for a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_job_executions_for_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_job_executions_for_job)
        """

    def list_job_executions_for_thing(
        self, **kwargs: Unpack[ListJobExecutionsForThingRequestTypeDef]
    ) -> ListJobExecutionsForThingResponseTypeDef:
        """
        Lists the job executions for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_job_executions_for_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_job_executions_for_thing)
        """

    def list_job_templates(
        self, **kwargs: Unpack[ListJobTemplatesRequestTypeDef]
    ) -> ListJobTemplatesResponseTypeDef:
        """
        Returns a list of job templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_job_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_job_templates)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsRequestTypeDef]) -> ListJobsResponseTypeDef:
        """
        Lists jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_jobs)
        """

    def list_managed_job_templates(
        self, **kwargs: Unpack[ListManagedJobTemplatesRequestTypeDef]
    ) -> ListManagedJobTemplatesResponseTypeDef:
        """
        Returns a list of managed job templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_managed_job_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_managed_job_templates)
        """

    def list_metric_values(
        self, **kwargs: Unpack[ListMetricValuesRequestTypeDef]
    ) -> ListMetricValuesResponseTypeDef:
        """
        Lists the values reported for an IoT Device Defender metric (device-side
        metric, cloud-side metric, or custom metric) by the given thing during the
        specified time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_metric_values.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_metric_values)
        """

    def list_mitigation_actions(
        self, **kwargs: Unpack[ListMitigationActionsRequestTypeDef]
    ) -> ListMitigationActionsResponseTypeDef:
        """
        Gets a list of all mitigation actions that match the specified filter criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_mitigation_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_mitigation_actions)
        """

    def list_ota_updates(
        self, **kwargs: Unpack[ListOTAUpdatesRequestTypeDef]
    ) -> ListOTAUpdatesResponseTypeDef:
        """
        Lists OTA updates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_ota_updates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_ota_updates)
        """

    def list_outgoing_certificates(
        self, **kwargs: Unpack[ListOutgoingCertificatesRequestTypeDef]
    ) -> ListOutgoingCertificatesResponseTypeDef:
        """
        Lists certificates that are being transferred but not yet accepted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_outgoing_certificates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_outgoing_certificates)
        """

    def list_package_versions(
        self, **kwargs: Unpack[ListPackageVersionsRequestTypeDef]
    ) -> ListPackageVersionsResponseTypeDef:
        """
        Lists the software package versions associated to the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_package_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_package_versions)
        """

    def list_packages(
        self, **kwargs: Unpack[ListPackagesRequestTypeDef]
    ) -> ListPackagesResponseTypeDef:
        """
        Lists the software packages associated to the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_packages.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_packages)
        """

    def list_policies(
        self, **kwargs: Unpack[ListPoliciesRequestTypeDef]
    ) -> ListPoliciesResponseTypeDef:
        """
        Lists your policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_policies)
        """

    def list_policy_principals(
        self, **kwargs: Unpack[ListPolicyPrincipalsRequestTypeDef]
    ) -> ListPolicyPrincipalsResponseTypeDef:
        """
        Lists the principals associated with the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_policy_principals.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_policy_principals)
        """

    def list_policy_versions(
        self, **kwargs: Unpack[ListPolicyVersionsRequestTypeDef]
    ) -> ListPolicyVersionsResponseTypeDef:
        """
        Lists the versions of the specified policy and identifies the default version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_policy_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_policy_versions)
        """

    def list_principal_policies(
        self, **kwargs: Unpack[ListPrincipalPoliciesRequestTypeDef]
    ) -> ListPrincipalPoliciesResponseTypeDef:
        """
        Lists the policies attached to the specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_principal_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_principal_policies)
        """

    def list_principal_things(
        self, **kwargs: Unpack[ListPrincipalThingsRequestTypeDef]
    ) -> ListPrincipalThingsResponseTypeDef:
        """
        Lists the things associated with the specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_principal_things.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_principal_things)
        """

    def list_principal_things_v2(
        self, **kwargs: Unpack[ListPrincipalThingsV2RequestTypeDef]
    ) -> ListPrincipalThingsV2ResponseTypeDef:
        """
        Lists the things associated with the specified principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_principal_things_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_principal_things_v2)
        """

    def list_provisioning_template_versions(
        self, **kwargs: Unpack[ListProvisioningTemplateVersionsRequestTypeDef]
    ) -> ListProvisioningTemplateVersionsResponseTypeDef:
        """
        A list of provisioning template versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_provisioning_template_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_provisioning_template_versions)
        """

    def list_provisioning_templates(
        self, **kwargs: Unpack[ListProvisioningTemplatesRequestTypeDef]
    ) -> ListProvisioningTemplatesResponseTypeDef:
        """
        Lists the provisioning templates in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_provisioning_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_provisioning_templates)
        """

    def list_related_resources_for_audit_finding(
        self, **kwargs: Unpack[ListRelatedResourcesForAuditFindingRequestTypeDef]
    ) -> ListRelatedResourcesForAuditFindingResponseTypeDef:
        """
        The related resources of an Audit finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_related_resources_for_audit_finding.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_related_resources_for_audit_finding)
        """

    def list_role_aliases(
        self, **kwargs: Unpack[ListRoleAliasesRequestTypeDef]
    ) -> ListRoleAliasesResponseTypeDef:
        """
        Lists the role aliases registered in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_role_aliases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_role_aliases)
        """

    def list_sbom_validation_results(
        self, **kwargs: Unpack[ListSbomValidationResultsRequestTypeDef]
    ) -> ListSbomValidationResultsResponseTypeDef:
        """
        The validation results for all software bill of materials (SBOM) attached to a
        specific software package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_sbom_validation_results.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_sbom_validation_results)
        """

    def list_scheduled_audits(
        self, **kwargs: Unpack[ListScheduledAuditsRequestTypeDef]
    ) -> ListScheduledAuditsResponseTypeDef:
        """
        Lists all of your scheduled audits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_scheduled_audits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_scheduled_audits)
        """

    def list_security_profiles(
        self, **kwargs: Unpack[ListSecurityProfilesRequestTypeDef]
    ) -> ListSecurityProfilesResponseTypeDef:
        """
        Lists the Device Defender security profiles you've created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_security_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_security_profiles)
        """

    def list_security_profiles_for_target(
        self, **kwargs: Unpack[ListSecurityProfilesForTargetRequestTypeDef]
    ) -> ListSecurityProfilesForTargetResponseTypeDef:
        """
        Lists the Device Defender security profiles attached to a target (thing group).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_security_profiles_for_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_security_profiles_for_target)
        """

    def list_streams(
        self, **kwargs: Unpack[ListStreamsRequestTypeDef]
    ) -> ListStreamsResponseTypeDef:
        """
        Lists all of the streams in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_streams.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_streams)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags (metadata) you have assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_tags_for_resource)
        """

    def list_targets_for_policy(
        self, **kwargs: Unpack[ListTargetsForPolicyRequestTypeDef]
    ) -> ListTargetsForPolicyResponseTypeDef:
        """
        List targets for the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_targets_for_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_targets_for_policy)
        """

    def list_targets_for_security_profile(
        self, **kwargs: Unpack[ListTargetsForSecurityProfileRequestTypeDef]
    ) -> ListTargetsForSecurityProfileResponseTypeDef:
        """
        Lists the targets (thing groups) associated with a given Device Defender
        security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_targets_for_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_targets_for_security_profile)
        """

    def list_thing_groups(
        self, **kwargs: Unpack[ListThingGroupsRequestTypeDef]
    ) -> ListThingGroupsResponseTypeDef:
        """
        List the thing groups in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_groups)
        """

    def list_thing_groups_for_thing(
        self, **kwargs: Unpack[ListThingGroupsForThingRequestTypeDef]
    ) -> ListThingGroupsForThingResponseTypeDef:
        """
        List the thing groups to which the specified thing belongs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_groups_for_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_groups_for_thing)
        """

    def list_thing_principals(
        self, **kwargs: Unpack[ListThingPrincipalsRequestTypeDef]
    ) -> ListThingPrincipalsResponseTypeDef:
        """
        Lists the principals associated with the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_principals.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_principals)
        """

    def list_thing_principals_v2(
        self, **kwargs: Unpack[ListThingPrincipalsV2RequestTypeDef]
    ) -> ListThingPrincipalsV2ResponseTypeDef:
        """
        Lists the principals associated with the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_principals_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_principals_v2)
        """

    def list_thing_registration_task_reports(
        self, **kwargs: Unpack[ListThingRegistrationTaskReportsRequestTypeDef]
    ) -> ListThingRegistrationTaskReportsResponseTypeDef:
        """
        Information about the thing registration tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_registration_task_reports.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_registration_task_reports)
        """

    def list_thing_registration_tasks(
        self, **kwargs: Unpack[ListThingRegistrationTasksRequestTypeDef]
    ) -> ListThingRegistrationTasksResponseTypeDef:
        """
        List bulk thing provisioning tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_registration_tasks.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_registration_tasks)
        """

    def list_thing_types(
        self, **kwargs: Unpack[ListThingTypesRequestTypeDef]
    ) -> ListThingTypesResponseTypeDef:
        """
        Lists the existing thing types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_thing_types.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_thing_types)
        """

    def list_things(self, **kwargs: Unpack[ListThingsRequestTypeDef]) -> ListThingsResponseTypeDef:
        """
        Lists your things.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_things.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_things)
        """

    def list_things_in_billing_group(
        self, **kwargs: Unpack[ListThingsInBillingGroupRequestTypeDef]
    ) -> ListThingsInBillingGroupResponseTypeDef:
        """
        Lists the things you have added to the given billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_things_in_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_things_in_billing_group)
        """

    def list_things_in_thing_group(
        self, **kwargs: Unpack[ListThingsInThingGroupRequestTypeDef]
    ) -> ListThingsInThingGroupResponseTypeDef:
        """
        Lists the things in the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_things_in_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_things_in_thing_group)
        """

    def list_topic_rule_destinations(
        self, **kwargs: Unpack[ListTopicRuleDestinationsRequestTypeDef]
    ) -> ListTopicRuleDestinationsResponseTypeDef:
        """
        Lists all the topic rule destinations in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_topic_rule_destinations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_topic_rule_destinations)
        """

    def list_topic_rules(
        self, **kwargs: Unpack[ListTopicRulesRequestTypeDef]
    ) -> ListTopicRulesResponseTypeDef:
        """
        Lists the rules for the specific topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_topic_rules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_topic_rules)
        """

    def list_v2_logging_levels(
        self, **kwargs: Unpack[ListV2LoggingLevelsRequestTypeDef]
    ) -> ListV2LoggingLevelsResponseTypeDef:
        """
        Lists logging levels.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_v2_logging_levels.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_v2_logging_levels)
        """

    def list_violation_events(
        self, **kwargs: Unpack[ListViolationEventsRequestTypeDef]
    ) -> ListViolationEventsResponseTypeDef:
        """
        Lists the Device Defender security profile violations discovered during the
        given time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/list_violation_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#list_violation_events)
        """

    def put_verification_state_on_violation(
        self, **kwargs: Unpack[PutVerificationStateOnViolationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Set a verification state and provide a description of that verification state
        on a violation (detect alarm).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/put_verification_state_on_violation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#put_verification_state_on_violation)
        """

    def register_ca_certificate(
        self, **kwargs: Unpack[RegisterCACertificateRequestTypeDef]
    ) -> RegisterCACertificateResponseTypeDef:
        """
        Registers a CA certificate with Amazon Web Services IoT Core.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/register_ca_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#register_ca_certificate)
        """

    def register_certificate(
        self, **kwargs: Unpack[RegisterCertificateRequestTypeDef]
    ) -> RegisterCertificateResponseTypeDef:
        """
        Registers a device certificate with IoT in the same <a
        href="https://docs.aws.amazon.com/iot/latest/apireference/API_CertificateDescription.html#iot-Type-CertificateDescription-certificateMode">certificate
        mode</a> as the signing CA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/register_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#register_certificate)
        """

    def register_certificate_without_ca(
        self, **kwargs: Unpack[RegisterCertificateWithoutCARequestTypeDef]
    ) -> RegisterCertificateWithoutCAResponseTypeDef:
        """
        Register a certificate that does not have a certificate authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/register_certificate_without_ca.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#register_certificate_without_ca)
        """

    def register_thing(
        self, **kwargs: Unpack[RegisterThingRequestTypeDef]
    ) -> RegisterThingResponseTypeDef:
        """
        Provisions a thing in the device registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/register_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#register_thing)
        """

    def reject_certificate_transfer(
        self, **kwargs: Unpack[RejectCertificateTransferRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Rejects a pending certificate transfer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/reject_certificate_transfer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#reject_certificate_transfer)
        """

    def remove_thing_from_billing_group(
        self, **kwargs: Unpack[RemoveThingFromBillingGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the given thing from the billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/remove_thing_from_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#remove_thing_from_billing_group)
        """

    def remove_thing_from_thing_group(
        self, **kwargs: Unpack[RemoveThingFromThingGroupRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Remove the specified thing from the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/remove_thing_from_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#remove_thing_from_thing_group)
        """

    def replace_topic_rule(
        self, **kwargs: Unpack[ReplaceTopicRuleRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Replaces the rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/replace_topic_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#replace_topic_rule)
        """

    def search_index(
        self, **kwargs: Unpack[SearchIndexRequestTypeDef]
    ) -> SearchIndexResponseTypeDef:
        """
        The query search index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/search_index.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#search_index)
        """

    def set_default_authorizer(
        self, **kwargs: Unpack[SetDefaultAuthorizerRequestTypeDef]
    ) -> SetDefaultAuthorizerResponseTypeDef:
        """
        Sets the default authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_default_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_default_authorizer)
        """

    def set_default_policy_version(
        self, **kwargs: Unpack[SetDefaultPolicyVersionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the specified version of the specified policy as the policy's default
        (operative) version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_default_policy_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_default_policy_version)
        """

    def set_logging_options(
        self, **kwargs: Unpack[SetLoggingOptionsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the logging options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_logging_options)
        """

    def set_v2_logging_level(
        self, **kwargs: Unpack[SetV2LoggingLevelRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the logging level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_v2_logging_level.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_v2_logging_level)
        """

    def set_v2_logging_options(
        self, **kwargs: Unpack[SetV2LoggingOptionsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the logging options for the V2 logging service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/set_v2_logging_options.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#set_v2_logging_options)
        """

    def start_audit_mitigation_actions_task(
        self, **kwargs: Unpack[StartAuditMitigationActionsTaskRequestTypeDef]
    ) -> StartAuditMitigationActionsTaskResponseTypeDef:
        """
        Starts a task that applies a set of mitigation actions to the specified target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/start_audit_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#start_audit_mitigation_actions_task)
        """

    def start_detect_mitigation_actions_task(
        self, **kwargs: Unpack[StartDetectMitigationActionsTaskRequestTypeDef]
    ) -> StartDetectMitigationActionsTaskResponseTypeDef:
        """
        Starts a Device Defender ML Detect mitigation actions task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/start_detect_mitigation_actions_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#start_detect_mitigation_actions_task)
        """

    def start_on_demand_audit_task(
        self, **kwargs: Unpack[StartOnDemandAuditTaskRequestTypeDef]
    ) -> StartOnDemandAuditTaskResponseTypeDef:
        """
        Starts an on-demand Device Defender audit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/start_on_demand_audit_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#start_on_demand_audit_task)
        """

    def start_thing_registration_task(
        self, **kwargs: Unpack[StartThingRegistrationTaskRequestTypeDef]
    ) -> StartThingRegistrationTaskResponseTypeDef:
        """
        Creates a bulk thing provisioning task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/start_thing_registration_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#start_thing_registration_task)
        """

    def stop_thing_registration_task(
        self, **kwargs: Unpack[StopThingRegistrationTaskRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a bulk thing provisioning task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/stop_thing_registration_task.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#stop_thing_registration_task)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds to or modifies the tags of the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#tag_resource)
        """

    def test_authorization(
        self, **kwargs: Unpack[TestAuthorizationRequestTypeDef]
    ) -> TestAuthorizationResponseTypeDef:
        """
        Tests if a specified principal is authorized to perform an IoT action on a
        specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/test_authorization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#test_authorization)
        """

    def test_invoke_authorizer(
        self, **kwargs: Unpack[TestInvokeAuthorizerRequestTypeDef]
    ) -> TestInvokeAuthorizerResponseTypeDef:
        """
        Tests a custom authorization behavior by invoking a specified custom authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/test_invoke_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#test_invoke_authorizer)
        """

    def transfer_certificate(
        self, **kwargs: Unpack[TransferCertificateRequestTypeDef]
    ) -> TransferCertificateResponseTypeDef:
        """
        Transfers the specified certificate to the specified Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/transfer_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#transfer_certificate)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the given tags (metadata) from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#untag_resource)
        """

    def update_account_audit_configuration(
        self, **kwargs: Unpack[UpdateAccountAuditConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Configures or reconfigures the Device Defender audit settings for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_account_audit_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_account_audit_configuration)
        """

    def update_audit_suppression(
        self, **kwargs: Unpack[UpdateAuditSuppressionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a Device Defender audit suppression.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_audit_suppression.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_audit_suppression)
        """

    def update_authorizer(
        self, **kwargs: Unpack[UpdateAuthorizerRequestTypeDef]
    ) -> UpdateAuthorizerResponseTypeDef:
        """
        Updates an authorizer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_authorizer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_authorizer)
        """

    def update_billing_group(
        self, **kwargs: Unpack[UpdateBillingGroupRequestTypeDef]
    ) -> UpdateBillingGroupResponseTypeDef:
        """
        Updates information about the billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_billing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_billing_group)
        """

    def update_ca_certificate(
        self, **kwargs: Unpack[UpdateCACertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a registered CA certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_ca_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_ca_certificate)
        """

    def update_certificate(
        self, **kwargs: Unpack[UpdateCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the status of the specified certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_certificate)
        """

    def update_certificate_provider(
        self, **kwargs: Unpack[UpdateCertificateProviderRequestTypeDef]
    ) -> UpdateCertificateProviderResponseTypeDef:
        """
        Updates a certificate provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_certificate_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_certificate_provider)
        """

    def update_command(
        self, **kwargs: Unpack[UpdateCommandRequestTypeDef]
    ) -> UpdateCommandResponseTypeDef:
        """
        Update information about a command or mark a command for deprecation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_command.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_command)
        """

    def update_custom_metric(
        self, **kwargs: Unpack[UpdateCustomMetricRequestTypeDef]
    ) -> UpdateCustomMetricResponseTypeDef:
        """
        Updates a Device Defender detect custom metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_custom_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_custom_metric)
        """

    def update_dimension(
        self, **kwargs: Unpack[UpdateDimensionRequestTypeDef]
    ) -> UpdateDimensionResponseTypeDef:
        """
        Updates the definition for a dimension.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_dimension.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_dimension)
        """

    def update_domain_configuration(
        self, **kwargs: Unpack[UpdateDomainConfigurationRequestTypeDef]
    ) -> UpdateDomainConfigurationResponseTypeDef:
        """
        Updates values stored in the domain configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_domain_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_domain_configuration)
        """

    def update_dynamic_thing_group(
        self, **kwargs: Unpack[UpdateDynamicThingGroupRequestTypeDef]
    ) -> UpdateDynamicThingGroupResponseTypeDef:
        """
        Updates a dynamic thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_dynamic_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_dynamic_thing_group)
        """

    def update_event_configurations(
        self, **kwargs: Unpack[UpdateEventConfigurationsRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the event configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_event_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_event_configurations)
        """

    def update_fleet_metric(
        self, **kwargs: Unpack[UpdateFleetMetricRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the data for a fleet metric.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_fleet_metric.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_fleet_metric)
        """

    def update_indexing_configuration(
        self, **kwargs: Unpack[UpdateIndexingConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the search configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_indexing_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_indexing_configuration)
        """

    def update_job(self, **kwargs: Unpack[UpdateJobRequestTypeDef]) -> EmptyResponseMetadataTypeDef:
        """
        Updates supported fields of the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_job)
        """

    def update_mitigation_action(
        self, **kwargs: Unpack[UpdateMitigationActionRequestTypeDef]
    ) -> UpdateMitigationActionResponseTypeDef:
        """
        Updates the definition for the specified mitigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_mitigation_action.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_mitigation_action)
        """

    def update_package(self, **kwargs: Unpack[UpdatePackageRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the supported fields for a specific software package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_package.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_package)
        """

    def update_package_configuration(
        self, **kwargs: Unpack[UpdatePackageConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the software package configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_package_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_package_configuration)
        """

    def update_package_version(
        self, **kwargs: Unpack[UpdatePackageVersionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the supported fields for a specific package version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_package_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_package_version)
        """

    def update_provisioning_template(
        self, **kwargs: Unpack[UpdateProvisioningTemplateRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_provisioning_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_provisioning_template)
        """

    def update_role_alias(
        self, **kwargs: Unpack[UpdateRoleAliasRequestTypeDef]
    ) -> UpdateRoleAliasResponseTypeDef:
        """
        Updates a role alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_role_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_role_alias)
        """

    def update_scheduled_audit(
        self, **kwargs: Unpack[UpdateScheduledAuditRequestTypeDef]
    ) -> UpdateScheduledAuditResponseTypeDef:
        """
        Updates a scheduled audit, including which checks are performed and how often
        the audit takes place.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_scheduled_audit.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_scheduled_audit)
        """

    def update_security_profile(
        self, **kwargs: Unpack[UpdateSecurityProfileRequestTypeDef]
    ) -> UpdateSecurityProfileResponseTypeDef:
        """
        Updates a Device Defender security profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_security_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_security_profile)
        """

    def update_stream(
        self, **kwargs: Unpack[UpdateStreamRequestTypeDef]
    ) -> UpdateStreamResponseTypeDef:
        """
        Updates an existing stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_stream)
        """

    def update_thing(self, **kwargs: Unpack[UpdateThingRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the data for a thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_thing)
        """

    def update_thing_group(
        self, **kwargs: Unpack[UpdateThingGroupRequestTypeDef]
    ) -> UpdateThingGroupResponseTypeDef:
        """
        Update a thing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_thing_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_thing_group)
        """

    def update_thing_groups_for_thing(
        self, **kwargs: Unpack[UpdateThingGroupsForThingRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the groups to which the thing belongs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_thing_groups_for_thing.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_thing_groups_for_thing)
        """

    def update_thing_type(self, **kwargs: Unpack[UpdateThingTypeRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates a thing type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_thing_type.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_thing_type)
        """

    def update_topic_rule_destination(
        self, **kwargs: Unpack[UpdateTopicRuleDestinationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a topic rule destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/update_topic_rule_destination.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#update_topic_rule_destination)
        """

    def validate_security_profile_behaviors(
        self, **kwargs: Unpack[ValidateSecurityProfileBehaviorsRequestTypeDef]
    ) -> ValidateSecurityProfileBehaviorsResponseTypeDef:
        """
        Validates a Device Defender security profile behaviors specification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/validate_security_profile_behaviors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#validate_security_profile_behaviors)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_behavior_model_training_summaries"]
    ) -> GetBehaviorModelTrainingSummariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_active_violations"]
    ) -> ListActiveViolationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_attached_policies"]
    ) -> ListAttachedPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_audit_findings"]
    ) -> ListAuditFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_audit_mitigation_actions_executions"]
    ) -> ListAuditMitigationActionsExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_audit_mitigation_actions_tasks"]
    ) -> ListAuditMitigationActionsTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_audit_suppressions"]
    ) -> ListAuditSuppressionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_audit_tasks"]
    ) -> ListAuditTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_authorizers"]
    ) -> ListAuthorizersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_billing_groups"]
    ) -> ListBillingGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ca_certificates"]
    ) -> ListCACertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_certificates_by_ca"]
    ) -> ListCertificatesByCAPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_command_executions"]
    ) -> ListCommandExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_commands"]
    ) -> ListCommandsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_custom_metrics"]
    ) -> ListCustomMetricsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_detect_mitigation_actions_executions"]
    ) -> ListDetectMitigationActionsExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_detect_mitigation_actions_tasks"]
    ) -> ListDetectMitigationActionsTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dimensions"]
    ) -> ListDimensionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_domain_configurations"]
    ) -> ListDomainConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fleet_metrics"]
    ) -> ListFleetMetricsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_indices"]
    ) -> ListIndicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_job_executions_for_job"]
    ) -> ListJobExecutionsForJobPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_job_executions_for_thing"]
    ) -> ListJobExecutionsForThingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_job_templates"]
    ) -> ListJobTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs"]
    ) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_job_templates"]
    ) -> ListManagedJobTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_metric_values"]
    ) -> ListMetricValuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_mitigation_actions"]
    ) -> ListMitigationActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ota_updates"]
    ) -> ListOTAUpdatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_outgoing_certificates"]
    ) -> ListOutgoingCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_package_versions"]
    ) -> ListPackageVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_packages"]
    ) -> ListPackagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policies"]
    ) -> ListPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policy_principals"]
    ) -> ListPolicyPrincipalsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_principal_policies"]
    ) -> ListPrincipalPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_principal_things"]
    ) -> ListPrincipalThingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_principal_things_v2"]
    ) -> ListPrincipalThingsV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_provisioning_template_versions"]
    ) -> ListProvisioningTemplateVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_provisioning_templates"]
    ) -> ListProvisioningTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_related_resources_for_audit_finding"]
    ) -> ListRelatedResourcesForAuditFindingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_role_aliases"]
    ) -> ListRoleAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sbom_validation_results"]
    ) -> ListSbomValidationResultsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_scheduled_audits"]
    ) -> ListScheduledAuditsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_security_profiles_for_target"]
    ) -> ListSecurityProfilesForTargetPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_security_profiles"]
    ) -> ListSecurityProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_streams"]
    ) -> ListStreamsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_targets_for_policy"]
    ) -> ListTargetsForPolicyPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_targets_for_security_profile"]
    ) -> ListTargetsForSecurityProfilePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_thing_groups_for_thing"]
    ) -> ListThingGroupsForThingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_thing_groups"]
    ) -> ListThingGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_thing_principals"]
    ) -> ListThingPrincipalsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_thing_principals_v2"]
    ) -> ListThingPrincipalsV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_thing_registration_task_reports"]
    ) -> ListThingRegistrationTaskReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_thing_registration_tasks"]
    ) -> ListThingRegistrationTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_thing_types"]
    ) -> ListThingTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_things_in_billing_group"]
    ) -> ListThingsInBillingGroupPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_things_in_thing_group"]
    ) -> ListThingsInThingGroupPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_things"]
    ) -> ListThingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_topic_rule_destinations"]
    ) -> ListTopicRuleDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_topic_rules"]
    ) -> ListTopicRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_v2_logging_levels"]
    ) -> ListV2LoggingLevelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_violation_events"]
    ) -> ListViolationEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot/client/#get_paginator)
        """
