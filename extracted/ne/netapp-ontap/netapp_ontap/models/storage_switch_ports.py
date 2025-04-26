r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageSwitchPorts", "StorageSwitchPortsSchema"]
__pdoc__ = {
    "StorageSwitchPortsSchema.resource": False,
    "StorageSwitchPortsSchema.opts": False,
    "StorageSwitchPorts": False,
}


class StorageSwitchPortsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageSwitchPorts object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether the storage switch port is enabled. """

    mode = marshmallow_fields.Str(data_key="mode", allow_none=True)
    r""" Storage switch port mode

Valid choices:

* unknown
* auto
* f_port
* fl_port
* e_port
* te_port
* u_port
* g_port
* other
* ex_port
* d_port
* sim_port
* ve_port
* ae_port
* af_port """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Storage switch port name """

    sfp = marshmallow_fields.Nested("netapp_ontap.models.storage_switch_ports_sfp.StorageSwitchPortsSfpSchema", unknown=EXCLUDE, data_key="sfp", allow_none=True)
    r""" The sfp field of the storage_switch_ports. """

    speed = Size(data_key="speed", allow_none=True)
    r""" Storage switch port speed, in Gbps """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Storage switch port state

Valid choices:

* error
* online
* offline """

    wwn = marshmallow_fields.Str(data_key="wwn", allow_none=True)
    r""" Storage switch port world wide name """

    @property
    def resource(self):
        return StorageSwitchPorts

    gettable_fields = [
        "enabled",
        "mode",
        "name",
        "sfp",
        "speed",
        "state",
        "wwn",
    ]
    """enabled,mode,name,sfp,speed,state,wwn,"""

    patchable_fields = [
        "enabled",
        "mode",
        "name",
        "sfp",
        "speed",
        "state",
        "wwn",
    ]
    """enabled,mode,name,sfp,speed,state,wwn,"""

    postable_fields = [
        "enabled",
        "mode",
        "name",
        "sfp",
        "speed",
        "state",
        "wwn",
    ]
    """enabled,mode,name,sfp,speed,state,wwn,"""


class StorageSwitchPorts(Resource):

    _schema = StorageSwitchPortsSchema
