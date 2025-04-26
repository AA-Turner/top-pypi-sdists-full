r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["StorageUnitEncryption", "StorageUnitEncryptionSchema"]
__pdoc__ = {
    "StorageUnitEncryptionSchema.resource": False,
    "StorageUnitEncryptionSchema.opts": False,
    "StorageUnitEncryption": False,
}


class StorageUnitEncryptionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the StorageUnitEncryption object"""

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Storage unit data encryption state.<br>_unencrypted_ &dash; Unencrypted.<br>_software_encrypted_ &dash; Software encryption enabled.<br>_software_conversion_queued_ &dash; Queued for software conversion.<br>_software_encrypting_ &dash; Software encryption is in progress.<br>_software_rekeying_ &dash; Encryption with a new key is in progress.<br>_software_conversion_paused_ &dash; Software conversion is paused.<br>_software_rekey_paused_ &dash; Encryption with a new key is paused.<br>_software_rekey_queued_ &dash; Queued for software rekey.


Valid choices:

* unencrypted
* software_encrypted
* software_conversion_queued
* software_encrypting
* software_rekeying
* software_conversion_paused
* software_rekey_paused
* software_rekey_queued """

    @property
    def resource(self):
        return StorageUnitEncryption

    gettable_fields = [
        "state",
    ]
    """state,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class StorageUnitEncryption(Resource):

    _schema = StorageUnitEncryptionSchema
