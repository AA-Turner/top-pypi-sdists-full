r"""
Copyright &copy; 2024 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields as marshmallow_fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["WebauthnCredentialsRelyingParty", "WebauthnCredentialsRelyingPartySchema"]
__pdoc__ = {
    "WebauthnCredentialsRelyingPartySchema.resource": False,
    "WebauthnCredentialsRelyingPartySchema.opts": False,
    "WebauthnCredentialsRelyingParty": False,
}


class WebauthnCredentialsRelyingPartySchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the WebauthnCredentialsRelyingParty object"""

    id = marshmallow_fields.Str(data_key="id", allow_none=True)
    r""" Relying Party ID.

Example: example.com """

    name = marshmallow_fields.Str(data_key="name", allow_none=True)
    r""" Relying Party Name.

Example: example.com """

    @property
    def resource(self):
        return WebauthnCredentialsRelyingParty

    gettable_fields = [
        "id",
        "name",
    ]
    """id,name,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class WebauthnCredentialsRelyingParty(Resource):

    _schema = WebauthnCredentialsRelyingPartySchema
