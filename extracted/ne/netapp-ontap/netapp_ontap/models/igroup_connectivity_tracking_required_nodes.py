r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupConnectivityTrackingRequiredNodes", "IgroupConnectivityTrackingRequiredNodesSchema"]
__pdoc__ = {
    "IgroupConnectivityTrackingRequiredNodesSchema.resource": False,
    "IgroupConnectivityTrackingRequiredNodesSchema.opts": False,
    "IgroupConnectivityTrackingRequiredNodes": False,
}


class IgroupConnectivityTrackingRequiredNodesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupConnectivityTrackingRequiredNodes object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the igroup_connectivity_tracking_required_nodes. """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The name field of the igroup_connectivity_tracking_required_nodes.

Example: node1 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The uuid field of the igroup_connectivity_tracking_required_nodes.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IgroupConnectivityTrackingRequiredNodes

    gettable_fields = [
        "links",
        "name",
        "uuid",
    ]
    """links,name,uuid,"""

    patchable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

    postable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""


class IgroupConnectivityTrackingRequiredNodes(Resource):

    _schema = IgroupConnectivityTrackingRequiredNodesSchema
