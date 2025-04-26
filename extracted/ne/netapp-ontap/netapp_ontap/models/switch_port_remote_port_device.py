r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SwitchPortRemotePortDevice", "SwitchPortRemotePortDeviceSchema"]
__pdoc__ = {
    "SwitchPortRemotePortDeviceSchema.resource": False,
    "SwitchPortRemotePortDeviceSchema.opts": False,
    "SwitchPortRemotePortDevice": False,
}


class SwitchPortRemotePortDeviceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SwitchPortRemotePortDevice object"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the switch_port_remote_port_device. """

    shelf = marshmallow_fields.Nested("netapp_ontap.models.switch_port_remote_port_device_shelf.SwitchPortRemotePortDeviceShelfSchema", unknown=EXCLUDE, data_key="shelf", allow_none=True)
    r""" Shelf connected to this port. """

    @property
    def resource(self):
        return SwitchPortRemotePortDevice

    gettable_fields = [
        "node.links",
        "node.name",
        "node.uuid",
        "shelf",
    ]
    """node.links,node.name,node.uuid,shelf,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SwitchPortRemotePortDevice(Resource):

    _schema = SwitchPortRemotePortDeviceSchema
