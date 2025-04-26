r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricsSvmUserIops", "TopMetricsSvmUserIopsSchema"]
__pdoc__ = {
    "TopMetricsSvmUserIopsSchema.resource": False,
    "TopMetricsSvmUserIopsSchema.opts": False,
    "TopMetricsSvmUserIops": False,
}


class TopMetricsSvmUserIopsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsSvmUserIops object"""

    error = marshmallow_fields.Nested("netapp_ontap.models.top_metric_value_error_bounds.TopMetricValueErrorBoundsSchema", unknown=EXCLUDE, data_key="error", allow_none=True)
    r""" The error field of the top_metrics_svm_user_iops. """

    read = Size(data_key="read", allow_none=True)
    r""" Average number of read operations per second.

Example: 4 """

    write = Size(data_key="write", allow_none=True)
    r""" Average number of write operations per second.

Example: 8 """

    @property
    def resource(self):
        return TopMetricsSvmUserIops

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


class TopMetricsSvmUserIops(Resource):

    _schema = TopMetricsSvmUserIopsSchema
