"""
Type annotations for quicksight service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_quicksight.client import QuickSightClient

    session = Session()
    client: QuickSightClient = session.client("quicksight")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeFolderPermissionsPaginator,
    DescribeFolderResolvedPermissionsPaginator,
    ListActionConnectorsPaginator,
    ListAnalysesPaginator,
    ListApprovalPoliciesPaginator,
    ListAssetBundleExportJobsPaginator,
    ListAssetBundleImportJobsPaginator,
    ListBrandsPaginator,
    ListCustomPermissionsPaginator,
    ListDashboardsPaginator,
    ListDashboardVersionsPaginator,
    ListDataSetsPaginator,
    ListDataSourcesPaginator,
    ListDlpSettingsPaginator,
    ListFlowsPaginator,
    ListFolderMembersPaginator,
    ListFoldersForResourcePaginator,
    ListFoldersPaginator,
    ListGroupMembershipsPaginator,
    ListGroupsPaginator,
    ListIAMPolicyAssignmentsForUserPaginator,
    ListIAMPolicyAssignmentsPaginator,
    ListIngestionsPaginator,
    ListKnowledgeBasesPaginator,
    ListLimitsProfilesPaginator,
    ListNamespacesPaginator,
    ListOAuthClientApplicationsPaginator,
    ListRoleMembershipsPaginator,
    ListTemplateAliasesPaginator,
    ListTemplatesPaginator,
    ListTemplateVersionsPaginator,
    ListThemesPaginator,
    ListThemeVersionsPaginator,
    ListTopicsV2Paginator,
    ListUserGroupsPaginator,
    ListUsersPaginator,
    SearchActionConnectorsPaginator,
    SearchAnalysesPaginator,
    SearchDashboardsPaginator,
    SearchDataSetsPaginator,
    SearchDataSourcesPaginator,
    SearchFlowsPaginator,
    SearchFoldersPaginator,
    SearchGroupsPaginator,
    SearchKnowledgeBasesPaginator,
    SearchTopicsPaginator,
    SearchTopicsV2Paginator,
)
from .type_defs import (
    BatchCreateTopicReviewedAnswerRequestTypeDef,
    BatchCreateTopicReviewedAnswerResponseTypeDef,
    BatchDeleteKnowledgeBaseRequestTypeDef,
    BatchDeleteKnowledgeBaseResponseTypeDef,
    BatchDeleteTopicReviewedAnswerRequestTypeDef,
    BatchDeleteTopicReviewedAnswerResponseTypeDef,
    BatchDescribeUserLimitsRequestTypeDef,
    BatchDescribeUserLimitsResponseTypeDef,
    CancelIngestionRequestTypeDef,
    CancelIngestionResponseTypeDef,
    CreateAccountCustomizationRequestTypeDef,
    CreateAccountCustomizationResponseTypeDef,
    CreateAccountSubscriptionRequestTypeDef,
    CreateAccountSubscriptionResponseTypeDef,
    CreateActionConnectorRequestTypeDef,
    CreateActionConnectorResponseTypeDef,
    CreateAgentRequestTypeDef,
    CreateAgentResponseTypeDef,
    CreateAnalysisRequestTypeDef,
    CreateAnalysisResponseTypeDef,
    CreateApprovalPolicyRequestTypeDef,
    CreateApprovalPolicyResponseTypeDef,
    CreateBrandRequestTypeDef,
    CreateBrandResponseTypeDef,
    CreateCustomPermissionsRequestTypeDef,
    CreateCustomPermissionsResponseTypeDef,
    CreateDashboardRequestTypeDef,
    CreateDashboardResponseTypeDef,
    CreateDataSetRequestTypeDef,
    CreateDataSetResponseTypeDef,
    CreateDataSourceRequestTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateDlpSettingRequestTypeDef,
    CreateDlpSettingResponseTypeDef,
    CreateFlowRequestTypeDef,
    CreateFlowResponseTypeDef,
    CreateFolderMembershipRequestTypeDef,
    CreateFolderMembershipResponseTypeDef,
    CreateFolderRequestTypeDef,
    CreateFolderResponseTypeDef,
    CreateGroupMembershipRequestTypeDef,
    CreateGroupMembershipResponseTypeDef,
    CreateGroupRequestTypeDef,
    CreateGroupResponseTypeDef,
    CreateIAMPolicyAssignmentRequestTypeDef,
    CreateIAMPolicyAssignmentResponseTypeDef,
    CreateIngestionRequestTypeDef,
    CreateIngestionResponseTypeDef,
    CreateKnowledgeBaseRequestTypeDef,
    CreateKnowledgeBaseResponseTypeDef,
    CreateLimitsProfileRequestTypeDef,
    CreateLimitsProfileResponseTypeDef,
    CreateNamespaceRequestTypeDef,
    CreateNamespaceResponseTypeDef,
    CreateOAuthClientApplicationRequestTypeDef,
    CreateOAuthClientApplicationResponseTypeDef,
    CreateRefreshScheduleRequestTypeDef,
    CreateRefreshScheduleResponseTypeDef,
    CreateRoleMembershipRequestTypeDef,
    CreateRoleMembershipResponseTypeDef,
    CreateSpaceRequestTypeDef,
    CreateSpaceResponseTypeDef,
    CreateTemplateAliasRequestTypeDef,
    CreateTemplateAliasResponseTypeDef,
    CreateTemplateRequestTypeDef,
    CreateTemplateResponseTypeDef,
    CreateThemeAliasRequestTypeDef,
    CreateThemeAliasResponseTypeDef,
    CreateThemeRequestTypeDef,
    CreateThemeResponseTypeDef,
    CreateTopicRefreshScheduleRequestTypeDef,
    CreateTopicRefreshScheduleResponseTypeDef,
    CreateTopicRequestTypeDef,
    CreateTopicResponseTypeDef,
    CreateTopicV2RequestTypeDef,
    CreateTopicV2ResponseTypeDef,
    CreateVPCConnectionRequestTypeDef,
    CreateVPCConnectionResponseTypeDef,
    DeleteAccountCustomizationRequestTypeDef,
    DeleteAccountCustomizationResponseTypeDef,
    DeleteAccountCustomPermissionRequestTypeDef,
    DeleteAccountCustomPermissionResponseTypeDef,
    DeleteAccountSubscriptionRequestTypeDef,
    DeleteAccountSubscriptionResponseTypeDef,
    DeleteActionConnectorRequestTypeDef,
    DeleteActionConnectorResponseTypeDef,
    DeleteAgentRequestTypeDef,
    DeleteAgentResponseTypeDef,
    DeleteAnalysisRequestTypeDef,
    DeleteAnalysisResponseTypeDef,
    DeleteApprovalPolicyRequestTypeDef,
    DeleteBrandAssignmentRequestTypeDef,
    DeleteBrandAssignmentResponseTypeDef,
    DeleteBrandRequestTypeDef,
    DeleteBrandResponseTypeDef,
    DeleteCustomPermissionsRequestTypeDef,
    DeleteCustomPermissionsResponseTypeDef,
    DeleteDashboardRequestTypeDef,
    DeleteDashboardResponseTypeDef,
    DeleteDataSetRefreshPropertiesRequestTypeDef,
    DeleteDataSetRefreshPropertiesResponseTypeDef,
    DeleteDataSetRequestTypeDef,
    DeleteDataSetResponseTypeDef,
    DeleteDataSourceRequestTypeDef,
    DeleteDataSourceResponseTypeDef,
    DeleteDefaultQBusinessApplicationRequestTypeDef,
    DeleteDefaultQBusinessApplicationResponseTypeDef,
    DeleteDlpSettingRequestTypeDef,
    DeleteDlpSettingResponseTypeDef,
    DeleteFlowRequestTypeDef,
    DeleteFlowResponseTypeDef,
    DeleteFolderMembershipRequestTypeDef,
    DeleteFolderMembershipResponseTypeDef,
    DeleteFolderRequestTypeDef,
    DeleteFolderResponseTypeDef,
    DeleteGroupMembershipRequestTypeDef,
    DeleteGroupMembershipResponseTypeDef,
    DeleteGroupRequestTypeDef,
    DeleteGroupResponseTypeDef,
    DeleteIAMPolicyAssignmentRequestTypeDef,
    DeleteIAMPolicyAssignmentResponseTypeDef,
    DeleteIdentityPropagationConfigRequestTypeDef,
    DeleteIdentityPropagationConfigResponseTypeDef,
    DeleteKnowledgeBaseRequestTypeDef,
    DeleteKnowledgeBaseResponseTypeDef,
    DeleteLimitsProfileRequestTypeDef,
    DeleteLimitsProfileResponseTypeDef,
    DeleteNamespaceRequestTypeDef,
    DeleteNamespaceResponseTypeDef,
    DeleteOAuthClientApplicationRequestTypeDef,
    DeleteOAuthClientApplicationResponseTypeDef,
    DeleteRefreshScheduleRequestTypeDef,
    DeleteRefreshScheduleResponseTypeDef,
    DeleteRoleCustomPermissionRequestTypeDef,
    DeleteRoleCustomPermissionResponseTypeDef,
    DeleteRoleMembershipRequestTypeDef,
    DeleteRoleMembershipResponseTypeDef,
    DeleteSpaceRequestTypeDef,
    DeleteSpaceResponseTypeDef,
    DeleteTemplateAliasRequestTypeDef,
    DeleteTemplateAliasResponseTypeDef,
    DeleteTemplateRequestTypeDef,
    DeleteTemplateResponseTypeDef,
    DeleteThemeAliasRequestTypeDef,
    DeleteThemeAliasResponseTypeDef,
    DeleteThemeRequestTypeDef,
    DeleteThemeResponseTypeDef,
    DeleteTopicRefreshScheduleRequestTypeDef,
    DeleteTopicRefreshScheduleResponseTypeDef,
    DeleteTopicRequestTypeDef,
    DeleteTopicResponseTypeDef,
    DeleteTopicV2RequestTypeDef,
    DeleteTopicV2ResponseTypeDef,
    DeleteUserByPrincipalIdRequestTypeDef,
    DeleteUserByPrincipalIdResponseTypeDef,
    DeleteUserCustomPermissionRequestTypeDef,
    DeleteUserCustomPermissionResponseTypeDef,
    DeleteUserRequestTypeDef,
    DeleteUserResponseTypeDef,
    DeleteVPCConnectionRequestTypeDef,
    DeleteVPCConnectionResponseTypeDef,
    DescribeAccountCustomizationRequestTypeDef,
    DescribeAccountCustomizationResponseTypeDef,
    DescribeAccountCustomPermissionRequestTypeDef,
    DescribeAccountCustomPermissionResponseTypeDef,
    DescribeAccountSettingsRequestTypeDef,
    DescribeAccountSettingsResponseTypeDef,
    DescribeAccountSubscriptionRequestTypeDef,
    DescribeAccountSubscriptionResponseTypeDef,
    DescribeActionConnectorPermissionsRequestTypeDef,
    DescribeActionConnectorPermissionsResponseTypeDef,
    DescribeActionConnectorRequestTypeDef,
    DescribeActionConnectorResponseTypeDef,
    DescribeAgentPermissionsRequestTypeDef,
    DescribeAgentPermissionsResponseTypeDef,
    DescribeAgentRequestTypeDef,
    DescribeAgentResponseTypeDef,
    DescribeAnalysisDefinitionRequestTypeDef,
    DescribeAnalysisDefinitionResponseTypeDef,
    DescribeAnalysisPermissionsRequestTypeDef,
    DescribeAnalysisPermissionsResponseTypeDef,
    DescribeAnalysisRequestTypeDef,
    DescribeAnalysisResponseTypeDef,
    DescribeApprovalPolicyRequestTypeDef,
    DescribeApprovalPolicyResponseTypeDef,
    DescribeAssetBundleExportJobRequestTypeDef,
    DescribeAssetBundleExportJobResponseTypeDef,
    DescribeAssetBundleImportJobRequestTypeDef,
    DescribeAssetBundleImportJobResponseTypeDef,
    DescribeAutomationJobRequestTypeDef,
    DescribeAutomationJobResponseTypeDef,
    DescribeBrandAssignmentRequestTypeDef,
    DescribeBrandAssignmentResponseTypeDef,
    DescribeBrandPublishedVersionRequestTypeDef,
    DescribeBrandPublishedVersionResponseTypeDef,
    DescribeBrandRequestTypeDef,
    DescribeBrandResponseTypeDef,
    DescribeCustomPermissionsRequestTypeDef,
    DescribeCustomPermissionsResponseTypeDef,
    DescribeDashboardDefinitionRequestTypeDef,
    DescribeDashboardDefinitionResponseTypeDef,
    DescribeDashboardPermissionsRequestTypeDef,
    DescribeDashboardPermissionsResponseTypeDef,
    DescribeDashboardRequestTypeDef,
    DescribeDashboardResponseTypeDef,
    DescribeDashboardSnapshotJobRequestTypeDef,
    DescribeDashboardSnapshotJobResponseTypeDef,
    DescribeDashboardSnapshotJobResultRequestTypeDef,
    DescribeDashboardSnapshotJobResultResponseTypeDef,
    DescribeDashboardsQAConfigurationRequestTypeDef,
    DescribeDashboardsQAConfigurationResponseTypeDef,
    DescribeDataSetPermissionsRequestTypeDef,
    DescribeDataSetPermissionsResponseTypeDef,
    DescribeDataSetRefreshPropertiesRequestTypeDef,
    DescribeDataSetRefreshPropertiesResponseTypeDef,
    DescribeDataSetRequestTypeDef,
    DescribeDataSetResponseTypeDef,
    DescribeDataSourcePermissionsRequestTypeDef,
    DescribeDataSourcePermissionsResponseTypeDef,
    DescribeDataSourceRequestTypeDef,
    DescribeDataSourceResponseTypeDef,
    DescribeDefaultQBusinessApplicationRequestTypeDef,
    DescribeDefaultQBusinessApplicationResponseTypeDef,
    DescribeDlpSettingRequestTypeDef,
    DescribeDlpSettingResponseTypeDef,
    DescribeFlowRequestTypeDef,
    DescribeFlowResponseTypeDef,
    DescribeFolderPermissionsRequestTypeDef,
    DescribeFolderPermissionsResponseTypeDef,
    DescribeFolderRequestTypeDef,
    DescribeFolderResolvedPermissionsRequestTypeDef,
    DescribeFolderResolvedPermissionsResponseTypeDef,
    DescribeFolderResponseTypeDef,
    DescribeGroupMembershipRequestTypeDef,
    DescribeGroupMembershipResponseTypeDef,
    DescribeGroupRequestTypeDef,
    DescribeGroupResponseTypeDef,
    DescribeIAMPolicyAssignmentRequestTypeDef,
    DescribeIAMPolicyAssignmentResponseTypeDef,
    DescribeIngestionRequestTypeDef,
    DescribeIngestionResponseTypeDef,
    DescribeIpRestrictionRequestTypeDef,
    DescribeIpRestrictionResponseTypeDef,
    DescribeKeyRegistrationRequestTypeDef,
    DescribeKeyRegistrationResponseTypeDef,
    DescribeKnowledgeBasePermissionsRequestTypeDef,
    DescribeKnowledgeBasePermissionsResponseTypeDef,
    DescribeKnowledgeBaseRequestTypeDef,
    DescribeKnowledgeBaseResponseTypeDef,
    DescribeLimitsProfileRequestTypeDef,
    DescribeLimitsProfileResponseTypeDef,
    DescribeNamespaceRequestTypeDef,
    DescribeNamespaceResponseTypeDef,
    DescribeOAuthClientApplicationRequestTypeDef,
    DescribeOAuthClientApplicationResponseTypeDef,
    DescribeQPersonalizationConfigurationRequestTypeDef,
    DescribeQPersonalizationConfigurationResponseTypeDef,
    DescribeQuickSightQSearchConfigurationRequestTypeDef,
    DescribeQuickSightQSearchConfigurationResponseTypeDef,
    DescribeRefreshScheduleRequestTypeDef,
    DescribeRefreshScheduleResponseTypeDef,
    DescribeRoleCustomPermissionRequestTypeDef,
    DescribeRoleCustomPermissionResponseTypeDef,
    DescribeSelfUpgradeConfigurationRequestTypeDef,
    DescribeSelfUpgradeConfigurationResponseTypeDef,
    DescribeSpacePermissionsRequestTypeDef,
    DescribeSpacePermissionsResponseTypeDef,
    DescribeSpaceRequestTypeDef,
    DescribeSpaceResponseTypeDef,
    DescribeTemplateAliasRequestTypeDef,
    DescribeTemplateAliasResponseTypeDef,
    DescribeTemplateDefinitionRequestTypeDef,
    DescribeTemplateDefinitionResponseTypeDef,
    DescribeTemplatePermissionsRequestTypeDef,
    DescribeTemplatePermissionsResponseTypeDef,
    DescribeTemplateRequestTypeDef,
    DescribeTemplateResponseTypeDef,
    DescribeThemeAliasRequestTypeDef,
    DescribeThemeAliasResponseTypeDef,
    DescribeThemePermissionsRequestTypeDef,
    DescribeThemePermissionsResponseTypeDef,
    DescribeThemeRequestTypeDef,
    DescribeThemeResponseTypeDef,
    DescribeTopicPermissionsRequestTypeDef,
    DescribeTopicPermissionsResponseTypeDef,
    DescribeTopicPermissionsV2RequestTypeDef,
    DescribeTopicPermissionsV2ResponseTypeDef,
    DescribeTopicRefreshRequestTypeDef,
    DescribeTopicRefreshResponseTypeDef,
    DescribeTopicRefreshScheduleRequestTypeDef,
    DescribeTopicRefreshScheduleResponseTypeDef,
    DescribeTopicRequestTypeDef,
    DescribeTopicResponseTypeDef,
    DescribeTopicV2RequestTypeDef,
    DescribeTopicV2ResponseTypeDef,
    DescribeUserRequestTypeDef,
    DescribeUserResponseTypeDef,
    DescribeVPCConnectionRequestTypeDef,
    DescribeVPCConnectionResponseTypeDef,
    GenerateEmbedUrlForAnonymousUserRequestTypeDef,
    GenerateEmbedUrlForAnonymousUserResponseTypeDef,
    GenerateEmbedUrlForRegisteredUserRequestTypeDef,
    GenerateEmbedUrlForRegisteredUserResponseTypeDef,
    GenerateEmbedUrlForRegisteredUserWithIdentityRequestTypeDef,
    GenerateEmbedUrlForRegisteredUserWithIdentityResponseTypeDef,
    GetDashboardEmbedUrlRequestTypeDef,
    GetDashboardEmbedUrlResponseTypeDef,
    GetFlowMetadataInputTypeDef,
    GetFlowMetadataOutputTypeDef,
    GetFlowPermissionsInputTypeDef,
    GetFlowPermissionsOutputTypeDef,
    GetIdentityContextRequestTypeDef,
    GetIdentityContextResponseTypeDef,
    GetSessionEmbedUrlRequestTypeDef,
    GetSessionEmbedUrlResponseTypeDef,
    ListActionConnectorsRequestTypeDef,
    ListActionConnectorsResponseTypeDef,
    ListAgentsRequestTypeDef,
    ListAgentsResponseTypeDef,
    ListAnalysesRequestTypeDef,
    ListAnalysesResponseTypeDef,
    ListApprovalPoliciesRequestTypeDef,
    ListApprovalPoliciesResponseTypeDef,
    ListAssetBundleExportJobsRequestTypeDef,
    ListAssetBundleExportJobsResponseTypeDef,
    ListAssetBundleImportJobsRequestTypeDef,
    ListAssetBundleImportJobsResponseTypeDef,
    ListBrandsRequestTypeDef,
    ListBrandsResponseTypeDef,
    ListCustomPermissionsRequestTypeDef,
    ListCustomPermissionsResponseTypeDef,
    ListDashboardsRequestTypeDef,
    ListDashboardsResponseTypeDef,
    ListDashboardVersionsRequestTypeDef,
    ListDashboardVersionsResponseTypeDef,
    ListDataSetsRequestTypeDef,
    ListDataSetsResponseTypeDef,
    ListDataSourcesRequestTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDlpSettingsRequestTypeDef,
    ListDlpSettingsResponseTypeDef,
    ListFlowsInputTypeDef,
    ListFlowsOutputTypeDef,
    ListFolderMembersRequestTypeDef,
    ListFolderMembersResponseTypeDef,
    ListFoldersForResourceRequestTypeDef,
    ListFoldersForResourceResponseTypeDef,
    ListFoldersRequestTypeDef,
    ListFoldersResponseTypeDef,
    ListGroupMembershipsRequestTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsRequestTypeDef,
    ListGroupsResponseTypeDef,
    ListIAMPolicyAssignmentsForUserRequestTypeDef,
    ListIAMPolicyAssignmentsForUserResponseTypeDef,
    ListIAMPolicyAssignmentsRequestTypeDef,
    ListIAMPolicyAssignmentsResponseTypeDef,
    ListIdentityPropagationConfigsRequestTypeDef,
    ListIdentityPropagationConfigsResponseTypeDef,
    ListIngestionsRequestTypeDef,
    ListIngestionsResponseTypeDef,
    ListKnowledgeBasesRequestTypeDef,
    ListKnowledgeBasesResponseTypeDef,
    ListLimitsProfilesRequestTypeDef,
    ListLimitsProfilesResponseTypeDef,
    ListNamespacesRequestTypeDef,
    ListNamespacesResponseTypeDef,
    ListOAuthClientApplicationsRequestTypeDef,
    ListOAuthClientApplicationsResponseTypeDef,
    ListRefreshSchedulesRequestTypeDef,
    ListRefreshSchedulesResponseTypeDef,
    ListRoleMembershipsRequestTypeDef,
    ListRoleMembershipsResponseTypeDef,
    ListSelfUpgradesRequestTypeDef,
    ListSelfUpgradesResponseTypeDef,
    ListSpaceResourcesRequestTypeDef,
    ListSpaceResourcesResponseTypeDef,
    ListSpacesRequestTypeDef,
    ListSpacesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTemplateAliasesRequestTypeDef,
    ListTemplateAliasesResponseTypeDef,
    ListTemplatesRequestTypeDef,
    ListTemplatesResponseTypeDef,
    ListTemplateVersionsRequestTypeDef,
    ListTemplateVersionsResponseTypeDef,
    ListThemeAliasesRequestTypeDef,
    ListThemeAliasesResponseTypeDef,
    ListThemesRequestTypeDef,
    ListThemesResponseTypeDef,
    ListThemeVersionsRequestTypeDef,
    ListThemeVersionsResponseTypeDef,
    ListTopicRefreshSchedulesRequestTypeDef,
    ListTopicRefreshSchedulesResponseTypeDef,
    ListTopicReviewedAnswersRequestTypeDef,
    ListTopicReviewedAnswersResponseTypeDef,
    ListTopicsRequestTypeDef,
    ListTopicsResponseTypeDef,
    ListTopicsV2RequestTypeDef,
    ListTopicsV2ResponseTypeDef,
    ListUserGroupsRequestTypeDef,
    ListUserGroupsResponseTypeDef,
    ListUsersIndexCapacityRequestTypeDef,
    ListUsersIndexCapacityResponseTypeDef,
    ListUsersRequestTypeDef,
    ListUsersResponseTypeDef,
    ListVPCConnectionsRequestTypeDef,
    ListVPCConnectionsResponseTypeDef,
    PredictQAResultsRequestTypeDef,
    PredictQAResultsResponseTypeDef,
    PutDataSetRefreshPropertiesRequestTypeDef,
    PutDataSetRefreshPropertiesResponseTypeDef,
    RegisterUserRequestTypeDef,
    RegisterUserResponseTypeDef,
    RestoreAnalysisRequestTypeDef,
    RestoreAnalysisResponseTypeDef,
    SearchActionConnectorsRequestTypeDef,
    SearchActionConnectorsResponseTypeDef,
    SearchAgentsRequestTypeDef,
    SearchAgentsResponseTypeDef,
    SearchAnalysesRequestTypeDef,
    SearchAnalysesResponseTypeDef,
    SearchDashboardsRequestTypeDef,
    SearchDashboardsResponseTypeDef,
    SearchDataSetsRequestTypeDef,
    SearchDataSetsResponseTypeDef,
    SearchDataSourcesRequestTypeDef,
    SearchDataSourcesResponseTypeDef,
    SearchFlowsInputTypeDef,
    SearchFlowsOutputTypeDef,
    SearchFoldersRequestTypeDef,
    SearchFoldersResponseTypeDef,
    SearchGroupsRequestTypeDef,
    SearchGroupsResponseTypeDef,
    SearchKnowledgeBasesRequestTypeDef,
    SearchKnowledgeBasesResponseTypeDef,
    SearchSpacesRequestTypeDef,
    SearchSpacesResponseTypeDef,
    SearchTopicsRequestTypeDef,
    SearchTopicsResponseTypeDef,
    SearchTopicsV2RequestTypeDef,
    SearchTopicsV2ResponseTypeDef,
    StartAssetBundleExportJobRequestTypeDef,
    StartAssetBundleExportJobResponseTypeDef,
    StartAssetBundleImportJobRequestTypeDef,
    StartAssetBundleImportJobResponseTypeDef,
    StartAutomationJobRequestTypeDef,
    StartAutomationJobResponseTypeDef,
    StartDashboardSnapshotJobRequestTypeDef,
    StartDashboardSnapshotJobResponseTypeDef,
    StartDashboardSnapshotJobScheduleRequestTypeDef,
    StartDashboardSnapshotJobScheduleResponseTypeDef,
    TagResourceRequestTypeDef,
    TagResourceResponseTypeDef,
    UntagResourceRequestTypeDef,
    UntagResourceResponseTypeDef,
    UpdateAccountCustomizationRequestTypeDef,
    UpdateAccountCustomizationResponseTypeDef,
    UpdateAccountCustomPermissionRequestTypeDef,
    UpdateAccountCustomPermissionResponseTypeDef,
    UpdateAccountSettingsRequestTypeDef,
    UpdateAccountSettingsResponseTypeDef,
    UpdateActionConnectorPermissionsRequestTypeDef,
    UpdateActionConnectorPermissionsResponseTypeDef,
    UpdateActionConnectorRequestTypeDef,
    UpdateActionConnectorResponseTypeDef,
    UpdateAgentPermissionsRequestTypeDef,
    UpdateAgentPermissionsResponseTypeDef,
    UpdateAgentRequestTypeDef,
    UpdateAgentResponseTypeDef,
    UpdateAnalysisPermissionsRequestTypeDef,
    UpdateAnalysisPermissionsResponseTypeDef,
    UpdateAnalysisRequestTypeDef,
    UpdateAnalysisResponseTypeDef,
    UpdateApplicationWithTokenExchangeGrantRequestTypeDef,
    UpdateApplicationWithTokenExchangeGrantResponseTypeDef,
    UpdateApprovalPolicyRequestTypeDef,
    UpdateApprovalPolicyResponseTypeDef,
    UpdateBrandAssignmentRequestTypeDef,
    UpdateBrandAssignmentResponseTypeDef,
    UpdateBrandPublishedVersionRequestTypeDef,
    UpdateBrandPublishedVersionResponseTypeDef,
    UpdateBrandRequestTypeDef,
    UpdateBrandResponseTypeDef,
    UpdateCustomPermissionsRequestTypeDef,
    UpdateCustomPermissionsResponseTypeDef,
    UpdateDashboardLinksRequestTypeDef,
    UpdateDashboardLinksResponseTypeDef,
    UpdateDashboardPermissionsRequestTypeDef,
    UpdateDashboardPermissionsResponseTypeDef,
    UpdateDashboardPublishedVersionRequestTypeDef,
    UpdateDashboardPublishedVersionResponseTypeDef,
    UpdateDashboardRequestTypeDef,
    UpdateDashboardResponseTypeDef,
    UpdateDashboardsQAConfigurationRequestTypeDef,
    UpdateDashboardsQAConfigurationResponseTypeDef,
    UpdateDataSetPermissionsRequestTypeDef,
    UpdateDataSetPermissionsResponseTypeDef,
    UpdateDataSetRequestTypeDef,
    UpdateDataSetResponseTypeDef,
    UpdateDataSourcePermissionsRequestTypeDef,
    UpdateDataSourcePermissionsResponseTypeDef,
    UpdateDataSourceRequestTypeDef,
    UpdateDataSourceResponseTypeDef,
    UpdateDefaultQBusinessApplicationRequestTypeDef,
    UpdateDefaultQBusinessApplicationResponseTypeDef,
    UpdateDlpSettingRequestTypeDef,
    UpdateDlpSettingResponseTypeDef,
    UpdateFlowPermissionsInputTypeDef,
    UpdateFlowPermissionsOutputTypeDef,
    UpdateFlowRequestTypeDef,
    UpdateFlowResponseTypeDef,
    UpdateFolderPermissionsRequestTypeDef,
    UpdateFolderPermissionsResponseTypeDef,
    UpdateFolderRequestTypeDef,
    UpdateFolderResponseTypeDef,
    UpdateGroupRequestTypeDef,
    UpdateGroupResponseTypeDef,
    UpdateIAMPolicyAssignmentRequestTypeDef,
    UpdateIAMPolicyAssignmentResponseTypeDef,
    UpdateIdentityPropagationConfigRequestTypeDef,
    UpdateIdentityPropagationConfigResponseTypeDef,
    UpdateIpRestrictionRequestTypeDef,
    UpdateIpRestrictionResponseTypeDef,
    UpdateKeyRegistrationRequestTypeDef,
    UpdateKeyRegistrationResponseTypeDef,
    UpdateKnowledgeBasePermissionsRequestTypeDef,
    UpdateKnowledgeBasePermissionsResponseTypeDef,
    UpdateKnowledgeBaseRequestTypeDef,
    UpdateKnowledgeBaseResponseTypeDef,
    UpdateLimitsProfileRequestTypeDef,
    UpdateLimitsProfileResponseTypeDef,
    UpdateOAuthClientApplicationRequestTypeDef,
    UpdateOAuthClientApplicationResponseTypeDef,
    UpdatePublicSharingSettingsRequestTypeDef,
    UpdatePublicSharingSettingsResponseTypeDef,
    UpdateQPersonalizationConfigurationRequestTypeDef,
    UpdateQPersonalizationConfigurationResponseTypeDef,
    UpdateQuickSightQSearchConfigurationRequestTypeDef,
    UpdateQuickSightQSearchConfigurationResponseTypeDef,
    UpdateRefreshScheduleRequestTypeDef,
    UpdateRefreshScheduleResponseTypeDef,
    UpdateRoleCustomPermissionRequestTypeDef,
    UpdateRoleCustomPermissionResponseTypeDef,
    UpdateSelfUpgradeConfigurationRequestTypeDef,
    UpdateSelfUpgradeConfigurationResponseTypeDef,
    UpdateSelfUpgradeRequestTypeDef,
    UpdateSelfUpgradeResponseTypeDef,
    UpdateSpacePermissionsRequestTypeDef,
    UpdateSpacePermissionsResponseTypeDef,
    UpdateSpaceRequestTypeDef,
    UpdateSpaceResourcesRequestTypeDef,
    UpdateSpaceResourcesResponseTypeDef,
    UpdateSpaceResponseTypeDef,
    UpdateSPICECapacityConfigurationRequestTypeDef,
    UpdateSPICECapacityConfigurationResponseTypeDef,
    UpdateTemplateAliasRequestTypeDef,
    UpdateTemplateAliasResponseTypeDef,
    UpdateTemplatePermissionsRequestTypeDef,
    UpdateTemplatePermissionsResponseTypeDef,
    UpdateTemplateRequestTypeDef,
    UpdateTemplateResponseTypeDef,
    UpdateThemeAliasRequestTypeDef,
    UpdateThemeAliasResponseTypeDef,
    UpdateThemePermissionsRequestTypeDef,
    UpdateThemePermissionsResponseTypeDef,
    UpdateThemeRequestTypeDef,
    UpdateThemeResponseTypeDef,
    UpdateTopicPermissionsRequestTypeDef,
    UpdateTopicPermissionsResponseTypeDef,
    UpdateTopicPermissionsV2RequestTypeDef,
    UpdateTopicPermissionsV2ResponseTypeDef,
    UpdateTopicRefreshScheduleRequestTypeDef,
    UpdateTopicRefreshScheduleResponseTypeDef,
    UpdateTopicRequestTypeDef,
    UpdateTopicResponseTypeDef,
    UpdateTopicV2RequestTypeDef,
    UpdateTopicV2ResponseTypeDef,
    UpdateUserCustomPermissionRequestTypeDef,
    UpdateUserCustomPermissionResponseTypeDef,
    UpdateUserRequestTypeDef,
    UpdateUserResponseTypeDef,
    UpdateVPCConnectionRequestTypeDef,
    UpdateVPCConnectionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("QuickSightClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConcurrentUpdatingException: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    CustomerManagedKeyUnavailableException: type[BotocoreClientError]
    DomainNotWhitelistedException: type[BotocoreClientError]
    IdentityTypeNotSupportedException: type[BotocoreClientError]
    InternalFailureException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    InvalidDataSetParameterValueException: type[BotocoreClientError]
    InvalidNextTokenException: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    InvalidParameterValueException: type[BotocoreClientError]
    InvalidRequestException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    PreconditionNotMetException: type[BotocoreClientError]
    QuickSightUserNotFoundException: type[BotocoreClientError]
    ResourceExistsException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ResourceUnavailableException: type[BotocoreClientError]
    SessionLifetimeInMinutesInvalidException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    UnsupportedPricingPlanException: type[BotocoreClientError]
    UnsupportedUserEditionException: type[BotocoreClientError]

class QuickSightClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        QuickSightClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight.html#QuickSight.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#generate_presigned_url)
        """

    def batch_create_topic_reviewed_answer(
        self, **kwargs: Unpack[BatchCreateTopicReviewedAnswerRequestTypeDef]
    ) -> BatchCreateTopicReviewedAnswerResponseTypeDef:
        """
        Creates new reviewed answers for a Q Topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/batch_create_topic_reviewed_answer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#batch_create_topic_reviewed_answer)
        """

    def batch_delete_knowledge_base(
        self, **kwargs: Unpack[BatchDeleteKnowledgeBaseRequestTypeDef]
    ) -> BatchDeleteKnowledgeBaseResponseTypeDef:
        """
        Deletes one or more knowledge bases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/batch_delete_knowledge_base.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#batch_delete_knowledge_base)
        """

    def batch_delete_topic_reviewed_answer(
        self, **kwargs: Unpack[BatchDeleteTopicReviewedAnswerRequestTypeDef]
    ) -> BatchDeleteTopicReviewedAnswerResponseTypeDef:
        """
        Deletes reviewed answers for Q Topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/batch_delete_topic_reviewed_answer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#batch_delete_topic_reviewed_answer)
        """

    def batch_describe_user_limits(
        self, **kwargs: Unpack[BatchDescribeUserLimitsRequestTypeDef]
    ) -> BatchDescribeUserLimitsResponseTypeDef:
        """
        Describes the effective resource limits for one or more Amazon Quick Sight
        users, including the limits that apply to each user based on their profile
        assignments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/batch_describe_user_limits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#batch_describe_user_limits)
        """

    def cancel_ingestion(
        self, **kwargs: Unpack[CancelIngestionRequestTypeDef]
    ) -> CancelIngestionResponseTypeDef:
        """
        Cancels an ongoing ingestion of data into SPICE.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/cancel_ingestion.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#cancel_ingestion)
        """

    def create_account_customization(
        self, **kwargs: Unpack[CreateAccountCustomizationRequestTypeDef]
    ) -> CreateAccountCustomizationResponseTypeDef:
        """
        Creates Amazon Quick Sight customizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_account_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_account_customization)
        """

    def create_account_subscription(
        self, **kwargs: Unpack[CreateAccountSubscriptionRequestTypeDef]
    ) -> CreateAccountSubscriptionResponseTypeDef:
        """
        Creates an Amazon Quick Sight account, or subscribes to Amazon Quick Sight Q.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_account_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_account_subscription)
        """

    def create_action_connector(
        self, **kwargs: Unpack[CreateActionConnectorRequestTypeDef]
    ) -> CreateActionConnectorResponseTypeDef:
        """
        Creates an action connector that enables Amazon Quick Sight to connect to
        external services and perform actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_action_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_action_connector)
        """

    def create_agent(
        self, **kwargs: Unpack[CreateAgentRequestTypeDef]
    ) -> CreateAgentResponseTypeDef:
        """
        Creates an agent in Amazon QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_agent)
        """

    def create_analysis(
        self, **kwargs: Unpack[CreateAnalysisRequestTypeDef]
    ) -> CreateAnalysisResponseTypeDef:
        """
        Creates an analysis in Amazon Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_analysis.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_analysis)
        """

    def create_approval_policy(
        self, **kwargs: Unpack[CreateApprovalPolicyRequestTypeDef]
    ) -> CreateApprovalPolicyResponseTypeDef:
        """
        Creates an approval policy in Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_approval_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_approval_policy)
        """

    def create_brand(
        self, **kwargs: Unpack[CreateBrandRequestTypeDef]
    ) -> CreateBrandResponseTypeDef:
        """
        Creates an Quick Sight brand.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_brand.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_brand)
        """

    def create_custom_permissions(
        self, **kwargs: Unpack[CreateCustomPermissionsRequestTypeDef]
    ) -> CreateCustomPermissionsResponseTypeDef:
        """
        Creates a custom permissions profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_custom_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_custom_permissions)
        """

    def create_dashboard(
        self, **kwargs: Unpack[CreateDashboardRequestTypeDef]
    ) -> CreateDashboardResponseTypeDef:
        """
        Creates a dashboard from either a template or directly with a
        <code>DashboardDefinition</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_dashboard.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_dashboard)
        """

    def create_data_set(
        self, **kwargs: Unpack[CreateDataSetRequestTypeDef]
    ) -> CreateDataSetResponseTypeDef:
        """
        Creates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_data_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_data_set)
        """

    def create_data_source(
        self, **kwargs: Unpack[CreateDataSourceRequestTypeDef]
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_data_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_data_source)
        """

    def create_dlp_setting(
        self, **kwargs: Unpack[CreateDlpSettingRequestTypeDef]
    ) -> CreateDlpSettingResponseTypeDef:
        """
        Creates a data loss prevention (DLP) setting configuration for an Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_dlp_setting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_dlp_setting)
        """

    def create_flow(self, **kwargs: Unpack[CreateFlowRequestTypeDef]) -> CreateFlowResponseTypeDef:
        """
        Creates a new flow in the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_flow)
        """

    def create_folder(
        self, **kwargs: Unpack[CreateFolderRequestTypeDef]
    ) -> CreateFolderResponseTypeDef:
        """
        Creates an empty shared folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_folder.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_folder)
        """

    def create_folder_membership(
        self, **kwargs: Unpack[CreateFolderMembershipRequestTypeDef]
    ) -> CreateFolderMembershipResponseTypeDef:
        """
        Adds an asset, such as a dashboard, analysis, or dataset into a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_folder_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_folder_membership)
        """

    def create_group(
        self, **kwargs: Unpack[CreateGroupRequestTypeDef]
    ) -> CreateGroupResponseTypeDef:
        """
        Use the <code>CreateGroup</code> operation to create a group in Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_group)
        """

    def create_group_membership(
        self, **kwargs: Unpack[CreateGroupMembershipRequestTypeDef]
    ) -> CreateGroupMembershipResponseTypeDef:
        """
        Adds an Amazon Quick Sight user to an Amazon Quick Sight group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_group_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_group_membership)
        """

    def create_iam_policy_assignment(
        self, **kwargs: Unpack[CreateIAMPolicyAssignmentRequestTypeDef]
    ) -> CreateIAMPolicyAssignmentResponseTypeDef:
        """
        Creates an assignment with one specified IAM policy, identified by its Amazon
        Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_iam_policy_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_iam_policy_assignment)
        """

    def create_ingestion(
        self, **kwargs: Unpack[CreateIngestionRequestTypeDef]
    ) -> CreateIngestionResponseTypeDef:
        """
        Creates and starts a new SPICE ingestion for a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_ingestion.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_ingestion)
        """

    def create_knowledge_base(
        self, **kwargs: Unpack[CreateKnowledgeBaseRequestTypeDef]
    ) -> CreateKnowledgeBaseResponseTypeDef:
        """
        Creates a knowledge base from a specified data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_knowledge_base.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_knowledge_base)
        """

    def create_limits_profile(
        self, **kwargs: Unpack[CreateLimitsProfileRequestTypeDef]
    ) -> CreateLimitsProfileResponseTypeDef:
        """
        Creates a limits profile that defines resource usage limits for Amazon Quick
        Sight users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_limits_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_limits_profile)
        """

    def create_namespace(
        self, **kwargs: Unpack[CreateNamespaceRequestTypeDef]
    ) -> CreateNamespaceResponseTypeDef:
        """
        (Enterprise edition only) Creates a new namespace for you to use with Amazon
        Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_namespace)
        """

    def create_o_auth_client_application(
        self, **kwargs: Unpack[CreateOAuthClientApplicationRequestTypeDef]
    ) -> CreateOAuthClientApplicationResponseTypeDef:
        """
        Creates an OAuthClientApplication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_o_auth_client_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_o_auth_client_application)
        """

    def create_refresh_schedule(
        self, **kwargs: Unpack[CreateRefreshScheduleRequestTypeDef]
    ) -> CreateRefreshScheduleResponseTypeDef:
        """
        Creates a refresh schedule for a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_refresh_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_refresh_schedule)
        """

    def create_role_membership(
        self, **kwargs: Unpack[CreateRoleMembershipRequestTypeDef]
    ) -> CreateRoleMembershipResponseTypeDef:
        """
        Use <code>CreateRoleMembership</code> to add an existing Quick Sight group to
        an existing role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_role_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_role_membership)
        """

    def create_space(
        self, **kwargs: Unpack[CreateSpaceRequestTypeDef]
    ) -> CreateSpaceResponseTypeDef:
        """
        Creates a new Amazon QuickSight space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_space)
        """

    def create_template(
        self, **kwargs: Unpack[CreateTemplateRequestTypeDef]
    ) -> CreateTemplateResponseTypeDef:
        """
        Creates a template either from a <code>TemplateDefinition</code> or from an
        existing Quick Sight analysis or template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_template)
        """

    def create_template_alias(
        self, **kwargs: Unpack[CreateTemplateAliasRequestTypeDef]
    ) -> CreateTemplateAliasResponseTypeDef:
        """
        Creates a template alias for a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_template_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_template_alias)
        """

    def create_theme(
        self, **kwargs: Unpack[CreateThemeRequestTypeDef]
    ) -> CreateThemeResponseTypeDef:
        """
        Creates a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_theme.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_theme)
        """

    def create_theme_alias(
        self, **kwargs: Unpack[CreateThemeAliasRequestTypeDef]
    ) -> CreateThemeAliasResponseTypeDef:
        """
        Creates a theme alias for a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_theme_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_theme_alias)
        """

    def create_topic(
        self, **kwargs: Unpack[CreateTopicRequestTypeDef]
    ) -> CreateTopicResponseTypeDef:
        """
        Creates a new Q topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_topic.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_topic)
        """

    def create_topic_refresh_schedule(
        self, **kwargs: Unpack[CreateTopicRefreshScheduleRequestTypeDef]
    ) -> CreateTopicRefreshScheduleResponseTypeDef:
        """
        Creates a topic refresh schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_topic_refresh_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_topic_refresh_schedule)
        """

    def create_topic_v2(
        self, **kwargs: Unpack[CreateTopicV2RequestTypeDef]
    ) -> CreateTopicV2ResponseTypeDef:
        """
        Creates a new Q topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_topic_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_topic_v2)
        """

    def create_vpc_connection(
        self, **kwargs: Unpack[CreateVPCConnectionRequestTypeDef]
    ) -> CreateVPCConnectionResponseTypeDef:
        """
        Creates a new VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_vpc_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_vpc_connection)
        """

    def delete_account_custom_permission(
        self, **kwargs: Unpack[DeleteAccountCustomPermissionRequestTypeDef]
    ) -> DeleteAccountCustomPermissionResponseTypeDef:
        """
        Unapplies a custom permissions profile from an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_account_custom_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_account_custom_permission)
        """

    def delete_account_customization(
        self, **kwargs: Unpack[DeleteAccountCustomizationRequestTypeDef]
    ) -> DeleteAccountCustomizationResponseTypeDef:
        """
        This API permanently deletes all Quick Sight customizations for the specified
        Amazon Web Services account and namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_account_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_account_customization)
        """

    def delete_account_subscription(
        self, **kwargs: Unpack[DeleteAccountSubscriptionRequestTypeDef]
    ) -> DeleteAccountSubscriptionResponseTypeDef:
        """
        Deleting your Quick Sight account subscription has permanent, irreversible
        consequences across all Amazon Web Services regions:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_account_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_account_subscription)
        """

    def delete_action_connector(
        self, **kwargs: Unpack[DeleteActionConnectorRequestTypeDef]
    ) -> DeleteActionConnectorResponseTypeDef:
        """
        Hard deletes an action connector, making it unrecoverable.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_action_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_action_connector)
        """

    def delete_agent(
        self, **kwargs: Unpack[DeleteAgentRequestTypeDef]
    ) -> DeleteAgentResponseTypeDef:
        """
        Deletes an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_agent)
        """

    def delete_analysis(
        self, **kwargs: Unpack[DeleteAnalysisRequestTypeDef]
    ) -> DeleteAnalysisResponseTypeDef:
        """
        Deletes an analysis from Amazon Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_analysis.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_analysis)
        """

    def delete_approval_policy(
        self, **kwargs: Unpack[DeleteApprovalPolicyRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an approval policy in Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_approval_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_approval_policy)
        """

    def delete_brand(
        self, **kwargs: Unpack[DeleteBrandRequestTypeDef]
    ) -> DeleteBrandResponseTypeDef:
        """
        This API permanently deletes the specified Quick Sight brand.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_brand.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_brand)
        """

    def delete_brand_assignment(
        self, **kwargs: Unpack[DeleteBrandAssignmentRequestTypeDef]
    ) -> DeleteBrandAssignmentResponseTypeDef:
        """
        Deletes a brand assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_brand_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_brand_assignment)
        """

    def delete_custom_permissions(
        self, **kwargs: Unpack[DeleteCustomPermissionsRequestTypeDef]
    ) -> DeleteCustomPermissionsResponseTypeDef:
        """
        Deletes a custom permissions profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_custom_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_custom_permissions)
        """

    def delete_dashboard(
        self, **kwargs: Unpack[DeleteDashboardRequestTypeDef]
    ) -> DeleteDashboardResponseTypeDef:
        """
        Deletes a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_dashboard.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_dashboard)
        """

    def delete_data_set(
        self, **kwargs: Unpack[DeleteDataSetRequestTypeDef]
    ) -> DeleteDataSetResponseTypeDef:
        """
        Deletes a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_data_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_data_set)
        """

    def delete_data_set_refresh_properties(
        self, **kwargs: Unpack[DeleteDataSetRefreshPropertiesRequestTypeDef]
    ) -> DeleteDataSetRefreshPropertiesResponseTypeDef:
        """
        Deletes the dataset refresh properties of the dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_data_set_refresh_properties.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_data_set_refresh_properties)
        """

    def delete_data_source(
        self, **kwargs: Unpack[DeleteDataSourceRequestTypeDef]
    ) -> DeleteDataSourceResponseTypeDef:
        """
        Deletes the data source permanently.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_data_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_data_source)
        """

    def delete_default_q_business_application(
        self, **kwargs: Unpack[DeleteDefaultQBusinessApplicationRequestTypeDef]
    ) -> DeleteDefaultQBusinessApplicationResponseTypeDef:
        """
        Deletes a linked Amazon Q Business application from an Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_default_q_business_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_default_q_business_application)
        """

    def delete_dlp_setting(
        self, **kwargs: Unpack[DeleteDlpSettingRequestTypeDef]
    ) -> DeleteDlpSettingResponseTypeDef:
        """
        Deletes a DLP setting configuration from an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_dlp_setting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_dlp_setting)
        """

    def delete_flow(self, **kwargs: Unpack[DeleteFlowRequestTypeDef]) -> DeleteFlowResponseTypeDef:
        """
        Permanently deletes a flow from the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_flow)
        """

    def delete_folder(
        self, **kwargs: Unpack[DeleteFolderRequestTypeDef]
    ) -> DeleteFolderResponseTypeDef:
        """
        Deletes an empty folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_folder.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_folder)
        """

    def delete_folder_membership(
        self, **kwargs: Unpack[DeleteFolderMembershipRequestTypeDef]
    ) -> DeleteFolderMembershipResponseTypeDef:
        """
        Removes an asset, such as a dashboard, analysis, or dataset, from a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_folder_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_folder_membership)
        """

    def delete_group(
        self, **kwargs: Unpack[DeleteGroupRequestTypeDef]
    ) -> DeleteGroupResponseTypeDef:
        """
        Removes a user group from Amazon Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_group)
        """

    def delete_group_membership(
        self, **kwargs: Unpack[DeleteGroupMembershipRequestTypeDef]
    ) -> DeleteGroupMembershipResponseTypeDef:
        """
        Removes a user from a group so that the user is no longer a member of the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_group_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_group_membership)
        """

    def delete_iam_policy_assignment(
        self, **kwargs: Unpack[DeleteIAMPolicyAssignmentRequestTypeDef]
    ) -> DeleteIAMPolicyAssignmentResponseTypeDef:
        """
        Deletes an existing IAM policy assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_iam_policy_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_iam_policy_assignment)
        """

    def delete_identity_propagation_config(
        self, **kwargs: Unpack[DeleteIdentityPropagationConfigRequestTypeDef]
    ) -> DeleteIdentityPropagationConfigResponseTypeDef:
        """
        Deletes all access scopes and authorized targets that are associated with a
        service from the Quick Sight IAM Identity Center application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_identity_propagation_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_identity_propagation_config)
        """

    def delete_knowledge_base(
        self, **kwargs: Unpack[DeleteKnowledgeBaseRequestTypeDef]
    ) -> DeleteKnowledgeBaseResponseTypeDef:
        """
        Deletes a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_knowledge_base.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_knowledge_base)
        """

    def delete_limits_profile(
        self, **kwargs: Unpack[DeleteLimitsProfileRequestTypeDef]
    ) -> DeleteLimitsProfileResponseTypeDef:
        """
        Deletes a limits profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_limits_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_limits_profile)
        """

    def delete_namespace(
        self, **kwargs: Unpack[DeleteNamespaceRequestTypeDef]
    ) -> DeleteNamespaceResponseTypeDef:
        """
        Deletes a namespace and the users and groups that are associated with the
        namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_namespace)
        """

    def delete_o_auth_client_application(
        self, **kwargs: Unpack[DeleteOAuthClientApplicationRequestTypeDef]
    ) -> DeleteOAuthClientApplicationResponseTypeDef:
        """
        Deletes an OAuthClientApplication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_o_auth_client_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_o_auth_client_application)
        """

    def delete_refresh_schedule(
        self, **kwargs: Unpack[DeleteRefreshScheduleRequestTypeDef]
    ) -> DeleteRefreshScheduleResponseTypeDef:
        """
        Deletes a refresh schedule from a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_refresh_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_refresh_schedule)
        """

    def delete_role_custom_permission(
        self, **kwargs: Unpack[DeleteRoleCustomPermissionRequestTypeDef]
    ) -> DeleteRoleCustomPermissionResponseTypeDef:
        """
        Removes custom permissions from the role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_role_custom_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_role_custom_permission)
        """

    def delete_role_membership(
        self, **kwargs: Unpack[DeleteRoleMembershipRequestTypeDef]
    ) -> DeleteRoleMembershipResponseTypeDef:
        """
        Removes a group from a role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_role_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_role_membership)
        """

    def delete_space(
        self, **kwargs: Unpack[DeleteSpaceRequestTypeDef]
    ) -> DeleteSpaceResponseTypeDef:
        """
        Deletes an Amazon QuickSight space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_space)
        """

    def delete_template(
        self, **kwargs: Unpack[DeleteTemplateRequestTypeDef]
    ) -> DeleteTemplateResponseTypeDef:
        """
        Deletes a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_template)
        """

    def delete_template_alias(
        self, **kwargs: Unpack[DeleteTemplateAliasRequestTypeDef]
    ) -> DeleteTemplateAliasResponseTypeDef:
        """
        Deletes the item that the specified template alias points to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_template_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_template_alias)
        """

    def delete_theme(
        self, **kwargs: Unpack[DeleteThemeRequestTypeDef]
    ) -> DeleteThemeResponseTypeDef:
        """
        Deletes a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_theme.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_theme)
        """

    def delete_theme_alias(
        self, **kwargs: Unpack[DeleteThemeAliasRequestTypeDef]
    ) -> DeleteThemeAliasResponseTypeDef:
        """
        Deletes the version of the theme that the specified theme alias points to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_theme_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_theme_alias)
        """

    def delete_topic(
        self, **kwargs: Unpack[DeleteTopicRequestTypeDef]
    ) -> DeleteTopicResponseTypeDef:
        """
        Deletes a topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_topic.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_topic)
        """

    def delete_topic_refresh_schedule(
        self, **kwargs: Unpack[DeleteTopicRefreshScheduleRequestTypeDef]
    ) -> DeleteTopicRefreshScheduleResponseTypeDef:
        """
        Deletes a topic refresh schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_topic_refresh_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_topic_refresh_schedule)
        """

    def delete_topic_v2(
        self, **kwargs: Unpack[DeleteTopicV2RequestTypeDef]
    ) -> DeleteTopicV2ResponseTypeDef:
        """
        Deletes a Q topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_topic_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_topic_v2)
        """

    def delete_user(self, **kwargs: Unpack[DeleteUserRequestTypeDef]) -> DeleteUserResponseTypeDef:
        """
        Deletes the Amazon Quick Sight user that is associated with the identity of the
        IAM user or role that's making the call.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_user)
        """

    def delete_user_by_principal_id(
        self, **kwargs: Unpack[DeleteUserByPrincipalIdRequestTypeDef]
    ) -> DeleteUserByPrincipalIdResponseTypeDef:
        """
        Deletes a user identified by its principal ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_user_by_principal_id.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_user_by_principal_id)
        """

    def delete_user_custom_permission(
        self, **kwargs: Unpack[DeleteUserCustomPermissionRequestTypeDef]
    ) -> DeleteUserCustomPermissionResponseTypeDef:
        """
        Deletes a custom permissions profile from a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_user_custom_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_user_custom_permission)
        """

    def delete_vpc_connection(
        self, **kwargs: Unpack[DeleteVPCConnectionRequestTypeDef]
    ) -> DeleteVPCConnectionResponseTypeDef:
        """
        Deletes a VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_vpc_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_vpc_connection)
        """

    def describe_account_custom_permission(
        self, **kwargs: Unpack[DescribeAccountCustomPermissionRequestTypeDef]
    ) -> DescribeAccountCustomPermissionResponseTypeDef:
        """
        Describes the custom permissions profile that is applied to an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_account_custom_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_account_custom_permission)
        """

    def describe_account_customization(
        self, **kwargs: Unpack[DescribeAccountCustomizationRequestTypeDef]
    ) -> DescribeAccountCustomizationResponseTypeDef:
        """
        Describes the customizations associated with the provided Amazon Web Services
        account and Amazon Quick Sight namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_account_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_account_customization)
        """

    def describe_account_settings(
        self, **kwargs: Unpack[DescribeAccountSettingsRequestTypeDef]
    ) -> DescribeAccountSettingsResponseTypeDef:
        """
        Describes the settings that were used when your Quick Sight subscription was
        first created in this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_account_settings)
        """

    def describe_account_subscription(
        self, **kwargs: Unpack[DescribeAccountSubscriptionRequestTypeDef]
    ) -> DescribeAccountSubscriptionResponseTypeDef:
        """
        Use the DescribeAccountSubscription operation to receive a description of an
        Quick Sight account's subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_account_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_account_subscription)
        """

    def describe_action_connector(
        self, **kwargs: Unpack[DescribeActionConnectorRequestTypeDef]
    ) -> DescribeActionConnectorResponseTypeDef:
        """
        Retrieves detailed information about an action connector, including its
        configuration, authentication settings, enabled actions, and current status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_action_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_action_connector)
        """

    def describe_action_connector_permissions(
        self, **kwargs: Unpack[DescribeActionConnectorPermissionsRequestTypeDef]
    ) -> DescribeActionConnectorPermissionsResponseTypeDef:
        """
        Retrieves the permissions configuration for an action connector, showing which
        users, groups, and namespaces have access and what operations they can perform.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_action_connector_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_action_connector_permissions)
        """

    def describe_agent(
        self, **kwargs: Unpack[DescribeAgentRequestTypeDef]
    ) -> DescribeAgentResponseTypeDef:
        """
        Describes an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_agent)
        """

    def describe_agent_permissions(
        self, **kwargs: Unpack[DescribeAgentPermissionsRequestTypeDef]
    ) -> DescribeAgentPermissionsResponseTypeDef:
        """
        Describes the resource permissions for an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_agent_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_agent_permissions)
        """

    def describe_analysis(
        self, **kwargs: Unpack[DescribeAnalysisRequestTypeDef]
    ) -> DescribeAnalysisResponseTypeDef:
        """
        Provides a summary of the metadata for an analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_analysis.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_analysis)
        """

    def describe_analysis_definition(
        self, **kwargs: Unpack[DescribeAnalysisDefinitionRequestTypeDef]
    ) -> DescribeAnalysisDefinitionResponseTypeDef:
        """
        Provides a detailed description of the definition of an analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_analysis_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_analysis_definition)
        """

    def describe_analysis_permissions(
        self, **kwargs: Unpack[DescribeAnalysisPermissionsRequestTypeDef]
    ) -> DescribeAnalysisPermissionsResponseTypeDef:
        """
        Provides the read and write permissions for an analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_analysis_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_analysis_permissions)
        """

    def describe_approval_policy(
        self, **kwargs: Unpack[DescribeApprovalPolicyRequestTypeDef]
    ) -> DescribeApprovalPolicyResponseTypeDef:
        """
        Describes an approval policy in Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_approval_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_approval_policy)
        """

    def describe_asset_bundle_export_job(
        self, **kwargs: Unpack[DescribeAssetBundleExportJobRequestTypeDef]
    ) -> DescribeAssetBundleExportJobResponseTypeDef:
        """
        Describes an existing export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_asset_bundle_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_asset_bundle_export_job)
        """

    def describe_asset_bundle_import_job(
        self, **kwargs: Unpack[DescribeAssetBundleImportJobRequestTypeDef]
    ) -> DescribeAssetBundleImportJobResponseTypeDef:
        """
        Describes an existing import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_asset_bundle_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_asset_bundle_import_job)
        """

    def describe_automation_job(
        self, **kwargs: Unpack[DescribeAutomationJobRequestTypeDef]
    ) -> DescribeAutomationJobResponseTypeDef:
        """
        Retrieves the status and details of a specified automation job, including its
        status and outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_automation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_automation_job)
        """

    def describe_brand(
        self, **kwargs: Unpack[DescribeBrandRequestTypeDef]
    ) -> DescribeBrandResponseTypeDef:
        """
        Describes a brand.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_brand.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_brand)
        """

    def describe_brand_assignment(
        self, **kwargs: Unpack[DescribeBrandAssignmentRequestTypeDef]
    ) -> DescribeBrandAssignmentResponseTypeDef:
        """
        Describes a brand assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_brand_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_brand_assignment)
        """

    def describe_brand_published_version(
        self, **kwargs: Unpack[DescribeBrandPublishedVersionRequestTypeDef]
    ) -> DescribeBrandPublishedVersionResponseTypeDef:
        """
        Describes the published version of the brand.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_brand_published_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_brand_published_version)
        """

    def describe_custom_permissions(
        self, **kwargs: Unpack[DescribeCustomPermissionsRequestTypeDef]
    ) -> DescribeCustomPermissionsResponseTypeDef:
        """
        Describes a custom permissions profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_custom_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_custom_permissions)
        """

    def describe_dashboard(
        self, **kwargs: Unpack[DescribeDashboardRequestTypeDef]
    ) -> DescribeDashboardResponseTypeDef:
        """
        Provides a summary for a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_dashboard.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_dashboard)
        """

    def describe_dashboard_definition(
        self, **kwargs: Unpack[DescribeDashboardDefinitionRequestTypeDef]
    ) -> DescribeDashboardDefinitionResponseTypeDef:
        """
        Provides a detailed description of the definition of a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_dashboard_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_dashboard_definition)
        """

    def describe_dashboard_permissions(
        self, **kwargs: Unpack[DescribeDashboardPermissionsRequestTypeDef]
    ) -> DescribeDashboardPermissionsResponseTypeDef:
        """
        Describes read and write permissions for a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_dashboard_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_dashboard_permissions)
        """

    def describe_dashboard_snapshot_job(
        self, **kwargs: Unpack[DescribeDashboardSnapshotJobRequestTypeDef]
    ) -> DescribeDashboardSnapshotJobResponseTypeDef:
        """
        Describes an existing snapshot job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_dashboard_snapshot_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_dashboard_snapshot_job)
        """

    def describe_dashboard_snapshot_job_result(
        self, **kwargs: Unpack[DescribeDashboardSnapshotJobResultRequestTypeDef]
    ) -> DescribeDashboardSnapshotJobResultResponseTypeDef:
        """
        Describes the result of an existing snapshot job that has finished running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_dashboard_snapshot_job_result.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_dashboard_snapshot_job_result)
        """

    def describe_dashboards_qa_configuration(
        self, **kwargs: Unpack[DescribeDashboardsQAConfigurationRequestTypeDef]
    ) -> DescribeDashboardsQAConfigurationResponseTypeDef:
        """
        Describes an existing dashboard QA configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_dashboards_qa_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_dashboards_qa_configuration)
        """

    def describe_data_set(
        self, **kwargs: Unpack[DescribeDataSetRequestTypeDef]
    ) -> DescribeDataSetResponseTypeDef:
        """
        Describes a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_data_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_data_set)
        """

    def describe_data_set_permissions(
        self, **kwargs: Unpack[DescribeDataSetPermissionsRequestTypeDef]
    ) -> DescribeDataSetPermissionsResponseTypeDef:
        """
        Describes the permissions on a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_data_set_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_data_set_permissions)
        """

    def describe_data_set_refresh_properties(
        self, **kwargs: Unpack[DescribeDataSetRefreshPropertiesRequestTypeDef]
    ) -> DescribeDataSetRefreshPropertiesResponseTypeDef:
        """
        Describes the refresh properties of a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_data_set_refresh_properties.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_data_set_refresh_properties)
        """

    def describe_data_source(
        self, **kwargs: Unpack[DescribeDataSourceRequestTypeDef]
    ) -> DescribeDataSourceResponseTypeDef:
        """
        Describes a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_data_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_data_source)
        """

    def describe_data_source_permissions(
        self, **kwargs: Unpack[DescribeDataSourcePermissionsRequestTypeDef]
    ) -> DescribeDataSourcePermissionsResponseTypeDef:
        """
        Describes the resource permissions for a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_data_source_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_data_source_permissions)
        """

    def describe_default_q_business_application(
        self, **kwargs: Unpack[DescribeDefaultQBusinessApplicationRequestTypeDef]
    ) -> DescribeDefaultQBusinessApplicationResponseTypeDef:
        """
        Describes a Amazon Q Business application that is linked to an Quick Sight
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_default_q_business_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_default_q_business_application)
        """

    def describe_dlp_setting(
        self, **kwargs: Unpack[DescribeDlpSettingRequestTypeDef]
    ) -> DescribeDlpSettingResponseTypeDef:
        """
        Describes the full configuration of a DLP setting in an Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_dlp_setting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_dlp_setting)
        """

    def describe_flow(
        self, **kwargs: Unpack[DescribeFlowRequestTypeDef]
    ) -> DescribeFlowResponseTypeDef:
        """
        Returns the full details of a flow for the latest version of the requested
        publish state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_flow)
        """

    def describe_folder(
        self, **kwargs: Unpack[DescribeFolderRequestTypeDef]
    ) -> DescribeFolderResponseTypeDef:
        """
        Describes a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_folder.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_folder)
        """

    def describe_folder_permissions(
        self, **kwargs: Unpack[DescribeFolderPermissionsRequestTypeDef]
    ) -> DescribeFolderPermissionsResponseTypeDef:
        """
        Describes permissions for a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_folder_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_folder_permissions)
        """

    def describe_folder_resolved_permissions(
        self, **kwargs: Unpack[DescribeFolderResolvedPermissionsRequestTypeDef]
    ) -> DescribeFolderResolvedPermissionsResponseTypeDef:
        """
        Describes the folder resolved permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_folder_resolved_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_folder_resolved_permissions)
        """

    def describe_group(
        self, **kwargs: Unpack[DescribeGroupRequestTypeDef]
    ) -> DescribeGroupResponseTypeDef:
        """
        Returns an Amazon Quick Sight group's description and Amazon Resource Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_group)
        """

    def describe_group_membership(
        self, **kwargs: Unpack[DescribeGroupMembershipRequestTypeDef]
    ) -> DescribeGroupMembershipResponseTypeDef:
        """
        Use the <code>DescribeGroupMembership</code> operation to determine if a user
        is a member of the specified group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_group_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_group_membership)
        """

    def describe_iam_policy_assignment(
        self, **kwargs: Unpack[DescribeIAMPolicyAssignmentRequestTypeDef]
    ) -> DescribeIAMPolicyAssignmentResponseTypeDef:
        """
        Describes an existing IAM policy assignment, as specified by the assignment
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_iam_policy_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_iam_policy_assignment)
        """

    def describe_ingestion(
        self, **kwargs: Unpack[DescribeIngestionRequestTypeDef]
    ) -> DescribeIngestionResponseTypeDef:
        """
        Describes a SPICE ingestion.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_ingestion.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_ingestion)
        """

    def describe_ip_restriction(
        self, **kwargs: Unpack[DescribeIpRestrictionRequestTypeDef]
    ) -> DescribeIpRestrictionResponseTypeDef:
        """
        Provides a summary and status of IP rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_ip_restriction.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_ip_restriction)
        """

    def describe_key_registration(
        self, **kwargs: Unpack[DescribeKeyRegistrationRequestTypeDef]
    ) -> DescribeKeyRegistrationResponseTypeDef:
        """
        Describes all customer managed key registrations in a Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_key_registration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_key_registration)
        """

    def describe_knowledge_base(
        self, **kwargs: Unpack[DescribeKnowledgeBaseRequestTypeDef]
    ) -> DescribeKnowledgeBaseResponseTypeDef:
        """
        Describes a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_knowledge_base.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_knowledge_base)
        """

    def describe_knowledge_base_permissions(
        self, **kwargs: Unpack[DescribeKnowledgeBasePermissionsRequestTypeDef]
    ) -> DescribeKnowledgeBasePermissionsResponseTypeDef:
        """
        Describes the resource permissions for a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_knowledge_base_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_knowledge_base_permissions)
        """

    def describe_limits_profile(
        self, **kwargs: Unpack[DescribeLimitsProfileRequestTypeDef]
    ) -> DescribeLimitsProfileResponseTypeDef:
        """
        Describes the properties of an existing limits profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_limits_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_limits_profile)
        """

    def describe_namespace(
        self, **kwargs: Unpack[DescribeNamespaceRequestTypeDef]
    ) -> DescribeNamespaceResponseTypeDef:
        """
        Describes the current namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_namespace)
        """

    def describe_o_auth_client_application(
        self, **kwargs: Unpack[DescribeOAuthClientApplicationRequestTypeDef]
    ) -> DescribeOAuthClientApplicationResponseTypeDef:
        """
        Describes an OAuthClientApplication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_o_auth_client_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_o_auth_client_application)
        """

    def describe_q_personalization_configuration(
        self, **kwargs: Unpack[DescribeQPersonalizationConfigurationRequestTypeDef]
    ) -> DescribeQPersonalizationConfigurationResponseTypeDef:
        """
        Describes a personalization configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_q_personalization_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_q_personalization_configuration)
        """

    def describe_quick_sight_q_search_configuration(
        self, **kwargs: Unpack[DescribeQuickSightQSearchConfigurationRequestTypeDef]
    ) -> DescribeQuickSightQSearchConfigurationResponseTypeDef:
        """
        Describes the state of a Quick Sight Q Search configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_quick_sight_q_search_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_quick_sight_q_search_configuration)
        """

    def describe_refresh_schedule(
        self, **kwargs: Unpack[DescribeRefreshScheduleRequestTypeDef]
    ) -> DescribeRefreshScheduleResponseTypeDef:
        """
        Provides a summary of a refresh schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_refresh_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_refresh_schedule)
        """

    def describe_role_custom_permission(
        self, **kwargs: Unpack[DescribeRoleCustomPermissionRequestTypeDef]
    ) -> DescribeRoleCustomPermissionResponseTypeDef:
        """
        Describes all custom permissions that are mapped to a role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_role_custom_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_role_custom_permission)
        """

    def describe_self_upgrade_configuration(
        self, **kwargs: Unpack[DescribeSelfUpgradeConfigurationRequestTypeDef]
    ) -> DescribeSelfUpgradeConfigurationResponseTypeDef:
        """
        Describes the self-upgrade configuration for a Quick account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_self_upgrade_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_self_upgrade_configuration)
        """

    def describe_space(
        self, **kwargs: Unpack[DescribeSpaceRequestTypeDef]
    ) -> DescribeSpaceResponseTypeDef:
        """
        Describes an Amazon QuickSight space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_space)
        """

    def describe_space_permissions(
        self, **kwargs: Unpack[DescribeSpacePermissionsRequestTypeDef]
    ) -> DescribeSpacePermissionsResponseTypeDef:
        """
        Describes the permissions for an Amazon QuickSight space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_space_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_space_permissions)
        """

    def describe_template(
        self, **kwargs: Unpack[DescribeTemplateRequestTypeDef]
    ) -> DescribeTemplateResponseTypeDef:
        """
        Describes a template's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_template)
        """

    def describe_template_alias(
        self, **kwargs: Unpack[DescribeTemplateAliasRequestTypeDef]
    ) -> DescribeTemplateAliasResponseTypeDef:
        """
        Describes the template alias for a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_template_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_template_alias)
        """

    def describe_template_definition(
        self, **kwargs: Unpack[DescribeTemplateDefinitionRequestTypeDef]
    ) -> DescribeTemplateDefinitionResponseTypeDef:
        """
        Provides a detailed description of the definition of a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_template_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_template_definition)
        """

    def describe_template_permissions(
        self, **kwargs: Unpack[DescribeTemplatePermissionsRequestTypeDef]
    ) -> DescribeTemplatePermissionsResponseTypeDef:
        """
        Describes read and write permissions on a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_template_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_template_permissions)
        """

    def describe_theme(
        self, **kwargs: Unpack[DescribeThemeRequestTypeDef]
    ) -> DescribeThemeResponseTypeDef:
        """
        Describes a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_theme.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_theme)
        """

    def describe_theme_alias(
        self, **kwargs: Unpack[DescribeThemeAliasRequestTypeDef]
    ) -> DescribeThemeAliasResponseTypeDef:
        """
        Describes the alias for a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_theme_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_theme_alias)
        """

    def describe_theme_permissions(
        self, **kwargs: Unpack[DescribeThemePermissionsRequestTypeDef]
    ) -> DescribeThemePermissionsResponseTypeDef:
        """
        Describes the read and write permissions for a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_theme_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_theme_permissions)
        """

    def describe_topic(
        self, **kwargs: Unpack[DescribeTopicRequestTypeDef]
    ) -> DescribeTopicResponseTypeDef:
        """
        Describes a topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_topic.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_topic)
        """

    def describe_topic_permissions(
        self, **kwargs: Unpack[DescribeTopicPermissionsRequestTypeDef]
    ) -> DescribeTopicPermissionsResponseTypeDef:
        """
        Describes the permissions of a topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_topic_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_topic_permissions)
        """

    def describe_topic_permissions_v2(
        self, **kwargs: Unpack[DescribeTopicPermissionsV2RequestTypeDef]
    ) -> DescribeTopicPermissionsV2ResponseTypeDef:
        """
        Describes the permissions of a topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_topic_permissions_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_topic_permissions_v2)
        """

    def describe_topic_refresh(
        self, **kwargs: Unpack[DescribeTopicRefreshRequestTypeDef]
    ) -> DescribeTopicRefreshResponseTypeDef:
        """
        Describes the status of a topic refresh.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_topic_refresh.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_topic_refresh)
        """

    def describe_topic_refresh_schedule(
        self, **kwargs: Unpack[DescribeTopicRefreshScheduleRequestTypeDef]
    ) -> DescribeTopicRefreshScheduleResponseTypeDef:
        """
        Deletes a topic refresh schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_topic_refresh_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_topic_refresh_schedule)
        """

    def describe_topic_v2(
        self, **kwargs: Unpack[DescribeTopicV2RequestTypeDef]
    ) -> DescribeTopicV2ResponseTypeDef:
        """
        Describes a Q topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_topic_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_topic_v2)
        """

    def describe_user(
        self, **kwargs: Unpack[DescribeUserRequestTypeDef]
    ) -> DescribeUserResponseTypeDef:
        """
        Returns information about a user, given the user name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_user)
        """

    def describe_vpc_connection(
        self, **kwargs: Unpack[DescribeVPCConnectionRequestTypeDef]
    ) -> DescribeVPCConnectionResponseTypeDef:
        """
        Describes a VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_vpc_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_vpc_connection)
        """

    def generate_embed_url_for_anonymous_user(
        self, **kwargs: Unpack[GenerateEmbedUrlForAnonymousUserRequestTypeDef]
    ) -> GenerateEmbedUrlForAnonymousUserResponseTypeDef:
        """
        Generates an embed URL that you can use to embed an Amazon Quick dashboard or
        visual in your website, without having to register any reader users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/generate_embed_url_for_anonymous_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#generate_embed_url_for_anonymous_user)
        """

    def generate_embed_url_for_registered_user(
        self, **kwargs: Unpack[GenerateEmbedUrlForRegisteredUserRequestTypeDef]
    ) -> GenerateEmbedUrlForRegisteredUserResponseTypeDef:
        """
        Generates an embed URL that you can use to embed an Amazon Quick experience in
        your website.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/generate_embed_url_for_registered_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#generate_embed_url_for_registered_user)
        """

    def generate_embed_url_for_registered_user_with_identity(
        self, **kwargs: Unpack[GenerateEmbedUrlForRegisteredUserWithIdentityRequestTypeDef]
    ) -> GenerateEmbedUrlForRegisteredUserWithIdentityResponseTypeDef:
        """
        Generates an embed URL that you can use to embed an Amazon Quick Sight
        experience in your website.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/generate_embed_url_for_registered_user_with_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#generate_embed_url_for_registered_user_with_identity)
        """

    def get_dashboard_embed_url(
        self, **kwargs: Unpack[GetDashboardEmbedUrlRequestTypeDef]
    ) -> GetDashboardEmbedUrlResponseTypeDef:
        """
        Generates a temporary session URL and authorization code(bearer token) that you
        can use to embed an Amazon Quick Sight read-only dashboard in your website or
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_dashboard_embed_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_dashboard_embed_url)
        """

    def get_flow_metadata(
        self, **kwargs: Unpack[GetFlowMetadataInputTypeDef]
    ) -> GetFlowMetadataOutputTypeDef:
        """
        Retrieves the metadata of a flow, not including its definition specifying the
        steps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_flow_metadata.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_flow_metadata)
        """

    def get_flow_permissions(
        self, **kwargs: Unpack[GetFlowPermissionsInputTypeDef]
    ) -> GetFlowPermissionsOutputTypeDef:
        """
        Get permissions for a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_flow_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_flow_permissions)
        """

    def get_identity_context(
        self, **kwargs: Unpack[GetIdentityContextRequestTypeDef]
    ) -> GetIdentityContextResponseTypeDef:
        """
        Retrieves the identity context for a Quick Sight user in a specified namespace,
        allowing you to obtain identity tokens that can be used with identity-enhanced
        IAM role sessions to call identity-aware APIs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_identity_context.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_identity_context)
        """

    def get_session_embed_url(
        self, **kwargs: Unpack[GetSessionEmbedUrlRequestTypeDef]
    ) -> GetSessionEmbedUrlResponseTypeDef:
        """
        Generates a session URL and authorization code that you can use to embed the
        Amazon Amazon Quick Sight console in your web server code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_session_embed_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_session_embed_url)
        """

    def list_action_connectors(
        self, **kwargs: Unpack[ListActionConnectorsRequestTypeDef]
    ) -> ListActionConnectorsResponseTypeDef:
        """
        Lists all action connectors in the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_action_connectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_action_connectors)
        """

    def list_agents(self, **kwargs: Unpack[ListAgentsRequestTypeDef]) -> ListAgentsResponseTypeDef:
        """
        Lists all agents in an Amazon QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_agents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_agents)
        """

    def list_analyses(
        self, **kwargs: Unpack[ListAnalysesRequestTypeDef]
    ) -> ListAnalysesResponseTypeDef:
        """
        Lists Amazon Quick Sight analyses that exist in the specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_analyses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_analyses)
        """

    def list_approval_policies(
        self, **kwargs: Unpack[ListApprovalPoliciesRequestTypeDef]
    ) -> ListApprovalPoliciesResponseTypeDef:
        """
        Lists all approval policies in the specified Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_approval_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_approval_policies)
        """

    def list_asset_bundle_export_jobs(
        self, **kwargs: Unpack[ListAssetBundleExportJobsRequestTypeDef]
    ) -> ListAssetBundleExportJobsResponseTypeDef:
        """
        Lists all asset bundle export jobs that have been taken place in the last 14
        days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_asset_bundle_export_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_asset_bundle_export_jobs)
        """

    def list_asset_bundle_import_jobs(
        self, **kwargs: Unpack[ListAssetBundleImportJobsRequestTypeDef]
    ) -> ListAssetBundleImportJobsResponseTypeDef:
        """
        Lists all asset bundle import jobs that have taken place in the last 14 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_asset_bundle_import_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_asset_bundle_import_jobs)
        """

    def list_brands(self, **kwargs: Unpack[ListBrandsRequestTypeDef]) -> ListBrandsResponseTypeDef:
        """
        Lists all brands in an Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_brands.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_brands)
        """

    def list_custom_permissions(
        self, **kwargs: Unpack[ListCustomPermissionsRequestTypeDef]
    ) -> ListCustomPermissionsResponseTypeDef:
        """
        Returns a list of all the custom permissions profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_custom_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_custom_permissions)
        """

    def list_dashboard_versions(
        self, **kwargs: Unpack[ListDashboardVersionsRequestTypeDef]
    ) -> ListDashboardVersionsResponseTypeDef:
        """
        Lists all the versions of the dashboards in the Amazon Quick Sight subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_dashboard_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_dashboard_versions)
        """

    def list_dashboards(
        self, **kwargs: Unpack[ListDashboardsRequestTypeDef]
    ) -> ListDashboardsResponseTypeDef:
        """
        Lists dashboards in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_dashboards.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_dashboards)
        """

    def list_data_sets(
        self, **kwargs: Unpack[ListDataSetsRequestTypeDef]
    ) -> ListDataSetsResponseTypeDef:
        """
        Lists all of the datasets belonging to the current Amazon Web Services account
        in an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_data_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_data_sets)
        """

    def list_data_sources(
        self, **kwargs: Unpack[ListDataSourcesRequestTypeDef]
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists data sources in current Amazon Web Services Region that belong to this
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_data_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_data_sources)
        """

    def list_dlp_settings(
        self, **kwargs: Unpack[ListDlpSettingsRequestTypeDef]
    ) -> ListDlpSettingsResponseTypeDef:
        """
        Lists all DLP settings in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_dlp_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_dlp_settings)
        """

    def list_flows(self, **kwargs: Unpack[ListFlowsInputTypeDef]) -> ListFlowsOutputTypeDef:
        """
        Lists flows in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_flows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_flows)
        """

    def list_folder_members(
        self, **kwargs: Unpack[ListFolderMembersRequestTypeDef]
    ) -> ListFolderMembersResponseTypeDef:
        """
        List all assets (<code>DASHBOARD</code>, <code>ANALYSIS</code>, and
        <code>DATASET</code>) in a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_folder_members.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_folder_members)
        """

    def list_folders(
        self, **kwargs: Unpack[ListFoldersRequestTypeDef]
    ) -> ListFoldersResponseTypeDef:
        """
        Lists all folders in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_folders.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_folders)
        """

    def list_folders_for_resource(
        self, **kwargs: Unpack[ListFoldersForResourceRequestTypeDef]
    ) -> ListFoldersForResourceResponseTypeDef:
        """
        List all folders that a resource is a member of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_folders_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_folders_for_resource)
        """

    def list_group_memberships(
        self, **kwargs: Unpack[ListGroupMembershipsRequestTypeDef]
    ) -> ListGroupMembershipsResponseTypeDef:
        """
        Lists member users in a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_group_memberships.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_group_memberships)
        """

    def list_groups(self, **kwargs: Unpack[ListGroupsRequestTypeDef]) -> ListGroupsResponseTypeDef:
        """
        Lists all user groups in Amazon Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_groups)
        """

    def list_iam_policy_assignments(
        self, **kwargs: Unpack[ListIAMPolicyAssignmentsRequestTypeDef]
    ) -> ListIAMPolicyAssignmentsResponseTypeDef:
        """
        Lists the IAM policy assignments in the current Amazon Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_iam_policy_assignments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_iam_policy_assignments)
        """

    def list_iam_policy_assignments_for_user(
        self, **kwargs: Unpack[ListIAMPolicyAssignmentsForUserRequestTypeDef]
    ) -> ListIAMPolicyAssignmentsForUserResponseTypeDef:
        """
        Lists all of the IAM policy assignments, including the Amazon Resource Names
        (ARNs), for the IAM policies assigned to the specified user and group, or
        groups that the user belongs to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_iam_policy_assignments_for_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_iam_policy_assignments_for_user)
        """

    def list_identity_propagation_configs(
        self, **kwargs: Unpack[ListIdentityPropagationConfigsRequestTypeDef]
    ) -> ListIdentityPropagationConfigsResponseTypeDef:
        """
        Lists all services and authorized targets that the Quick Sight IAM Identity
        Center application can access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_identity_propagation_configs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_identity_propagation_configs)
        """

    def list_ingestions(
        self, **kwargs: Unpack[ListIngestionsRequestTypeDef]
    ) -> ListIngestionsResponseTypeDef:
        """
        Lists the history of SPICE ingestions for a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_ingestions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_ingestions)
        """

    def list_knowledge_bases(
        self, **kwargs: Unpack[ListKnowledgeBasesRequestTypeDef]
    ) -> ListKnowledgeBasesResponseTypeDef:
        """
        Lists all knowledge bases in an Amazon QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_knowledge_bases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_knowledge_bases)
        """

    def list_limits_profiles(
        self, **kwargs: Unpack[ListLimitsProfilesRequestTypeDef]
    ) -> ListLimitsProfilesResponseTypeDef:
        """
        Lists all limits profiles in an Amazon Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_limits_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_limits_profiles)
        """

    def list_namespaces(
        self, **kwargs: Unpack[ListNamespacesRequestTypeDef]
    ) -> ListNamespacesResponseTypeDef:
        """
        Lists the namespaces for the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_namespaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_namespaces)
        """

    def list_o_auth_client_applications(
        self, **kwargs: Unpack[ListOAuthClientApplicationsRequestTypeDef]
    ) -> ListOAuthClientApplicationsResponseTypeDef:
        """
        Lists all OAuthClientApplications in the current Amazon Web Services Region
        that belong to this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_o_auth_client_applications.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_o_auth_client_applications)
        """

    def list_refresh_schedules(
        self, **kwargs: Unpack[ListRefreshSchedulesRequestTypeDef]
    ) -> ListRefreshSchedulesResponseTypeDef:
        """
        Lists the refresh schedules of a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_refresh_schedules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_refresh_schedules)
        """

    def list_role_memberships(
        self, **kwargs: Unpack[ListRoleMembershipsRequestTypeDef]
    ) -> ListRoleMembershipsResponseTypeDef:
        """
        Lists all groups that are associated with a role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_role_memberships.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_role_memberships)
        """

    def list_self_upgrades(
        self, **kwargs: Unpack[ListSelfUpgradesRequestTypeDef]
    ) -> ListSelfUpgradesResponseTypeDef:
        """
        Lists all self-upgrade requests for a Quick account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_self_upgrades.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_self_upgrades)
        """

    def list_space_resources(
        self, **kwargs: Unpack[ListSpaceResourcesRequestTypeDef]
    ) -> ListSpaceResourcesResponseTypeDef:
        """
        Lists the resources in an Amazon QuickSight space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_space_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_space_resources)
        """

    def list_spaces(self, **kwargs: Unpack[ListSpacesRequestTypeDef]) -> ListSpacesResponseTypeDef:
        """
        Lists all Amazon QuickSight spaces in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_spaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_spaces)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags assigned to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_tags_for_resource)
        """

    def list_template_aliases(
        self, **kwargs: Unpack[ListTemplateAliasesRequestTypeDef]
    ) -> ListTemplateAliasesResponseTypeDef:
        """
        Lists all the aliases of a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_template_aliases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_template_aliases)
        """

    def list_template_versions(
        self, **kwargs: Unpack[ListTemplateVersionsRequestTypeDef]
    ) -> ListTemplateVersionsResponseTypeDef:
        """
        Lists all the versions of the templates in the current Amazon Quick Sight
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_template_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_template_versions)
        """

    def list_templates(
        self, **kwargs: Unpack[ListTemplatesRequestTypeDef]
    ) -> ListTemplatesResponseTypeDef:
        """
        Lists all the templates in the current Amazon Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_templates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_templates)
        """

    def list_theme_aliases(
        self, **kwargs: Unpack[ListThemeAliasesRequestTypeDef]
    ) -> ListThemeAliasesResponseTypeDef:
        """
        Lists all the aliases of a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_theme_aliases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_theme_aliases)
        """

    def list_theme_versions(
        self, **kwargs: Unpack[ListThemeVersionsRequestTypeDef]
    ) -> ListThemeVersionsResponseTypeDef:
        """
        Lists all the versions of the themes in the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_theme_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_theme_versions)
        """

    def list_themes(self, **kwargs: Unpack[ListThemesRequestTypeDef]) -> ListThemesResponseTypeDef:
        """
        Lists all the themes in the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_themes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_themes)
        """

    def list_topic_refresh_schedules(
        self, **kwargs: Unpack[ListTopicRefreshSchedulesRequestTypeDef]
    ) -> ListTopicRefreshSchedulesResponseTypeDef:
        """
        Lists all of the refresh schedules for a topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_topic_refresh_schedules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_topic_refresh_schedules)
        """

    def list_topic_reviewed_answers(
        self, **kwargs: Unpack[ListTopicReviewedAnswersRequestTypeDef]
    ) -> ListTopicReviewedAnswersResponseTypeDef:
        """
        Lists all reviewed answers for a Q Topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_topic_reviewed_answers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_topic_reviewed_answers)
        """

    def list_topics(self, **kwargs: Unpack[ListTopicsRequestTypeDef]) -> ListTopicsResponseTypeDef:
        """
        Lists all of the topics within an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_topics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_topics)
        """

    def list_topics_v2(
        self, **kwargs: Unpack[ListTopicsV2RequestTypeDef]
    ) -> ListTopicsV2ResponseTypeDef:
        """
        Lists all of the Q topics in the specified Amazon Web Services account in an
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_topics_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_topics_v2)
        """

    def list_user_groups(
        self, **kwargs: Unpack[ListUserGroupsRequestTypeDef]
    ) -> ListUserGroupsResponseTypeDef:
        """
        Lists the Amazon Quick Sight groups that an Amazon Quick Sight user is a member
        of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_user_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_user_groups)
        """

    def list_users(self, **kwargs: Unpack[ListUsersRequestTypeDef]) -> ListUsersResponseTypeDef:
        """
        Returns a list of all of the Amazon Quick Sight users belonging to this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_users)
        """

    def list_users_index_capacity(
        self, **kwargs: Unpack[ListUsersIndexCapacityRequestTypeDef]
    ) -> ListUsersIndexCapacityResponseTypeDef:
        """
        Lists per-user index capacity consumption for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_users_index_capacity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_users_index_capacity)
        """

    def list_vpc_connections(
        self, **kwargs: Unpack[ListVPCConnectionsRequestTypeDef]
    ) -> ListVPCConnectionsResponseTypeDef:
        """
        Lists all of the VPC connections in the current set Amazon Web Services Region
        of an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_vpc_connections.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_vpc_connections)
        """

    def predict_qa_results(
        self, **kwargs: Unpack[PredictQAResultsRequestTypeDef]
    ) -> PredictQAResultsResponseTypeDef:
        """
        Predicts existing visuals or generates new visuals to answer a given query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/predict_qa_results.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#predict_qa_results)
        """

    def put_data_set_refresh_properties(
        self, **kwargs: Unpack[PutDataSetRefreshPropertiesRequestTypeDef]
    ) -> PutDataSetRefreshPropertiesResponseTypeDef:
        """
        Creates or updates the dataset refresh properties for the dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/put_data_set_refresh_properties.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#put_data_set_refresh_properties)
        """

    def register_user(
        self, **kwargs: Unpack[RegisterUserRequestTypeDef]
    ) -> RegisterUserResponseTypeDef:
        """
        Creates an Amazon Quick Sight user whose identity is associated with the
        Identity and Access Management (IAM) identity or role specified in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/register_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#register_user)
        """

    def restore_analysis(
        self, **kwargs: Unpack[RestoreAnalysisRequestTypeDef]
    ) -> RestoreAnalysisResponseTypeDef:
        """
        Restores an analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/restore_analysis.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#restore_analysis)
        """

    def search_action_connectors(
        self, **kwargs: Unpack[SearchActionConnectorsRequestTypeDef]
    ) -> SearchActionConnectorsResponseTypeDef:
        """
        Searches for action connectors in the specified Amazon Web Services account
        using filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_action_connectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_action_connectors)
        """

    def search_agents(
        self, **kwargs: Unpack[SearchAgentsRequestTypeDef]
    ) -> SearchAgentsResponseTypeDef:
        """
        Searches for agents based on specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_agents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_agents)
        """

    def search_analyses(
        self, **kwargs: Unpack[SearchAnalysesRequestTypeDef]
    ) -> SearchAnalysesResponseTypeDef:
        """
        Searches for analyses that belong to the user specified in the filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_analyses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_analyses)
        """

    def search_dashboards(
        self, **kwargs: Unpack[SearchDashboardsRequestTypeDef]
    ) -> SearchDashboardsResponseTypeDef:
        """
        Searches for dashboards that belong to a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_dashboards.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_dashboards)
        """

    def search_data_sets(
        self, **kwargs: Unpack[SearchDataSetsRequestTypeDef]
    ) -> SearchDataSetsResponseTypeDef:
        """
        Use the <code>SearchDataSets</code> operation to search for datasets that
        belong to an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_data_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_data_sets)
        """

    def search_data_sources(
        self, **kwargs: Unpack[SearchDataSourcesRequestTypeDef]
    ) -> SearchDataSourcesResponseTypeDef:
        """
        Use the <code>SearchDataSources</code> operation to search for data sources
        that belong to an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_data_sources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_data_sources)
        """

    def search_flows(self, **kwargs: Unpack[SearchFlowsInputTypeDef]) -> SearchFlowsOutputTypeDef:
        """
        Search for the flows in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_flows.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_flows)
        """

    def search_folders(
        self, **kwargs: Unpack[SearchFoldersRequestTypeDef]
    ) -> SearchFoldersResponseTypeDef:
        """
        Searches the subfolders in a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_folders.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_folders)
        """

    def search_groups(
        self, **kwargs: Unpack[SearchGroupsRequestTypeDef]
    ) -> SearchGroupsResponseTypeDef:
        """
        Use the <code>SearchGroups</code> operation to search groups in a specified
        Quick Sight namespace using the supplied filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_groups)
        """

    def search_knowledge_bases(
        self, **kwargs: Unpack[SearchKnowledgeBasesRequestTypeDef]
    ) -> SearchKnowledgeBasesResponseTypeDef:
        """
        Searches for a subset of knowledge bases based on specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_knowledge_bases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_knowledge_bases)
        """

    def search_spaces(
        self, **kwargs: Unpack[SearchSpacesRequestTypeDef]
    ) -> SearchSpacesResponseTypeDef:
        """
        Searches for Amazon QuickSight spaces that match the specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_spaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_spaces)
        """

    def search_topics(
        self, **kwargs: Unpack[SearchTopicsRequestTypeDef]
    ) -> SearchTopicsResponseTypeDef:
        """
        Searches for any Q topic that exists in an Quick account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_topics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_topics)
        """

    def search_topics_v2(
        self, **kwargs: Unpack[SearchTopicsV2RequestTypeDef]
    ) -> SearchTopicsV2ResponseTypeDef:
        """
        Searches for any Q topic that exists in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_topics_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_topics_v2)
        """

    def start_asset_bundle_export_job(
        self, **kwargs: Unpack[StartAssetBundleExportJobRequestTypeDef]
    ) -> StartAssetBundleExportJobResponseTypeDef:
        """
        Starts an Asset Bundle export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/start_asset_bundle_export_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#start_asset_bundle_export_job)
        """

    def start_asset_bundle_import_job(
        self, **kwargs: Unpack[StartAssetBundleImportJobRequestTypeDef]
    ) -> StartAssetBundleImportJobResponseTypeDef:
        """
        Starts an Asset Bundle import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/start_asset_bundle_import_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#start_asset_bundle_import_job)
        """

    def start_automation_job(
        self, **kwargs: Unpack[StartAutomationJobRequestTypeDef]
    ) -> StartAutomationJobResponseTypeDef:
        """
        Starts a new job for a specified automation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/start_automation_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#start_automation_job)
        """

    def start_dashboard_snapshot_job(
        self, **kwargs: Unpack[StartDashboardSnapshotJobRequestTypeDef]
    ) -> StartDashboardSnapshotJobResponseTypeDef:
        """
        Starts an asynchronous job that generates a snapshot of a dashboard's output.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/start_dashboard_snapshot_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#start_dashboard_snapshot_job)
        """

    def start_dashboard_snapshot_job_schedule(
        self, **kwargs: Unpack[StartDashboardSnapshotJobScheduleRequestTypeDef]
    ) -> StartDashboardSnapshotJobScheduleResponseTypeDef:
        """
        Starts an asynchronous job that runs an existing dashboard schedule and sends
        the dashboard snapshot through email.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/start_dashboard_snapshot_job_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#start_dashboard_snapshot_job_schedule)
        """

    def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> TagResourceResponseTypeDef:
        """
        Assigns one or more tags (key-value pairs) to the specified Amazon Quick Sight
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> UntagResourceResponseTypeDef:
        """
        Removes a tag or tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#untag_resource)
        """

    def update_account_custom_permission(
        self, **kwargs: Unpack[UpdateAccountCustomPermissionRequestTypeDef]
    ) -> UpdateAccountCustomPermissionResponseTypeDef:
        """
        Applies a custom permissions profile to an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_account_custom_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_account_custom_permission)
        """

    def update_account_customization(
        self, **kwargs: Unpack[UpdateAccountCustomizationRequestTypeDef]
    ) -> UpdateAccountCustomizationResponseTypeDef:
        """
        Updates Amazon Quick Sight customizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_account_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_account_customization)
        """

    def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsRequestTypeDef]
    ) -> UpdateAccountSettingsResponseTypeDef:
        """
        Updates the Amazon Quick Sight settings in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_account_settings)
        """

    def update_action_connector(
        self, **kwargs: Unpack[UpdateActionConnectorRequestTypeDef]
    ) -> UpdateActionConnectorResponseTypeDef:
        """
        Updates an existing action connector with new configuration details,
        authentication settings, or enabled actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_action_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_action_connector)
        """

    def update_action_connector_permissions(
        self, **kwargs: Unpack[UpdateActionConnectorPermissionsRequestTypeDef]
    ) -> UpdateActionConnectorPermissionsResponseTypeDef:
        """
        Updates the permissions for an action connector by granting or revoking access
        for specific users and groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_action_connector_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_action_connector_permissions)
        """

    def update_agent(
        self, **kwargs: Unpack[UpdateAgentRequestTypeDef]
    ) -> UpdateAgentResponseTypeDef:
        """
        Updates an existing agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_agent.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_agent)
        """

    def update_agent_permissions(
        self, **kwargs: Unpack[UpdateAgentPermissionsRequestTypeDef]
    ) -> UpdateAgentPermissionsResponseTypeDef:
        """
        Updates the resource permissions for an agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_agent_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_agent_permissions)
        """

    def update_analysis(
        self, **kwargs: Unpack[UpdateAnalysisRequestTypeDef]
    ) -> UpdateAnalysisResponseTypeDef:
        """
        Updates an analysis in Amazon Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_analysis.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_analysis)
        """

    def update_analysis_permissions(
        self, **kwargs: Unpack[UpdateAnalysisPermissionsRequestTypeDef]
    ) -> UpdateAnalysisPermissionsResponseTypeDef:
        """
        Updates the read and write permissions for an analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_analysis_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_analysis_permissions)
        """

    def update_application_with_token_exchange_grant(
        self, **kwargs: Unpack[UpdateApplicationWithTokenExchangeGrantRequestTypeDef]
    ) -> UpdateApplicationWithTokenExchangeGrantResponseTypeDef:
        """
        Updates an Quick application with a token exchange grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_application_with_token_exchange_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_application_with_token_exchange_grant)
        """

    def update_approval_policy(
        self, **kwargs: Unpack[UpdateApprovalPolicyRequestTypeDef]
    ) -> UpdateApprovalPolicyResponseTypeDef:
        """
        Updates an approval policy in Quick Sight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_approval_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_approval_policy)
        """

    def update_brand(
        self, **kwargs: Unpack[UpdateBrandRequestTypeDef]
    ) -> UpdateBrandResponseTypeDef:
        """
        Updates a brand.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_brand.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_brand)
        """

    def update_brand_assignment(
        self, **kwargs: Unpack[UpdateBrandAssignmentRequestTypeDef]
    ) -> UpdateBrandAssignmentResponseTypeDef:
        """
        Updates a brand assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_brand_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_brand_assignment)
        """

    def update_brand_published_version(
        self, **kwargs: Unpack[UpdateBrandPublishedVersionRequestTypeDef]
    ) -> UpdateBrandPublishedVersionResponseTypeDef:
        """
        Updates the published version of a brand.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_brand_published_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_brand_published_version)
        """

    def update_custom_permissions(
        self, **kwargs: Unpack[UpdateCustomPermissionsRequestTypeDef]
    ) -> UpdateCustomPermissionsResponseTypeDef:
        """
        Updates a custom permissions profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_custom_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_custom_permissions)
        """

    def update_dashboard(
        self, **kwargs: Unpack[UpdateDashboardRequestTypeDef]
    ) -> UpdateDashboardResponseTypeDef:
        """
        Updates a dashboard in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_dashboard.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_dashboard)
        """

    def update_dashboard_links(
        self, **kwargs: Unpack[UpdateDashboardLinksRequestTypeDef]
    ) -> UpdateDashboardLinksResponseTypeDef:
        """
        Updates the linked analyses on a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_dashboard_links.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_dashboard_links)
        """

    def update_dashboard_permissions(
        self, **kwargs: Unpack[UpdateDashboardPermissionsRequestTypeDef]
    ) -> UpdateDashboardPermissionsResponseTypeDef:
        """
        Updates read and write permissions on a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_dashboard_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_dashboard_permissions)
        """

    def update_dashboard_published_version(
        self, **kwargs: Unpack[UpdateDashboardPublishedVersionRequestTypeDef]
    ) -> UpdateDashboardPublishedVersionResponseTypeDef:
        """
        Updates the published version of a dashboard.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_dashboard_published_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_dashboard_published_version)
        """

    def update_dashboards_qa_configuration(
        self, **kwargs: Unpack[UpdateDashboardsQAConfigurationRequestTypeDef]
    ) -> UpdateDashboardsQAConfigurationResponseTypeDef:
        """
        Updates a Dashboard QA configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_dashboards_qa_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_dashboards_qa_configuration)
        """

    def update_data_set(
        self, **kwargs: Unpack[UpdateDataSetRequestTypeDef]
    ) -> UpdateDataSetResponseTypeDef:
        """
        Updates a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_data_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_data_set)
        """

    def update_data_set_permissions(
        self, **kwargs: Unpack[UpdateDataSetPermissionsRequestTypeDef]
    ) -> UpdateDataSetPermissionsResponseTypeDef:
        """
        Updates the permissions on a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_data_set_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_data_set_permissions)
        """

    def update_data_source(
        self, **kwargs: Unpack[UpdateDataSourceRequestTypeDef]
    ) -> UpdateDataSourceResponseTypeDef:
        """
        Updates a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_data_source.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_data_source)
        """

    def update_data_source_permissions(
        self, **kwargs: Unpack[UpdateDataSourcePermissionsRequestTypeDef]
    ) -> UpdateDataSourcePermissionsResponseTypeDef:
        """
        Updates the permissions to a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_data_source_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_data_source_permissions)
        """

    def update_default_q_business_application(
        self, **kwargs: Unpack[UpdateDefaultQBusinessApplicationRequestTypeDef]
    ) -> UpdateDefaultQBusinessApplicationResponseTypeDef:
        """
        Updates a Amazon Q Business application that is linked to a Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_default_q_business_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_default_q_business_application)
        """

    def update_dlp_setting(
        self, **kwargs: Unpack[UpdateDlpSettingRequestTypeDef]
    ) -> UpdateDlpSettingResponseTypeDef:
        """
        Updates an existing DLP setting configuration in an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_dlp_setting.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_dlp_setting)
        """

    def update_flow(self, **kwargs: Unpack[UpdateFlowRequestTypeDef]) -> UpdateFlowResponseTypeDef:
        """
        Updates an existing flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_flow.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_flow)
        """

    def update_flow_permissions(
        self, **kwargs: Unpack[UpdateFlowPermissionsInputTypeDef]
    ) -> UpdateFlowPermissionsOutputTypeDef:
        """
        Updates permissions against principals on a flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_flow_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_flow_permissions)
        """

    def update_folder(
        self, **kwargs: Unpack[UpdateFolderRequestTypeDef]
    ) -> UpdateFolderResponseTypeDef:
        """
        Updates the name of a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_folder.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_folder)
        """

    def update_folder_permissions(
        self, **kwargs: Unpack[UpdateFolderPermissionsRequestTypeDef]
    ) -> UpdateFolderPermissionsResponseTypeDef:
        """
        Updates permissions of a folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_folder_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_folder_permissions)
        """

    def update_group(
        self, **kwargs: Unpack[UpdateGroupRequestTypeDef]
    ) -> UpdateGroupResponseTypeDef:
        """
        Changes a group description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_group)
        """

    def update_iam_policy_assignment(
        self, **kwargs: Unpack[UpdateIAMPolicyAssignmentRequestTypeDef]
    ) -> UpdateIAMPolicyAssignmentResponseTypeDef:
        """
        Updates an existing IAM policy assignment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_iam_policy_assignment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_iam_policy_assignment)
        """

    def update_identity_propagation_config(
        self, **kwargs: Unpack[UpdateIdentityPropagationConfigRequestTypeDef]
    ) -> UpdateIdentityPropagationConfigResponseTypeDef:
        """
        Adds or updates services and authorized targets to configure what the Quick
        Sight IAM Identity Center application can access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_identity_propagation_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_identity_propagation_config)
        """

    def update_ip_restriction(
        self, **kwargs: Unpack[UpdateIpRestrictionRequestTypeDef]
    ) -> UpdateIpRestrictionResponseTypeDef:
        """
        Updates the content and status of IP rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_ip_restriction.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_ip_restriction)
        """

    def update_key_registration(
        self, **kwargs: Unpack[UpdateKeyRegistrationRequestTypeDef]
    ) -> UpdateKeyRegistrationResponseTypeDef:
        """
        Updates a customer managed key in a Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_key_registration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_key_registration)
        """

    def update_knowledge_base(
        self, **kwargs: Unpack[UpdateKnowledgeBaseRequestTypeDef]
    ) -> UpdateKnowledgeBaseResponseTypeDef:
        """
        Updates the properties of an existing knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_knowledge_base.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_knowledge_base)
        """

    def update_knowledge_base_permissions(
        self, **kwargs: Unpack[UpdateKnowledgeBasePermissionsRequestTypeDef]
    ) -> UpdateKnowledgeBasePermissionsResponseTypeDef:
        """
        Updates the resource permissions for a knowledge base.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_knowledge_base_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_knowledge_base_permissions)
        """

    def update_limits_profile(
        self, **kwargs: Unpack[UpdateLimitsProfileRequestTypeDef]
    ) -> UpdateLimitsProfileResponseTypeDef:
        """
        Updates the properties of an existing limits profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_limits_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_limits_profile)
        """

    def update_o_auth_client_application(
        self, **kwargs: Unpack[UpdateOAuthClientApplicationRequestTypeDef]
    ) -> UpdateOAuthClientApplicationResponseTypeDef:
        """
        Updates an OAuthClientApplication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_o_auth_client_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_o_auth_client_application)
        """

    def update_public_sharing_settings(
        self, **kwargs: Unpack[UpdatePublicSharingSettingsRequestTypeDef]
    ) -> UpdatePublicSharingSettingsResponseTypeDef:
        """
        This API controls public sharing settings for your entire Quick Sight account,
        affecting data security and access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_public_sharing_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_public_sharing_settings)
        """

    def update_q_personalization_configuration(
        self, **kwargs: Unpack[UpdateQPersonalizationConfigurationRequestTypeDef]
    ) -> UpdateQPersonalizationConfigurationResponseTypeDef:
        """
        Updates a personalization configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_q_personalization_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_q_personalization_configuration)
        """

    def update_quick_sight_q_search_configuration(
        self, **kwargs: Unpack[UpdateQuickSightQSearchConfigurationRequestTypeDef]
    ) -> UpdateQuickSightQSearchConfigurationResponseTypeDef:
        """
        Updates the state of a Quick Sight Q Search configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_quick_sight_q_search_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_quick_sight_q_search_configuration)
        """

    def update_refresh_schedule(
        self, **kwargs: Unpack[UpdateRefreshScheduleRequestTypeDef]
    ) -> UpdateRefreshScheduleResponseTypeDef:
        """
        Updates a refresh schedule for a dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_refresh_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_refresh_schedule)
        """

    def update_role_custom_permission(
        self, **kwargs: Unpack[UpdateRoleCustomPermissionRequestTypeDef]
    ) -> UpdateRoleCustomPermissionResponseTypeDef:
        """
        Updates the custom permissions that are associated with a role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_role_custom_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_role_custom_permission)
        """

    def update_spice_capacity_configuration(
        self, **kwargs: Unpack[UpdateSPICECapacityConfigurationRequestTypeDef]
    ) -> UpdateSPICECapacityConfigurationResponseTypeDef:
        """
        Updates the SPICE capacity configuration for a Quick Sight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_spice_capacity_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_spice_capacity_configuration)
        """

    def update_self_upgrade(
        self, **kwargs: Unpack[UpdateSelfUpgradeRequestTypeDef]
    ) -> UpdateSelfUpgradeResponseTypeDef:
        """
        Updates a self-upgrade request for a Quick user by approving, denying, or
        verifying the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_self_upgrade.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_self_upgrade)
        """

    def update_self_upgrade_configuration(
        self, **kwargs: Unpack[UpdateSelfUpgradeConfigurationRequestTypeDef]
    ) -> UpdateSelfUpgradeConfigurationResponseTypeDef:
        """
        Updates the self-upgrade configuration for a Quick account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_self_upgrade_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_self_upgrade_configuration)
        """

    def update_space(
        self, **kwargs: Unpack[UpdateSpaceRequestTypeDef]
    ) -> UpdateSpaceResponseTypeDef:
        """
        Updates the metadata of an Amazon QuickSight space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_space)
        """

    def update_space_permissions(
        self, **kwargs: Unpack[UpdateSpacePermissionsRequestTypeDef]
    ) -> UpdateSpacePermissionsResponseTypeDef:
        """
        Updates the permissions for an Amazon QuickSight space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_space_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_space_permissions)
        """

    def update_space_resources(
        self, **kwargs: Unpack[UpdateSpaceResourcesRequestTypeDef]
    ) -> UpdateSpaceResourcesResponseTypeDef:
        """
        Adds or removes resources from an Amazon QuickSight space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_space_resources.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_space_resources)
        """

    def update_template(
        self, **kwargs: Unpack[UpdateTemplateRequestTypeDef]
    ) -> UpdateTemplateResponseTypeDef:
        """
        Updates a template from an existing Amazon Quick Sight analysis or another
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_template.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_template)
        """

    def update_template_alias(
        self, **kwargs: Unpack[UpdateTemplateAliasRequestTypeDef]
    ) -> UpdateTemplateAliasResponseTypeDef:
        """
        Updates the template alias of a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_template_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_template_alias)
        """

    def update_template_permissions(
        self, **kwargs: Unpack[UpdateTemplatePermissionsRequestTypeDef]
    ) -> UpdateTemplatePermissionsResponseTypeDef:
        """
        Updates the resource permissions for a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_template_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_template_permissions)
        """

    def update_theme(
        self, **kwargs: Unpack[UpdateThemeRequestTypeDef]
    ) -> UpdateThemeResponseTypeDef:
        """
        Updates a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_theme.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_theme)
        """

    def update_theme_alias(
        self, **kwargs: Unpack[UpdateThemeAliasRequestTypeDef]
    ) -> UpdateThemeAliasResponseTypeDef:
        """
        Updates an alias of a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_theme_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_theme_alias)
        """

    def update_theme_permissions(
        self, **kwargs: Unpack[UpdateThemePermissionsRequestTypeDef]
    ) -> UpdateThemePermissionsResponseTypeDef:
        """
        Updates the resource permissions for a theme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_theme_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_theme_permissions)
        """

    def update_topic(
        self, **kwargs: Unpack[UpdateTopicRequestTypeDef]
    ) -> UpdateTopicResponseTypeDef:
        """
        Updates a topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_topic.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_topic)
        """

    def update_topic_permissions(
        self, **kwargs: Unpack[UpdateTopicPermissionsRequestTypeDef]
    ) -> UpdateTopicPermissionsResponseTypeDef:
        """
        Updates the permissions of a topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_topic_permissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_topic_permissions)
        """

    def update_topic_permissions_v2(
        self, **kwargs: Unpack[UpdateTopicPermissionsV2RequestTypeDef]
    ) -> UpdateTopicPermissionsV2ResponseTypeDef:
        """
        Updates the permissions of a topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_topic_permissions_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_topic_permissions_v2)
        """

    def update_topic_refresh_schedule(
        self, **kwargs: Unpack[UpdateTopicRefreshScheduleRequestTypeDef]
    ) -> UpdateTopicRefreshScheduleResponseTypeDef:
        """
        Updates a topic refresh schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_topic_refresh_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_topic_refresh_schedule)
        """

    def update_topic_v2(
        self, **kwargs: Unpack[UpdateTopicV2RequestTypeDef]
    ) -> UpdateTopicV2ResponseTypeDef:
        """
        Updates the definition of a Q topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_topic_v2.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_topic_v2)
        """

    def update_user(self, **kwargs: Unpack[UpdateUserRequestTypeDef]) -> UpdateUserResponseTypeDef:
        """
        Updates an Amazon Quick Sight user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_user)
        """

    def update_user_custom_permission(
        self, **kwargs: Unpack[UpdateUserCustomPermissionRequestTypeDef]
    ) -> UpdateUserCustomPermissionResponseTypeDef:
        """
        Updates a custom permissions profile for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_user_custom_permission.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_user_custom_permission)
        """

    def update_vpc_connection(
        self, **kwargs: Unpack[UpdateVPCConnectionRequestTypeDef]
    ) -> UpdateVPCConnectionResponseTypeDef:
        """
        Updates a VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_vpc_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_vpc_connection)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_folder_permissions"]
    ) -> DescribeFolderPermissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_folder_resolved_permissions"]
    ) -> DescribeFolderResolvedPermissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_action_connectors"]
    ) -> ListActionConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_analyses"]
    ) -> ListAnalysesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_approval_policies"]
    ) -> ListApprovalPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_asset_bundle_export_jobs"]
    ) -> ListAssetBundleExportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_asset_bundle_import_jobs"]
    ) -> ListAssetBundleImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_brands"]
    ) -> ListBrandsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_custom_permissions"]
    ) -> ListCustomPermissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dashboard_versions"]
    ) -> ListDashboardVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dashboards"]
    ) -> ListDashboardsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_sets"]
    ) -> ListDataSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_sources"]
    ) -> ListDataSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dlp_settings"]
    ) -> ListDlpSettingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_flows"]
    ) -> ListFlowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_folder_members"]
    ) -> ListFolderMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_folders_for_resource"]
    ) -> ListFoldersForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_folders"]
    ) -> ListFoldersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_group_memberships"]
    ) -> ListGroupMembershipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_groups"]
    ) -> ListGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_iam_policy_assignments_for_user"]
    ) -> ListIAMPolicyAssignmentsForUserPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_iam_policy_assignments"]
    ) -> ListIAMPolicyAssignmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ingestions"]
    ) -> ListIngestionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_knowledge_bases"]
    ) -> ListKnowledgeBasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_limits_profiles"]
    ) -> ListLimitsProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_namespaces"]
    ) -> ListNamespacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_o_auth_client_applications"]
    ) -> ListOAuthClientApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_role_memberships"]
    ) -> ListRoleMembershipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_template_aliases"]
    ) -> ListTemplateAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_template_versions"]
    ) -> ListTemplateVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_templates"]
    ) -> ListTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_theme_versions"]
    ) -> ListThemeVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_themes"]
    ) -> ListThemesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_topics_v2"]
    ) -> ListTopicsV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_user_groups"]
    ) -> ListUserGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_users"]
    ) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_action_connectors"]
    ) -> SearchActionConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_analyses"]
    ) -> SearchAnalysesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_dashboards"]
    ) -> SearchDashboardsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_data_sets"]
    ) -> SearchDataSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_data_sources"]
    ) -> SearchDataSourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_flows"]
    ) -> SearchFlowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_folders"]
    ) -> SearchFoldersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_groups"]
    ) -> SearchGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_knowledge_bases"]
    ) -> SearchKnowledgeBasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_topics"]
    ) -> SearchTopicsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_topics_v2"]
    ) -> SearchTopicsV2Paginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """
