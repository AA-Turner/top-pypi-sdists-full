r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["MetroclusterDiagDetails", "MetroclusterDiagDetailsSchema"]
__pdoc__ = {
    "MetroclusterDiagDetailsSchema.resource": False,
    "MetroclusterDiagDetailsSchema.opts": False,
    "MetroclusterDiagDetails": False,
}


class MetroclusterDiagDetailsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the MetroclusterDiagDetails object"""

    aggregate = marshmallow_fields.Nested("netapp_ontap.resources.aggregate.AggregateSchema", unknown=EXCLUDE, data_key="aggregate", allow_none=True)
    r""" The aggregate field of the metrocluster_diag_details. """

    checks = marshmallow_fields.List(marshmallow_fields.Nested("netapp_ontap.models.metrocluster_diag_check.MetroclusterDiagCheckSchema", unknown=EXCLUDE, allow_none=True), data_key="checks", allow_none=True)
    r""" Collection of MetroCluster checks done for component. """

    cluster = marshmallow_fields.Nested("netapp_ontap.resources.cluster.ClusterSchema", unknown=EXCLUDE, data_key="cluster", allow_none=True)
    r""" The cluster field of the metrocluster_diag_details. """

    node = marshmallow_fields.Nested("netapp_ontap.resources.node.NodeSchema", unknown=EXCLUDE, data_key="node", allow_none=True)
    r""" The node field of the metrocluster_diag_details. """

    timestamp = ImpreciseDateTime(data_key="timestamp", allow_none=True)
    r""" Time check was done.

Example: 2016-03-10T22:35:16.000+0000 """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the metrocluster_diag_details. """

    @property
    def resource(self):
        return MetroclusterDiagDetails

    gettable_fields = [
        "aggregate.links",
        "aggregate.name",
        "aggregate.uuid",
        "checks",
        "cluster.links",
        "cluster.name",
        "cluster.uuid",
        "node.links",
        "node.name",
        "node.uuid",
        "timestamp",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """aggregate.links,aggregate.name,aggregate.uuid,checks,cluster.links,cluster.name,cluster.uuid,node.links,node.name,node.uuid,timestamp,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class MetroclusterDiagDetails(Resource):

    _schema = MetroclusterDiagDetailsSchema
