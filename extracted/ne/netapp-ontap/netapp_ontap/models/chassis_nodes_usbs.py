r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ChassisNodesUsbs", "ChassisNodesUsbsSchema"]
__pdoc__ = {
    "ChassisNodesUsbsSchema.resource": False,
    "ChassisNodesUsbsSchema.opts": False,
    "ChassisNodesUsbs": False,
}


class ChassisNodesUsbsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ChassisNodesUsbs object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether or not the USB ports are enabled. """

    ports = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.chassis_nodes_usbs_ports.ChassisNodesUsbsPortsSchema", unknown=EXCLUDE, allow_none=True), data_key="ports", allow_none=True)
    r""" The ports field of the chassis_nodes_usbs. """

    supported = marshmallow_fields.Boolean(data_key="supported", allow_none=True)
    r""" Indicates whether or not USB ports are supported on the current platform. """

    @property
    def resource(self):
        return ChassisNodesUsbs

    gettable_fields = [
        "enabled",
        "ports",
        "supported",
    ]
    """enabled,ports,supported,"""

    patchable_fields = [
        "enabled",
        "ports",
        "supported",
    ]
    """enabled,ports,supported,"""

    postable_fields = [
        "enabled",
        "ports",
        "supported",
    ]
    """enabled,ports,supported,"""


class ChassisNodesUsbs(Resource):

    _schema = ChassisNodesUsbsSchema
