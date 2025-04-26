r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AnalyticsInfoByAccessedTime", "AnalyticsInfoByAccessedTimeSchema"]
__pdoc__ = {
    "AnalyticsInfoByAccessedTimeSchema.resource": False,
    "AnalyticsInfoByAccessedTimeSchema.opts": False,
    "AnalyticsInfoByAccessedTime": False,
}


class AnalyticsInfoByAccessedTimeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AnalyticsInfoByAccessedTime object"""

    bytes_used = marshmallow_fields.Nested("netapp_ontap.models.analytics_histogram_by_time.AnalyticsHistogramByTimeSchema", unknown=EXCLUDE, data_key="bytes_used", allow_none=True)
    r""" Histogram maintained by file system analytics that associates data with specific periods of time. <br/>
The properties of this object are three parallel lists as described here. For any index *i*, the *i*th element of each list corresponds to the same logical bucket within the histogram. """

    @property
    def resource(self):
        return AnalyticsInfoByAccessedTime

    gettable_fields = [
        "bytes_used",
    ]
    """bytes_used,"""

    patchable_fields = [
        "bytes_used",
    ]
    """bytes_used,"""

    postable_fields = [
        "bytes_used",
    ]
    """bytes_used,"""


class AnalyticsInfoByAccessedTime(Resource):

    _schema = AnalyticsInfoByAccessedTimeSchema
