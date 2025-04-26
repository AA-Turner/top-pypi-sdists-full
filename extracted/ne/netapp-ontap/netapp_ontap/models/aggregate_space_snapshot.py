r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateSpaceSnapshot", "AggregateSpaceSnapshotSchema"]
__pdoc__ = {
    "AggregateSpaceSnapshotSchema.resource": False,
    "AggregateSpaceSnapshotSchema.opts": False,
    "AggregateSpaceSnapshot": False,
}


class AggregateSpaceSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateSpaceSnapshot object"""

    available = Size(data_key="available", allow_none=True)
    r""" Available space for snapshots in bytes

Example: 2000 """

    reserve_percent = Size(data_key="reserve_percent", allow_none=True)
    r""" Percentage of space reserved for snapshots

Example: 20 """

    total = Size(data_key="total", allow_none=True)
    r""" Total space for snapshots in bytes

Example: 5000 """

    used = Size(data_key="used", allow_none=True)
    r""" Space used by snapshots in bytes

Example: 3000 """

    used_percent = Size(data_key="used_percent", allow_none=True)
    r""" Percentage of disk space used by snapshots

Example: 45 """

    @property
    def resource(self):
        return AggregateSpaceSnapshot

    gettable_fields = [
        "available",
        "reserve_percent",
        "total",
        "used",
        "used_percent",
    ]
    """available,reserve_percent,total,used,used_percent,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class AggregateSpaceSnapshot(Resource):

    _schema = AggregateSpaceSnapshotSchema
