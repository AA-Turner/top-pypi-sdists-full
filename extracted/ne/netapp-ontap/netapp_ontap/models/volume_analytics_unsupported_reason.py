r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeAnalyticsUnsupportedReason", "VolumeAnalyticsUnsupportedReasonSchema"]
__pdoc__ = {
    "VolumeAnalyticsUnsupportedReasonSchema.resource": False,
    "VolumeAnalyticsUnsupportedReasonSchema.opts": False,
    "VolumeAnalyticsUnsupportedReason": False,
}


class VolumeAnalyticsUnsupportedReasonSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeAnalyticsUnsupportedReason object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" If file system analytics is not supported on the volume, this field provides the error code explaining why.

Example: 111411207 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" If file system analytics is not supported on the volume, this field provides the error message explaining why.

Example: File system analytics cannot be enabled on volumes that contain LUNs. """

    @property
    def resource(self):
        return VolumeAnalyticsUnsupportedReason

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


class VolumeAnalyticsUnsupportedReason(Resource):

    _schema = VolumeAnalyticsUnsupportedReasonSchema
