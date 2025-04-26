r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationCifsProperties", "ApplicationCifsPropertiesSchema"]
__pdoc__ = {
    "ApplicationCifsPropertiesSchema.resource": False,
    "ApplicationCifsPropertiesSchema.opts": False,
    "ApplicationCifsProperties": False,
}


class ApplicationCifsPropertiesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationCifsProperties object"""

    backing_storage = marshmallow_fields.Nested("netapp_ontap.models.application_cifs_properties_backing_storage.ApplicationCifsPropertiesBackingStorageSchema", unknown=EXCLUDE, data_key="backing_storage", allow_none=True)
    r""" The backing_storage field of the application_cifs_properties. """

    ips = marshmallow_fields.List(marshmallow_fields.Str, data_key="ips", allow_none=True)
    r""" The ips field of the application_cifs_properties. """

    path = marshmallow_fields.Str(data_key="path", allow_none=True)
    r""" Junction path """

    permissions = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.application_cifs_properties_permissions.ApplicationCifsPropertiesPermissionsSchema", unknown=EXCLUDE, allow_none=True), data_key="permissions", allow_none=True)
    r""" The permissions field of the application_cifs_properties. """

    server = marshmallow_fields.Nested("netapp_ontap.models.application_cifs_properties_server.ApplicationCifsPropertiesServerSchema", unknown=EXCLUDE, data_key="server", allow_none=True)
    r""" The server field of the application_cifs_properties. """

    share = marshmallow_fields.Nested("netapp_ontap.models.application_cifs_properties_share.ApplicationCifsPropertiesShareSchema", unknown=EXCLUDE, data_key="share", allow_none=True)
    r""" The share field of the application_cifs_properties. """

    @property
    def resource(self):
        return ApplicationCifsProperties

    gettable_fields = [
        "backing_storage",
        "ips",
        "path",
        "permissions",
        "server",
        "share",
    ]
    """backing_storage,ips,path,permissions,server,share,"""

    patchable_fields = [
        "ips",
    ]
    """ips,"""

    postable_fields = [
        "ips",
    ]
    """ips,"""


class ApplicationCifsProperties(Resource):

    _schema = ApplicationCifsPropertiesSchema
