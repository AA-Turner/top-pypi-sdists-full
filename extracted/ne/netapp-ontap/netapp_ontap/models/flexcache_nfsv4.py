r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["FlexcacheNfsv4", "FlexcacheNfsv4Schema"]
__pdoc__ = {
    "FlexcacheNfsv4Schema.resource": False,
    "FlexcacheNfsv4Schema.opts": False,
    "FlexcacheNfsv4": False,
}

class FlexcacheNfsv4Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheNfsv4 object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether NFSv4 access is enabled on the FlexCache volume. """

    @property
    def resource(self):
        return FlexcacheNfsv4

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


class FlexcacheNfsv4(Resource):

    _schema = FlexcacheNfsv4Schema
