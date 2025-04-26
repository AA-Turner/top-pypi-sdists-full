r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["WebauthnCredentialsCredential", "WebauthnCredentialsCredentialSchema"]
__pdoc__ = {
    "WebauthnCredentialsCredentialSchema.resource": False,
    "WebauthnCredentialsCredentialSchema.opts": False,
    "WebauthnCredentialsCredential": False,
}


class WebauthnCredentialsCredentialSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WebauthnCredentialsCredential object"""

    id_sha = marshmallow_fields.Str(data_key="id_sha", allow_none=True)
    r""" SHA-256 Hashed representation of Credential ID.

Example: xxxxxxxxxxxxxxxxxxxxxxebfb30f20bf6db74xxxxxxxxxxxxxxxxxxxxxxxxxx """

    type = marshmallow_fields.Str(data_key="type", allow_none=True)
    r""" Credential type.

Valid choices:

* public_key """

    @property
    def resource(self):
        return WebauthnCredentialsCredential

    gettable_fields = [
        "id_sha",
        "type",
    ]
    """id_sha,type,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class WebauthnCredentialsCredential(Resource):

    _schema = WebauthnCredentialsCredentialSchema
