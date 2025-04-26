r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["LunMapReportingNodesLinks", "LunMapReportingNodesLinksSchema"]
__pdoc__ = {
    "LunMapReportingNodesLinksSchema.resource": False,
    "LunMapReportingNodesLinksSchema.opts": False,
    "LunMapReportingNodesLinks": False,
}


class LunMapReportingNodesLinksSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the LunMapReportingNodesLinks object"""

    node = marshmallow_fields.Nested("netapp_ontap.models.href.HrefSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the lun_map_reporting_nodes_links. """

    self_ = marshmallow_fields.Nested("netapp_ontap.models.href.HrefSchema", unknown=EXCLUDE, data_key="self", allow_none=True)
    r""" The self_ field of the lun_map_reporting_nodes_links. """

    @property
    def resource(self):
        return LunMapReportingNodesLinks

    gettable_fields = [
        "node",
        "self_",
    ]
    """node,self_,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class LunMapReportingNodesLinks(Resource):

    _schema = LunMapReportingNodesLinksSchema
