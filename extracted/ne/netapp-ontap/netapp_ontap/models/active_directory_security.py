r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ActiveDirectorySecurity", "ActiveDirectorySecuritySchema"]
__pdoc__ = {
    "ActiveDirectorySecuritySchema.resource": False,
    "ActiveDirectorySecuritySchema.opts": False,
    "ActiveDirectorySecurity": False,
}


class ActiveDirectorySecuritySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ActiveDirectorySecurity object"""

    advertised_kdc_encryptions = marshmallow_fields.List(marshmallow_fields.Str, data_key="advertised_kdc_encryptions", allow_none=True)
    r""" The advertised_kdc_encryptions field of the active_directory_security. """

    @property
    def resource(self):
        return ActiveDirectorySecurity

    gettable_fields = [
        "advertised_kdc_encryptions",
    ]
    """advertised_kdc_encryptions,"""

    patchable_fields = [
        "advertised_kdc_encryptions",
    ]
    """advertised_kdc_encryptions,"""

    postable_fields = [
        "advertised_kdc_encryptions",
    ]
    """advertised_kdc_encryptions,"""


class ActiveDirectorySecurity(Resource):

    _schema = ActiveDirectorySecuritySchema
