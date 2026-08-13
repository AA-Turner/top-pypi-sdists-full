r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["SecurityClusterNetworkIpsecPolicyLocalIp", "SecurityClusterNetworkIpsecPolicyLocalIpSchema"]
__pdoc__ = {
    "SecurityClusterNetworkIpsecPolicyLocalIpSchema.resource": False,
    "SecurityClusterNetworkIpsecPolicyLocalIpSchema.opts": False,
    "SecurityClusterNetworkIpsecPolicyLocalIp": False,
}

class SecurityClusterNetworkIpsecPolicyLocalIpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityClusterNetworkIpsecPolicyLocalIp object"""

    address = marshmallow_fields.Str(data_key="address", allow_none=True)
    r""" IPv4 or IPv6 address.

Example: 192.168.1.1 """

    netmask = Size(data_key="netmask", allow_none=True)
    r""" IPv4 mask length or IPv6 prefix length.

Example: 24 """

    @property
    def resource(self):
        return SecurityClusterNetworkIpsecPolicyLocalIp

    gettable_fields = [
        "address",
        "netmask",
    ]
    """address,netmask,"""

    patchable_fields = [
        "address",
        "netmask",
    ]
    """address,netmask,"""

    postable_fields = [
        "address",
        "netmask",
    ]
    """address,netmask,"""


class SecurityClusterNetworkIpsecPolicyLocalIp(Resource):

    _schema = SecurityClusterNetworkIpsecPolicyLocalIpSchema
