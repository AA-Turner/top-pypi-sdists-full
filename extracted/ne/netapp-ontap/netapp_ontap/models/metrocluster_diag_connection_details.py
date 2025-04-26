r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MetroclusterDiagConnectionDetails", "MetroclusterDiagConnectionDetailsSchema"]
__pdoc__ = {
    "MetroclusterDiagConnectionDetailsSchema.resource": False,
    "MetroclusterDiagConnectionDetailsSchema.opts": False,
    "MetroclusterDiagConnectionDetails": False,
}


class MetroclusterDiagConnectionDetailsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterDiagConnectionDetails object"""

    cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", unknown=EXCLUDE, data_key="cluster", allow_none=True)
    r""" The cluster field of the metrocluster_diag_connection_details. """

    connections = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.metrocluster_diag_connection.MetroclusterDiagConnectionSchema", unknown=EXCLUDE, allow_none=True), data_key="connections", allow_none=True)
    r""" The connections field of the metrocluster_diag_connection_details. """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the metrocluster_diag_connection_details. """

    @property
    def resource(self):
        return MetroclusterDiagConnectionDetails

    gettable_fields = [
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "connections",
        "node.links",
        "node.name",
        "node.uuid",
    ]
    """cluster.links,cluster.name,cluster.uuid,connections,node.links,node.name,node.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class MetroclusterDiagConnectionDetails(Resource):

    _schema = MetroclusterDiagConnectionDetailsSchema
