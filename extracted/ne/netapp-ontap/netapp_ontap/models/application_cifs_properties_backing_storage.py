r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ApplicationCifsPropertiesBackingStorage", "ApplicationCifsPropertiesBackingStorageSchema"]
__pdoc__ = {
    "ApplicationCifsPropertiesBackingStorageSchema.resource": False,
    "ApplicationCifsPropertiesBackingStorageSchema.opts": False,
    "ApplicationCifsPropertiesBackingStorage": False,
}


class ApplicationCifsPropertiesBackingStorageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ApplicationCifsPropertiesBackingStorage object"""

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Backing storage type

Valid choices:

* volume """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Backing storage UUID """

    @property
    def resource(self):
        return ApplicationCifsPropertiesBackingStorage

    gettable_fields = [
        "type",
        "uuid",
    ]
    """type,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class ApplicationCifsPropertiesBackingStorage(Resource):

    _schema = ApplicationCifsPropertiesBackingStorageSchema
