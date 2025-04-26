r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FlexcacheCifsChangeNotify", "FlexcacheCifsChangeNotifySchema"]
__pdoc__ = {
    "FlexcacheCifsChangeNotifySchema.resource": False,
    "FlexcacheCifsChangeNotifySchema.opts": False,
    "FlexcacheCifsChangeNotify": False,
}


class FlexcacheCifsChangeNotifySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcacheCifsChangeNotify object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Specifies whether a CIFS change notification is enabled for the FlexCache volume. """

    @property
    def resource(self):
        return FlexcacheCifsChangeNotify

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


class FlexcacheCifsChangeNotify(Resource):

    _schema = FlexcacheCifsChangeNotifySchema
