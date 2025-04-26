r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MetroclusterPartner", "MetroclusterPartnerSchema"]
__pdoc__ = {
    "MetroclusterPartnerSchema.resource": False,
    "MetroclusterPartnerSchema.opts": False,
    "MetroclusterPartner": False,
}


class MetroclusterPartnerSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterPartner object"""

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the metrocluster_partner. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" The type field of the metrocluster_partner.

Valid choices:

* ha
* dr
* aux """

    @property
    def resource(self):
        return MetroclusterPartner

    gettable_fields = [
        "node.links",
        "node.name",
        "node.uuid",
        "type",
    ]
    """node.links,node.name,node.uuid,type,"""

    patchable_fields = [
        "node.name",
        "node.uuid",
        "type",
    ]
    """node.name,node.uuid,type,"""

    postable_fields = [
        "node.name",
        "node.uuid",
        "type",
    ]
    """node.name,node.uuid,type,"""


class MetroclusterPartner(Resource):

    _schema = MetroclusterPartnerSchema
