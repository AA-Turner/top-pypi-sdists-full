r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageBridgeFcPorts", "StorageBridgeFcPortsSchema"]
__pdoc__ = {
    "StorageBridgeFcPortsSchema.resource": False,
    "StorageBridgeFcPortsSchema.opts": False,
    "StorageBridgeFcPorts": False,
}


class StorageBridgeFcPortsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageBridgeFcPorts object"""

    configured_data_rate = marshmallow_fields.Number(data_key="configured_data_rate", allow_none=True)
    r""" Bridge FC port configured data rate, in Gbps """

    connection_mode = marshmallow_fields.Str(data_key="connection_mode", allow_none=True)
    r""" Bridge FC port configured connection mode

Valid choices:

* loop
* ptp
* loop_preferred
* ptp_preferred """

    data_rate_capability = marshmallow_fields.Number(data_key="data_rate_capability", allow_none=True)
    r""" Bridge FC port data rate capability, in Gbps """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether the bridge FC port is enabled. """

    id = Size(data_key="id", allow_none=True)
    r""" Bridge FC port index """

    negotiated_data_rate = marshmallow_fields.Number(data_key="negotiated_data_rate", allow_none=True)
    r""" Bridge FC port negotiated data rate, in Gbps """

    peer_wwn = marshmallow_fields.Str(data_key="peer_wwn", allow_none=True)
    r""" Bridge FC port peer port world wide name

Example: 200650eb1a238892 """

    sfp = marshmallow_fields.Nested("netapp_ontap.models.storage_bridge_fc_ports_sfp.StorageBridgeFcPortsSfpSchema", unknown=EXCLUDE, data_key="sfp", allow_none=True)
    r""" The sfp field of the storage_bridge_fc_ports. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Bridge FC port state

Valid choices:

* error
* online
* offline """

    wwn = marshmallow_fields.Str(data_key="wwn", allow_none=True)
    r""" Bridge FC port world wide name

Example: 2100001086a54100 """

    @property
    def resource(self):
        return StorageBridgeFcPorts

    gettable_fields = [
        "configured_data_rate",
        "connection_mode",
        "data_rate_capability",
        "enabled",
        "id",
        "negotiated_data_rate",
        "peer_wwn",
        "sfp",
        "state",
        "wwn",
    ]
    """configured_data_rate,connection_mode,data_rate_capability,enabled,id,negotiated_data_rate,peer_wwn,sfp,state,wwn,"""

    patchable_fields = [
        "configured_data_rate",
        "connection_mode",
        "data_rate_capability",
        "enabled",
        "id",
        "negotiated_data_rate",
        "peer_wwn",
        "sfp",
        "state",
        "wwn",
    ]
    """configured_data_rate,connection_mode,data_rate_capability,enabled,id,negotiated_data_rate,peer_wwn,sfp,state,wwn,"""

    postable_fields = [
        "configured_data_rate",
        "connection_mode",
        "data_rate_capability",
        "enabled",
        "id",
        "negotiated_data_rate",
        "peer_wwn",
        "sfp",
        "state",
        "wwn",
    ]
    """configured_data_rate,connection_mode,data_rate_capability,enabled,id,negotiated_data_rate,peer_wwn,sfp,state,wwn,"""


class StorageBridgeFcPorts(Resource):

    _schema = StorageBridgeFcPortsSchema
