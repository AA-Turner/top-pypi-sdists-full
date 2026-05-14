"""
Type annotations for rtbfabric service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_rtbfabric.client import RTBFabricClient
    from types_boto3_rtbfabric.waiter import (
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

    session = Session()
    client: RTBFabricClient = session.client("rtbfabric")

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

from botocore.waiter import Waiter

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


class CertificateAssociatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/CertificateAssociated.html#RTBFabric.Waiter.CertificateAssociated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#certificateassociatedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetCertificateAssociationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/CertificateAssociated.html#RTBFabric.Waiter.CertificateAssociated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#certificateassociatedwaiter)
        """


class CertificateDisassociatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/CertificateDisassociated.html#RTBFabric.Waiter.CertificateDisassociated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#certificatedisassociatedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetCertificateAssociationRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/CertificateDisassociated.html#RTBFabric.Waiter.CertificateDisassociated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#certificatedisassociatedwaiter)
        """


class InboundExternalLinkActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/InboundExternalLinkActive.html#RTBFabric.Waiter.InboundExternalLinkActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#inboundexternallinkactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetInboundExternalLinkRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/InboundExternalLinkActive.html#RTBFabric.Waiter.InboundExternalLinkActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#inboundexternallinkactivewaiter)
        """


class InboundExternalLinkDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/InboundExternalLinkDeleted.html#RTBFabric.Waiter.InboundExternalLinkDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#inboundexternallinkdeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetInboundExternalLinkRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/InboundExternalLinkDeleted.html#RTBFabric.Waiter.InboundExternalLinkDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#inboundexternallinkdeletedwaiter)
        """


class LinkAcceptedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkAccepted.html#RTBFabric.Waiter.LinkAccepted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkacceptedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkAccepted.html#RTBFabric.Waiter.LinkAccepted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkacceptedwaiter)
        """


class LinkActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkActive.html#RTBFabric.Waiter.LinkActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkActive.html#RTBFabric.Waiter.LinkActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkactivewaiter)
        """


class LinkDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkDeleted.html#RTBFabric.Waiter.LinkDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkdeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkDeleted.html#RTBFabric.Waiter.LinkDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkdeletedwaiter)
        """


class LinkRoutingRuleActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkRoutingRuleActive.html#RTBFabric.Waiter.LinkRoutingRuleActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkroutingruleactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRoutingRuleRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkRoutingRuleActive.html#RTBFabric.Waiter.LinkRoutingRuleActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkroutingruleactivewaiter)
        """


class LinkRoutingRuleDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkRoutingRuleDeleted.html#RTBFabric.Waiter.LinkRoutingRuleDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkroutingruledeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLinkRoutingRuleRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/LinkRoutingRuleDeleted.html#RTBFabric.Waiter.LinkRoutingRuleDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#linkroutingruledeletedwaiter)
        """


class OutboundExternalLinkActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/OutboundExternalLinkActive.html#RTBFabric.Waiter.OutboundExternalLinkActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#outboundexternallinkactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetOutboundExternalLinkRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/OutboundExternalLinkActive.html#RTBFabric.Waiter.OutboundExternalLinkActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#outboundexternallinkactivewaiter)
        """


class OutboundExternalLinkDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/OutboundExternalLinkDeleted.html#RTBFabric.Waiter.OutboundExternalLinkDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#outboundexternallinkdeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetOutboundExternalLinkRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/OutboundExternalLinkDeleted.html#RTBFabric.Waiter.OutboundExternalLinkDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#outboundexternallinkdeletedwaiter)
        """


class RequesterGatewayActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/RequesterGatewayActive.html#RTBFabric.Waiter.RequesterGatewayActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#requestergatewayactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRequesterGatewayRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/RequesterGatewayActive.html#RTBFabric.Waiter.RequesterGatewayActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#requestergatewayactivewaiter)
        """


class RequesterGatewayDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/RequesterGatewayDeleted.html#RTBFabric.Waiter.RequesterGatewayDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#requestergatewaydeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRequesterGatewayRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/RequesterGatewayDeleted.html#RTBFabric.Waiter.RequesterGatewayDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#requestergatewaydeletedwaiter)
        """


class ResponderGatewayActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/ResponderGatewayActive.html#RTBFabric.Waiter.ResponderGatewayActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#respondergatewayactivewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetResponderGatewayRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/ResponderGatewayActive.html#RTBFabric.Waiter.ResponderGatewayActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#respondergatewayactivewaiter)
        """


class ResponderGatewayDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/ResponderGatewayDeleted.html#RTBFabric.Waiter.ResponderGatewayDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#respondergatewaydeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetResponderGatewayRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/waiter/ResponderGatewayDeleted.html#RTBFabric.Waiter.ResponderGatewayDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_rtbfabric/waiters/#respondergatewaydeletedwaiter)
        """
