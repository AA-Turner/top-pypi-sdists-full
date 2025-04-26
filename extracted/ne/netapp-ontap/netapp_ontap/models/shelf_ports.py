r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfPorts", "ShelfPortsSchema"]
__pdoc__ = {
    "ShelfPortsSchema.resource": False,
    "ShelfPortsSchema.opts": False,
    "ShelfPorts": False,
}


class ShelfPortsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfPorts object"""

    cable = marshmallow_fields.Nested("netapp_ontap.models.shelf_ports_cable.ShelfPortsCableSchema", unknown=EXCLUDE, data_key="cable", allow_none=True)
    r""" The cable field of the shelf_ports. """

    designator = marshmallow_fields.Str(data_key="designator", allow_none=True)
    r""" The designator field of the shelf_ports.

Valid choices:

* circle
* square
* 1
* 2
* 3
* 4 """

    id = Size(data_key="id", allow_none=True)
    r""" The id field of the shelf_ports.

Example: 0 """

    internal = marshmallow_fields.Boolean(data_key="internal", allow_none=True)
    r""" The internal field of the shelf_ports. """

    mac_address = marshmallow_fields.Str(data_key="mac_address", allow_none=True)
    r""" The mac_address field of the shelf_ports. """

    module_id = marshmallow_fields.Str(data_key="module_id", allow_none=True)
    r""" The module_id field of the shelf_ports.

Valid choices:

* a
* b """

    remote = marshmallow_fields.Nested("netapp_ontap.models.shelf_ports_remote.ShelfPortsRemoteSchema", unknown=EXCLUDE, data_key="remote", allow_none=True)
    r""" The remote field of the shelf_ports. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the shelf_ports.

Valid choices:

* connected
* disconnected
* error """

    wwn = marshmallow_fields.Str(data_key="wwn", allow_none=True)
    r""" The wwn field of the shelf_ports.

Example: 500A0980000B6C3F """

    @property
    def resource(self):
        return ShelfPorts

    gettable_fields = [
        "cable",
        "designator",
        "id",
        "internal",
        "mac_address",
        "module_id",
        "remote",
        "state",
        "wwn",
    ]
    """cable,designator,id,internal,mac_address,module_id,remote,state,wwn,"""

    patchable_fields = [
        "cable",
        "designator",
        "id",
        "internal",
        "mac_address",
        "module_id",
        "remote",
        "state",
        "wwn",
    ]
    """cable,designator,id,internal,mac_address,module_id,remote,state,wwn,"""

    postable_fields = [
        "cable",
        "designator",
        "id",
        "internal",
        "mac_address",
        "module_id",
        "remote",
        "state",
        "wwn",
    ]
    """cable,designator,id,internal,mac_address,module_id,remote,state,wwn,"""


class ShelfPorts(Resource):

    _schema = ShelfPortsSchema
