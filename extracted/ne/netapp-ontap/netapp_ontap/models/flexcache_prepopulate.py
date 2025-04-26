r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FlexcachePrepopulate", "FlexcachePrepopulateSchema"]
__pdoc__ = {
    "FlexcachePrepopulateSchema.resource": False,
    "FlexcachePrepopulateSchema.opts": False,
    "FlexcachePrepopulate": False,
}


class FlexcachePrepopulateSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FlexcachePrepopulate object"""

    dir_paths = marshmallow_fields.List(marshmallow_fields.Str, data_key="dir_paths", allow_none=True)
    r""" The dir_paths field of the flexcache_prepopulate. """

    exclude_dir_paths = marshmallow_fields.List(marshmallow_fields.Str, data_key="exclude_dir_paths", allow_none=True)
    r""" The exclude_dir_paths field of the flexcache_prepopulate. """

    recurse = marshmallow_fields.Boolean(data_key="recurse", allow_none=True)
    r""" Specifies whether or not the prepopulate action should search through the `dir_paths` recursively. If not set, the default value _true_ is used. """

    @property
    def resource(self):
        return FlexcachePrepopulate

    gettable_fields = [
    ]
    """"""

    patchable_fields = [
        "dir_paths",
        "exclude_dir_paths",
        "recurse",
    ]
    """dir_paths,exclude_dir_paths,recurse,"""

    postable_fields = [
        "dir_paths",
        "exclude_dir_paths",
        "recurse",
    ]
    """dir_paths,exclude_dir_paths,recurse,"""


class FlexcachePrepopulate(Resource):

    _schema = FlexcachePrepopulateSchema
