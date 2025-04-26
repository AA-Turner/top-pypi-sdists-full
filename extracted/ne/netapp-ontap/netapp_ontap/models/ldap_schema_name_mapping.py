r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LdapSchemaNameMapping", "LdapSchemaNameMappingSchema"]
__pdoc__ = {
    "LdapSchemaNameMappingSchema.resource": False,
    "LdapSchemaNameMappingSchema.opts": False,
    "LdapSchemaNameMapping": False,
}


class LdapSchemaNameMappingSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LdapSchemaNameMapping object"""

    account = marshmallow_fields.Nested("netapp_ontap.models.ldap_schema_account.LdapSchemaAccountSchema", unknown=EXCLUDE, data_key="account", allow_none=True)
    r""" The account field of the ldap_schema_name_mapping. """

    windows_to_unix = marshmallow_fields.Nested("netapp_ontap.models.windows_to_unix.WindowsToUnixSchema", unknown=EXCLUDE, data_key="windows_to_unix", allow_none=True)
    r""" The windows_to_unix field of the ldap_schema_name_mapping. """

    @property
    def resource(self):
        return LdapSchemaNameMapping

    gettable_fields = [
        "account",
        "windows_to_unix",
    ]
    """account,windows_to_unix,"""

    patchable_fields = [
        "account",
        "windows_to_unix",
    ]
    """account,windows_to_unix,"""

    postable_fields = [
    ]
    """"""


class LdapSchemaNameMapping(Resource):

    _schema = LdapSchemaNameMappingSchema
