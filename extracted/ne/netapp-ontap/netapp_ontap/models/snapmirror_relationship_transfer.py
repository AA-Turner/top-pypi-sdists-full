r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SnapmirrorRelationshipTransfer", "SnapmirrorRelationshipTransferSchema"]
__pdoc__ = {
    "SnapmirrorRelationshipTransferSchema.resource": False,
    "SnapmirrorRelationshipTransferSchema.opts": False,
    "SnapmirrorRelationshipTransfer": False,
}


class SnapmirrorRelationshipTransferSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SnapmirrorRelationshipTransfer object"""

    links = marshmallow_fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links", allow_none=True)
    r""" The links field of the snapmirror_relationship_transfer. """

    bytes_transferred = Size(data_key="bytes_transferred", allow_none=True)
    r""" Total bytes transferred in the current or last successful transfer. """

    end_time = ImpreciseDateTime(data_key="end_time", allow_none=True)
    r""" End time of the last transfer.

Example: 2020-12-03T02:36:19.000+0000 """

    last_updated_time = ImpreciseDateTime(data_key="last_updated_time", allow_none=True)
    r""" Last updated time of the bytes transferred in the current transfer.

Example: 2023-09-14T22:39:19.000+0000 """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" The state field of the snapmirror_relationship_transfer.

Valid choices:

* aborted
* failed
* hard_aborted
* queued
* success
* transferring """

    total_duration = marshmallow_fields.Str(data_key="total_duration", allow_none=True)
    r""" Elapsed time to transfer all snapshots for the last successful transfer.

Example: PT28M41S """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Specifies the operation type of the current transfer on the relationship. The _initialize_ transfer occurs when the relationship state changes from "uninitialized" to "snapmirrored" or "in_sync". The _update_ transfer occurs when snapshots are being transferred from the source endpoint to the destination endpoint as part of a scheduled or manual update. The _resync_ transfer occurs when the relationship state changes from "broken_off" to "snapmirrored" or "in_sync". The _restore_ transfer occurs when a snapshot is being restored from a destination endpoint to another endpoint.

Valid choices:

* initialize
* update
* resync
* restore """

    uuid = marshmallow_fields.Str(data_key="uuid", allow_none=True)
    r""" Transfer UUID. This property is applicable only for active transfers.

Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return SnapmirrorRelationshipTransfer

    gettable_fields = [
        "links",
        "bytes_transferred",
        "end_time",
        "last_updated_time",
        "state",
        "total_duration",
        "type",
        "uuid",
    ]
    """links,bytes_transferred,end_time,last_updated_time,state,total_duration,type,uuid,"""

    patchable_fields = [
        "bytes_transferred",
        "end_time",
        "last_updated_time",
        "state",
        "total_duration",
        "type",
        "uuid",
    ]
    """bytes_transferred,end_time,last_updated_time,state,total_duration,type,uuid,"""

    postable_fields = [
        "bytes_transferred",
        "end_time",
        "last_updated_time",
        "state",
        "total_duration",
        "type",
        "uuid",
    ]
    """bytes_transferred,end_time,last_updated_time,state,total_duration,type,uuid,"""


class SnapmirrorRelationshipTransfer(Resource):

    _schema = SnapmirrorRelationshipTransferSchema
