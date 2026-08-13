r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["FlexcacheWrite", "FlexcacheWriteSchema"]
__pdoc__ = {
    "FlexcacheWriteSchema.resource": False,
    "FlexcacheWriteSchema.opts": False,
    "FlexcacheWrite": False,
}

class FlexcacheWriteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheWrite object"""

    absorption_enabled = marshmallow_fields.Boolean(data_key="absorption_enabled", allow_none=True)
    r""" Indicates whether Write Absorption is enabled on the FlexCache volume. Write Absorption enables the FlexCache volume to absorb writes locally and synchronize them with the origin volume. """

    @property
    def resource(self):
        return FlexcacheWrite

    gettable_fields = [
        "absorption_enabled",
    ]
    """absorption_enabled,"""

    patchable_fields = [
        "absorption_enabled",
    ]
    """absorption_enabled,"""

    postable_fields = [
        "absorption_enabled",
    ]
    """absorption_enabled,"""


class FlexcacheWrite(Resource):

    _schema = FlexcacheWriteSchema
