"""
Main interface for rtbfabric service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_rtbfabric import (
        CertificateAssociatedWaiter,
        CertificateDisassociatedWaiter,
        Client,
        InboundExternalLinkActiveWaiter,
        InboundExternalLinkDeletedWaiter,
        LinkAcceptedWaiter,
        LinkActiveWaiter,
        LinkDeletedWaiter,
        LinkRoutingRuleActiveWaiter,
        LinkRoutingRuleDeletedWaiter,
        ListCertificateAssociationsPaginator,
        ListLinkRoutingRulesPaginator,
        ListLinksPaginator,
        ListRequesterGatewaysPaginator,
        ListResponderGatewaysPaginator,
        OutboundExternalLinkActiveWaiter,
        OutboundExternalLinkDeletedWaiter,
        RTBFabricClient,
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

    list_certificate_associations_paginator: ListCertificateAssociationsPaginator = client.get_paginator("list_certificate_associations")
    list_link_routing_rules_paginator: ListLinkRoutingRulesPaginator = client.get_paginator("list_link_routing_rules")
    list_links_paginator: ListLinksPaginator = client.get_paginator("list_links")
    list_requester_gateways_paginator: ListRequesterGatewaysPaginator = client.get_paginator("list_requester_gateways")
    list_responder_gateways_paginator: ListResponderGatewaysPaginator = client.get_paginator("list_responder_gateways")
    ```
"""

from .client import RTBFabricClient
from .paginator import (
    ListCertificateAssociationsPaginator,
    ListLinkRoutingRulesPaginator,
    ListLinksPaginator,
    ListRequesterGatewaysPaginator,
    ListResponderGatewaysPaginator,
)
from .waiter import (
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

Client = RTBFabricClient


__all__ = (
    "CertificateAssociatedWaiter",
    "CertificateDisassociatedWaiter",
    "Client",
    "InboundExternalLinkActiveWaiter",
    "InboundExternalLinkDeletedWaiter",
    "LinkAcceptedWaiter",
    "LinkActiveWaiter",
    "LinkDeletedWaiter",
    "LinkRoutingRuleActiveWaiter",
    "LinkRoutingRuleDeletedWaiter",
    "ListCertificateAssociationsPaginator",
    "ListLinkRoutingRulesPaginator",
    "ListLinksPaginator",
    "ListRequesterGatewaysPaginator",
    "ListResponderGatewaysPaginator",
    "OutboundExternalLinkActiveWaiter",
    "OutboundExternalLinkDeletedWaiter",
    "RTBFabricClient",
    "RequesterGatewayActiveWaiter",
    "RequesterGatewayDeletedWaiter",
    "ResponderGatewayActiveWaiter",
    "ResponderGatewayDeletedWaiter",
)
