r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AnalyticsHistogramByTime", "AnalyticsHistogramByTimeSchema"]
__pdoc__ = {
    "AnalyticsHistogramByTimeSchema.resource": False,
    "AnalyticsHistogramByTimeSchema.opts": False,
    "AnalyticsHistogramByTime": False,
}


class AnalyticsHistogramByTimeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AnalyticsHistogramByTime object"""

    labels = marshmallow_fields.List(marshmallow_fields.Str, data_key="labels", allow_none=True)
    r""" The labels field of the analytics_histogram_by_time. """

    newest_label = marshmallow_fields.Str(data_key="newest_label", allow_none=True)
    r""" The newest time label with a non-zero histogram value. """

    oldest_label = marshmallow_fields.Str(data_key="oldest_label", allow_none=True)
    r""" The oldest time label with a non-zero histogram value. """

    percentages = marshmallow_fields.List(marshmallow_fields.Number, data_key="percentages", allow_none=True)
    r""" Percentages for this histogram

Example: [0.1,11.24,0.18,15.75,0.75,83.5,0] """

    values = marshmallow_fields.List(Size, data_key="values", allow_none=True)
    r""" Values for this histogram

Example: [15925248,1735569408,27672576,2430595072,116105216,12889948160,0] """

    @property
    def resource(self):
        return AnalyticsHistogramByTime

    gettable_fields = [
        "labels",
        "newest_label",
        "oldest_label",
        "percentages",
        "values",
    ]
    """labels,newest_label,oldest_label,percentages,values,"""

    patchable_fields = [
        "labels",
        "newest_label",
        "oldest_label",
        "percentages",
        "values",
    ]
    """labels,newest_label,oldest_label,percentages,values,"""

    postable_fields = [
        "labels",
        "newest_label",
        "oldest_label",
        "percentages",
        "values",
    ]
    """labels,newest_label,oldest_label,percentages,values,"""


class AnalyticsHistogramByTime(Resource):

    _schema = AnalyticsHistogramByTimeSchema
