r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["KerberosRealmKdc", "KerberosRealmKdcSchema"]
__pdoc__ = {
    "KerberosRealmKdcSchema.resource": False,
    "KerberosRealmKdcSchema.opts": False,
    "KerberosRealmKdc": False,
}


class KerberosRealmKdcSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the KerberosRealmKdc object"""

    ip = marshmallow_fields.Str(data_key="ip", allow_none=True)
    r""" KDC IP address

Example: 1.2.3.4 """

    port = Size(data_key="port", allow_none=True)
    r""" KDC port

Example: 88 """

    vendor = marshmallow_fields.Str(data_key="vendor", allow_none=True)
    r""" Key Distribution Center (KDC) vendor. Following values are supported:

* microsoft - Microsoft Active Directory KDC
* other - MIT Kerberos KDC or other KDC


Valid choices:

* microsoft
* other """

    @property
    def resource(self):
        return KerberosRealmKdc

    gettable_fields = [
        "ip",
        "port",
        "vendor",
    ]
    """ip,port,vendor,"""

    patchable_fields = [
        "ip",
        "port",
        "vendor",
    ]
    """ip,port,vendor,"""

    postable_fields = [
        "ip",
        "port",
        "vendor",
    ]
    """ip,port,vendor,"""


class KerberosRealmKdc(Resource):

    _schema = KerberosRealmKdcSchema
