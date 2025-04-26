r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeAnalytics", "VolumeAnalyticsSchema"]
__pdoc__ = {
    "VolumeAnalyticsSchema.resource": False,
    "VolumeAnalyticsSchema.opts": False,
    "VolumeAnalytics": False,
}


class VolumeAnalyticsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeAnalytics object"""

    files_scanned = Size(data_key="files_scanned", allow_none=True)
    r""" Number of files in the volume that the file system analytics initialization scan has processed. Only returned when the state is `initializing`.

Example: 43002 """

    initialization = marshmallow_fields.Nested("netapp_ontap.models.volume_analytics_initialization.VolumeAnalyticsInitializationSchema", unknown=EXCLUDE, data_key="initialization", allow_none=True)
    r""" The initialization field of the volume_analytics. """

    scan_progress = Size(data_key="scan_progress", allow_none=True)
    r""" Percentage of files in the volume that the file system analytics initialization scan has processed. Only returned when the state is `initializing`.

Example: 17 """

    scan_throttle_reason = marshmallow_fields.Nested("netapp_ontap.models.volume_analytics_scan_throttle_reason.VolumeAnalyticsScanThrottleReasonSchema", unknown=EXCLUDE, data_key="scan_throttle_reason", allow_none=True)
    r""" The scan_throttle_reason field of the volume_analytics. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" File system analytics state of the volume. If this value is "on", ONTAP collects extra file system analytics information for all directories on the volume. There will be a slight impact to I/O performance to collect this information. If this value is "off", file system analytics information is not collected and not available to be viewed. If this value is "initializing", that means file system analytics was recently turned on, and the initialization scan to gather information for all existing files and directories is currently running. If this value is "initialization_paused", this means that the initialization scan is currently paused. If this value is 'unknown', this means that there was an internal error when determining the file system analytics state for the volume.

Valid choices:

* unknown
* initializing
* initialization_paused
* off
* on """

    supported = marshmallow_fields.Boolean(data_key="supported", allow_none=True)
    r""" This field indicates whether or not file system analytics is supported on the volume. If file system analytics is not supported, the reason will be specified in the "analytics.unsupported_reason" field. """

    total_files = Size(data_key="total_files", allow_none=True)
    r""" Total number of files in the volume that the file system analytics initialization scan will process. Only returned when the state is `initializing`.

Example: 101890 """

    unsupported_reason = marshmallow_fields.Nested("netapp_ontap.models.volume_analytics_unsupported_reason.VolumeAnalyticsUnsupportedReasonSchema", unknown=EXCLUDE, data_key="unsupported_reason", allow_none=True)
    r""" The unsupported_reason field of the volume_analytics. """

    @property
    def resource(self):
        return VolumeAnalytics

    gettable_fields = [
        "files_scanned",
        "initialization",
        "scan_progress",
        "scan_throttle_reason",
        "state",
        "supported",
        "total_files",
        "unsupported_reason",
    ]
    """files_scanned,initialization,scan_progress,scan_throttle_reason,state,supported,total_files,unsupported_reason,"""

    patchable_fields = [
        "initialization",
        "scan_throttle_reason",
        "state",
        "unsupported_reason",
    ]
    """initialization,scan_throttle_reason,state,unsupported_reason,"""

    postable_fields = [
        "initialization",
        "scan_throttle_reason",
        "state",
        "unsupported_reason",
    ]
    """initialization,scan_throttle_reason,state,unsupported_reason,"""


class VolumeAnalytics(Resource):

    _schema = VolumeAnalyticsSchema
