r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["DcnNodeStatistics", "DcnNodeStatisticsSchema"]
__pdoc__ = {
    "DcnNodeStatisticsSchema.resource": False,
    "DcnNodeStatisticsSchema.opts": False,
    "DcnNodeStatistics": False,
}

class DcnNodeStatisticsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DcnNodeStatistics object"""

    cpu = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_statistics_cpu", "DcnNodeStatisticsCpuSchema"),
                unknown=EXCLUDE,
                data_key="cpu",
                allow_none=True
            )
    r""" The cpu field of the dcn_node_statistics. """

    gpu = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.dcn_node_statistics_gpu", "DcnNodeStatisticsGpuSchema"),
                unknown=EXCLUDE,
                data_key="gpu",
                allow_none=True
            )
    r""" The gpu field of the dcn_node_statistics. """

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

    @property
    def resource(self):
        return DcnNodeStatistics

    gettable_fields = [
        "cpu",
        "gpu",
        "status",
        "timestamp",
    ]
    """cpu,gpu,status,timestamp,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class DcnNodeStatistics(Resource):

    _schema = DcnNodeStatisticsSchema
