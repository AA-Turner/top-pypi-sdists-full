r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricsClientIops", "TopMetricsClientIopsSchema"]
__pdoc__ = {
    "TopMetricsClientIopsSchema.resource": False,
    "TopMetricsClientIopsSchema.opts": False,
    "TopMetricsClientIops": False,
}


class TopMetricsClientIopsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsClientIops object"""

    error = marshmallow_fields.Nested("netapp_ontap.models.top_metric_value_error_bounds.TopMetricValueErrorBoundsSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" The error field of the top_metrics_client_iops. """

    read = Size(data_key="read", allow_none=True)
    r""" Average number of read operations per second.

Example: 5 """

    write = Size(data_key="write", allow_none=True)
    r""" Average number of write operations per second.

Example: 10 """

    @property
    def resource(self):
        return TopMetricsClientIops

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


class TopMetricsClientIops(Resource):

    _schema = TopMetricsClientIopsSchema
