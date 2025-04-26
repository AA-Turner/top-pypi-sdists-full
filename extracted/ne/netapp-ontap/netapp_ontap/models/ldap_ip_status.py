r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LdapIpStatus", "LdapIpStatusSchema"]
__pdoc__ = {
    "LdapIpStatusSchema.resource": False,
    "LdapIpStatusSchema.opts": False,
    "LdapIpStatus": False,
}


class LdapIpStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LdapIpStatus object"""

    code = Size(data_key="code", allow_none=True)
    r""" Code corresponding to the error message. If there is no error, it is 0 to indicate success.


Example: 65537300 """

    dn_messages = marshmallow_fields.List(marshmallow_fields.Str, data_key="dn_messages", allow_none=True)
    r""" The dn_messages field of the ldap_ip_status. """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Provides additional details on the error. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Status of the LDAP service.


Valid choices:

* up
* down """

    @property
    def resource(self):
        return LdapIpStatus

    gettable_fields = [
        "code",
        "dn_messages",
        "message",
        "state",
    ]
    """code,dn_messages,message,state,"""

    patchable_fields = [
        "code",
        "dn_messages",
        "message",
        "state",
    ]
    """code,dn_messages,message,state,"""

    postable_fields = [
        "code",
        "dn_messages",
        "message",
        "state",
    ]
    """code,dn_messages,message,state,"""


class LdapIpStatus(Resource):

    _schema = LdapIpStatusSchema
