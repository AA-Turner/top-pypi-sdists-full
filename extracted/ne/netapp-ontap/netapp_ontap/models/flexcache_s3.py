r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["FlexcacheS3", "FlexcacheS3Schema"]
__pdoc__ = {
    "FlexcacheS3Schema.resource": False,
    "FlexcacheS3Schema.opts": False,
    "FlexcacheS3": False,
}

class FlexcacheS3Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheS3 object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Indicates whether S3 access is enabled on the Flexcache volume. """

    @property
    def resource(self):
        return FlexcacheS3

    gettable_fields = [
        "enabled",
    ]
    """enabled,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""


class FlexcacheS3(Resource):

    _schema = FlexcacheS3Schema
