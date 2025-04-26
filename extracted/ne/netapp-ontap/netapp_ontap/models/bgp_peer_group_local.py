r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["BgpPeerGroupLocal", "BgpPeerGroupLocalSchema"]
__pdoc__ = {
    "BgpPeerGroupLocalSchema.resource": False,
    "BgpPeerGroupLocalSchema.opts": False,
    "BgpPeerGroupLocal": False,
}


class BgpPeerGroupLocalSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the BgpPeerGroupLocal object"""

    interface = marshmallow_fields.Nested("netapp_ontap.resources.ip_interface.IpInterfaceSchema", unknown=EXCLUDE, data_key="interface", allow_none=True)
    r""" The interface field of the bgp_peer_group_local. """

    ip = marshmallow_fields.Nested("netapp_ontap.models.bgp_peer_group_local_ip.BgpPeerGroupLocalIpSchema", unknown=EXCLUDE, data_key="ip", allow_none=True)
    r""" IP information to create a new interface. """

    port = marshmallow_fields.Nested("netapp_ontap.resources.port.PortSchema", unknown=EXCLUDE, data_key="port", allow_none=True)
    r""" The port field of the bgp_peer_group_local. """

    @property
    def resource(self):
        return BgpPeerGroupLocal

    gettable_fields = [
        "interface.links",
        "interface.ip",
        "interface.name",
        "interface.uuid",
        "port.links",
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """interface.links,interface.ip,interface.name,interface.uuid,port.links,port.name,port.node,port.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "interface.name",
        "interface.uuid",
        "ip",
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """interface.name,interface.uuid,ip,port.name,port.node,port.uuid,"""


class BgpPeerGroupLocal(Resource):

    _schema = BgpPeerGroupLocalSchema
