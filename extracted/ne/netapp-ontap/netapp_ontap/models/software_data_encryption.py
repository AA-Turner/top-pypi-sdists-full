r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SoftwareDataEncryption", "SoftwareDataEncryptionSchema"]
__pdoc__ = {
    "SoftwareDataEncryptionSchema.resource": False,
    "SoftwareDataEncryptionSchema.opts": False,
    "SoftwareDataEncryption": False,
}


class SoftwareDataEncryptionSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SoftwareDataEncryption object"""

    conversion_enabled = marshmallow_fields.Boolean(data_key="conversion_enabled", allow_none=True)
    r""" Indicates whether or not software encryption conversion is enabled on the cluster. A PATCH request initiates the conversion of all non-encrypted metadata volumes in the cluster to encrypted metadata volumes and all non-NAE aggregates to NAE aggregates. For the PATCH request to start, the cluster must have either an Onboard or an external key manager set up and the aggregates should either be empty or have only metadata volumes. No data volumes should be present in any of the aggregates in the cluster. For MetroCluster configurations, a PATCH request enables conversion on all the aggregates and metadata volumes of both local and remote clusters and is not allowed when the MetroCluster is in switchover state. """

    disabled_by_default = marshmallow_fields.Boolean(data_key="disabled_by_default", allow_none=True)
    r""" Indicates whether or not default software data at rest encryption is disabled on the cluster. """

    encryption_state = marshmallow_fields.Str(data_key="encryption_state", allow_none=True)
    r""" Software data encryption state.<br>encrypted &dash; All the volumes are encrypted.<br>encrypting &dash; Encryption conversion operation is in progress.<br>partial &dash; Some volumes are encrypted, and others remains in plain text.<br>rekeying &dash; All volumes are currently being encrypted with a new key.<br>unencrypted &dash; None of the volumes are encrypted.<br>conversion_paused &dash; Encryption conversion operation is paused on one or more volumes.<br>rekey_paused &dash; Encryption rekey operation is paused on one or more volumes.

Valid choices:

* encrypted
* encrypting
* partial
* rekeying
* unencrypted
* conversion_paused
* rekey_paused """

    rekey = marshmallow_fields.Boolean(data_key="rekey", allow_none=True)
    r""" The rekey field of the software_data_encryption. """

    @property
    def resource(self):
        return SoftwareDataEncryption

    gettable_fields = [
        "conversion_enabled",
        "disabled_by_default",
        "encryption_state",
    ]
    """conversion_enabled,disabled_by_default,encryption_state,"""

    patchable_fields = [
        "conversion_enabled",
        "disabled_by_default",
        "rekey",
    ]
    """conversion_enabled,disabled_by_default,rekey,"""

    postable_fields = [
    ]
    """"""


class SoftwareDataEncryption(Resource):

    _schema = SoftwareDataEncryptionSchema
