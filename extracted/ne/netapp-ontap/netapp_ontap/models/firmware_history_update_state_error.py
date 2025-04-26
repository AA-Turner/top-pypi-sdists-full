r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["FirmwareHistoryUpdateStateError", "FirmwareHistoryUpdateStateErrorSchema"]
__pdoc__ = {
    "FirmwareHistoryUpdateStateErrorSchema.resource": False,
    "FirmwareHistoryUpdateStateErrorSchema.opts": False,
    "FirmwareHistoryUpdateStateError": False,
}


class FirmwareHistoryUpdateStateErrorSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the FirmwareHistoryUpdateStateError object"""

    code = Size(data_key="code", allow_none=True)
    r""" Code corresponding to the status message.

Example: 2228325 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Error message returned when a firmware update job fails.

Example: Cannot open local staging ZIP file disk_firmware.zip """

    @property
    def resource(self):
        return FirmwareHistoryUpdateStateError

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    postable_fields = [
        "code",
        "message",
    ]
    """code,message,"""


class FirmwareHistoryUpdateStateError(Resource):

    _schema = FirmwareHistoryUpdateStateErrorSchema
