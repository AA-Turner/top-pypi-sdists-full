r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ActiveDirectoryPreferredDcs", "ActiveDirectoryPreferredDcsSchema"]
__pdoc__ = {
    "ActiveDirectoryPreferredDcsSchema.resource": False,
    "ActiveDirectoryPreferredDcsSchema.opts": False,
    "ActiveDirectoryPreferredDcs": False,
}


class ActiveDirectoryPreferredDcsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ActiveDirectoryPreferredDcs object"""

    fqdn = marshmallow_fields.Str(data_key="fqdn", allow_none=True)
    r""" Fully Qualified Domain Name.

Example: test.com """

    server_ip = marshmallow_fields.Str(data_key="server_ip", allow_none=True)
    r""" IP address of the preferred DC. The address can be either an IPv4 or an IPv6 address.

Example: 4.4.4.4 """

    @property
    def resource(self):
        return ActiveDirectoryPreferredDcs

    gettable_fields = [
        "fqdn",
        "server_ip",
    ]
    """fqdn,server_ip,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "fqdn",
        "server_ip",
    ]
    """fqdn,server_ip,"""


class ActiveDirectoryPreferredDcs(Resource):

    _schema = ActiveDirectoryPreferredDcsSchema
