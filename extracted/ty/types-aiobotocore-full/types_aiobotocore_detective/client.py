"""
Type annotations for detective service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_detective.client import DetectiveClient

    session = get_session()
    async with session.create_client("detective") as client:
        client: DetectiveClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    AcceptInvitationRequestTypeDef,
    BatchGetGraphMemberDatasourcesRequestTypeDef,
    BatchGetGraphMemberDatasourcesResponseTypeDef,
    BatchGetMembershipDatasourcesRequestTypeDef,
    BatchGetMembershipDatasourcesResponseTypeDef,
    CreateGraphRequestTypeDef,
    CreateGraphResponseTypeDef,
    CreateMembersRequestTypeDef,
    CreateMembersResponseTypeDef,
    DeleteGraphRequestTypeDef,
    DeleteMembersRequestTypeDef,
    DeleteMembersResponseTypeDef,
    DescribeOrganizationConfigurationRequestTypeDef,
    DescribeOrganizationConfigurationResponseTypeDef,
    DisassociateMembershipRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableOrganizationAdminAccountRequestTypeDef,
    GetInvestigationRequestTypeDef,
    GetInvestigationResponseTypeDef,
    GetMembersRequestTypeDef,
    GetMembersResponseTypeDef,
    ListDatasourcePackagesRequestTypeDef,
    ListDatasourcePackagesResponseTypeDef,
    ListGraphsRequestTypeDef,
    ListGraphsResponseTypeDef,
    ListIndicatorsRequestTypeDef,
    ListIndicatorsResponseTypeDef,
    ListInvestigationsRequestTypeDef,
    ListInvestigationsResponseTypeDef,
    ListInvitationsRequestTypeDef,
    ListInvitationsResponseTypeDef,
    ListMembersRequestTypeDef,
    ListMembersResponseTypeDef,
    ListOrganizationAdminAccountsRequestTypeDef,
    ListOrganizationAdminAccountsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RejectInvitationRequestTypeDef,
    StartInvestigationRequestTypeDef,
    StartInvestigationResponseTypeDef,
    StartMonitoringMemberRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDatasourcePackagesRequestTypeDef,
    UpdateInvestigationStateRequestTypeDef,
    UpdateOrganizationConfigurationRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("DetectiveClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class DetectiveClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DetectiveClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#generate_presigned_url)
        """

    async def accept_invitation(
        self, **kwargs: Unpack[AcceptInvitationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Accepts an invitation for the member account to contribute data to a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/accept_invitation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#accept_invitation)
        """

    async def batch_get_graph_member_datasources(
        self, **kwargs: Unpack[BatchGetGraphMemberDatasourcesRequestTypeDef]
    ) -> BatchGetGraphMemberDatasourcesResponseTypeDef:
        """
        Gets data source package information for the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/batch_get_graph_member_datasources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#batch_get_graph_member_datasources)
        """

    async def batch_get_membership_datasources(
        self, **kwargs: Unpack[BatchGetMembershipDatasourcesRequestTypeDef]
    ) -> BatchGetMembershipDatasourcesResponseTypeDef:
        """
        Gets information on the data source package history for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/batch_get_membership_datasources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#batch_get_membership_datasources)
        """

    async def create_graph(
        self, **kwargs: Unpack[CreateGraphRequestTypeDef]
    ) -> CreateGraphResponseTypeDef:
        """
        Creates a new behavior graph for the calling account, and sets that account as
        the administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/create_graph.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#create_graph)
        """

    async def create_members(
        self, **kwargs: Unpack[CreateMembersRequestTypeDef]
    ) -> CreateMembersResponseTypeDef:
        """
        <code>CreateMembers</code> is used to send invitations to accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/create_members.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#create_members)
        """

    async def delete_graph(
        self, **kwargs: Unpack[DeleteGraphRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables the specified behavior graph and queues it to be deleted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/delete_graph.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#delete_graph)
        """

    async def delete_members(
        self, **kwargs: Unpack[DeleteMembersRequestTypeDef]
    ) -> DeleteMembersResponseTypeDef:
        """
        Removes the specified member accounts from the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/delete_members.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#delete_members)
        """

    async def describe_organization_configuration(
        self, **kwargs: Unpack[DescribeOrganizationConfigurationRequestTypeDef]
    ) -> DescribeOrganizationConfigurationResponseTypeDef:
        """
        Returns information about the configuration for the organization behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/describe_organization_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#describe_organization_configuration)
        """

    async def disable_organization_admin_account(self) -> EmptyResponseMetadataTypeDef:
        """
        Removes the Detective administrator account in the current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/disable_organization_admin_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#disable_organization_admin_account)
        """

    async def disassociate_membership(
        self, **kwargs: Unpack[DisassociateMembershipRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the member account from the specified behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/disassociate_membership.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#disassociate_membership)
        """

    async def enable_organization_admin_account(
        self, **kwargs: Unpack[EnableOrganizationAdminAccountRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Designates the Detective administrator account for the organization in the
        current Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/enable_organization_admin_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#enable_organization_admin_account)
        """

    async def get_investigation(
        self, **kwargs: Unpack[GetInvestigationRequestTypeDef]
    ) -> GetInvestigationResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/get_investigation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#get_investigation)
        """

    async def get_members(
        self, **kwargs: Unpack[GetMembersRequestTypeDef]
    ) -> GetMembersResponseTypeDef:
        """
        Returns the membership details for specified member accounts for a behavior
        graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/get_members.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#get_members)
        """

    async def list_datasource_packages(
        self, **kwargs: Unpack[ListDatasourcePackagesRequestTypeDef]
    ) -> ListDatasourcePackagesResponseTypeDef:
        """
        Lists data source packages in the behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_datasource_packages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_datasource_packages)
        """

    async def list_graphs(
        self, **kwargs: Unpack[ListGraphsRequestTypeDef]
    ) -> ListGraphsResponseTypeDef:
        """
        Returns the list of behavior graphs that the calling account is an
        administrator account of.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_graphs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_graphs)
        """

    async def list_indicators(
        self, **kwargs: Unpack[ListIndicatorsRequestTypeDef]
    ) -> ListIndicatorsResponseTypeDef:
        """
        Gets the indicators from an investigation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_indicators.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_indicators)
        """

    async def list_investigations(
        self, **kwargs: Unpack[ListInvestigationsRequestTypeDef]
    ) -> ListInvestigationsResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_investigations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_investigations)
        """

    async def list_invitations(
        self, **kwargs: Unpack[ListInvitationsRequestTypeDef]
    ) -> ListInvitationsResponseTypeDef:
        """
        Retrieves the list of open and accepted behavior graph invitations for the
        member account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_invitations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_invitations)
        """

    async def list_members(
        self, **kwargs: Unpack[ListMembersRequestTypeDef]
    ) -> ListMembersResponseTypeDef:
        """
        Retrieves the list of member accounts for a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_members.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_members)
        """

    async def list_organization_admin_accounts(
        self, **kwargs: Unpack[ListOrganizationAdminAccountsRequestTypeDef]
    ) -> ListOrganizationAdminAccountsResponseTypeDef:
        """
        Returns information about the Detective administrator account for an
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_organization_admin_accounts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_organization_admin_accounts)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the tag values that are assigned to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#list_tags_for_resource)
        """

    async def reject_invitation(
        self, **kwargs: Unpack[RejectInvitationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Rejects an invitation to contribute the account data to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/reject_invitation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#reject_invitation)
        """

    async def start_investigation(
        self, **kwargs: Unpack[StartInvestigationRequestTypeDef]
    ) -> StartInvestigationResponseTypeDef:
        """
        Detective investigations lets you investigate IAM users and IAM roles using
        indicators of compromise.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/start_investigation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#start_investigation)
        """

    async def start_monitoring_member(
        self, **kwargs: Unpack[StartMonitoringMemberRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sends a request to enable data ingest for a member account that has a status of
        <code>ACCEPTED_BUT_DISABLED</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/start_monitoring_member.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#start_monitoring_member)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Applies tag values to a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from a behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#untag_resource)
        """

    async def update_datasource_packages(
        self, **kwargs: Unpack[UpdateDatasourcePackagesRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Starts a data source package for the Detective behavior graph.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/update_datasource_packages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#update_datasource_packages)
        """

    async def update_investigation_state(
        self, **kwargs: Unpack[UpdateInvestigationStateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the state of an investigation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/update_investigation_state.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#update_investigation_state)
        """

    async def update_organization_configuration(
        self, **kwargs: Unpack[UpdateOrganizationConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the configuration for the Organizations integration in the current
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective/client/update_organization_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/#update_organization_configuration)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/detective.html#Detective.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/client/)
        """
