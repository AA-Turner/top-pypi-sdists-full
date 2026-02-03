r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["VdiskSpaceSnapshotAutodelete", "VdiskSpaceSnapshotAutodeleteSchema"]
__pdoc__ = {
    "VdiskSpaceSnapshotAutodeleteSchema.resource": False,
    "VdiskSpaceSnapshotAutodeleteSchema.opts": False,
    "VdiskSpaceSnapshotAutodelete": False,
}

class VdiskSpaceSnapshotAutodeleteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VdiskSpaceSnapshotAutodelete object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether snapshot autodelete is currently enabled. """

    @property
    def resource(self):
        return VdiskSpaceSnapshotAutodelete

    gettable_fields = [
        "enabled",
    ]
    """enabled,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""


class VdiskSpaceSnapshotAutodelete(Resource):

    _schema = VdiskSpaceSnapshotAutodeleteSchema
