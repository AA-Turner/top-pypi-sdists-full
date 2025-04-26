r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationNfsProperties", "ApplicationNfsPropertiesSchema"]
__pdoc__ = {
    "ApplicationNfsPropertiesSchema.resource": False,
    "ApplicationNfsPropertiesSchema.opts": False,
    "ApplicationNfsProperties": False,
}


class ApplicationNfsPropertiesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationNfsProperties object"""

    backing_storage = marshmallow_fields.Nested("netapp_ontap.models.application_cifs_properties_backing_storage.ApplicationCifsPropertiesBackingStorageSchema", unknown=EXCLUDE, data_key="backing_storage", allow_none=True)
    r""" The backing_storage field of the application_nfs_properties. """

    export_policy = marshmallow_fields.Nested("netapp_ontap.models.application_nfs_properties_export_policy.ApplicationNfsPropertiesExportPolicySchema", unknown=EXCLUDE, data_key="export_policy", allow_none=True)
    r""" The export_policy field of the application_nfs_properties. """

    ips = marshmallow_fields.List(marshmallow_fields.Str, data_key="ips", allow_none=True)
    r""" The ips field of the application_nfs_properties. """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" Junction path """

    permissions = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_nfs_properties_permissions.ApplicationNfsPropertiesPermissionsSchema", unknown=EXCLUDE, allow_none=True), data_key="permissions", allow_none=True)
    r""" The permissions field of the application_nfs_properties. """

    @property
    def resource(self):
        return ApplicationNfsProperties

    gettable_fields = [
        "backing_storage",
        "export_policy",
        "ips",
        "path",
        "permissions",
    ]
    """backing_storage,export_policy,ips,path,permissions,"""

    patchable_fields = [
        "ips",
    ]
    """ips,"""

    postable_fields = [
        "ips",
    ]
    """ips,"""


class ApplicationNfsProperties(Resource):

    _schema = ApplicationNfsPropertiesSchema
