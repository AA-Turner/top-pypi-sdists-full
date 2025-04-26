r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupVolumeSnapshot", "ConsistencyGroupVolumeSnapshotSchema"]
__pdoc__ = {
    "ConsistencyGroupVolumeSnapshotSchema.resource": False,
    "ConsistencyGroupVolumeSnapshotSchema.opts": False,
    "ConsistencyGroupVolumeSnapshot": False,
}


class ConsistencyGroupVolumeSnapshotSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupVolumeSnapshot object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the consistency_group_volume_snapshot. """

    snapshot = marshmallow_fields.Nested("netapp_ontap.resources.snapshot.SnapshotSchema", unknown=EXCLUDE, data_key="snapshot", allow_none=True)
    r""" The snapshot field of the consistency_group_volume_snapshot. """

    volume = marshmallow_fields.Nested("netapp_ontap.resources.volume.VolumeSchema", unknown=EXCLUDE, data_key="volume", allow_none=True)
    r""" The volume field of the consistency_group_volume_snapshot. """

    @property
    def resource(self):
        return ConsistencyGroupVolumeSnapshot

    gettable_fields = [
        "links",
        "snapshot.links",
        "snapshot.name",
        "snapshot.uuid",
        "volume.links",
        "volume.name",
        "volume.uuid",
    ]
    """links,snapshot.links,snapshot.name,snapshot.uuid,volume.links,volume.name,volume.uuid,"""

    patchable_fields = [
        "snapshot.name",
        "snapshot.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """snapshot.name,snapshot.uuid,volume.name,volume.uuid,"""

    postable_fields = [
        "snapshot.name",
        "snapshot.uuid",
        "volume.name",
        "volume.uuid",
    ]
    """snapshot.name,snapshot.uuid,volume.name,volume.uuid,"""


class ConsistencyGroupVolumeSnapshot(Resource):

    _schema = ConsistencyGroupVolumeSnapshotSchema
