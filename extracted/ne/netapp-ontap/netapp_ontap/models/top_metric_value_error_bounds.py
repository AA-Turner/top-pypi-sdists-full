r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricValueErrorBounds", "TopMetricValueErrorBoundsSchema"]
__pdoc__ = {
    "TopMetricValueErrorBoundsSchema.resource": False,
    "TopMetricValueErrorBoundsSchema.opts": False,
    "TopMetricValueErrorBounds": False,
}


class TopMetricValueErrorBoundsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricValueErrorBounds object"""

    lower_bound = Size(data_key="lower_bound", allow_none=True)
    r""" Lower bound of the nominal value of a metric.

Example: 34 """

    upper_bound = Size(data_key="upper_bound", allow_none=True)
    r""" Upper bound of the nominal value of a metric.

Example: 54 """

    @property
    def resource(self):
        return TopMetricValueErrorBounds

    gettable_fields = [
        "lower_bound",
        "upper_bound",
    ]
    """lower_bound,upper_bound,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class TopMetricValueErrorBounds(Resource):

    _schema = TopMetricValueErrorBoundsSchema
