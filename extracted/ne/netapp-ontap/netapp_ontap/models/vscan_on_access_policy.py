r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["VscanOnAccessPolicy", "VscanOnAccessPolicySchema"]
__pdoc__ = {
    "VscanOnAccessPolicySchema.resource": False,
    "VscanOnAccessPolicySchema.opts": False,
    "VscanOnAccessPolicy": False,
}

class VscanOnAccessPolicySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VscanOnAccessPolicy object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Status of the On-Access Vscan policy """

    mandatory = marshmallow_fields.Boolean(data_key="mandatory", allow_none=True)
    r""" Specifies if scanning is mandatory. File access is denied if there are no external virus-scanning servers available for virus scanning. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" On-Access policy name

Example: on-access-test """

    protocol = marshmallow_fields.Str(data_key="protocol", allow_none=True)
    r""" Specifies the file access protocol for the on-access policy. The following lists the possible protocols. CIFS  - SMB protocol

Valid choices:

* cifs """

    scope = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.vscan_on_access_scope", "VscanOnAccessScopeSchema"),
                unknown=EXCLUDE,
                data_key="scope",
                allow_none=True
            )
    r""" The scope field of the vscan_on_access_policy. """

    @property
    def resource(self):
        return VscanOnAccessPolicy

    gettable_fields = [
        "enabled",
        "mandatory",
        "name",
        "protocol",
        "scope",
    ]
    """enabled,mandatory,name,protocol,scope,"""

    patchable_fields = [
        "enabled",
        "mandatory",
        "protocol",
        "scope",
    ]
    """enabled,mandatory,protocol,scope,"""

    postable_fields = [
        "enabled",
        "mandatory",
        "name",
        "protocol",
        "scope",
    ]
    """enabled,mandatory,name,protocol,scope,"""


class VscanOnAccessPolicy(Resource):

    _schema = VscanOnAccessPolicySchema
