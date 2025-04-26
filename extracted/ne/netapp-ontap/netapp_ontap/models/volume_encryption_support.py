r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeEncryptionSupport", "VolumeEncryptionSupportSchema"]
__pdoc__ = {
    "VolumeEncryptionSupportSchema.resource": False,
    "VolumeEncryptionSupportSchema.opts": False,
    "VolumeEncryptionSupport": False,
}


class VolumeEncryptionSupportSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeEncryptionSupport object"""

    code = Size(data_key="code", allow_none=True)
    r""" Code corresponding to the status message. Returns a 0 if volume encryption is supported in all nodes of the cluster.

Example: 346758 """

    message = marshmallow_fields.Str(data_key="message", allow_none=True)
    r""" Reason for not supporting volume encryption.

Example: No platform support for volume encryption in following nodes - node1, node2. """

    supported = marshmallow_fields.Boolean(data_key="supported", allow_none=True)
    r""" Set to true when volume encryption support is available on all nodes of the cluster. """

    @property
    def resource(self):
        return VolumeEncryptionSupport

    gettable_fields = [
        "code",
        "message",
        "supported",
    ]
    """code,message,supported,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class VolumeEncryptionSupport(Resource):

    _schema = VolumeEncryptionSupportSchema
