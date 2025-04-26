r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FcSwitchPortsAttachedDevice", "FcSwitchPortsAttachedDeviceSchema"]
__pdoc__ = {
    "FcSwitchPortsAttachedDeviceSchema.resource": False,
    "FcSwitchPortsAttachedDeviceSchema.opts": False,
    "FcSwitchPortsAttachedDevice": False,
}


class FcSwitchPortsAttachedDeviceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcSwitchPortsAttachedDevice object"""

    port_id = marshmallow_fields.Str(data_key="port_id", allow_none=True)
    r""" The Fibre Channel port identifier of the attach device.


Example: 70400 """

    wwpn = marshmallow_fields.Str(data_key="wwpn", allow_none=True)
    r""" The world-wide port name (WWPN) of the attached device.


Example: 50:0a:21:22:23:24:25:26 """

    @property
    def resource(self):
        return FcSwitchPortsAttachedDevice

    gettable_fields = [
        "port_id",
        "wwpn",
    ]
    """port_id,wwpn,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class FcSwitchPortsAttachedDevice(Resource):

    _schema = FcSwitchPortsAttachedDeviceSchema
