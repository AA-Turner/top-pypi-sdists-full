r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupSnapshotSnaplock", "ConsistencyGroupSnapshotSnaplockSchema"]
__pdoc__ = {
    "ConsistencyGroupSnapshotSnaplockSchema.resource": False,
    "ConsistencyGroupSnapshotSnaplockSchema.opts": False,
    "ConsistencyGroupSnapshotSnaplock": False,
}


class ConsistencyGroupSnapshotSnaplockSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupSnapshotSnaplock object"""

    expired = marshmallow_fields.Boolean(data_key="expired", allow_none=True)
    r""" Indicates whether a SnapLock snapshot has expired.

Example: true """

    expiry_time = ImpreciseDateTime(data_key="expiry_time", allow_none=True)
    r""" SnapLock expiry time for the snapshot, if the snapshot is taken on a consistency-group. A snapshot is not allowed to be deleted until the SnapLock ComplianceClock time goes beyond this expiry time.

Example: 2019-02-04T19:00:00.000+0000 """

    time_until_expiry = marshmallow_fields.Str(data_key="time_until_expiry", allow_none=True)
    r""" Indicates the remaining SnapLock expiry time of a locked snapshot, in iso8601 period format. This field is set only when the remaining time interval is less than 136 years.

Example: PT3H27M45S """

    @property
    def resource(self):
        return ConsistencyGroupSnapshotSnaplock

    gettable_fields = [
        "expired",
        "expiry_time",
        "time_until_expiry",
    ]
    """expired,expiry_time,time_until_expiry,"""

    patchable_fields = [
        "expiry_time",
    ]
    """expiry_time,"""

    postable_fields = [
        "expiry_time",
    ]
    """expiry_time,"""


class ConsistencyGroupSnapshotSnaplock(Resource):

    _schema = ConsistencyGroupSnapshotSnaplockSchema
