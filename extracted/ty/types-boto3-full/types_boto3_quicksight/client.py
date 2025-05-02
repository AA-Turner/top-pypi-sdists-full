"""
Type annotations for quicksight service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/)

Copyright 2025 Vlad Emelianov

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
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeFolderPermissionsPaginator,
    DescribeFolderResolvedPermissionsPaginator,
    ListAnalysesPaginator,
    ListAssetBundleExportJobsPaginator,
    ListAssetBundleImportJobsPaginator,
    ListBrandsPaginator,
    ListCustomPermissionsPaginator,
    ListDashboardsPaginator,
    ListDashboardVersionsPaginator,
    ListDataSetsPaginator,
    ListDataSourcesPaginator,
    ListFolderMembersPaginator,
    ListFoldersForResourcePaginator,
    ListFoldersPaginator,
    ListGroupMembershipsPaginator,
    ListGroupsPaginator,
    ListIAMPolicyAssignmentsForUserPaginator,
    ListIAMPolicyAssignmentsPaginator,
    ListIngestionsPaginator,
    ListNamespacesPaginator,
    ListRoleMembershipsPaginator,
    ListTemplateAliasesPaginator,
    ListTemplatesPaginator,
    ListTemplateVersionsPaginator,
    ListThemesPaginator,
    ListThemeVersionsPaginator,
    ListUserGroupsPaginator,
    ListUsersPaginator,
    SearchAnalysesPaginator,
    SearchDashboardsPaginator,
    SearchDataSetsPaginator,
    SearchDataSourcesPaginator,
    SearchFoldersPaginator,
    SearchGroupsPaginator,
    SearchTopicsPaginator,
)
from .type_defs import (
    BatchCreateTopicReviewedAnswerRequestTypeDef,
    BatchCreateTopicReviewedAnswerResponseTypeDef,
    BatchDeleteTopicReviewedAnswerRequestTypeDef,
    BatchDeleteTopicReviewedAnswerResponseTypeDef,
    CancelIngestionRequestTypeDef,
    CancelIngestionResponseTypeDef,
    CreateAccountCustomizationRequestTypeDef,
    CreateAccountCustomizationResponseTypeDef,
    CreateAccountSubscriptionRequestTypeDef,
    CreateAccountSubscriptionResponseTypeDef,
    CreateAnalysisRequestTypeDef,
    CreateAnalysisResponseTypeDef,
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
    CreateNamespaceRequestTypeDef,
    CreateNamespaceResponseTypeDef,
    CreateRefreshScheduleRequestTypeDef,
    CreateRefreshScheduleResponseTypeDef,
    CreateRoleMembershipRequestTypeDef,
    CreateRoleMembershipResponseTypeDef,
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
    CreateVPCConnectionRequestTypeDef,
    CreateVPCConnectionResponseTypeDef,
    DeleteAccountCustomizationRequestTypeDef,
    DeleteAccountCustomizationResponseTypeDef,
    DeleteAccountSubscriptionRequestTypeDef,
    DeleteAccountSubscriptionResponseTypeDef,
    DeleteAnalysisRequestTypeDef,
    DeleteAnalysisResponseTypeDef,
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
    DeleteNamespaceRequestTypeDef,
    DeleteNamespaceResponseTypeDef,
    DeleteRefreshScheduleRequestTypeDef,
    DeleteRefreshScheduleResponseTypeDef,
    DeleteRoleCustomPermissionRequestTypeDef,
    DeleteRoleCustomPermissionResponseTypeDef,
    DeleteRoleMembershipRequestTypeDef,
    DeleteRoleMembershipResponseTypeDef,
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
    DescribeAccountSettingsRequestTypeDef,
    DescribeAccountSettingsResponseTypeDef,
    DescribeAccountSubscriptionRequestTypeDef,
    DescribeAccountSubscriptionResponseTypeDef,
    DescribeAnalysisDefinitionRequestTypeDef,
    DescribeAnalysisDefinitionResponseTypeDef,
    DescribeAnalysisPermissionsRequestTypeDef,
    DescribeAnalysisPermissionsResponseTypeDef,
    DescribeAnalysisRequestTypeDef,
    DescribeAnalysisResponseTypeDef,
    DescribeAssetBundleExportJobRequestTypeDef,
    DescribeAssetBundleExportJobResponseTypeDef,
    DescribeAssetBundleImportJobRequestTypeDef,
    DescribeAssetBundleImportJobResponseTypeDef,
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
    DescribeNamespaceRequestTypeDef,
    DescribeNamespaceResponseTypeDef,
    DescribeQPersonalizationConfigurationRequestTypeDef,
    DescribeQPersonalizationConfigurationResponseTypeDef,
    DescribeQuickSightQSearchConfigurationRequestTypeDef,
    DescribeQuickSightQSearchConfigurationResponseTypeDef,
    DescribeRefreshScheduleRequestTypeDef,
    DescribeRefreshScheduleResponseTypeDef,
    DescribeRoleCustomPermissionRequestTypeDef,
    DescribeRoleCustomPermissionResponseTypeDef,
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
    DescribeTopicRefreshRequestTypeDef,
    DescribeTopicRefreshResponseTypeDef,
    DescribeTopicRefreshScheduleRequestTypeDef,
    DescribeTopicRefreshScheduleResponseTypeDef,
    DescribeTopicRequestTypeDef,
    DescribeTopicResponseTypeDef,
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
    GetSessionEmbedUrlRequestTypeDef,
    GetSessionEmbedUrlResponseTypeDef,
    ListAnalysesRequestTypeDef,
    ListAnalysesResponseTypeDef,
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
    ListNamespacesRequestTypeDef,
    ListNamespacesResponseTypeDef,
    ListRefreshSchedulesRequestTypeDef,
    ListRefreshSchedulesResponseTypeDef,
    ListRoleMembershipsRequestTypeDef,
    ListRoleMembershipsResponseTypeDef,
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
    ListUserGroupsRequestTypeDef,
    ListUserGroupsResponseTypeDef,
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
    SearchAnalysesRequestTypeDef,
    SearchAnalysesResponseTypeDef,
    SearchDashboardsRequestTypeDef,
    SearchDashboardsResponseTypeDef,
    SearchDataSetsRequestTypeDef,
    SearchDataSetsResponseTypeDef,
    SearchDataSourcesRequestTypeDef,
    SearchDataSourcesResponseTypeDef,
    SearchFoldersRequestTypeDef,
    SearchFoldersResponseTypeDef,
    SearchGroupsRequestTypeDef,
    SearchGroupsResponseTypeDef,
    SearchTopicsRequestTypeDef,
    SearchTopicsResponseTypeDef,
    StartAssetBundleExportJobRequestTypeDef,
    StartAssetBundleExportJobResponseTypeDef,
    StartAssetBundleImportJobRequestTypeDef,
    StartAssetBundleImportJobResponseTypeDef,
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
    UpdateAccountSettingsRequestTypeDef,
    UpdateAccountSettingsResponseTypeDef,
    UpdateAnalysisPermissionsRequestTypeDef,
    UpdateAnalysisPermissionsResponseTypeDef,
    UpdateAnalysisRequestTypeDef,
    UpdateAnalysisResponseTypeDef,
    UpdateApplicationWithTokenExchangeGrantRequestTypeDef,
    UpdateApplicationWithTokenExchangeGrantResponseTypeDef,
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
    UpdateTopicRefreshScheduleRequestTypeDef,
    UpdateTopicRefreshScheduleResponseTypeDef,
    UpdateTopicRequestTypeDef,
    UpdateTopicResponseTypeDef,
    UpdateUserCustomPermissionRequestTypeDef,
    UpdateUserCustomPermissionResponseTypeDef,
    UpdateUserRequestTypeDef,
    UpdateUserResponseTypeDef,
    UpdateVPCConnectionRequestTypeDef,
    UpdateVPCConnectionResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("QuickSightClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentUpdatingException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CustomerManagedKeyUnavailableException: Type[BotocoreClientError]
    DomainNotWhitelistedException: Type[BotocoreClientError]
    IdentityTypeNotSupportedException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    PreconditionNotMetException: Type[BotocoreClientError]
    QuickSightUserNotFoundException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    SessionLifetimeInMinutesInvalidException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedPricingPlanException: Type[BotocoreClientError]
    UnsupportedUserEditionException: Type[BotocoreClientError]


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

    def batch_delete_topic_reviewed_answer(
        self, **kwargs: Unpack[BatchDeleteTopicReviewedAnswerRequestTypeDef]
    ) -> BatchDeleteTopicReviewedAnswerResponseTypeDef:
        """
        Deletes reviewed answers for Q Topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/batch_delete_topic_reviewed_answer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#batch_delete_topic_reviewed_answer)
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
        Creates Amazon QuickSight customizations for the current Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_account_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_account_customization)
        """

    def create_account_subscription(
        self, **kwargs: Unpack[CreateAccountSubscriptionRequestTypeDef]
    ) -> CreateAccountSubscriptionResponseTypeDef:
        """
        Creates an Amazon QuickSight account, or subscribes to Amazon QuickSight Q.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_account_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_account_subscription)
        """

    def create_analysis(
        self, **kwargs: Unpack[CreateAnalysisRequestTypeDef]
    ) -> CreateAnalysisResponseTypeDef:
        """
        Creates an analysis in Amazon QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_analysis.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_analysis)
        """

    def create_brand(
        self, **kwargs: Unpack[CreateBrandRequestTypeDef]
    ) -> CreateBrandResponseTypeDef:
        """
        Creates an Amazon QuickSight brand.

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
        Use the <code>CreateGroup</code> operation to create a group in Amazon
        QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_group)
        """

    def create_group_membership(
        self, **kwargs: Unpack[CreateGroupMembershipRequestTypeDef]
    ) -> CreateGroupMembershipResponseTypeDef:
        """
        Adds an Amazon QuickSight user to an Amazon QuickSight group.

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

    def create_namespace(
        self, **kwargs: Unpack[CreateNamespaceRequestTypeDef]
    ) -> CreateNamespaceResponseTypeDef:
        """
        (Enterprise edition only) Creates a new namespace for you to use with Amazon
        QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_namespace)
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
        Use <code>CreateRoleMembership</code> to add an existing Amazon QuickSight
        group to an existing role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_role_membership.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_role_membership)
        """

    def create_template(
        self, **kwargs: Unpack[CreateTemplateRequestTypeDef]
    ) -> CreateTemplateResponseTypeDef:
        """
        Creates a template either from a <code>TemplateDefinition</code> or from an
        existing Amazon QuickSight analysis or template.

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

    def create_vpc_connection(
        self, **kwargs: Unpack[CreateVPCConnectionRequestTypeDef]
    ) -> CreateVPCConnectionResponseTypeDef:
        """
        Creates a new VPC connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_vpc_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#create_vpc_connection)
        """

    def delete_account_customization(
        self, **kwargs: Unpack[DeleteAccountCustomizationRequestTypeDef]
    ) -> DeleteAccountCustomizationResponseTypeDef:
        """
        Deletes all Amazon QuickSight customizations in this Amazon Web Services Region
        for the specified Amazon Web Services account and Amazon QuickSight namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_account_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_account_customization)
        """

    def delete_account_subscription(
        self, **kwargs: Unpack[DeleteAccountSubscriptionRequestTypeDef]
    ) -> DeleteAccountSubscriptionResponseTypeDef:
        """
        Use the <code>DeleteAccountSubscription</code> operation to delete an Amazon
        QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_account_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_account_subscription)
        """

    def delete_analysis(
        self, **kwargs: Unpack[DeleteAnalysisRequestTypeDef]
    ) -> DeleteAnalysisResponseTypeDef:
        """
        Deletes an analysis from Amazon QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_analysis.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_analysis)
        """

    def delete_brand(
        self, **kwargs: Unpack[DeleteBrandRequestTypeDef]
    ) -> DeleteBrandResponseTypeDef:
        """
        Deletes an Amazon QuickSight brand.

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
        Deletes a linked Amazon Q Business application from an Amazon QuickSight
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_default_q_business_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_default_q_business_application)
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
        Removes a user group from Amazon QuickSight.

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
        service from the Amazon QuickSight IAM Identity Center application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/delete_identity_propagation_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#delete_identity_propagation_config)
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

    def delete_user(self, **kwargs: Unpack[DeleteUserRequestTypeDef]) -> DeleteUserResponseTypeDef:
        """
        Deletes the Amazon QuickSight user that is associated with the identity of the
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

    def describe_account_customization(
        self, **kwargs: Unpack[DescribeAccountCustomizationRequestTypeDef]
    ) -> DescribeAccountCustomizationResponseTypeDef:
        """
        Describes the customizations associated with the provided Amazon Web Services
        account and Amazon Amazon QuickSight namespace in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_account_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_account_customization)
        """

    def describe_account_settings(
        self, **kwargs: Unpack[DescribeAccountSettingsRequestTypeDef]
    ) -> DescribeAccountSettingsResponseTypeDef:
        """
        Describes the settings that were used when your Amazon QuickSight subscription
        was first created in this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_account_settings)
        """

    def describe_account_subscription(
        self, **kwargs: Unpack[DescribeAccountSubscriptionRequestTypeDef]
    ) -> DescribeAccountSubscriptionResponseTypeDef:
        """
        Use the DescribeAccountSubscription operation to receive a description of an
        Amazon QuickSight account's subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_account_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_account_subscription)
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
        Describes a Amazon Q Business application that is linked to an Amazon
        QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_default_q_business_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_default_q_business_application)
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
        Returns an Amazon QuickSight group's description and Amazon Resource Name (ARN).

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
        Describes all customer managed key registrations in a Amazon QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_key_registration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_key_registration)
        """

    def describe_namespace(
        self, **kwargs: Unpack[DescribeNamespaceRequestTypeDef]
    ) -> DescribeNamespaceResponseTypeDef:
        """
        Describes the current namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#describe_namespace)
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
        Describes the state of a Amazon QuickSight Q Search configuration.

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
        Generates an embed URL that you can use to embed an Amazon QuickSight dashboard
        or visual in your website, without having to register any reader users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/generate_embed_url_for_anonymous_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#generate_embed_url_for_anonymous_user)
        """

    def generate_embed_url_for_registered_user(
        self, **kwargs: Unpack[GenerateEmbedUrlForRegisteredUserRequestTypeDef]
    ) -> GenerateEmbedUrlForRegisteredUserResponseTypeDef:
        """
        Generates an embed URL that you can use to embed an Amazon QuickSight
        experience in your website.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/generate_embed_url_for_registered_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#generate_embed_url_for_registered_user)
        """

    def generate_embed_url_for_registered_user_with_identity(
        self, **kwargs: Unpack[GenerateEmbedUrlForRegisteredUserWithIdentityRequestTypeDef]
    ) -> GenerateEmbedUrlForRegisteredUserWithIdentityResponseTypeDef:
        """
        Generates an embed URL that you can use to embed an Amazon QuickSight
        experience in your website.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/generate_embed_url_for_registered_user_with_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#generate_embed_url_for_registered_user_with_identity)
        """

    def get_dashboard_embed_url(
        self, **kwargs: Unpack[GetDashboardEmbedUrlRequestTypeDef]
    ) -> GetDashboardEmbedUrlResponseTypeDef:
        """
        Generates a temporary session URL and authorization code(bearer token) that you
        can use to embed an Amazon QuickSight read-only dashboard in your website or
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_dashboard_embed_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_dashboard_embed_url)
        """

    def get_session_embed_url(
        self, **kwargs: Unpack[GetSessionEmbedUrlRequestTypeDef]
    ) -> GetSessionEmbedUrlResponseTypeDef:
        """
        Generates a session URL and authorization code that you can use to embed the
        Amazon Amazon QuickSight console in your web server code.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_session_embed_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_session_embed_url)
        """

    def list_analyses(
        self, **kwargs: Unpack[ListAnalysesRequestTypeDef]
    ) -> ListAnalysesResponseTypeDef:
        """
        Lists Amazon QuickSight analyses that exist in the specified Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_analyses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_analyses)
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
        Lists all brands in an Amazon QuickSight account.

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
        Lists all the versions of the dashboards in the Amazon QuickSight subscription.

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
        Lists all user groups in Amazon QuickSight.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_groups)
        """

    def list_iam_policy_assignments(
        self, **kwargs: Unpack[ListIAMPolicyAssignmentsRequestTypeDef]
    ) -> ListIAMPolicyAssignmentsResponseTypeDef:
        """
        Lists the IAM policy assignments in the current Amazon QuickSight account.

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
        Lists all services and authorized targets that the Amazon QuickSight IAM
        Identity Center application can access.

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

    def list_namespaces(
        self, **kwargs: Unpack[ListNamespacesRequestTypeDef]
    ) -> ListNamespacesResponseTypeDef:
        """
        Lists the namespaces for the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_namespaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_namespaces)
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
        Lists all the versions of the templates in the current Amazon QuickSight
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_template_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_template_versions)
        """

    def list_templates(
        self, **kwargs: Unpack[ListTemplatesRequestTypeDef]
    ) -> ListTemplatesResponseTypeDef:
        """
        Lists all the templates in the current Amazon QuickSight account.

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

    def list_user_groups(
        self, **kwargs: Unpack[ListUserGroupsRequestTypeDef]
    ) -> ListUserGroupsResponseTypeDef:
        """
        Lists the Amazon QuickSight groups that an Amazon QuickSight user is a member
        of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_user_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_user_groups)
        """

    def list_users(self, **kwargs: Unpack[ListUsersRequestTypeDef]) -> ListUsersResponseTypeDef:
        """
        Returns a list of all of the Amazon QuickSight users belonging to this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/list_users.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#list_users)
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
        Creates an Amazon QuickSight user whose identity is associated with the
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
        Amazon QuickSight namespace using the supplied filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_groups)
        """

    def search_topics(
        self, **kwargs: Unpack[SearchTopicsRequestTypeDef]
    ) -> SearchTopicsResponseTypeDef:
        """
        Searches for any Q topic that exists in an Amazon QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/search_topics.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#search_topics)
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
        Assigns one or more tags (key-value pairs) to the specified Amazon QuickSight
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

    def update_account_customization(
        self, **kwargs: Unpack[UpdateAccountCustomizationRequestTypeDef]
    ) -> UpdateAccountCustomizationResponseTypeDef:
        """
        Updates Amazon QuickSight customizations for the current Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_account_customization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_account_customization)
        """

    def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsRequestTypeDef]
    ) -> UpdateAccountSettingsResponseTypeDef:
        """
        Updates the Amazon QuickSight settings in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_account_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_account_settings)
        """

    def update_analysis(
        self, **kwargs: Unpack[UpdateAnalysisRequestTypeDef]
    ) -> UpdateAnalysisResponseTypeDef:
        """
        Updates an analysis in Amazon QuickSight.

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
        Updates an Amazon QuickSight application with a token exchange grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_application_with_token_exchange_grant.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_application_with_token_exchange_grant)
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
        Updates a Amazon Q Business application that is linked to a Amazon QuickSight
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_default_q_business_application.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_default_q_business_application)
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
        Adds or updates services and authorized targets to configure what the Amazon
        QuickSight IAM Identity Center application can access.

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
        Updates a customer managed key in a Amazon QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_key_registration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_key_registration)
        """

    def update_public_sharing_settings(
        self, **kwargs: Unpack[UpdatePublicSharingSettingsRequestTypeDef]
    ) -> UpdatePublicSharingSettingsResponseTypeDef:
        """
        Use the <code>UpdatePublicSharingSettings</code> operation to turn on or turn
        off the public sharing settings of an Amazon QuickSight dashboard.

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
        Updates the state of a Amazon QuickSight Q Search configuration.

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
        Updates the SPICE capacity configuration for a Amazon QuickSight account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_spice_capacity_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_spice_capacity_configuration)
        """

    def update_template(
        self, **kwargs: Unpack[UpdateTemplateRequestTypeDef]
    ) -> UpdateTemplateResponseTypeDef:
        """
        Updates a template from an existing Amazon QuickSight analysis or another
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

    def update_topic_refresh_schedule(
        self, **kwargs: Unpack[UpdateTopicRefreshScheduleRequestTypeDef]
    ) -> UpdateTopicRefreshScheduleResponseTypeDef:
        """
        Updates a topic refresh schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_topic_refresh_schedule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#update_topic_refresh_schedule)
        """

    def update_user(self, **kwargs: Unpack[UpdateUserRequestTypeDef]) -> UpdateUserResponseTypeDef:
        """
        Updates an Amazon QuickSight user.

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
        self, operation_name: Literal["list_analyses"]
    ) -> ListAnalysesPaginator:
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
        self, operation_name: Literal["list_namespaces"]
    ) -> ListNamespacesPaginator:
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
        self, operation_name: Literal["search_topics"]
    ) -> SearchTopicsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_quicksight/client/#get_paginator)
        """
