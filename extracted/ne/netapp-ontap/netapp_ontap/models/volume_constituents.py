r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeConstituents", "VolumeConstituentsSchema"]
__pdoc__ = {
    "VolumeConstituentsSchema.resource": False,
    "VolumeConstituentsSchema.opts": False,
    "VolumeConstituents": False,
}


class VolumeConstituentsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeConstituents object"""

    aggregates = marshmallow_fields.Nested("netapp_ontap.models.volume_constituents_aggregates.VolumeConstituentsAggregatesSchema", unknown=EXCLUDE, data_key="aggregates", allow_none=True)
    r""" The aggregates field of the volume_constituents. """

    movement = marshmallow_fields.Nested("netapp_ontap.models.volume_constituents_movement.VolumeConstituentsMovementSchema", unknown=EXCLUDE, data_key="movement", allow_none=True)
    r""" Volume movement. All attributes are modify, that is, not writable through POST. Set PATCH state to destination_aggregate to initiate a volume move operation. Volume movement on FlexGroup volume constituents is not supported. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" FlexGroup volume constituent name. """

    space = marshmallow_fields.Nested("netapp_ontap.models.volume_constituents_space.VolumeConstituentsSpaceSchema", unknown=EXCLUDE, data_key="space", allow_none=True)
    r""" The space field of the volume_constituents. """

    @property
    def resource(self):
        return VolumeConstituents

    gettable_fields = [
        "aggregates",
        "movement",
        "name",
        "space",
    ]
    """aggregates,movement,name,space,"""

    patchable_fields = [
        "aggregates",
        "movement",
        "space",
    ]
    """aggregates,movement,space,"""

    postable_fields = [
        "aggregates",
        "movement",
        "space",
    ]
    """aggregates,movement,space,"""


class VolumeConstituents(Resource):

    _schema = VolumeConstituentsSchema
