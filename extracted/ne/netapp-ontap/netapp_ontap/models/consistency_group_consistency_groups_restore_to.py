r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupConsistencyGroupsRestoreTo", "ConsistencyGroupConsistencyGroupsRestoreToSchema"]
__pdoc__ = {
    "ConsistencyGroupConsistencyGroupsRestoreToSchema.resource": False,
    "ConsistencyGroupConsistencyGroupsRestoreToSchema.opts": False,
    "ConsistencyGroupConsistencyGroupsRestoreTo": False,
}


class ConsistencyGroupConsistencyGroupsRestoreToSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupConsistencyGroupsRestoreTo object"""

    snapshot = marshmallow_fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_restore_to_snapshot.ConsistencyGroupConsistencyGroupsRestoreToSnapshotSchema", unknown=EXCLUDE, data_key="snapshot", allow_none=True)
    r""" A consistency group's snapshot """

    @property
    def resource(self):
        return ConsistencyGroupConsistencyGroupsRestoreTo

    gettable_fields = [
        "snapshot",
    ]
    """snapshot,"""

    patchable_fields = [
        "snapshot",
    ]
    """snapshot,"""

    postable_fields = [
        "snapshot",
    ]
    """snapshot,"""


class ConsistencyGroupConsistencyGroupsRestoreTo(Resource):

    _schema = ConsistencyGroupConsistencyGroupsRestoreToSchema
