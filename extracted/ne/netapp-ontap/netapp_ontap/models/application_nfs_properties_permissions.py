r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationNfsPropertiesPermissions", "ApplicationNfsPropertiesPermissionsSchema"]
__pdoc__ = {
    "ApplicationNfsPropertiesPermissionsSchema.resource": False,
    "ApplicationNfsPropertiesPermissionsSchema.opts": False,
    "ApplicationNfsPropertiesPermissions": False,
}


class ApplicationNfsPropertiesPermissionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationNfsPropertiesPermissions object"""

    access = marshmallow_fields.Str(data_key="access", allow_none=True)
    r""" Access granted to the host """

    host = marshmallow_fields.Str(data_key="host", allow_none=True)
    r""" Host granted access """

    @property
    def resource(self):
        return ApplicationNfsPropertiesPermissions

    gettable_fields = [
        "access",
        "host",
    ]
    """access,host,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationNfsPropertiesPermissions(Resource):

    _schema = ApplicationNfsPropertiesPermissionsSchema
