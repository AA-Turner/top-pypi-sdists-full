r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PerformanceLunMetricSpace", "PerformanceLunMetricSpaceSchema"]
__pdoc__ = {
    "PerformanceLunMetricSpaceSchema.resource": False,
    "PerformanceLunMetricSpaceSchema.opts": False,
    "PerformanceLunMetricSpace": False,
}


class PerformanceLunMetricSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PerformanceLunMetricSpace object"""

    available = Size(data_key="available", allow_none=True)
    r""" Total available free space of the LUN.


Example: 924 """

    duration = marshmallow_fields.Str(data_key="duration", allow_none=True)
    r""" The duration over which this sample is calculated. The time durations are represented in the ISO-8601 standard format. Samples can be calculated over the following durations:


Valid choices:

* PT15S
* PT5M
* PT30M
* PT2H
* PT1D """

    size = Size(data_key="size", allow_none=True)
    r""" Total allocated space of the LUN.


Example: 1024 """

    status = marshmallow_fields.Str(data_key="status", allow_none=True)
    r""" Errors associated with the sample. For example, if the aggregation of data over multiple nodes fails, any partial errors might return "ok" on success or "error" on an internal uncategorized failure. When a sample collection is missed but completed at a later time, it is back filled to the previous 15 second timestamp and tagged with "backfilled_data". The "Inconsistent_ delta_time" error occurs when the time between two collections is not the same for all nodes. Therefore, the aggregated value might be over or under inflated. "Negative_delta" is returned when an expected monotonically increasing value has decreased in value. "Inconsistent_old_data" is returned when one or more nodes do not have the latest data.

Valid choices:

* ok
* error
* partial_no_data
* partial_no_uuid
* partial_no_response
* partial_other_error
* negative_delta
* backfilled_data
* inconsistent_delta_time
* inconsistent_old_data """

    used = Size(data_key="used", allow_none=True)
    r""" Total occupied space of the LUN.


Example: 100 """

    used_by_snapshots = Size(data_key="used_by_snapshots", allow_none=True)
    r""" Total space used by snapshots of the LUN.


Example: 30 """

    @property
    def resource(self):
        return PerformanceLunMetricSpace

    gettable_fields = [
        "available",
        "duration",
        "size",
        "status",
        "used",
        "used_by_snapshots",
    ]
    """available,duration,size,status,used,used_by_snapshots,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class PerformanceLunMetricSpace(Resource):

    _schema = PerformanceLunMetricSpaceSchema
