r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AccountApplication", "AccountApplicationSchema"]
__pdoc__ = {
    "AccountApplicationSchema.resource": False,
    "AccountApplicationSchema.opts": False,
    "AccountApplication": False,
}


class AccountApplicationSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AccountApplication object"""

    application = marshmallow_fields.Str(data_key="application", allow_none=True)
    r""" Applications

Valid choices:

* amqp
* console
* http
* ontapi
* service_processor
* ssh """

    authentication_methods = marshmallow_fields.List(marshmallow_fields.Str, data_key="authentication_methods", allow_none=True)
    r""" The authentication_methods field of the account_application. """

    is_ldap_fastbind = marshmallow_fields.Boolean(data_key="is_ldap_fastbind", allow_none=True)
    r""" Optional property that specifies the mode of authentication as LDAP Fastbind. """

    is_ns_switch_group = marshmallow_fields.Boolean(data_key="is_ns_switch_group", allow_none=True)
    r""" Optional property that specifies whether the user is an LDAP or NIS group. """

    second_authentication_method = marshmallow_fields.Str(data_key="second_authentication_method", allow_none=True)
    r""" An optional additional authentication method for multi-factor authentication (MFA). This property is only supported for SSH (_ssh_) and Service Processor (_service_processor_) applications. It is ignored for all other applications. Time-based One-Time Passwords (TOTPs) are only supported with the authentication method password or public key. For the Service Processor (_service_processor_) application, _none_ and _publickey_ are the only supported enum values.

Valid choices:

* none
* password
* publickey
* nsswitch
* domain
* totp """

    @property
    def resource(self):
        return AccountApplication

    gettable_fields = [
        "application",
        "authentication_methods",
        "is_ldap_fastbind",
        "is_ns_switch_group",
        "second_authentication_method",
    ]
    """application,authentication_methods,is_ldap_fastbind,is_ns_switch_group,second_authentication_method,"""

    patchable_fields = [
        "application",
        "authentication_methods",
        "is_ldap_fastbind",
        "is_ns_switch_group",
        "second_authentication_method",
    ]
    """application,authentication_methods,is_ldap_fastbind,is_ns_switch_group,second_authentication_method,"""

    postable_fields = [
        "application",
        "authentication_methods",
        "is_ldap_fastbind",
        "is_ns_switch_group",
        "second_authentication_method",
    ]
    """application,authentication_methods,is_ldap_fastbind,is_ns_switch_group,second_authentication_method,"""


class AccountApplication(Resource):

    _schema = AccountApplicationSchema
