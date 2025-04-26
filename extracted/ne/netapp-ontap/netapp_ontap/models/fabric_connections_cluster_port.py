r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FabricConnectionsClusterPort", "FabricConnectionsClusterPortSchema"]
__pdoc__ = {
    "FabricConnectionsClusterPortSchema.resource": False,
    "FabricConnectionsClusterPortSchema.opts": False,
    "FabricConnectionsClusterPort": False,
}


class FabricConnectionsClusterPortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FabricConnectionsClusterPort object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the fabric_connections_cluster_port. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the cluster Fibre Channel port.


Example: 0a """

    node = marshmallow_fields.Nested("netapp_ontap.models.fabric_connections_cluster_port_node.FabricConnectionsClusterPortNodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node on which the cluster Fibre Channel port is located. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the cluster Fibre Channel port.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    wwpn = marshmallow_fields.Str(data_key="wwpn", allow_none=True)
    r""" The world wide port name (WWPN) of the cluster Fibre Channel port.


Example: 50:0a:11:22:33:44:55:66 """

    @property
    def resource(self):
        return FabricConnectionsClusterPort

    gettable_fields = [
        "links",
        "name",
        "node",
        "uuid",
        "wwpn",
    ]
    """links,name,node,uuid,wwpn,"""

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


class FabricConnectionsClusterPort(Resource):

    _schema = FabricConnectionsClusterPortSchema
