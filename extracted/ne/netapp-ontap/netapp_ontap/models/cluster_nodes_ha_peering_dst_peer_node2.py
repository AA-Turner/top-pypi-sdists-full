r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ClusterNodesHaPeeringDstPeerNode2", "ClusterNodesHaPeeringDstPeerNode2Schema"]
__pdoc__ = {
    "ClusterNodesHaPeeringDstPeerNode2Schema.resource": False,
    "ClusterNodesHaPeeringDstPeerNode2Schema.opts": False,
    "ClusterNodesHaPeeringDstPeerNode2": False,
}

class ClusterNodesHaPeeringDstPeerNode2Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHaPeeringDstPeerNode2 object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The second failover destination peer node name.

Example: node-02 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The second failover destination peer node UUID.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ClusterNodesHaPeeringDstPeerNode2

    gettable_fields = [
        "name",
        "uuid",
    ]
    """name,uuid,"""

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


class ClusterNodesHaPeeringDstPeerNode2(Resource):

    _schema = ClusterNodesHaPeeringDstPeerNode2Schema
