r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PortReachableBroadcastDomains", "PortReachableBroadcastDomainsSchema"]
__pdoc__ = {
    "PortReachableBroadcastDomainsSchema.resource": False,
    "PortReachableBroadcastDomainsSchema.opts": False,
    "PortReachableBroadcastDomains": False,
}


class PortReachableBroadcastDomainsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PortReachableBroadcastDomains object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the port_reachable_broadcast_domains. """

    ipspace = marshmallow_fields.Nested("netapp_ontap.models.broadcast_domain_reference_ipspace.BroadcastDomainReferenceIpspaceSchema", unknown=EXCLUDE, data_key="ipspace", allow_none=True)
    r""" The ipspace field of the port_reachable_broadcast_domains. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the broadcast domain, scoped to its IPspace

Example: bd1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Broadcast domain UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return PortReachableBroadcastDomains

    gettable_fields = [
        "links",
        "ipspace",
        "name",
        "uuid",
    ]
    """links,ipspace,name,uuid,"""

    patchable_fields = [
        "ipspace",
        "name",
        "uuid",
    ]
    """ipspace,name,uuid,"""

    postable_fields = [
        "ipspace",
        "name",
        "uuid",
    ]
    """ipspace,name,uuid,"""


class PortReachableBroadcastDomains(Resource):

    _schema = PortReachableBroadcastDomainsSchema
