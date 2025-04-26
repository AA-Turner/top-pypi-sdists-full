r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FlexcacheAtimeScrub", "FlexcacheAtimeScrubSchema"]
__pdoc__ = {
    "FlexcacheAtimeScrubSchema.resource": False,
    "FlexcacheAtimeScrubSchema.opts": False,
    "FlexcacheAtimeScrub": False,
}


class FlexcacheAtimeScrubSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheAtimeScrub object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether scrubbing of inactive files based on atime is enabled for the FlexCache volume. When scrubbing is enabled, files whose atime is older than the specified duration are evicted from the cache volume. The scrubber runs once a day and looks for files whose atime has exceeded the provisioned value. """

    period = Size(data_key="period", allow_none=True)
    r""" Specifies the atime duration in days after which a cached file is considered inactive. Inactive files are purged from the FlexCache volumes when the scrubber runs once a day. """

    @property
    def resource(self):
        return FlexcacheAtimeScrub

    gettable_fields = [
        "enabled",
        "period",
    ]
    """enabled,period,"""

    patchable_fields = [
        "enabled",
        "period",
    ]
    """enabled,period,"""

    postable_fields = [
        "enabled",
        "period",
    ]
    """enabled,period,"""


class FlexcacheAtimeScrub(Resource):

    _schema = FlexcacheAtimeScrubSchema
