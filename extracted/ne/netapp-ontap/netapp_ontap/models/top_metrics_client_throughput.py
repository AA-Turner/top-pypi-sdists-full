r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricsClientThroughput", "TopMetricsClientThroughputSchema"]
__pdoc__ = {
    "TopMetricsClientThroughputSchema.resource": False,
    "TopMetricsClientThroughputSchema.opts": False,
    "TopMetricsClientThroughput": False,
}


class TopMetricsClientThroughputSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsClientThroughput object"""

    error = marshmallow_fields.Nested("netapp_ontap.models.top_metric_value_error_bounds.TopMetricValueErrorBoundsSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" The error field of the top_metrics_client_throughput. """

    read = Size(data_key="read", allow_none=True)
    r""" Average number of read bytes received per second.

Example: 12 """

    write = Size(data_key="write", allow_none=True)
    r""" Average number of write bytes received per second.

Example: 2 """

    @property
    def resource(self):
        return TopMetricsClientThroughput

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


class TopMetricsClientThroughput(Resource):

    _schema = TopMetricsClientThroughputSchema
