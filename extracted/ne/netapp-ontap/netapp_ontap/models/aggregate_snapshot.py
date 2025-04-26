r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateSnapshot", "AggregateSnapshotSchema"]
__pdoc__ = {
    "AggregateSnapshotSchema.resource": False,
    "AggregateSnapshotSchema.opts": False,
    "AggregateSnapshot": False,
}


class AggregateSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateSnapshot object"""

    files_total = Size(data_key="files_total", allow_none=True)
    r""" Total files allowed in snapshots

Example: 10 """

    files_used = Size(data_key="files_used", allow_none=True)
    r""" Total files created in snapshots

Example: 3 """

    max_files_available = Size(data_key="max_files_available", allow_none=True)
    r""" Maximum files available for snapshots

Example: 5 """

    max_files_used = Size(data_key="max_files_used", allow_none=True)
    r""" Files in use by snapshots

Example: 50 """

    @property
    def resource(self):
        return AggregateSnapshot

    gettable_fields = [
        "files_total",
        "files_used",
        "max_files_available",
        "max_files_used",
    ]
    """files_total,files_used,max_files_available,max_files_used,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AggregateSnapshot(Resource):

    _schema = AggregateSnapshotSchema
