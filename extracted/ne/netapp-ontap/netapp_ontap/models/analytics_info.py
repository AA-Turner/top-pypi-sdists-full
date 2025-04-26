r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AnalyticsInfo", "AnalyticsInfoSchema"]
__pdoc__ = {
    "AnalyticsInfoSchema.resource": False,
    "AnalyticsInfoSchema.opts": False,
    "AnalyticsInfo": False,
}


class AnalyticsInfoSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AnalyticsInfo object"""

    by_accessed_time = marshmallow_fields.Nested("netapp_ontap.models.analytics_info_by_accessed_time.AnalyticsInfoByAccessedTimeSchema", unknown=EXCLUDE, data_key="by_accessed_time", allow_none=True)
    r""" File system analytics information, broken down by date of last access. """

    by_modified_time = marshmallow_fields.Nested("netapp_ontap.models.analytics_info_by_modified_time.AnalyticsInfoByModifiedTimeSchema", unknown=EXCLUDE, data_key="by_modified_time", allow_none=True)
    r""" File system analytics information, broken down by date of last modification. """

    bytes_used = Size(data_key="bytes_used", allow_none=True)
    r""" Number of bytes used on-disk

Example: 15436648448 """

    file_count = Size(data_key="file_count", allow_none=True)
    r""" Number of descendants

Example: 21134 """

    incomplete_data = marshmallow_fields.Boolean(data_key="incomplete_data", allow_none=True)
    r""" Returns true if data collection is incomplete for this directory tree. """

    subdir_count = Size(data_key="subdir_count", allow_none=True)
    r""" Number of sub directories

Example: 35 """

    @property
    def resource(self):
        return AnalyticsInfo

    gettable_fields = [
        "by_accessed_time",
        "by_modified_time",
        "bytes_used",
        "file_count",
        "incomplete_data",
        "subdir_count",
    ]
    """by_accessed_time,by_modified_time,bytes_used,file_count,incomplete_data,subdir_count,"""

    patchable_fields = [
        "by_accessed_time",
        "by_modified_time",
        "bytes_used",
        "file_count",
        "incomplete_data",
        "subdir_count",
    ]
    """by_accessed_time,by_modified_time,bytes_used,file_count,incomplete_data,subdir_count,"""

    postable_fields = [
        "by_accessed_time",
        "by_modified_time",
        "bytes_used",
        "file_count",
        "incomplete_data",
        "subdir_count",
    ]
    """by_accessed_time,by_modified_time,bytes_used,file_count,incomplete_data,subdir_count,"""


class AnalyticsInfo(Resource):

    _schema = AnalyticsInfoSchema
