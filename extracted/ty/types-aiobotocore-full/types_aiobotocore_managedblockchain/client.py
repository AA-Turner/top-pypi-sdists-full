"""
Type annotations for managedblockchain service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_managedblockchain.client import ManagedBlockchainClient

    session = get_session()
    async with session.create_client("managedblockchain") as client:
        client: ManagedBlockchainClient
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

from .paginator import ListAccessorsPaginator
from .type_defs import (
    CreateAccessorInputTypeDef,
    CreateAccessorOutputTypeDef,
    CreateMemberInputTypeDef,
    CreateMemberOutputTypeDef,
    CreateNetworkInputTypeDef,
    CreateNetworkOutputTypeDef,
    CreateNodeInputTypeDef,
    CreateNodeOutputTypeDef,
    CreateProposalInputTypeDef,
    CreateProposalOutputTypeDef,
    DeleteAccessorInputTypeDef,
    DeleteMemberInputTypeDef,
    DeleteNodeInputTypeDef,
    GetAccessorInputTypeDef,
    GetAccessorOutputTypeDef,
    GetMemberInputTypeDef,
    GetMemberOutputTypeDef,
    GetNetworkInputTypeDef,
    GetNetworkOutputTypeDef,
    GetNodeInputTypeDef,
    GetNodeOutputTypeDef,
    GetProposalInputTypeDef,
    GetProposalOutputTypeDef,
    ListAccessorsInputTypeDef,
    ListAccessorsOutputTypeDef,
    ListInvitationsInputTypeDef,
    ListInvitationsOutputTypeDef,
    ListMembersInputTypeDef,
    ListMembersOutputTypeDef,
    ListNetworksInputTypeDef,
    ListNetworksOutputTypeDef,
    ListNodesInputTypeDef,
    ListNodesOutputTypeDef,
    ListProposalsInputTypeDef,
    ListProposalsOutputTypeDef,
    ListProposalVotesInputTypeDef,
    ListProposalVotesOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RejectInvitationInputTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateMemberInputTypeDef,
    UpdateNodeInputTypeDef,
    VoteOnProposalInputTypeDef,
)

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


__all__ = ("ManagedBlockchainClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IllegalActionException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceNotReadyException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class ManagedBlockchainClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ManagedBlockchainClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#generate_presigned_url)
        """

    async def create_accessor(
        self, **kwargs: Unpack[CreateAccessorInputTypeDef]
    ) -> CreateAccessorOutputTypeDef:
        """
        Creates a new accessor for use with Amazon Managed Blockchain service that
        supports token based access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_accessor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_accessor)
        """

    async def create_member(
        self, **kwargs: Unpack[CreateMemberInputTypeDef]
    ) -> CreateMemberOutputTypeDef:
        """
        Creates a member within a Managed Blockchain network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_member.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_member)
        """

    async def create_network(
        self, **kwargs: Unpack[CreateNetworkInputTypeDef]
    ) -> CreateNetworkOutputTypeDef:
        """
        Creates a new blockchain network using Amazon Managed Blockchain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_network)
        """

    async def create_node(
        self, **kwargs: Unpack[CreateNodeInputTypeDef]
    ) -> CreateNodeOutputTypeDef:
        """
        Creates a node on the specified blockchain network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_node)
        """

    async def create_proposal(
        self, **kwargs: Unpack[CreateProposalInputTypeDef]
    ) -> CreateProposalOutputTypeDef:
        """
        Creates a proposal for a change to the network that other members of the
        network can vote on, for example, a proposal to add a new member to the
        network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/create_proposal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#create_proposal)
        """

    async def delete_accessor(self, **kwargs: Unpack[DeleteAccessorInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes an accessor that your Amazon Web Services account owns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/delete_accessor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#delete_accessor)
        """

    async def delete_member(self, **kwargs: Unpack[DeleteMemberInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/delete_member.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#delete_member)
        """

    async def delete_node(self, **kwargs: Unpack[DeleteNodeInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes a node that your Amazon Web Services account owns.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/delete_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#delete_node)
        """

    async def get_accessor(
        self, **kwargs: Unpack[GetAccessorInputTypeDef]
    ) -> GetAccessorOutputTypeDef:
        """
        Returns detailed information about an accessor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_accessor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_accessor)
        """

    async def get_member(self, **kwargs: Unpack[GetMemberInputTypeDef]) -> GetMemberOutputTypeDef:
        """
        Returns detailed information about a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_member.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_member)
        """

    async def get_network(
        self, **kwargs: Unpack[GetNetworkInputTypeDef]
    ) -> GetNetworkOutputTypeDef:
        """
        Returns detailed information about a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_network.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_network)
        """

    async def get_node(self, **kwargs: Unpack[GetNodeInputTypeDef]) -> GetNodeOutputTypeDef:
        """
        Returns detailed information about a node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_node)
        """

    async def get_proposal(
        self, **kwargs: Unpack[GetProposalInputTypeDef]
    ) -> GetProposalOutputTypeDef:
        """
        Returns detailed information about a proposal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_proposal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_proposal)
        """

    async def list_accessors(
        self, **kwargs: Unpack[ListAccessorsInputTypeDef]
    ) -> ListAccessorsOutputTypeDef:
        """
        Returns a list of the accessors and their properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_accessors.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_accessors)
        """

    async def list_invitations(
        self, **kwargs: Unpack[ListInvitationsInputTypeDef]
    ) -> ListInvitationsOutputTypeDef:
        """
        Returns a list of all invitations for the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_invitations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_invitations)
        """

    async def list_members(
        self, **kwargs: Unpack[ListMembersInputTypeDef]
    ) -> ListMembersOutputTypeDef:
        """
        Returns a list of the members in a network and properties of their
        configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_members.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_members)
        """

    async def list_networks(
        self, **kwargs: Unpack[ListNetworksInputTypeDef]
    ) -> ListNetworksOutputTypeDef:
        """
        Returns information about the networks in which the current Amazon Web Services
        account participates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_networks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_networks)
        """

    async def list_nodes(self, **kwargs: Unpack[ListNodesInputTypeDef]) -> ListNodesOutputTypeDef:
        """
        Returns information about the nodes within a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_nodes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_nodes)
        """

    async def list_proposal_votes(
        self, **kwargs: Unpack[ListProposalVotesInputTypeDef]
    ) -> ListProposalVotesOutputTypeDef:
        """
        Returns the list of votes for a specified proposal, including the value of each
        vote and the unique identifier of the member that cast the vote.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_proposal_votes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_proposal_votes)
        """

    async def list_proposals(
        self, **kwargs: Unpack[ListProposalsInputTypeDef]
    ) -> ListProposalsOutputTypeDef:
        """
        Returns a list of proposals for the network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_proposals.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_proposals)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#list_tags_for_resource)
        """

    async def reject_invitation(
        self, **kwargs: Unpack[RejectInvitationInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Rejects an invitation to join a network.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/reject_invitation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#reject_invitation)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or overwrites the specified tags for the specified Amazon Managed
        Blockchain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified tags from the Amazon Managed Blockchain resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#untag_resource)
        """

    async def update_member(self, **kwargs: Unpack[UpdateMemberInputTypeDef]) -> Dict[str, Any]:
        """
        Updates a member configuration with new parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/update_member.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#update_member)
        """

    async def update_node(self, **kwargs: Unpack[UpdateNodeInputTypeDef]) -> Dict[str, Any]:
        """
        Updates a node configuration with new parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/update_node.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#update_node)
        """

    async def vote_on_proposal(
        self, **kwargs: Unpack[VoteOnProposalInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Casts a vote for a specified <code>ProposalId</code> on behalf of a member.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/vote_on_proposal.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#vote_on_proposal)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_accessors"]
    ) -> ListAccessorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain.html#ManagedBlockchain.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/client/)
        """
