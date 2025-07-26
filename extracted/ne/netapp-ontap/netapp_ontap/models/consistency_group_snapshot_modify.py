r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupSnapshotModify", "ConsistencyGroupSnapshotModifySchema"]
__pdoc__ = {
    "ConsistencyGroupSnapshotModifySchema.resource": False,
    "ConsistencyGroupSnapshotModifySchema.opts": False,
    "ConsistencyGroupSnapshotModify": False,
}


class ConsistencyGroupSnapshotModifySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupSnapshotModify object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Name of the snapshot. """

    @property
    def resource(self):
        return ConsistencyGroupSnapshotModify

    gettable_fields = [
        "name",
    ]
    """name,"""

    patchable_fields = [
        "name",
    ]
    """name,"""

    postable_fields = [
        "name",
    ]
    """name,"""


class ConsistencyGroupSnapshotModify(Resource):

    _schema = ConsistencyGroupSnapshotModifySchema
