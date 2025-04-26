r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PlexResync", "PlexResyncSchema"]
__pdoc__ = {
    "PlexResyncSchema.resource": False,
    "PlexResyncSchema.opts": False,
    "PlexResync": False,
}


class PlexResyncSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PlexResync object"""

    active = marshmallow_fields.Boolean(data_key="active", allow_none=True)
    r""" Plex is being resynchronized to its mirrored plex """

    level = marshmallow_fields.Str(data_key="level", allow_none=True)
    r""" Plex resyncing level

Valid choices:

* full
* incremental """

    percent = Size(data_key="percent", allow_none=True)
    r""" Plex resyncing percentage

Example: 10 """

    @property
    def resource(self):
        return PlexResync

    gettable_fields = [
        "active",
        "level",
        "percent",
    ]
    """active,level,percent,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class PlexResync(Resource):

    _schema = PlexResyncSchema
