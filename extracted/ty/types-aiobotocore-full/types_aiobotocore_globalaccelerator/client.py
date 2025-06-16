"""
Type annotations for globalaccelerator service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_globalaccelerator.client import GlobalAcceleratorClient

    session = get_session()
    async with session.create_client("globalaccelerator") as client:
        client: GlobalAcceleratorClient
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
    ListAcceleratorsPaginator,
    ListByoipCidrsPaginator,
    ListCrossAccountAttachmentsPaginator,
    ListCrossAccountResourcesPaginator,
    ListCustomRoutingAcceleratorsPaginator,
    ListCustomRoutingEndpointGroupsPaginator,
    ListCustomRoutingListenersPaginator,
    ListCustomRoutingPortMappingsByDestinationPaginator,
    ListCustomRoutingPortMappingsPaginator,
    ListEndpointGroupsPaginator,
    ListListenersPaginator,
)
from .type_defs import (
    AddCustomRoutingEndpointsRequestTypeDef,
    AddCustomRoutingEndpointsResponseTypeDef,
    AddEndpointsRequestTypeDef,
    AddEndpointsResponseTypeDef,
    AdvertiseByoipCidrRequestTypeDef,
    AdvertiseByoipCidrResponseTypeDef,
    AllowCustomRoutingTrafficRequestTypeDef,
    CreateAcceleratorRequestTypeDef,
    CreateAcceleratorResponseTypeDef,
    CreateCrossAccountAttachmentRequestTypeDef,
    CreateCrossAccountAttachmentResponseTypeDef,
    CreateCustomRoutingAcceleratorRequestTypeDef,
    CreateCustomRoutingAcceleratorResponseTypeDef,
    CreateCustomRoutingEndpointGroupRequestTypeDef,
    CreateCustomRoutingEndpointGroupResponseTypeDef,
    CreateCustomRoutingListenerRequestTypeDef,
    CreateCustomRoutingListenerResponseTypeDef,
    CreateEndpointGroupRequestTypeDef,
    CreateEndpointGroupResponseTypeDef,
    CreateListenerRequestTypeDef,
    CreateListenerResponseTypeDef,
    DeleteAcceleratorRequestTypeDef,
    DeleteCrossAccountAttachmentRequestTypeDef,
    DeleteCustomRoutingAcceleratorRequestTypeDef,
    DeleteCustomRoutingEndpointGroupRequestTypeDef,
    DeleteCustomRoutingListenerRequestTypeDef,
    DeleteEndpointGroupRequestTypeDef,
    DeleteListenerRequestTypeDef,
    DenyCustomRoutingTrafficRequestTypeDef,
    DeprovisionByoipCidrRequestTypeDef,
    DeprovisionByoipCidrResponseTypeDef,
    DescribeAcceleratorAttributesRequestTypeDef,
    DescribeAcceleratorAttributesResponseTypeDef,
    DescribeAcceleratorRequestTypeDef,
    DescribeAcceleratorResponseTypeDef,
    DescribeCrossAccountAttachmentRequestTypeDef,
    DescribeCrossAccountAttachmentResponseTypeDef,
    DescribeCustomRoutingAcceleratorAttributesRequestTypeDef,
    DescribeCustomRoutingAcceleratorAttributesResponseTypeDef,
    DescribeCustomRoutingAcceleratorRequestTypeDef,
    DescribeCustomRoutingAcceleratorResponseTypeDef,
    DescribeCustomRoutingEndpointGroupRequestTypeDef,
    DescribeCustomRoutingEndpointGroupResponseTypeDef,
    DescribeCustomRoutingListenerRequestTypeDef,
    DescribeCustomRoutingListenerResponseTypeDef,
    DescribeEndpointGroupRequestTypeDef,
    DescribeEndpointGroupResponseTypeDef,
    DescribeListenerRequestTypeDef,
    DescribeListenerResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ListAcceleratorsRequestTypeDef,
    ListAcceleratorsResponseTypeDef,
    ListByoipCidrsRequestTypeDef,
    ListByoipCidrsResponseTypeDef,
    ListCrossAccountAttachmentsRequestTypeDef,
    ListCrossAccountAttachmentsResponseTypeDef,
    ListCrossAccountResourceAccountsResponseTypeDef,
    ListCrossAccountResourcesRequestTypeDef,
    ListCrossAccountResourcesResponseTypeDef,
    ListCustomRoutingAcceleratorsRequestTypeDef,
    ListCustomRoutingAcceleratorsResponseTypeDef,
    ListCustomRoutingEndpointGroupsRequestTypeDef,
    ListCustomRoutingEndpointGroupsResponseTypeDef,
    ListCustomRoutingListenersRequestTypeDef,
    ListCustomRoutingListenersResponseTypeDef,
    ListCustomRoutingPortMappingsByDestinationRequestTypeDef,
    ListCustomRoutingPortMappingsByDestinationResponseTypeDef,
    ListCustomRoutingPortMappingsRequestTypeDef,
    ListCustomRoutingPortMappingsResponseTypeDef,
    ListEndpointGroupsRequestTypeDef,
    ListEndpointGroupsResponseTypeDef,
    ListListenersRequestTypeDef,
    ListListenersResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ProvisionByoipCidrRequestTypeDef,
    ProvisionByoipCidrResponseTypeDef,
    RemoveCustomRoutingEndpointsRequestTypeDef,
    RemoveEndpointsRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAcceleratorAttributesRequestTypeDef,
    UpdateAcceleratorAttributesResponseTypeDef,
    UpdateAcceleratorRequestTypeDef,
    UpdateAcceleratorResponseTypeDef,
    UpdateCrossAccountAttachmentRequestTypeDef,
    UpdateCrossAccountAttachmentResponseTypeDef,
    UpdateCustomRoutingAcceleratorAttributesRequestTypeDef,
    UpdateCustomRoutingAcceleratorAttributesResponseTypeDef,
    UpdateCustomRoutingAcceleratorRequestTypeDef,
    UpdateCustomRoutingAcceleratorResponseTypeDef,
    UpdateCustomRoutingListenerRequestTypeDef,
    UpdateCustomRoutingListenerResponseTypeDef,
    UpdateEndpointGroupRequestTypeDef,
    UpdateEndpointGroupResponseTypeDef,
    UpdateListenerRequestTypeDef,
    UpdateListenerResponseTypeDef,
    WithdrawByoipCidrRequestTypeDef,
    WithdrawByoipCidrResponseTypeDef,
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


__all__ = ("GlobalAcceleratorClient",)


class Exceptions(BaseClientExceptions):
    AcceleratorNotDisabledException: Type[BotocoreClientError]
    AcceleratorNotFoundException: Type[BotocoreClientError]
    AccessDeniedException: Type[BotocoreClientError]
    AssociatedEndpointGroupFoundException: Type[BotocoreClientError]
    AssociatedListenerFoundException: Type[BotocoreClientError]
    AttachmentNotFoundException: Type[BotocoreClientError]
    ByoipCidrNotFoundException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    EndpointAlreadyExistsException: Type[BotocoreClientError]
    EndpointGroupAlreadyExistsException: Type[BotocoreClientError]
    EndpointGroupNotFoundException: Type[BotocoreClientError]
    EndpointNotFoundException: Type[BotocoreClientError]
    IncorrectCidrStateException: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidPortRangeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ListenerNotFoundException: Type[BotocoreClientError]
    TransactionInProgressException: Type[BotocoreClientError]


class GlobalAcceleratorClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlobalAcceleratorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#generate_presigned_url)
        """

    async def add_custom_routing_endpoints(
        self, **kwargs: Unpack[AddCustomRoutingEndpointsRequestTypeDef]
    ) -> AddCustomRoutingEndpointsResponseTypeDef:
        """
        Associate a virtual private cloud (VPC) subnet endpoint with your custom
        routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/add_custom_routing_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#add_custom_routing_endpoints)
        """

    async def add_endpoints(
        self, **kwargs: Unpack[AddEndpointsRequestTypeDef]
    ) -> AddEndpointsResponseTypeDef:
        """
        Add endpoints to an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/add_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#add_endpoints)
        """

    async def advertise_byoip_cidr(
        self, **kwargs: Unpack[AdvertiseByoipCidrRequestTypeDef]
    ) -> AdvertiseByoipCidrResponseTypeDef:
        """
        Advertises an IPv4 address range that is provisioned for use with your Amazon
        Web Services resources through bring your own IP addresses (BYOIP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/advertise_byoip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#advertise_byoip_cidr)
        """

    async def allow_custom_routing_traffic(
        self, **kwargs: Unpack[AllowCustomRoutingTrafficRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the Amazon EC2 instance (destination) IP addresses and ports for a VPC
        subnet endpoint that can receive traffic for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/allow_custom_routing_traffic.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#allow_custom_routing_traffic)
        """

    async def create_accelerator(
        self, **kwargs: Unpack[CreateAcceleratorRequestTypeDef]
    ) -> CreateAcceleratorResponseTypeDef:
        """
        Create an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_accelerator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_accelerator)
        """

    async def create_cross_account_attachment(
        self, **kwargs: Unpack[CreateCrossAccountAttachmentRequestTypeDef]
    ) -> CreateCrossAccountAttachmentResponseTypeDef:
        """
        Create a cross-account attachment in Global Accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_cross_account_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_cross_account_attachment)
        """

    async def create_custom_routing_accelerator(
        self, **kwargs: Unpack[CreateCustomRoutingAcceleratorRequestTypeDef]
    ) -> CreateCustomRoutingAcceleratorResponseTypeDef:
        """
        Create a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_custom_routing_accelerator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_custom_routing_accelerator)
        """

    async def create_custom_routing_endpoint_group(
        self, **kwargs: Unpack[CreateCustomRoutingEndpointGroupRequestTypeDef]
    ) -> CreateCustomRoutingEndpointGroupResponseTypeDef:
        """
        Create an endpoint group for the specified listener for a custom routing
        accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_custom_routing_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_custom_routing_endpoint_group)
        """

    async def create_custom_routing_listener(
        self, **kwargs: Unpack[CreateCustomRoutingListenerRequestTypeDef]
    ) -> CreateCustomRoutingListenerResponseTypeDef:
        """
        Create a listener to process inbound connections from clients to a custom
        routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_custom_routing_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_custom_routing_listener)
        """

    async def create_endpoint_group(
        self, **kwargs: Unpack[CreateEndpointGroupRequestTypeDef]
    ) -> CreateEndpointGroupResponseTypeDef:
        """
        Create an endpoint group for the specified listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_endpoint_group)
        """

    async def create_listener(
        self, **kwargs: Unpack[CreateListenerRequestTypeDef]
    ) -> CreateListenerResponseTypeDef:
        """
        Create a listener to process inbound connections from clients to an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/create_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#create_listener)
        """

    async def delete_accelerator(
        self, **kwargs: Unpack[DeleteAcceleratorRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_accelerator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_accelerator)
        """

    async def delete_cross_account_attachment(
        self, **kwargs: Unpack[DeleteCrossAccountAttachmentRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a cross-account attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_cross_account_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_cross_account_attachment)
        """

    async def delete_custom_routing_accelerator(
        self, **kwargs: Unpack[DeleteCustomRoutingAcceleratorRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_custom_routing_accelerator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_custom_routing_accelerator)
        """

    async def delete_custom_routing_endpoint_group(
        self, **kwargs: Unpack[DeleteCustomRoutingEndpointGroupRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an endpoint group from a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_custom_routing_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_custom_routing_endpoint_group)
        """

    async def delete_custom_routing_listener(
        self, **kwargs: Unpack[DeleteCustomRoutingListenerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_custom_routing_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_custom_routing_listener)
        """

    async def delete_endpoint_group(
        self, **kwargs: Unpack[DeleteEndpointGroupRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an endpoint group from a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_endpoint_group)
        """

    async def delete_listener(
        self, **kwargs: Unpack[DeleteListenerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a listener from an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/delete_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#delete_listener)
        """

    async def deny_custom_routing_traffic(
        self, **kwargs: Unpack[DenyCustomRoutingTrafficRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Specify the Amazon EC2 instance (destination) IP addresses and ports for a VPC
        subnet endpoint that cannot receive traffic for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/deny_custom_routing_traffic.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#deny_custom_routing_traffic)
        """

    async def deprovision_byoip_cidr(
        self, **kwargs: Unpack[DeprovisionByoipCidrRequestTypeDef]
    ) -> DeprovisionByoipCidrResponseTypeDef:
        """
        Releases the specified address range that you provisioned to use with your
        Amazon Web Services resources through bring your own IP addresses (BYOIP) and
        deletes the corresponding address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/deprovision_byoip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#deprovision_byoip_cidr)
        """

    async def describe_accelerator(
        self, **kwargs: Unpack[DescribeAcceleratorRequestTypeDef]
    ) -> DescribeAcceleratorResponseTypeDef:
        """
        Describe an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_accelerator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_accelerator)
        """

    async def describe_accelerator_attributes(
        self, **kwargs: Unpack[DescribeAcceleratorAttributesRequestTypeDef]
    ) -> DescribeAcceleratorAttributesResponseTypeDef:
        """
        Describe the attributes of an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_accelerator_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_accelerator_attributes)
        """

    async def describe_cross_account_attachment(
        self, **kwargs: Unpack[DescribeCrossAccountAttachmentRequestTypeDef]
    ) -> DescribeCrossAccountAttachmentResponseTypeDef:
        """
        Gets configuration information about a cross-account attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_cross_account_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_cross_account_attachment)
        """

    async def describe_custom_routing_accelerator(
        self, **kwargs: Unpack[DescribeCustomRoutingAcceleratorRequestTypeDef]
    ) -> DescribeCustomRoutingAcceleratorResponseTypeDef:
        """
        Describe a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_custom_routing_accelerator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_custom_routing_accelerator)
        """

    async def describe_custom_routing_accelerator_attributes(
        self, **kwargs: Unpack[DescribeCustomRoutingAcceleratorAttributesRequestTypeDef]
    ) -> DescribeCustomRoutingAcceleratorAttributesResponseTypeDef:
        """
        Describe the attributes of a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_custom_routing_accelerator_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_custom_routing_accelerator_attributes)
        """

    async def describe_custom_routing_endpoint_group(
        self, **kwargs: Unpack[DescribeCustomRoutingEndpointGroupRequestTypeDef]
    ) -> DescribeCustomRoutingEndpointGroupResponseTypeDef:
        """
        Describe an endpoint group for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_custom_routing_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_custom_routing_endpoint_group)
        """

    async def describe_custom_routing_listener(
        self, **kwargs: Unpack[DescribeCustomRoutingListenerRequestTypeDef]
    ) -> DescribeCustomRoutingListenerResponseTypeDef:
        """
        The description of a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_custom_routing_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_custom_routing_listener)
        """

    async def describe_endpoint_group(
        self, **kwargs: Unpack[DescribeEndpointGroupRequestTypeDef]
    ) -> DescribeEndpointGroupResponseTypeDef:
        """
        Describe an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_endpoint_group)
        """

    async def describe_listener(
        self, **kwargs: Unpack[DescribeListenerRequestTypeDef]
    ) -> DescribeListenerResponseTypeDef:
        """
        Describe a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/describe_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#describe_listener)
        """

    async def list_accelerators(
        self, **kwargs: Unpack[ListAcceleratorsRequestTypeDef]
    ) -> ListAcceleratorsResponseTypeDef:
        """
        List the accelerators for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_accelerators.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_accelerators)
        """

    async def list_byoip_cidrs(
        self, **kwargs: Unpack[ListByoipCidrsRequestTypeDef]
    ) -> ListByoipCidrsResponseTypeDef:
        """
        Lists the IP address ranges that were specified in calls to <a
        href="https://docs.aws.amazon.com/global-accelerator/latest/api/ProvisionByoipCidr.html">ProvisionByoipCidr</a>,
        including the current state and a history of state changes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_byoip_cidrs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_byoip_cidrs)
        """

    async def list_cross_account_attachments(
        self, **kwargs: Unpack[ListCrossAccountAttachmentsRequestTypeDef]
    ) -> ListCrossAccountAttachmentsResponseTypeDef:
        """
        List the cross-account attachments that have been created in Global Accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_cross_account_attachments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_cross_account_attachments)
        """

    async def list_cross_account_resource_accounts(
        self,
    ) -> ListCrossAccountResourceAccountsResponseTypeDef:
        """
        List the accounts that have cross-account resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_cross_account_resource_accounts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_cross_account_resource_accounts)
        """

    async def list_cross_account_resources(
        self, **kwargs: Unpack[ListCrossAccountResourcesRequestTypeDef]
    ) -> ListCrossAccountResourcesResponseTypeDef:
        """
        List the cross-account resources available to work with.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_cross_account_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_cross_account_resources)
        """

    async def list_custom_routing_accelerators(
        self, **kwargs: Unpack[ListCustomRoutingAcceleratorsRequestTypeDef]
    ) -> ListCustomRoutingAcceleratorsResponseTypeDef:
        """
        List the custom routing accelerators for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_accelerators.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_accelerators)
        """

    async def list_custom_routing_endpoint_groups(
        self, **kwargs: Unpack[ListCustomRoutingEndpointGroupsRequestTypeDef]
    ) -> ListCustomRoutingEndpointGroupsResponseTypeDef:
        """
        List the endpoint groups that are associated with a listener for a custom
        routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_endpoint_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_endpoint_groups)
        """

    async def list_custom_routing_listeners(
        self, **kwargs: Unpack[ListCustomRoutingListenersRequestTypeDef]
    ) -> ListCustomRoutingListenersResponseTypeDef:
        """
        List the listeners for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_listeners.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_listeners)
        """

    async def list_custom_routing_port_mappings(
        self, **kwargs: Unpack[ListCustomRoutingPortMappingsRequestTypeDef]
    ) -> ListCustomRoutingPortMappingsResponseTypeDef:
        """
        Provides a complete mapping from the public accelerator IP address and port to
        destination EC2 instance IP addresses and ports in the virtual public cloud
        (VPC) subnet endpoint for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_port_mappings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_port_mappings)
        """

    async def list_custom_routing_port_mappings_by_destination(
        self, **kwargs: Unpack[ListCustomRoutingPortMappingsByDestinationRequestTypeDef]
    ) -> ListCustomRoutingPortMappingsByDestinationResponseTypeDef:
        """
        List the port mappings for a specific EC2 instance (destination) in a VPC
        subnet endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_custom_routing_port_mappings_by_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_custom_routing_port_mappings_by_destination)
        """

    async def list_endpoint_groups(
        self, **kwargs: Unpack[ListEndpointGroupsRequestTypeDef]
    ) -> ListEndpointGroupsResponseTypeDef:
        """
        List the endpoint groups that are associated with a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_endpoint_groups.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_endpoint_groups)
        """

    async def list_listeners(
        self, **kwargs: Unpack[ListListenersRequestTypeDef]
    ) -> ListListenersResponseTypeDef:
        """
        List the listeners for an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_listeners.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_listeners)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags for an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#list_tags_for_resource)
        """

    async def provision_byoip_cidr(
        self, **kwargs: Unpack[ProvisionByoipCidrRequestTypeDef]
    ) -> ProvisionByoipCidrResponseTypeDef:
        """
        Provisions an IP address range to use with your Amazon Web Services resources
        through bring your own IP addresses (BYOIP) and creates a corresponding address
        pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/provision_byoip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#provision_byoip_cidr)
        """

    async def remove_custom_routing_endpoints(
        self, **kwargs: Unpack[RemoveCustomRoutingEndpointsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove endpoints from a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/remove_custom_routing_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#remove_custom_routing_endpoints)
        """

    async def remove_endpoints(
        self, **kwargs: Unpack[RemoveEndpointsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove endpoints from an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/remove_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#remove_endpoints)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Add tags to an accelerator resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Remove tags from a Global Accelerator resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#untag_resource)
        """

    async def update_accelerator(
        self, **kwargs: Unpack[UpdateAcceleratorRequestTypeDef]
    ) -> UpdateAcceleratorResponseTypeDef:
        """
        Update an accelerator to make changes, such as the following:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_accelerator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_accelerator)
        """

    async def update_accelerator_attributes(
        self, **kwargs: Unpack[UpdateAcceleratorAttributesRequestTypeDef]
    ) -> UpdateAcceleratorAttributesResponseTypeDef:
        """
        Update the attributes for an accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_accelerator_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_accelerator_attributes)
        """

    async def update_cross_account_attachment(
        self, **kwargs: Unpack[UpdateCrossAccountAttachmentRequestTypeDef]
    ) -> UpdateCrossAccountAttachmentResponseTypeDef:
        """
        Update a cross-account attachment to add or remove principals or resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_cross_account_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_cross_account_attachment)
        """

    async def update_custom_routing_accelerator(
        self, **kwargs: Unpack[UpdateCustomRoutingAcceleratorRequestTypeDef]
    ) -> UpdateCustomRoutingAcceleratorResponseTypeDef:
        """
        Update a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_custom_routing_accelerator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_custom_routing_accelerator)
        """

    async def update_custom_routing_accelerator_attributes(
        self, **kwargs: Unpack[UpdateCustomRoutingAcceleratorAttributesRequestTypeDef]
    ) -> UpdateCustomRoutingAcceleratorAttributesResponseTypeDef:
        """
        Update the attributes for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_custom_routing_accelerator_attributes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_custom_routing_accelerator_attributes)
        """

    async def update_custom_routing_listener(
        self, **kwargs: Unpack[UpdateCustomRoutingListenerRequestTypeDef]
    ) -> UpdateCustomRoutingListenerResponseTypeDef:
        """
        Update a listener for a custom routing accelerator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_custom_routing_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_custom_routing_listener)
        """

    async def update_endpoint_group(
        self, **kwargs: Unpack[UpdateEndpointGroupRequestTypeDef]
    ) -> UpdateEndpointGroupResponseTypeDef:
        """
        Update an endpoint group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_endpoint_group.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_endpoint_group)
        """

    async def update_listener(
        self, **kwargs: Unpack[UpdateListenerRequestTypeDef]
    ) -> UpdateListenerResponseTypeDef:
        """
        Update a listener.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/update_listener.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#update_listener)
        """

    async def withdraw_byoip_cidr(
        self, **kwargs: Unpack[WithdrawByoipCidrRequestTypeDef]
    ) -> WithdrawByoipCidrResponseTypeDef:
        """
        Stops advertising an address range that is provisioned as an address pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/withdraw_byoip_cidr.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#withdraw_byoip_cidr)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_accelerators"]
    ) -> ListAcceleratorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_byoip_cidrs"]
    ) -> ListByoipCidrsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cross_account_attachments"]
    ) -> ListCrossAccountAttachmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cross_account_resources"]
    ) -> ListCrossAccountResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_custom_routing_accelerators"]
    ) -> ListCustomRoutingAcceleratorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_custom_routing_endpoint_groups"]
    ) -> ListCustomRoutingEndpointGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_custom_routing_listeners"]
    ) -> ListCustomRoutingListenersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_custom_routing_port_mappings_by_destination"]
    ) -> ListCustomRoutingPortMappingsByDestinationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_custom_routing_port_mappings"]
    ) -> ListCustomRoutingPortMappingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_endpoint_groups"]
    ) -> ListEndpointGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_listeners"]
    ) -> ListListenersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html#GlobalAccelerator.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_globalaccelerator/client/)
        """
