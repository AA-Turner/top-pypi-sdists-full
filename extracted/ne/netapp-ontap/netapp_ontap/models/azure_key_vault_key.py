r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AzureKeyVaultKey", "AzureKeyVaultKeySchema"]
__pdoc__ = {
    "AzureKeyVaultKeySchema.resource": False,
    "AzureKeyVaultKeySchema.opts": False,
    "AzureKeyVaultKey": False,
}


class AzureKeyVaultKeySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AzureKeyVaultKey object"""

    key_id = marshmallow_fields.Str(data_key="key_id", allow_none=True)
    r""" Key identifier of the AKV key encryption key.

Example: https://keyvault1.vault.azure.net/keys/key1/12345678901234567890123456789012 """

    @property
    def resource(self):
        return AzureKeyVaultKey

    gettable_fields = [
        "key_id",
    ]
    """key_id,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "key_id",
    ]
    """key_id,"""


class AzureKeyVaultKey(Resource):

    _schema = AzureKeyVaultKeySchema
