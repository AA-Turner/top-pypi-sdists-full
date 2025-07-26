r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeNodes", "VolumeNodesSchema"]
__pdoc__ = {
    "VolumeNodesSchema.resource": False,
    "VolumeNodesSchema.opts": False,
    "VolumeNodes": False,
}


class VolumeNodesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeNodes object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" List of the node names hosting the volume. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" List of the node UUIDs hosting the volume. """

    @property
    def resource(self):
        return VolumeNodes

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class VolumeNodes(Resource):

    _schema = VolumeNodesSchema
