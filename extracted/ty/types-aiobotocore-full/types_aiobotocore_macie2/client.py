"""
Type annotations for macie2 service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_macie2.client import Macie2Client

    session = get_session()
    async with session.create_client("macie2") as client:
        client: Macie2Client
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    DescribeBucketsPaginator,
    GetUsageStatisticsPaginator,
    ListAllowListsPaginator,
    ListAutomatedDiscoveryAccountsPaginator,
    ListClassificationJobsPaginator,
    ListClassificationScopesPaginator,
    ListCustomDataIdentifiersPaginator,
    ListFindingsFiltersPaginator,
    ListFindingsPaginator,
    ListInvitationsPaginator,
    ListManagedDataIdentifiersPaginator,
    ListMembersPaginator,
    ListOrganizationAdminAccountsPaginator,
    ListResourceProfileArtifactsPaginator,
    ListResourceProfileDetectionsPaginator,
    ListSensitivityInspectionTemplatesPaginator,
    SearchResourcesPaginator,
)
from .type_defs import (
    AcceptInvitationRequestTypeDef,
    BatchGetCustomDataIdentifiersRequestTypeDef,
    BatchGetCustomDataIdentifiersResponseTypeDef,
    BatchUpdateAutomatedDiscoveryAccountsRequestTypeDef,
    BatchUpdateAutomatedDiscoveryAccountsResponseTypeDef,
    CreateAllowListRequestTypeDef,
    CreateAllowListResponseTypeDef,
    CreateClassificationJobRequestTypeDef,
    CreateClassificationJobResponseTypeDef,
    CreateCustomDataIdentifierRequestTypeDef,
    CreateCustomDataIdentifierResponseTypeDef,
    CreateFindingsFilterRequestTypeDef,
    CreateFindingsFilterResponseTypeDef,
    CreateInvitationsRequestTypeDef,
    CreateInvitationsResponseTypeDef,
    CreateMemberRequestTypeDef,
    CreateMemberResponseTypeDef,
    CreateSampleFindingsRequestTypeDef,
    DeclineInvitationsRequestTypeDef,
    DeclineInvitationsResponseTypeDef,
    DeleteAllowListRequestTypeDef,
    DeleteCustomDataIdentifierRequestTypeDef,
    DeleteFindingsFilterRequestTypeDef,
    DeleteInvitationsRequestTypeDef,
    DeleteInvitationsResponseTypeDef,
    DeleteMemberRequestTypeDef,
    DescribeBucketsRequestTypeDef,
    DescribeBucketsResponseTypeDef,
    DescribeClassificationJobRequestTypeDef,
    DescribeClassificationJobResponseTypeDef,
    DescribeOrganizationConfigurationResponseTypeDef,
    DisableOrganizationAdminAccountRequestTypeDef,
    DisassociateMemberRequestTypeDef,
    EnableMacieRequestTypeDef,
    EnableOrganizationAdminAccountRequestTypeDef,
    GetAdministratorAccountResponseTypeDef,
    GetAllowListRequestTypeDef,
    GetAllowListResponseTypeDef,
    GetAutomatedDiscoveryConfigurationResponseTypeDef,
    GetBucketStatisticsRequestTypeDef,
    GetBucketStatisticsResponseTypeDef,
    GetClassificationExportConfigurationResponseTypeDef,
    GetClassificationScopeRequestTypeDef,
    GetClassificationScopeResponseTypeDef,
    GetCustomDataIdentifierRequestTypeDef,
    GetCustomDataIdentifierResponseTypeDef,
    GetFindingsFilterRequestTypeDef,
    GetFindingsFilterResponseTypeDef,
    GetFindingsPublicationConfigurationResponseTypeDef,
    GetFindingsRequestTypeDef,
    GetFindingsResponseTypeDef,
    GetFindingStatisticsRequestTypeDef,
    GetFindingStatisticsResponseTypeDef,
    GetInvitationsCountResponseTypeDef,
    GetMacieSessionResponseTypeDef,
    GetMasterAccountResponseTypeDef,
    GetMemberRequestTypeDef,
    GetMemberResponseTypeDef,
    GetResourceProfileRequestTypeDef,
    GetResourceProfileResponseTypeDef,
    GetRevealConfigurationResponseTypeDef,
    GetSensitiveDataOccurrencesAvailabilityRequestTypeDef,
    GetSensitiveDataOccurrencesAvailabilityResponseTypeDef,
    GetSensitiveDataOccurrencesRequestTypeDef,
    GetSensitiveDataOccurrencesResponseTypeDef,
    GetSensitivityInspectionTemplateRequestTypeDef,
    GetSensitivityInspectionTemplateResponseTypeDef,
    GetUsageStatisticsRequestTypeDef,
    GetUsageStatisticsResponseTypeDef,
    GetUsageTotalsRequestTypeDef,
    GetUsageTotalsResponseTypeDef,
    ListAllowListsRequestTypeDef,
    ListAllowListsResponseTypeDef,
    ListAutomatedDiscoveryAccountsRequestTypeDef,
    ListAutomatedDiscoveryAccountsResponseTypeDef,
    ListClassificationJobsRequestTypeDef,
    ListClassificationJobsResponseTypeDef,
    ListClassificationScopesRequestTypeDef,
    ListClassificationScopesResponseTypeDef,
    ListCustomDataIdentifiersRequestTypeDef,
    ListCustomDataIdentifiersResponseTypeDef,
    ListFindingsFiltersRequestTypeDef,
    ListFindingsFiltersResponseTypeDef,
    ListFindingsRequestTypeDef,
    ListFindingsResponseTypeDef,
    ListInvitationsRequestTypeDef,
    ListInvitationsResponseTypeDef,
    ListManagedDataIdentifiersRequestTypeDef,
    ListManagedDataIdentifiersResponseTypeDef,
    ListMembersRequestTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListResourceProfileArtifactsRequestTypeDef,
    ListResourceProfileArtifactsResponseTypeDef,
    ListResourceProfileDetectionsRequestTypeDef,
    ListResourceProfileDetectionsResponseTypeDef,
    ListSensitivityInspectionTemplatesRequestTypeDef,
    ListSensitivityInspectionTemplatesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutClassificationExportConfigurationRequestTypeDef,
    PutClassificationExportConfigurationResponseTypeDef,
    PutFindingsPublicationConfigurationRequestTypeDef,
    SearchResourcesRequestTypeDef,
    SearchResourcesResponseTypeDef,
    TagResourceRequestTypeDef,
    TestCustomDataIdentifierRequestTypeDef,
    TestCustomDataIdentifierResponseTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAllowListRequestTypeDef,
    UpdateAllowListResponseTypeDef,
    UpdateAutomatedDiscoveryConfigurationRequestTypeDef,
    UpdateClassificationJobRequestTypeDef,
    UpdateClassificationScopeRequestTypeDef,
    UpdateFindingsFilterRequestTypeDef,
    UpdateFindingsFilterResponseTypeDef,
    UpdateMacieSessionRequestTypeDef,
    UpdateMemberSessionRequestTypeDef,
    UpdateOrganizationConfigurationRequestTypeDef,
    UpdateResourceProfileDetectionsRequestTypeDef,
    UpdateResourceProfileRequestTypeDef,
    UpdateRevealConfigurationRequestTypeDef,
    UpdateRevealConfigurationResponseTypeDef,
    UpdateSensitivityInspectionTemplateRequestTypeDef,
)
from .waiter import FindingRevealedWaiter

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("Macie2Client",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnprocessableEntityException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class Macie2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Macie2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#generate_presigned_url)
        """

    async def accept_invitation(
        self, **kwargs: Unpack[AcceptInvitationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Accepts an Amazon Macie membership invitation that was received from a specific
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/accept_invitation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#accept_invitation)
        """

    async def batch_get_custom_data_identifiers(
        self, **kwargs: Unpack[BatchGetCustomDataIdentifiersRequestTypeDef]
    ) -> BatchGetCustomDataIdentifiersResponseTypeDef:
        """
        Retrieves information about one or more custom data identifiers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/batch_get_custom_data_identifiers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#batch_get_custom_data_identifiers)
        """

    async def batch_update_automated_discovery_accounts(
        self, **kwargs: Unpack[BatchUpdateAutomatedDiscoveryAccountsRequestTypeDef]
    ) -> BatchUpdateAutomatedDiscoveryAccountsResponseTypeDef:
        """
        Changes the status of automated sensitive data discovery for one or more
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/batch_update_automated_discovery_accounts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#batch_update_automated_discovery_accounts)
        """

    async def create_allow_list(
        self, **kwargs: Unpack[CreateAllowListRequestTypeDef]
    ) -> CreateAllowListResponseTypeDef:
        """
        Creates and defines the settings for an allow list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/create_allow_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_allow_list)
        """

    async def create_classification_job(
        self, **kwargs: Unpack[CreateClassificationJobRequestTypeDef]
    ) -> CreateClassificationJobResponseTypeDef:
        """
        Creates and defines the settings for a classification job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/create_classification_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_classification_job)
        """

    async def create_custom_data_identifier(
        self, **kwargs: Unpack[CreateCustomDataIdentifierRequestTypeDef]
    ) -> CreateCustomDataIdentifierResponseTypeDef:
        """
        Creates and defines the criteria and other settings for a custom data
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/create_custom_data_identifier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_custom_data_identifier)
        """

    async def create_findings_filter(
        self, **kwargs: Unpack[CreateFindingsFilterRequestTypeDef]
    ) -> CreateFindingsFilterResponseTypeDef:
        """
        Creates and defines the criteria and other settings for a findings filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/create_findings_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_findings_filter)
        """

    async def create_invitations(
        self, **kwargs: Unpack[CreateInvitationsRequestTypeDef]
    ) -> CreateInvitationsResponseTypeDef:
        """
        Sends an Amazon Macie membership invitation to one or more accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/create_invitations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_invitations)
        """

    async def create_member(
        self, **kwargs: Unpack[CreateMemberRequestTypeDef]
    ) -> CreateMemberResponseTypeDef:
        """
        Associates an account with an Amazon Macie administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/create_member.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_member)
        """

    async def create_sample_findings(
        self, **kwargs: Unpack[CreateSampleFindingsRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates sample findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/create_sample_findings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#create_sample_findings)
        """

    async def decline_invitations(
        self, **kwargs: Unpack[DeclineInvitationsRequestTypeDef]
    ) -> DeclineInvitationsResponseTypeDef:
        """
        Declines Amazon Macie membership invitations that were received from specific
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/decline_invitations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#decline_invitations)
        """

    async def delete_allow_list(
        self, **kwargs: Unpack[DeleteAllowListRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an allow list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/delete_allow_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_allow_list)
        """

    async def delete_custom_data_identifier(
        self, **kwargs: Unpack[DeleteCustomDataIdentifierRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Soft deletes a custom data identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/delete_custom_data_identifier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_custom_data_identifier)
        """

    async def delete_findings_filter(
        self, **kwargs: Unpack[DeleteFindingsFilterRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a findings filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/delete_findings_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_findings_filter)
        """

    async def delete_invitations(
        self, **kwargs: Unpack[DeleteInvitationsRequestTypeDef]
    ) -> DeleteInvitationsResponseTypeDef:
        """
        Deletes Amazon Macie membership invitations that were received from specific
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/delete_invitations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_invitations)
        """

    async def delete_member(self, **kwargs: Unpack[DeleteMemberRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the association between an Amazon Macie administrator account and an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/delete_member.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#delete_member)
        """

    async def describe_buckets(
        self, **kwargs: Unpack[DescribeBucketsRequestTypeDef]
    ) -> DescribeBucketsResponseTypeDef:
        """
        Retrieves (queries) statistical data and other information about one or more S3
        buckets that Amazon Macie monitors and analyzes for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/describe_buckets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#describe_buckets)
        """

    async def describe_classification_job(
        self, **kwargs: Unpack[DescribeClassificationJobRequestTypeDef]
    ) -> DescribeClassificationJobResponseTypeDef:
        """
        Retrieves the status and settings for a classification job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/describe_classification_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#describe_classification_job)
        """

    async def describe_organization_configuration(
        self,
    ) -> DescribeOrganizationConfigurationResponseTypeDef:
        """
        Retrieves the Amazon Macie configuration settings for an organization in
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/describe_organization_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#describe_organization_configuration)
        """

    async def disable_macie(self) -> Dict[str, Any]:
        """
        Disables Amazon Macie and deletes all settings and resources for a Macie
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/disable_macie.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disable_macie)
        """

    async def disable_organization_admin_account(
        self, **kwargs: Unpack[DisableOrganizationAdminAccountRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disables an account as the delegated Amazon Macie administrator account for an
        organization in Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/disable_organization_admin_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disable_organization_admin_account)
        """

    async def disassociate_from_administrator_account(self) -> Dict[str, Any]:
        """
        Disassociates a member account from its Amazon Macie administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/disassociate_from_administrator_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disassociate_from_administrator_account)
        """

    async def disassociate_from_master_account(self) -> Dict[str, Any]:
        """
        (Deprecated) Disassociates a member account from its Amazon Macie administrator
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/disassociate_from_master_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disassociate_from_master_account)
        """

    async def disassociate_member(
        self, **kwargs: Unpack[DisassociateMemberRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates an Amazon Macie administrator account from a member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/disassociate_member.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#disassociate_member)
        """

    async def enable_macie(self, **kwargs: Unpack[EnableMacieRequestTypeDef]) -> Dict[str, Any]:
        """
        Enables Amazon Macie and specifies the configuration settings for a Macie
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/enable_macie.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#enable_macie)
        """

    async def enable_organization_admin_account(
        self, **kwargs: Unpack[EnableOrganizationAdminAccountRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Designates an account as the delegated Amazon Macie administrator account for
        an organization in Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/enable_organization_admin_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#enable_organization_admin_account)
        """

    async def get_administrator_account(self) -> GetAdministratorAccountResponseTypeDef:
        """
        Retrieves information about the Amazon Macie administrator account for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_administrator_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_administrator_account)
        """

    async def get_allow_list(
        self, **kwargs: Unpack[GetAllowListRequestTypeDef]
    ) -> GetAllowListResponseTypeDef:
        """
        Retrieves the settings and status of an allow list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_allow_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_allow_list)
        """

    async def get_automated_discovery_configuration(
        self,
    ) -> GetAutomatedDiscoveryConfigurationResponseTypeDef:
        """
        Retrieves the configuration settings and status of automated sensitive data
        discovery for an organization or standalone account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_automated_discovery_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_automated_discovery_configuration)
        """

    async def get_bucket_statistics(
        self, **kwargs: Unpack[GetBucketStatisticsRequestTypeDef]
    ) -> GetBucketStatisticsResponseTypeDef:
        """
        Retrieves (queries) aggregated statistical data about all the S3 buckets that
        Amazon Macie monitors and analyzes for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_bucket_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_bucket_statistics)
        """

    async def get_classification_export_configuration(
        self,
    ) -> GetClassificationExportConfigurationResponseTypeDef:
        """
        Retrieves the configuration settings for storing data classification results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_classification_export_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_classification_export_configuration)
        """

    async def get_classification_scope(
        self, **kwargs: Unpack[GetClassificationScopeRequestTypeDef]
    ) -> GetClassificationScopeResponseTypeDef:
        """
        Retrieves the classification scope settings for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_classification_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_classification_scope)
        """

    async def get_custom_data_identifier(
        self, **kwargs: Unpack[GetCustomDataIdentifierRequestTypeDef]
    ) -> GetCustomDataIdentifierResponseTypeDef:
        """
        Retrieves the criteria and other settings for a custom data identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_custom_data_identifier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_custom_data_identifier)
        """

    async def get_finding_statistics(
        self, **kwargs: Unpack[GetFindingStatisticsRequestTypeDef]
    ) -> GetFindingStatisticsResponseTypeDef:
        """
        Retrieves (queries) aggregated statistical data about findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_finding_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_finding_statistics)
        """

    async def get_findings(
        self, **kwargs: Unpack[GetFindingsRequestTypeDef]
    ) -> GetFindingsResponseTypeDef:
        """
        Retrieves the details of one or more findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_findings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_findings)
        """

    async def get_findings_filter(
        self, **kwargs: Unpack[GetFindingsFilterRequestTypeDef]
    ) -> GetFindingsFilterResponseTypeDef:
        """
        Retrieves the criteria and other settings for a findings filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_findings_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_findings_filter)
        """

    async def get_findings_publication_configuration(
        self,
    ) -> GetFindingsPublicationConfigurationResponseTypeDef:
        """
        Retrieves the configuration settings for publishing findings to Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_findings_publication_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_findings_publication_configuration)
        """

    async def get_invitations_count(self) -> GetInvitationsCountResponseTypeDef:
        """
        Retrieves the count of Amazon Macie membership invitations that were received
        by an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_invitations_count.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_invitations_count)
        """

    async def get_macie_session(self) -> GetMacieSessionResponseTypeDef:
        """
        Retrieves the status and configuration settings for an Amazon Macie account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_macie_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_macie_session)
        """

    async def get_master_account(self) -> GetMasterAccountResponseTypeDef:
        """
        (Deprecated) Retrieves information about the Amazon Macie administrator account
        for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_master_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_master_account)
        """

    async def get_member(
        self, **kwargs: Unpack[GetMemberRequestTypeDef]
    ) -> GetMemberResponseTypeDef:
        """
        Retrieves information about an account that's associated with an Amazon Macie
        administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_member.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_member)
        """

    async def get_resource_profile(
        self, **kwargs: Unpack[GetResourceProfileRequestTypeDef]
    ) -> GetResourceProfileResponseTypeDef:
        """
        Retrieves (queries) sensitive data discovery statistics and the sensitivity
        score for an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_resource_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_resource_profile)
        """

    async def get_reveal_configuration(self) -> GetRevealConfigurationResponseTypeDef:
        """
        Retrieves the status and configuration settings for retrieving occurrences of
        sensitive data reported by findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_reveal_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_reveal_configuration)
        """

    async def get_sensitive_data_occurrences(
        self, **kwargs: Unpack[GetSensitiveDataOccurrencesRequestTypeDef]
    ) -> GetSensitiveDataOccurrencesResponseTypeDef:
        """
        Retrieves occurrences of sensitive data reported by a finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_sensitive_data_occurrences.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_sensitive_data_occurrences)
        """

    async def get_sensitive_data_occurrences_availability(
        self, **kwargs: Unpack[GetSensitiveDataOccurrencesAvailabilityRequestTypeDef]
    ) -> GetSensitiveDataOccurrencesAvailabilityResponseTypeDef:
        """
        Checks whether occurrences of sensitive data can be retrieved for a finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_sensitive_data_occurrences_availability.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_sensitive_data_occurrences_availability)
        """

    async def get_sensitivity_inspection_template(
        self, **kwargs: Unpack[GetSensitivityInspectionTemplateRequestTypeDef]
    ) -> GetSensitivityInspectionTemplateResponseTypeDef:
        """
        Retrieves the settings for the sensitivity inspection template for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_sensitivity_inspection_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_sensitivity_inspection_template)
        """

    async def get_usage_statistics(
        self, **kwargs: Unpack[GetUsageStatisticsRequestTypeDef]
    ) -> GetUsageStatisticsResponseTypeDef:
        """
        Retrieves (queries) quotas and aggregated usage data for one or more accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_usage_statistics.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_usage_statistics)
        """

    async def get_usage_totals(
        self, **kwargs: Unpack[GetUsageTotalsRequestTypeDef]
    ) -> GetUsageTotalsResponseTypeDef:
        """
        Retrieves (queries) aggregated usage data for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_usage_totals.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_usage_totals)
        """

    async def list_allow_lists(
        self, **kwargs: Unpack[ListAllowListsRequestTypeDef]
    ) -> ListAllowListsResponseTypeDef:
        """
        Retrieves a subset of information about all the allow lists for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_allow_lists.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_allow_lists)
        """

    async def list_automated_discovery_accounts(
        self, **kwargs: Unpack[ListAutomatedDiscoveryAccountsRequestTypeDef]
    ) -> ListAutomatedDiscoveryAccountsResponseTypeDef:
        """
        Retrieves the status of automated sensitive data discovery for one or more
        accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_automated_discovery_accounts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_automated_discovery_accounts)
        """

    async def list_classification_jobs(
        self, **kwargs: Unpack[ListClassificationJobsRequestTypeDef]
    ) -> ListClassificationJobsResponseTypeDef:
        """
        Retrieves a subset of information about one or more classification jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_classification_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_classification_jobs)
        """

    async def list_classification_scopes(
        self, **kwargs: Unpack[ListClassificationScopesRequestTypeDef]
    ) -> ListClassificationScopesResponseTypeDef:
        """
        Retrieves a subset of information about the classification scope for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_classification_scopes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_classification_scopes)
        """

    async def list_custom_data_identifiers(
        self, **kwargs: Unpack[ListCustomDataIdentifiersRequestTypeDef]
    ) -> ListCustomDataIdentifiersResponseTypeDef:
        """
        Retrieves a subset of information about the custom data identifiers for an
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_custom_data_identifiers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_custom_data_identifiers)
        """

    async def list_findings(
        self, **kwargs: Unpack[ListFindingsRequestTypeDef]
    ) -> ListFindingsResponseTypeDef:
        """
        Retrieves a subset of information about one or more findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_findings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_findings)
        """

    async def list_findings_filters(
        self, **kwargs: Unpack[ListFindingsFiltersRequestTypeDef]
    ) -> ListFindingsFiltersResponseTypeDef:
        """
        Retrieves a subset of information about all the findings filters for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_findings_filters.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_findings_filters)
        """

    async def list_invitations(
        self, **kwargs: Unpack[ListInvitationsRequestTypeDef]
    ) -> ListInvitationsResponseTypeDef:
        """
        Retrieves information about Amazon Macie membership invitations that were
        received by an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_invitations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_invitations)
        """

    async def list_managed_data_identifiers(
        self, **kwargs: Unpack[ListManagedDataIdentifiersRequestTypeDef]
    ) -> ListManagedDataIdentifiersResponseTypeDef:
        """
        Retrieves information about all the managed data identifiers that Amazon Macie
        currently provides.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_managed_data_identifiers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_managed_data_identifiers)
        """

    async def list_members(
        self, **kwargs: Unpack[ListMembersRequestTypeDef]
    ) -> ListMembersResponseTypeDef:
        """
        Retrieves information about the accounts that are associated with an Amazon
        Macie administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_members.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_members)
        """

    async def list_organization_admin_accounts(
        self, **kwargs: Unpack[ListOrganizationAdminAccountsRequestTypeDef]
    ) -> ListOrganizationAdminAccountsResponseTypeDef:
        """
        Retrieves information about the delegated Amazon Macie administrator account
        for an organization in Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_organization_admin_accounts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_organization_admin_accounts)
        """

    async def list_resource_profile_artifacts(
        self, **kwargs: Unpack[ListResourceProfileArtifactsRequestTypeDef]
    ) -> ListResourceProfileArtifactsResponseTypeDef:
        """
        Retrieves information about objects that Amazon Macie selected from an S3
        bucket for automated sensitive data discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_resource_profile_artifacts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_resource_profile_artifacts)
        """

    async def list_resource_profile_detections(
        self, **kwargs: Unpack[ListResourceProfileDetectionsRequestTypeDef]
    ) -> ListResourceProfileDetectionsResponseTypeDef:
        """
        Retrieves information about the types and amount of sensitive data that Amazon
        Macie found in an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_resource_profile_detections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_resource_profile_detections)
        """

    async def list_sensitivity_inspection_templates(
        self, **kwargs: Unpack[ListSensitivityInspectionTemplatesRequestTypeDef]
    ) -> ListSensitivityInspectionTemplatesResponseTypeDef:
        """
        Retrieves a subset of information about the sensitivity inspection template for
        an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_sensitivity_inspection_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_sensitivity_inspection_templates)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the tags (keys and values) that are associated with an Amazon Macie
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#list_tags_for_resource)
        """

    async def put_classification_export_configuration(
        self, **kwargs: Unpack[PutClassificationExportConfigurationRequestTypeDef]
    ) -> PutClassificationExportConfigurationResponseTypeDef:
        """
        Adds or updates the configuration settings for storing data classification
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/put_classification_export_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#put_classification_export_configuration)
        """

    async def put_findings_publication_configuration(
        self, **kwargs: Unpack[PutFindingsPublicationConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration settings for publishing findings to Security Hub.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/put_findings_publication_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#put_findings_publication_configuration)
        """

    async def search_resources(
        self, **kwargs: Unpack[SearchResourcesRequestTypeDef]
    ) -> SearchResourcesResponseTypeDef:
        """
        Retrieves (queries) statistical data and other information about Amazon Web
        Services resources that Amazon Macie monitors and analyzes for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/search_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#search_resources)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or updates one or more tags (keys and values) that are associated with an
        Amazon Macie resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#tag_resource)
        """

    async def test_custom_data_identifier(
        self, **kwargs: Unpack[TestCustomDataIdentifierRequestTypeDef]
    ) -> TestCustomDataIdentifierResponseTypeDef:
        """
        Tests criteria for a custom data identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/test_custom_data_identifier.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#test_custom_data_identifier)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags (keys and values) from an Amazon Macie resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#untag_resource)
        """

    async def update_allow_list(
        self, **kwargs: Unpack[UpdateAllowListRequestTypeDef]
    ) -> UpdateAllowListResponseTypeDef:
        """
        Updates the settings for an allow list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_allow_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_allow_list)
        """

    async def update_automated_discovery_configuration(
        self, **kwargs: Unpack[UpdateAutomatedDiscoveryConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the configuration settings and status of automated sensitive data
        discovery for an organization or standalone account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_automated_discovery_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_automated_discovery_configuration)
        """

    async def update_classification_job(
        self, **kwargs: Unpack[UpdateClassificationJobRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the status of a classification job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_classification_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_classification_job)
        """

    async def update_classification_scope(
        self, **kwargs: Unpack[UpdateClassificationScopeRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the classification scope settings for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_classification_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_classification_scope)
        """

    async def update_findings_filter(
        self, **kwargs: Unpack[UpdateFindingsFilterRequestTypeDef]
    ) -> UpdateFindingsFilterResponseTypeDef:
        """
        Updates the criteria and other settings for a findings filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_findings_filter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_findings_filter)
        """

    async def update_macie_session(
        self, **kwargs: Unpack[UpdateMacieSessionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Suspends or re-enables Amazon Macie, or updates the configuration settings for
        a Macie account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_macie_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_macie_session)
        """

    async def update_member_session(
        self, **kwargs: Unpack[UpdateMemberSessionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Enables an Amazon Macie administrator to suspend or re-enable Macie for a
        member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_member_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_member_session)
        """

    async def update_organization_configuration(
        self, **kwargs: Unpack[UpdateOrganizationConfigurationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the Amazon Macie configuration settings for an organization in
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_organization_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_organization_configuration)
        """

    async def update_resource_profile(
        self, **kwargs: Unpack[UpdateResourceProfileRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the sensitivity score for an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_resource_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_resource_profile)
        """

    async def update_resource_profile_detections(
        self, **kwargs: Unpack[UpdateResourceProfileDetectionsRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the sensitivity scoring settings for an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_resource_profile_detections.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_resource_profile_detections)
        """

    async def update_reveal_configuration(
        self, **kwargs: Unpack[UpdateRevealConfigurationRequestTypeDef]
    ) -> UpdateRevealConfigurationResponseTypeDef:
        """
        Updates the status and configuration settings for retrieving occurrences of
        sensitive data reported by findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_reveal_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_reveal_configuration)
        """

    async def update_sensitivity_inspection_template(
        self, **kwargs: Unpack[UpdateSensitivityInspectionTemplateRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the settings for the sensitivity inspection template for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/update_sensitivity_inspection_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#update_sensitivity_inspection_template)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_buckets"]
    ) -> DescribeBucketsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_usage_statistics"]
    ) -> GetUsageStatisticsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_allow_lists"]
    ) -> ListAllowListsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_automated_discovery_accounts"]
    ) -> ListAutomatedDiscoveryAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_classification_jobs"]
    ) -> ListClassificationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_classification_scopes"]
    ) -> ListClassificationScopesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_custom_data_identifiers"]
    ) -> ListCustomDataIdentifiersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_findings_filters"]
    ) -> ListFindingsFiltersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_findings"]
    ) -> ListFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_invitations"]
    ) -> ListInvitationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_data_identifiers"]
    ) -> ListManagedDataIdentifiersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_members"]
    ) -> ListMembersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_organization_admin_accounts"]
    ) -> ListOrganizationAdminAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_profile_artifacts"]
    ) -> ListResourceProfileArtifactsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_profile_detections"]
    ) -> ListResourceProfileDetectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sensitivity_inspection_templates"]
    ) -> ListSensitivityInspectionTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_resources"]
    ) -> SearchResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["finding_revealed"]
    ) -> FindingRevealedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/macie2.html#Macie2.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_macie2/client/)
        """
