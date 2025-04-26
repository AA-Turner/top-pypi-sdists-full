r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeEncryptionStatus", "VolumeEncryptionStatusSchema"]
__pdoc__ = {
    "VolumeEncryptionStatusSchema.resource": False,
    "VolumeEncryptionStatusSchema.opts": False,
    "VolumeEncryptionStatus": False,
}


class VolumeEncryptionStatusSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeEncryptionStatus object"""

    code = marshmallow_fields.Str(data_key="code", allow_none=True)
    r""" Encryption progress message code. """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Encryption progress message. """

    @property
    def resource(self):
        return VolumeEncryptionStatus

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class VolumeEncryptionStatus(Resource):

    _schema = VolumeEncryptionStatusSchema
