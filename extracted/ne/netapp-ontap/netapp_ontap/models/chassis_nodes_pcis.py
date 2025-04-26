r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ChassisNodesPcis", "ChassisNodesPcisSchema"]
__pdoc__ = {
    "ChassisNodesPcisSchema.resource": False,
    "ChassisNodesPcisSchema.opts": False,
    "ChassisNodesPcis": False,
}


class ChassisNodesPcisSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ChassisNodesPcis object"""

    cards = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.chassis_nodes_pcis_cards.ChassisNodesPcisCardsSchema", unknown=EXCLUDE, allow_none=True), data_key="cards", allow_none=True)
    r""" The cards field of the chassis_nodes_pcis. """

    @property
    def resource(self):
        return ChassisNodesPcis

    gettable_fields = [
        "cards",
    ]
    """cards,"""

    patchable_fields = [
        "cards",
    ]
    """cards,"""

    postable_fields = [
        "cards",
    ]
    """cards,"""


class ChassisNodesPcis(Resource):

    _schema = ChassisNodesPcisSchema
