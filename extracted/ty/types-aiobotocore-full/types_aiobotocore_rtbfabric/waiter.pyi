"""
Type annotations for rtbfabric service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_rtbfabric.client import RTBFabricClient
    from types_aiobotocore_rtbfabric.waiter import (
        CertificateAssociatedWaiter,
        CertificateDisassociatedWaiter,
        InboundExternalLinkActiveWaiter,
        InboundExternalLinkDeletedWaiter,
        LinkAcceptedWaiter,
        LinkActiveWaiter,
        LinkDeletedWaiter,
        LinkRoutingRuleActiveWaiter,
        LinkRoutingRuleDeletedWaiter,
        OutboundExternalLinkActiveWaiter,
        OutboundExternalLinkDeletedWaiter,
        RequesterGatewayActiveWaiter,
        RequesterGatewayDeletedWaiter,
        ResponderGatewayActiveWaiter,
        ResponderGatewayDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("rtbfabric") as client:
        client: RTBFabricClient

        certificate_associated_waiter: CertificateAssociatedWaiter = client.get_waiter("certificate_associated")
        certificate_disassociated_waiter: CertificateDisassociatedWaiter = client.get_waiter("certificate_disassociated")
        inbound_external_link_active_waiter: InboundExternalLinkActiveWaiter = client.get_waiter("inbound_external_link_active")
        inbound_external_link_deleted_waiter: InboundExternalLinkDeletedWaiter = client.get_waiter("inbound_external_link_deleted")
        link_accepted_waiter: LinkAcceptedWaiter = client.get_waiter("link_accepted")
        link_active_waiter: LinkActiveWaiter = client.get_waiter("link_active")
        link_deleted_waiter: LinkDeletedWaiter = client.get_waiter("link_deleted")
        link_routing_rule_active_waiter: LinkRoutingRuleActiveWaiter = client.get_waiter("link_routing_rule_active")
        link_routing_rule_deleted_waiter: LinkRoutingRuleDeletedWaiter = client.get_waiter("link_routing_rule_deleted")
        outbound_external_link_active_waiter: OutboundExternalLinkActiveWaiter = client.get_waiter("outbound_external_link_active")
        outbound_external_link_deleted_waiter: OutboundExternalLinkDeletedWaiter = client.get_waiter("outbound_external_link_deleted")
        requester_gateway_active_waiter: RequesterGatewayActiveWaiter = client.get_waiter("requester_gateway_active")
        requester_gateway_deleted_waiter: RequesterGatewayDeletedWaiter = client.get_waiter("requester_gateway_deleted")
        responder_gateway_active_waiter: ResponderGatewayActiveWaiter = client.get_waiter("responder_gateway_active")
        responder_gateway_deleted_waiter: ResponderGatewayDeletedWaiter = client.get_waiter("responder_gateway_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetCertificateAssociationRequestWaitExtraTypeDef,
    GetCertificateAssociationRequestWaitTypeDef,
    GetInboundExternalLinkRequestWaitExtraTypeDef,
    GetInboundExternalLinkRequestWaitTypeDef,
    GetLinkRequestWaitExtraExtraTypeDef,
    GetLinkRequestWaitExtraTypeDef,
    GetLinkRequestWaitTypeDef,
    GetLinkRoutingRuleRequestWaitExtraTypeDef,
    GetLinkRoutingRuleRequestWaitTypeDef,
    GetOutboundExternalLinkRequestWaitExtraTypeDef,
    GetOutboundExternalLinkRequestWaitTypeDef,
    GetRequesterGatewayRequestWaitExtraTypeDef,
    GetRequesterGatewayRequestWaitTypeDef,
    GetResponderGatewayRequestWaitExtraTypeDef,
    GetResponderGatewayRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "CertificateAssociatedWaiter",
    "CertificateDisassociatedWaiter",
    "InboundExternalLinkActiveWaiter",
    "InboundExternalLinkDeletedWaiter",
    "LinkAcceptedWaiter",
    "LinkActiveWaiter",
    "LinkDeletedWaiter",
    "LinkRoutingRuleActiveWaiter",
    "LinkRoutingRuleDeletedWaiter",
    "OutboundExternalLinkActiveWaiter",
    "OutboundExternalLinkDeletedWaiter",
    "RequesterGatewayActiveWaiter",
    "RequesterGatewayDeletedWaiter",
    "ResponderGatewayActiveWaiter",
    "ResponderGatewayDeletedWaiter",
)

class CertificateAssociatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/CertificateAssociated.html#RTBFabric.Waiter.CertificateAssociated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#certificateassociatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetCertificateAssociationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/CertificateAssociated.html#RTBFabric.Waiter.CertificateAssociated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#certificateassociatedwaiter)
        """

class CertificateDisassociatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/CertificateDisassociated.html#RTBFabric.Waiter.CertificateDisassociated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#certificatedisassociatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetCertificateAssociationRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/CertificateDisassociated.html#RTBFabric.Waiter.CertificateDisassociated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#certificatedisassociatedwaiter)
        """

class InboundExternalLinkActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/InboundExternalLinkActive.html#RTBFabric.Waiter.InboundExternalLinkActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#inboundexternallinkactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetInboundExternalLinkRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/InboundExternalLinkActive.html#RTBFabric.Waiter.InboundExternalLinkActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#inboundexternallinkactivewaiter)
        """

class InboundExternalLinkDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/InboundExternalLinkDeleted.html#RTBFabric.Waiter.InboundExternalLinkDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#inboundexternallinkdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetInboundExternalLinkRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/InboundExternalLinkDeleted.html#RTBFabric.Waiter.InboundExternalLinkDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#inboundexternallinkdeletedwaiter)
        """

class LinkAcceptedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkAccepted.html#RTBFabric.Waiter.LinkAccepted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkacceptedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkAccepted.html#RTBFabric.Waiter.LinkAccepted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkacceptedwaiter)
        """

class LinkActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkActive.html#RTBFabric.Waiter.LinkActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkActive.html#RTBFabric.Waiter.LinkActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkactivewaiter)
        """

class LinkDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkDeleted.html#RTBFabric.Waiter.LinkDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkDeleted.html#RTBFabric.Waiter.LinkDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkdeletedwaiter)
        """

class LinkRoutingRuleActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkRoutingRuleActive.html#RTBFabric.Waiter.LinkRoutingRuleActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkroutingruleactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRoutingRuleRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkRoutingRuleActive.html#RTBFabric.Waiter.LinkRoutingRuleActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkroutingruleactivewaiter)
        """

class LinkRoutingRuleDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkRoutingRuleDeleted.html#RTBFabric.Waiter.LinkRoutingRuleDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkroutingruledeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRoutingRuleRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkRoutingRuleDeleted.html#RTBFabric.Waiter.LinkRoutingRuleDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#linkroutingruledeletedwaiter)
        """

class OutboundExternalLinkActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/OutboundExternalLinkActive.html#RTBFabric.Waiter.OutboundExternalLinkActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#outboundexternallinkactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetOutboundExternalLinkRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/OutboundExternalLinkActive.html#RTBFabric.Waiter.OutboundExternalLinkActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#outboundexternallinkactivewaiter)
        """

class OutboundExternalLinkDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/OutboundExternalLinkDeleted.html#RTBFabric.Waiter.OutboundExternalLinkDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#outboundexternallinkdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetOutboundExternalLinkRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/OutboundExternalLinkDeleted.html#RTBFabric.Waiter.OutboundExternalLinkDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#outboundexternallinkdeletedwaiter)
        """

class RequesterGatewayActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/RequesterGatewayActive.html#RTBFabric.Waiter.RequesterGatewayActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#requestergatewayactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRequesterGatewayRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/RequesterGatewayActive.html#RTBFabric.Waiter.RequesterGatewayActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#requestergatewayactivewaiter)
        """

class RequesterGatewayDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/RequesterGatewayDeleted.html#RTBFabric.Waiter.RequesterGatewayDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#requestergatewaydeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRequesterGatewayRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/RequesterGatewayDeleted.html#RTBFabric.Waiter.RequesterGatewayDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#requestergatewaydeletedwaiter)
        """

class ResponderGatewayActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/ResponderGatewayActive.html#RTBFabric.Waiter.ResponderGatewayActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#respondergatewayactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetResponderGatewayRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/ResponderGatewayActive.html#RTBFabric.Waiter.ResponderGatewayActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#respondergatewayactivewaiter)
        """

class ResponderGatewayDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/ResponderGatewayDeleted.html#RTBFabric.Waiter.ResponderGatewayDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#respondergatewaydeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetResponderGatewayRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/ResponderGatewayDeleted.html#RTBFabric.Waiter.ResponderGatewayDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rtbfabric/waiters/#respondergatewaydeletedwaiter)
        """
