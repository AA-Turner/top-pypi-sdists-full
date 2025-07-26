r"""
Copyright &copy; 2025 NetApp Inc.
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

    functional_roles = marshmallow_fields.List(marshmallow_fields.Str, data_key="functional_roles", allow_none=True)
    r""" The functional_roles field of the switch_port_remote_port. """

    mtu = Size(data_key="mtu", allow_none=True)
    r""" MTU in octets. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Remote port name. """

    @property
    def resource(self):
        return SwitchPortRemotePort

    gettable_fields = [
        "device",
        "functional_roles",
        "mtu",
        "name",
    ]
    """device,functional_roles,mtu,name,"""

    patchable_fields = [
        "device",
        "functional_roles",
    ]
    """device,functional_roles,"""

    postable_fields = [
        "device",
        "functional_roles",
    ]
    """device,functional_roles,"""


class SwitchPortRemotePort(Resource):

    _schema = SwitchPortRemotePortSchema
