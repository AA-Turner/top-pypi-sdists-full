r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SwitchPortRemotePort", "SwitchPortRemotePortSchema"]
__pdoc__ = {
    "SwitchPortRemotePortSchema.resource": False,
    "SwitchPortRemotePortSchema.opts": False,
    "SwitchPortRemotePort": False,
}


class SwitchPortRemotePortSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SwitchPortRemotePort object"""

    device = marshmallow_fields.Nested("netapp_ontap.models.switch_port_remote_port_device.SwitchPortRemotePortDeviceSchema", unknown=EXCLUDE, data_key="device", allow_none=True)
    r""" Device connected to port. """

    mtu = Size(data_key="mtu", allow_none=True)
    r""" MTU in octets. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Port Name. """

    @property
    def resource(self):
        return SwitchPortRemotePort

    gettable_fields = [
        "device",
        "mtu",
        "name",
    ]
    """device,mtu,name,"""

    patchable_fields = [
        "device",
    ]
    """device,"""

    postable_fields = [
        "device",
    ]
    """device,"""


class SwitchPortRemotePort(Resource):

    _schema = SwitchPortRemotePortSchema
