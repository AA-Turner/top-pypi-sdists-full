r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["StorageUnitSpaceSnapshot1Autodelete", "StorageUnitSpaceSnapshot1AutodeleteSchema"]
__pdoc__ = {
    "StorageUnitSpaceSnapshot1AutodeleteSchema.resource": False,
    "StorageUnitSpaceSnapshot1AutodeleteSchema.opts": False,
    "StorageUnitSpaceSnapshot1Autodelete": False,
}

class StorageUnitSpaceSnapshot1AutodeleteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitSpaceSnapshot1Autodelete object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether snapshot autodelete is currently enabled. """

    @property
    def resource(self):
        return StorageUnitSpaceSnapshot1Autodelete

    gettable_fields = [
        "enabled",
    ]
    """enabled,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
    ]
    """"""


class StorageUnitSpaceSnapshot1Autodelete(Resource):

    _schema = StorageUnitSpaceSnapshot1AutodeleteSchema
