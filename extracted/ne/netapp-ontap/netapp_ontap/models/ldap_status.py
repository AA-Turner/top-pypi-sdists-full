r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LdapStatus", "LdapStatusSchema"]
__pdoc__ = {
    "LdapStatusSchema.resource": False,
    "LdapStatusSchema.opts": False,
    "LdapStatus": False,
}


class LdapStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LdapStatus object"""

    code = Size(data_key="code", allow_none=True)
    r""" This field is no longer supported. Use ipv4.code or ipv6.code instead.


Example: 65537300 """

    dn_message = marshmallow_fields.List(marshmallow_fields.Str, data_key="dn_message", allow_none=True)
    r""" The dn_message field of the ldap_status. """

    ipv4 = marshmallow_fields.Nested("netapp_ontap.models.ldap_ip_status.LdapIpStatusSchema", unknown=EXCLUDE, data_key="ipv4", allow_none=True)
    r""" The ipv4 field of the ldap_status. """

    ipv4_state = marshmallow_fields.Str(data_key="ipv4_state", allow_none=True)
    r""" This field is no longer supported. Use ipv4.state instead.


Valid choices:

* up
* down """

    ipv6 = marshmallow_fields.Nested("netapp_ontap.models.ldap_ip_status.LdapIpStatusSchema", unknown=EXCLUDE, data_key="ipv6", allow_none=True)
    r""" The ipv6 field of the ldap_status. """

    ipv6_state = marshmallow_fields.Str(data_key="ipv6_state", allow_none=True)
    r""" This field is no longer supported. Use ipv6.state instead.


Valid choices:

* up
* down """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" This field is no longer supported. Use ipv4.message or ipv6.message instead. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The status of the LDAP service for the SVM. The LDAP service is up if either `ipv4_state` or `ipv6_state` is up.
The LDAP service is down if both `ipv4_state` and `ipv6_state` are down.


Valid choices:

* up
* down """

    @property
    def resource(self):
        return LdapStatus

    gettable_fields = [
        "code",
        "dn_message",
        "ipv4",
        "ipv4_state",
        "ipv6",
        "ipv6_state",
        "message",
        "state",
    ]
    """code,dn_message,ipv4,ipv4_state,ipv6,ipv6_state,message,state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class LdapStatus(Resource):

    _schema = LdapStatusSchema
