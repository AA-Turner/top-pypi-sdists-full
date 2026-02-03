r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["LocalStorage", "LocalStorageSchema"]
__pdoc__ = {
    "LocalStorageSchema.resource": False,
    "LocalStorageSchema.opts": False,
    "LocalStorage": False,
}

class LocalStorageSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LocalStorage object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the local storage. Required for a local data source in a POST request.

Example: vol1 """

    svm = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.resources.svm", "SvmSchema"),
                unknown=EXCLUDE,
                data_key="svm",
                allow_none=True
            )
    r""" The svm field of the local_storage. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The unique identifier of the local storage volume or bucket. Required for a local data source in a POST request.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return LocalStorage

    gettable_fields = [
        "name",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """name,svm.links,svm.name,svm.uuid,uuid,"""

    patchable_fields = [
        "name",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """name,svm.name,svm.uuid,uuid,"""

    postable_fields = [
        "name",
        "svm.name",
        "svm.uuid",
        "uuid",
    ]
    """name,svm.name,svm.uuid,uuid,"""


class LocalStorage(Resource):

    _schema = LocalStorageSchema
