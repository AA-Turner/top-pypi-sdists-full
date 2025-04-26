r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfPortsRemote", "ShelfPortsRemoteSchema"]
__pdoc__ = {
    "ShelfPortsRemoteSchema.resource": False,
    "ShelfPortsRemoteSchema.opts": False,
    "ShelfPortsRemote": False,
}


class ShelfPortsRemoteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfPortsRemote object"""

    chassis = marshmallow_fields.Str(data_key="chassis", allow_none=True)
    r""" The chassis field of the shelf_ports_remote. """

    device = marshmallow_fields.Str(data_key="device", allow_none=True)
    r""" The device field of the shelf_ports_remote. """

    mac_address = marshmallow_fields.Str(data_key="mac_address", allow_none=True)
    r""" The mac_address field of the shelf_ports_remote. """

    phy = marshmallow_fields.Str(data_key="phy", allow_none=True)
    r""" The phy field of the shelf_ports_remote.

Example: 12 """

    port = marshmallow_fields.Str(data_key="port", allow_none=True)
    r""" The port field of the shelf_ports_remote. """

    wwn = marshmallow_fields.Str(data_key="wwn", allow_none=True)
    r""" The wwn field of the shelf_ports_remote.

Example: 50000D1703544B80 """

    @property
    def resource(self):
        return ShelfPortsRemote

    gettable_fields = [
        "chassis",
        "device",
        "mac_address",
        "phy",
        "port",
        "wwn",
    ]
    """chassis,device,mac_address,phy,port,wwn,"""

    patchable_fields = [
        "chassis",
        "device",
        "mac_address",
        "phy",
        "port",
        "wwn",
    ]
    """chassis,device,mac_address,phy,port,wwn,"""

    postable_fields = [
        "chassis",
        "device",
        "mac_address",
        "phy",
        "port",
        "wwn",
    ]
    """chassis,device,mac_address,phy,port,wwn,"""


class ShelfPortsRemote(Resource):

    _schema = ShelfPortsRemoteSchema
