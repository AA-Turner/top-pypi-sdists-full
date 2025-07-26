r"""
Copyright &copy; 2025 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeConstituentsNode", "VolumeConstituentsNodeSchema"]
__pdoc__ = {
    "VolumeConstituentsNodeSchema.resource": False,
    "VolumeConstituentsNodeSchema.opts": False,
    "VolumeConstituentsNode": False,
}


class VolumeConstituentsNodeSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeConstituentsNode object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" List of the node names hosting the FlexGroup volume constituent. """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" List of the node UUIDs hosting the FlexGroup volume constituent. """

    @property
    def resource(self):
        return VolumeConstituentsNode

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


class VolumeConstituentsNode(Resource):

    _schema = VolumeConstituentsNodeSchema
