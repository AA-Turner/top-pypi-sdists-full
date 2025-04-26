r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FcSwitchPorts", "FcSwitchPortsSchema"]
__pdoc__ = {
    "FcSwitchPortsSchema.resource": False,
    "FcSwitchPortsSchema.opts": False,
    "FcSwitchPorts": False,
}


class FcSwitchPortsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FcSwitchPorts object"""

    attached_device = marshmallow_fields.Nested("netapp_ontap.models.fc_switch_ports_attached_device.FcSwitchPortsAttachedDeviceSchema", unknown=EXCLUDE, data_key="attached_device", allow_none=True)
    r""" The Fibre Channel (FC) device attached to the FC switch port. """

    slot = marshmallow_fields.Str(data_key="slot", allow_none=True)
    r""" The slot of the Fibre Channel switch port.


Example: 1 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state of the Fibre Channel switch port.


Valid choices:

* unknown
* online
* offline
* testing
* fault """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type of the Fibre Channel switch port.


Valid choices:

* b_port
* e_port
* f_port
* fl_port
* fnl_port
* fv_port
* n_port
* nl_port
* nv_port
* nx_port
* sd_port
* te_port
* tf_port
* tl_port
* tnp_port
* none """

    wwpn = marshmallow_fields.Str(data_key="wwpn", allow_none=True)
    r""" The world wide port name (WWPN) of the Fibre Channel switch port.


Example: 50:0a:31:32:33:34:35:36 """

    @property
    def resource(self):
        return FcSwitchPorts

    gettable_fields = [
        "attached_device",
        "slot",
        "state",
        "type",
        "wwpn",
    ]
    """attached_device,slot,state,type,wwpn,"""

    patchable_fields = [
        "attached_device",
    ]
    """attached_device,"""

    postable_fields = [
        "attached_device",
    ]
    """attached_device,"""


class FcSwitchPorts(Resource):

    _schema = FcSwitchPortsSchema
