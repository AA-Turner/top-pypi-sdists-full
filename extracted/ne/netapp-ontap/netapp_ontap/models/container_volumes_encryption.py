r"""
Copyright &copy; 2026 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""
from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size, lazy_import_schema


__all__ = ["ContainerVolumesEncryption", "ContainerVolumesEncryptionSchema"]
__pdoc__ = {
    "ContainerVolumesEncryptionSchema.resource": False,
    "ContainerVolumesEncryptionSchema.opts": False,
    "ContainerVolumesEncryption": False,
}

class ContainerVolumesEncryptionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ContainerVolumesEncryption object"""

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Creates an encrypted or unencrypted volume. For POST requests, when set to 'true', a new key is generated and used to encrypt the specified volume. The underlying SVM must be configured with the key manager. When set to 'false', the volume created will be unencrypted.

Example: true """

    @property
    def resource(self):
        return ContainerVolumesEncryption

    gettable_fields = [
        "enabled",
    ]
    """enabled,"""

    patchable_fields = [
        "enabled",
    ]
    """enabled,"""

    postable_fields = [
        "enabled",
    ]
    """enabled,"""


class ContainerVolumesEncryption(Resource):

    _schema = ContainerVolumesEncryptionSchema
