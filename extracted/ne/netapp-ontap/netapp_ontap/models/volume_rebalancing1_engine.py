r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["VolumeRebalancing1Engine", "VolumeRebalancing1EngineSchema"]
__pdoc__ = {
    "VolumeRebalancing1EngineSchema.resource": False,
    "VolumeRebalancing1EngineSchema.opts": False,
    "VolumeRebalancing1Engine": False,
}

class VolumeRebalancing1EngineSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeRebalancing1Engine object"""

    movement = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.volume_rebalancing1_engine_movement", "VolumeRebalancing1EngineMovementSchema"),
                unknown=EXCLUDE,
                data_key="movement",
                allow_none=True
            )
    r""" The movement field of the volume_rebalancing1_engine. """

    scanner = marshmallow_fields.Nested(
                lambda: lazy_import_schema("netapp_ontap.models.volume_rebalancing1_engine_scanner", "VolumeRebalancing1EngineScannerSchema"),
                unknown=EXCLUDE,
                data_key="scanner",
                allow_none=True
            )
    r""" The scanner field of the volume_rebalancing1_engine. """

    @property
    def resource(self):
        return VolumeRebalancing1Engine

    gettable_fields = [
        "movement",
        "scanner",
    ]
    """movement,scanner,"""

    patchable_fields = [
        "movement",
        "scanner",
    ]
    """movement,scanner,"""

    postable_fields = [
        "movement",
        "scanner",
    ]
    """movement,scanner,"""


class VolumeRebalancing1Engine(Resource):

    _schema = VolumeRebalancing1EngineSchema
