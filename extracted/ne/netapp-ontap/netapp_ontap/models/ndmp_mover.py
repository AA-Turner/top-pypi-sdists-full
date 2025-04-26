r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NdmpMover", "NdmpMoverSchema"]
__pdoc__ = {
    "NdmpMoverSchema.resource": False,
    "NdmpMoverSchema.opts": False,
    "NdmpMover": False,
}


class NdmpMoverSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NdmpMover object"""

    bytes_moved = Size(data_key="bytes_moved", allow_none=True)
    r""" Indicates the NDMP mover bytes moved.

Example: 645120 """

    connection = marshmallow_fields.Nested("netapp_ontap.models.ndmp_connect.NdmpConnectSchema", unknown=EXCLUDE, data_key="connection", allow_none=True)
    r""" Indicates the NDMP connection attributes. """

    mode = marshmallow_fields.Str(data_key="mode", allow_none=True)
    r""" Indicates the NDMP mover mode of operation. """

    reason = marshmallow_fields.Str(data_key="reason", allow_none=True)
    r""" Indicates the reason for the NDMP mover pause or halt. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Indicates the NDMP mover state. """

    @property
    def resource(self):
        return NdmpMover

    gettable_fields = [
        "bytes_moved",
        "connection",
        "mode",
        "reason",
        "state",
    ]
    """bytes_moved,connection,mode,reason,state,"""

    patchable_fields = [
        "bytes_moved",
        "connection",
        "mode",
        "reason",
        "state",
    ]
    """bytes_moved,connection,mode,reason,state,"""

    postable_fields = [
        "bytes_moved",
        "connection",
        "mode",
        "reason",
        "state",
    ]
    """bytes_moved,connection,mode,reason,state,"""


class NdmpMover(Resource):

    _schema = NdmpMoverSchema
