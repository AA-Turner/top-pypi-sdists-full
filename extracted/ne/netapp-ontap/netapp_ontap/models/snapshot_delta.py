r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapshotDelta", "SnapshotDeltaSchema"]
__pdoc__ = {
    "SnapshotDeltaSchema.resource": False,
    "SnapshotDeltaSchema.opts": False,
    "SnapshotDelta": False,
}


class SnapshotDeltaSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapshotDelta object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the snapshot_delta. """

    size_consumed = Size(data_key="size_consumed", allow_none=True)
    r""" Indicates the space that has changed between two specified WAFL file systems, in bytes. """

    time_elapsed = marshmallow_fields.Str(data_key="time_elapsed", allow_none=True)
    r""" Time elapsed between two specified WAFL file systems. """

    @property
    def resource(self):
        return SnapshotDelta

    gettable_fields = [
        "links",
        "size_consumed",
        "time_elapsed",
    ]
    """links,size_consumed,time_elapsed,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class SnapshotDelta(Resource):

    _schema = SnapshotDeltaSchema
