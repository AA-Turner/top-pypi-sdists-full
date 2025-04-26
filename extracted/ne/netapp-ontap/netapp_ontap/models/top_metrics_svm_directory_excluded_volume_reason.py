r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["TopMetricsSvmDirectoryExcludedVolumeReason", "TopMetricsSvmDirectoryExcludedVolumeReasonSchema"]
__pdoc__ = {
    "TopMetricsSvmDirectoryExcludedVolumeReasonSchema.resource": False,
    "TopMetricsSvmDirectoryExcludedVolumeReasonSchema.opts": False,
    "TopMetricsSvmDirectoryExcludedVolumeReason": False,
}


class TopMetricsSvmDirectoryExcludedVolumeReasonSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the TopMetricsSvmDirectoryExcludedVolumeReason object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Warning code indicating why the volume is not included in the SVM activity tracking REST API.

Example: 111411 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Details why the volume is not included in the SVM activity tracking REST API.

Example: The volume is offline. """

    @property
    def resource(self):
        return TopMetricsSvmDirectoryExcludedVolumeReason

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class TopMetricsSvmDirectoryExcludedVolumeReason(Resource):

    _schema = TopMetricsSvmDirectoryExcludedVolumeReasonSchema
