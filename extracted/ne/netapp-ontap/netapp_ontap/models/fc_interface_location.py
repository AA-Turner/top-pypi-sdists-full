r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FcInterfaceLocation", "FcInterfaceLocationSchema"]
__pdoc__ = {
    "FcInterfaceLocationSchema.resource": False,
    "FcInterfaceLocationSchema.opts": False,
    "FcInterfaceLocation": False,
}


class FcInterfaceLocationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcInterfaceLocation object"""

    home_node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="home_node", allow_none=True)
    r""" The home_node field of the fc_interface_location. """

    home_port = marshmallow_fields.Nested("netapp_ontap.resources.fc_port.FcPortSchema", unknown=EXCLUDE, data_key="home_port", allow_none=True)
    r""" The home_port field of the fc_interface_location. """

    is_home = marshmallow_fields.Boolean(data_key="is_home", allow_none=True)
    r""" Indicates if the FC interface is currently on its home node. """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the fc_interface_location. """

    port = marshmallow_fields.Nested("netapp_ontap.resources.fc_port.FcPortSchema", unknown=EXCLUDE, data_key="port", allow_none=True)
    r""" The port field of the fc_interface_location. """

    @property
    def resource(self):
        return FcInterfaceLocation

    gettable_fields = [
        "home_node.links",
        "home_node.name",
        "home_node.uuid",
        "home_port.links",
        "home_port.name",
        "home_port.node",
        "home_port.uuid",
        "is_home",
        "node.links",
        "node.name",
        "node.uuid",
        "port.links",
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """home_node.links,home_node.name,home_node.uuid,home_port.links,home_port.name,home_port.node,home_port.uuid,is_home,node.links,node.name,node.uuid,port.links,port.name,port.node,port.uuid,"""

    patchable_fields = [
        "home_port.name",
        "home_port.node",
        "home_port.uuid",
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """home_port.name,home_port.node,home_port.uuid,port.name,port.node,port.uuid,"""

    postable_fields = [
        "home_port.name",
        "home_port.node",
        "home_port.uuid",
        "port.name",
        "port.node",
        "port.uuid",
    ]
    """home_port.name,home_port.node,home_port.uuid,port.name,port.node,port.uuid,"""


class FcInterfaceLocation(Resource):

    _schema = FcInterfaceLocationSchema
