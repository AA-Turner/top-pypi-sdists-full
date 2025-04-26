r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeActivityTracking", "VolumeActivityTrackingSchema"]
__pdoc__ = {
    "VolumeActivityTrackingSchema.resource": False,
    "VolumeActivityTrackingSchema.opts": False,
    "VolumeActivityTracking": False,
}


class VolumeActivityTrackingSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeActivityTracking object"""

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Activity tracking state of the volume. If this value is "on", ONTAP collects top metrics information for the volume in real time. There is a slight impact to I/O performance in order to collect this information. If this value is "off", no activity tracking information is collected or available to view.

Valid choices:

* off
* on """

    supported = marshmallow_fields.Boolean(data_key="supported", allow_none=True)
    r""" This field indicates whether or not volume activity tracking is supported on the volume. If volume activity tracking is not supported, the reason why is provided in the "activity_tracking.unsupported_reason" field. """

    unsupported_reason = marshmallow_fields.Nested("netapp_ontap.models.volume_activity_tracking_unsupported_reason.VolumeActivityTrackingUnsupportedReasonSchema", unknown=EXCLUDE, data_key="unsupported_reason", allow_none=True)
    r""" The unsupported_reason field of the volume_activity_tracking. """

    @property
    def resource(self):
        return VolumeActivityTracking

    gettable_fields = [
        "state",
        "supported",
        "unsupported_reason",
    ]
    """state,supported,unsupported_reason,"""

    patchable_fields = [
        "state",
        "unsupported_reason",
    ]
    """state,unsupported_reason,"""

    postable_fields = [
        "state",
        "unsupported_reason",
    ]
    """state,unsupported_reason,"""


class VolumeActivityTracking(Resource):

    _schema = VolumeActivityTrackingSchema
