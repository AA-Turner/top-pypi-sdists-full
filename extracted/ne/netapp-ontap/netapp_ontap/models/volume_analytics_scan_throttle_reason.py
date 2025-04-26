r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeAnalyticsScanThrottleReason", "VolumeAnalyticsScanThrottleReasonSchema"]
__pdoc__ = {
    "VolumeAnalyticsScanThrottleReasonSchema.resource": False,
    "VolumeAnalyticsScanThrottleReasonSchema.opts": False,
    "VolumeAnalyticsScanThrottleReason": False,
}


class VolumeAnalyticsScanThrottleReasonSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeAnalyticsScanThrottleReason object"""

    arguments = marshmallow_fields.List(marshmallow_fields.Str, data_key="arguments", allow_none=True)
    r""" Arguments present in the warning message encountered. """

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Warning code indicating why scanner throttling is reported.

Example: 6739881 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" A message that provides details for scan throttling.

Example: The file system analytics scan running on volume "fsavol2" in SVM "vs2" has slowed down on node "my_node". Reason: Computing resources are being used by higher priority workloads. """

    @property
    def resource(self):
        return VolumeAnalyticsScanThrottleReason

    gettable_fields = [
        "arguments",
        "code",
        "message",
    ]
    """arguments,code,message,"""

    patchable_fields = [
        "arguments",
    ]
    """arguments,"""

    postable_fields = [
        "arguments",
    ]
    """arguments,"""


class VolumeAnalyticsScanThrottleReason(Resource):

    _schema = VolumeAnalyticsScanThrottleReasonSchema
