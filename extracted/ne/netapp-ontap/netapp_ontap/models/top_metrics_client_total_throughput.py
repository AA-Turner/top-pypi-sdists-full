r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["TopMetricsClientTotalThroughput", "TopMetricsClientTotalThroughputSchema"]
__pdoc__ = {
    "TopMetricsClientTotalThroughputSchema.resource": False,
    "TopMetricsClientTotalThroughputSchema.opts": False,
    "TopMetricsClientTotalThroughput": False,
}

class TopMetricsClientTotalThroughputSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsClientTotalThroughput object"""

    error = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.top_metric_value_error_bounds", "TopMetricValueErrorBoundsSchema"),
                unknown=EXCLUDE,
                data_key="error",
                allow_none=True
            )
    r""" The error field of the top_metrics_client_total_throughput. """

    read = Size(data_key="read", allow_none=True)
    r""" Total bytes read in the observation window.

Example: 2800 """

    write = Size(data_key="write", allow_none=True)
    r""" Total bytes written in the observation window.

Example: 600 """

    @property
    def resource(self):
        return TopMetricsClientTotalThroughput

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


class TopMetricsClientTotalThroughput(Resource):

    _schema = TopMetricsClientTotalThroughputSchema
