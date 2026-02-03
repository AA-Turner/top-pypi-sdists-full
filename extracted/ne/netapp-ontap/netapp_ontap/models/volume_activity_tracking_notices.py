r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["VolumeActivityTrackingNotices", "VolumeActivityTrackingNoticesSchema"]
__pdoc__ = {
    "VolumeActivityTrackingNoticesSchema.resource": False,
    "VolumeActivityTrackingNoticesSchema.opts": False,
    "VolumeActivityTrackingNotices": False,
}

class VolumeActivityTrackingNoticesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeActivityTrackingNotices object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" An error code related to activity tracking.

Example: 124518424 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" A notice message related to activity tracking.

Example: The top metrics report contains partial data for read operations because NFSv4 reads using Multi-Processor I/O (MPIO) are not tracked. """

    @property
    def resource(self):
        return VolumeActivityTrackingNotices

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


class VolumeActivityTrackingNotices(Resource):

    _schema = VolumeActivityTrackingNoticesSchema
