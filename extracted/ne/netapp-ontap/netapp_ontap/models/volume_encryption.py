r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VolumeEncryption", "VolumeEncryptionSchema"]
__pdoc__ = {
    "VolumeEncryptionSchema.resource": False,
    "VolumeEncryptionSchema.opts": False,
    "VolumeEncryption": False,
}


class VolumeEncryptionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VolumeEncryption object"""

    action = marshmallow_fields.Str(data_key="action", allow_none=True)
    r""" This field can be used to pause an ongoing rekey or conversion operation or resume a paused rekey or conversion operation. Valid in PATCH. The following actions are supported for this field:<br>conversion_pause &dash; Pause an encryption conversion operation currently in progress.<br>conversion_resume &dash; Resume a paused encryption conversion operation.<br>rekey_pause &dash; Pause an encryption rekey operation currently in progress.<br>rekey_resume &dash; Resume a paused encryption rekey operation.

Valid choices:

* conversion_pause
* conversion_resume
* rekey_pause
* rekey_resume """

    enabled = marshmallow_fields.Boolean(data_key="enabled", allow_none=True)
    r""" Creates an encrypted or an unencrypted volume. For POST, when set to 'true', a new key is generated and used to encrypt the given volume. In that case, the underlying SVM must be configured with the key manager. When set to 'false', the volume created will be unencrypted. For PATCH, when set to 'true', it encrypts an unencrypted volume. Specifying the parameter as 'false' in a PATCH operation for an encrypted volume is only supported when moving the volume to another aggregate. """

    key_create_time = ImpreciseDateTime(data_key="key_create_time", allow_none=True)
    r""" Encryption key creation time of the volume.

Example: 2022-01-01T19:00:00.000+0000 """

    key_id = marshmallow_fields.Str(data_key="key_id", allow_none=True)
    r""" The key ID used for creating encrypted volume. A new key-id is generated for creating an encrypted volume. This key-id is associated with the generated key. """

    key_manager_attribute = marshmallow_fields.Str(data_key="key_manager_attribute", allow_none=True)
    r""" Specifies an additional key manager attribute that is an identifier-value pair, separated by '='. For example, CRN=unique-value. This parameter is required when using the POST method and an IBM Key Lore key manager is configured on the SVM.

Example: CRN=v1:bluemix:public:containers-kubernetes:us-south:a/asdfghjkl1234:asdfghjkl1234:worker:kubernetes-asdfghjkl-worker1 """

    rekey = marshmallow_fields.Boolean(data_key="rekey", allow_none=True)
    r""" If set to 'true', re-encrypts the volume with a new key. Valid in PATCH. """

    state = marshmallow_fields.Str(data_key="state", allow_none=True)
    r""" Volume encryption state.<br>encrypted &dash; The volume is completely encrypted.<br>encrypting &dash; Encryption operation is in progress.<br>partial &dash; Some constituents are encrypted and some are not. Applicable only for FlexGroup volume.<br>rekeying. Encryption of volume with a new key is in progress.<br>unencrypted &dash; The volume is a plain-text one.

Valid choices:

* encrypted
* encrypting
* partial
* rekeying
* unencrypted """

    status = marshmallow_fields.Nested("netapp_ontap.models.volume_encryption_status.VolumeEncryptionStatusSchema", unknown=EXCLUDE, data_key="status", allow_none=True)
    r""" The status field of the volume_encryption. """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Volume encryption type.<br>none &dash; The volume is a plain-text one.<br>volume &dash; The volume is encrypted with NVE (NetApp Volume Encryption).<br>aggregate &dash; The volume is encrypted with NAE (NetApp Aggregate Encryption).

Valid choices:

* none
* volume
* aggregate """

    @property
    def resource(self):
        return VolumeEncryption

    gettable_fields = [
        "action",
        "enabled",
        "key_create_time",
        "key_id",
        "rekey",
        "state",
        "status",
        "type",
    ]
    """action,enabled,key_create_time,key_id,rekey,state,status,type,"""

    patchable_fields = [
        "action",
        "enabled",
        "rekey",
        "status",
    ]
    """action,enabled,rekey,status,"""

    postable_fields = [
        "action",
        "enabled",
        "key_manager_attribute",
        "status",
    ]
    """action,enabled,key_manager_attribute,status,"""


class VolumeEncryption(Resource):

    _schema = VolumeEncryptionSchema
