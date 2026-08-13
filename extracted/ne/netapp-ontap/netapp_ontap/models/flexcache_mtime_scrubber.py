r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["FlexcacheMtimeScrubber", "FlexcacheMtimeScrubberSchema"]
__pdoc__ = {
    "FlexcacheMtimeScrubberSchema.resource": False,
    "FlexcacheMtimeScrubberSchema.opts": False,
    "FlexcacheMtimeScrubber": False,
}

class FlexcacheMtimeScrubberSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheMtimeScrubber object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether mtime-based scrubber is enabled on the FlexCache volume. The mtime scrubber automatically scrubs files from the cache based on their modification time. """

    threshold = Size(data_key="threshold", allow_none=True)
    r""" Specifies the mtime threshold in seconds. Files that have not been modified within this threshold duration are eligible for scrubbing from the FlexCache volume. Valid range is 900 to 86400 seconds (15 minutes to 24 hours). """

    @property
    def resource(self):
        return FlexcacheMtimeScrubber

    gettable_fields = [
        "enabled",
        "threshold",
    ]
    """enabled,threshold,"""

    patchable_fields = [
        "enabled",
        "threshold",
    ]
    """enabled,threshold,"""

    postable_fields = [
        "enabled",
        "threshold",
    ]
    """enabled,threshold,"""


class FlexcacheMtimeScrubber(Resource):

    _schema = FlexcacheMtimeScrubberSchema
