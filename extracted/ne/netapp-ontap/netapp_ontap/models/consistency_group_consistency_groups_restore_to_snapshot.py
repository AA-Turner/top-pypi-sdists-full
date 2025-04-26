r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupConsistencyGroupsRestoreToSnapshot", "ConsistencyGroupConsistencyGroupsRestoreToSnapshotSchema"]
__pdoc__ = {
    "ConsistencyGroupConsistencyGroupsRestoreToSnapshotSchema.resource": False,
    "ConsistencyGroupConsistencyGroupsRestoreToSnapshotSchema.opts": False,
    "ConsistencyGroupConsistencyGroupsRestoreToSnapshot": False,
}


class ConsistencyGroupConsistencyGroupsRestoreToSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupConsistencyGroupsRestoreToSnapshot object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name of the consistency group's snapshot to restore to. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The UUID of the consistency group's snapshot to restore to. """

    @property
    def resource(self):
        return ConsistencyGroupConsistencyGroupsRestoreToSnapshot

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class ConsistencyGroupConsistencyGroupsRestoreToSnapshot(Resource):

    _schema = ConsistencyGroupConsistencyGroupsRestoreToSnapshotSchema
