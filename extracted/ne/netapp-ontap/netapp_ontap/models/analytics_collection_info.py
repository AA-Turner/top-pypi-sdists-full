r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AnalyticsCollectionInfo", "AnalyticsCollectionInfoSchema"]
__pdoc__ = {
    "AnalyticsCollectionInfoSchema.resource": False,
    "AnalyticsCollectionInfoSchema.opts": False,
    "AnalyticsCollectionInfo": False,
}


class AnalyticsCollectionInfoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AnalyticsCollectionInfo object"""

    by_accessed_time = marshmallow_fields.Nested("netapp_ontap.models.analytics_collection_info_by_accessed_time.AnalyticsCollectionInfoByAccessedTimeSchema", unknown=EXCLUDE, data_key="by_accessed_time", allow_none=True)
    r""" File system analytics information, broken down by date of last access. """

    by_modified_time = marshmallow_fields.Nested("netapp_ontap.models.analytics_collection_info_by_modified_time.AnalyticsCollectionInfoByModifiedTimeSchema", unknown=EXCLUDE, data_key="by_modified_time", allow_none=True)
    r""" File system analytics information, broken down by date of last modification. """

    @property
    def resource(self):
        return AnalyticsCollectionInfo

    gettable_fields = [
        "by_accessed_time",
        "by_modified_time",
    ]
    """by_accessed_time,by_modified_time,"""

    patchable_fields = [
        "by_accessed_time",
        "by_modified_time",
    ]
    """by_accessed_time,by_modified_time,"""

    postable_fields = [
        "by_accessed_time",
        "by_modified_time",
    ]
    """by_accessed_time,by_modified_time,"""


class AnalyticsCollectionInfo(Resource):

    _schema = AnalyticsCollectionInfoSchema
