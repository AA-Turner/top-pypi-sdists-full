r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["FlexcacheCifs", "FlexcacheCifsSchema"]
__pdoc__ = {
    "FlexcacheCifsSchema.resource": False,
    "FlexcacheCifsSchema.opts": False,
    "FlexcacheCifs": False,
}

class FlexcacheCifsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheCifs object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether CIFS access is enabled on the FlexCache volume. """

    @property
    def resource(self):
        return FlexcacheCifs

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


class FlexcacheCifs(Resource):

    _schema = FlexcacheCifsSchema
