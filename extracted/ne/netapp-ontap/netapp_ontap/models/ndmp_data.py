r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NdmpData", "NdmpDataSchema"]
__pdoc__ = {
    "NdmpDataSchema.resource": False,
    "NdmpDataSchema.opts": False,
    "NdmpData": False,
}


class NdmpDataSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NdmpData object"""

    bytes_processed = Size(data_key="bytes_processed", allow_none=True)
    r""" Indicates the NDMP data bytes processed.

Example: 5000 """

    connection = marshmallow_fields.Nested("netapp_ontap.models.ndmp_connect.NdmpConnectSchema", unknown=EXCLUDE, data_key="connection", allow_none=True)
    r""" Indicates the NDMP connection attributes. """

    operation = marshmallow_fields.Str(data_key="operation", allow_none=True)
    r""" Indicates the NDMP data server operation.

Valid choices:

* backup
* restore
* none """

    reason = marshmallow_fields.Str(data_key="reason", allow_none=True)
    r""" Indicates the reason for the NDMP data server halt. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Indicates the state of the NDMP data server. """

    @property
    def resource(self):
        return NdmpData

    gettable_fields = [
        "bytes_processed",
        "connection",
        "operation",
        "reason",
        "state",
    ]
    """bytes_processed,connection,operation,reason,state,"""

    patchable_fields = [
        "bytes_processed",
        "connection",
        "operation",
        "reason",
        "state",
    ]
    """bytes_processed,connection,operation,reason,state,"""

    postable_fields = [
        "bytes_processed",
        "connection",
        "operation",
        "reason",
        "state",
    ]
    """bytes_processed,connection,operation,reason,state,"""


class NdmpData(Resource):

    _schema = NdmpDataSchema
