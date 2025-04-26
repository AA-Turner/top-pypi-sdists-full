r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AnalyticsCollectionInfoByAccessedTimeBytesUsed", "AnalyticsCollectionInfoByAccessedTimeBytesUsedSchema"]
__pdoc__ = {
    "AnalyticsCollectionInfoByAccessedTimeBytesUsedSchema.resource": False,
    "AnalyticsCollectionInfoByAccessedTimeBytesUsedSchema.opts": False,
    "AnalyticsCollectionInfoByAccessedTimeBytesUsed": False,
}


class AnalyticsCollectionInfoByAccessedTimeBytesUsedSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AnalyticsCollectionInfoByAccessedTimeBytesUsed object"""

    labels = marshmallow_fields.List(marshmallow_fields.Str, data_key="labels", allow_none=True)
    r""" The labels field of the analytics_collection_info_by_accessed_time_bytes_used. """

    @property
    def resource(self):
        return AnalyticsCollectionInfoByAccessedTimeBytesUsed

    gettable_fields = [
        "labels",
    ]
    """labels,"""

    patchable_fields = [
        "labels",
    ]
    """labels,"""

    postable_fields = [
        "labels",
    ]
    """labels,"""


class AnalyticsCollectionInfoByAccessedTimeBytesUsed(Resource):

    _schema = AnalyticsCollectionInfoByAccessedTimeBytesUsedSchema
