r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeNetworkExternalInterface", "DcnNodeNetworkExternalInterfaceSchema"]
__pdoc__ = {
    "DcnNodeNetworkExternalInterfaceSchema.resource": False,
    "DcnNodeNetworkExternalInterfaceSchema.opts": False,
    "DcnNodeNetworkExternalInterface": False,
}

class DcnNodeNetworkExternalInterfaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeNetworkExternalInterface object"""

    mac_address = marshmallow_fields.Str(data_key="mac_address", allow_none=True)
    r""" The MAC address of the node's external interface.

Example: 00:B0:D0:63:C2:26 """

    mtu = Size(data_key="mtu", allow_none=True)
    r""" The MTU of the external interface.

Example: 1500 """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The OS-level name of the external network interface.

Example: ext """

    @property
    def resource(self):
        return DcnNodeNetworkExternalInterface

    gettable_fields = [
        "mac_address",
        "mtu",
        "name",
    ]
    """mac_address,mtu,name,"""

    patchable_fields = [
        "mtu",
    ]
    """mtu,"""

    postable_fields = [
        "mtu",
    ]
    """mtu,"""


class DcnNodeNetworkExternalInterface(Resource):

    _schema = DcnNodeNetworkExternalInterfaceSchema
