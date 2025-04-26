r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricsDirectoryIops", "TopMetricsDirectoryIopsSchema"]
__pdoc__ = {
    "TopMetricsDirectoryIopsSchema.resource": False,
    "TopMetricsDirectoryIopsSchema.opts": False,
    "TopMetricsDirectoryIops": False,
}


class TopMetricsDirectoryIopsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsDirectoryIops object"""

    error = marshmallow_fields.Nested("netapp_ontap.models.top_metric_value_error_bounds.TopMetricValueErrorBoundsSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" The error field of the top_metrics_directory_iops. """

    read = Size(data_key="read", allow_none=True)
    r""" Average number of read operations per second.

Example: 10 """

    write = Size(data_key="write", allow_none=True)
    r""" Average number of write operations per second.

Example: 5 """

    @property
    def resource(self):
        return TopMetricsDirectoryIops

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


class TopMetricsDirectoryIops(Resource):

    _schema = TopMetricsDirectoryIopsSchema
