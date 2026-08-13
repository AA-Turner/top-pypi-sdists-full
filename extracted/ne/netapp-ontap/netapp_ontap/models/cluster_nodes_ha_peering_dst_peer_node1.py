r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ClusterNodesHaPeeringDstPeerNode1", "ClusterNodesHaPeeringDstPeerNode1Schema"]
__pdoc__ = {
    "ClusterNodesHaPeeringDstPeerNode1Schema.resource": False,
    "ClusterNodesHaPeeringDstPeerNode1Schema.opts": False,
    "ClusterNodesHaPeeringDstPeerNode1": False,
}

class ClusterNodesHaPeeringDstPeerNode1Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterNodesHaPeeringDstPeerNode1 object"""

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" The first failover destination peer node name.

Example: node-01 """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" The first failover destination peer node UUID.

Example: 4ea7a442-86d1-11e0-ae1c-123478563411 """

    @property
    def resource(self):
        return ClusterNodesHaPeeringDstPeerNode1

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


class ClusterNodesHaPeeringDstPeerNode1(Resource):

    _schema = ClusterNodesHaPeeringDstPeerNode1Schema
