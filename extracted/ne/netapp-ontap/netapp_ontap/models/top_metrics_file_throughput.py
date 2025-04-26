r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricsFileThroughput", "TopMetricsFileThroughputSchema"]
__pdoc__ = {
    "TopMetricsFileThroughputSchema.resource": False,
    "TopMetricsFileThroughputSchema.opts": False,
    "TopMetricsFileThroughput": False,
}


class TopMetricsFileThroughputSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsFileThroughput object"""

    error = marshmallow_fields.Nested("netapp_ontap.models.top_metric_value_error_bounds.TopMetricValueErrorBoundsSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" The error field of the top_metrics_file_throughput. """

    read = Size(data_key="read", allow_none=True)
    r""" Average number of read bytes received per second.

Example: 2 """

    write = Size(data_key="write", allow_none=True)
    r""" Average number of write bytes received per second.

Example: 20 """

    @property
    def resource(self):
        return TopMetricsFileThroughput

    gettable_fields = [
        "error",
        "read",
        "write",
    ]
    """error,read,write,"""

    patchable_fields = [
        "error",
    ]
    """error,"""

    postable_fields = [
        "error",
    ]
    """error,"""


class TopMetricsFileThroughput(Resource):

    _schema = TopMetricsFileThroughputSchema
