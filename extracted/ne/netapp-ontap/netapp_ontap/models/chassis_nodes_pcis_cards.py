r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ChassisNodesPcisCards", "ChassisNodesPcisCardsSchema"]
__pdoc__ = {
    "ChassisNodesPcisCardsSchema.resource": False,
    "ChassisNodesPcisCardsSchema.opts": False,
    "ChassisNodesPcisCards": False,
}


class ChassisNodesPcisCardsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ChassisNodesPcisCards object"""

    device = marshmallow_fields.Str(data_key="device", allow_none=True)
    r""" The description of the PCI card.

Example: Intel Lewisburg series chipset SATA Controller """

    info = marshmallow_fields.Str(data_key="info", allow_none=True)
    r""" The info string from the device driver of the PCI card.

Example: Additional Info: 0 (0xaaf00000)   SHM2S86Q120GLM22NP FW1146 114473MB 512B/sect (SPG190108GW) """

    slot = marshmallow_fields.Str(data_key="slot", allow_none=True)
    r""" The slot where the PCI card is placed. This can sometimes take the form of "6-1" to indicate slot and subslot.

Example: 0 """

    @property
    def resource(self):
        return ChassisNodesPcisCards

    gettable_fields = [
        "device",
        "info",
        "slot",
    ]
    """device,info,slot,"""

    patchable_fields = [
        "device",
        "info",
        "slot",
    ]
    """device,info,slot,"""

    postable_fields = [
        "device",
        "info",
        "slot",
    ]
    """device,info,slot,"""


class ChassisNodesPcisCards(Resource):

    _schema = ChassisNodesPcisCardsSchema
