r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PortLagActivePorts", "PortLagActivePortsSchema"]
__pdoc__ = {
    "PortLagActivePortsSchema.resource": False,
    "PortLagActivePortsSchema.opts": False,
    "PortLagActivePorts": False,
}


class PortLagActivePortsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PortLagActivePorts object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the port_lag_active_ports. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the port_lag_active_ports.

Example: e1b """

    node = marshmallow_fields.Nested("netapp_ontap.models.bgp_peer_group_local_port_node.BgpPeerGroupLocalPortNodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the port_lag_active_ports. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The uuid field of the port_lag_active_ports.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return PortLagActivePorts

    gettable_fields = [
        "links",
        "name",
        "node",
        "uuid",
    ]
    """links,name,node,uuid,"""

    patchable_fields = [
        "name",
        "node",
        "uuid",
    ]
    """name,node,uuid,"""

    postable_fields = [
        "name",
        "node",
        "uuid",
    ]
    """name,node,uuid,"""


class PortLagActivePorts(Resource):

    _schema = PortLagActivePortsSchema
