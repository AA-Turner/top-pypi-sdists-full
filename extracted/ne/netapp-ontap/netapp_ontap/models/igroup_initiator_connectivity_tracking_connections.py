r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IgroupInitiatorConnectivityTrackingConnections", "IgroupInitiatorConnectivityTrackingConnectionsSchema"]
__pdoc__ = {
    "IgroupInitiatorConnectivityTrackingConnectionsSchema.resource": False,
    "IgroupInitiatorConnectivityTrackingConnectionsSchema.opts": False,
    "IgroupInitiatorConnectivityTrackingConnections": False,
}


class IgroupInitiatorConnectivityTrackingConnectionsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IgroupInitiatorConnectivityTrackingConnections object"""

    logins = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.igroup_initiator_connectivity_tracking_connections_logins.IgroupInitiatorConnectivityTrackingConnectionsLoginsSchema", unknown=EXCLUDE, allow_none=True), data_key="logins", allow_none=True)
    r""" The logins field of the igroup_initiator_connectivity_tracking_connections. """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the igroup_initiator_connectivity_tracking_connections. """

    @property
    def resource(self):
        return IgroupInitiatorConnectivityTrackingConnections

    gettable_fields = [
        "logins",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """logins,node.links,node.name,node.uuid,"""

    patchable_fields = [
        "logins",
        "node.name",
        "node.uuid",
    ]
    """logins,node.name,node.uuid,"""

    postable_fields = [
        "logins",
        "node.name",
        "node.uuid",
    ]
    """logins,node.name,node.uuid,"""


class IgroupInitiatorConnectivityTrackingConnections(Resource):

    _schema = IgroupInitiatorConnectivityTrackingConnectionsSchema
