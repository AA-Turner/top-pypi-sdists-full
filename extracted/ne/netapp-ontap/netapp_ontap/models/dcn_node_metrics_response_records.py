r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeMetricsResponseRecords", "DcnNodeMetricsResponseRecordsSchema"]
__pdoc__ = {
    "DcnNodeMetricsResponseRecordsSchema.resource": False,
    "DcnNodeMetricsResponseRecordsSchema.opts": False,
    "DcnNodeMetricsResponseRecords": False,
}

class DcnNodeMetricsResponseRecordsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeMetricsResponseRecords object"""

    cpu = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_metrics_cpu", "DcnNodeMetricsCpuSchema"),
                unknown=EXCLUDE,
                data_key="cpu",
                allow_none=True
            )
    r""" The cpu field of the dcn_node_metrics_response_records. """

    duration = marshmallow_fields.Str(data_key="duration", allow_none=True)
    r""" The duration over which this sample is calculated. The time durations are represented in the ISO-8601 standard format. Samples can be calculated over the following durations:


Valid choices:

* PT15S
* PT5M
* PT30M
* PT2H
* P1D """

    gpu = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_metrics_gpu", "DcnNodeMetricsGpuSchema"),
                unknown=EXCLUDE,
                data_key="gpu",
                allow_none=True
            )
    r""" The gpu field of the dcn_node_metrics_response_records. """

    status = marshmallow_fields.Str(data_key="status", allow_none=True)
    r""" * ok: The sample was collected successfully without any errors.
* error: An internal uncategorized failure occurred during the sample collection.
* partial_no_data: The sample collection was incomplete due to missing data.
* partial_no_uuid: The sample collection was incomplete due to a missing UUID.
* partial_no_response: The sample collection was incomplete due to no response from one or more nodes.
* partial_other_error: The sample collection was incomplete due to other unspecified errors.
* negative_delta: An expected monotonically increasing value has decreased in value.
* backfilled_data: The sample collection was completed at a later time and backfilled to the previous 15-second timestamp.
* inconsistent_delta_time: The time between two collections is not the same for all nodes, causing the aggregated value to be over or under-inflated.
* inconsistent_old_data: One or more nodes do not have the latest data.


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

    timestamp = ImpreciseDateTime(data_key="timestamp", allow_none=True)
    r""" The timestamp of the performance data.

Example: 2017-01-25T11:20:13.000+0000 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Unique identifier for the node.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return DcnNodeMetricsResponseRecords

    gettable_fields = [
        "cpu",
        "duration",
        "gpu",
        "status",
        "timestamp",
        "uuid",
    ]
    """cpu,duration,gpu,status,timestamp,uuid,"""

    patchable_fields = [
        "cpu",
        "duration",
        "gpu",
        "status",
        "timestamp",
        "uuid",
    ]
    """cpu,duration,gpu,status,timestamp,uuid,"""

    postable_fields = [
        "cpu",
        "duration",
        "gpu",
        "status",
        "timestamp",
        "uuid",
    ]
    """cpu,duration,gpu,status,timestamp,uuid,"""


class DcnNodeMetricsResponseRecords(Resource):

    _schema = DcnNodeMetricsResponseRecordsSchema
