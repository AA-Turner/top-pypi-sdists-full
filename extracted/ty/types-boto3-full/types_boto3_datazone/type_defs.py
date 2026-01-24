"""
Type annotations for datazone service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_datazone/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_datazone.type_defs import AcceptChoiceTypeDef

    data: AcceptChoiceTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    AcceptRuleBehaviorType,
    AttributeEntityTypeType,
    AuthenticationTypeType,
    AuthTypeType,
    ChangeActionType,
    ComputeEnvironmentsType,
    ConfigurableActionTypeAuthorizationType,
    ConfigurationStatusType,
    ConnectionScopeType,
    ConnectionStatusType,
    ConnectionTypeType,
    DataAssetActivityStatusType,
    DataProductStatusType,
    DataSourceErrorTypeType,
    DataSourceRunStatusType,
    DataSourceRunTypeType,
    DataSourceStatusType,
    DeploymentModeType,
    DeploymentStatusType,
    DeploymentTypeType,
    DomainStatusType,
    DomainVersionType,
    EdgeDirectionType,
    EnableSettingType,
    EntityTypeType,
    EnvironmentStatusType,
    FilterExpressionTypeType,
    FilterOperatorType,
    FilterStatusType,
    FormTypeStatusType,
    GlossaryStatusType,
    GlossaryTermStatusType,
    GlueConnectionTypeType,
    GovernanceTypeType,
    GroupProfileStatusType,
    GroupSearchTypeType,
    HyperPodOrchestratorType,
    InventorySearchScopeType,
    JobRunModeType,
    JobRunStatusType,
    LineageEventProcessingStatusType,
    LineageImportStatusType,
    ListingStatusType,
    ManagedPolicyTypeType,
    MetadataGenerationRunStatusType,
    MetadataGenerationRunTypeType,
    NotificationRoleType,
    NotificationTypeType,
    OAuth2GrantTypeType,
    OpenLineageRunStateType,
    OverallDeploymentStatusType,
    ProjectDesignationType,
    ProjectStatusType,
    ProtocolType,
    RejectRuleBehaviorType,
    ResourceTagSourceType,
    RuleActionType,
    RuleScopeSelectionModeType,
    RuleTypeType,
    S3PermissionType,
    SearchOutputAdditionalAttributeType,
    SelfGrantStatusType,
    SortKeyType,
    SortOrderType,
    StatusType,
    SubscriptionGrantCreationModeType,
    SubscriptionGrantOverallStatusType,
    SubscriptionGrantStatusType,
    SubscriptionRequestStatusType,
    SubscriptionStatusType,
    TargetEntityTypeType,
    TaskStatusType,
    TimeSeriesEntityTypeType,
    TimezoneType,
    TypesSearchScopeType,
    UserAssignmentType,
    UserDesignationType,
    UserProfileStatusType,
    UserProfileTypeType,
    UserSearchTypeType,
    UserTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AcceptChoiceTypeDef",
    "AcceptPredictionsInputTypeDef",
    "AcceptPredictionsOutputTypeDef",
    "AcceptRuleTypeDef",
    "AcceptSubscriptionRequestInputTypeDef",
    "AcceptSubscriptionRequestOutputTypeDef",
    "AcceptedAssetScopeTypeDef",
    "AccountInfoOutputTypeDef",
    "AccountInfoTypeDef",
    "AccountPoolSummaryTypeDef",
    "AccountSourceOutputTypeDef",
    "AccountSourceTypeDef",
    "AccountSourceUnionTypeDef",
    "ActionParametersTypeDef",
    "AddEntityOwnerInputTypeDef",
    "AddPolicyGrantInputTypeDef",
    "AddPolicyGrantOutputTypeDef",
    "AddToProjectMemberPoolPolicyGrantDetailTypeDef",
    "AggregationListItemTypeDef",
    "AggregationOutputItemTypeDef",
    "AggregationOutputTypeDef",
    "AmazonQPropertiesInputTypeDef",
    "AmazonQPropertiesOutputTypeDef",
    "AmazonQPropertiesPatchTypeDef",
    "AssetFilterConfigurationOutputTypeDef",
    "AssetFilterConfigurationTypeDef",
    "AssetFilterConfigurationUnionTypeDef",
    "AssetFilterSummaryTypeDef",
    "AssetInDataProductListingItemTypeDef",
    "AssetItemAdditionalAttributesTypeDef",
    "AssetItemTypeDef",
    "AssetListingDetailsTypeDef",
    "AssetListingItemAdditionalAttributesTypeDef",
    "AssetListingItemTypeDef",
    "AssetListingTypeDef",
    "AssetPermissionTypeDef",
    "AssetRevisionTypeDef",
    "AssetScopeTypeDef",
    "AssetTargetNameMapTypeDef",
    "AssetTypeItemTypeDef",
    "AssetTypesForRuleOutputTypeDef",
    "AssetTypesForRuleTypeDef",
    "AssociateEnvironmentRoleInputTypeDef",
    "AssociateGovernedTermsInputTypeDef",
    "AthenaPropertiesInputTypeDef",
    "AthenaPropertiesOutputTypeDef",
    "AthenaPropertiesPatchTypeDef",
    "AttributeErrorTypeDef",
    "AttributeInputTypeDef",
    "AuthenticationConfigurationInputTypeDef",
    "AuthenticationConfigurationPatchTypeDef",
    "AuthenticationConfigurationTypeDef",
    "AuthorizationCodePropertiesTypeDef",
    "AwsAccountTypeDef",
    "AwsConsoleLinkParametersTypeDef",
    "AwsLocationTypeDef",
    "BasicAuthenticationCredentialsTypeDef",
    "BatchGetAttributeOutputTypeDef",
    "BatchGetAttributesMetadataInputTypeDef",
    "BatchGetAttributesMetadataOutputTypeDef",
    "BatchPutAttributeOutputTypeDef",
    "BatchPutAttributesMetadataInputTypeDef",
    "BatchPutAttributesMetadataOutputTypeDef",
    "BlobTypeDef",
    "BusinessNameGenerationConfigurationTypeDef",
    "CancelMetadataGenerationRunInputTypeDef",
    "CancelSubscriptionInputTypeDef",
    "CancelSubscriptionOutputTypeDef",
    "CloudFormationPropertiesTypeDef",
    "ColumnFilterConfigurationOutputTypeDef",
    "ColumnFilterConfigurationTypeDef",
    "ConfigurableActionParameterTypeDef",
    "ConfigurableEnvironmentActionTypeDef",
    "ConnectionCredentialsTypeDef",
    "ConnectionPropertiesInputTypeDef",
    "ConnectionPropertiesOutputTypeDef",
    "ConnectionPropertiesPatchTypeDef",
    "ConnectionSummaryTypeDef",
    "CreateAccountPoolInputTypeDef",
    "CreateAccountPoolOutputTypeDef",
    "CreateAssetFilterInputTypeDef",
    "CreateAssetFilterOutputTypeDef",
    "CreateAssetInputTypeDef",
    "CreateAssetOutputTypeDef",
    "CreateAssetRevisionInputTypeDef",
    "CreateAssetRevisionOutputTypeDef",
    "CreateAssetTypeInputTypeDef",
    "CreateAssetTypeOutputTypeDef",
    "CreateAssetTypePolicyGrantDetailTypeDef",
    "CreateConnectionInputTypeDef",
    "CreateConnectionOutputTypeDef",
    "CreateDataProductInputTypeDef",
    "CreateDataProductOutputTypeDef",
    "CreateDataProductRevisionInputTypeDef",
    "CreateDataProductRevisionOutputTypeDef",
    "CreateDataSourceInputTypeDef",
    "CreateDataSourceOutputTypeDef",
    "CreateDomainInputTypeDef",
    "CreateDomainOutputTypeDef",
    "CreateDomainUnitInputTypeDef",
    "CreateDomainUnitOutputTypeDef",
    "CreateDomainUnitPolicyGrantDetailTypeDef",
    "CreateEnvironmentActionInputTypeDef",
    "CreateEnvironmentActionOutputTypeDef",
    "CreateEnvironmentBlueprintInputTypeDef",
    "CreateEnvironmentBlueprintOutputTypeDef",
    "CreateEnvironmentInputTypeDef",
    "CreateEnvironmentOutputTypeDef",
    "CreateEnvironmentProfileInputTypeDef",
    "CreateEnvironmentProfileOutputTypeDef",
    "CreateEnvironmentProfilePolicyGrantDetailTypeDef",
    "CreateFormTypeInputTypeDef",
    "CreateFormTypeOutputTypeDef",
    "CreateFormTypePolicyGrantDetailTypeDef",
    "CreateGlossaryInputTypeDef",
    "CreateGlossaryOutputTypeDef",
    "CreateGlossaryPolicyGrantDetailTypeDef",
    "CreateGlossaryTermInputTypeDef",
    "CreateGlossaryTermOutputTypeDef",
    "CreateGroupProfileInputTypeDef",
    "CreateGroupProfileOutputTypeDef",
    "CreateListingChangeSetInputTypeDef",
    "CreateListingChangeSetOutputTypeDef",
    "CreateProjectFromProjectProfilePolicyGrantDetailOutputTypeDef",
    "CreateProjectFromProjectProfilePolicyGrantDetailTypeDef",
    "CreateProjectInputTypeDef",
    "CreateProjectMembershipInputTypeDef",
    "CreateProjectOutputTypeDef",
    "CreateProjectPolicyGrantDetailTypeDef",
    "CreateProjectProfileInputTypeDef",
    "CreateProjectProfileOutputTypeDef",
    "CreateRuleInputTypeDef",
    "CreateRuleOutputTypeDef",
    "CreateSubscriptionGrantInputTypeDef",
    "CreateSubscriptionGrantOutputTypeDef",
    "CreateSubscriptionRequestInputTypeDef",
    "CreateSubscriptionRequestOutputTypeDef",
    "CreateSubscriptionTargetInputTypeDef",
    "CreateSubscriptionTargetOutputTypeDef",
    "CreateUserProfileInputTypeDef",
    "CreateUserProfileOutputTypeDef",
    "CustomAccountPoolHandlerTypeDef",
    "CustomParameterTypeDef",
    "DataProductItemAdditionalAttributesTypeDef",
    "DataProductItemOutputTypeDef",
    "DataProductItemTypeDef",
    "DataProductItemUnionTypeDef",
    "DataProductListingItemAdditionalAttributesTypeDef",
    "DataProductListingItemTypeDef",
    "DataProductListingTypeDef",
    "DataProductResultItemTypeDef",
    "DataProductRevisionTypeDef",
    "DataSourceConfigurationInputTypeDef",
    "DataSourceConfigurationOutputTypeDef",
    "DataSourceErrorMessageTypeDef",
    "DataSourceRunActivityTypeDef",
    "DataSourceRunLineageSummaryTypeDef",
    "DataSourceRunSummaryTypeDef",
    "DataSourceSummaryTypeDef",
    "DeleteAccountPoolInputTypeDef",
    "DeleteAssetFilterInputTypeDef",
    "DeleteAssetInputTypeDef",
    "DeleteAssetTypeInputTypeDef",
    "DeleteConnectionInputTypeDef",
    "DeleteConnectionOutputTypeDef",
    "DeleteDataExportConfigurationInputTypeDef",
    "DeleteDataProductInputTypeDef",
    "DeleteDataSourceInputTypeDef",
    "DeleteDataSourceOutputTypeDef",
    "DeleteDomainInputTypeDef",
    "DeleteDomainOutputTypeDef",
    "DeleteDomainUnitInputTypeDef",
    "DeleteEnvironmentActionInputTypeDef",
    "DeleteEnvironmentBlueprintConfigurationInputTypeDef",
    "DeleteEnvironmentBlueprintInputTypeDef",
    "DeleteEnvironmentInputTypeDef",
    "DeleteEnvironmentProfileInputTypeDef",
    "DeleteFormTypeInputTypeDef",
    "DeleteGlossaryInputTypeDef",
    "DeleteGlossaryTermInputTypeDef",
    "DeleteListingInputTypeDef",
    "DeleteProjectInputTypeDef",
    "DeleteProjectMembershipInputTypeDef",
    "DeleteProjectProfileInputTypeDef",
    "DeleteRuleInputTypeDef",
    "DeleteSubscriptionGrantInputTypeDef",
    "DeleteSubscriptionGrantOutputTypeDef",
    "DeleteSubscriptionRequestInputTypeDef",
    "DeleteSubscriptionTargetInputTypeDef",
    "DeleteTimeSeriesDataPointsInputTypeDef",
    "DeploymentPropertiesTypeDef",
    "DeploymentTypeDef",
    "DetailedGlossaryTermTypeDef",
    "DisassociateEnvironmentRoleInputTypeDef",
    "DisassociateGovernedTermsInputTypeDef",
    "DomainSummaryTypeDef",
    "DomainUnitFilterForProjectTypeDef",
    "DomainUnitGrantFilterOutputTypeDef",
    "DomainUnitGrantFilterTypeDef",
    "DomainUnitGroupPropertiesTypeDef",
    "DomainUnitOwnerPropertiesTypeDef",
    "DomainUnitPolicyGrantPrincipalOutputTypeDef",
    "DomainUnitPolicyGrantPrincipalTypeDef",
    "DomainUnitSummaryTypeDef",
    "DomainUnitTargetTypeDef",
    "DomainUnitUserPropertiesTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionConfigurationTypeDef",
    "EnvironmentActionSummaryTypeDef",
    "EnvironmentBlueprintConfigurationItemTypeDef",
    "EnvironmentBlueprintSummaryTypeDef",
    "EnvironmentConfigurationOutputTypeDef",
    "EnvironmentConfigurationParameterTypeDef",
    "EnvironmentConfigurationParametersDetailsOutputTypeDef",
    "EnvironmentConfigurationParametersDetailsTypeDef",
    "EnvironmentConfigurationParametersDetailsUnionTypeDef",
    "EnvironmentConfigurationTypeDef",
    "EnvironmentConfigurationUnionTypeDef",
    "EnvironmentConfigurationUserParameterOutputTypeDef",
    "EnvironmentConfigurationUserParameterTypeDef",
    "EnvironmentConfigurationUserParameterUnionTypeDef",
    "EnvironmentDeploymentDetailsOutputTypeDef",
    "EnvironmentDeploymentDetailsTypeDef",
    "EnvironmentDeploymentDetailsUnionTypeDef",
    "EnvironmentErrorTypeDef",
    "EnvironmentParameterTypeDef",
    "EnvironmentProfileSummaryTypeDef",
    "EnvironmentResolvedAccountTypeDef",
    "EnvironmentSummaryTypeDef",
    "EqualToExpressionTypeDef",
    "EventSummaryTypeDef",
    "FailureCauseTypeDef",
    "FilterClausePaginatorTypeDef",
    "FilterClauseTypeDef",
    "FilterExpressionTypeDef",
    "FilterTypeDef",
    "FormEntryInputTypeDef",
    "FormEntryOutputTypeDef",
    "FormInputTypeDef",
    "FormOutputTypeDef",
    "FormTypeDataTypeDef",
    "GetAccountPoolInputTypeDef",
    "GetAccountPoolOutputTypeDef",
    "GetAssetFilterInputTypeDef",
    "GetAssetFilterOutputTypeDef",
    "GetAssetInputTypeDef",
    "GetAssetOutputTypeDef",
    "GetAssetTypeInputTypeDef",
    "GetAssetTypeOutputTypeDef",
    "GetConnectionInputTypeDef",
    "GetConnectionOutputTypeDef",
    "GetDataExportConfigurationInputTypeDef",
    "GetDataExportConfigurationOutputTypeDef",
    "GetDataProductInputTypeDef",
    "GetDataProductOutputTypeDef",
    "GetDataSourceInputTypeDef",
    "GetDataSourceOutputTypeDef",
    "GetDataSourceRunInputTypeDef",
    "GetDataSourceRunOutputTypeDef",
    "GetDomainInputTypeDef",
    "GetDomainOutputTypeDef",
    "GetDomainUnitInputTypeDef",
    "GetDomainUnitOutputTypeDef",
    "GetEnvironmentActionInputTypeDef",
    "GetEnvironmentActionOutputTypeDef",
    "GetEnvironmentBlueprintConfigurationInputTypeDef",
    "GetEnvironmentBlueprintConfigurationOutputTypeDef",
    "GetEnvironmentBlueprintInputTypeDef",
    "GetEnvironmentBlueprintOutputTypeDef",
    "GetEnvironmentCredentialsInputTypeDef",
    "GetEnvironmentCredentialsOutputTypeDef",
    "GetEnvironmentInputTypeDef",
    "GetEnvironmentOutputTypeDef",
    "GetEnvironmentProfileInputTypeDef",
    "GetEnvironmentProfileOutputTypeDef",
    "GetFormTypeInputTypeDef",
    "GetFormTypeOutputTypeDef",
    "GetGlossaryInputTypeDef",
    "GetGlossaryOutputTypeDef",
    "GetGlossaryTermInputTypeDef",
    "GetGlossaryTermOutputTypeDef",
    "GetGroupProfileInputTypeDef",
    "GetGroupProfileOutputTypeDef",
    "GetIamPortalLoginUrlInputTypeDef",
    "GetIamPortalLoginUrlOutputTypeDef",
    "GetJobRunInputTypeDef",
    "GetJobRunOutputTypeDef",
    "GetLineageEventInputTypeDef",
    "GetLineageEventOutputTypeDef",
    "GetLineageNodeInputTypeDef",
    "GetLineageNodeOutputTypeDef",
    "GetListingInputTypeDef",
    "GetListingOutputTypeDef",
    "GetMetadataGenerationRunInputTypeDef",
    "GetMetadataGenerationRunOutputTypeDef",
    "GetProjectInputTypeDef",
    "GetProjectOutputTypeDef",
    "GetProjectProfileInputTypeDef",
    "GetProjectProfileOutputTypeDef",
    "GetRuleInputTypeDef",
    "GetRuleOutputTypeDef",
    "GetSubscriptionGrantInputTypeDef",
    "GetSubscriptionGrantOutputTypeDef",
    "GetSubscriptionInputTypeDef",
    "GetSubscriptionOutputTypeDef",
    "GetSubscriptionRequestDetailsInputTypeDef",
    "GetSubscriptionRequestDetailsOutputTypeDef",
    "GetSubscriptionTargetInputTypeDef",
    "GetSubscriptionTargetOutputTypeDef",
    "GetTimeSeriesDataPointInputTypeDef",
    "GetTimeSeriesDataPointOutputTypeDef",
    "GetUserProfileInputTypeDef",
    "GetUserProfileOutputTypeDef",
    "GlossaryItemAdditionalAttributesTypeDef",
    "GlossaryItemTypeDef",
    "GlossaryTermEnforcementDetailOutputTypeDef",
    "GlossaryTermEnforcementDetailTypeDef",
    "GlossaryTermItemAdditionalAttributesTypeDef",
    "GlossaryTermItemTypeDef",
    "GlueConnectionInputTypeDef",
    "GlueConnectionPatchTypeDef",
    "GlueConnectionTypeDef",
    "GlueOAuth2CredentialsTypeDef",
    "GluePropertiesInputTypeDef",
    "GluePropertiesOutputTypeDef",
    "GluePropertiesPatchTypeDef",
    "GlueRunConfigurationInputTypeDef",
    "GlueRunConfigurationOutputTypeDef",
    "GlueSelfGrantStatusOutputTypeDef",
    "GrantedEntityInputTypeDef",
    "GrantedEntityTypeDef",
    "GreaterThanExpressionTypeDef",
    "GreaterThanOrEqualToExpressionTypeDef",
    "GroupDetailsTypeDef",
    "GroupPolicyGrantPrincipalTypeDef",
    "GroupProfileSummaryTypeDef",
    "HyperPodPropertiesInputTypeDef",
    "HyperPodPropertiesOutputTypeDef",
    "IamPropertiesInputTypeDef",
    "IamPropertiesOutputTypeDef",
    "IamPropertiesPatchTypeDef",
    "IamUserProfileDetailsTypeDef",
    "ImportTypeDef",
    "InExpressionOutputTypeDef",
    "InExpressionTypeDef",
    "IsNotNullExpressionTypeDef",
    "IsNullExpressionTypeDef",
    "JobRunDetailsTypeDef",
    "JobRunErrorTypeDef",
    "JobRunSummaryTypeDef",
    "LakeFormationConfigurationOutputTypeDef",
    "LakeFormationConfigurationTypeDef",
    "LakeFormationConfigurationUnionTypeDef",
    "LessThanExpressionTypeDef",
    "LessThanOrEqualToExpressionTypeDef",
    "LikeExpressionTypeDef",
    "LineageEventSummaryTypeDef",
    "LineageInfoTypeDef",
    "LineageNodeReferenceTypeDef",
    "LineageNodeSummaryTypeDef",
    "LineageNodeTypeItemTypeDef",
    "LineageRunDetailsTypeDef",
    "LineageSqlQueryRunDetailsTypeDef",
    "LineageSyncScheduleTypeDef",
    "ListAccountPoolsInputPaginateTypeDef",
    "ListAccountPoolsInputTypeDef",
    "ListAccountPoolsOutputTypeDef",
    "ListAccountsInAccountPoolInputPaginateTypeDef",
    "ListAccountsInAccountPoolInputTypeDef",
    "ListAccountsInAccountPoolOutputTypeDef",
    "ListAssetFiltersInputPaginateTypeDef",
    "ListAssetFiltersInputTypeDef",
    "ListAssetFiltersOutputTypeDef",
    "ListAssetRevisionsInputPaginateTypeDef",
    "ListAssetRevisionsInputTypeDef",
    "ListAssetRevisionsOutputTypeDef",
    "ListConnectionsInputPaginateTypeDef",
    "ListConnectionsInputTypeDef",
    "ListConnectionsOutputTypeDef",
    "ListDataProductRevisionsInputPaginateTypeDef",
    "ListDataProductRevisionsInputTypeDef",
    "ListDataProductRevisionsOutputTypeDef",
    "ListDataSourceRunActivitiesInputPaginateTypeDef",
    "ListDataSourceRunActivitiesInputTypeDef",
    "ListDataSourceRunActivitiesOutputTypeDef",
    "ListDataSourceRunsInputPaginateTypeDef",
    "ListDataSourceRunsInputTypeDef",
    "ListDataSourceRunsOutputTypeDef",
    "ListDataSourcesInputPaginateTypeDef",
    "ListDataSourcesInputTypeDef",
    "ListDataSourcesOutputTypeDef",
    "ListDomainUnitsForParentInputPaginateTypeDef",
    "ListDomainUnitsForParentInputTypeDef",
    "ListDomainUnitsForParentOutputTypeDef",
    "ListDomainsInputPaginateTypeDef",
    "ListDomainsInputTypeDef",
    "ListDomainsOutputTypeDef",
    "ListEntityOwnersInputPaginateTypeDef",
    "ListEntityOwnersInputTypeDef",
    "ListEntityOwnersOutputTypeDef",
    "ListEnvironmentActionsInputPaginateTypeDef",
    "ListEnvironmentActionsInputTypeDef",
    "ListEnvironmentActionsOutputTypeDef",
    "ListEnvironmentBlueprintConfigurationsInputPaginateTypeDef",
    "ListEnvironmentBlueprintConfigurationsInputTypeDef",
    "ListEnvironmentBlueprintConfigurationsOutputTypeDef",
    "ListEnvironmentBlueprintsInputPaginateTypeDef",
    "ListEnvironmentBlueprintsInputTypeDef",
    "ListEnvironmentBlueprintsOutputTypeDef",
    "ListEnvironmentProfilesInputPaginateTypeDef",
    "ListEnvironmentProfilesInputTypeDef",
    "ListEnvironmentProfilesOutputTypeDef",
    "ListEnvironmentsInputPaginateTypeDef",
    "ListEnvironmentsInputTypeDef",
    "ListEnvironmentsOutputTypeDef",
    "ListJobRunsInputPaginateTypeDef",
    "ListJobRunsInputTypeDef",
    "ListJobRunsOutputTypeDef",
    "ListLineageEventsInputPaginateTypeDef",
    "ListLineageEventsInputTypeDef",
    "ListLineageEventsOutputTypeDef",
    "ListLineageNodeHistoryInputPaginateTypeDef",
    "ListLineageNodeHistoryInputTypeDef",
    "ListLineageNodeHistoryOutputTypeDef",
    "ListMetadataGenerationRunsInputPaginateTypeDef",
    "ListMetadataGenerationRunsInputTypeDef",
    "ListMetadataGenerationRunsOutputTypeDef",
    "ListNotificationsInputPaginateTypeDef",
    "ListNotificationsInputTypeDef",
    "ListNotificationsOutputTypeDef",
    "ListPolicyGrantsInputPaginateTypeDef",
    "ListPolicyGrantsInputTypeDef",
    "ListPolicyGrantsOutputTypeDef",
    "ListProjectMembershipsInputPaginateTypeDef",
    "ListProjectMembershipsInputTypeDef",
    "ListProjectMembershipsOutputTypeDef",
    "ListProjectProfilesInputPaginateTypeDef",
    "ListProjectProfilesInputTypeDef",
    "ListProjectProfilesOutputTypeDef",
    "ListProjectsInputPaginateTypeDef",
    "ListProjectsInputTypeDef",
    "ListProjectsOutputTypeDef",
    "ListRulesInputPaginateTypeDef",
    "ListRulesInputTypeDef",
    "ListRulesOutputTypeDef",
    "ListSubscriptionGrantsInputPaginateTypeDef",
    "ListSubscriptionGrantsInputTypeDef",
    "ListSubscriptionGrantsOutputTypeDef",
    "ListSubscriptionRequestsInputPaginateTypeDef",
    "ListSubscriptionRequestsInputTypeDef",
    "ListSubscriptionRequestsOutputTypeDef",
    "ListSubscriptionTargetsInputPaginateTypeDef",
    "ListSubscriptionTargetsInputTypeDef",
    "ListSubscriptionTargetsOutputTypeDef",
    "ListSubscriptionsInputPaginateTypeDef",
    "ListSubscriptionsInputTypeDef",
    "ListSubscriptionsOutputTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTimeSeriesDataPointsInputPaginateTypeDef",
    "ListTimeSeriesDataPointsInputTypeDef",
    "ListTimeSeriesDataPointsOutputTypeDef",
    "ListingItemTypeDef",
    "ListingRevisionInputTypeDef",
    "ListingRevisionTypeDef",
    "ListingSummaryItemTypeDef",
    "ListingSummaryTypeDef",
    "ManagedEndpointCredentialsTypeDef",
    "MatchOffsetTypeDef",
    "MatchRationaleItemTypeDef",
    "MemberDetailsTypeDef",
    "MemberTypeDef",
    "MetadataFormEnforcementDetailOutputTypeDef",
    "MetadataFormEnforcementDetailTypeDef",
    "MetadataFormReferenceTypeDef",
    "MetadataFormSummaryTypeDef",
    "MetadataGenerationRunItemTypeDef",
    "MetadataGenerationRunTargetTypeDef",
    "MetadataGenerationRunTypeStatTypeDef",
    "MlflowPropertiesInputTypeDef",
    "MlflowPropertiesOutputTypeDef",
    "MlflowPropertiesPatchTypeDef",
    "ModelTypeDef",
    "NameIdentifierTypeDef",
    "NotEqualToExpressionTypeDef",
    "NotInExpressionOutputTypeDef",
    "NotInExpressionTypeDef",
    "NotLikeExpressionTypeDef",
    "NotificationOutputTypeDef",
    "NotificationResourceTypeDef",
    "OAuth2ClientApplicationTypeDef",
    "OAuth2PropertiesOutputTypeDef",
    "OAuth2PropertiesTypeDef",
    "OAuth2PropertiesUnionTypeDef",
    "OpenLineageRunEventSummaryTypeDef",
    "OverrideDomainUnitOwnersPolicyGrantDetailTypeDef",
    "OverrideProjectOwnersPolicyGrantDetailTypeDef",
    "OwnerGroupPropertiesOutputTypeDef",
    "OwnerGroupPropertiesTypeDef",
    "OwnerPropertiesOutputTypeDef",
    "OwnerPropertiesTypeDef",
    "OwnerUserPropertiesOutputTypeDef",
    "OwnerUserPropertiesTypeDef",
    "PaginatorConfigTypeDef",
    "PermissionsOutputTypeDef",
    "PermissionsTypeDef",
    "PermissionsUnionTypeDef",
    "PhysicalConnectionRequirementsOutputTypeDef",
    "PhysicalConnectionRequirementsTypeDef",
    "PhysicalConnectionRequirementsUnionTypeDef",
    "PhysicalEndpointTypeDef",
    "PolicyGrantDetailOutputTypeDef",
    "PolicyGrantDetailTypeDef",
    "PolicyGrantDetailUnionTypeDef",
    "PolicyGrantMemberTypeDef",
    "PolicyGrantPrincipalOutputTypeDef",
    "PolicyGrantPrincipalTypeDef",
    "PolicyGrantPrincipalUnionTypeDef",
    "PostLineageEventInputTypeDef",
    "PostLineageEventOutputTypeDef",
    "PostTimeSeriesDataPointsInputTypeDef",
    "PostTimeSeriesDataPointsOutputTypeDef",
    "PredictionConfigurationTypeDef",
    "ProjectDeletionErrorTypeDef",
    "ProjectGrantFilterTypeDef",
    "ProjectMemberTypeDef",
    "ProjectPolicyGrantPrincipalTypeDef",
    "ProjectProfileSummaryTypeDef",
    "ProjectSummaryTypeDef",
    "ProjectsForRuleOutputTypeDef",
    "ProjectsForRuleTypeDef",
    "ProvisioningConfigurationOutputTypeDef",
    "ProvisioningConfigurationTypeDef",
    "ProvisioningConfigurationUnionTypeDef",
    "ProvisioningPropertiesTypeDef",
    "PutDataExportConfigurationInputTypeDef",
    "PutEnvironmentBlueprintConfigurationInputTypeDef",
    "PutEnvironmentBlueprintConfigurationOutputTypeDef",
    "RecommendationConfigurationTypeDef",
    "RedshiftClusterStorageTypeDef",
    "RedshiftCredentialConfigurationTypeDef",
    "RedshiftCredentialsTypeDef",
    "RedshiftLineageSyncConfigurationInputTypeDef",
    "RedshiftLineageSyncConfigurationOutputTypeDef",
    "RedshiftPropertiesInputTypeDef",
    "RedshiftPropertiesOutputTypeDef",
    "RedshiftPropertiesPatchTypeDef",
    "RedshiftRunConfigurationInputTypeDef",
    "RedshiftRunConfigurationOutputTypeDef",
    "RedshiftSelfGrantStatusOutputTypeDef",
    "RedshiftServerlessStorageTypeDef",
    "RedshiftStoragePropertiesTypeDef",
    "RedshiftStorageTypeDef",
    "RegionTypeDef",
    "RejectChoiceTypeDef",
    "RejectPredictionsInputTypeDef",
    "RejectPredictionsOutputTypeDef",
    "RejectRuleTypeDef",
    "RejectSubscriptionRequestInputTypeDef",
    "RejectSubscriptionRequestOutputTypeDef",
    "RelationalFilterConfigurationOutputTypeDef",
    "RelationalFilterConfigurationTypeDef",
    "RelationalFilterConfigurationUnionTypeDef",
    "RemoveEntityOwnerInputTypeDef",
    "RemovePolicyGrantInputTypeDef",
    "ResourceTagParameterTypeDef",
    "ResourceTagTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "RevokeSubscriptionInputTypeDef",
    "RevokeSubscriptionOutputTypeDef",
    "RowFilterConfigurationOutputTypeDef",
    "RowFilterConfigurationTypeDef",
    "RowFilterExpressionOutputTypeDef",
    "RowFilterExpressionTypeDef",
    "RowFilterOutputTypeDef",
    "RowFilterTypeDef",
    "RuleDetailOutputTypeDef",
    "RuleDetailTypeDef",
    "RuleDetailUnionTypeDef",
    "RuleScopeOutputTypeDef",
    "RuleScopeTypeDef",
    "RuleScopeUnionTypeDef",
    "RuleSummaryTypeDef",
    "RuleTargetTypeDef",
    "RunStatisticsForAssetsTypeDef",
    "S3PropertiesInputTypeDef",
    "S3PropertiesOutputTypeDef",
    "S3PropertiesPatchTypeDef",
    "SageMakerRunConfigurationInputTypeDef",
    "SageMakerRunConfigurationOutputTypeDef",
    "ScheduleConfigurationTypeDef",
    "SearchGroupProfilesInputPaginateTypeDef",
    "SearchGroupProfilesInputTypeDef",
    "SearchGroupProfilesOutputTypeDef",
    "SearchInItemTypeDef",
    "SearchInputPaginateTypeDef",
    "SearchInputTypeDef",
    "SearchInventoryResultItemTypeDef",
    "SearchListingsInputPaginateTypeDef",
    "SearchListingsInputTypeDef",
    "SearchListingsOutputTypeDef",
    "SearchOutputTypeDef",
    "SearchResultItemTypeDef",
    "SearchSortTypeDef",
    "SearchTypesInputPaginateTypeDef",
    "SearchTypesInputTypeDef",
    "SearchTypesOutputTypeDef",
    "SearchTypesResultItemTypeDef",
    "SearchUserProfilesInputPaginateTypeDef",
    "SearchUserProfilesInputTypeDef",
    "SearchUserProfilesOutputTypeDef",
    "SelfGrantStatusDetailTypeDef",
    "SelfGrantStatusOutputTypeDef",
    "SingleSignOnTypeDef",
    "SparkEmrPropertiesInputTypeDef",
    "SparkEmrPropertiesOutputTypeDef",
    "SparkEmrPropertiesPatchTypeDef",
    "SparkGlueArgsTypeDef",
    "SparkGluePropertiesInputTypeDef",
    "SparkGluePropertiesOutputTypeDef",
    "SsoUserProfileDetailsTypeDef",
    "StartDataSourceRunInputTypeDef",
    "StartDataSourceRunOutputTypeDef",
    "StartMetadataGenerationRunInputTypeDef",
    "StartMetadataGenerationRunOutputTypeDef",
    "SubscribedAssetListingTypeDef",
    "SubscribedAssetTypeDef",
    "SubscribedGroupInputTypeDef",
    "SubscribedGroupTypeDef",
    "SubscribedIamPrincipalInputTypeDef",
    "SubscribedIamPrincipalTypeDef",
    "SubscribedListingInputTypeDef",
    "SubscribedListingItemTypeDef",
    "SubscribedListingTypeDef",
    "SubscribedPrincipalInputTypeDef",
    "SubscribedPrincipalTypeDef",
    "SubscribedProductListingTypeDef",
    "SubscribedProjectInputTypeDef",
    "SubscribedProjectTypeDef",
    "SubscribedUserInputTypeDef",
    "SubscribedUserTypeDef",
    "SubscriptionGrantSummaryTypeDef",
    "SubscriptionRequestSummaryTypeDef",
    "SubscriptionSummaryTypeDef",
    "SubscriptionTargetFormTypeDef",
    "SubscriptionTargetSummaryTypeDef",
    "TagResourceRequestTypeDef",
    "TermRelationsOutputTypeDef",
    "TermRelationsTypeDef",
    "TermRelationsUnionTypeDef",
    "TextMatchItemTypeDef",
    "TimeSeriesDataPointFormInputTypeDef",
    "TimeSeriesDataPointFormOutputTypeDef",
    "TimeSeriesDataPointSummaryFormOutputTypeDef",
    "TimestampTypeDef",
    "TopicTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAccountPoolInputTypeDef",
    "UpdateAccountPoolOutputTypeDef",
    "UpdateAssetFilterInputTypeDef",
    "UpdateAssetFilterOutputTypeDef",
    "UpdateConnectionInputTypeDef",
    "UpdateConnectionOutputTypeDef",
    "UpdateDataSourceInputTypeDef",
    "UpdateDataSourceOutputTypeDef",
    "UpdateDomainInputTypeDef",
    "UpdateDomainOutputTypeDef",
    "UpdateDomainUnitInputTypeDef",
    "UpdateDomainUnitOutputTypeDef",
    "UpdateEnvironmentActionInputTypeDef",
    "UpdateEnvironmentActionOutputTypeDef",
    "UpdateEnvironmentBlueprintInputTypeDef",
    "UpdateEnvironmentBlueprintOutputTypeDef",
    "UpdateEnvironmentInputTypeDef",
    "UpdateEnvironmentOutputTypeDef",
    "UpdateEnvironmentProfileInputTypeDef",
    "UpdateEnvironmentProfileOutputTypeDef",
    "UpdateGlossaryInputTypeDef",
    "UpdateGlossaryOutputTypeDef",
    "UpdateGlossaryTermInputTypeDef",
    "UpdateGlossaryTermOutputTypeDef",
    "UpdateGroupProfileInputTypeDef",
    "UpdateGroupProfileOutputTypeDef",
    "UpdateProjectInputTypeDef",
    "UpdateProjectOutputTypeDef",
    "UpdateProjectProfileInputTypeDef",
    "UpdateProjectProfileOutputTypeDef",
    "UpdateRootDomainUnitOwnerInputTypeDef",
    "UpdateRuleInputTypeDef",
    "UpdateRuleOutputTypeDef",
    "UpdateSubscriptionGrantStatusInputTypeDef",
    "UpdateSubscriptionGrantStatusOutputTypeDef",
    "UpdateSubscriptionRequestInputTypeDef",
    "UpdateSubscriptionRequestOutputTypeDef",
    "UpdateSubscriptionTargetInputTypeDef",
    "UpdateSubscriptionTargetOutputTypeDef",
    "UpdateUserProfileInputTypeDef",
    "UpdateUserProfileOutputTypeDef",
    "UseAssetTypePolicyGrantDetailTypeDef",
    "UserDetailsTypeDef",
    "UserPolicyGrantPrincipalOutputTypeDef",
    "UserPolicyGrantPrincipalTypeDef",
    "UserProfileDetailsTypeDef",
    "UserProfileSummaryTypeDef",
    "UsernamePasswordTypeDef",
)


class AcceptChoiceTypeDef(TypedDict):
    predictionTarget: str
    predictionChoice: NotRequired[int]
    editedValue: NotRequired[str]


class AcceptRuleTypeDef(TypedDict):
    rule: NotRequired[AcceptRuleBehaviorType]
    threshold: NotRequired[float]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AcceptedAssetScopeTypeDef(TypedDict):
    assetId: str
    filterIds: Sequence[str]


class FormOutputTypeDef(TypedDict):
    formName: str
    typeName: NotRequired[str]
    typeRevision: NotRequired[str]
    content: NotRequired[str]


class AccountInfoOutputTypeDef(TypedDict):
    awsAccountId: str
    supportedRegions: list[str]
    awsAccountName: NotRequired[str]


class AccountInfoTypeDef(TypedDict):
    awsAccountId: str
    supportedRegions: Sequence[str]
    awsAccountName: NotRequired[str]


AccountPoolSummaryTypeDef = TypedDict(
    "AccountPoolSummaryTypeDef",
    {
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "resolutionStrategy": NotRequired[Literal["MANUAL"]],
        "domainUnitId": NotRequired[str],
        "createdBy": NotRequired[str],
        "updatedBy": NotRequired[str],
    },
)


class CustomAccountPoolHandlerTypeDef(TypedDict):
    lambdaFunctionArn: str
    lambdaExecutionRoleArn: NotRequired[str]


class AwsConsoleLinkParametersTypeDef(TypedDict):
    uri: NotRequired[str]


class AddToProjectMemberPoolPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]


class AggregationListItemTypeDef(TypedDict):
    attribute: str
    displayValue: NotRequired[str]


class AggregationOutputItemTypeDef(TypedDict):
    value: NotRequired[str]
    count: NotRequired[int]
    displayValue: NotRequired[str]


class AmazonQPropertiesInputTypeDef(TypedDict):
    isEnabled: bool
    profileArn: NotRequired[str]
    authMode: NotRequired[str]


class AmazonQPropertiesOutputTypeDef(TypedDict):
    isEnabled: bool
    profileArn: NotRequired[str]
    authMode: NotRequired[str]


class AmazonQPropertiesPatchTypeDef(TypedDict):
    isEnabled: bool
    profileArn: NotRequired[str]
    authMode: NotRequired[str]


class ColumnFilterConfigurationOutputTypeDef(TypedDict):
    includedColumnNames: NotRequired[list[str]]


class ColumnFilterConfigurationTypeDef(TypedDict):
    includedColumnNames: NotRequired[Sequence[str]]


AssetFilterSummaryTypeDef = TypedDict(
    "AssetFilterSummaryTypeDef",
    {
        "id": str,
        "domainId": str,
        "assetId": str,
        "name": str,
        "description": NotRequired[str],
        "status": NotRequired[FilterStatusType],
        "effectiveColumnNames": NotRequired[list[str]],
        "effectiveRowFilter": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "errorMessage": NotRequired[str],
    },
)


class AssetInDataProductListingItemTypeDef(TypedDict):
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    entityType: NotRequired[str]


TimeSeriesDataPointSummaryFormOutputTypeDef = TypedDict(
    "TimeSeriesDataPointSummaryFormOutputTypeDef",
    {
        "formName": str,
        "typeIdentifier": str,
        "timestamp": datetime,
        "typeRevision": NotRequired[str],
        "contentSummary": NotRequired[str],
        "id": NotRequired[str],
    },
)


class AssetListingDetailsTypeDef(TypedDict):
    listingId: str
    listingStatus: ListingStatusType


class DetailedGlossaryTermTypeDef(TypedDict):
    name: NotRequired[str]
    shortDescription: NotRequired[str]


AssetRevisionTypeDef = TypedDict(
    "AssetRevisionTypeDef",
    {
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "revision": NotRequired[str],
        "createdBy": NotRequired[str],
        "createdAt": NotRequired[datetime],
    },
)


class AssetScopeTypeDef(TypedDict):
    assetId: str
    filterIds: list[str]
    status: str
    errorMessage: NotRequired[str]


class AssetTargetNameMapTypeDef(TypedDict):
    assetId: str
    targetName: str


class FormEntryOutputTypeDef(TypedDict):
    typeName: str
    typeRevision: str
    required: NotRequired[bool]


class AssetTypesForRuleOutputTypeDef(TypedDict):
    selectionMode: RuleScopeSelectionModeType
    specificAssetTypes: NotRequired[list[str]]


class AssetTypesForRuleTypeDef(TypedDict):
    selectionMode: RuleScopeSelectionModeType
    specificAssetTypes: NotRequired[Sequence[str]]


class AssociateEnvironmentRoleInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    environmentRoleArn: str


class AssociateGovernedTermsInputTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["ASSET"]
    governedGlossaryTerms: Sequence[str]


class AthenaPropertiesInputTypeDef(TypedDict):
    workgroupName: NotRequired[str]


class AthenaPropertiesOutputTypeDef(TypedDict):
    workgroupName: NotRequired[str]


class AthenaPropertiesPatchTypeDef(TypedDict):
    workgroupName: NotRequired[str]


class AttributeErrorTypeDef(TypedDict):
    attributeIdentifier: str
    code: str
    message: str


class FormInputTypeDef(TypedDict):
    formName: str
    typeIdentifier: NotRequired[str]
    typeRevision: NotRequired[str]
    content: NotRequired[str]


class BasicAuthenticationCredentialsTypeDef(TypedDict):
    userName: NotRequired[str]
    password: NotRequired[str]


class AuthorizationCodePropertiesTypeDef(TypedDict):
    authorizationCode: NotRequired[str]
    redirectUri: NotRequired[str]


class AwsAccountTypeDef(TypedDict):
    awsAccountId: NotRequired[str]
    awsAccountIdPath: NotRequired[str]


class AwsLocationTypeDef(TypedDict):
    accessRole: NotRequired[str]
    awsAccountId: NotRequired[str]
    awsRegion: NotRequired[str]
    iamConnectionId: NotRequired[str]


class BatchGetAttributesMetadataInputTypeDef(TypedDict):
    domainIdentifier: str
    entityType: AttributeEntityTypeType
    entityIdentifier: str
    attributeIdentifiers: Sequence[str]
    entityRevision: NotRequired[str]


class BatchPutAttributeOutputTypeDef(TypedDict):
    attributeIdentifier: str


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class BusinessNameGenerationConfigurationTypeDef(TypedDict):
    enabled: NotRequired[bool]


class CancelMetadataGenerationRunInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class CancelSubscriptionInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class CloudFormationPropertiesTypeDef(TypedDict):
    templateUrl: str


class ConfigurableActionParameterTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]


class ConnectionCredentialsTypeDef(TypedDict):
    accessKeyId: NotRequired[str]
    secretAccessKey: NotRequired[str]
    sessionToken: NotRequired[str]
    expiration: NotRequired[datetime]


class HyperPodPropertiesInputTypeDef(TypedDict):
    clusterName: str


class IamPropertiesInputTypeDef(TypedDict):
    glueLineageSyncEnabled: NotRequired[bool]


class MlflowPropertiesInputTypeDef(TypedDict):
    trackingServerArn: NotRequired[str]


class S3PropertiesInputTypeDef(TypedDict):
    s3Uri: str
    s3AccessGrantLocationId: NotRequired[str]


class SparkEmrPropertiesInputTypeDef(TypedDict):
    computeArn: NotRequired[str]
    instanceProfileArn: NotRequired[str]
    javaVirtualEnv: NotRequired[str]
    logUri: NotRequired[str]
    pythonVirtualEnv: NotRequired[str]
    runtimeRole: NotRequired[str]
    trustedCertificatesS3Uri: NotRequired[str]
    managedEndpointArn: NotRequired[str]


class GluePropertiesOutputTypeDef(TypedDict):
    status: NotRequired[ConnectionStatusType]
    errorMessage: NotRequired[str]


class HyperPodPropertiesOutputTypeDef(TypedDict):
    clusterName: str
    clusterArn: NotRequired[str]
    orchestrator: NotRequired[HyperPodOrchestratorType]


class IamPropertiesOutputTypeDef(TypedDict):
    environmentId: NotRequired[str]
    glueLineageSyncEnabled: NotRequired[bool]


class MlflowPropertiesOutputTypeDef(TypedDict):
    trackingServerArn: NotRequired[str]


class S3PropertiesOutputTypeDef(TypedDict):
    s3Uri: str
    s3AccessGrantLocationId: NotRequired[str]
    status: NotRequired[ConnectionStatusType]
    errorMessage: NotRequired[str]


class IamPropertiesPatchTypeDef(TypedDict):
    glueLineageSyncEnabled: NotRequired[bool]


class MlflowPropertiesPatchTypeDef(TypedDict):
    trackingServerArn: NotRequired[str]


class S3PropertiesPatchTypeDef(TypedDict):
    s3Uri: str
    s3AccessGrantLocationId: NotRequired[str]


class SparkEmrPropertiesPatchTypeDef(TypedDict):
    computeArn: NotRequired[str]
    instanceProfileArn: NotRequired[str]
    javaVirtualEnv: NotRequired[str]
    logUri: NotRequired[str]
    pythonVirtualEnv: NotRequired[str]
    runtimeRole: NotRequired[str]
    trustedCertificatesS3Uri: NotRequired[str]
    managedEndpointArn: NotRequired[str]


class FormEntryInputTypeDef(TypedDict):
    typeIdentifier: str
    typeRevision: str
    required: NotRequired[bool]


class CreateAssetTypePolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]


class DataProductItemOutputTypeDef(TypedDict):
    itemType: Literal["ASSET"]
    identifier: str
    revision: NotRequired[str]
    glossaryTerms: NotRequired[list[str]]


class RecommendationConfigurationTypeDef(TypedDict):
    enableBusinessNameGeneration: NotRequired[bool]


class ScheduleConfigurationTypeDef(TypedDict):
    timezone: NotRequired[TimezoneType]
    schedule: NotRequired[str]


class DataSourceErrorMessageTypeDef(TypedDict):
    errorType: DataSourceErrorTypeType
    errorDetail: NotRequired[str]


SingleSignOnTypeDef = TypedDict(
    "SingleSignOnTypeDef",
    {
        "type": NotRequired[AuthTypeType],
        "userAssignment": NotRequired[UserAssignmentType],
        "idcInstanceArn": NotRequired[str],
    },
)


class CreateDomainUnitInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    parentDomainUnitIdentifier: str
    description: NotRequired[str]
    clientToken: NotRequired[str]


class CreateDomainUnitPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]


class CustomParameterTypeDef(TypedDict):
    keyName: str
    fieldType: str
    description: NotRequired[str]
    defaultValue: NotRequired[str]
    isEditable: NotRequired[bool]
    isOptional: NotRequired[bool]
    isUpdateSupported: NotRequired[bool]


class DeploymentPropertiesTypeDef(TypedDict):
    startTimeoutMinutes: NotRequired[int]
    endTimeoutMinutes: NotRequired[int]


class EnvironmentParameterTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]


ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "value": str,
        "type": str,
        "provider": NotRequired[str],
        "name": NotRequired[str],
    },
)


class CreateEnvironmentProfilePolicyGrantDetailTypeDef(TypedDict):
    domainUnitId: NotRequired[str]


class ModelTypeDef(TypedDict):
    smithy: NotRequired[str]


class CreateFormTypePolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]


class CreateGlossaryInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    owningProjectIdentifier: str
    description: NotRequired[str]
    status: NotRequired[GlossaryStatusType]
    usageRestrictions: NotRequired[Sequence[Literal["ASSET_GOVERNED_TERMS"]]]
    clientToken: NotRequired[str]


class CreateGlossaryPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]


class TermRelationsOutputTypeDef(TypedDict):
    isA: NotRequired[list[str]]
    classifies: NotRequired[list[str]]


class CreateGroupProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: str
    clientToken: NotRequired[str]


class CreateListingChangeSetInputTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: EntityTypeType
    action: ChangeActionType
    entityRevision: NotRequired[str]
    clientToken: NotRequired[str]


class CreateProjectFromProjectProfilePolicyGrantDetailOutputTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]
    projectProfiles: NotRequired[list[str]]


class CreateProjectFromProjectProfilePolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]
    projectProfiles: NotRequired[Sequence[str]]


class MemberTypeDef(TypedDict):
    userIdentifier: NotRequired[str]
    groupIdentifier: NotRequired[str]


class ProjectDeletionErrorTypeDef(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]


class ResourceTagTypeDef(TypedDict):
    key: str
    value: str
    source: ResourceTagSourceType


class CreateProjectPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]


class ResourceTagParameterTypeDef(TypedDict):
    key: str
    value: str
    isValueEditable: bool


class SubscribedListingInputTypeDef(TypedDict):
    identifier: str


class SubscriptionTargetFormTypeDef(TypedDict):
    formName: str
    content: str


class CreateUserProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    userIdentifier: str
    userType: NotRequired[UserTypeType]
    clientToken: NotRequired[str]


class DataProductItemTypeDef(TypedDict):
    itemType: Literal["ASSET"]
    identifier: str
    revision: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]


DataProductRevisionTypeDef = TypedDict(
    "DataProductRevisionTypeDef",
    {
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "revision": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
    },
)


class SageMakerRunConfigurationInputTypeDef(TypedDict):
    trackingAssets: Mapping[str, Sequence[str]]


class SageMakerRunConfigurationOutputTypeDef(TypedDict):
    trackingAssets: dict[str, list[str]]
    accountId: NotRequired[str]
    region: NotRequired[str]


class LineageInfoTypeDef(TypedDict):
    eventId: NotRequired[str]
    eventStatus: NotRequired[LineageEventProcessingStatusType]
    errorMessage: NotRequired[str]


class DataSourceRunLineageSummaryTypeDef(TypedDict):
    importStatus: NotRequired[LineageImportStatusType]


class RunStatisticsForAssetsTypeDef(TypedDict):
    added: NotRequired[int]
    updated: NotRequired[int]
    unchanged: NotRequired[int]
    skipped: NotRequired[int]
    failed: NotRequired[int]


class DeleteAccountPoolInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteAssetFilterInputTypeDef(TypedDict):
    domainIdentifier: str
    assetIdentifier: str
    identifier: str


class DeleteAssetInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteAssetTypeInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteConnectionInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteDataExportConfigurationInputTypeDef(TypedDict):
    domainIdentifier: str


class DeleteDataProductInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteDataSourceInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    clientToken: NotRequired[str]
    retainPermissionsOnRevokeFailure: NotRequired[bool]


class DeleteDomainInputTypeDef(TypedDict):
    identifier: str
    clientToken: NotRequired[str]
    skipDeletionCheck: NotRequired[bool]


class DeleteDomainUnitInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteEnvironmentActionInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str


class DeleteEnvironmentBlueprintConfigurationInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentBlueprintIdentifier: str


class DeleteEnvironmentBlueprintInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteEnvironmentInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteEnvironmentProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteFormTypeInputTypeDef(TypedDict):
    domainIdentifier: str
    formTypeIdentifier: str


class DeleteGlossaryInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteGlossaryTermInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteListingInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteProjectInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    skipDeletionCheck: NotRequired[bool]


class DeleteProjectProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteRuleInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteSubscriptionGrantInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteSubscriptionRequestInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class DeleteSubscriptionTargetInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str


class DeleteTimeSeriesDataPointsInputTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    clientToken: NotRequired[str]


class EnvironmentErrorTypeDef(TypedDict):
    message: str
    code: NotRequired[str]


class DisassociateEnvironmentRoleInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    environmentRoleArn: str


class DisassociateGovernedTermsInputTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: Literal["ASSET"]
    governedGlossaryTerms: Sequence[str]


DomainSummaryTypeDef = TypedDict(
    "DomainSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "managedAccountId": str,
        "status": DomainStatusType,
        "createdAt": datetime,
        "description": NotRequired[str],
        "portalUrl": NotRequired[str],
        "lastUpdatedAt": NotRequired[datetime],
        "domainVersion": NotRequired[DomainVersionType],
    },
)


class DomainUnitFilterForProjectTypeDef(TypedDict):
    domainUnit: str
    includeChildDomainUnits: NotRequired[bool]


class DomainUnitGrantFilterOutputTypeDef(TypedDict):
    allDomainUnitsGrantFilter: NotRequired[dict[str, Any]]


class DomainUnitGrantFilterTypeDef(TypedDict):
    allDomainUnitsGrantFilter: NotRequired[Mapping[str, Any]]


class DomainUnitGroupPropertiesTypeDef(TypedDict):
    groupId: NotRequired[str]


class DomainUnitUserPropertiesTypeDef(TypedDict):
    userId: NotRequired[str]


DomainUnitSummaryTypeDef = TypedDict(
    "DomainUnitSummaryTypeDef",
    {
        "name": str,
        "id": str,
    },
)


class DomainUnitTargetTypeDef(TypedDict):
    domainUnitId: str
    includeChildDomainUnits: NotRequired[bool]


class EncryptionConfigurationTypeDef(TypedDict):
    kmsKeyArn: NotRequired[str]
    sseAlgorithm: NotRequired[str]


class RegionTypeDef(TypedDict):
    regionName: NotRequired[str]
    regionNamePath: NotRequired[str]


class EnvironmentConfigurationParameterTypeDef(TypedDict):
    name: NotRequired[str]
    value: NotRequired[str]
    isEditable: NotRequired[bool]


class EnvironmentResolvedAccountTypeDef(TypedDict):
    awsAccountId: str
    regionName: str
    sourceAccountPoolId: NotRequired[str]


EnvironmentProfileSummaryTypeDef = TypedDict(
    "EnvironmentProfileSummaryTypeDef",
    {
        "id": str,
        "domainId": str,
        "createdBy": str,
        "name": str,
        "environmentBlueprintId": str,
        "awsAccountId": NotRequired[str],
        "awsAccountRegion": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "description": NotRequired[str],
        "projectId": NotRequired[str],
    },
)
EnvironmentSummaryTypeDef = TypedDict(
    "EnvironmentSummaryTypeDef",
    {
        "projectId": str,
        "domainId": str,
        "createdBy": str,
        "name": str,
        "provider": str,
        "id": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "description": NotRequired[str],
        "environmentProfileId": NotRequired[str],
        "awsAccountId": NotRequired[str],
        "awsAccountRegion": NotRequired[str],
        "status": NotRequired[EnvironmentStatusType],
        "environmentConfigurationId": NotRequired[str],
    },
)


class EqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str


class FailureCauseTypeDef(TypedDict):
    message: NotRequired[str]


FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "attribute": str,
        "value": NotRequired[str],
        "intValue": NotRequired[int],
        "operator": NotRequired[FilterOperatorType],
    },
)
FilterExpressionTypeDef = TypedDict(
    "FilterExpressionTypeDef",
    {
        "type": FilterExpressionTypeType,
        "expression": str,
    },
)


class ImportTypeDef(TypedDict):
    name: str
    revision: str


class GetAccountPoolInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetAssetFilterInputTypeDef(TypedDict):
    domainIdentifier: str
    assetIdentifier: str
    identifier: str


class GetAssetInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]


class GetAssetTypeInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]


class GetConnectionInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    withSecret: NotRequired[bool]


class GetDataExportConfigurationInputTypeDef(TypedDict):
    domainIdentifier: str


class GetDataProductInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]


class GetDataSourceInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetDataSourceRunInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetDomainInputTypeDef(TypedDict):
    identifier: str


class GetDomainUnitInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetEnvironmentActionInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str


class GetEnvironmentBlueprintConfigurationInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentBlueprintIdentifier: str


class GetEnvironmentBlueprintInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetEnvironmentCredentialsInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str


class GetEnvironmentInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetEnvironmentProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetFormTypeInputTypeDef(TypedDict):
    domainIdentifier: str
    formTypeIdentifier: str
    revision: NotRequired[str]


class GetGlossaryInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetGlossaryTermInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetGroupProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: str


class GetIamPortalLoginUrlInputTypeDef(TypedDict):
    domainIdentifier: str


class GetJobRunInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class JobRunErrorTypeDef(TypedDict):
    message: str


class GetLineageEventInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


TimestampTypeDef = Union[datetime, str]
LineageNodeReferenceTypeDef = TypedDict(
    "LineageNodeReferenceTypeDef",
    {
        "id": NotRequired[str],
        "eventTimestamp": NotRequired[datetime],
    },
)


class GetListingInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    listingRevision: NotRequired[str]


GetMetadataGenerationRunInputTypeDef = TypedDict(
    "GetMetadataGenerationRunInputTypeDef",
    {
        "domainIdentifier": str,
        "identifier": str,
        "type": NotRequired[MetadataGenerationRunTypeType],
    },
)
MetadataGenerationRunTargetTypeDef = TypedDict(
    "MetadataGenerationRunTargetTypeDef",
    {
        "type": Literal["ASSET"],
        "identifier": str,
        "revision": NotRequired[str],
    },
)
MetadataGenerationRunTypeStatTypeDef = TypedDict(
    "MetadataGenerationRunTypeStatTypeDef",
    {
        "type": MetadataGenerationRunTypeType,
        "status": MetadataGenerationRunStatusType,
        "errorMessage": NotRequired[str],
    },
)


class GetProjectInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetProjectProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetRuleInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]


class GetSubscriptionGrantInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetSubscriptionInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetSubscriptionRequestDetailsInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str


class GetSubscriptionTargetInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str


class GetTimeSeriesDataPointInputTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    identifier: str
    formName: str


TimeSeriesDataPointFormOutputTypeDef = TypedDict(
    "TimeSeriesDataPointFormOutputTypeDef",
    {
        "formName": str,
        "typeIdentifier": str,
        "timestamp": datetime,
        "typeRevision": NotRequired[str],
        "content": NotRequired[str],
        "id": NotRequired[str],
    },
)
GetUserProfileInputTypeDef = TypedDict(
    "GetUserProfileInputTypeDef",
    {
        "domainIdentifier": str,
        "userIdentifier": str,
        "type": NotRequired[UserProfileTypeType],
    },
)


class GlossaryTermEnforcementDetailOutputTypeDef(TypedDict):
    requiredGlossaryTermIds: NotRequired[list[str]]


class GlossaryTermEnforcementDetailTypeDef(TypedDict):
    requiredGlossaryTermIds: NotRequired[Sequence[str]]


class PhysicalConnectionRequirementsOutputTypeDef(TypedDict):
    subnetId: NotRequired[str]
    subnetIdList: NotRequired[list[str]]
    securityGroupIdList: NotRequired[list[str]]
    availabilityZone: NotRequired[str]


class GlueOAuth2CredentialsTypeDef(TypedDict):
    userManagedClientApplicationClientSecret: NotRequired[str]
    accessToken: NotRequired[str]
    refreshToken: NotRequired[str]
    jwtToken: NotRequired[str]


class SelfGrantStatusDetailTypeDef(TypedDict):
    databaseName: str
    status: SelfGrantStatusType
    schemaName: NotRequired[str]
    failureCause: NotRequired[str]


class ListingRevisionInputTypeDef(TypedDict):
    identifier: str
    revision: str


ListingRevisionTypeDef = TypedDict(
    "ListingRevisionTypeDef",
    {
        "id": str,
        "revision": str,
    },
)


class GreaterThanExpressionTypeDef(TypedDict):
    columnName: str
    value: str


class GreaterThanOrEqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str


class GroupDetailsTypeDef(TypedDict):
    groupId: str


class GroupPolicyGrantPrincipalTypeDef(TypedDict):
    groupIdentifier: NotRequired[str]


GroupProfileSummaryTypeDef = TypedDict(
    "GroupProfileSummaryTypeDef",
    {
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "status": NotRequired[GroupProfileStatusType],
        "groupName": NotRequired[str],
    },
)


class IamUserProfileDetailsTypeDef(TypedDict):
    arn: NotRequired[str]
    principalId: NotRequired[str]


class InExpressionOutputTypeDef(TypedDict):
    columnName: str
    values: list[str]


class InExpressionTypeDef(TypedDict):
    columnName: str
    values: Sequence[str]


class IsNotNullExpressionTypeDef(TypedDict):
    columnName: str


class IsNullExpressionTypeDef(TypedDict):
    columnName: str


class LakeFormationConfigurationOutputTypeDef(TypedDict):
    locationRegistrationRole: NotRequired[str]
    locationRegistrationExcludeS3Locations: NotRequired[list[str]]


class LakeFormationConfigurationTypeDef(TypedDict):
    locationRegistrationRole: NotRequired[str]
    locationRegistrationExcludeS3Locations: NotRequired[Sequence[str]]


class LessThanExpressionTypeDef(TypedDict):
    columnName: str
    value: str


class LessThanOrEqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str


class LikeExpressionTypeDef(TypedDict):
    columnName: str
    value: str


LineageNodeSummaryTypeDef = TypedDict(
    "LineageNodeSummaryTypeDef",
    {
        "domainId": str,
        "id": str,
        "typeName": str,
        "name": NotRequired[str],
        "description": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
        "typeRevision": NotRequired[str],
        "sourceIdentifier": NotRequired[str],
        "eventTimestamp": NotRequired[datetime],
    },
)


class LineageSqlQueryRunDetailsTypeDef(TypedDict):
    queryStartTime: NotRequired[datetime]
    queryEndTime: NotRequired[datetime]
    totalQueriesProcessed: NotRequired[int]
    numQueriesFailed: NotRequired[int]
    errorMessages: NotRequired[list[str]]


class LineageSyncScheduleTypeDef(TypedDict):
    schedule: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListAccountPoolsInputTypeDef(TypedDict):
    domainIdentifier: str
    name: NotRequired[str]
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAccountsInAccountPoolInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAssetFiltersInputTypeDef(TypedDict):
    domainIdentifier: str
    assetIdentifier: str
    status: NotRequired[FilterStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListAssetRevisionsInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


ListConnectionsInputTypeDef = TypedDict(
    "ListConnectionsInputTypeDef",
    {
        "domainIdentifier": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "sortBy": NotRequired[Literal["NAME"]],
        "sortOrder": NotRequired[SortOrderType],
        "name": NotRequired[str],
        "environmentIdentifier": NotRequired[str],
        "projectIdentifier": NotRequired[str],
        "type": NotRequired[ConnectionTypeType],
        "scope": NotRequired[ConnectionScopeType],
    },
)


class ListDataProductRevisionsInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListDataSourceRunActivitiesInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    status: NotRequired[DataAssetActivityStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListDataSourceRunsInputTypeDef(TypedDict):
    domainIdentifier: str
    dataSourceIdentifier: str
    status: NotRequired[DataSourceRunStatusType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


ListDataSourcesInputTypeDef = TypedDict(
    "ListDataSourcesInputTypeDef",
    {
        "domainIdentifier": str,
        "projectIdentifier": str,
        "environmentIdentifier": NotRequired[str],
        "connectionIdentifier": NotRequired[str],
        "type": NotRequired[str],
        "status": NotRequired[DataSourceStatusType],
        "name": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)


class ListDomainUnitsForParentInputTypeDef(TypedDict):
    domainIdentifier: str
    parentDomainUnitIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListDomainsInputTypeDef(TypedDict):
    status: NotRequired[DomainStatusType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListEntityOwnersInputTypeDef(TypedDict):
    domainIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    entityIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListEnvironmentActionsInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListEnvironmentBlueprintConfigurationsInputTypeDef(TypedDict):
    domainIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListEnvironmentBlueprintsInputTypeDef(TypedDict):
    domainIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    name: NotRequired[str]
    managed: NotRequired[bool]


class ListEnvironmentProfilesInputTypeDef(TypedDict):
    domainIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    projectIdentifier: NotRequired[str]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListEnvironmentsInputTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    awsAccountId: NotRequired[str]
    status: NotRequired[EnvironmentStatusType]
    awsAccountRegion: NotRequired[str]
    environmentProfileIdentifier: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    provider: NotRequired[str]
    name: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListJobRunsInputTypeDef(TypedDict):
    domainIdentifier: str
    jobIdentifier: str
    status: NotRequired[JobRunStatusType]
    sortOrder: NotRequired[SortOrderType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


ListMetadataGenerationRunsInputTypeDef = TypedDict(
    "ListMetadataGenerationRunsInputTypeDef",
    {
        "domainIdentifier": str,
        "status": NotRequired[MetadataGenerationRunStatusType],
        "type": NotRequired[MetadataGenerationRunTypeType],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "targetIdentifier": NotRequired[str],
    },
)


class ListPolicyGrantsInputTypeDef(TypedDict):
    domainIdentifier: str
    entityType: TargetEntityTypeType
    entityIdentifier: str
    policyType: ManagedPolicyTypeType
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListProjectMembershipsInputTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListProjectProfilesInputTypeDef(TypedDict):
    domainIdentifier: str
    name: NotRequired[str]
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


ProjectProfileSummaryTypeDef = TypedDict(
    "ProjectProfileSummaryTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "createdBy": str,
        "description": NotRequired[str],
        "status": NotRequired[StatusType],
        "createdAt": NotRequired[datetime],
        "lastUpdatedAt": NotRequired[datetime],
        "domainUnitId": NotRequired[str],
    },
)


class ListProjectsInputTypeDef(TypedDict):
    domainIdentifier: str
    userIdentifier: NotRequired[str]
    groupIdentifier: NotRequired[str]
    name: NotRequired[str]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class ListRulesInputTypeDef(TypedDict):
    domainIdentifier: str
    targetType: Literal["DOMAIN_UNIT"]
    targetIdentifier: str
    ruleType: NotRequired[RuleTypeType]
    action: NotRequired[RuleActionType]
    projectIds: NotRequired[Sequence[str]]
    assetTypes: NotRequired[Sequence[str]]
    dataProduct: NotRequired[bool]
    includeCascaded: NotRequired[bool]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSubscriptionGrantsInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentId: NotRequired[str]
    subscriptionTargetId: NotRequired[str]
    subscribedListingId: NotRequired[str]
    subscriptionId: NotRequired[str]
    owningProjectId: NotRequired[str]
    owningIamPrincipalArn: NotRequired[str]
    owningUserId: NotRequired[str]
    owningGroupId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSubscriptionRequestsInputTypeDef(TypedDict):
    domainIdentifier: str
    status: NotRequired[SubscriptionRequestStatusType]
    subscribedListingId: NotRequired[str]
    owningProjectId: NotRequired[str]
    owningIamPrincipalArn: NotRequired[str]
    approverProjectId: NotRequired[str]
    owningUserId: NotRequired[str]
    owningGroupId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSubscriptionTargetsInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListSubscriptionsInputTypeDef(TypedDict):
    domainIdentifier: str
    subscriptionRequestIdentifier: NotRequired[str]
    status: NotRequired[SubscriptionStatusType]
    subscribedListingId: NotRequired[str]
    owningProjectId: NotRequired[str]
    owningIamPrincipalArn: NotRequired[str]
    owningUserId: NotRequired[str]
    owningGroupId: NotRequired[str]
    approverProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


ManagedEndpointCredentialsTypeDef = TypedDict(
    "ManagedEndpointCredentialsTypeDef",
    {
        "id": NotRequired[str],
        "token": NotRequired[str],
    },
)


class MatchOffsetTypeDef(TypedDict):
    startOffset: NotRequired[int]
    endOffset: NotRequired[int]


class UserDetailsTypeDef(TypedDict):
    userId: str


class MetadataFormReferenceTypeDef(TypedDict):
    typeIdentifier: str
    typeRevision: str


class MetadataFormSummaryTypeDef(TypedDict):
    typeName: str
    typeRevision: str
    formName: NotRequired[str]


class NameIdentifierTypeDef(TypedDict):
    name: NotRequired[str]
    namespace: NotRequired[str]


class NotEqualToExpressionTypeDef(TypedDict):
    columnName: str
    value: str


class NotInExpressionOutputTypeDef(TypedDict):
    columnName: str
    values: list[str]


class NotInExpressionTypeDef(TypedDict):
    columnName: str
    values: Sequence[str]


class NotLikeExpressionTypeDef(TypedDict):
    columnName: str
    value: str


NotificationResourceTypeDef = TypedDict(
    "NotificationResourceTypeDef",
    {
        "type": Literal["PROJECT"],
        "id": str,
        "name": NotRequired[str],
    },
)


class OAuth2ClientApplicationTypeDef(TypedDict):
    userManagedClientApplicationClientId: NotRequired[str]
    aWSManagedClientApplicationReference: NotRequired[str]


class OverrideDomainUnitOwnersPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]


class OverrideProjectOwnersPolicyGrantDetailTypeDef(TypedDict):
    includeChildDomainUnits: NotRequired[bool]


class OwnerGroupPropertiesOutputTypeDef(TypedDict):
    groupId: NotRequired[str]


class OwnerGroupPropertiesTypeDef(TypedDict):
    groupIdentifier: str


class OwnerUserPropertiesOutputTypeDef(TypedDict):
    userId: NotRequired[str]


class OwnerUserPropertiesTypeDef(TypedDict):
    userIdentifier: str


class PermissionsOutputTypeDef(TypedDict):
    s3: NotRequired[list[S3PermissionType]]


class PermissionsTypeDef(TypedDict):
    s3: NotRequired[Sequence[S3PermissionType]]


class PhysicalConnectionRequirementsTypeDef(TypedDict):
    subnetId: NotRequired[str]
    subnetIdList: NotRequired[Sequence[str]]
    securityGroupIdList: NotRequired[Sequence[str]]
    availabilityZone: NotRequired[str]


class UseAssetTypePolicyGrantDetailTypeDef(TypedDict):
    domainUnitId: NotRequired[str]


class UserPolicyGrantPrincipalOutputTypeDef(TypedDict):
    userIdentifier: NotRequired[str]
    allUsersGrantFilter: NotRequired[dict[str, Any]]


class UserPolicyGrantPrincipalTypeDef(TypedDict):
    userIdentifier: NotRequired[str]
    allUsersGrantFilter: NotRequired[Mapping[str, Any]]


class ProjectsForRuleOutputTypeDef(TypedDict):
    selectionMode: RuleScopeSelectionModeType
    specificProjects: NotRequired[list[str]]


class ProjectsForRuleTypeDef(TypedDict):
    selectionMode: RuleScopeSelectionModeType
    specificProjects: NotRequired[Sequence[str]]


class RedshiftClusterStorageTypeDef(TypedDict):
    clusterName: str


class RedshiftCredentialConfigurationTypeDef(TypedDict):
    secretManagerArn: str


class UsernamePasswordTypeDef(TypedDict):
    password: str
    username: str


class RedshiftStoragePropertiesTypeDef(TypedDict):
    clusterName: NotRequired[str]
    workgroupName: NotRequired[str]


class RedshiftServerlessStorageTypeDef(TypedDict):
    workgroupName: str


class RejectChoiceTypeDef(TypedDict):
    predictionTarget: str
    predictionChoices: NotRequired[Sequence[int]]


class RejectRuleTypeDef(TypedDict):
    rule: NotRequired[RejectRuleBehaviorType]
    threshold: NotRequired[float]


class RejectSubscriptionRequestInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    decisionComment: NotRequired[str]


class RevokeSubscriptionInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    retainPermissions: NotRequired[bool]


class SearchGroupProfilesInputTypeDef(TypedDict):
    domainIdentifier: str
    groupType: GroupSearchTypeType
    searchText: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SearchInItemTypeDef(TypedDict):
    attribute: str


class SearchSortTypeDef(TypedDict):
    attribute: str
    order: NotRequired[SortOrderType]


class SearchUserProfilesInputTypeDef(TypedDict):
    domainIdentifier: str
    userType: UserSearchTypeType
    searchText: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class SparkGlueArgsTypeDef(TypedDict):
    connection: NotRequired[str]


class SsoUserProfileDetailsTypeDef(TypedDict):
    username: NotRequired[str]
    firstName: NotRequired[str]
    lastName: NotRequired[str]


class StartDataSourceRunInputTypeDef(TypedDict):
    domainIdentifier: str
    dataSourceIdentifier: str
    clientToken: NotRequired[str]


class SubscribedGroupInputTypeDef(TypedDict):
    identifier: NotRequired[str]


SubscribedGroupTypeDef = TypedDict(
    "SubscribedGroupTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)


class SubscribedIamPrincipalInputTypeDef(TypedDict):
    identifier: NotRequired[str]


class SubscribedIamPrincipalTypeDef(TypedDict):
    principalArn: NotRequired[str]


class SubscribedProjectInputTypeDef(TypedDict):
    identifier: NotRequired[str]


class SubscribedUserInputTypeDef(TypedDict):
    identifier: NotRequired[str]


SubscribedProjectTypeDef = TypedDict(
    "SubscribedProjectTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class TermRelationsTypeDef(TypedDict):
    isA: NotRequired[Sequence[str]]
    classifies: NotRequired[Sequence[str]]


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class UpdateDomainUnitInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    name: NotRequired[str]


class UpdateGlossaryInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[GlossaryStatusType]
    clientToken: NotRequired[str]


class UpdateGroupProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    groupIdentifier: str
    status: GroupProfileStatusType


class UpdateRootDomainUnitOwnerInputTypeDef(TypedDict):
    domainIdentifier: str
    currentOwner: str
    newOwner: str
    clientToken: NotRequired[str]


class UpdateSubscriptionRequestInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    requestReason: str


UpdateUserProfileInputTypeDef = TypedDict(
    "UpdateUserProfileInputTypeDef",
    {
        "domainIdentifier": str,
        "userIdentifier": str,
        "status": UserProfileStatusType,
        "type": NotRequired[UserProfileTypeType],
    },
)


class AcceptPredictionsInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]
    acceptRule: NotRequired[AcceptRuleTypeDef]
    acceptChoices: NotRequired[Sequence[AcceptChoiceTypeDef]]
    clientToken: NotRequired[str]


class AcceptPredictionsOutputTypeDef(TypedDict):
    domainId: str
    assetId: str
    revision: str
    ResponseMetadata: ResponseMetadataTypeDef


class AddPolicyGrantOutputTypeDef(TypedDict):
    grantId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateFormTypeOutputTypeDef(TypedDict):
    domainId: str
    name: str
    revision: str
    description: str
    owningProjectId: str
    originDomainId: str
    originProjectId: str
    ResponseMetadata: ResponseMetadataTypeDef


CreateGlossaryOutputTypeDef = TypedDict(
    "CreateGlossaryOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "description": str,
        "status": GlossaryStatusType,
        "usageRestrictions": list[Literal["ASSET_GOVERNED_TERMS"]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateGroupProfileOutputTypeDef = TypedDict(
    "CreateGroupProfileOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "status": GroupProfileStatusType,
        "groupName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateListingChangeSetOutputTypeDef(TypedDict):
    listingId: str
    listingRevision: str
    status: ListingStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteConnectionOutputTypeDef(TypedDict):
    status: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDomainOutputTypeDef(TypedDict):
    status: DomainStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetEnvironmentCredentialsOutputTypeDef(TypedDict):
    accessKeyId: str
    secretAccessKey: str
    sessionToken: str
    expiration: datetime
    ResponseMetadata: ResponseMetadataTypeDef


GetGlossaryOutputTypeDef = TypedDict(
    "GetGlossaryOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "owningProjectId": str,
        "name": str,
        "description": str,
        "status": GlossaryStatusType,
        "createdAt": datetime,
        "createdBy": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "usageRestrictions": list[Literal["ASSET_GOVERNED_TERMS"]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGroupProfileOutputTypeDef = TypedDict(
    "GetGroupProfileOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "status": GroupProfileStatusType,
        "groupName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GetIamPortalLoginUrlOutputTypeDef(TypedDict):
    authCodeUrl: str
    userProfileId: str
    ResponseMetadata: ResponseMetadataTypeDef


GetLineageEventOutputTypeDef = TypedDict(
    "GetLineageEventOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "event": StreamingBody,
        "createdBy": str,
        "processingStatus": LineageEventProcessingStatusType,
        "eventTime": datetime,
        "createdAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


PostLineageEventOutputTypeDef = TypedDict(
    "PostLineageEventOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class RejectPredictionsOutputTypeDef(TypedDict):
    domainId: str
    assetId: str
    assetRevision: str
    ResponseMetadata: ResponseMetadataTypeDef


StartMetadataGenerationRunOutputTypeDef = TypedDict(
    "StartMetadataGenerationRunOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "status": MetadataGenerationRunStatusType,
        "type": MetadataGenerationRunTypeType,
        "types": list[MetadataGenerationRunTypeType],
        "createdAt": datetime,
        "createdBy": str,
        "owningProjectId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGlossaryOutputTypeDef = TypedDict(
    "UpdateGlossaryOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "description": str,
        "status": GlossaryStatusType,
        "usageRestrictions": list[Literal["ASSET_GOVERNED_TERMS"]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGroupProfileOutputTypeDef = TypedDict(
    "UpdateGroupProfileOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "status": GroupProfileStatusType,
        "groupName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class BatchGetAttributeOutputTypeDef(TypedDict):
    attributeIdentifier: str
    forms: NotRequired[list[FormOutputTypeDef]]


class ListAccountsInAccountPoolOutputTypeDef(TypedDict):
    items: list[AccountInfoOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListAccountPoolsOutputTypeDef(TypedDict):
    items: list[AccountPoolSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AccountSourceOutputTypeDef(TypedDict):
    accounts: NotRequired[list[AccountInfoOutputTypeDef]]
    customAccountPoolHandler: NotRequired[CustomAccountPoolHandlerTypeDef]


class AccountSourceTypeDef(TypedDict):
    accounts: NotRequired[Sequence[AccountInfoTypeDef]]
    customAccountPoolHandler: NotRequired[CustomAccountPoolHandlerTypeDef]


class ActionParametersTypeDef(TypedDict):
    awsConsoleLink: NotRequired[AwsConsoleLinkParametersTypeDef]


class AggregationOutputTypeDef(TypedDict):
    attribute: NotRequired[str]
    displayValue: NotRequired[str]
    items: NotRequired[list[AggregationOutputItemTypeDef]]


class ListAssetFiltersOutputTypeDef(TypedDict):
    items: list[AssetFilterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTimeSeriesDataPointsOutputTypeDef(TypedDict):
    items: list[TimeSeriesDataPointSummaryFormOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


GetAssetOutputTypeDef = TypedDict(
    "GetAssetOutputTypeDef",
    {
        "id": str,
        "name": str,
        "typeIdentifier": str,
        "typeRevision": str,
        "externalIdentifier": str,
        "revision": str,
        "description": str,
        "createdAt": datetime,
        "createdBy": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "glossaryTerms": list[str],
        "governedGlossaryTerms": list[str],
        "owningProjectId": str,
        "domainId": str,
        "listing": AssetListingDetailsTypeDef,
        "formsOutput": list[FormOutputTypeDef],
        "readOnlyFormsOutput": list[FormOutputTypeDef],
        "latestTimeSeriesDataPointFormsOutput": list[TimeSeriesDataPointSummaryFormOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class AssetListingTypeDef(TypedDict):
    assetId: NotRequired[str]
    assetRevision: NotRequired[str]
    assetType: NotRequired[str]
    createdAt: NotRequired[datetime]
    forms: NotRequired[str]
    latestTimeSeriesDataPointForms: NotRequired[list[TimeSeriesDataPointSummaryFormOutputTypeDef]]
    glossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]
    governedGlossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]
    owningProjectId: NotRequired[str]


class ListingSummaryItemTypeDef(TypedDict):
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]
    glossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]


class ListingSummaryTypeDef(TypedDict):
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]
    glossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]


class SubscribedProductListingTypeDef(TypedDict):
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    glossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]
    name: NotRequired[str]
    description: NotRequired[str]
    assetListings: NotRequired[list[AssetInDataProductListingItemTypeDef]]


class ListAssetRevisionsOutputTypeDef(TypedDict):
    items: list[AssetRevisionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AssetTypeItemTypeDef(TypedDict):
    domainId: str
    name: str
    revision: str
    formsOutput: dict[str, FormEntryOutputTypeDef]
    owningProjectId: str
    description: NotRequired[str]
    originDomainId: NotRequired[str]
    originProjectId: NotRequired[str]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]


class CreateAssetTypeOutputTypeDef(TypedDict):
    domainId: str
    name: str
    revision: str
    description: str
    formsOutput: dict[str, FormEntryOutputTypeDef]
    owningProjectId: str
    originDomainId: str
    originProjectId: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetAssetTypeOutputTypeDef(TypedDict):
    domainId: str
    name: str
    revision: str
    description: str
    formsOutput: dict[str, FormEntryOutputTypeDef]
    owningProjectId: str
    originDomainId: str
    originProjectId: str
    createdAt: datetime
    createdBy: str
    updatedAt: datetime
    updatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef


class LineageNodeTypeItemTypeDef(TypedDict):
    domainId: str
    revision: str
    formsOutput: dict[str, FormEntryOutputTypeDef]
    name: NotRequired[str]
    description: NotRequired[str]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    updatedAt: NotRequired[datetime]
    updatedBy: NotRequired[str]


class AttributeInputTypeDef(TypedDict):
    attributeIdentifier: str
    forms: Sequence[FormInputTypeDef]


class AuthenticationConfigurationPatchTypeDef(TypedDict):
    secretArn: NotRequired[str]
    basicAuthenticationCredentials: NotRequired[BasicAuthenticationCredentialsTypeDef]


class BatchPutAttributesMetadataOutputTypeDef(TypedDict):
    errors: list[AttributeErrorTypeDef]
    attributes: list[BatchPutAttributeOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PostLineageEventInputTypeDef(TypedDict):
    domainIdentifier: str
    event: BlobTypeDef
    clientToken: NotRequired[str]


class PredictionConfigurationTypeDef(TypedDict):
    businessNameGeneration: NotRequired[BusinessNameGenerationConfigurationTypeDef]


class ProvisioningPropertiesTypeDef(TypedDict):
    cloudFormation: NotRequired[CloudFormationPropertiesTypeDef]


ConfigurableEnvironmentActionTypeDef = TypedDict(
    "ConfigurableEnvironmentActionTypeDef",
    {
        "type": str,
        "parameters": list[ConfigurableActionParameterTypeDef],
        "auth": NotRequired[ConfigurableActionTypeAuthorizationType],
    },
)


class CreateAssetTypeInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    formsInput: Mapping[str, FormEntryInputTypeDef]
    owningProjectIdentifier: str
    description: NotRequired[str]


CreateDataProductOutputTypeDef = TypedDict(
    "CreateDataProductOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "revision": str,
        "owningProjectId": str,
        "name": str,
        "status": DataProductStatusType,
        "description": str,
        "glossaryTerms": list[str],
        "items": list[DataProductItemOutputTypeDef],
        "formsOutput": list[FormOutputTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDataProductRevisionOutputTypeDef = TypedDict(
    "CreateDataProductRevisionOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "revision": str,
        "owningProjectId": str,
        "name": str,
        "status": DataProductStatusType,
        "description": str,
        "glossaryTerms": list[str],
        "items": list[DataProductItemOutputTypeDef],
        "formsOutput": list[FormOutputTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataProductOutputTypeDef = TypedDict(
    "GetDataProductOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "revision": str,
        "owningProjectId": str,
        "name": str,
        "status": DataProductStatusType,
        "description": str,
        "glossaryTerms": list[str],
        "items": list[DataProductItemOutputTypeDef],
        "formsOutput": list[FormOutputTypeDef],
        "createdAt": datetime,
        "createdBy": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataSourceSummaryTypeDef = TypedDict(
    "DataSourceSummaryTypeDef",
    {
        "domainId": str,
        "dataSourceId": str,
        "name": str,
        "type": str,
        "status": DataSourceStatusType,
        "environmentId": NotRequired[str],
        "connectionId": NotRequired[str],
        "enableSetting": NotRequired[EnableSettingType],
        "schedule": NotRequired[ScheduleConfigurationTypeDef],
        "lastRunStatus": NotRequired[DataSourceRunStatusType],
        "lastRunAt": NotRequired[datetime],
        "lastRunErrorMessage": NotRequired[DataSourceErrorMessageTypeDef],
        "lastRunAssetCount": NotRequired[int],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "description": NotRequired[str],
    },
)


class CreateDomainInputTypeDef(TypedDict):
    name: str
    domainExecutionRole: str
    description: NotRequired[str]
    singleSignOn: NotRequired[SingleSignOnTypeDef]
    kmsKeyIdentifier: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    domainVersion: NotRequired[DomainVersionType]
    serviceRole: NotRequired[str]
    clientToken: NotRequired[str]


CreateDomainOutputTypeDef = TypedDict(
    "CreateDomainOutputTypeDef",
    {
        "id": str,
        "rootDomainUnitId": str,
        "name": str,
        "description": str,
        "singleSignOn": SingleSignOnTypeDef,
        "domainExecutionRole": str,
        "arn": str,
        "kmsKeyIdentifier": str,
        "status": DomainStatusType,
        "portalUrl": str,
        "tags": dict[str, str],
        "domainVersion": DomainVersionType,
        "serviceRole": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDomainOutputTypeDef = TypedDict(
    "GetDomainOutputTypeDef",
    {
        "id": str,
        "rootDomainUnitId": str,
        "name": str,
        "description": str,
        "singleSignOn": SingleSignOnTypeDef,
        "domainExecutionRole": str,
        "arn": str,
        "kmsKeyIdentifier": str,
        "status": DomainStatusType,
        "portalUrl": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "tags": dict[str, str],
        "domainVersion": DomainVersionType,
        "serviceRole": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdateDomainInputTypeDef(TypedDict):
    identifier: str
    description: NotRequired[str]
    singleSignOn: NotRequired[SingleSignOnTypeDef]
    domainExecutionRole: NotRequired[str]
    serviceRole: NotRequired[str]
    name: NotRequired[str]
    clientToken: NotRequired[str]


UpdateDomainOutputTypeDef = TypedDict(
    "UpdateDomainOutputTypeDef",
    {
        "id": str,
        "rootDomainUnitId": str,
        "description": str,
        "singleSignOn": SingleSignOnTypeDef,
        "domainExecutionRole": str,
        "serviceRole": str,
        "name": str,
        "lastUpdatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateEnvironmentProfileOutputTypeDef = TypedDict(
    "CreateEnvironmentProfileOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "name": str,
        "description": str,
        "environmentBlueprintId": str,
        "projectId": str,
        "userParameters": list[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetEnvironmentProfileOutputTypeDef = TypedDict(
    "GetEnvironmentProfileOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "name": str,
        "description": str,
        "environmentBlueprintId": str,
        "projectId": str,
        "userParameters": list[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateEnvironmentProfileOutputTypeDef = TypedDict(
    "UpdateEnvironmentProfileOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "awsAccountId": str,
        "awsAccountRegion": str,
        "createdBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "name": str,
        "description": str,
        "environmentBlueprintId": str,
        "projectId": str,
        "userParameters": list[CustomParameterTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateEnvironmentInputTypeDef(TypedDict):
    projectIdentifier: str
    domainIdentifier: str
    name: str
    description: NotRequired[str]
    environmentProfileIdentifier: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]
    glossaryTerms: NotRequired[Sequence[str]]
    environmentAccountIdentifier: NotRequired[str]
    environmentAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    deploymentOrder: NotRequired[int]
    environmentConfigurationId: NotRequired[str]


class CreateEnvironmentProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    environmentBlueprintIdentifier: str
    projectIdentifier: str
    description: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]


class UpdateEnvironmentInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    blueprintVersion: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]


class UpdateEnvironmentProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]


class CreateFormTypeInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    model: ModelTypeDef
    owningProjectIdentifier: str
    status: NotRequired[FormTypeStatusType]
    description: NotRequired[str]


CreateGlossaryTermOutputTypeDef = TypedDict(
    "CreateGlossaryTermOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "glossaryId": str,
        "name": str,
        "status": GlossaryTermStatusType,
        "shortDescription": str,
        "longDescription": str,
        "termRelations": TermRelationsOutputTypeDef,
        "usageRestrictions": list[Literal["ASSET_GOVERNED_TERMS"]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetGlossaryTermOutputTypeDef = TypedDict(
    "GetGlossaryTermOutputTypeDef",
    {
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "name": str,
        "shortDescription": str,
        "longDescription": str,
        "termRelations": TermRelationsOutputTypeDef,
        "status": GlossaryTermStatusType,
        "createdAt": datetime,
        "createdBy": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "usageRestrictions": list[Literal["ASSET_GOVERNED_TERMS"]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateGlossaryTermOutputTypeDef = TypedDict(
    "UpdateGlossaryTermOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "glossaryId": str,
        "name": str,
        "status": GlossaryTermStatusType,
        "shortDescription": str,
        "longDescription": str,
        "termRelations": TermRelationsOutputTypeDef,
        "usageRestrictions": list[Literal["ASSET_GOVERNED_TERMS"]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateProjectMembershipInputTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    member: MemberTypeDef
    designation: UserDesignationType


class DeleteProjectMembershipInputTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    member: MemberTypeDef


ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "createdBy": str,
        "description": NotRequired[str],
        "projectStatus": NotRequired[ProjectStatusType],
        "failureReasons": NotRequired[list[ProjectDeletionErrorTypeDef]],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "domainUnitId": NotRequired[str],
    },
)
CreateSubscriptionTargetInputTypeDef = TypedDict(
    "CreateSubscriptionTargetInputTypeDef",
    {
        "domainIdentifier": str,
        "environmentIdentifier": str,
        "name": str,
        "type": str,
        "subscriptionTargetConfig": Sequence[SubscriptionTargetFormTypeDef],
        "authorizedPrincipals": Sequence[str],
        "manageAccessRole": str,
        "applicableAssetTypes": Sequence[str],
        "provider": NotRequired[str],
        "clientToken": NotRequired[str],
        "subscriptionGrantCreationMode": NotRequired[SubscriptionGrantCreationModeType],
    },
)
CreateSubscriptionTargetOutputTypeDef = TypedDict(
    "CreateSubscriptionTargetOutputTypeDef",
    {
        "id": str,
        "authorizedPrincipals": list[str],
        "domainId": str,
        "projectId": str,
        "environmentId": str,
        "name": str,
        "type": str,
        "createdBy": str,
        "updatedBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "manageAccessRole": str,
        "applicableAssetTypes": list[str],
        "subscriptionTargetConfig": list[SubscriptionTargetFormTypeDef],
        "provider": str,
        "subscriptionGrantCreationMode": SubscriptionGrantCreationModeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionTargetOutputTypeDef = TypedDict(
    "GetSubscriptionTargetOutputTypeDef",
    {
        "id": str,
        "authorizedPrincipals": list[str],
        "domainId": str,
        "projectId": str,
        "environmentId": str,
        "name": str,
        "type": str,
        "createdBy": str,
        "updatedBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "manageAccessRole": str,
        "applicableAssetTypes": list[str],
        "subscriptionTargetConfig": list[SubscriptionTargetFormTypeDef],
        "provider": str,
        "subscriptionGrantCreationMode": SubscriptionGrantCreationModeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscriptionTargetSummaryTypeDef = TypedDict(
    "SubscriptionTargetSummaryTypeDef",
    {
        "id": str,
        "authorizedPrincipals": list[str],
        "domainId": str,
        "projectId": str,
        "environmentId": str,
        "name": str,
        "type": str,
        "createdBy": str,
        "createdAt": datetime,
        "applicableAssetTypes": list[str],
        "subscriptionTargetConfig": list[SubscriptionTargetFormTypeDef],
        "provider": str,
        "updatedBy": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "manageAccessRole": NotRequired[str],
        "subscriptionGrantCreationMode": NotRequired[SubscriptionGrantCreationModeType],
    },
)


class UpdateSubscriptionTargetInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str
    name: NotRequired[str]
    authorizedPrincipals: NotRequired[Sequence[str]]
    applicableAssetTypes: NotRequired[Sequence[str]]
    subscriptionTargetConfig: NotRequired[Sequence[SubscriptionTargetFormTypeDef]]
    manageAccessRole: NotRequired[str]
    provider: NotRequired[str]
    subscriptionGrantCreationMode: NotRequired[SubscriptionGrantCreationModeType]


UpdateSubscriptionTargetOutputTypeDef = TypedDict(
    "UpdateSubscriptionTargetOutputTypeDef",
    {
        "id": str,
        "authorizedPrincipals": list[str],
        "domainId": str,
        "projectId": str,
        "environmentId": str,
        "name": str,
        "type": str,
        "createdBy": str,
        "updatedBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "manageAccessRole": str,
        "applicableAssetTypes": list[str],
        "subscriptionTargetConfig": list[SubscriptionTargetFormTypeDef],
        "provider": str,
        "subscriptionGrantCreationMode": SubscriptionGrantCreationModeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataProductItemUnionTypeDef = Union[DataProductItemTypeDef, DataProductItemOutputTypeDef]


class ListDataProductRevisionsOutputTypeDef(TypedDict):
    items: list[DataProductRevisionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class DataSourceRunActivityTypeDef(TypedDict):
    database: str
    dataSourceRunId: str
    technicalName: str
    dataAssetStatus: DataAssetActivityStatusType
    projectId: str
    createdAt: datetime
    updatedAt: datetime
    dataAssetId: NotRequired[str]
    technicalDescription: NotRequired[str]
    errorMessage: NotRequired[DataSourceErrorMessageTypeDef]
    lineageSummary: NotRequired[LineageInfoTypeDef]


DataSourceRunSummaryTypeDef = TypedDict(
    "DataSourceRunSummaryTypeDef",
    {
        "id": str,
        "dataSourceId": str,
        "type": DataSourceRunTypeType,
        "status": DataSourceRunStatusType,
        "projectId": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "runStatisticsForAssets": NotRequired[RunStatisticsForAssetsTypeDef],
        "errorMessage": NotRequired[DataSourceErrorMessageTypeDef],
        "startedAt": NotRequired[datetime],
        "stoppedAt": NotRequired[datetime],
        "lineageSummary": NotRequired[DataSourceRunLineageSummaryTypeDef],
    },
)
GetDataSourceRunOutputTypeDef = TypedDict(
    "GetDataSourceRunOutputTypeDef",
    {
        "domainId": str,
        "dataSourceId": str,
        "id": str,
        "projectId": str,
        "status": DataSourceRunStatusType,
        "type": DataSourceRunTypeType,
        "dataSourceConfigurationSnapshot": str,
        "runStatisticsForAssets": RunStatisticsForAssetsTypeDef,
        "lineageSummary": DataSourceRunLineageSummaryTypeDef,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "startedAt": datetime,
        "stoppedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
StartDataSourceRunOutputTypeDef = TypedDict(
    "StartDataSourceRunOutputTypeDef",
    {
        "domainId": str,
        "dataSourceId": str,
        "id": str,
        "projectId": str,
        "status": DataSourceRunStatusType,
        "type": DataSourceRunTypeType,
        "dataSourceConfigurationSnapshot": str,
        "runStatisticsForAssets": RunStatisticsForAssetsTypeDef,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "startedAt": datetime,
        "stoppedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DeploymentTypeDef(TypedDict):
    deploymentId: NotRequired[str]
    deploymentType: NotRequired[DeploymentTypeType]
    deploymentStatus: NotRequired[DeploymentStatusType]
    failureReason: NotRequired[EnvironmentErrorTypeDef]
    messages: NotRequired[list[str]]
    isDeploymentComplete: NotRequired[bool]


class EnvironmentDeploymentDetailsOutputTypeDef(TypedDict):
    overallDeploymentStatus: NotRequired[OverallDeploymentStatusType]
    environmentFailureReasons: NotRequired[dict[str, list[EnvironmentErrorTypeDef]]]


class EnvironmentDeploymentDetailsTypeDef(TypedDict):
    overallDeploymentStatus: NotRequired[OverallDeploymentStatusType]
    environmentFailureReasons: NotRequired[Mapping[str, Sequence[EnvironmentErrorTypeDef]]]


class ListDomainsOutputTypeDef(TypedDict):
    items: list[DomainSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ProjectGrantFilterTypeDef(TypedDict):
    domainUnitFilter: NotRequired[DomainUnitFilterForProjectTypeDef]


class DomainUnitPolicyGrantPrincipalOutputTypeDef(TypedDict):
    domainUnitDesignation: Literal["OWNER"]
    domainUnitIdentifier: NotRequired[str]
    domainUnitGrantFilter: NotRequired[DomainUnitGrantFilterOutputTypeDef]


class DomainUnitPolicyGrantPrincipalTypeDef(TypedDict):
    domainUnitDesignation: Literal["OWNER"]
    domainUnitIdentifier: NotRequired[str]
    domainUnitGrantFilter: NotRequired[DomainUnitGrantFilterTypeDef]


class DomainUnitOwnerPropertiesTypeDef(TypedDict):
    user: NotRequired[DomainUnitUserPropertiesTypeDef]
    group: NotRequired[DomainUnitGroupPropertiesTypeDef]


class ListDomainUnitsForParentOutputTypeDef(TypedDict):
    items: list[DomainUnitSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class RuleTargetTypeDef(TypedDict):
    domainUnitTarget: NotRequired[DomainUnitTargetTypeDef]


class GetDataExportConfigurationOutputTypeDef(TypedDict):
    isExportEnabled: bool
    status: ConfigurationStatusType
    encryptionConfiguration: EncryptionConfigurationTypeDef
    s3TableBucketArn: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef


class PutDataExportConfigurationInputTypeDef(TypedDict):
    domainIdentifier: str
    enableExport: bool
    encryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    clientToken: NotRequired[str]


class EnvironmentConfigurationParametersDetailsOutputTypeDef(TypedDict):
    ssmPath: NotRequired[str]
    parameterOverrides: NotRequired[list[EnvironmentConfigurationParameterTypeDef]]
    resolvedParameters: NotRequired[list[EnvironmentConfigurationParameterTypeDef]]


class EnvironmentConfigurationParametersDetailsTypeDef(TypedDict):
    ssmPath: NotRequired[str]
    parameterOverrides: NotRequired[Sequence[EnvironmentConfigurationParameterTypeDef]]
    resolvedParameters: NotRequired[Sequence[EnvironmentConfigurationParameterTypeDef]]


class EnvironmentConfigurationUserParameterOutputTypeDef(TypedDict):
    environmentId: NotRequired[str]
    environmentResolvedAccount: NotRequired[EnvironmentResolvedAccountTypeDef]
    environmentConfigurationName: NotRequired[str]
    environmentParameters: NotRequired[list[EnvironmentParameterTypeDef]]


class EnvironmentConfigurationUserParameterTypeDef(TypedDict):
    environmentId: NotRequired[str]
    environmentResolvedAccount: NotRequired[EnvironmentResolvedAccountTypeDef]
    environmentConfigurationName: NotRequired[str]
    environmentParameters: NotRequired[Sequence[EnvironmentParameterTypeDef]]


class ListEnvironmentProfilesOutputTypeDef(TypedDict):
    items: list[EnvironmentProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListEnvironmentsOutputTypeDef(TypedDict):
    items: list[EnvironmentSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateSubscriptionGrantStatusInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    assetIdentifier: str
    status: SubscriptionGrantStatusType
    failureCause: NotRequired[FailureCauseTypeDef]
    targetName: NotRequired[str]


FilterClausePaginatorTypeDef = TypedDict(
    "FilterClausePaginatorTypeDef",
    {
        "filter": NotRequired[FilterTypeDef],
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
    },
)
FilterClauseTypeDef = TypedDict(
    "FilterClauseTypeDef",
    {
        "filter": NotRequired[FilterTypeDef],
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
    },
)


class RelationalFilterConfigurationOutputTypeDef(TypedDict):
    databaseName: str
    schemaName: NotRequired[str]
    filterExpressions: NotRequired[list[FilterExpressionTypeDef]]


class RelationalFilterConfigurationTypeDef(TypedDict):
    databaseName: str
    schemaName: NotRequired[str]
    filterExpressions: NotRequired[Sequence[FilterExpressionTypeDef]]


class FormTypeDataTypeDef(TypedDict):
    domainId: str
    name: str
    revision: str
    model: NotRequired[ModelTypeDef]
    status: NotRequired[FormTypeStatusType]
    owningProjectId: NotRequired[str]
    originDomainId: NotRequired[str]
    originProjectId: NotRequired[str]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    description: NotRequired[str]
    imports: NotRequired[list[ImportTypeDef]]


class GetFormTypeOutputTypeDef(TypedDict):
    domainId: str
    name: str
    revision: str
    model: ModelTypeDef
    owningProjectId: str
    originDomainId: str
    originProjectId: str
    status: FormTypeStatusType
    createdAt: datetime
    createdBy: str
    description: str
    imports: list[ImportTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class JobRunSummaryTypeDef(TypedDict):
    domainId: NotRequired[str]
    jobId: NotRequired[str]
    jobType: NotRequired[Literal["LINEAGE"]]
    runId: NotRequired[str]
    runMode: NotRequired[JobRunModeType]
    status: NotRequired[JobRunStatusType]
    error: NotRequired[JobRunErrorTypeDef]
    createdBy: NotRequired[str]
    createdAt: NotRequired[datetime]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]


class GetLineageNodeInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    eventTimestamp: NotRequired[TimestampTypeDef]


class ListLineageEventsInputTypeDef(TypedDict):
    domainIdentifier: str
    maxResults: NotRequired[int]
    timestampAfter: NotRequired[TimestampTypeDef]
    timestampBefore: NotRequired[TimestampTypeDef]
    processingStatus: NotRequired[LineageEventProcessingStatusType]
    sortOrder: NotRequired[SortOrderType]
    nextToken: NotRequired[str]


class ListLineageNodeHistoryInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    direction: NotRequired[EdgeDirectionType]
    eventTimestampGTE: NotRequired[TimestampTypeDef]
    eventTimestampLTE: NotRequired[TimestampTypeDef]
    sortOrder: NotRequired[SortOrderType]


ListNotificationsInputTypeDef = TypedDict(
    "ListNotificationsInputTypeDef",
    {
        "domainIdentifier": str,
        "type": NotificationTypeType,
        "afterTimestamp": NotRequired[TimestampTypeDef],
        "beforeTimestamp": NotRequired[TimestampTypeDef],
        "subjects": NotRequired[Sequence[str]],
        "taskStatus": NotRequired[TaskStatusType],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)


class ListTimeSeriesDataPointsInputTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    startedAt: NotRequired[TimestampTypeDef]
    endedAt: NotRequired[TimestampTypeDef]
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]


class TimeSeriesDataPointFormInputTypeDef(TypedDict):
    formName: str
    typeIdentifier: str
    timestamp: TimestampTypeDef
    typeRevision: NotRequired[str]
    content: NotRequired[str]


GetLineageNodeOutputTypeDef = TypedDict(
    "GetLineageNodeOutputTypeDef",
    {
        "domainId": str,
        "name": str,
        "description": str,
        "createdAt": datetime,
        "createdBy": str,
        "updatedAt": datetime,
        "updatedBy": str,
        "id": str,
        "typeName": str,
        "typeRevision": str,
        "sourceIdentifier": str,
        "eventTimestamp": datetime,
        "formsOutput": list[FormOutputTypeDef],
        "upstreamNodes": list[LineageNodeReferenceTypeDef],
        "downstreamNodes": list[LineageNodeReferenceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
MetadataGenerationRunItemTypeDef = TypedDict(
    "MetadataGenerationRunItemTypeDef",
    {
        "domainId": str,
        "id": str,
        "owningProjectId": str,
        "target": NotRequired[MetadataGenerationRunTargetTypeDef],
        "status": NotRequired[MetadataGenerationRunStatusType],
        "type": NotRequired[MetadataGenerationRunTypeType],
        "types": NotRequired[list[MetadataGenerationRunTypeType]],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
    },
)
StartMetadataGenerationRunInputTypeDef = TypedDict(
    "StartMetadataGenerationRunInputTypeDef",
    {
        "domainIdentifier": str,
        "target": MetadataGenerationRunTargetTypeDef,
        "owningProjectIdentifier": str,
        "type": NotRequired[MetadataGenerationRunTypeType],
        "types": NotRequired[Sequence[MetadataGenerationRunTypeType]],
        "clientToken": NotRequired[str],
    },
)
GetMetadataGenerationRunOutputTypeDef = TypedDict(
    "GetMetadataGenerationRunOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "target": MetadataGenerationRunTargetTypeDef,
        "status": MetadataGenerationRunStatusType,
        "type": MetadataGenerationRunTypeType,
        "types": list[MetadataGenerationRunTypeType],
        "createdAt": datetime,
        "createdBy": str,
        "owningProjectId": str,
        "typeStats": list[MetadataGenerationRunTypeStatTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GetTimeSeriesDataPointOutputTypeDef(TypedDict):
    domainId: str
    entityId: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    form: TimeSeriesDataPointFormOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class PostTimeSeriesDataPointsOutputTypeDef(TypedDict):
    domainId: str
    entityId: str
    entityType: TimeSeriesEntityTypeType
    forms: list[TimeSeriesDataPointFormOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GlueSelfGrantStatusOutputTypeDef(TypedDict):
    selfGrantStatusDetails: list[SelfGrantStatusDetailTypeDef]


class RedshiftSelfGrantStatusOutputTypeDef(TypedDict):
    selfGrantStatusDetails: list[SelfGrantStatusDetailTypeDef]


class GrantedEntityInputTypeDef(TypedDict):
    listing: NotRequired[ListingRevisionInputTypeDef]


class GrantedEntityTypeDef(TypedDict):
    listing: NotRequired[ListingRevisionTypeDef]


class SearchGroupProfilesOutputTypeDef(TypedDict):
    items: list[GroupProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ProvisioningConfigurationOutputTypeDef(TypedDict):
    lakeFormationConfiguration: NotRequired[LakeFormationConfigurationOutputTypeDef]


LakeFormationConfigurationUnionTypeDef = Union[
    LakeFormationConfigurationTypeDef, LakeFormationConfigurationOutputTypeDef
]


class ListLineageNodeHistoryOutputTypeDef(TypedDict):
    nodes: list[LineageNodeSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class LineageRunDetailsTypeDef(TypedDict):
    sqlQueryRunDetails: NotRequired[LineageSqlQueryRunDetailsTypeDef]


class RedshiftLineageSyncConfigurationInputTypeDef(TypedDict):
    enabled: NotRequired[bool]
    schedule: NotRequired[LineageSyncScheduleTypeDef]


class RedshiftLineageSyncConfigurationOutputTypeDef(TypedDict):
    lineageJobId: NotRequired[str]
    enabled: NotRequired[bool]
    schedule: NotRequired[LineageSyncScheduleTypeDef]


class ListAccountPoolsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    name: NotRequired[str]
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAccountsInAccountPoolInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetFiltersInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    assetIdentifier: str
    status: NotRequired[FilterStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListAssetRevisionsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListConnectionsInputPaginateTypeDef = TypedDict(
    "ListConnectionsInputPaginateTypeDef",
    {
        "domainIdentifier": str,
        "sortBy": NotRequired[Literal["NAME"]],
        "sortOrder": NotRequired[SortOrderType],
        "name": NotRequired[str],
        "environmentIdentifier": NotRequired[str],
        "projectIdentifier": NotRequired[str],
        "type": NotRequired[ConnectionTypeType],
        "scope": NotRequired[ConnectionScopeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListDataProductRevisionsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSourceRunActivitiesInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    status: NotRequired[DataAssetActivityStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDataSourceRunsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    dataSourceIdentifier: str
    status: NotRequired[DataSourceRunStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListDataSourcesInputPaginateTypeDef = TypedDict(
    "ListDataSourcesInputPaginateTypeDef",
    {
        "domainIdentifier": str,
        "projectIdentifier": str,
        "environmentIdentifier": NotRequired[str],
        "connectionIdentifier": NotRequired[str],
        "type": NotRequired[str],
        "status": NotRequired[DataSourceStatusType],
        "name": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListDomainUnitsForParentInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    parentDomainUnitIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDomainsInputPaginateTypeDef(TypedDict):
    status: NotRequired[DomainStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEntityOwnersInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    entityIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentActionsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentBlueprintConfigurationsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentBlueprintsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    name: NotRequired[str]
    managed: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentProfilesInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    awsAccountId: NotRequired[str]
    awsAccountRegion: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    projectIdentifier: NotRequired[str]
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListEnvironmentsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    awsAccountId: NotRequired[str]
    status: NotRequired[EnvironmentStatusType]
    awsAccountRegion: NotRequired[str]
    environmentProfileIdentifier: NotRequired[str]
    environmentBlueprintIdentifier: NotRequired[str]
    provider: NotRequired[str]
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListJobRunsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    jobIdentifier: str
    status: NotRequired[JobRunStatusType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLineageEventsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    timestampAfter: NotRequired[TimestampTypeDef]
    timestampBefore: NotRequired[TimestampTypeDef]
    processingStatus: NotRequired[LineageEventProcessingStatusType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListLineageNodeHistoryInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    direction: NotRequired[EdgeDirectionType]
    eventTimestampGTE: NotRequired[TimestampTypeDef]
    eventTimestampLTE: NotRequired[TimestampTypeDef]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


ListMetadataGenerationRunsInputPaginateTypeDef = TypedDict(
    "ListMetadataGenerationRunsInputPaginateTypeDef",
    {
        "domainIdentifier": str,
        "status": NotRequired[MetadataGenerationRunStatusType],
        "type": NotRequired[MetadataGenerationRunTypeType],
        "targetIdentifier": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListNotificationsInputPaginateTypeDef = TypedDict(
    "ListNotificationsInputPaginateTypeDef",
    {
        "domainIdentifier": str,
        "type": NotificationTypeType,
        "afterTimestamp": NotRequired[TimestampTypeDef],
        "beforeTimestamp": NotRequired[TimestampTypeDef],
        "subjects": NotRequired[Sequence[str]],
        "taskStatus": NotRequired[TaskStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListPolicyGrantsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    entityType: TargetEntityTypeType
    entityIdentifier: str
    policyType: ManagedPolicyTypeType
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectMembershipsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    projectIdentifier: str
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectProfilesInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    name: NotRequired[str]
    sortBy: NotRequired[Literal["NAME"]]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    userIdentifier: NotRequired[str]
    groupIdentifier: NotRequired[str]
    name: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListRulesInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    targetType: Literal["DOMAIN_UNIT"]
    targetIdentifier: str
    ruleType: NotRequired[RuleTypeType]
    action: NotRequired[RuleActionType]
    projectIds: NotRequired[Sequence[str]]
    assetTypes: NotRequired[Sequence[str]]
    dataProduct: NotRequired[bool]
    includeCascaded: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSubscriptionGrantsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    environmentId: NotRequired[str]
    subscriptionTargetId: NotRequired[str]
    subscribedListingId: NotRequired[str]
    subscriptionId: NotRequired[str]
    owningProjectId: NotRequired[str]
    owningIamPrincipalArn: NotRequired[str]
    owningUserId: NotRequired[str]
    owningGroupId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSubscriptionRequestsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    status: NotRequired[SubscriptionRequestStatusType]
    subscribedListingId: NotRequired[str]
    owningProjectId: NotRequired[str]
    owningIamPrincipalArn: NotRequired[str]
    approverProjectId: NotRequired[str]
    owningUserId: NotRequired[str]
    owningGroupId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSubscriptionTargetsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListSubscriptionsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    subscriptionRequestIdentifier: NotRequired[str]
    status: NotRequired[SubscriptionStatusType]
    subscribedListingId: NotRequired[str]
    owningProjectId: NotRequired[str]
    owningIamPrincipalArn: NotRequired[str]
    owningUserId: NotRequired[str]
    owningGroupId: NotRequired[str]
    approverProjectId: NotRequired[str]
    sortBy: NotRequired[SortKeyType]
    sortOrder: NotRequired[SortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTimeSeriesDataPointsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    formName: str
    startedAt: NotRequired[TimestampTypeDef]
    endedAt: NotRequired[TimestampTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchGroupProfilesInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    groupType: GroupSearchTypeType
    searchText: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchUserProfilesInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    userType: UserSearchTypeType
    searchText: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListProjectProfilesOutputTypeDef(TypedDict):
    items: list[ProjectProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class TextMatchItemTypeDef(TypedDict):
    attribute: NotRequired[str]
    text: NotRequired[str]
    matchOffsets: NotRequired[list[MatchOffsetTypeDef]]


class MemberDetailsTypeDef(TypedDict):
    user: NotRequired[UserDetailsTypeDef]
    group: NotRequired[GroupDetailsTypeDef]


class MetadataFormEnforcementDetailOutputTypeDef(TypedDict):
    requiredMetadataForms: NotRequired[list[MetadataFormReferenceTypeDef]]


class MetadataFormEnforcementDetailTypeDef(TypedDict):
    requiredMetadataForms: NotRequired[Sequence[MetadataFormReferenceTypeDef]]


class OpenLineageRunEventSummaryTypeDef(TypedDict):
    eventType: NotRequired[OpenLineageRunStateType]
    runId: NotRequired[str]
    job: NotRequired[NameIdentifierTypeDef]
    inputs: NotRequired[list[NameIdentifierTypeDef]]
    outputs: NotRequired[list[NameIdentifierTypeDef]]


RowFilterExpressionOutputTypeDef = TypedDict(
    "RowFilterExpressionOutputTypeDef",
    {
        "equalTo": NotRequired[EqualToExpressionTypeDef],
        "notEqualTo": NotRequired[NotEqualToExpressionTypeDef],
        "greaterThan": NotRequired[GreaterThanExpressionTypeDef],
        "lessThan": NotRequired[LessThanExpressionTypeDef],
        "greaterThanOrEqualTo": NotRequired[GreaterThanOrEqualToExpressionTypeDef],
        "lessThanOrEqualTo": NotRequired[LessThanOrEqualToExpressionTypeDef],
        "isNull": NotRequired[IsNullExpressionTypeDef],
        "isNotNull": NotRequired[IsNotNullExpressionTypeDef],
        "in": NotRequired[InExpressionOutputTypeDef],
        "notIn": NotRequired[NotInExpressionOutputTypeDef],
        "like": NotRequired[LikeExpressionTypeDef],
        "notLike": NotRequired[NotLikeExpressionTypeDef],
    },
)
RowFilterExpressionTypeDef = TypedDict(
    "RowFilterExpressionTypeDef",
    {
        "equalTo": NotRequired[EqualToExpressionTypeDef],
        "notEqualTo": NotRequired[NotEqualToExpressionTypeDef],
        "greaterThan": NotRequired[GreaterThanExpressionTypeDef],
        "lessThan": NotRequired[LessThanExpressionTypeDef],
        "greaterThanOrEqualTo": NotRequired[GreaterThanOrEqualToExpressionTypeDef],
        "lessThanOrEqualTo": NotRequired[LessThanOrEqualToExpressionTypeDef],
        "isNull": NotRequired[IsNullExpressionTypeDef],
        "isNotNull": NotRequired[IsNotNullExpressionTypeDef],
        "in": NotRequired[InExpressionTypeDef],
        "notIn": NotRequired[NotInExpressionTypeDef],
        "like": NotRequired[LikeExpressionTypeDef],
        "notLike": NotRequired[NotLikeExpressionTypeDef],
    },
)


class TopicTypeDef(TypedDict):
    subject: str
    resource: NotificationResourceTypeDef
    role: NotificationRoleType


class OAuth2PropertiesOutputTypeDef(TypedDict):
    oAuth2GrantType: NotRequired[OAuth2GrantTypeType]
    oAuth2ClientApplication: NotRequired[OAuth2ClientApplicationTypeDef]
    tokenUrl: NotRequired[str]
    tokenUrlParametersMap: NotRequired[dict[str, str]]
    authorizationCodeProperties: NotRequired[AuthorizationCodePropertiesTypeDef]
    oAuth2Credentials: NotRequired[GlueOAuth2CredentialsTypeDef]


class OAuth2PropertiesTypeDef(TypedDict):
    oAuth2GrantType: NotRequired[OAuth2GrantTypeType]
    oAuth2ClientApplication: NotRequired[OAuth2ClientApplicationTypeDef]
    tokenUrl: NotRequired[str]
    tokenUrlParametersMap: NotRequired[Mapping[str, str]]
    authorizationCodeProperties: NotRequired[AuthorizationCodePropertiesTypeDef]
    oAuth2Credentials: NotRequired[GlueOAuth2CredentialsTypeDef]


class OwnerPropertiesOutputTypeDef(TypedDict):
    user: NotRequired[OwnerUserPropertiesOutputTypeDef]
    group: NotRequired[OwnerGroupPropertiesOutputTypeDef]


class OwnerPropertiesTypeDef(TypedDict):
    user: NotRequired[OwnerUserPropertiesTypeDef]
    group: NotRequired[OwnerGroupPropertiesTypeDef]


class SubscribedAssetListingTypeDef(TypedDict):
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    entityType: NotRequired[str]
    forms: NotRequired[str]
    glossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]
    assetScope: NotRequired[AssetScopeTypeDef]
    permissions: NotRequired[PermissionsOutputTypeDef]


class SubscribedAssetTypeDef(TypedDict):
    assetId: str
    assetRevision: str
    status: SubscriptionGrantStatusType
    targetName: NotRequired[str]
    failureCause: NotRequired[FailureCauseTypeDef]
    grantedTimestamp: NotRequired[datetime]
    failureTimestamp: NotRequired[datetime]
    assetScope: NotRequired[AssetScopeTypeDef]
    permissions: NotRequired[PermissionsOutputTypeDef]


PermissionsUnionTypeDef = Union[PermissionsTypeDef, PermissionsOutputTypeDef]
PhysicalConnectionRequirementsUnionTypeDef = Union[
    PhysicalConnectionRequirementsTypeDef, PhysicalConnectionRequirementsOutputTypeDef
]


class PolicyGrantDetailOutputTypeDef(TypedDict):
    createDomainUnit: NotRequired[CreateDomainUnitPolicyGrantDetailTypeDef]
    overrideDomainUnitOwners: NotRequired[OverrideDomainUnitOwnersPolicyGrantDetailTypeDef]
    addToProjectMemberPool: NotRequired[AddToProjectMemberPoolPolicyGrantDetailTypeDef]
    overrideProjectOwners: NotRequired[OverrideProjectOwnersPolicyGrantDetailTypeDef]
    createGlossary: NotRequired[CreateGlossaryPolicyGrantDetailTypeDef]
    createFormType: NotRequired[CreateFormTypePolicyGrantDetailTypeDef]
    createAssetType: NotRequired[CreateAssetTypePolicyGrantDetailTypeDef]
    createProject: NotRequired[CreateProjectPolicyGrantDetailTypeDef]
    createEnvironmentProfile: NotRequired[CreateEnvironmentProfilePolicyGrantDetailTypeDef]
    delegateCreateEnvironmentProfile: NotRequired[dict[str, Any]]
    createEnvironment: NotRequired[dict[str, Any]]
    createEnvironmentFromBlueprint: NotRequired[dict[str, Any]]
    createProjectFromProjectProfile: NotRequired[
        CreateProjectFromProjectProfilePolicyGrantDetailOutputTypeDef
    ]
    useAssetType: NotRequired[UseAssetTypePolicyGrantDetailTypeDef]


class PolicyGrantDetailTypeDef(TypedDict):
    createDomainUnit: NotRequired[CreateDomainUnitPolicyGrantDetailTypeDef]
    overrideDomainUnitOwners: NotRequired[OverrideDomainUnitOwnersPolicyGrantDetailTypeDef]
    addToProjectMemberPool: NotRequired[AddToProjectMemberPoolPolicyGrantDetailTypeDef]
    overrideProjectOwners: NotRequired[OverrideProjectOwnersPolicyGrantDetailTypeDef]
    createGlossary: NotRequired[CreateGlossaryPolicyGrantDetailTypeDef]
    createFormType: NotRequired[CreateFormTypePolicyGrantDetailTypeDef]
    createAssetType: NotRequired[CreateAssetTypePolicyGrantDetailTypeDef]
    createProject: NotRequired[CreateProjectPolicyGrantDetailTypeDef]
    createEnvironmentProfile: NotRequired[CreateEnvironmentProfilePolicyGrantDetailTypeDef]
    delegateCreateEnvironmentProfile: NotRequired[Mapping[str, Any]]
    createEnvironment: NotRequired[Mapping[str, Any]]
    createEnvironmentFromBlueprint: NotRequired[Mapping[str, Any]]
    createProjectFromProjectProfile: NotRequired[
        CreateProjectFromProjectProfilePolicyGrantDetailTypeDef
    ]
    useAssetType: NotRequired[UseAssetTypePolicyGrantDetailTypeDef]


class RuleScopeOutputTypeDef(TypedDict):
    assetType: NotRequired[AssetTypesForRuleOutputTypeDef]
    dataProduct: NotRequired[bool]
    project: NotRequired[ProjectsForRuleOutputTypeDef]


class RuleScopeTypeDef(TypedDict):
    assetType: NotRequired[AssetTypesForRuleTypeDef]
    dataProduct: NotRequired[bool]
    project: NotRequired[ProjectsForRuleTypeDef]


class RedshiftCredentialsTypeDef(TypedDict):
    secretArn: NotRequired[str]
    usernamePassword: NotRequired[UsernamePasswordTypeDef]


class SparkEmrPropertiesOutputTypeDef(TypedDict):
    computeArn: NotRequired[str]
    credentials: NotRequired[UsernamePasswordTypeDef]
    credentialsExpiration: NotRequired[datetime]
    governanceType: NotRequired[GovernanceTypeType]
    instanceProfileArn: NotRequired[str]
    javaVirtualEnv: NotRequired[str]
    livyEndpoint: NotRequired[str]
    logUri: NotRequired[str]
    pythonVirtualEnv: NotRequired[str]
    runtimeRole: NotRequired[str]
    trustedCertificatesS3Uri: NotRequired[str]
    certificateData: NotRequired[str]
    managedEndpointArn: NotRequired[str]
    managedEndpointCredentials: NotRequired[ManagedEndpointCredentialsTypeDef]


class RedshiftStorageTypeDef(TypedDict):
    redshiftClusterSource: NotRequired[RedshiftClusterStorageTypeDef]
    redshiftServerlessSource: NotRequired[RedshiftServerlessStorageTypeDef]


class RejectPredictionsInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    revision: NotRequired[str]
    rejectRule: NotRequired[RejectRuleTypeDef]
    rejectChoices: NotRequired[Sequence[RejectChoiceTypeDef]]
    clientToken: NotRequired[str]


class SparkGluePropertiesInputTypeDef(TypedDict):
    additionalArgs: NotRequired[SparkGlueArgsTypeDef]
    glueConnectionName: NotRequired[str]
    glueVersion: NotRequired[str]
    idleTimeout: NotRequired[int]
    javaVirtualEnv: NotRequired[str]
    numberOfWorkers: NotRequired[int]
    pythonVirtualEnv: NotRequired[str]
    workerType: NotRequired[str]


class SparkGluePropertiesOutputTypeDef(TypedDict):
    additionalArgs: NotRequired[SparkGlueArgsTypeDef]
    glueConnectionName: NotRequired[str]
    glueVersion: NotRequired[str]
    idleTimeout: NotRequired[int]
    javaVirtualEnv: NotRequired[str]
    numberOfWorkers: NotRequired[int]
    pythonVirtualEnv: NotRequired[str]
    workerType: NotRequired[str]


class UserProfileDetailsTypeDef(TypedDict):
    iam: NotRequired[IamUserProfileDetailsTypeDef]
    sso: NotRequired[SsoUserProfileDetailsTypeDef]


class SubscribedPrincipalInputTypeDef(TypedDict):
    project: NotRequired[SubscribedProjectInputTypeDef]
    user: NotRequired[SubscribedUserInputTypeDef]
    group: NotRequired[SubscribedGroupInputTypeDef]
    iam: NotRequired[SubscribedIamPrincipalInputTypeDef]


TermRelationsUnionTypeDef = Union[TermRelationsTypeDef, TermRelationsOutputTypeDef]


class BatchGetAttributesMetadataOutputTypeDef(TypedDict):
    attributes: list[BatchGetAttributeOutputTypeDef]
    errors: list[AttributeErrorTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


CreateAccountPoolOutputTypeDef = TypedDict(
    "CreateAccountPoolOutputTypeDef",
    {
        "domainId": str,
        "name": str,
        "id": str,
        "description": str,
        "resolutionStrategy": Literal["MANUAL"],
        "accountSource": AccountSourceOutputTypeDef,
        "createdBy": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "updatedBy": str,
        "domainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAccountPoolOutputTypeDef = TypedDict(
    "GetAccountPoolOutputTypeDef",
    {
        "domainId": str,
        "name": str,
        "id": str,
        "description": str,
        "resolutionStrategy": Literal["MANUAL"],
        "accountSource": AccountSourceOutputTypeDef,
        "createdBy": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "updatedBy": str,
        "domainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAccountPoolOutputTypeDef = TypedDict(
    "UpdateAccountPoolOutputTypeDef",
    {
        "domainId": str,
        "name": str,
        "id": str,
        "description": str,
        "resolutionStrategy": Literal["MANUAL"],
        "accountSource": AccountSourceOutputTypeDef,
        "createdBy": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "updatedBy": str,
        "domainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AccountSourceUnionTypeDef = Union[AccountSourceTypeDef, AccountSourceOutputTypeDef]


class CreateEnvironmentActionInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    name: str
    parameters: ActionParametersTypeDef
    description: NotRequired[str]


CreateEnvironmentActionOutputTypeDef = TypedDict(
    "CreateEnvironmentActionOutputTypeDef",
    {
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentActionSummaryTypeDef = TypedDict(
    "EnvironmentActionSummaryTypeDef",
    {
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "description": NotRequired[str],
    },
)
GetEnvironmentActionOutputTypeDef = TypedDict(
    "GetEnvironmentActionOutputTypeDef",
    {
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdateEnvironmentActionInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    identifier: str
    parameters: NotRequired[ActionParametersTypeDef]
    name: NotRequired[str]
    description: NotRequired[str]


UpdateEnvironmentActionOutputTypeDef = TypedDict(
    "UpdateEnvironmentActionOutputTypeDef",
    {
        "domainId": str,
        "environmentId": str,
        "id": str,
        "name": str,
        "parameters": ActionParametersTypeDef,
        "description": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class DataProductListingTypeDef(TypedDict):
    dataProductId: NotRequired[str]
    dataProductRevision: NotRequired[str]
    createdAt: NotRequired[datetime]
    forms: NotRequired[str]
    glossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]
    owningProjectId: NotRequired[str]
    items: NotRequired[list[ListingSummaryTypeDef]]


class BatchPutAttributesMetadataInputTypeDef(TypedDict):
    domainIdentifier: str
    entityType: AttributeEntityTypeType
    entityIdentifier: str
    attributes: Sequence[AttributeInputTypeDef]
    clientToken: NotRequired[str]


class GlueConnectionPatchTypeDef(TypedDict):
    description: NotRequired[str]
    connectionProperties: NotRequired[Mapping[str, str]]
    authenticationConfiguration: NotRequired[AuthenticationConfigurationPatchTypeDef]


class CreateAssetInputTypeDef(TypedDict):
    name: str
    domainIdentifier: str
    typeIdentifier: str
    owningProjectIdentifier: str
    externalIdentifier: NotRequired[str]
    typeRevision: NotRequired[str]
    description: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    predictionConfiguration: NotRequired[PredictionConfigurationTypeDef]
    clientToken: NotRequired[str]


CreateAssetOutputTypeDef = TypedDict(
    "CreateAssetOutputTypeDef",
    {
        "id": str,
        "name": str,
        "typeIdentifier": str,
        "typeRevision": str,
        "externalIdentifier": str,
        "revision": str,
        "description": str,
        "createdAt": datetime,
        "createdBy": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "glossaryTerms": list[str],
        "governedGlossaryTerms": list[str],
        "owningProjectId": str,
        "domainId": str,
        "listing": AssetListingDetailsTypeDef,
        "formsOutput": list[FormOutputTypeDef],
        "readOnlyFormsOutput": list[FormOutputTypeDef],
        "latestTimeSeriesDataPointFormsOutput": list[TimeSeriesDataPointSummaryFormOutputTypeDef],
        "predictionConfiguration": PredictionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateAssetRevisionInputTypeDef(TypedDict):
    name: str
    domainIdentifier: str
    identifier: str
    typeRevision: NotRequired[str]
    description: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    predictionConfiguration: NotRequired[PredictionConfigurationTypeDef]
    clientToken: NotRequired[str]


CreateAssetRevisionOutputTypeDef = TypedDict(
    "CreateAssetRevisionOutputTypeDef",
    {
        "id": str,
        "name": str,
        "typeIdentifier": str,
        "typeRevision": str,
        "externalIdentifier": str,
        "revision": str,
        "description": str,
        "createdAt": datetime,
        "createdBy": str,
        "firstRevisionCreatedAt": datetime,
        "firstRevisionCreatedBy": str,
        "glossaryTerms": list[str],
        "governedGlossaryTerms": list[str],
        "owningProjectId": str,
        "domainId": str,
        "listing": AssetListingDetailsTypeDef,
        "formsOutput": list[FormOutputTypeDef],
        "readOnlyFormsOutput": list[FormOutputTypeDef],
        "latestTimeSeriesDataPointFormsOutput": list[TimeSeriesDataPointSummaryFormOutputTypeDef],
        "predictionConfiguration": PredictionConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CreateEnvironmentBlueprintInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    provisioningProperties: ProvisioningPropertiesTypeDef
    description: NotRequired[str]
    userParameters: NotRequired[Sequence[CustomParameterTypeDef]]


CreateEnvironmentBlueprintOutputTypeDef = TypedDict(
    "CreateEnvironmentBlueprintOutputTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "provider": str,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "userParameters": list[CustomParameterTypeDef],
        "glossaryTerms": list[str],
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentBlueprintSummaryTypeDef = TypedDict(
    "EnvironmentBlueprintSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "provider": str,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "description": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
    },
)
GetEnvironmentBlueprintOutputTypeDef = TypedDict(
    "GetEnvironmentBlueprintOutputTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "provider": str,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "userParameters": list[CustomParameterTypeDef],
        "glossaryTerms": list[str],
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdateEnvironmentBlueprintInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    provisioningProperties: NotRequired[ProvisioningPropertiesTypeDef]
    userParameters: NotRequired[Sequence[CustomParameterTypeDef]]


UpdateEnvironmentBlueprintOutputTypeDef = TypedDict(
    "UpdateEnvironmentBlueprintOutputTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "provider": str,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "userParameters": list[CustomParameterTypeDef],
        "glossaryTerms": list[str],
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ListDataSourcesOutputTypeDef(TypedDict):
    items: list[DataSourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListProjectsOutputTypeDef(TypedDict):
    items: list[ProjectSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSubscriptionTargetsOutputTypeDef(TypedDict):
    items: list[SubscriptionTargetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateDataProductInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    owningProjectIdentifier: str
    description: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    items: NotRequired[Sequence[DataProductItemUnionTypeDef]]
    clientToken: NotRequired[str]


class CreateDataProductRevisionInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: str
    description: NotRequired[str]
    glossaryTerms: NotRequired[Sequence[str]]
    items: NotRequired[Sequence[DataProductItemUnionTypeDef]]
    formsInput: NotRequired[Sequence[FormInputTypeDef]]
    clientToken: NotRequired[str]


class ListDataSourceRunActivitiesOutputTypeDef(TypedDict):
    items: list[DataSourceRunActivityTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListDataSourceRunsOutputTypeDef(TypedDict):
    items: list[DataSourceRunSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


CreateEnvironmentOutputTypeDef = TypedDict(
    "CreateEnvironmentOutputTypeDef",
    {
        "projectId": str,
        "id": str,
        "domainId": str,
        "createdBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "name": str,
        "description": str,
        "environmentProfileId": str,
        "awsAccountId": str,
        "awsAccountRegion": str,
        "provider": str,
        "provisionedResources": list[ResourceTypeDef],
        "status": EnvironmentStatusType,
        "environmentActions": list[ConfigurableEnvironmentActionTypeDef],
        "glossaryTerms": list[str],
        "userParameters": list[CustomParameterTypeDef],
        "lastDeployment": DeploymentTypeDef,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "environmentBlueprintId": str,
        "environmentConfigurationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetEnvironmentOutputTypeDef = TypedDict(
    "GetEnvironmentOutputTypeDef",
    {
        "projectId": str,
        "id": str,
        "domainId": str,
        "createdBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "name": str,
        "description": str,
        "environmentProfileId": str,
        "awsAccountId": str,
        "awsAccountRegion": str,
        "provider": str,
        "provisionedResources": list[ResourceTypeDef],
        "status": EnvironmentStatusType,
        "environmentActions": list[ConfigurableEnvironmentActionTypeDef],
        "glossaryTerms": list[str],
        "userParameters": list[CustomParameterTypeDef],
        "lastDeployment": DeploymentTypeDef,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "environmentBlueprintId": str,
        "environmentConfigurationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateEnvironmentOutputTypeDef = TypedDict(
    "UpdateEnvironmentOutputTypeDef",
    {
        "projectId": str,
        "id": str,
        "domainId": str,
        "createdBy": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "name": str,
        "description": str,
        "environmentProfileId": str,
        "awsAccountId": str,
        "awsAccountRegion": str,
        "provider": str,
        "provisionedResources": list[ResourceTypeDef],
        "status": EnvironmentStatusType,
        "environmentActions": list[ConfigurableEnvironmentActionTypeDef],
        "glossaryTerms": list[str],
        "userParameters": list[CustomParameterTypeDef],
        "lastDeployment": DeploymentTypeDef,
        "provisioningProperties": ProvisioningPropertiesTypeDef,
        "deploymentProperties": DeploymentPropertiesTypeDef,
        "environmentBlueprintId": str,
        "environmentConfigurationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentDeploymentDetailsUnionTypeDef = Union[
    EnvironmentDeploymentDetailsTypeDef, EnvironmentDeploymentDetailsOutputTypeDef
]


class ProjectPolicyGrantPrincipalTypeDef(TypedDict):
    projectDesignation: ProjectDesignationType
    projectIdentifier: NotRequired[str]
    projectGrantFilter: NotRequired[ProjectGrantFilterTypeDef]


CreateDomainUnitOutputTypeDef = TypedDict(
    "CreateDomainUnitOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "name": str,
        "parentDomainUnitId": str,
        "description": str,
        "owners": list[DomainUnitOwnerPropertiesTypeDef],
        "ancestorDomainUnitIds": list[str],
        "createdAt": datetime,
        "createdBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDomainUnitOutputTypeDef = TypedDict(
    "GetDomainUnitOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "name": str,
        "parentDomainUnitId": str,
        "description": str,
        "owners": list[DomainUnitOwnerPropertiesTypeDef],
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "createdBy": str,
        "lastUpdatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDomainUnitOutputTypeDef = TypedDict(
    "UpdateDomainUnitOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "name": str,
        "owners": list[DomainUnitOwnerPropertiesTypeDef],
        "description": str,
        "parentDomainUnitId": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "createdBy": str,
        "lastUpdatedBy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentConfigurationOutputTypeDef = TypedDict(
    "EnvironmentConfigurationOutputTypeDef",
    {
        "name": str,
        "environmentBlueprintId": str,
        "id": NotRequired[str],
        "description": NotRequired[str],
        "deploymentMode": NotRequired[DeploymentModeType],
        "configurationParameters": NotRequired[
            EnvironmentConfigurationParametersDetailsOutputTypeDef
        ],
        "awsAccount": NotRequired[AwsAccountTypeDef],
        "accountPools": NotRequired[list[str]],
        "awsRegion": NotRequired[RegionTypeDef],
        "deploymentOrder": NotRequired[int],
    },
)
EnvironmentConfigurationParametersDetailsUnionTypeDef = Union[
    EnvironmentConfigurationParametersDetailsTypeDef,
    EnvironmentConfigurationParametersDetailsOutputTypeDef,
]
CreateProjectOutputTypeDef = TypedDict(
    "CreateProjectOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "description": str,
        "projectStatus": ProjectStatusType,
        "failureReasons": list[ProjectDeletionErrorTypeDef],
        "createdBy": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "resourceTags": list[ResourceTagTypeDef],
        "glossaryTerms": list[str],
        "domainUnitId": str,
        "projectProfileId": str,
        "userParameters": list[EnvironmentConfigurationUserParameterOutputTypeDef],
        "environmentDeploymentDetails": EnvironmentDeploymentDetailsOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetProjectOutputTypeDef = TypedDict(
    "GetProjectOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "description": str,
        "projectStatus": ProjectStatusType,
        "failureReasons": list[ProjectDeletionErrorTypeDef],
        "createdBy": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "resourceTags": list[ResourceTagTypeDef],
        "glossaryTerms": list[str],
        "domainUnitId": str,
        "projectProfileId": str,
        "userParameters": list[EnvironmentConfigurationUserParameterOutputTypeDef],
        "environmentDeploymentDetails": EnvironmentDeploymentDetailsOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateProjectOutputTypeDef = TypedDict(
    "UpdateProjectOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "description": str,
        "projectStatus": ProjectStatusType,
        "failureReasons": list[ProjectDeletionErrorTypeDef],
        "createdBy": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "resourceTags": list[ResourceTagTypeDef],
        "glossaryTerms": list[str],
        "domainUnitId": str,
        "projectProfileId": str,
        "userParameters": list[EnvironmentConfigurationUserParameterOutputTypeDef],
        "environmentDeploymentDetails": EnvironmentDeploymentDetailsOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentConfigurationUserParameterUnionTypeDef = Union[
    EnvironmentConfigurationUserParameterTypeDef, EnvironmentConfigurationUserParameterOutputTypeDef
]


class SearchInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    searchScope: InventorySearchScopeType
    owningProjectIdentifier: NotRequired[str]
    searchText: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    filters: NotRequired[FilterClausePaginatorTypeDef]
    sort: NotRequired[SearchSortTypeDef]
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchListingsInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    searchText: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    filters: NotRequired[FilterClausePaginatorTypeDef]
    aggregations: NotRequired[Sequence[AggregationListItemTypeDef]]
    sort: NotRequired[SearchSortTypeDef]
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchTypesInputPaginateTypeDef(TypedDict):
    domainIdentifier: str
    searchScope: TypesSearchScopeType
    managed: bool
    searchText: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    filters: NotRequired[FilterClausePaginatorTypeDef]
    sort: NotRequired[SearchSortTypeDef]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class SearchInputTypeDef(TypedDict):
    domainIdentifier: str
    searchScope: InventorySearchScopeType
    owningProjectIdentifier: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchText: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    filters: NotRequired[FilterClauseTypeDef]
    sort: NotRequired[SearchSortTypeDef]
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]


class SearchListingsInputTypeDef(TypedDict):
    domainIdentifier: str
    searchText: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filters: NotRequired[FilterClauseTypeDef]
    aggregations: NotRequired[Sequence[AggregationListItemTypeDef]]
    sort: NotRequired[SearchSortTypeDef]
    additionalAttributes: NotRequired[Sequence[SearchOutputAdditionalAttributeType]]


class SearchTypesInputTypeDef(TypedDict):
    domainIdentifier: str
    searchScope: TypesSearchScopeType
    managed: bool
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    searchText: NotRequired[str]
    searchIn: NotRequired[Sequence[SearchInItemTypeDef]]
    filters: NotRequired[FilterClauseTypeDef]
    sort: NotRequired[SearchSortTypeDef]


class GlueRunConfigurationOutputTypeDef(TypedDict):
    relationalFilterConfigurations: list[RelationalFilterConfigurationOutputTypeDef]
    accountId: NotRequired[str]
    region: NotRequired[str]
    dataAccessRole: NotRequired[str]
    autoImportDataQualityResult: NotRequired[bool]
    catalogName: NotRequired[str]


RelationalFilterConfigurationUnionTypeDef = Union[
    RelationalFilterConfigurationTypeDef, RelationalFilterConfigurationOutputTypeDef
]


class SearchTypesResultItemTypeDef(TypedDict):
    assetTypeItem: NotRequired[AssetTypeItemTypeDef]
    formTypeItem: NotRequired[FormTypeDataTypeDef]
    lineageNodeTypeItem: NotRequired[LineageNodeTypeItemTypeDef]


class ListJobRunsOutputTypeDef(TypedDict):
    items: list[JobRunSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PostTimeSeriesDataPointsInputTypeDef(TypedDict):
    domainIdentifier: str
    entityIdentifier: str
    entityType: TimeSeriesEntityTypeType
    forms: Sequence[TimeSeriesDataPointFormInputTypeDef]
    clientToken: NotRequired[str]


class ListMetadataGenerationRunsOutputTypeDef(TypedDict):
    items: list[MetadataGenerationRunItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SelfGrantStatusOutputTypeDef(TypedDict):
    glueSelfGrantStatus: NotRequired[GlueSelfGrantStatusOutputTypeDef]
    redshiftSelfGrantStatus: NotRequired[RedshiftSelfGrantStatusOutputTypeDef]


class CreateSubscriptionGrantInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentIdentifier: str
    grantedEntity: GrantedEntityInputTypeDef
    subscriptionTargetIdentifier: NotRequired[str]
    assetTargetNames: NotRequired[Sequence[AssetTargetNameMapTypeDef]]
    clientToken: NotRequired[str]


class EnvironmentBlueprintConfigurationItemTypeDef(TypedDict):
    domainId: str
    environmentBlueprintId: str
    provisioningRoleArn: NotRequired[str]
    environmentRolePermissionBoundary: NotRequired[str]
    manageAccessRoleArn: NotRequired[str]
    enabledRegions: NotRequired[list[str]]
    regionalParameters: NotRequired[dict[str, dict[str, str]]]
    createdAt: NotRequired[datetime]
    updatedAt: NotRequired[datetime]
    provisioningConfigurations: NotRequired[list[ProvisioningConfigurationOutputTypeDef]]


class GetEnvironmentBlueprintConfigurationOutputTypeDef(TypedDict):
    domainId: str
    environmentBlueprintId: str
    provisioningRoleArn: str
    environmentRolePermissionBoundary: str
    manageAccessRoleArn: str
    enabledRegions: list[str]
    regionalParameters: dict[str, dict[str, str]]
    createdAt: datetime
    updatedAt: datetime
    provisioningConfigurations: list[ProvisioningConfigurationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PutEnvironmentBlueprintConfigurationOutputTypeDef(TypedDict):
    domainId: str
    environmentBlueprintId: str
    provisioningRoleArn: str
    environmentRolePermissionBoundary: str
    manageAccessRoleArn: str
    enabledRegions: list[str]
    regionalParameters: dict[str, dict[str, str]]
    createdAt: datetime
    updatedAt: datetime
    provisioningConfigurations: list[ProvisioningConfigurationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ProvisioningConfigurationTypeDef(TypedDict):
    lakeFormationConfiguration: NotRequired[LakeFormationConfigurationUnionTypeDef]


class JobRunDetailsTypeDef(TypedDict):
    lineageRunDetails: NotRequired[LineageRunDetailsTypeDef]


class MatchRationaleItemTypeDef(TypedDict):
    textMatches: NotRequired[list[TextMatchItemTypeDef]]


class ProjectMemberTypeDef(TypedDict):
    memberDetails: MemberDetailsTypeDef
    designation: UserDesignationType


class RuleDetailOutputTypeDef(TypedDict):
    metadataFormEnforcementDetail: NotRequired[MetadataFormEnforcementDetailOutputTypeDef]
    glossaryTermEnforcementDetail: NotRequired[GlossaryTermEnforcementDetailOutputTypeDef]


class RuleDetailTypeDef(TypedDict):
    metadataFormEnforcementDetail: NotRequired[MetadataFormEnforcementDetailTypeDef]
    glossaryTermEnforcementDetail: NotRequired[GlossaryTermEnforcementDetailTypeDef]


class EventSummaryTypeDef(TypedDict):
    openLineageRunEventSummary: NotRequired[OpenLineageRunEventSummaryTypeDef]


RowFilterOutputTypeDef = TypedDict(
    "RowFilterOutputTypeDef",
    {
        "expression": NotRequired[RowFilterExpressionOutputTypeDef],
        "and": NotRequired[list[dict[str, Any]]],
        "or": NotRequired[list[dict[str, Any]]],
    },
)
RowFilterTypeDef = TypedDict(
    "RowFilterTypeDef",
    {
        "expression": NotRequired[RowFilterExpressionTypeDef],
        "and": NotRequired[Sequence[Mapping[str, Any]]],
        "or": NotRequired[Sequence[Mapping[str, Any]]],
    },
)
NotificationOutputTypeDef = TypedDict(
    "NotificationOutputTypeDef",
    {
        "identifier": str,
        "domainIdentifier": str,
        "type": NotificationTypeType,
        "topic": TopicTypeDef,
        "title": str,
        "message": str,
        "actionLink": str,
        "creationTimestamp": datetime,
        "lastUpdatedTimestamp": datetime,
        "status": NotRequired[TaskStatusType],
        "metadata": NotRequired[dict[str, str]],
    },
)


class AuthenticationConfigurationTypeDef(TypedDict):
    authenticationType: NotRequired[AuthenticationTypeType]
    secretArn: NotRequired[str]
    oAuth2Properties: NotRequired[OAuth2PropertiesOutputTypeDef]


OAuth2PropertiesUnionTypeDef = Union[OAuth2PropertiesTypeDef, OAuth2PropertiesOutputTypeDef]


class ListEntityOwnersOutputTypeDef(TypedDict):
    owners: list[OwnerPropertiesOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AddEntityOwnerInputTypeDef(TypedDict):
    domainIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    entityIdentifier: str
    owner: OwnerPropertiesTypeDef
    clientToken: NotRequired[str]


class RemoveEntityOwnerInputTypeDef(TypedDict):
    domainIdentifier: str
    entityType: Literal["DOMAIN_UNIT"]
    entityIdentifier: str
    owner: OwnerPropertiesTypeDef
    clientToken: NotRequired[str]


class SubscribedListingItemTypeDef(TypedDict):
    assetListing: NotRequired[SubscribedAssetListingTypeDef]
    productListing: NotRequired[SubscribedProductListingTypeDef]


CreateSubscriptionGrantOutputTypeDef = TypedDict(
    "CreateSubscriptionGrantOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "environmentId": str,
        "subscriptionTargetId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "status": SubscriptionGrantOverallStatusType,
        "assets": list[SubscribedAssetTypeDef],
        "subscriptionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteSubscriptionGrantOutputTypeDef = TypedDict(
    "DeleteSubscriptionGrantOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "environmentId": str,
        "subscriptionTargetId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "status": SubscriptionGrantOverallStatusType,
        "assets": list[SubscribedAssetTypeDef],
        "subscriptionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionGrantOutputTypeDef = TypedDict(
    "GetSubscriptionGrantOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "environmentId": str,
        "subscriptionTargetId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "status": SubscriptionGrantOverallStatusType,
        "assets": list[SubscribedAssetTypeDef],
        "subscriptionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscriptionGrantSummaryTypeDef = TypedDict(
    "SubscriptionGrantSummaryTypeDef",
    {
        "id": str,
        "createdBy": str,
        "domainId": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "subscriptionTargetId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "status": SubscriptionGrantOverallStatusType,
        "updatedBy": NotRequired[str],
        "environmentId": NotRequired[str],
        "assets": NotRequired[list[SubscribedAssetTypeDef]],
        "subscriptionId": NotRequired[str],
    },
)
UpdateSubscriptionGrantStatusOutputTypeDef = TypedDict(
    "UpdateSubscriptionGrantStatusOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "environmentId": str,
        "subscriptionTargetId": str,
        "grantedEntity": GrantedEntityTypeDef,
        "status": SubscriptionGrantOverallStatusType,
        "assets": list[SubscribedAssetTypeDef],
        "subscriptionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class AssetPermissionTypeDef(TypedDict):
    assetId: str
    permissions: PermissionsUnionTypeDef


PolicyGrantDetailUnionTypeDef = Union[PolicyGrantDetailTypeDef, PolicyGrantDetailOutputTypeDef]


class RuleSummaryTypeDef(TypedDict):
    identifier: NotRequired[str]
    revision: NotRequired[str]
    ruleType: NotRequired[RuleTypeType]
    name: NotRequired[str]
    targetType: NotRequired[Literal["DOMAIN_UNIT"]]
    target: NotRequired[RuleTargetTypeDef]
    action: NotRequired[RuleActionType]
    scope: NotRequired[RuleScopeOutputTypeDef]
    updatedAt: NotRequired[datetime]
    lastUpdatedBy: NotRequired[str]


RuleScopeUnionTypeDef = Union[RuleScopeTypeDef, RuleScopeOutputTypeDef]


class RedshiftPropertiesInputTypeDef(TypedDict):
    storage: NotRequired[RedshiftStoragePropertiesTypeDef]
    databaseName: NotRequired[str]
    host: NotRequired[str]
    port: NotRequired[int]
    credentials: NotRequired[RedshiftCredentialsTypeDef]
    lineageSync: NotRequired[RedshiftLineageSyncConfigurationInputTypeDef]


class RedshiftPropertiesOutputTypeDef(TypedDict):
    storage: NotRequired[RedshiftStoragePropertiesTypeDef]
    credentials: NotRequired[RedshiftCredentialsTypeDef]
    isProvisionedSecret: NotRequired[bool]
    jdbcIamUrl: NotRequired[str]
    jdbcUrl: NotRequired[str]
    redshiftTempDir: NotRequired[str]
    lineageSync: NotRequired[RedshiftLineageSyncConfigurationOutputTypeDef]
    status: NotRequired[ConnectionStatusType]
    databaseName: NotRequired[str]


class RedshiftPropertiesPatchTypeDef(TypedDict):
    storage: NotRequired[RedshiftStoragePropertiesTypeDef]
    databaseName: NotRequired[str]
    host: NotRequired[str]
    port: NotRequired[int]
    credentials: NotRequired[RedshiftCredentialsTypeDef]
    lineageSync: NotRequired[RedshiftLineageSyncConfigurationInputTypeDef]


class RedshiftRunConfigurationOutputTypeDef(TypedDict):
    relationalFilterConfigurations: list[RelationalFilterConfigurationOutputTypeDef]
    redshiftStorage: RedshiftStorageTypeDef
    accountId: NotRequired[str]
    region: NotRequired[str]
    dataAccessRole: NotRequired[str]
    redshiftCredentialConfiguration: NotRequired[RedshiftCredentialConfigurationTypeDef]


CreateUserProfileOutputTypeDef = TypedDict(
    "CreateUserProfileOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "type": UserProfileTypeType,
        "status": UserProfileStatusType,
        "details": UserProfileDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetUserProfileOutputTypeDef = TypedDict(
    "GetUserProfileOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "type": UserProfileTypeType,
        "status": UserProfileStatusType,
        "details": UserProfileDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscribedUserTypeDef = TypedDict(
    "SubscribedUserTypeDef",
    {
        "id": NotRequired[str],
        "details": NotRequired[UserProfileDetailsTypeDef],
    },
)
UpdateUserProfileOutputTypeDef = TypedDict(
    "UpdateUserProfileOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "type": UserProfileTypeType,
        "status": UserProfileStatusType,
        "details": UserProfileDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UserProfileSummaryTypeDef = TypedDict(
    "UserProfileSummaryTypeDef",
    {
        "domainId": NotRequired[str],
        "id": NotRequired[str],
        "type": NotRequired[UserProfileTypeType],
        "status": NotRequired[UserProfileStatusType],
        "details": NotRequired[UserProfileDetailsTypeDef],
    },
)


class CreateGlossaryTermInputTypeDef(TypedDict):
    domainIdentifier: str
    glossaryIdentifier: str
    name: str
    status: NotRequired[GlossaryTermStatusType]
    shortDescription: NotRequired[str]
    longDescription: NotRequired[str]
    termRelations: NotRequired[TermRelationsUnionTypeDef]
    clientToken: NotRequired[str]


class UpdateGlossaryTermInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    glossaryIdentifier: NotRequired[str]
    name: NotRequired[str]
    shortDescription: NotRequired[str]
    longDescription: NotRequired[str]
    termRelations: NotRequired[TermRelationsUnionTypeDef]
    status: NotRequired[GlossaryTermStatusType]


class CreateAccountPoolInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    resolutionStrategy: Literal["MANUAL"]
    accountSource: AccountSourceUnionTypeDef
    description: NotRequired[str]


class UpdateAccountPoolInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    resolutionStrategy: NotRequired[Literal["MANUAL"]]
    accountSource: NotRequired[AccountSourceUnionTypeDef]


class ListEnvironmentActionsOutputTypeDef(TypedDict):
    items: list[EnvironmentActionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListingItemTypeDef(TypedDict):
    assetListing: NotRequired[AssetListingTypeDef]
    dataProductListing: NotRequired[DataProductListingTypeDef]


class GluePropertiesPatchTypeDef(TypedDict):
    glueConnectionInput: NotRequired[GlueConnectionPatchTypeDef]


class ListEnvironmentBlueprintsOutputTypeDef(TypedDict):
    items: list[EnvironmentBlueprintSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class PolicyGrantPrincipalOutputTypeDef(TypedDict):
    user: NotRequired[UserPolicyGrantPrincipalOutputTypeDef]
    group: NotRequired[GroupPolicyGrantPrincipalTypeDef]
    project: NotRequired[ProjectPolicyGrantPrincipalTypeDef]
    domainUnit: NotRequired[DomainUnitPolicyGrantPrincipalOutputTypeDef]


class PolicyGrantPrincipalTypeDef(TypedDict):
    user: NotRequired[UserPolicyGrantPrincipalTypeDef]
    group: NotRequired[GroupPolicyGrantPrincipalTypeDef]
    project: NotRequired[ProjectPolicyGrantPrincipalTypeDef]
    domainUnit: NotRequired[DomainUnitPolicyGrantPrincipalTypeDef]


CreateProjectProfileOutputTypeDef = TypedDict(
    "CreateProjectProfileOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "description": str,
        "status": StatusType,
        "projectResourceTags": list[ResourceTagParameterTypeDef],
        "allowCustomProjectResourceTags": bool,
        "projectResourceTagsDescription": str,
        "environmentConfigurations": list[EnvironmentConfigurationOutputTypeDef],
        "createdBy": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "domainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetProjectProfileOutputTypeDef = TypedDict(
    "GetProjectProfileOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "description": str,
        "status": StatusType,
        "projectResourceTags": list[ResourceTagParameterTypeDef],
        "allowCustomProjectResourceTags": bool,
        "projectResourceTagsDescription": str,
        "environmentConfigurations": list[EnvironmentConfigurationOutputTypeDef],
        "createdBy": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "domainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateProjectProfileOutputTypeDef = TypedDict(
    "UpdateProjectProfileOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "description": str,
        "status": StatusType,
        "projectResourceTags": list[ResourceTagParameterTypeDef],
        "allowCustomProjectResourceTags": bool,
        "projectResourceTagsDescription": str,
        "environmentConfigurations": list[EnvironmentConfigurationOutputTypeDef],
        "createdBy": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "domainUnitId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
EnvironmentConfigurationTypeDef = TypedDict(
    "EnvironmentConfigurationTypeDef",
    {
        "name": str,
        "environmentBlueprintId": str,
        "id": NotRequired[str],
        "description": NotRequired[str],
        "deploymentMode": NotRequired[DeploymentModeType],
        "configurationParameters": NotRequired[
            EnvironmentConfigurationParametersDetailsUnionTypeDef
        ],
        "awsAccount": NotRequired[AwsAccountTypeDef],
        "accountPools": NotRequired[Sequence[str]],
        "awsRegion": NotRequired[RegionTypeDef],
        "deploymentOrder": NotRequired[int],
    },
)


class CreateProjectInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    description: NotRequired[str]
    resourceTags: NotRequired[Mapping[str, str]]
    glossaryTerms: NotRequired[Sequence[str]]
    domainUnitId: NotRequired[str]
    projectProfileId: NotRequired[str]
    userParameters: NotRequired[Sequence[EnvironmentConfigurationUserParameterUnionTypeDef]]


class UpdateProjectInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    resourceTags: NotRequired[Mapping[str, str]]
    glossaryTerms: NotRequired[Sequence[str]]
    domainUnitId: NotRequired[str]
    environmentDeploymentDetails: NotRequired[EnvironmentDeploymentDetailsUnionTypeDef]
    userParameters: NotRequired[Sequence[EnvironmentConfigurationUserParameterUnionTypeDef]]
    projectProfileVersion: NotRequired[str]


class GlueRunConfigurationInputTypeDef(TypedDict):
    relationalFilterConfigurations: Sequence[RelationalFilterConfigurationUnionTypeDef]
    dataAccessRole: NotRequired[str]
    autoImportDataQualityResult: NotRequired[bool]
    catalogName: NotRequired[str]


class RedshiftRunConfigurationInputTypeDef(TypedDict):
    relationalFilterConfigurations: Sequence[RelationalFilterConfigurationUnionTypeDef]
    dataAccessRole: NotRequired[str]
    redshiftCredentialConfiguration: NotRequired[RedshiftCredentialConfigurationTypeDef]
    redshiftStorage: NotRequired[RedshiftStorageTypeDef]


class SearchTypesOutputTypeDef(TypedDict):
    items: list[SearchTypesResultItemTypeDef]
    totalMatchCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListEnvironmentBlueprintConfigurationsOutputTypeDef(TypedDict):
    items: list[EnvironmentBlueprintConfigurationItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ProvisioningConfigurationUnionTypeDef = Union[
    ProvisioningConfigurationTypeDef, ProvisioningConfigurationOutputTypeDef
]
GetJobRunOutputTypeDef = TypedDict(
    "GetJobRunOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "jobId": str,
        "jobType": Literal["LINEAGE"],
        "runMode": JobRunModeType,
        "details": JobRunDetailsTypeDef,
        "status": JobRunStatusType,
        "error": JobRunErrorTypeDef,
        "createdBy": str,
        "createdAt": datetime,
        "startTime": datetime,
        "endTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class AssetItemAdditionalAttributesTypeDef(TypedDict):
    formsOutput: NotRequired[list[FormOutputTypeDef]]
    readOnlyFormsOutput: NotRequired[list[FormOutputTypeDef]]
    latestTimeSeriesDataPointFormsOutput: NotRequired[
        list[TimeSeriesDataPointSummaryFormOutputTypeDef]
    ]
    matchRationale: NotRequired[list[MatchRationaleItemTypeDef]]


class AssetListingItemAdditionalAttributesTypeDef(TypedDict):
    forms: NotRequired[str]
    matchRationale: NotRequired[list[MatchRationaleItemTypeDef]]
    latestTimeSeriesDataPointForms: NotRequired[list[TimeSeriesDataPointSummaryFormOutputTypeDef]]


class DataProductItemAdditionalAttributesTypeDef(TypedDict):
    matchRationale: NotRequired[list[MatchRationaleItemTypeDef]]


class DataProductListingItemAdditionalAttributesTypeDef(TypedDict):
    forms: NotRequired[str]
    matchRationale: NotRequired[list[MatchRationaleItemTypeDef]]


class GlossaryItemAdditionalAttributesTypeDef(TypedDict):
    matchRationale: NotRequired[list[MatchRationaleItemTypeDef]]


class GlossaryTermItemAdditionalAttributesTypeDef(TypedDict):
    matchRationale: NotRequired[list[MatchRationaleItemTypeDef]]


class ListProjectMembershipsOutputTypeDef(TypedDict):
    members: list[ProjectMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateRuleOutputTypeDef(TypedDict):
    identifier: str
    name: str
    ruleType: RuleTypeType
    target: RuleTargetTypeDef
    action: RuleActionType
    scope: RuleScopeOutputTypeDef
    detail: RuleDetailOutputTypeDef
    targetType: Literal["DOMAIN_UNIT"]
    description: str
    createdAt: datetime
    createdBy: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetRuleOutputTypeDef(TypedDict):
    identifier: str
    revision: str
    name: str
    ruleType: RuleTypeType
    target: RuleTargetTypeDef
    action: RuleActionType
    scope: RuleScopeOutputTypeDef
    detail: RuleDetailOutputTypeDef
    targetType: Literal["DOMAIN_UNIT"]
    description: str
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    lastUpdatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRuleOutputTypeDef(TypedDict):
    identifier: str
    revision: str
    name: str
    ruleType: RuleTypeType
    target: RuleTargetTypeDef
    action: RuleActionType
    scope: RuleScopeOutputTypeDef
    detail: RuleDetailOutputTypeDef
    description: str
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    lastUpdatedBy: str
    ResponseMetadata: ResponseMetadataTypeDef


RuleDetailUnionTypeDef = Union[RuleDetailTypeDef, RuleDetailOutputTypeDef]
LineageEventSummaryTypeDef = TypedDict(
    "LineageEventSummaryTypeDef",
    {
        "id": NotRequired[str],
        "domainId": NotRequired[str],
        "processingStatus": NotRequired[LineageEventProcessingStatusType],
        "eventTime": NotRequired[datetime],
        "eventSummary": NotRequired[EventSummaryTypeDef],
        "createdBy": NotRequired[str],
        "createdAt": NotRequired[datetime],
    },
)


class RowFilterConfigurationOutputTypeDef(TypedDict):
    rowFilter: RowFilterOutputTypeDef
    sensitive: NotRequired[bool]


class RowFilterConfigurationTypeDef(TypedDict):
    rowFilter: RowFilterTypeDef
    sensitive: NotRequired[bool]


class ListNotificationsOutputTypeDef(TypedDict):
    notifications: list[NotificationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class GlueConnectionTypeDef(TypedDict):
    name: NotRequired[str]
    description: NotRequired[str]
    connectionType: NotRequired[ConnectionTypeType]
    matchCriteria: NotRequired[list[str]]
    connectionProperties: NotRequired[dict[str, str]]
    sparkProperties: NotRequired[dict[str, str]]
    athenaProperties: NotRequired[dict[str, str]]
    pythonProperties: NotRequired[dict[str, str]]
    physicalConnectionRequirements: NotRequired[PhysicalConnectionRequirementsOutputTypeDef]
    creationTime: NotRequired[datetime]
    lastUpdatedTime: NotRequired[datetime]
    lastUpdatedBy: NotRequired[str]
    status: NotRequired[ConnectionStatusType]
    statusReason: NotRequired[str]
    lastConnectionValidationTime: NotRequired[datetime]
    authenticationConfiguration: NotRequired[AuthenticationConfigurationTypeDef]
    connectionSchemaVersion: NotRequired[int]
    compatibleComputeEnvironments: NotRequired[list[ComputeEnvironmentsType]]


class AuthenticationConfigurationInputTypeDef(TypedDict):
    authenticationType: NotRequired[AuthenticationTypeType]
    oAuth2Properties: NotRequired[OAuth2PropertiesUnionTypeDef]
    secretArn: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    basicAuthenticationCredentials: NotRequired[BasicAuthenticationCredentialsTypeDef]
    customAuthenticationCredentials: NotRequired[Mapping[str, str]]


SubscribedListingTypeDef = TypedDict(
    "SubscribedListingTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "item": SubscribedListingItemTypeDef,
        "ownerProjectId": str,
        "revision": NotRequired[str],
        "ownerProjectName": NotRequired[str],
    },
)


class ListSubscriptionGrantsOutputTypeDef(TypedDict):
    items: list[SubscriptionGrantSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AcceptSubscriptionRequestInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    decisionComment: NotRequired[str]
    assetScopes: NotRequired[Sequence[AcceptedAssetScopeTypeDef]]
    assetPermissions: NotRequired[Sequence[AssetPermissionTypeDef]]


class CreateSubscriptionRequestInputTypeDef(TypedDict):
    domainIdentifier: str
    subscribedPrincipals: Sequence[SubscribedPrincipalInputTypeDef]
    subscribedListings: Sequence[SubscribedListingInputTypeDef]
    requestReason: str
    clientToken: NotRequired[str]
    metadataForms: NotRequired[Sequence[FormInputTypeDef]]
    assetPermissions: NotRequired[Sequence[AssetPermissionTypeDef]]
    assetScopes: NotRequired[Sequence[AcceptedAssetScopeTypeDef]]


class ListRulesOutputTypeDef(TypedDict):
    items: list[RuleSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ConnectionPropertiesOutputTypeDef(TypedDict):
    athenaProperties: NotRequired[AthenaPropertiesOutputTypeDef]
    glueProperties: NotRequired[GluePropertiesOutputTypeDef]
    hyperPodProperties: NotRequired[HyperPodPropertiesOutputTypeDef]
    iamProperties: NotRequired[IamPropertiesOutputTypeDef]
    redshiftProperties: NotRequired[RedshiftPropertiesOutputTypeDef]
    sparkEmrProperties: NotRequired[SparkEmrPropertiesOutputTypeDef]
    sparkGlueProperties: NotRequired[SparkGluePropertiesOutputTypeDef]
    s3Properties: NotRequired[S3PropertiesOutputTypeDef]
    amazonQProperties: NotRequired[AmazonQPropertiesOutputTypeDef]
    mlflowProperties: NotRequired[MlflowPropertiesOutputTypeDef]


class DataSourceConfigurationOutputTypeDef(TypedDict):
    glueRunConfiguration: NotRequired[GlueRunConfigurationOutputTypeDef]
    redshiftRunConfiguration: NotRequired[RedshiftRunConfigurationOutputTypeDef]
    sageMakerRunConfiguration: NotRequired[SageMakerRunConfigurationOutputTypeDef]


class SubscribedPrincipalTypeDef(TypedDict):
    project: NotRequired[SubscribedProjectTypeDef]
    user: NotRequired[SubscribedUserTypeDef]
    group: NotRequired[SubscribedGroupTypeDef]
    iam: NotRequired[SubscribedIamPrincipalTypeDef]


class SearchUserProfilesOutputTypeDef(TypedDict):
    items: list[UserProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


GetListingOutputTypeDef = TypedDict(
    "GetListingOutputTypeDef",
    {
        "domainId": str,
        "id": str,
        "listingRevision": str,
        "createdAt": datetime,
        "updatedAt": datetime,
        "createdBy": str,
        "updatedBy": str,
        "item": ListingItemTypeDef,
        "name": str,
        "description": str,
        "status": ListingStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class ConnectionPropertiesPatchTypeDef(TypedDict):
    athenaProperties: NotRequired[AthenaPropertiesPatchTypeDef]
    glueProperties: NotRequired[GluePropertiesPatchTypeDef]
    iamProperties: NotRequired[IamPropertiesPatchTypeDef]
    redshiftProperties: NotRequired[RedshiftPropertiesPatchTypeDef]
    sparkEmrProperties: NotRequired[SparkEmrPropertiesPatchTypeDef]
    s3Properties: NotRequired[S3PropertiesPatchTypeDef]
    amazonQProperties: NotRequired[AmazonQPropertiesPatchTypeDef]
    mlflowProperties: NotRequired[MlflowPropertiesPatchTypeDef]


class PolicyGrantMemberTypeDef(TypedDict):
    principal: NotRequired[PolicyGrantPrincipalOutputTypeDef]
    detail: NotRequired[PolicyGrantDetailOutputTypeDef]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    grantId: NotRequired[str]


PolicyGrantPrincipalUnionTypeDef = Union[
    PolicyGrantPrincipalTypeDef, PolicyGrantPrincipalOutputTypeDef
]
EnvironmentConfigurationUnionTypeDef = Union[
    EnvironmentConfigurationTypeDef, EnvironmentConfigurationOutputTypeDef
]


class DataSourceConfigurationInputTypeDef(TypedDict):
    glueRunConfiguration: NotRequired[GlueRunConfigurationInputTypeDef]
    redshiftRunConfiguration: NotRequired[RedshiftRunConfigurationInputTypeDef]
    sageMakerRunConfiguration: NotRequired[SageMakerRunConfigurationInputTypeDef]


class PutEnvironmentBlueprintConfigurationInputTypeDef(TypedDict):
    domainIdentifier: str
    environmentBlueprintIdentifier: str
    enabledRegions: Sequence[str]
    provisioningRoleArn: NotRequired[str]
    manageAccessRoleArn: NotRequired[str]
    environmentRolePermissionBoundary: NotRequired[str]
    regionalParameters: NotRequired[Mapping[str, Mapping[str, str]]]
    globalParameters: NotRequired[Mapping[str, str]]
    provisioningConfigurations: NotRequired[Sequence[ProvisioningConfigurationUnionTypeDef]]


class AssetItemTypeDef(TypedDict):
    domainId: str
    identifier: str
    name: str
    typeIdentifier: str
    typeRevision: str
    owningProjectId: str
    externalIdentifier: NotRequired[str]
    description: NotRequired[str]
    createdAt: NotRequired[datetime]
    createdBy: NotRequired[str]
    firstRevisionCreatedAt: NotRequired[datetime]
    firstRevisionCreatedBy: NotRequired[str]
    glossaryTerms: NotRequired[list[str]]
    additionalAttributes: NotRequired[AssetItemAdditionalAttributesTypeDef]
    governedGlossaryTerms: NotRequired[list[str]]


class AssetListingItemTypeDef(TypedDict):
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]
    name: NotRequired[str]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    entityType: NotRequired[str]
    description: NotRequired[str]
    createdAt: NotRequired[datetime]
    listingCreatedBy: NotRequired[str]
    listingUpdatedBy: NotRequired[str]
    glossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]
    governedGlossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]
    owningProjectId: NotRequired[str]
    additionalAttributes: NotRequired[AssetListingItemAdditionalAttributesTypeDef]


DataProductResultItemTypeDef = TypedDict(
    "DataProductResultItemTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "description": NotRequired[str],
        "glossaryTerms": NotRequired[list[str]],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "firstRevisionCreatedAt": NotRequired[datetime],
        "firstRevisionCreatedBy": NotRequired[str],
        "additionalAttributes": NotRequired[DataProductItemAdditionalAttributesTypeDef],
    },
)


class DataProductListingItemTypeDef(TypedDict):
    listingId: NotRequired[str]
    listingRevision: NotRequired[str]
    name: NotRequired[str]
    entityId: NotRequired[str]
    entityRevision: NotRequired[str]
    description: NotRequired[str]
    createdAt: NotRequired[datetime]
    listingCreatedBy: NotRequired[str]
    listingUpdatedBy: NotRequired[str]
    glossaryTerms: NotRequired[list[DetailedGlossaryTermTypeDef]]
    owningProjectId: NotRequired[str]
    additionalAttributes: NotRequired[DataProductListingItemAdditionalAttributesTypeDef]
    items: NotRequired[list[ListingSummaryItemTypeDef]]


GlossaryItemTypeDef = TypedDict(
    "GlossaryItemTypeDef",
    {
        "domainId": str,
        "id": str,
        "name": str,
        "owningProjectId": str,
        "status": GlossaryStatusType,
        "description": NotRequired[str],
        "usageRestrictions": NotRequired[list[Literal["ASSET_GOVERNED_TERMS"]]],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
        "additionalAttributes": NotRequired[GlossaryItemAdditionalAttributesTypeDef],
    },
)
GlossaryTermItemTypeDef = TypedDict(
    "GlossaryTermItemTypeDef",
    {
        "domainId": str,
        "glossaryId": str,
        "id": str,
        "name": str,
        "status": GlossaryTermStatusType,
        "shortDescription": NotRequired[str],
        "usageRestrictions": NotRequired[list[Literal["ASSET_GOVERNED_TERMS"]]],
        "longDescription": NotRequired[str],
        "termRelations": NotRequired[TermRelationsOutputTypeDef],
        "createdAt": NotRequired[datetime],
        "createdBy": NotRequired[str],
        "updatedAt": NotRequired[datetime],
        "updatedBy": NotRequired[str],
        "additionalAttributes": NotRequired[GlossaryTermItemAdditionalAttributesTypeDef],
    },
)


class CreateRuleInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    target: RuleTargetTypeDef
    action: RuleActionType
    scope: RuleScopeUnionTypeDef
    detail: RuleDetailUnionTypeDef
    description: NotRequired[str]
    clientToken: NotRequired[str]


class UpdateRuleInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    scope: NotRequired[RuleScopeUnionTypeDef]
    detail: NotRequired[RuleDetailUnionTypeDef]
    includeChildDomainUnits: NotRequired[bool]


class ListLineageEventsOutputTypeDef(TypedDict):
    items: list[LineageEventSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AssetFilterConfigurationOutputTypeDef(TypedDict):
    columnConfiguration: NotRequired[ColumnFilterConfigurationOutputTypeDef]
    rowConfiguration: NotRequired[RowFilterConfigurationOutputTypeDef]


class AssetFilterConfigurationTypeDef(TypedDict):
    columnConfiguration: NotRequired[ColumnFilterConfigurationTypeDef]
    rowConfiguration: NotRequired[RowFilterConfigurationTypeDef]


class PhysicalEndpointTypeDef(TypedDict):
    awsLocation: NotRequired[AwsLocationTypeDef]
    glueConnectionName: NotRequired[str]
    glueConnection: NotRequired[GlueConnectionTypeDef]
    enableTrustedIdentityPropagation: NotRequired[bool]
    host: NotRequired[str]
    port: NotRequired[int]
    protocol: NotRequired[ProtocolType]
    stage: NotRequired[str]


class GlueConnectionInputTypeDef(TypedDict):
    connectionProperties: NotRequired[Mapping[str, str]]
    physicalConnectionRequirements: NotRequired[PhysicalConnectionRequirementsUnionTypeDef]
    name: NotRequired[str]
    description: NotRequired[str]
    connectionType: NotRequired[GlueConnectionTypeType]
    matchCriteria: NotRequired[str]
    validateCredentials: NotRequired[bool]
    validateForComputeEnvironments: NotRequired[Sequence[ComputeEnvironmentsType]]
    sparkProperties: NotRequired[Mapping[str, str]]
    athenaProperties: NotRequired[Mapping[str, str]]
    pythonProperties: NotRequired[Mapping[str, str]]
    authenticationConfiguration: NotRequired[AuthenticationConfigurationInputTypeDef]


CreateDataSourceOutputTypeDef = TypedDict(
    "CreateDataSourceOutputTypeDef",
    {
        "id": str,
        "status": DataSourceStatusType,
        "type": str,
        "name": str,
        "description": str,
        "domainId": str,
        "projectId": str,
        "environmentId": str,
        "connectionId": str,
        "configuration": DataSourceConfigurationOutputTypeDef,
        "recommendation": RecommendationConfigurationTypeDef,
        "enableSetting": EnableSettingType,
        "publishOnImport": bool,
        "assetFormsOutput": list[FormOutputTypeDef],
        "schedule": ScheduleConfigurationTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDataSourceOutputTypeDef = TypedDict(
    "DeleteDataSourceOutputTypeDef",
    {
        "id": str,
        "status": DataSourceStatusType,
        "type": str,
        "name": str,
        "description": str,
        "domainId": str,
        "projectId": str,
        "environmentId": str,
        "connectionId": str,
        "configuration": DataSourceConfigurationOutputTypeDef,
        "enableSetting": EnableSettingType,
        "publishOnImport": bool,
        "assetFormsOutput": list[FormOutputTypeDef],
        "schedule": ScheduleConfigurationTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "selfGrantStatus": SelfGrantStatusOutputTypeDef,
        "retainPermissionsOnRevokeFailure": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataSourceOutputTypeDef = TypedDict(
    "GetDataSourceOutputTypeDef",
    {
        "id": str,
        "status": DataSourceStatusType,
        "type": str,
        "name": str,
        "description": str,
        "domainId": str,
        "projectId": str,
        "environmentId": str,
        "connectionId": str,
        "configuration": DataSourceConfigurationOutputTypeDef,
        "recommendation": RecommendationConfigurationTypeDef,
        "enableSetting": EnableSettingType,
        "publishOnImport": bool,
        "assetFormsOutput": list[FormOutputTypeDef],
        "schedule": ScheduleConfigurationTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "lastRunAssetCount": int,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "selfGrantStatus": SelfGrantStatusOutputTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDataSourceOutputTypeDef = TypedDict(
    "UpdateDataSourceOutputTypeDef",
    {
        "id": str,
        "status": DataSourceStatusType,
        "type": str,
        "name": str,
        "description": str,
        "domainId": str,
        "projectId": str,
        "environmentId": str,
        "connectionId": str,
        "configuration": DataSourceConfigurationOutputTypeDef,
        "recommendation": RecommendationConfigurationTypeDef,
        "enableSetting": EnableSettingType,
        "publishOnImport": bool,
        "assetFormsOutput": list[FormOutputTypeDef],
        "schedule": ScheduleConfigurationTypeDef,
        "lastRunStatus": DataSourceRunStatusType,
        "lastRunAt": datetime,
        "lastRunErrorMessage": DataSourceErrorMessageTypeDef,
        "errorMessage": DataSourceErrorMessageTypeDef,
        "createdAt": datetime,
        "updatedAt": datetime,
        "selfGrantStatus": SelfGrantStatusOutputTypeDef,
        "retainPermissionsOnRevokeFailure": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AcceptSubscriptionRequestOutputTypeDef = TypedDict(
    "AcceptSubscriptionRequestOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "status": SubscriptionRequestStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "requestReason": str,
        "subscribedPrincipals": list[SubscribedPrincipalTypeDef],
        "subscribedListings": list[SubscribedListingTypeDef],
        "reviewerId": str,
        "decisionComment": str,
        "existingSubscriptionId": str,
        "metadataForms": list[FormOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CancelSubscriptionOutputTypeDef = TypedDict(
    "CancelSubscriptionOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "status": SubscriptionStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscribedListing": SubscribedListingTypeDef,
        "subscriptionRequestId": str,
        "retainPermissions": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateSubscriptionRequestOutputTypeDef = TypedDict(
    "CreateSubscriptionRequestOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "status": SubscriptionRequestStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "requestReason": str,
        "subscribedPrincipals": list[SubscribedPrincipalTypeDef],
        "subscribedListings": list[SubscribedListingTypeDef],
        "reviewerId": str,
        "decisionComment": str,
        "existingSubscriptionId": str,
        "metadataForms": list[FormOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionOutputTypeDef = TypedDict(
    "GetSubscriptionOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "status": SubscriptionStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscribedListing": SubscribedListingTypeDef,
        "subscriptionRequestId": str,
        "retainPermissions": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetSubscriptionRequestDetailsOutputTypeDef = TypedDict(
    "GetSubscriptionRequestDetailsOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "status": SubscriptionRequestStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "requestReason": str,
        "subscribedPrincipals": list[SubscribedPrincipalTypeDef],
        "subscribedListings": list[SubscribedListingTypeDef],
        "reviewerId": str,
        "decisionComment": str,
        "existingSubscriptionId": str,
        "metadataForms": list[FormOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RejectSubscriptionRequestOutputTypeDef = TypedDict(
    "RejectSubscriptionRequestOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "status": SubscriptionRequestStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "requestReason": str,
        "subscribedPrincipals": list[SubscribedPrincipalTypeDef],
        "subscribedListings": list[SubscribedListingTypeDef],
        "reviewerId": str,
        "decisionComment": str,
        "existingSubscriptionId": str,
        "metadataForms": list[FormOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
RevokeSubscriptionOutputTypeDef = TypedDict(
    "RevokeSubscriptionOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "status": SubscriptionStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscribedListing": SubscribedListingTypeDef,
        "subscriptionRequestId": str,
        "retainPermissions": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SubscriptionRequestSummaryTypeDef = TypedDict(
    "SubscriptionRequestSummaryTypeDef",
    {
        "id": str,
        "createdBy": str,
        "domainId": str,
        "status": SubscriptionRequestStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "requestReason": str,
        "subscribedPrincipals": list[SubscribedPrincipalTypeDef],
        "subscribedListings": list[SubscribedListingTypeDef],
        "updatedBy": NotRequired[str],
        "reviewerId": NotRequired[str],
        "decisionComment": NotRequired[str],
        "existingSubscriptionId": NotRequired[str],
        "metadataFormsSummary": NotRequired[list[MetadataFormSummaryTypeDef]],
    },
)
SubscriptionSummaryTypeDef = TypedDict(
    "SubscriptionSummaryTypeDef",
    {
        "id": str,
        "createdBy": str,
        "domainId": str,
        "status": SubscriptionStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "subscribedPrincipal": SubscribedPrincipalTypeDef,
        "subscribedListing": SubscribedListingTypeDef,
        "updatedBy": NotRequired[str],
        "subscriptionRequestId": NotRequired[str],
        "retainPermissions": NotRequired[bool],
    },
)
UpdateSubscriptionRequestOutputTypeDef = TypedDict(
    "UpdateSubscriptionRequestOutputTypeDef",
    {
        "id": str,
        "createdBy": str,
        "updatedBy": str,
        "domainId": str,
        "status": SubscriptionRequestStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "requestReason": str,
        "subscribedPrincipals": list[SubscribedPrincipalTypeDef],
        "subscribedListings": list[SubscribedListingTypeDef],
        "reviewerId": str,
        "decisionComment": str,
        "existingSubscriptionId": str,
        "metadataForms": list[FormOutputTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class UpdateConnectionInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    description: NotRequired[str]
    awsLocation: NotRequired[AwsLocationTypeDef]
    props: NotRequired[ConnectionPropertiesPatchTypeDef]


class ListPolicyGrantsOutputTypeDef(TypedDict):
    grantList: list[PolicyGrantMemberTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class AddPolicyGrantInputTypeDef(TypedDict):
    domainIdentifier: str
    entityType: TargetEntityTypeType
    entityIdentifier: str
    policyType: ManagedPolicyTypeType
    principal: PolicyGrantPrincipalUnionTypeDef
    detail: PolicyGrantDetailUnionTypeDef
    clientToken: NotRequired[str]


class RemovePolicyGrantInputTypeDef(TypedDict):
    domainIdentifier: str
    entityType: TargetEntityTypeType
    entityIdentifier: str
    policyType: ManagedPolicyTypeType
    principal: PolicyGrantPrincipalUnionTypeDef
    grantIdentifier: NotRequired[str]
    clientToken: NotRequired[str]


class CreateProjectProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    description: NotRequired[str]
    status: NotRequired[StatusType]
    projectResourceTags: NotRequired[Sequence[ResourceTagParameterTypeDef]]
    allowCustomProjectResourceTags: NotRequired[bool]
    projectResourceTagsDescription: NotRequired[str]
    environmentConfigurations: NotRequired[Sequence[EnvironmentConfigurationUnionTypeDef]]
    domainUnitIdentifier: NotRequired[str]


class UpdateProjectProfileInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    status: NotRequired[StatusType]
    projectResourceTags: NotRequired[Sequence[ResourceTagParameterTypeDef]]
    allowCustomProjectResourceTags: NotRequired[bool]
    projectResourceTagsDescription: NotRequired[str]
    environmentConfigurations: NotRequired[Sequence[EnvironmentConfigurationUnionTypeDef]]
    domainUnitIdentifier: NotRequired[str]


CreateDataSourceInputTypeDef = TypedDict(
    "CreateDataSourceInputTypeDef",
    {
        "name": str,
        "domainIdentifier": str,
        "projectIdentifier": str,
        "type": str,
        "description": NotRequired[str],
        "environmentIdentifier": NotRequired[str],
        "connectionIdentifier": NotRequired[str],
        "configuration": NotRequired[DataSourceConfigurationInputTypeDef],
        "recommendation": NotRequired[RecommendationConfigurationTypeDef],
        "enableSetting": NotRequired[EnableSettingType],
        "schedule": NotRequired[ScheduleConfigurationTypeDef],
        "publishOnImport": NotRequired[bool],
        "assetFormsInput": NotRequired[Sequence[FormInputTypeDef]],
        "clientToken": NotRequired[str],
    },
)


class UpdateDataSourceInputTypeDef(TypedDict):
    domainIdentifier: str
    identifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    enableSetting: NotRequired[EnableSettingType]
    publishOnImport: NotRequired[bool]
    assetFormsInput: NotRequired[Sequence[FormInputTypeDef]]
    schedule: NotRequired[ScheduleConfigurationTypeDef]
    configuration: NotRequired[DataSourceConfigurationInputTypeDef]
    recommendation: NotRequired[RecommendationConfigurationTypeDef]
    retainPermissionsOnRevokeFailure: NotRequired[bool]


class SearchResultItemTypeDef(TypedDict):
    assetListing: NotRequired[AssetListingItemTypeDef]
    dataProductListing: NotRequired[DataProductListingItemTypeDef]


class SearchInventoryResultItemTypeDef(TypedDict):
    glossaryItem: NotRequired[GlossaryItemTypeDef]
    glossaryTermItem: NotRequired[GlossaryTermItemTypeDef]
    assetItem: NotRequired[AssetItemTypeDef]
    dataProductItem: NotRequired[DataProductResultItemTypeDef]


CreateAssetFilterOutputTypeDef = TypedDict(
    "CreateAssetFilterOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "assetId": str,
        "name": str,
        "description": str,
        "status": FilterStatusType,
        "configuration": AssetFilterConfigurationOutputTypeDef,
        "createdAt": datetime,
        "errorMessage": str,
        "effectiveColumnNames": list[str],
        "effectiveRowFilter": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetAssetFilterOutputTypeDef = TypedDict(
    "GetAssetFilterOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "assetId": str,
        "name": str,
        "description": str,
        "status": FilterStatusType,
        "configuration": AssetFilterConfigurationOutputTypeDef,
        "createdAt": datetime,
        "errorMessage": str,
        "effectiveColumnNames": list[str],
        "effectiveRowFilter": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateAssetFilterOutputTypeDef = TypedDict(
    "UpdateAssetFilterOutputTypeDef",
    {
        "id": str,
        "domainId": str,
        "assetId": str,
        "name": str,
        "description": str,
        "status": FilterStatusType,
        "configuration": AssetFilterConfigurationOutputTypeDef,
        "createdAt": datetime,
        "errorMessage": str,
        "effectiveColumnNames": list[str],
        "effectiveRowFilter": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
AssetFilterConfigurationUnionTypeDef = Union[
    AssetFilterConfigurationTypeDef, AssetFilterConfigurationOutputTypeDef
]
ConnectionSummaryTypeDef = TypedDict(
    "ConnectionSummaryTypeDef",
    {
        "connectionId": str,
        "domainId": str,
        "domainUnitId": str,
        "name": str,
        "physicalEndpoints": list[PhysicalEndpointTypeDef],
        "type": ConnectionTypeType,
        "environmentId": NotRequired[str],
        "projectId": NotRequired[str],
        "props": NotRequired[ConnectionPropertiesOutputTypeDef],
        "scope": NotRequired[ConnectionScopeType],
    },
)
CreateConnectionOutputTypeDef = TypedDict(
    "CreateConnectionOutputTypeDef",
    {
        "connectionId": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentId": str,
        "name": str,
        "physicalEndpoints": list[PhysicalEndpointTypeDef],
        "projectId": str,
        "props": ConnectionPropertiesOutputTypeDef,
        "type": ConnectionTypeType,
        "scope": ConnectionScopeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetConnectionOutputTypeDef = TypedDict(
    "GetConnectionOutputTypeDef",
    {
        "connectionCredentials": ConnectionCredentialsTypeDef,
        "connectionId": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentId": str,
        "environmentUserRole": str,
        "name": str,
        "physicalEndpoints": list[PhysicalEndpointTypeDef],
        "projectId": str,
        "props": ConnectionPropertiesOutputTypeDef,
        "type": ConnectionTypeType,
        "scope": ConnectionScopeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateConnectionOutputTypeDef = TypedDict(
    "UpdateConnectionOutputTypeDef",
    {
        "connectionId": str,
        "description": str,
        "domainId": str,
        "domainUnitId": str,
        "environmentId": str,
        "name": str,
        "physicalEndpoints": list[PhysicalEndpointTypeDef],
        "projectId": str,
        "props": ConnectionPropertiesOutputTypeDef,
        "type": ConnectionTypeType,
        "scope": ConnectionScopeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class GluePropertiesInputTypeDef(TypedDict):
    glueConnectionInput: NotRequired[GlueConnectionInputTypeDef]


class ListSubscriptionRequestsOutputTypeDef(TypedDict):
    items: list[SubscriptionRequestSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSubscriptionsOutputTypeDef(TypedDict):
    items: list[SubscriptionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchListingsOutputTypeDef(TypedDict):
    items: list[SearchResultItemTypeDef]
    totalMatchCount: int
    aggregates: list[AggregationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class SearchOutputTypeDef(TypedDict):
    items: list[SearchInventoryResultItemTypeDef]
    totalMatchCount: int
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateAssetFilterInputTypeDef(TypedDict):
    domainIdentifier: str
    assetIdentifier: str
    name: str
    configuration: AssetFilterConfigurationUnionTypeDef
    description: NotRequired[str]
    clientToken: NotRequired[str]


class UpdateAssetFilterInputTypeDef(TypedDict):
    domainIdentifier: str
    assetIdentifier: str
    identifier: str
    name: NotRequired[str]
    description: NotRequired[str]
    configuration: NotRequired[AssetFilterConfigurationUnionTypeDef]


class ListConnectionsOutputTypeDef(TypedDict):
    items: list[ConnectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ConnectionPropertiesInputTypeDef(TypedDict):
    athenaProperties: NotRequired[AthenaPropertiesInputTypeDef]
    glueProperties: NotRequired[GluePropertiesInputTypeDef]
    hyperPodProperties: NotRequired[HyperPodPropertiesInputTypeDef]
    iamProperties: NotRequired[IamPropertiesInputTypeDef]
    redshiftProperties: NotRequired[RedshiftPropertiesInputTypeDef]
    sparkEmrProperties: NotRequired[SparkEmrPropertiesInputTypeDef]
    sparkGlueProperties: NotRequired[SparkGluePropertiesInputTypeDef]
    s3Properties: NotRequired[S3PropertiesInputTypeDef]
    amazonQProperties: NotRequired[AmazonQPropertiesInputTypeDef]
    mlflowProperties: NotRequired[MlflowPropertiesInputTypeDef]


class CreateConnectionInputTypeDef(TypedDict):
    domainIdentifier: str
    name: str
    awsLocation: NotRequired[AwsLocationTypeDef]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    environmentIdentifier: NotRequired[str]
    props: NotRequired[ConnectionPropertiesInputTypeDef]
    enableTrustedIdentityPropagation: NotRequired[bool]
    scope: NotRequired[ConnectionScopeType]
