r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfAcps", "ShelfAcpsSchema"]
__pdoc__ = {
    "ShelfAcpsSchema.resource": False,
    "ShelfAcpsSchema.opts": False,
    "ShelfAcps": False,
}


class ShelfAcpsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfAcps object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" The address field of the shelf_acps.

Example: 192.168.1.104 """

    channel = marshmallow_fields.Str(data_key="channel", allow_none=True)
    r""" The channel field of the shelf_acps.

Valid choices:

* unknown
* out_of_band
* in_band """

    connection_state = marshmallow_fields.Str(data_key="connection_state", allow_none=True)
    r""" The connection_state field of the shelf_acps.

Valid choices:

* no_connectivity
* partial_connectivity
* full_connectivity
* additional_connectivity
* unknown_connectivity
* not_available
* active
* disabled """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" The enabled field of the shelf_acps. """

    error = marshmallow_fields.Nested("netapp_ontap.models.shelf_acps_error.ShelfAcpsErrorSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" Error object is populated when connection_state becomes non-optimal """

    netmask = marshmallow_fields.Str(data_key="netmask", allow_none=True)
    r""" The netmask field of the shelf_acps.

Example: 255.255.252.0 """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the shelf_acps. """

    port = marshmallow_fields.Str(data_key="port", allow_none=True)
    r""" The port field of the shelf_acps.

Example: e0P """

    subnet = marshmallow_fields.Str(data_key="subnet", allow_none=True)
    r""" The subnet field of the shelf_acps.

Example: 192.168.0.1 """

    @property
    def resource(self):
        return ShelfAcps

    gettable_fields = [
        "address",
        "channel",
        "connection_state",
        "enabled",
        "error",
        "netmask",
        "node.links",
        "node.name",
        "node.uuid",
        "port",
        "subnet",
    ]
    """address,channel,connection_state,enabled,error,netmask,node.links,node.name,node.uuid,port,subnet,"""

    patchable_fields = [
        "address",
        "channel",
        "connection_state",
        "enabled",
        "error",
        "netmask",
        "node.name",
        "node.uuid",
        "port",
        "subnet",
    ]
    """address,channel,connection_state,enabled,error,netmask,node.name,node.uuid,port,subnet,"""

    postable_fields = [
        "address",
        "channel",
        "connection_state",
        "enabled",
        "error",
        "netmask",
        "node.name",
        "node.uuid",
        "port",
        "subnet",
    ]
    """address,channel,connection_state,enabled,error,netmask,node.name,node.uuid,port,subnet,"""


class ShelfAcps(Resource):

    _schema = ShelfAcpsSchema
